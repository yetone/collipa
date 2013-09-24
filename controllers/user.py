# coding: utf-8

import time
import random
import hashlib
import base64
import tornado.web
import os
import sys
import logging
import tempfile
import Image

import config
from ._base import BaseHandler
from pony.orm import *

from models import User, MessageBox, Message
from .api import WebSocketHandler
from forms import SignupForm, SigninForm, MessageForm, SettingForm
from extensions import mc, rd
from helpers import force_int, get_year, get_month

config = config.rec()

class EmailMixin(object):

    def _create_token(self, user):
        salt = user.create_token(8)
        created = str(int(time.time()))
        hsh = hashlib.sha1(salt + created + user.token).hexdigest()
        token = "%s|%s|%s|%s" % (user.email, salt, created, hsh)
        return base64.b64encode(token)

    @db_session
    def _verify_token(self, token):
        try:
            token = base64.b64decode(token)
        except:
            result = {"status": "error", "message": "验证链接错误"}
            self.flash_message(result)
            return None
        splits = token.split('|')
        if len(splits) != 4:
            result = {"status": "error", "message": "验证链接错误"}
            self.flash_message(result)
            return None
        email, salt, created, hsh = splits
        delta = time.time() - int(created)
        if delta < 1:
            result = {"status": "error", "message": "验证链接错误"}
            self.flash_message(result)
            return None
        if delta > 3600:
            # 1 hour
            result = {"status": "info", "message":
                    "此验证链接已过期，请再次验证"}
            self.flash_message(result)
            return None
        user = User.get(email=email)
        if not user:
            return None
        if hsh == hashlib.sha1(salt + created + user.token).hexdigest():
            return user
        self.flash_message("验证链接错误", 'error')
        return None

    def send_email(self, this, email, subject, content):
        from libs.tornadomail.message import EmailMessage
        message = EmailMessage(subject, content, config.smtp_user,
                [email], connection=self.mail_connection)
        message.send()

class HomeHandler(BaseHandler):
    @db_session
    def get(self, urlname, view='index', category='all'):
        page = force_int(self.get_argument('page', 1), 1)
        user = User.get(urlname=urlname)
        if not user:
            raise tornado.web.HTTPError(404)
        action = self.get_argument('action', None)
        if action and self.current_user:
            if action == 'follow' and user != self.current_user:
                result = self.current_user.follow(whom_id=user.id)
                if self.is_ajax:
                    return self.write(result)
                else:
                    self.flash_message(result)
                    return self.redirect_next_url()
        items = []
        item_count = 0
        url = user.url
        if view == 'topics':
            items = user.get_topics(page=page, category=category)
            item_count = count(user.get_topics(page=None, category=category))
            url = url + '/topics'
        elif view == 'replies':
            items = user.get_replies(page=page, category=category)
            item_count = count(user.get_replies(page=None, category=category))
            url = url + '/replies'
        elif view == 'followings':
            items = user.get_followings(page=page)
            item_count = count(user.get_followings(page=None))
            url = url + '/followings'
        elif view == 'followers':
            items = user.get_followers(page=page)
            item_count = count(user.get_followers(page=None))
            url = url + '/followers'
        page_count = (item_count + config.paged - 1) // config.paged
        return self.render("user/index.html", user=user, items=items, view=view,
                category=category, page=page, page_count=page_count, url=url)

class SignupHandler(BaseHandler, EmailMixin):
    @db_session
    def get(self):
        token = self.get_argument('verify', None)
        if token:
            user = self._verify_token(token)
            if user:
                user.role = 'user'
                try:
                    commit()
                except:
                    pass
                result = {'status': 'success', 'message': '您的账户已经激活'}
                self.flash_message(result)
            return self.redirect('/account/setting')
        if self.current_user:
            return self.redirect_next_url()

        form = SignupForm()
        return self.render("user/signup.html", form=form)

    @db_session
    def post(self):
        if self.current_user and self.get_argument("action", '') == 'email':
            if self.current_user.role != 'unverify':
                result = {'status': 'success', 'message': '您的账户已经激活'}
                self.flash_message(result)
            else:
                self.send_register_email(self.current_user)
                return self.redirect("/account/setting")
        if self.current_user:
            return self.redirect_next_url()

        form = SignupForm(self.request.arguments)
        if form.validate():
            user = form.save()
            self.set_current_user(user)
            self.send_register_email(user)
            return self.redirect_next_url()
        return self.render("user/signup.html", form=form)

    def send_register_email(self, user):
        token = self._create_token(user)
        url = '%s/signup?verify=%s' % \
                (config.site_url, token)

        subject = "帐号激活 - " + config.site_name
        template = (
            '<p>尊敬的 <strong>%(email)s</strong> 您好！</p>'
            '<p>您的账户尚未激活，请点击此链接：'
            '<a href="%(url)s">点我激活</a>.</p>'
            '<p>如果您的浏览器不能点击此链接，'
            '请复制下面的链接然后粘贴在浏览器的地址栏里进行激活：</p>'
            '<p>%(url)s</p>'
        ) % {'email': user.name, 'url': url}
        self.send_email(self, user.email, subject, template)
        result = {'status': 'info', 'message':
                '激活邮件已经发到您的邮箱，请去邮箱进行激活'}
        self.flash_message(result)

class SigninHandler(BaseHandler):
    def get(self):
        form = SigninForm()
        return self.render("user/signin.html", form=form)

    @db_session
    def post(self):
        form = SigninForm(self.request.arguments)
        if form.validate():
            self.set_current_user(form.user)
            return self.redirect(self.next_url)
        return self.render("user/signin.html", form=form)

class SignoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        return self.redirect(self.next_url)

class NotificationHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    def get(self):
        page = force_int(self.get_argument('page', 1), 1)
        category = self.get_argument('category', 'all')
        self.render("user/notification.html",
                category=category, page=page)
        self.current_user.read_notifications()
        return

class MessageHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    def get(self):
        page = force_int(self.get_argument('page', 1), 1)
        user_id = force_int(self.get_argument('user_id', 0), 0)
        current_user = self.current_user
        user = User.get(id=user_id)
        if user:
            message_box = current_user.get_message_box(user=user)
            if not message_box:
                result = {"status": "error", "message": "无此私信"}
                if self.is_ajax:
                    return self.write(result)
                self.flash_message(result)
                return self.redirect_next_url()
            form = MessageForm()
            self.render("user/message.html", user=user, message_box=message_box,
                    form=form, page=page)
            if message_box.status == 0:
                message_box.status = 1
                try:
                    commit()
                except:
                    pass
            return
        category = self.get_argument('category', 'all')
        return self.render("user/message_box.html", category=category, page=page)

class MessageCreateHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    def post(self):
        user_id = force_int(self.get_argument('user_id', 0), 0)
        sender = self.current_user
        receiver = User.get(id=user_id)
        if receiver:
            form = MessageForm(self.request.arguments)
            if form.validate():
                """
                message_box1 = current_user.get_message_box(user=user)
                message_box2 = user.get_message_box(user=current_user)
                if not message_box1:
                    message_box1 = MessageBox(sender_id=current_user.id,
                            receiver_id=user.id, status=1).save()
                if not message_box2:
                    message_box2 = MessageBox(sender_id=user.id,
                            receiver_id=current_user.id).save()
                """
                message = form.save(sender_id=sender.id,
                                    receiver_id=receiver.id)
                result = {"status": "success", "message": "私信发送成功",
                        "content": message.content, "created": message.created,
                        "avatar": sender.get_avatar(size=48), "url":
                        sender.url, "id": message.id}
            else:
                result = {"status": "error", "message": "请填写至少 4 字的内容"}
            if self.is_ajax:
                self.write(result)
            else:
                self.flash_message(result)
                self.redirect_next_url()
            self.finish()
            WebSocketHandler.send_message(message.receiver_id, message)
            return
        result = {"status": "error", "message": "没有目标用户，不能发送私信哦"}
        if self.is_ajax:
            return self.write(result)
        self.flash_message(result)
        return self.redirect_next_url()

class ApiGetUserNameHandler(BaseHandler):
    @db_session
    def get(self):
        users = User.select()
        user_json = []
        for user in users:
            user_json.append({"value": user.name, "label": user.nickname})
        return self.write(user_json)

class PasswordHandler(BaseHandler, EmailMixin):
    """Password

    - GET: 1. form view 2. verify link from email
    - POST: 1. send email to find password. 2. change password
    """
    @db_session
    def get(self):
        token = self.get_argument('verify', None)
        if token and self._verify_token(token):
            return self.render('user/password.html', token=token)

        if not self.current_user:
            return self.redirect('/signin')
        return self.render('user/password.html', token=None)

    @db_session
    def post(self):
        action = self.get_argument('action', None)
        if action == 'email':
            self.send_password_email()
            if not self._finished:
                self.redirect('/account/setting')
            return
        password = self.get_argument('password', None)
        if password:
            return self.change_password()
        self.find_password()

    @db_session
    def send_password_email(self):
        email = self.get_argument('email', None)
        if self.current_user:
            user = self.current_user
        elif not email:
            result = {"status": "error", "message": "请输入邮箱地址"}
            self.flash_message(result)
            return self.redirect('/signin')
        else:
            user = User.get(email=email)
            if not user:
                result = {"status": "error", "message": "用户不存在"}
                self.flash_message(result)
                return self.redirect('/signin')

        token = self._create_token(user)
        url = '%s/account/password?verify=%s' % \
                (config.site_url, token)

        template = (
            '<div>你好 <strong>%(nickname)s</strong></div>'
            '<br /><div>请点击下面的链接来找回你的密码： '
            '<a href="%(url)s">this link</a>.<div><br />'
            "<div>如果你的浏览器不能点击上面的链接 "
            '把下面的链接地址粘贴复制到你的浏览器地址栏: <br />'
            '%(url)s </div>'
        ) % {'nickname': user.nickname, 'url': url}
        result = {"status": "success", "message": "邮件已经发送，请检查您的邮箱"}
        self.flash_message(result)
        self.send_email(self, user.email, '找回密码', template)

    @db_session
    @tornado.web.authenticated
    def change_password(self):
        user = User.get(id=self.current_user.id)
        password = self.get_argument('password', None)
        if not user.check_password(password):
            result = {"status": "error", "message": "旧密码有误"}
            self.flash_message(result)
            return self.render('user/password.html', token=None)
        password1 = self.get_argument('password1', None)
        password2 = self.get_argument('password2', None)
        self._change_password(user, password1, password2)

    def find_password(self):
        token = self.get_argument('token', None)
        if not token:
            return self.redirect('/account/password')
        user = self._verify_token(token)
        if not user:
            return self.redirect('/account/password')
        password1 = self.get_argument('password1', None)
        password2 = self.get_argument('password2', None)
        self._change_password(user, password1, password2)

    @db_session
    def _change_password(self, user, password1, password2):
        if password1 != password2:
            token = self.get_argument('verify', None)
            result = {"status": "error", "message": "两次输入的密码不匹配"}
            self.flash_message(result)
            return self.render('user/password.html', token=token)
        if not password1:
            token = self.get_argument('verify', None)
            result = {"status": "error", "message": "新密码不能为空"}
            self.flash_message(result)
            return self.render('user/password.html', token=token)
        user.password = user.create_password(password1)
        user.token = user.create_token(16)
        try:
            commit()
        except:
            pass
        result = {"status": "success", "message": "密码已修改"}
        self.flash_message(result)
        self.set_current_user(user)
        return self.redirect('/account/password')

class FindPasswordHandler(BaseHandler):

    @db_session
    def get(self):
        if self.current_user:
            return self.redirect_next_url()
        return self.render("user/findpassword.html")

class SettingHandler(BaseHandler):

    @db_session
    @tornado.web.authenticated
    def get(self):
        user = self.current_user
        form = SettingForm.init(user)
        return self.render("user/setting.html", form=form)

    @db_session
    @tornado.web.authenticated
    def post(self):
        user = self.current_user
        form = SettingForm.init(user=user, args=self.request.arguments)
        if form.validate():
            user = form.save(user)
            return self.redirect_next_url()
        return self.render("user/setting.html", form=form)

class AvatarDelHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    def get(self):
        user = self.current_user
        if user.avatar:
            try:
                os.system('rm -f %s%s*' % (sys.path[0],
                    user.avatar[:user.avatar.rfind('x')]))
            except:
                pass
            user.avatar = None
            try:
                commit()
            except:
                pass
        self.redirect(self.next_url)

class AvatarUploadHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    def get(self):
        self.render("user/avatar_upload.html")
        return

    @db_session
    def post(self):
        if self.request.files == {} or 'myavatar' not in self.request.files:
            self.write({"status": "error",
                "message": "请选择图片！"})
            return
        image_type_list = ['image/gif', 'image/jpeg', 'image/pjpeg',
                'image/png', 'image/bmp', 'image/x-png']
        send_file = self.request.files['myavatar'][0]
        if send_file['content_type'] not in image_type_list:
            self.write({"status": "error",
                "message": "仅支持 jpg, jpeg, bmp, gif, png\
                    格式的图片！"})
            return
        if len(send_file['body']) > 100 * 1024 * 1024:
            self.write({"status": "error",
                "message": "请上传100M以下的图片！"})
            return
        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        tmp_file.write(send_file['body'])
        tmp_file.seek(0)
        try:
            image_one = Image.open(tmp_file.name)
        except IOError, error:
            logging.info(error)
            logging.info('+' * 30 + '\n')
            logging.info(self.request.headers)
            tmp_file.close()
            self.write({"status": "error",
                "message": "图片不合法！"})
            return
        width = image_one.size[0]
        height = image_one.size[1]
        if width < 24 or height < 24 or width > 20000 or height > 20000:
            tmp_file.close()
            self.write({"status": "error",
                "message": "图片长宽在24px~20000px之间！"})
            return
        timestamp = str(int(time.time()))
        user = self.current_user
        upload_path = sys.path[0] + "/static/upload/avatar/"
        if user:
            timestamp += '_' + str(user.id)
        else:
            timestamp += '_' + ('').join(random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba', 6))
        if not os.path.exists(upload_path):
            try:
                os.system('mkdir -p %s' % upload_path)
            except:
                pass
        image_format = send_file['filename'].split('.').pop().lower()
        tmp_name = upload_path + timestamp + '.' + image_format
        if os.path.exists(tmp_name):
            while True:
                if os.path.exists(tmp_name):
                    timestamp += '_' + ('').join(random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba', 6))
                    tmp_name = upload_path + timestamp + '.' + image_format
                else:
                    break
        image_one.save(tmp_name)
        tmp_file.close()
        if user:
            user.avatar_tmp = '/' +\
                '/'.join(tmp_name.split('/')[tmp_name.split('/').index("static"):])
            src = user.avatar_tmp
        else:
            src = '/' +\
                '/'.join(tmp_name.split('/')[tmp_name.split('/').index("static"):])
        if self.is_ajax:
            print(src)
        return self.write({"status": "success", "message": "成功上传头像", "src":
            src, "height": height, "width": width})

class AvatarCropHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    def get(self):
        if not self.current_user.avatar_tmp:
            result = {"status": "error", "message": "您还没有上传头像哦"}
            if self.is_ajax:
                return self.write(result)
            self.flash_message(result)
            return self.redirect_next_url()
        return self.render("user/avatar_crop.html")

    @db_session
    @tornado.web.authenticated
    def post(self):
        user = self.current_user
        x = int(self.get_argument('x', 0))
        y = int(self.get_argument('y', 0))
        w = int(self.get_argument('w', 128))
        h = int(self.get_argument('h', 128))
        avatar = sys.path[0] + user.avatar_tmp
        image_one = Image.open(avatar)
        box = (x, y, x + w, y + h)
        image_crop = image_one.crop(box)
        image_two = image_crop.resize((48, 48), Image.ANTIALIAS)
        image_three = image_crop.resize((60, 60), Image.ANTIALIAS)
        image_four = image_crop.resize((128, 128), Image.ANTIALIAS)

        image_format = avatar[avatar.rfind('.'):]
        save_path = avatar[: avatar.rfind('.')]
        tmp_name_crop = save_path + '_crop' + image_format
        tmp_name2 = save_path + 'x48' + image_format
        tmp_name3 = save_path + 'x60' + image_format
        tmp_name4 = save_path + 'x128' + image_format
        image_crop.save(tmp_name_crop)
        image_two.save(tmp_name2)
        image_three.save(tmp_name3)
        image_four.save(tmp_name4)
        if user.avatar:
            try:
                os.system('rm -f %s%s*' %
                    (sys.path[0],
                        user.avatar[:user.avatar.rfind('.')]))
            except:
                pass
        user.avatar = user.avatar_tmp
        try:
            commit()
        except:
            pass
        src = self.current_user.avatar_tmp
        avatar = self.current_user.get_avatar(size=128)
        result = {"status": "success", "message": "头像设置成功", "src": src,
                "avatar": avatar}
        if self.is_ajax:
            return self.write(result)
        self.flash_message(result)
        return self.redirect_next_url()

class BackgroundDelHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    def get(self):
        try:
            os.system('rm -f %s%s' % (sys.path[0],
                self.current_user.background_img))
        except:
            pass
        self.current_user.background_img = ''
        try:
            commit()
        except:
            pass
        result = {"status": "success", "message": "已成功重置背景图片"}
        if self.is_ajax:
            return self.write(result)
        self.flash_message(result)
        return self.redirect_next_url()

class ImgUploadHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    def post(self):
        if not self.has_permission:
            return
        user = self.current_user
        if not user:
            return self.redirect_next_url()
        if self.request.files == {} or 'myimage' not in self.request.files:
            self.write({"status": "error",
                "message": "对不起，请选择图片"})
            return
        image_type_list = ['image/gif', 'image/jpeg', 'image/pjpeg',
                'image/png', 'image/bmp', 'image/x-png']
        send_file = self.request.files['myimage'][0]
        if send_file['content_type'] not in image_type_list:
            self.write({"status": "error",
                "message": "对不起，仅支持 jpg, jpeg, bmp, gif, png\
                    格式的图片"})
            return
        if len(send_file['body']) > 6 * 1024 * 1024:
            self.write({"status": "error",
                "message": "对不起，请上传6M以下的图片"})
            return
        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        tmp_file.write(send_file['body'])
        tmp_file.seek(0)
        try:
            image_one = Image.open(tmp_file.name)
        except IOError, error:
            logging.info(error)
            logging.info('+' * 30 + '\n')
            logging.info(self.request.headers)
            tmp_file.close()
            self.write({"status": "error",
                "message": "对不起，此文件不是图片"})
            return
        width = image_one.size[0]
        height = image_one.size[1]
        if width < 80 or height < 80 or width > 30000 or height > 30000:
            tmp_file.close()
            self.write({"status": "error",
                "message": "对不起，请上传长宽在80px~30000px之间的图片！"})
            return
        user = self.current_user
        upload_path = sys.path[0] + "/static/upload/" + get_year() + '/' +\
            get_month() + "/"
        if not os.path.exists(upload_path):
            try:
                os.system('mkdir -p %s' % upload_path)
            except:
                pass
        timestamp = str(int(time.time())) +\
            ('').join(random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba',
                6)) + '_' + str(user.id)
        image_format = send_file['filename'].split('.').pop().lower()
        tmp_name = upload_path + timestamp + '.' + image_format
        image_one.save(tmp_name)
        tmp_file.close()
        path = '/' +\
            '/'.join(tmp_name.split('/')[tmp_name.split('/').index("static"):])
        category = self.get_argument('category', None)
        print category
        del_path = None
        if category == 'head':
            del_path = user.head_img
            user.head_img = path
            result = {'path': path, 'status': "success", 'message':
                    '头部背景设置成功', 'category': 'head'}
        elif category == 'background':
            del_path = user.background_img
            user.background_img = path
            result = {'path': path, 'status': "success", 'message':
                    '背景设置成功', 'category': 'background'}
        else:
            result = {'path': path, 'status': "success", 'message':
                '图片上传成功'}
        if del_path:
            try:
                os.system('rm -f %s%s' % (sys.path[0],
                    del_path))
            except:
                pass
        if self.is_ajax:
            return self.write(result)
        return

class ShowHandler(BaseHandler):
    @db_session
    def get(self):
        page = force_int(self.get_argument('page', 1), 1)
        category = self.get_argument('category', None)
        limit = 12
        hot_users = User.get_users(category='hot', limit=limit)
        new_users = User.get_users(category='new', limit=limit)
        page_count = 0
        users = []
        url = '/users'
        if category == 'all':
            user_count = count(User.get_users(page=None))
            page_count = (user_count + config.user_paged - 1) // config.user_paged
            users = User.get_users(page=page)
            url = '/users?category=all'
        elif category == 'online':
            users = set()
            online = rd.smembers("online") or [0]
            online = [int(i) for i in online]
            users = User.select(lambda rv: rv.id in online)
            print users
            user_count = len(users)
            page_count = (user_count + config.user_paged - 1) // config.user_paged
            url = '/users?category=online'
        return self.render("user/show.html", users=users, hot_users=hot_users,
                new_users=new_users, page=page,
                page_count=page_count, url=url, category=category)
