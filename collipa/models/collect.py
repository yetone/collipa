# coding: utf-8

import time
from pony import orm
from ._base import db, BaseModel
from collipa import config


class Collect(db.Entity, BaseModel):
    user_id = orm.Required(int)

    created_at = orm.Required(int, default=int(time.time()))

    collect_class_id = orm.Optional(int)
    topic_id = orm.Optional(int)
    reply_id = orm.Optional(int)
    tweet_id = orm.Optional(int)

    content = orm.Optional(orm.LongUnicode)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Collect: %s>' % self.id

    def save(self):
        now = int(time.time())
        self.created_at = now

        if self.topic_id:
            self.topic.collect_count += 1
            self.topic.author.collect_count += 1
            self.content = self.topic.content

            self.topic.author.income(coin=config.collect_coin, role="collect",
                                     topic_id=self.topic_id)
            self.author.spend(coin=config.collect_coin, role="collect",
                              topic_id=self.topic_id)

        if self.reply_id:
            self.reply.collect_count += 1
            self.reply.author.collect_count += 1
            self.content = self.reply.content

            self.reply.author.income(coin=config.collect_coin, role="collect",
                                     reply_id=self.reply_id)
            self.author.spend(coin=config.collect_coin, role="collect",
                              reply_id=self.reply_id)

        self.author.collection_count += 1

        return super(Collect, self).save()

    def delete(self):
        if self.topic_id:
            self.topic.collect_count -= 1
            self.topic.author.collect_count -= 1
        if self.reply_id:
            self.reply.collect_count -= 1
            self.reply.author.collect_count -= 1

        self.author.collection_count -= 1

        super(Collect, self).delete()
