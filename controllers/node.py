# coding: utf-8

import time
import random
import tornado.web

import os
import sys
import logging
import tempfile
import Image

import config
from ._base import BaseHandler
from pony.orm import *

from models import Node
from forms import NodeForm, NodeEditForm
from helpers import strip_tags, get_year, get_month, force_int

config = config.rec()

class HomeHandler(BaseHandler):
    @db_session
    def get(self, urlname, category='all'):
        node = Node.get(urlname=urlname)
        if not node:
            raise tornado.web.HTTPError(404)
        page = force_int(self.get_argument('page', 1), 1)
        action = self.get_argument('action', None)
        tag = self.get_argument('tag', None)
        if tag:
            if tag == 'description':
                result = {'status': 'success', 'message': '简介传输成功',
                        'node_description': node.description,
                        'node_topic_count': node.topic_count,
                        'node_follow_count': node.follow_count}
                return self.write(result)
            if tag == 'relationship':
                parent_nodes = node.parent_nodes
                child_nodes = node.child_nodes
                sibling_nodes = node.sibling_nodes
                parent_json = []
                children_json = []
                sibling_json = []
                for p in parent_nodes:
                    parent_json.append(dict(id=p.id, name=p.name,
                        url=p.url,
                        description=p.description,
                        summary=p.summary,
                        urlname=p.urlname,
                        icon=p.icon))
                for c in child_nodes:
                    children_json.append(dict(id=c.id, name=c.name,
                        url=c.url,
                        description=c.description,
                        summary=c.summary,
                        urlname=c.urlname,
                        icon=c.icon))
                for s in sibling_nodes:
                    sibling_json.append(dict(id=s.id, name=s.name,
                        url=s.url,
                        description=s.description,
                        summary=s.summary,
                        urlname=s.urlname,
                        icon=s.icon))
                result = {'status': 'success', 'parent_nodes': parent_json, 'child_nodes':
                        children_json, 'sibling_nodes': sibling_json}
                return self.write(result)
        user = self.current_user
        if action and user:
            if action == 'follow':
                result = user.follow(node_id=node.id)
                if self.is_ajax:
                    return self.write(result)
                self.flash_message(result)
                return self.redirect_next_url()
        topic_count = count(node.get_topics(page=None, category=category))
        page_count = (topic_count + config.reply_paged - 1) // config.reply_paged
        url = node.url + '?category=' + category
        topics = node.get_topics(page=page, category=category)
        return self.render("node/index.html", node=node, topics=topics,
                category=category, page=page, page_count=page_count, url=url)

class CreateHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    def get(self):
        if not self.has_permission:
            return
        if not self.current_user.is_admin:
            return self.redirect_next_url()
        node_id = int(self.get_argument('node_id', 0))
        node = Node.get(id=node_id)
        if node:
            selected = [node.name]
        else:
            selected = []
        form = NodeForm.init(Node.get_node_choices(), selected)
        return self.render("node/create.html", form=form)

    @db_session
    @tornado.web.authenticated
    def post(self):
        if not self.has_permission:
            return
        if not self.current_user.is_admin:
            return self.redirect_next_url()
        user = self.current_user
        form = NodeForm(self.request.arguments)
        if form.validate():
            node = form.save(user)
            return self.redirect(node.url)
        return self.render("node/create.html", form=form)

class EditHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    def get(self, urlname):
        if not self.has_permission:
            return
        if not self.current_user.is_admin:
            return self.redirect_next_url()
        node = Node.get(urlname=urlname)
        if node:
            selected = [n.name for n in node.parent_nodes]
        else:
            return self.redirect_next_url()
        args = {'name': [node.name], 'urlname': [node.urlname],
                'description': [node.description], 'style': [node.style]}
        form = NodeEditForm.init(Node.get_node_choices(), selected, args=args,
                node=node)
        return self.render("node/edit.html", form=form, node=node)

    @db_session
    @tornado.web.authenticated
    def post(self, urlname):
        if not self.has_permission:
            return
        if not self.current_user.is_admin:
            return self.redirect_next_url()
        node = Node.get(urlname=urlname)
        if not node:
            return self.redirect_next_url()
        user = self.current_user
        args = self.request.arguments
        try:
            selected = args.get('parent_name')
            print(selected)
        except:
            selected = [n.name for n in node.parent_nodes]
            args = {'name': [node.name], 'urlname': [node.urlname],
                    'description': [node.description], 'style': [node.style]}
        form = NodeEditForm.init(Node.get_node_choices(), selected, args=args,
                node=node)
        if form.validate():
            node = form.save(user, node=node)
            result = {'status': 'success', 'message': '节点修改成功',
                    'node_url': node.url}
            if self.is_ajax:
                return self.write(result)
            self.flash_message(result)
            return self.redirect(node.url)
        if self.is_ajax:
            return self.write(form.result)
        return self.render("node/edit.html", form=form, node=node)

class ImgUploadHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    def post(self, node_id):
        if not self.has_permission:
            return
        if not self.current_user.is_admin:
            return self.redirect_next_url()
        category = self.get_argument('category', None)
        node = Node.get(id=node_id)
        if not node:
            return self.redirect_next_url()
        if self.request.files == {} or 'myimage' not in self.request.files:
            self.write({"status": "error",
                "message": "对不起，请选择图片"})
            return
        image_type_list = ['image/gif', 'image/jpeg', 'image/pjpeg',
                'image/png', 'image/bmp', 'image/x-png']
        icon_type_list = ['image/gif', 'image/jpeg', 'image/pjpeg',
                'image/png', 'image/bmp', 'image/x-png', 'image/ico .ico',
                'image/x-icon']
        send_file = self.request.files['myimage'][0]
        if category != 'icon' and send_file['content_type'] not in image_type_list:
            self.write({"status": "error",
                "message": "对不起，仅支持 jpg, jpeg, bmp, gif, png\
                    格式的图片"})
            return
        if category == 'icon' and send_file['content_type'] not in icon_type_list:
            self.write({"status": "error",
                "message": "对不起，仅支持 ico, jpg, jpeg, bmp, gif, png\
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
        if width < 20 or height < 20 or width > 30000 or height > 30000:
            tmp_file.close()
            self.write({"status": "error",
                "message": "对不起，请上传长宽在20px~30000px之间的图片！"})
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
        print category
        del_path = None
        if category == 'head':
            del_path = node.head_img
            node.head_img = path
            result = {'path': path, 'status': "success", 'message':
                    '节点头部背景设置成功', 'category': 'head'}
        elif category == 'icon':
            image_two = image_one.resize((75, 75), Image.ANTIALIAS)

            tmp_name2 = upload_path + timestamp + 'x75.' + image_format
            image_two.save(tmp_name2)
            try:
                os.system('rm -f %s%s' % (sys.path[0], path))
            except:
                pass
            path = '/' +\
                '/'.join(tmp_name2.split('/')[tmp_name2.split('/').index("static"):])
            del_path = node.icon_img
            node.icon_img = path
            result = {'path': path, 'status': "success", 'message':
                    '节点图标设置成功', 'category': 'icon'}
        elif category == 'background':
            del_path = node.background_img
            node.background_img = path
            result = {'path': path, 'status': "success", 'message':
                    '节点背景设置成功', 'category': 'background'}
        else:
            result = {'path': path, 'status': "success", 'message':
                '图片上传成功'}
        if del_path:
            try:
                os.system('rm -f %s%s' % (sys.path[0],
                    del_path))
            except:
                pass
        try:
            commit()
        except:
            pass
        if self.is_ajax:
            return self.write(result)
        return

class ShowHandler(BaseHandler):
    @db_session
    def get(self):
        page = force_int(self.get_argument('page', 1), 1)
        page_count = 0
        nodes = []
        category = self.get_argument('category', None)
        hot_nodes = Node.get_nodes(category='hot', limit=8)
        new_nodes = Node.get_nodes(category='new', limit=8)
        url = '/nodes'
        if category == 'all':
            nodes = Node.get_nodes(category='all', page=page)
            node_count = count(Node.get_nodes(page=None))
            page_count = (node_count + config.node_paged - 1) // config.node_paged
            url = '/nodes?category=' + category
        return self.render("node/show.html", hot_nodes=hot_nodes,
                new_nodes=new_nodes, nodes=nodes, category=category, page=page,
                page_count=page_count, url=url)
