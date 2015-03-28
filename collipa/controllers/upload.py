# coding: utf-8

import time

import os
import sys
import tornado.web
from pony import orm
from ._base import BaseHandler
from collipa.helpers import get_year, get_month, gen_random_str


class UploadHandler(BaseHandler):
    @orm.db_session
    @tornado.web.authenticated
    def post(self, category):
        if not self.has_permission:
            return
        if not self.request.files or 'myfile' not in self.request.files:
            self.write({"status": "error",
                        "message": "对不起，请选择文件"})
            return

        file_type_list = []
        if category == 'music':
            file_type_list = ['audio/mpeg', 'audio/x-wav', 'audio/mp3']
        if not file_type_list:
            return
        send_file = self.request.files['myfile'][0]
        if send_file['content_type'] not in file_type_list:
            if category == 'music':
                self.write({"status": "error",
                            "message": "对不起，仅支持 mp3, wav 格式的音乐文件"})
                return

        if category == 'music':
            if len(send_file['body']) > 20 * 1024 * 1024:
                self.write({"status": "error",
                            "message": "对不起，请上传20M以下的音乐文件"})
                return

        user = self.current_user
        if category == 'music':
            upload_path = sys.path[0] + "/static/upload/music/" + get_year() + '/' +\
                get_month() + "/"
        if not os.path.exists(upload_path):
            try:
                os.system('mkdir -p %s' % upload_path)
            except:
                pass

        timestamp = str(int(time.time())) + gen_random_str() + '_' + str(user.id)
        image_format = send_file['filename'].split('.').pop().lower()
        file_path = upload_path + timestamp + '.' + image_format
        with open(file_path, 'wb') as f:
            f.write(send_file['body'])

        path = '/' + '/'.join(file_path.split('/')[file_path.split('/').index("static"):])
        if category == 'music':
            if self.is_ajax:
                return self.write({
                    'path': path,
                    'status': "success",
                    'message': '上传成功',
                    'category': 'music',
                    'content_type': send_file['content_type'],
                })
        return
