# coding: utf-8

import logging
import tornado.web
import tornado.websocket
import tornado.escape

import time
import config
from ._base import BaseHandler
from pony.orm import *

from models import User
from extensions import mc, rd
from helpers import force_int

config = config.rec()

class WebSocketHandler(BaseHandler, tornado.websocket.WebSocketHandler):
    users = set()
    online = set()

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    @db_session
    def open(self):
        if self not in WebSocketHandler.users:
            self.user_id = 0
            if self.current_user:
                self.user_id = self.current_user.id
                WebSocketHandler.online.add(self.current_user.id)
                rd.sadd("online", self.current_user.id)
            WebSocketHandler.users.add(self)
            self.on_message("online")

    def on_close(self):
        if self in WebSocketHandler.users:
            if self.current_user:
                WebSocketHandler.online.remove(self.user_id)
                rd.srem("online", self.user_id)
            WebSocketHandler.users.remove(self)
            self.on_message("offline")

    @classmethod
    def send_online(cls):
        online = rd.smembers("online")
        logging.info("Online user count is " + unicode(len(online)))
        for user in cls.users:
            try:
                user.write_message({"type": "online", "count": unicode(len(online))})
            except:
                logging.error("Error sending online user count", exc_info=True)

    @classmethod
    @db_session
    def send_message(cls, user_id, message):
        logging.info("Message send")
        for this in cls.users:
            if this.user_id == user_id:
                try:
                    user = User[user_id]
                    this.write_message({"type": "message",
                                        "count": user.unread_message_box_count,
                                        "content": message.content,
                                        "created": message.created,
                                        "id": message.id,
                                        "avatar": message.sender.get_avatar(size=48),
                                        "url": message.sender.url,
                                        "nickname": message.sender.nickname,
                                        "message_box_id": message.message_box2_id})
                except Exception, e:
                    print e
                    logging.error("Error sending message", exc_info=True)

    @classmethod
    @db_session
    def send_notification(cls, user_id):
        logging.info("Notification send")
        for this in cls.users:
            if this.user_id == user_id:
                try:
                    user = User[user_id]
                    this.write_message({"type": "notification",
                                        "count": user.unread_notification_count})
                except Exception, e:
                    print e
                    logging.error("Error sending notification", exc_info=True)

    def on_message(self, message):
        logging.info(message)
        WebSocketHandler.send_online()

class GetUserNameHandler(BaseHandler):
    @db_session
    def get(self):
        users = User.select()
        user_json = []
        for user in users:
            user_json.append({"value": user.name, "label": user.nickname})
        return self.write(user_json)
