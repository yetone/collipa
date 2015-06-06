# coding: utf-8

import time
from pony import orm
from ._base import db, BaseModel
import collipa.models


class History(db.Entity, BaseModel):
    user_id = orm.Required(int)
    content = orm.Required(orm.LongUnicode)

    created_at = orm.Required(int, default=int(time.time()))

    topic_id = orm.Optional(int)
    reply_id = orm.Optional(int)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<History: %s>' % self.id

    @property
    def item(self):
        if self.topic_id:
            return collipa.models.Topic.get(id=self.topic_id)
        elif self.reply_id:
            return collipa.models.Reply.get(id=self.reply_id)

    def save(self):
        now = int(time.time())
        self.created_at = now

        return super(History, self).save()

    def delete(self):

        super(History, self).delete()
