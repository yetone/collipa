# coding: utf-8

import time
from pony import orm
from ._base import db, BaseModel
import collipa.models


class Block(db.Entity, BaseModel):
    user_id = orm.Required(int)

    created_at = orm.Required(int, default=int(time.time()))

    """ 屏蔽类型
        topic_id    屏蔽主题
        reply_id    屏蔽评论
        node_id     屏蔽节点
        blocker_id  屏蔽用户
    """
    topic_id = orm.Optional(int)
    reply_id = orm.Optional(int)
    tweet_id = orm.Optional(int)
    node_id = orm.Optional(int)
    blocker_id = orm.Optional(int)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Block: %s>' % self.id

    @property
    def blocker(self):
        if self.blocker_id:
            return collipa.models.User.get(id=self.blocker_id)
        return None

    def save(self):
        super(m.Up, self).save()

    def delete(self):
        super(m.Up, self).delete()
