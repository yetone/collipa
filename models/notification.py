# coding: utf-8

import logging
import time
from pony import orm
from ._base import db, SessionMixin, ModelMixin
import models as m
import config

config = config.Config()


class Notification(db.Entity, SessionMixin, ModelMixin):
    sender_id = orm.Optional(int)
    receiver_id = orm.Optional(int)

    """ 提醒类型
        'reply'   : 评论提醒
        'answer'  : 回复提醒
        'mention' : 提及提醒
        'up'      : 赞同提醒
        'thank'   : 感谢提醒
    """
    role = orm.Required(unicode, default='reply')

    """ 状态
        1:      已读
        0:      未读
    """
    status = orm.Required(int, default=0)

    """ 开关
        1:      开
        0:      关
    """
    switch = orm.Required(int, default=1)

    created_at = orm.Required(int, default=int(time.time()))
    updated_at = orm.Required(int, default=int(time.time()))

    topic_id = orm.Optional(int)
    reply_id = orm.Optional(int)
    tweet_id = orm.Optional(int)

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
        import controllers as ctl

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
        logging.info('I am send websocket to %d', notification.receiver_id)

        return notification
