# coding: utf-8

import time
from pony import orm
from ._base import db, BaseModel
import collipa.models
from collipa import config
from collipa.helpers import get_mention_names


class Reply(db.Entity, BaseModel):
    user_id = orm.Required(int)
    topic_id = orm.Optional(int)
    tweet_id = orm.Optional(int)
    image_id = orm.Optional(int)

    content = orm.Required(orm.LongUnicode)

    role = orm.Required(unicode, 10, default='reply')
    compute_count = orm.Required(int, default=config.reply_compute_count)

    thank_count = orm.Required(int, default=0)
    up_count = orm.Required(int, default=0)
    down_count = orm.Required(int, default=0)
    report_count = orm.Required(int, default=0)
    collect_count = orm.Required(int, default=0)

    floor = orm.Required(int, default=1)

    created_at = orm.Required(int, default=int(time.time()))
    updated_at = orm.Required(int, default=int(time.time()))
    active = orm.Required(int, default=int(time.time()))

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Reply: %s>' % self.id

    @property
    def url(self):
        return '/reply/%s' % self.id

    def compute_role(self):
        up_count = self.up_count
        down_count = self.down_count
        max_count = max(up_count, down_count)
        delta = abs(up_count - down_count)
        ratio = max_count / delta

        if ratio < 2 and max_count == down_count:
            self.role = 'down'
        else:
            self.role = 'up'
        if ratio > 6:
            self.role = 'dispute'
        if self.role == 'up' and self.reply_count > 20 and\
           self.reply_hits > 60:
            self.role = 'hot'

            if not collipa.models.Bill.get(user_id=self.author.id, role='reply-hot',
                                           reply_id=self.id):
                self.author.income(coin=config.reply_hot_coin,
                                   role='reply-hot', reply_id=self.id)
                bank = collipa.models.Bank.get_one()
                bank.spend(coin=config.reply_hot_coin, role='reply-hot',
                           reply_id=self.id)
        if self.report_count > 12 and self.up_count < 5:
            self.role = 'report'

            if not collipa.models.Bill.get(user_id=self.author.id, role='reply-report',
                                           reply_id=self.id):
                self.author.spend(coin=config.reply_report_coin,
                                  role='reply-report', reply_id=self.id)
                bank = collipa.models.Bank.get_one()
                bank.income(coin=config.reply_report_coin, role='reply-report',
                            reply_id=self.id)

        try:
            orm.commit()
        except:
            pass

    def save(self, category='create', user=None):
        bank = collipa.models.Bank.get_one()
        now = int(time.time())
        if category == 'create':
            self.created_at = now

            self.topic.reply_count += 1
            self.topic.last_reply_date = now
            self.topic.active = now
            self.floor = self.topic.reply_count
            self.author.reply_count += 1

            self.author.spend(coin=config.reply_create_coin,
                              role='reply-create', reply_id=self.id)
            bank.income(coin=config.reply_create_coin, role="reply-create",
                        reply_id=self.id, spender_id=self.author.id)

            if self.user_id != self.topic.user_id:
                receiver_id = self.topic.user_id
                topic_id = self.topic_id
                notification = collipa.models.Notification.get(receiver_id=receiver_id,
                                                               topic_id=topic_id,
                                                               role='reply')
                if notification:
                    if notification.switch == 1:
                        notification.status = 0
                        notification.updated_at = now
                else:
                    collipa.models.Notification(receiver_id=receiver_id,
                                                topic_id=topic_id,
                                                role='reply').save()

        if category == 'edit' and not user:
            self.author.spend(coin=config.reply_edit_coin,
                              role='reply-edit', reply_id=self.id)
            bank.income(coin=config.reply_edit_coin,
                        role='reply-edit',
                        reply_id=self.id,
                        spender_id=self.author.id)

        if not user:
            user = self.author

        self.updated_at = now
        self.active = now

        user.active = now

        return super(Reply, self).save()

    def remove(self, user=None):
        self.topic.reply_count -= 1
        self.author.reply_count -= 1
        for th in collipa.models.Thank.select(lambda rv: rv.reply_id == self.id):
            th.delete()
        for up in collipa.models.Up.select(lambda rv: rv.reply_id == self.id):
            up.delete()
        for dw in collipa.models.Down.select(lambda rv: rv.reply_id == self.id):
            dw.delete()
        for rp in collipa.models.Report.select(lambda rv: rv.reply_id == self.id):
            rp.delete()

        if not user:
            user = self.author
        user.active = int(time.time())

        super(Reply, self).remove()

    def get_uppers(self, after_date=None, before_date=None):
        if after_date:
            user_ids = orm.select(rv.user_id for rv in collipa.models.Up
                                  if rv.reply_id == self.id and rv.created_at > after_date)
        elif before_date:
            user_ids = orm.select(rv.user_id for rv in collipa.models.Up
                                  if rv.reply_id == self.id and rv.created_at < before_date)
        else:
            user_ids = orm.select(rv.user_id for rv in collipa.models.Up
                                  if rv.reply_id == self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda: orm.desc(rv.created_at))

            users = orm.select(rv for rv in collipa.models.User if rv.id in user_ids)
        return users

    def get_thankers(self, after_date=None, before_date=None):
        if after_date:
            user_ids = orm.select(rv.user_id for rv in collipa.models.Thank
                                  if rv.reply_id == self.id and rv.created_at > after_date)
        elif before_date:
            user_ids = orm.select(rv.user_id for rv in collipa.models.Thank
                                  if rv.reply_id == self.id and rv.created_at < before_date)
        else:
            user_ids = orm.select(rv.user_id for rv in collipa.models.Thank
                                  if rv.reply_id == self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda: orm.desc(rv.created_at))

            users = orm.select(rv for rv in collipa.models.User if rv.id in user_ids)
        return users

    @property
    def histories(self):
        histories = (collipa.models.History
                     .select(lambda rv: rv.reply_id == self.id)
                     .order_by(lambda: orm.desc(rv.created_at)))
        return histories

    def get_histories(self, page=1):
        histories = (collipa.models.History
                     .select(lambda rv: rv.reply_id == self.id)
                     .order_by(lambda: orm.desc(rv.created_at)))
        return histories[(page - 1) * config.paged: page * config.paged]

    @property
    def history_count(self):
        return orm.count(self.histories)

    def put_notifier(self):
        names = get_mention_names(self.content)
        for name in names:
            user = collipa.models.User.get(name=name)
            if user and user.id != self.topic.user_id:
                collipa.models.Notification(reply_id=self.id,
                                            receiver_id=user.id,
                                            role='mention').save()
        return self
