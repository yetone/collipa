# coding: utf-8

import time
from pony.orm import Required, desc
from ._base import db, SessionMixin, ModelMixin
import models as m
import config

config = config.rec()


class MessageBox(db.Entity, SessionMixin, ModelMixin):
    sender_id = Required(int)
    receiver_id = Required(int)

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
    updated_at = Required(int, default=int(time.time()))

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<MessageBox: %s>' % self.id

    @property
    def sender(self):
        return m.User.get(id=self.sender_id)

    @property
    def receiver(self):
        return m.User.get(id=self.receiver_id)

    @property
    def message(self):
        message = m.Message.select(lambda rv: rv.message_box1_id == self.id or
                                   rv.message_box2_id == self.id).order_by(lambda rv: desc(rv.created_at))
        if message:
            message = message[:][0]
        else:
            message = None
        return message

    def get_messages(self, page=1):
        messages = m.Message.select(lambda rv: rv.message_box1_id == self.id or
                                    rv.message_box2_id == self.id).order_by(lambda rv: desc(rv.created_at))
        messages = messages[(page - 1) * config.paged: page * config.paged]
        return messages

    def save(self):
        now = int(time.time())
        self.created_at = now
        self.updated_at = now

        return super(MessageBox, self).save()
