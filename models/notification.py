# coding: utf-8

import time
from pony.orm import *
from ._base import db, SessionMixin, ModelMixin
import models as m
import controllers as ctl
import config

config = config.rec()

class Notification(db.Entity, SessionMixin, ModelMixin):
    sender_id = Optional(int)
    receiver_id = Optional(int)

    """ 提醒类型
        'reply':        评论提醒
        'answer':       回复提醒
        'mention':      提及提醒
        'up':           赞同提醒
        'thank':        感谢提醒
    """
    role = Required(unicode, default='reply')

    """ 状态
        1:      已读
        0:      未读
    """
    status = Required(int, default=0)

    """ 开关
        1:      开
        0:      关
    """
    switch = Required(int, default=1)

    created_at = Required(int, default=int(time.time()))
    updated_at = Required(int, default=int(time.time()))

    topic_id = Optional(int)
    reply_id = Optional(int)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Notification: %s>' % self.id

    @property
    def sender(self):
        return m.User.get(id=self.sender_id)

    @property
    def receiver(self):
        return m.User.get(id=self.receiver_id)

    def save(self):
        now = int(time.time())
        self.created_at = now
        self.updated_at = now
        if not self.receiver_id:
            if self.topic_id:
                self.receiver_id = self.topic.user_id
            elif self.reply_id:
                self.receiver_id = self.reply.user_id

        notification = super(Notification, self).save()

        ctl.WebSocketHandler.send_notification(notification.receiver_id)

        return notification
