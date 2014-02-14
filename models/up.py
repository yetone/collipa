# coding: utf-8

import time
from pony.orm import *
from ._base import db, SessionMixin, ModelMixin
import config

config = config.rec()

class Up(db.Entity, SessionMixin, ModelMixin):
    user_id = Required(int)

    created_at = Required(int, default=int(time.time()))

    topic_id = Optional(int)
    reply_id = Optional(int)
    tweet_id = Optional(int)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Up: %s>' % self.id

    def save(self):
        now = int(time.time())
        self.created_at = now

        if self.topic_id:
            topic = self.topic
            if topic.user_id == self.user_id:
                self.delete()
                try:
                    commit()
                except:
                    pass
                return None

            if topic.compute_count > 0 and topic.up_count in\
                config.topic_compute_key_list:
                topic.compute_role()

            topic.up_count += 1
            topic.author.up_count += 1

        if self.reply_id:
            reply = self.reply
            if reply.user_id == self.user_id:
                self.delete()
                try:
                    commit()
                except:
                    pass
                return None

            if reply.compute_count > 0 and reply.up_count in\
                config.reply_compute_key_list:
                reply.compute_role()

            reply.up_count += 1
            reply.author.up_count += 1

        return super(Up, self).save()

    def remove(self):
        if self.topic_id:
            self.topic.up_count -= 1
            self.topic.author.up_count -= 1

        if self.reply_id:
            self.reply.up_count -= 1
            self.reply.author.up_count -= 1

        super(Up, self).remove()
