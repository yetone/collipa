# coding: utf-8

import time
from pony.orm import *
from ._base import db, SessionMixin, ModelMixin
import models as m
import config
from helpers import get_mention_names

config = config.rec()

class Reply(db.Entity, SessionMixin, ModelMixin):
    user_id = Required(int)
    topic_id = Optional(int)
    tweet_id = Optional(int)
    image_id = Optional(int)

    content = Required(LongUnicode)

    role = Required(unicode, 10, default='reply')
    compute_count = Required(int, default=config.reply_compute_count)

    thank_count = Required(int, default=0)
    up_count = Required(int, default=0)
    down_count = Required(int, default=0)
    report_count = Required(int, default=0)
    collect_count = Required(int, default=0)

    floor = Required(int, default=1)

    created_at = Required(int, default=int(time.time()))
    updated_at = Required(int, default=int(time.time()))
    active = Required(int, default=int(time.time()))

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
        if self.role == 'up' and self.reply_count > 20 and self.reply_hits > 60:
            self.role = 'hot'

            if not m.Bill.get(user_id=self.author.id, role='reply-hot',
                    reply_id=self.id):
                self.author.income(coin=config.reply_hot_coin,
                        role='reply-hot', reply_id=self.id)
                bank = m.Bank.get_one()
                bank.spend(coin=config.reply_hot_coin, role='reply-hot',
                        reply_id=self.id)
        if self.report_count > 12 and self.up_count < 5:
            self.role = 'report'

            if not m.Bill.get(user_id=self.author.id, role='reply-report',
                    reply_id=self.id):
                self.author.spend(coin=config.reply_report_coin,
                        role='reply-report', reply_id=self.id)
                bank = m.Bank.get_one()
                bank.income(coin=config.reply_report_coin, role='reply-report',
                        reply_id=self.id)

        try:
            commit()
        except:
            pass

    def save(self, category='create', user=None):
        bank = m.Bank.get_one()
        now = int(time.time())
        if category == 'create':
            self.created_at = now

            self.topic.reply_count += 1
            self.topic.last_reply_date = now
            self.topic.active = now
            self.floor = self.topic.reply_count
            self.author.reply_count += 1

            self.author.spend(coin=config.reply_create_coin, role='reply-create', reply_id=self.id)
            bank.income(coin=config.reply_create_coin, role="reply-create",
                    reply_id=self.id, spender_id=self.author.id)

            if self.user_id != self.topic.user_id:
                receiver_id = self.topic.user_id
                topic_id = self.topic_id
                notification = m.Notification.get(receiver_id=receiver_id,
                        topic_id=topic_id, role='reply')
                if notification:
                    if notification.switch == 1:
                        notification.status = 0
                        notification.updated_at = now
                else:
                    notification = m.Notification(receiver_id=receiver_id,
                            topic_id=topic_id, role='reply').save()

        if category == 'edit' and not user:
            self.author.spend(coin=config.reply_edit_coin, role='reply-edit', reply_id=self.id)
            bank.income(coin=config.reply_edit_coin, role='reply-edit', reply_id=self.id,
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
        for th in m.Thank.select(lambda rv: rv.reply_id == self.id):
            th.delete()
        for up in m.Up.select(lambda rv: rv.reply_id == self.id):
            up.delete()
        for dw in m.Down.select(lambda rv: rv.reply_id == self.id):
            dw.delete()
        for rp in m.Report.select(lambda rv: rv.reply_id == self.id):
            rp.delete()

        if not user:
            user = self.author
        user.active = int(time.time())

        super(Reply, self).remove()

    def get_uppers(self, after_date=None, before_date=None):
        if after_date:
            user_ids = select(rv.user_id for rv in m.Up if rv.reply_id ==
                    self.id and rv.created_at >
                    after_date)
        elif before_date:
            user_ids = select(rv.user_id for rv in m.Up if rv.reply_id ==
                    self.id and rv.created_at <
                    before_date)
        else:
            user_ids = select(rv.user_id for rv in m.Up if rv.reply_id ==
                    self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda rv: desc(rv.created_at))

            users = select(rv for rv in m.User if rv.id in user_ids)
        return users

    def get_thankers(self, after_date=None, before_date=None):
        if after_date:
            user_ids = select(rv.user_id for rv in m.Thank if rv.reply_id ==
                    self.id and rv.created_at >
                    after_date)
        elif before_date:
            user_ids = select(rv.user_id for rv in m.Thank if rv.reply_id ==
                    self.id and rv.created_at <
                    before_date)
        else:
            user_ids = select(rv.user_id for rv in m.Thank if rv.reply_id ==
                    self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda rv: desc(rv.created_at))

            users = select(rv for rv in m.User if rv.id in user_ids)
        return users

    @property
    def histories(self):
        histories = m.History.select(lambda rv: rv.reply_id ==
                self.id).order_by(lambda rv: desc(rv.created_at))
        return histories

    def get_histories(self, page=1):
        histories = m.History.select(lambda rv: rv.reply_id ==
                self.id).order_by(lambda rv: desc(rv.created_at))
        return histories[(page - 1) * config.paged: page * config.paged]

    @property
    def history_count(self):
        return count(self.histories)

    def put_notifier(self):
        if 'class="mention"' not in self.content:
            return self
        names = get_mention_names(self.content)
        for name in names:
            user = m.User.get(name=name)
            if user and user.id != self.topic.user_id:
                m.Notification(reply_id=self.id, receiver_id=user.id,
                        role='mention').save()
        return self
