# coding: utf-8

import time
import random

import os
import sys
import logging
import tempfile
from PIL import Image as Img
from pony import orm
from ._base import BaseHandler
import tornado.web
from models import Image, Album
from helpers import get_year, get_month, require_permission, force_int

import config
from .user import EmailMixin

config = config.Config()


class HomeHandler(BaseHandler, EmailMixin):
    @orm.db_session
    def get(self, image_id):
        image_id = int(image_id)
        image = Image.get(id=image_id)
        if not image:
            raise tornado.web.HTTPError(404)
        return self.render("image/index.html", image=image)

    @orm.db_session
    @require_permission
    def put(self, image_id):
        image_id = int(image_id)
        image = Image.get(id=image_id)
        if not image:
            raise tornado.web.HTTPError(404)
        album_id = self.get_int('album_id', None)
        if not album_id:
            return self.send_error_result(msg=u'没有指定专辑哦')
        album = Album.get(id=album_id)
        if not album:
            return self.send_error_result(msg=u'专辑不存在')
        if album.user_id != self.current_user.id:
            return self.send_error_result(msg=u'此专辑不是您的专辑')
        if image.album_id != album_id:
            image.album_id = album_id
        return self.send_success_result()


    @orm.db_session
    @tornado.web.authenticated
    def delete(self, image_id):
        image = Image.get(id=image_id)
        if not image:
            return self.redirect_next_url()
        if self.current_user.is_admin and image.user_id != self.current_user.id:
            subject = "图片删除通知 - " + config.site_name
            template = (
                '<p>尊敬的 <strong>%(nickname)s</strong> 您好！</p>'
                '您在 %(site) 的图片由于违反社区规定而被删除。</p>'
            ) % {
                'nickname': image.author.nickname,
                'site': config.site_name,
            }
            self.send_email(self, image.author.email, subject, template)
        if image.user_id == self.current_user.id:
            image.remove()
            result = {'status': 'success', 'message': '已成功删除'}
        else:
            result = {'status': 'error', 'message': '你没有权限啊, baby'}
        return self.write(result)


class ListHandler(BaseHandler):
    @orm.db_session
    def get(self):
        album_id = self.get_argument('album_id', None)
        from_id = force_int(self.get_argument('from_id', 0), 0)
        limit = force_int(self.get_argument('limit', config.paged), config.paged)
        if not album_id:
            result = {'status': 'error', 'message': '没有指定专辑'}
            return self.write(result)
        images = Image.query_by_album_id(album_id, from_id=from_id, limit=limit + 1)
        has_more = len(images) > limit
        object_list = []
        for image in images:
            object_list.append(image.to_dict())
        return self.write({'status': 'success', 'object_list': object_list, 'has_more': has_more})


class UploadHandler(BaseHandler):
    @orm.db_session
    @tornado.web.authenticated
    @require_permission
    def post(self):
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
        if len(send_file['body']) > 100 * 1024 * 1024:
            self.write({"status": "error",
                        "message": "对不起，请上传100M以下的图片"})
            return
        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        tmp_file.write(send_file['body'])
        tmp_file.seek(0)
        try:
            image_one = Img.open(tmp_file.name)
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
        upload_path = sys.path[0] + "/static/upload/image/" + get_year() + '/' +\
            get_month() + "/"
        if not os.path.exists(upload_path):
            try:
                os.system('mkdir -p %s' % upload_path)
            except:
                pass
        timestamp = str(int(time.time())) +\
            ''.join(random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba',
                                  6)) + '_' + str(user.id)
        image_format = send_file['filename'].split('.').pop().lower()
        tmp_name = upload_path + timestamp + '.' + image_format
        image_one.save(tmp_name, image_one.format or 'JPEG')
        tmp_file.close()
        path = '/' +\
            '/'.join(tmp_name.split('/')[tmp_name.split('/').index("static"):])
        album_id = self.get_argument('album_id', '')
        if not album_id:
            album = user.default_album
        else:
            album = Album.get(id=album_id)
            if not (album and album.user_id != user.id):
                album = user.default_album
        image = Image(user_id=user.id,
                      album_id=album.id,
                      path=path,
                      width=width,
                      height=height).save()
        image.crop()
        return self.send_success_result(msg=u'上传成功', data=image.to_dict())
