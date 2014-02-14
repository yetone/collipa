# coding: utf-8

import time
from pony.orm import *
from ._base import db, SessionMixin, ModelMixin
import models as m
import config
from helpers import get_mention_names

config = config.rec()


class Tweet(db.Entity, SessionMixin, ModelMixin):
    user_id = Required(int)

    content = Required(LongUnicode)

    role = Required(unicode, 10, default='tweet')

    thank_count = Required(int, default=0)
    up_count = Required(int, default=0)
    down_count = Required(int, default=0)
    report_count = Required(int, default=0)
    collect_count = Required(int, default=0)

    created_at = Required(int, default=int(time.time()))
    updated_at = Required(int, default=int(time.time()))
    active = Required(int, default=int(time.time()))

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Tweet: %s>' % self.id

    @property
    def url(self):
        return '/tweet/%s' % self.id

    def save(self, category='create', user=None):
        now = int(time.time())
        if category == 'create':
            self.created_at = now
            self.author.tweet_count += 1

        if not user:
            user = self.author

        self.updated_at = now
        self.active = now

        user.active = now

        return super(Tweet, self).save()

    def remove(self, user=None):
        self.author.tweet_count -= 1
        for th in m.Thank.select(lambda rv: rv.tweet_id == self.id):
            th.delete()
        for up in m.Up.select(lambda rv: rv.tweet_id == self.id):
            up.delete()
        for dw in m.Down.select(lambda rv: rv.tweet_id == self.id):
            dw.delete()
        for rp in m.Report.select(lambda rv: rv.tweet_id == self.id):
            rp.delete()

        if not user:
            user = self.author
        user.active = int(time.time())

        super(Tweet, self).remove()

    def get_uppers(self, after_date=None, before_date=None):
        if after_date:
            user_ids = select(rv.user_id for rv in m.Up if rv.tweet_id ==
                    self.id and rv.created_at >
                    after_date)
        elif before_date:
            user_ids = select(rv.user_id for rv in m.Up if rv.tweet_id ==
                    self.id and rv.created_at <
                    before_date)
        else:
            user_ids = select(rv.user_id for rv in m.Up if rv.tweet_id ==
                    self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda rv: desc(rv.created_at))

            users = select(rv for rv in m.User if rv.id in user_ids)
        return users

    def get_thankers(self, after_date=None, before_date=None):
        if after_date:
            user_ids = select(rv.user_id for rv in m.Thank if rv.tweet_id ==
                    self.id and rv.created_at >
                    after_date)
        elif before_date:
            user_ids = select(rv.user_id for rv in m.Thank if rv.tweet_id ==
                    self.id and rv.created_at <
                    before_date)
        else:
            user_ids = select(rv.user_id for rv in m.Thank if rv.tweet_id ==
                    self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda rv: desc(rv.created_at))

            users = select(rv for rv in m.User if rv.id in user_ids)
        return users

    def put_notifier(self):
        if 'class="mention"' not in self.content:
            return self
        names = get_mention_names(self.content)
        for name in names:
            user = m.User.get(name=name)
            if user and user.id != self.topic.user_id:
                m.Notification(tweet_id=self.id, receiver_id=user.id,
                        role='mention').save()
        return self
