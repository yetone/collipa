# coding: utf-8

import time
import hashlib
import base64
import tornado.web
import os
import logging
import tempfile
from pony import orm

from .api import WebSocketHandler
from ._base import BaseHandler

from collipa.models import User
from collipa.forms import SignupForm, SigninForm, MessageForm, SettingForm
from collipa.extensions import rd
from collipa.helpers import (
    force_int,
    get_year,
    get_month,
    gen_random_str,
    get_asset_path,
    mkdir_p,
    get_relative_path,
    remove_file,
)
from collipa.libs.pil import Image
from collipa import config


class EmailMixin(object):
    def _create_token(self, user):
        salt = user.create_token(8)
        created = str(int(time.time()))
        hsh = hashlib.sha1(salt + created + user.token).hexdigest()
        token = "%s|%s|%s|%s" % (user.email, salt, created, hsh)
        return base64.b64encode(token)

    @orm.db_session
    def _verify_token(self, token):
        try:
            token = base64.b64decode(token)
        except:
            result = {"status": "error", "message": "验证链接错误"}
            self.flash_message(**result)
            return None
        splits = token.split('|')
        if len(splits) != 4:
            result = {"status": "error", "message": "验证链接错误"}
            self.flash_message(**result)
            return None
        email, salt, created, hsh = splits
        delta = time.time() - int(created)
        if delta < 1:
            result = {"status": "error", "message": "验证链接错误"}
            self.flash_message(**result)
            return None
        if delta > 3600:
            # 1 hour
            result = {"status": "info", "message": "此验证链接已过期，请再次验证"}
            self.flash_message(**result)
            return None
        user = User.get(email=email)
        if not user:
            return None
        if hsh == hashlib.sha1(salt + created + user.token).hexdigest():
            return user
        result = {"status": "error", "message": "验证链接错误"}
        self.flash_message(**result)
        return None

    def send_email(self, this, email, subject, content):
        from collipa.libs.tornadomail.message import EmailMessage
        message = EmailMessage(subject, content, config.smtp_user,
                               [email], connection=self.mail_connection)
        message.send()


class HomeHandler(BaseHandler):
    @orm.db_session
    def get(self, urlname, view='index', category='all'):
        page = force_int(self.get_argument('page', 1), 1)
        user = User.get(urlname=urlname)
        if not user:
            raise tornado.web.HTTPError(404)
        action = self.get_argument('action', None)
        if action and self.current_user:
            if action == 'follow' and user != self.current_user:
                result = self.current_user.follow(whom_id=user.id)
                return self.send_result(result)
        items = []
        item_count = 0
        url = user.url
        if view == 'topics':
            items = user.get_topics(page=page, category=category)
            item_count = orm.count(user.get_topics(page=None, category=category))
            url += '/topics'
        elif view == 'replies':
            items = user.get_replies(page=page, category=category)
            item_count = orm.count(user.get_replies(page=None, category=category))
            url += '/replies'
        elif view == 'followings':
            items = user.get_followings(page=page)
            item_count = orm.count(user.get_followings(page=None))
            url += '/followings'
        elif view == 'followers':
            items = user.get_followers(page=page)
            item_count = orm.count(user.get_followers(page=None))
            url += '/followers'
        elif view == 'albums':
            items = user.get_albums(page=page)
            item_count = orm.count(user.get_albums(page=None))
            url += '/albums'
        page_count = (item_count + config.paged - 1) // config.paged
        return self.render("user/index.html", user=user, items=items,
                           view=view, category=category, page=page,
                           page_count=page_count, url=url)


class SignupHandler(BaseHandler, EmailMixin):
    @orm.db_session
    def get(self):
        token = self.get_argument('verify', None)
        if token:
            user = self._verify_token(token)
            if user:
                user.role = 'user'
                try:
                    orm.commit()
                except:
                    pass
                result = {'status': 'success', 'message': '您的账户已经激活'}
                self.flash_message(**result)
            return self.redirect('/account/setting')
        if self.current_user:
            return self.redirect_next_url()

        form = SignupForm()
        return self.render("user/signup.html", form=form)

    @orm.db_session
    def post(self):
        if self.current_user and self.get_argument("action", '') == 'email':
            if self.current_user.role != 'unverify':
                result = {'status': 'success', 'message': '您的账户已经激活'}
                self.flash_message(**result)
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
        url = '%s/signup?verify=%s' % (config.site_url, token)

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
        self.flash_message(**result)


class SigninHandler(BaseHandler):
    def get(self):
        form = SigninForm()
        return self.render("user/signin.html", form=form)

    @orm.db_session
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
    @orm.db_session
    @tornado.web.authenticated
    def get(self):
        page = force_int(self.get_argument('page', 1), 1)
        category = self.get_argument('category', 'all')
        self.render("user/notification.html",
                    category=category, page=page)
        return self.current_user.read_notifications()


class MessageHandler(BaseHandler):
    @orm.db_session
    @tornado.web.authenticated
    def get(self):
        page = force_int(self.get_argument('page', 1), 1)
        user_id = force_int(self.get_argument('user_id', 0), 0)
        action = self.get_argument('action', None)
        current_user = self.current_user
        user = User.get(id=user_id)
        if not user:
            category = self.get_argument('category', 'all')
            return self.render("user/message_box.html",
                               category=category, page=page)
        message_box = current_user.get_message_box(user=user)
        if action == "read":
            message_box.status = 1
            return self.write({"status": "success", "message": "已读"})
        if not message_box:
            result = {"status": "error", "message": "无此私信"}
            return self.send_result(result)
        form = MessageForm()
        self.render("user/message.html", user=user, message_box=message_box,
                    form=form, page=page)
        if message_box.status == 0:
            message_box.status = 1
            try:
                orm.commit()
            except:
                pass


class MessageCreateHandler(BaseHandler):
    @orm.db_session
    @tornado.web.authenticated
    def post(self):
        user_id = force_int(self.get_argument('user_id', 0), 0)
        sender = self.current_user
        receiver = User.get(id=user_id)
        if receiver:
            form = MessageForm(self.request.arguments)
            if form.validate():
                message = form.save(sender_id=sender.id,
                                    receiver_id=receiver.id)
                result = {
                    "status": "success",
                    "message": "私信发送成功",
                    "content": message.content,
                    "created": message.created,
                    "avatar": sender.get_avatar(size=48),
                    "url": sender.url,
                    "id": message.id,
                }
            else:
                result = {"status": "error", "message": "请填写至少 4 字的内容"}
            self.send_result(result)
            self.finish()
            return WebSocketHandler.send_message(message.receiver_id, message)
        result = {"status": "error", "message": "没有目标用户，不能发送私信哦"}
        self.send_result(result)


class ApiGetUserNameHandler(BaseHandler):
    @orm.db_session
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
    @orm.db_session
    def get(self):
        token = self.get_argument('verify', None)
        if token and self._verify_token(token):
            return self.render('user/password.html', token=token)

        if not self.current_user:
            return self.redirect('/signin')
        return self.render('user/password.html', token=None)

    @orm.db_session
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

    @orm.db_session
    def send_password_email(self):
        email = self.get_argument('email', None)
        if self.current_user:
            user = self.current_user
        elif not email:
            result = {"status": "error", "message": "请输入邮箱地址"}
            self.flash_message(**result)
            return self.redirect('/signin')
        else:
            user = User.get(email=email)
            if not user:
                result = {"status": "error", "message": "用户不存在"}
                self.flash_message(**result)
                return self.redirect('/signin')

        token = self._create_token(user)
        url = '%s/account/password?verify=%s' % (config.site_url, token)

        template = (
            '<div>你好 <strong>%(nickname)s</strong></div>'
            '<br /><div>请点击下面的链接来找回你的密码： '
            '<a href="%(url)s">this link</a>.<div><br />'
            "<div>如果你的浏览器不能点击上面的链接 "
            '把下面的链接地址粘贴复制到你的浏览器地址栏: <br />'
            '%(url)s </div>'
        ) % {'nickname': user.nickname, 'url': url}
        result = {"status": "success", "message": "邮件已经发送，请检查您的邮箱"}
        self.flash_message(**result)
        self.send_email(self, user.email, '找回密码', template)

    @orm.db_session
    @tornado.web.authenticated
    def change_password(self):
        user = User.get(id=self.current_user.id)
        password = self.get_argument('password', None)
        if not user.check_password(password):
            result = {"status": "error", "message": "旧密码有误"}
            self.flash_message(**result)
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

    @orm.db_session
    def _change_password(self, user, password1, password2):
        if password1 != password2:
            token = self.get_argument('verify', None)
            result = {"status": "error", "message": "两次输入的密码不匹配"}
            self.flash_message(**result)
            return self.render('user/password.html', token=token)
        if not password1:
            token = self.get_argument('verify', None)
            result = {"status": "error", "message": "新密码不能为空"}
            self.flash_message(**result)
            return self.render('user/password.html', token=token)
        user.password = user.create_password(password1)
        user.token = user.create_token(16)
        try:
            orm.commit()
        except:
            pass
        result = {"status": "success", "message": "密码已修改"}
        self.flash_message(**result)
        self.set_current_user(user)
        return self.redirect('/account/password')


class FindPasswordHandler(BaseHandler):
    @orm.db_session
    def get(self):
        if self.current_user:
            return self.redirect_next_url()
        return self.render("user/findpassword.html")


class SettingHandler(BaseHandler):
    @orm.db_session
    @tornado.web.authenticated
    def get(self):
        user = self.current_user
        form = SettingForm.init(user)
        return self.render("user/setting.html", form=form)

    @orm.db_session
    @tornado.web.authenticated
    def post(self):
        user = self.current_user
        form = SettingForm.init(user=user, **self.request.arguments)
        if form.validate():
            form.save(user)
            return self.redirect_next_url()
        return self.render("user/setting.html", form=form)

    @orm.db_session
    @tornado.web.authenticated
    def delete(self):
        action = self.get_argument("action", None)
        if not action:
            return
        result = {}
        if action == 'reset_head':
            self.current_user.reset_img('head')
            result = {"status": "success", "message": "头部背景已重置"}
        elif action == 'reset_bg':
            self.current_user.reset_img('background')
            result = {"status": "success", "message": "背景已重置"}
        return self.send_result(result, '/account/setting')


class AvatarDelHandler(BaseHandler):
    @orm.db_session
    @tornado.web.authenticated
    def get(self):
        user = self.current_user
        if user.avatar:
            try:
                os.system('rm -f %s*' % get_asset_path(user.avatar[:user.avatar.rfind('x')]))
            except:
                pass
            user.avatar = None
        self.redirect(self.next_url)


class AvatarUploadHandler(BaseHandler):
    @orm.db_session
    @tornado.web.authenticated
    def get(self):
        self.render("user/avatar_upload.html")

    @orm.db_session
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
        except IOError as error:
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
        upload_path = os.path.join(config.upload_path, 'avatar')
        mkdir_p(upload_path)
        if user:
            timestamp += '_' + str(user.id)
        else:
            timestamp += '_' + gen_random_str()
        image_format = send_file['filename'].split('.').pop().lower()
        filename = timestamp + '.' + image_format
        tmp_path = os.path.join(upload_path, filename)
        if os.path.exists(tmp_path):
            while True:
                if os.path.exists(tmp_path):
                    timestamp += '_' + gen_random_str()
                    filename = timestamp + '.' + image_format
                    tmp_path = os.path.join(upload_path, filename)
                else:
                    break
        image_one.save(tmp_path)
        tmp_file.close()
        src = '/' + get_relative_path(tmp_path)
        if user:
            user.avatar_tmp = src
        data = {"src": src, "height": height, "width": width}
        return self.send_success_result(msg=u'成功上传头像', data=data)


class AvatarCropHandler(BaseHandler):
    @orm.db_session
    @tornado.web.authenticated
    def get(self):
        if not self.current_user.avatar_tmp:
            result = {"status": "error", "message": "您还没有上传头像哦"}
            return self.send_result(result)
        return self.render("user/avatar_crop.html")

    @orm.db_session
    @tornado.web.authenticated
    def post(self):
        user = self.current_user
        x = int(self.get_argument('x', 0))
        y = int(self.get_argument('y', 0))
        w = int(self.get_argument('w', 128))
        h = int(self.get_argument('h', 128))

        box = (x, y, x + w, y + h)
        avatar = get_asset_path(user.avatar_tmp)

        image_format = avatar[avatar.rfind('.'):]
        save_path = avatar[:avatar.rfind('.')]

        image = Image.open(avatar).crop(box)
        tmp_name = save_path + '_crop' + image_format
        image.save(tmp_name)

        size_set = ((48, 48), (60, 60), (128, 128))
        for size in size_set:
            image = Image.open(avatar).crop(box).resize(size, Image.ANTIALIAS)
            tmp_name = '%sx%d%s' % (save_path, size[0], image_format)
            image.save(tmp_name)

        if user.avatar:
            try:
                os.system('rm -f %s*' % get_asset_path(user.avatar[:user.avatar.rfind('.')]))
            except:
                pass
        user.avatar = user.avatar_tmp
        try:
            orm.commit()
        except:
            pass
        src = self.current_user.avatar_tmp
        avatar = self.current_user.get_avatar(size=128)
        data = {"src": src, "avatar": avatar}
        return self.send_success_result(msg=u'头像设置成功', data=data)


class BackgroundDelHandler(BaseHandler):
    @orm.db_session
    @tornado.web.authenticated
    def post(self):
        remove_file(get_asset_path(self.current_user.background_img))
        self.current_user.background_img = ''
        try:
            orm.commit()
        except:
            pass
        result = {"status": "success", "message": "已成功重置背景图片"}
        self.send_result(result)


class ImgUploadHandler(BaseHandler):
    @orm.db_session
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
        except IOError as error:
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
        upload_path = os.path.join(config.upload_path, get_year(), get_month())
        mkdir_p(upload_path)
        timestamp = str(int(time.time())) + gen_random_str() + '_' + str(user.id)
        image_format = send_file['filename'].split('.').pop().lower()
        filename = timestamp + '.' + image_format
        tmp_path = os.path.join(upload_path, filename)
        image_one.save(tmp_path)
        tmp_file.close()
        path = '/' + get_relative_path(tmp_path)
        category = self.get_argument('category', None)
        del_path = None
        if category == 'head':
            del_path = user.head_img
            user.head_img = path
            data = {'path': path, 'category': 'head'}
        elif category == 'background':
            del_path = user.background_img
            user.background_img = path
            data = {'path': path, 'category': 'background'}
        else:
            data = {'path': path, 'category': 'other'}
        if del_path:
            remove_file(get_asset_path(del_path))
        return self.send_success_result(data=data)


class ShowHandler(BaseHandler):
    @orm.db_session
    def get(self):
        import ipdb; ipdb.set_trace()
        page = force_int(self.get_argument('page', 1), 1)
        category = self.get_argument('category', None)
        limit = 12
        hot_users = User.get_users(category='hot', limit=limit)
        new_users = User.get_users(category='new', limit=limit)
        page_count = 0
        users = []
        url = '/users'
        if category == 'all':
            user_count = orm.count(User.get_users(page=None))
            page_count = (user_count + config.user_paged - 1) // config.user_paged
            users = User.get_users(page=page)
            url = '/users?category=all'
        elif category == 'online':
            online = rd.smembers("online") or [0]
            online = [int(i) for i in online]
            users = User.select(lambda rv: rv.id in online)
            user_count = len(users)
            page_count = (user_count + config.user_paged - 1) // config.user_paged
            url = '/users?category=online'
        return self.render("user/show.html", users=users, hot_users=hot_users,
                           new_users=new_users, page=page,
                           page_count=page_count, url=url, category=category)
