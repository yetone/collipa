# coding: utf-8

import time
from pony import orm
from ._base import db, BaseModel
import collipa.models
from collipa import config


class MessageBox(db.Entity, BaseModel):
    sender_id = orm.Required(int)
    receiver_id = orm.Required(int)

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
    updated_at = orm.Required(int, default=int(time.time()))

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<MessageBox: %s>' % self.id

    @property
    def sender(self):
        return collipa.models.User.get(id=self.sender_id)

    @property
    def receiver(self):
        return collipa.models.User.get(id=self.receiver_id)

    @property
    def message(self):
        message = (collipa.models.Message
                   .select(lambda rv: rv.message_box1_id == self.id or rv.message_box2_id == self.id)
                   .order_by(lambda rv: orm.desc(rv.created_at)).first())
        return message

    def get_messages(self, page=1):
        messages = (collipa.models.Message
                    .select(lambda rv: rv.message_box1_id == self.id or rv.message_box2_id == self.id)
                    .order_by(lambda rv: orm.desc(rv.created_at)))
        messages = messages[(page - 1) * config.paged: page * config.paged]
        return messages

    def save(self):
        now = int(time.time())
        self.created_at = now
        self.updated_at = now

        return super(MessageBox, self).save()
