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
from extensions import mc
from helpers import force_int

config = config.rec()

class OnlineCountHandler(BaseHandler, tornado.websocket.WebSocketHandler):
    users = set()
    online = set()

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    @db_session
    def open(self):
        if self.current_user and self not in OnlineCountHandler.users:
            self.user_id = self.current_user.id
            OnlineCountHandler.users.add(self)
            OnlineCountHandler.online.add(self.current_user.id)
            mc.set("online", OnlineCountHandler.online, 60 * 60 * 24)
            self.on_message("open")

    def on_close(self):
        if self.current_user and self in OnlineCountHandler.users:
            OnlineCountHandler.users.remove(self)
            OnlineCountHandler.online.remove(self.user_id)
            mc.set("online", OnlineCountHandler.online, 60 * 60 * 24)
            self.on_message("close")

    @classmethod
    def send_updates(cls):
        logging.info("Online user count is " + unicode(len(cls.users)))
        for user in cls.users:
            try:
                user.write_message(unicode(len(cls.users)))
            except:
                logging.error("Error sending online user count", exc_info=True)

    def on_message(self, message):
        logging.info(message)
        OnlineCountHandler.send_updates()

class GetUserNameHandler(BaseHandler):
    @db_session
    def get(self):
        users = User.select()
        user_json = []
        for user in users:
            user_json.append({"value": user.name, "label": user.nickname})
        return self.write(user_json)
