# coding: utf-8

import time
from pony import orm
from ._base import db, BaseModel


class Report(db.Entity, BaseModel):
    user_id = orm.Required(int)

    created_at = orm.Required(int, default=int(time.time()))

    topic_id = orm.Optional(int)
    reply_id = orm.Optional(int)
    tweet_id = orm.Optional(int)
    album_id = orm.Optional(int)
    image_id = orm.Optional(int)

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

    def delete(self):
        if self.topic_id:
            self.topic.report_count -= 1
            self.topic.author.report_count -= 1
        if self.reply_id:
            self.reply.report_count -= 1
            self.reply.author.report_count -= 1

        super(Report, self).delete()
