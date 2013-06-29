# coding: utf-8

import time
from pony.orm import *
from ._base import db, SessionMixin, ModelMixin
import models as m
import config

config = config.rec()

class Message(db.Entity, SessionMixin, ModelMixin):
    message_box1_id = Required(int)
    message_box2_id = Required(int)
    user_id = Required(int)

    content = Required(LongUnicode)

    """ 信息类型
        'message':        私信
    """
    role = Required(unicode, default='message')

    """ 状态
        1:      已读
        0:      未读
    """
    status = Required(int, default=0)

    created_at = Required(int, default=int(time.time()))

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Message: %s>' % self.id

    @property
    def message_box1(self):
        return m.MessageBox.get(id=self.message_box1_id)

    @property
    def message_box2(self):
        return m.MessageBox.get(id=self.message_box2_id)

    def save(self):
        now = int(time.time())
        self.created_at = now

        try:
            commit()
        except Exception, e:
            print type(e).__name__
            print e
            raise
        message = super(Message, self).save()

        self.message_box1.updated_at = now
        self.message_box2.updated_at = now
        self.message_box2.status = 0

        return message
