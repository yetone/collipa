# coding: utf-8

import time
from pony.orm import *
from ._base import db, SessionMixin, ModelMixin
import models as m
import config

config = config.rec()

class Block(db.Entity, SessionMixin, ModelMixin):
    user_id = Required(int)

    created_at = Required(int, default=int(time.time()))

    """ 屏蔽类型
        topic_id    屏蔽主题
        reply_id    屏蔽评论
        node_id     屏蔽节点
        blocker_id  屏蔽用户
    """
    topic_id = Optional(int)
    reply_id = Optional(int)
    tweet_id = Optional(int)
    node_id = Optional(int)
    blocker_id = Optional(int)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Block: %s>' % self.id

    @property
    def blocker(self):
        if self.blocker_id:
            return m.User.get(id=blocker_id)
        return None

    def save(self):

        super(Up, self).save()

    def remove(self):

        super(Up, self).remove()
