# coding: utf-8

import time
from pony import orm
from ._base import db, BaseModel
from collipa import config


class Down(db.Entity, BaseModel):
    user_id = orm.Required(int)

    created_at = orm.Required(int, default=int(time.time()))

    topic_id = orm.Optional(int)
    reply_id = orm.Optional(int)
    tweet_id = orm.Optional(int)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Down: %s>' % self.id

    def save(self):
        now = int(time.time())
        self.created_at = now

        if self.topic_id:
            topic = self.topic
            if topic.user_id == self.user_id:
                self.delete()
                try:
                    orm.commit()
                except:
                    pass
                return None

            if topic.compute_count > 0 and topic.down_count in config.topic_compute_key_list:
                topic.compute_role()

            topic.down_count += 1
            topic.author.down_count += 1

        if self.reply_id:
            reply = self.reply
            if reply.user_id == self.user_id:
                self.delete()
                try:
                    orm.commit()
                except:
                    pass
                return None

            if reply.compute_count > 0 and reply.down_count in config.reply_compute_key_list:
                reply.compute_role()

            reply.down_count += 1
            reply.author.down_count += 1

        return super(Down, self).save()

    def delete(self):
        if self.topic_id:
            self.topic.down_count -= 1
            self.topic.author.down_count -= 1
        if self.reply_id:
            self.reply.down_count -= 1
            self.reply.author.down_count -= 1

        super(Down, self).delete()
