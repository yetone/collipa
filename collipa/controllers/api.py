# coding: utf-8

import logging
import tornado.web
import tornado.websocket
import tornado.escape

from ._base import BaseHandler
from pony import orm

from collipa.models import User
from collipa.extensions import rd


class WebSocketHandler(BaseHandler, tornado.websocket.WebSocketHandler):
    users = {}
    onlines = set()

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def __init__(self, application, request, **kwargs):
        super(WebSocketHandler, self).__init__(application, request, **kwargs)
        self.user_id = None
        if self.current_user:
            self.user_id = self.current_user.id

    @orm.db_session
    def open(self):
        if self.user_id:
            if self.user_id not in self.users:
                self.users[self.user_id] = set()
            self.users[self.user_id].add(self)
            User.online(self.user_id)
        self.onlines.add(self)
        self.send_online()

    def on_close(self):
        if self.user_id:
            if self.user_id in self.users:
                try:
                    self.users[self.user_id].remove(self)
                except KeyError:
                    pass
            User.offline(self.user_id)
        self.onlines.remove(self)
        self.send_online()

    def send(self, event, extra=None, **kwargs):
        extra = extra or {}
        body = {
            'event': event,
            'extra': extra,
            'data': kwargs,
        }
        self.write_message(body)

    @classmethod
    def send_online(cls):
        for ws in cls.onlines:
            try:
                ws.send('online', count=User.get_online_count())
            except Exception as e:
                logging.error("Error sending online user count", exc_info=True)
                if type(e).__name__ == "AttributeError":
                    ws.on_close()

    @classmethod
    @orm.db_session
    def send_message(cls, user_id, message):
        logging.info("Message send")
        if user_id not in cls.users:
            return
        user = User[user_id]
        if not user:
            return
        data = {
            "count": user.unread_message_box_count,
            "content": message.content,
            "created": message.created,
            "id": message.id,
            "avatar": message.sender.get_avatar(size=48),
            "sender_id": message.sender.id,
            "url": message.sender.url,
            "nickname": message.sender.nickname,
            "message_box_id": message.message_box2_id,
        }

        wss = cls.users[user_id]
        for ws in wss:
            try:
                ws.send('message', **data)
            except Exception, e:
                logging.error(e)
                logging.error("Error sending message", exc_info=True)

    @classmethod
    @orm.db_session
    def send_notification(cls, user_id):
        logging.info("Notification send")
        if user_id not in cls.users:
            return
        user = User[user_id]
        if not user:
            return
        data = {
            "count": user.unread_notification_count,
        }
        wss = cls.users[user_id]
        for ws in wss:
            try:
                ws.send('notification', **data)
            except Exception, e:
                logging.error(e)
                logging.error("Error sending notification", exc_info=True)

    def on_message(self, message):
        logging.info(message)


class GetUserNameHandler(BaseHandler):
    @orm.db_session
    def get(self):
        users = User.select()
        user_json = []
        for user in users:
            user_json.append({"value": user.name, "label": user.nickname})
        return self.write(user_json)


class MentionHandler(BaseHandler):
    @orm.db_session
    def get(self):
        word = self.get_argument('word', None)
        if not word:
            return self.write({
                'status': 'error',
                'message': '没有关键字'
            })
        user_list = User.mention(word)
        user_json = []
        for user in user_list:
            user_json.append({
                'id': user.id,
                'name': user.name,
                'nickname': user.nickname,
                'url': user.url,
                'avatar': user.get_avatar()
            })
        return self.write({
            'status': 'success',
            'user_list': user_json
        })
