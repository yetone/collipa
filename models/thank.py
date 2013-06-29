# coding: utf-8

import time
from pony.orm import *
from ._base import db, SessionMixin, ModelMixin
import config

config = config.rec()

class Thank(db.Entity, SessionMixin, ModelMixin):
    user_id = Required(int)

    created_at = Required(int, default=int(time.time()))

    topic_id = Optional(int)
    reply_id = Optional(int)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Thank: %s>' % self.id

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

            topic.thank_count += 1
            topic.author.thank_count += 1

            topic.author.income(coin=config.thank_coin, role="thank",
                    topic_id=self.topic_id)
            self.author.spend(coin=config.thank_coin, role="thank",
                    topic_id=self.topic_id)

        if self.reply_id:
            reply = self.reply
            if reply.user_id == self.user_id:
                self.delete()
                try:
                    commit()
                except:
                    pass
                return None

            reply.thank_count += 1
            reply.author.thank_count += 1

            reply.author.income(coin=config.thank_coin, role="thank",
                    reply_id=self.reply_id)
            self.author.spend(coin=config.thank_coin, role="thank",
                    reply_id=self.reply_id)

        return super(Thank, self).save()

    def remove(self):
        if self.topic_id:
            self.topic.thank_count -= 1
            self.topic.author.thank_count -= 1

            self.author.income(coin=config.thank_coin, role="thank-remove",
                    topic_id=self.topic_id)
            self.topic.author.spend(coin=config.thank_coin, role="thank-remove",
                    topic_id=self.topic_id)

        if self.reply_id:
            self.reply.thank_count -= 1
            self.reply.author.thank_count -= 1

            self.author.income(coin=config.thank_coin, role="thank-remove",
                    reply_id=self.reply_id)
            self.reply.author.spend(coin=config.thank_coin, role="thank-remove",
                    reply_id=self.reply_id)

        super(Thank, self).remove()
