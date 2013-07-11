# coding: utf-8

import time
from pony.orm import *
from ._base import db, SessionMixin, ModelMixin
import config
import models as m

config = config.rec()

class Topic(db.Entity, SessionMixin, ModelMixin):
    user_id = Required(int)
    node_id = Required(int)

    title = Required(unicode)
    content = Required(LongUnicode)

    hits = Required(int, default=0)
    role = Required(unicode, 10, default='topic')
    compute_count = Required(int, default=config.topic_compute_count)

    reply_count = Required(int, default=0)
    thank_count = Required(int, default=0)
    up_count = Required(int, default=0)
    down_count = Required(int, default=0)
    report_count = Required(int, default=0)
    collect_count = Required(int, default=0)
    follow_count = Required(int, default=0)

    created_at = Required(int, default=int(time.time()))
    updated_at = Required(int, default=int(time.time()))
    active = Required(int, default=int(time.time()))

    last_reply_date = Required(int, default=int(time.time()))

    topic_id = Optional(int)

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Topic: %s>' % self.id

    @property
    def url(self):
        return '/topic/%s' % self.id

    @property
    def url_sharp(self):
        return '/topic/%s#reply%s' % (self.id, self.reply_count)

    @property
    def replies(self):
        replies = m.Reply.select(lambda rv: rv.topic_id ==
                self.id).order_by(lambda rv: desc(rv.created_at))
        return replies

    def get_replies(self, page=1, category='all', order_by='created_at',
            limit=None):
        if category == 'all':
            replies = m.Reply.select(lambda rv: rv.topic_id ==
                    self.id)
        else:
            if category == 'hot':
                replies = m.Reply.select(lambda rv: rv.topic_id ==
                        self.id)
                #now = int(time.time())
                #ago = now - 60 * 60 * 24
                #replies = select(rv for rv in m.Reply if rv.topic_id == self.id
                #        and rv.created_at > ago)
                limit = 10
                order_by = 'smart'
            elif category == 'author':
                replies = select(rv for rv in m.Reply if rv.topic_id == self.id
                        and rv.user_id == self.user_id)
            else:
                replies = select(rv for rv in m.Reply if rv.topic_id ==
                        self.id and rv.role == category)

        if order_by == 'smart':
            replies = replies.order_by(lambda rv: desc((rv.collect_count +
                rv.thank_count) * 10 + (rv.up_count - rv.down_count) * 5))
        else:
            replies = replies.order_by(lambda rv: rv.created_at)

        if limit:
            return replies[:limit]
        if page:
            return replies[(page - 1) * config.reply_paged: page *
                    config.reply_paged]
        else:
            return replies

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

            if not m.Bill.get(user_id=self.author.id, role='topic-hot',
                    topic_id=self.id):
                self.author.income(coin=config.topic_hot_coin, role='topic-hot', topic_id=self.id)
                bank = m.Bank.get_one()
                bank.spend(coin=config.topic_hot_coin, role='topic-hot',
                        topic_id=self.id)
        if self.report_count > 12 and self.up_count < 5:
            self.role = 'report'

            if not m.Bill.get(user_id=self.author.id, role='topic-report',
                    topic_id=self.id):
                self.author.spend(coin=config.topic_report_coin,
                        role='topic-report', topic_id=self.id)
                bank = m.Bank.get_one()
                bank.income(coin=config.topic_report_coin, role='topic-report',
                        topic_id=self.id)

        try:
            commit()
        except:
            pass

    def save(self, category='create', user=None):
        bank = m.Bank.get_one()
        now = int(time.time())

        if category == 'create':
            self.created_at = now
            self.last_reply_date = now

            self.node.topic_count += 1
            self.author.topic_count += 1

            self.author.spend(coin=config.topic_create_coin, role="topic-create", topic_id=self.id)
            bank.income(coin=config.topic_create_coin, role="topic-create", topic_id=self.id,
                    spender_id=self.author.id)

        if category == 'edit' and not user:
            self.author.spend(coin=config.topic_edit_coin, role='topic-edit', topic_id=self.id)
            bank.income(coin=config.topic_edit_coin, role='topic-edit', topic_id=self.id,
                    spender_id=self.author.id)

        if not user:
            user = self.author

        self.updated_at = now
        self.active = now

        self.node.active = now
        user.active = now

        return super(Topic, self).save()

    def move(self, user=None, node=None):
        if not node:
            return self
        if self.node_id == node.id:
            return self

        old_node = m.Node.get(self.node_id)
        old_node.topic_count -= 1
        self.node_id = node.id
        node.topic_count += 1

        if not user:
            user = self.author

        now = int(time.time())
        user.active = now
        self.node.active = now

        try:
            commit()
        except:
            pass

    def remove(self, user=None):
        self.node.topic_count -= 1
        self.author.topic_count -= 1
        for th in m.Thank.select(lambda rv: rv.topic_id == self.id):
            th.delete()
        for up in m.Up.select(lambda rv: rv.topic_id == self.id):
            up.delete()
        for dw in m.Down.select(lambda rv: rv.topic_id == self.id):
            dw.delete()
        for rp in m.Report.select(lambda rv: rv.topic_id == self.id):
            rp.delete()
        for reply in self.replies:
            reply.remove()

        if not user:
            user = self.author
        user.active = int(time.time())

        super(Topic, self).remove()

    def get_uppers(self, after_date=None, before_date=None):
        if after_date:
            user_ids = select(rv.user_id for rv in m.Up if rv.topic_id ==
                    self.id and rv.created_at >
                    after_date)
        elif before_date:
            user_ids = select(rv.user_id for rv in m.Up if rv.topic_id ==
                    self.id and rv.created_at <
                    before_date)
        else:
            user_ids = select(rv.user_id for rv in m.Up if rv.topic_id ==
                    self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda rv: desc(rv.created_at))

            users = select(rv for rv in m.User if rv.id in user_ids)
        return users

    def get_thankers(self, after_date=None, before_date=None):
        if after_date:
            user_ids = select(rv.user_id for rv in m.Thank if rv.topic_id ==
                    self.id and rv.created_at >
                    after_date)
        elif before_date:
            user_ids = select(rv.user_id for rv in m.Thank if rv.topic_id ==
                    self.id and rv.created_at <
                    before_date)
        else:
            user_ids = select(rv.user_id for rv in m.Thank if rv.topic_id ==
                    self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda rv: desc(rv.created_at))

            users = select(rv for rv in m.User if rv.id in user_ids)
        return users

    def get_replyers(self, after_date=None, before_date=None):
        if after_date:
            user_ids = select(rv.user_id for rv in m.Reply if rv.topic_id ==
                    self.id and rv.user_id != self.user_id and rv.created_at >
                    after_date)
        elif before_date:
            user_ids = select(rv.user_id for rv in m.Reply if rv.topic_id ==
                    self.id and rv.user_id != self.user_id and rv.created_at <
                    before_date)
        else:
            user_ids = select(rv.user_id for rv in m.Reply if rv.topic_id ==
                    self.id and rv.user_id != self.user_id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda rv: desc(rv.created_at))

            users = select(rv for rv in m.User if rv.id in user_ids)
        return users

    @property
    def histories(self):
        histories = m.History.select(lambda rv: rv.topic_id ==
                self.id).order_by(lambda rv: desc(rv.created_at))
        return histories

    def get_histories(self, page=1):
        histories = m.History.select(lambda rv: rv.topic_id ==
                self.id).order_by(lambda rv: desc(rv.created_at))
        return histories[(page - 1) * config.paged: page * config.paged]

    @property
    def history_count(self):
        return count(self.histories)
