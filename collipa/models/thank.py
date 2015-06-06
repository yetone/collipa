# coding: utf-8

import time
from pony import orm
from ._base import db, BaseModel
from collipa import config


class Thank(db.Entity, BaseModel):
    user_id = orm.Required(int)

    created_at = orm.Required(int, default=int(time.time()))

    topic_id = orm.Optional(int)
    reply_id = orm.Optional(int)
    tweet_id = orm.Optional(int)

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
                    orm.commit()
                except:
                    pass
                return None

            topic.thank_count += 1
            topic.author.thank_count += 1

            topic.author.income(coin=config.thank_coin,
                                role="thank",
                                topic_id=self.topic_id)
            self.author.spend(coin=config.thank_coin,
                              role="thank",
                              topic_id=self.topic_id)

        if self.reply_id:
            reply = self.reply
            if reply.user_id == self.user_id:
                self.delete()
                try:
                    orm.commit()
                except:
                    pass
                return None

            reply.thank_count += 1
            reply.author.thank_count += 1

            reply.author.income(coin=config.thank_coin,
                                role="thank",
                                reply_id=self.reply_id)
            self.author.spend(coin=config.thank_coin,
                              role="thank",
                              reply_id=self.reply_id)

        return super(Thank, self).save()

    def delete(self):
        if self.topic_id:
            self.topic.thank_count -= 1
            self.topic.author.thank_count -= 1

            self.author.income(coin=config.thank_coin,
                               role="thank-remove",
                               topic_id=self.topic_id)
            self.topic.author.spend(coin=config.thank_coin,
                                    role="thank-remove",
                                    topic_id=self.topic_id)

        if self.reply_id:
            self.reply.thank_count -= 1
            self.reply.author.thank_count -= 1

            self.author.income(coin=config.thank_coin,
                               role="thank-remove",
                               reply_id=self.reply_id)
            self.reply.author.spend(coin=config.thank_coin,
                                    role="thank-remove",
                                    reply_id=self.reply_id)

        super(Thank, self).delete()
