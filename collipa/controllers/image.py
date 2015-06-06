# coding: utf-8

import logging
import tempfile
import tornado.web
from pony import orm
from ._base import BaseHandler
from .user import EmailMixin
from collipa.libs.pil import Image as Img
from collipa.models import Image, Album
from collipa.helpers import require_permission, gen_upload_path, get_relative_path, force_int

from collipa import config


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
        if image.topic_id:
            return self.send_error_result(msg=u'此图片被主题《%s》引用，无法删除' % image.topic.title)
        if self.current_user.is_admin and image.user_id != self.current_user.id:
            subject = "图片删除通知 - " + config.site_name
            template = (
                '<p>尊敬的 <strong>{nickname}</strong> 您好！</p>'
                '您在 {site} 的图片由于违反社区规定而被删除。</p>'
            )
            content = template.format(
                nickname=image.author.nickname,
                site=config.site_name
            )
            self.send_email(self, image.author.email, subject, content)
        if self.current_user.is_admin or image.user_id == self.current_user.id:
            image.delete()
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
        return self.send_success_result(object_list=object_list, has_more=has_more)


class UploadHandler(BaseHandler):
    @orm.db_session
    @tornado.web.authenticated
    @require_permission
    def post(self):
        if not self.request.files or 'myimage' not in self.request.files:
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
            img = Img.open(tmp_file.name)
        except IOError, error:
            logging.info(error)
            logging.info('+' * 30 + '\n')
            logging.info(self.request.headers)
            tmp_file.close()
            self.write({"status": "error",
                        "message": "对不起，此文件不是图片"})
            return

        width, height = img.size
        if width < 80 or height < 80 or width > 30000 or height > 30000:
            tmp_file.close()
            self.write({"status": "error",
                        "message": "对不起，请上传长宽在80px~30000px之间的图片！"})
            return

        user = self.current_user
        suffix = img.format.lower()
        upload_path = gen_upload_path(suffix=suffix)

        img.save(upload_path, img.format or 'JPEG')
        tmp_file.close()

        path = '/%s' % get_relative_path(upload_path).lstrip('/')
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
        return self.send_success_result(msg=u'上传成功', **image.to_dict())
