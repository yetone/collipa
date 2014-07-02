# coding: utf-8

import time
from pony.orm import Required, Optional
from ._base import db, SessionMixin, ModelMixin
import config

config = config.rec()


class Report(db.Entity, SessionMixin, ModelMixin):
    user_id = Required(int)

    created_at = Required(int, default=int(time.time()))

    topic_id = Optional(int)
    reply_id = Optional(int)
    tweet_id = Optional(int)
    album_id = Optional(int)
    image_id = Optional(int)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Report: %s>' % self.id

    def save(self):
        now = int(time.time())
        self.created_at = now

        if self.topic_id:
            topic = self.topic
            if topic.report_count > 12:
                topic.compute_role()

            topic.report_count += 1
            topic.author.report_count += 1

        if self.reply_id:
            reply = self.reply
            if reply.report_count > 12:
                reply.compute_role()

            reply.report_count += 1
            reply.author.report_count += 1

        return super(Report, self).save()

    def remove(self):
        if self.topic_id:
            self.topic.report_count -= 1
            self.topic.author.report_count -= 1
        if self.reply_id:
            self.reply.report_count -= 1
            self.reply.author.report_count -= 1

        super(Report, self).remove()
