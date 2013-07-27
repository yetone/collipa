# coding: utf-8

import time
import random

import os
import sys
import logging
import tempfile
import Image
from ._base import BaseHandler
import tornado.web
from helpers import strip_tags, get_year, get_month
from pony.orm import *

class UploadHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    def post(self):
        if not self.has_permission:
            return
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
        if self.is_ajax:
            return self.write({'path': path, 'status': "success", 'message':
                '上传成功'})
        return
