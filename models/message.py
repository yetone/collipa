# coding: utf-8

import time
from pony import orm
from ._base import db, SessionMixin, ModelMixin
import models as m
import config

config = config.Config()


class Message(db.Entity, SessionMixin, ModelMixin):
    message_box1_id = orm.Required(int, default=0)
    message_box2_id = orm.Required(int, default=0)

    sender_id = orm.Required(int)
    receiver_id = orm.Required(int)

    content = orm.Required(orm.LongUnicode)

    """ 信息类型
        'message':        私信
    """
    role = orm.Required(unicode, default='message')

    """ 状态
        1:      已读
        0:      未读
    """
    status = orm.Required(int, default=0)

    created_at = orm.Required(int, default=int(time.time()))

    def __str__(self):
        return self.sender_id

    def __repr__(self):
        return '<Message: %s>' % self.sender_id

    @property
    def message_box1(self):
        return m.MessageBox.get(id=self.message_box1_id)

    @property
    def message_box2(self):
        return m.MessageBox.get(id=self.message_box2_id)

    @property
    def sender(self):
        return m.User[self.sender_id]

    @property
    def receiver(self):
        return m.User[self.receiver_id]

    def save(self):
        now = int(time.time())
        self.created_at = now

        message_box1 = self.sender.get_message_box(user=self.receiver)
        message_box2 = self.receiver.get_message_box(user=self.sender)
        if not message_box1:
            message_box1 = m.MessageBox(sender_id=self.sender.id,
                                        receiver_id=self.receiver.id,
                                        status=1).save()
        if not message_box2:
            message_box2 = m.MessageBox(sender_id=self.receiver.id,
                                        receiver_id=self.sender.id,
                                        status=0).save()
        else:
            message_box2.status = 0

        self.message_box1_id = message_box1.id
        self.message_box2_id = message_box2.id

        message_box1.updated_at = now
        message_box2.updated_at = now

        message = super(Message, self).save()

        return message
