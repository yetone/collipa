# coding: utf-8

import tornado.web

from pony import orm

from collipa import models as m
from collipa.helpers import force_int


class BaseHandler(tornado.web.RequestHandler):
    @orm.db_session
    def get_current_user(self):
        user_json = self.get_secure_cookie('user')
        if user_json:
            id = int(tornado.escape.json_decode(user_json)['id'])
            token = tornado.escape.json_decode(user_json)['token']
            user = m.User.get(id=id)
            if not user:
                return None
            if token == user.token:
                return user
            self.clear_cookie('user')
            return None
        else:
            return None

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie('user',
                                   tornado.escape.json_encode({
                                       'token': user.token,
                                       'id': user.id
                                   }))
        else:
            self.clear_cookie('user')

    def set_index_category(self, category='index'):
        self.set_secure_cookie('index_category',
                               tornado.escape.json_encode(category))
        return category

    @property
    def index_category(self):
        category_json = self.get_secure_cookie('index_category')
        if not category_json:
            return self.set_index_category()
        return tornado.escape.json_decode(category_json)

    def set_node_category(self, node, category='index'):
        self.set_secure_cookie('node_category_%s' % node.id,
                               tornado.escape.json_encode(category))
        return category

    def get_node_category(self, node):
        category_json = self.get_secure_cookie('node_category_%s' % node.id)
        if not category_json:
            return self.set_node_category(node)
        return tornado.escape.json_decode(category_json)

    @property
    def is_ajax(self):
        if '_ajax' in self.request.arguments:
            return True
        if 'X-Requested-With' in self.request.headers and\
                self.request.headers['X-Requested-With'].lower() ==\
                'xmlhttprequest':
            return True
        return False

    @property
    def next_url(self):
        next_url = self.get_argument('next', None)
        return next_url or '/'

    def redirect_next_url(self):
        return self.redirect(self.next_url)

    def _(self, message, plural_message=None, count=None):
        return None

    @property
    def messages(self):
        if not hasattr(self, '_messages'):
            messages = self.get_secure_cookie('flash_messages')
            self._messages = []
            if messages:
                self._messages = tornado.escape.json_decode(messages)
        return self._messages

    def flash_message(self, **kwargs):
        def get_category_message(messages):
            for cat, msg in messages:
                yield (cat, msg)

        if not kwargs:
            messages = self.messages
            self._messages = []
            self.clear_cookie('flash_messages')
            return get_category_message(messages)

        msg = kwargs.get('message', None)
        category = kwargs.get('status', None)
        message = (category, msg)
        self.messages.append(message)
        self.set_secure_cookie('flash_messages',
                               tornado.escape.json_encode(self.messages))
        return message

    @property
    def mail_connection(self):
        return self.application.mail_connection

    @property
    def has_permission(self):
        if self.current_user and (self.current_user.role != 'unverify' or
                                  self.current_user.is_admin):
            return True
        if self.current_user.role == 'unverify':
            result = {"status": "error",
                      "message": "对不起，您的账户尚未激活，请到注册邮箱检查激活邮件"}
        else:
            result = {"status": "error",
                      "message": "对不起，您没有相关权限"}
        if self.is_ajax:
            self.write(result)
        else:
            self.flash_message(**result)
            self.redirect_next_url()
        return False

    def send_result(self, result, redirect_url=None):
        if self.is_ajax:
            return self.write(result)
        self.flash_message(**result)
        return self.redirect(redirect_url or self.next_url)

    def send_result_and_render(self, result, tpl, data=None):
        data = data or dict()
        if self.is_ajax:
            return self.write(result)
        self.flash_message(**result)
        return self.render(tpl, **data)

    @property
    def page(self):
        return force_int(self.get_argument('page', 1))

    def send_error_result(self, msg, redirect_url=None):
        result = {'status': 'error', 'message': msg}
        return self.send_result(result, redirect_url)

    def send_success_result(self, msg=u'操作成功', redirect_url=None, **kwargs):
        result = {
            'status': 'success',
            'message': msg,
            'data': kwargs,
        }
        return self.send_result(result, redirect_url)

    def get_int(self, name, default=None):
        return force_int(self.get_argument(name, default), default)
