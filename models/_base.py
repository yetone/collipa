# coding: utf-8

import models as m
from helpers import format_date, cached_property
import config
from pony.orm import *

__all__ = [
    'db', 'SessionMixin', 'ModelMixin',
]

config = config.rec()

db = Database('mysql', config.db_host, config.db_user, config.db_pass,
        config.db_name)

class SessionMixin(object):
    def save(self):
        try:
            commit()
        except:
            pass
        return self

    def remove(self):
        self.delete()
        try:
            commit()
        except:
            pass
        return self

class ModelMixin(object):
    @staticmethod
    def paginate(self, page, per_page):
        return self[(page - 1) * per_page, page * per_page]

    @cached_property
    def author(self):
        try:
            return m.User[self.user_id]
        except:
            return None

    @cached_property
    def topic(self):
        try:
            return m.Topic[self.topic_id]
        except:
            return None

    @cached_property
    def node(self):
        try:
            return m.Node[self.node_id]
        except:
            return None

    @cached_property
    def reply(self):
        try:
            return m.Reply[self.reply_id]
        except:
            return None

    @cached_property
    def created(self):
        try:
            return format_date(self.created_at)
        except:
            return None

    @cached_property
    def updated(self):
        try:
            return format_date(self.updated_at)
        except:
            return None

    @cached_property
    def actived(self):
        try:
            return format_date(self.active)
        except:
            return None

    @cached_property
    def collect_class(self):
        try:
            return m.CollectClass[self.collect_class_id]
        except:
            return None
