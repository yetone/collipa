# coding: utf-8

import time
from pony import orm
from ._base import db, SessionMixin, ModelMixin
import models as m
import config
from helpers import get_mention_names

config = config.Config()


class Tweet(db.Entity, SessionMixin, ModelMixin):
    user_id = orm.Required(int)

    content = orm.Required(orm.LongUnicode)

    role = orm.Required(unicode, 10, default='tweet')

    thank_count = orm.Required(int, default=0)
    up_count = orm.Required(int, default=0)
    down_count = orm.Required(int, default=0)
    report_count = orm.Required(int, default=0)
    collect_count = orm.Required(int, default=0)

    created_at = orm.Required(int, default=int(time.time()))
    updated_at = orm.Required(int, default=int(time.time()))
    active = orm.Required(int, default=int(time.time()))
    has_img = orm.Optional(unicode, 10)

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
            user_ids = orm.select(rv.user_id for rv in m.Up if rv.tweet_id == self.id and rv.created_at > after_date)
        elif before_date:
            user_ids = orm.select(rv.user_id for rv in m.Up if rv.tweet_id == self.id and rv.created_at < before_date)
        else:
            user_ids = orm.select(rv.user_id for rv in m.Up if rv.tweet_id == self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda rv: orm.desc(rv.created_at))

            users = orm.select(rv for rv in m.User if rv.id in user_ids)
        return users

    def get_thankers(self, after_date=None, before_date=None):
        if after_date:
            user_ids = orm.select(rv.user_id for rv in m.Thank if rv.tweet_id == self.id and rv.created_at > after_date)
        elif before_date:
            user_ids = orm.select(rv.user_id for rv in m.Thank if rv.tweet_id == self.id and rv.created_at < before_date)
        else:
            user_ids = orm.select(rv.user_id for rv in m.Thank if rv.tweet_id == self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda rv: orm.desc(rv.created_at))

            users = orm.select(rv for rv in m.User if rv.id in user_ids)
        return users

    def put_notifier(self):
        if 'class="mention"' not in self.content:
            return self
        names = get_mention_names(self.content)
        for name in names:
            user = m.User.get(name=name)
            if user and user.id != self.user_id:
                m.Notification(tweet_id=self.id, receiver_id=user.id,
                               role='mention').save()
        return self

    @staticmethod
    def get_timeline(page=1, from_id=None, count=config.paged):
        if not from_id:
            tweets = orm.select(rv for rv in Tweet).order_by(lambda rv:
                                                             orm.desc(rv.created_at))[(page - 1) * count: page * count]
        else:
            tweets = orm.select(rv for rv in m.Tweet if rv.id < from_id).order_by(lambda rv:
                                                                                 orm.desc(rv.created_at))[:count]
        return tweets

    @property
    def images(self):
        return m.Image.select(lambda rv: rv.tweet_id == self.id)
