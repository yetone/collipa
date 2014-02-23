# coding: utf-8

import time
from pony.orm import *
from ._base import db, SessionMixin, ModelMixin
import models as m
import config
from helpers import get_mention_names

config = config.rec()

class Image(db.Entity, SessionMixin, ModelMixin):
    user_id = Required(int)
    topic_id = Optional(int)
    reply_id = Optional(int)
    album_id = Required(int)
    tweet_id = Optional(int)
    width = Required(int)
    height = Required(int)

    path = Required(unicode, 400)

    role = Required(unicode, 10, default='image')
    compute_count = Required(int, default=config.reply_compute_count)

    thank_count = Required(int, default=0)
    up_count = Required(int, default=0)
    down_count = Required(int, default=0)
    report_count = Required(int, default=0)
    collect_count = Required(int, default=0)

    created_at = Required(int, default=int(time.time()))
    updated_at = Required(int, default=int(time.time()))

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Image: %s>' % self.id

    @property
    def url(self):
        return '/image/%s' % self.id

    def save(self, category='create', user=None):
        now = int(time.time())
        self.created_at = now
        self.updated_at = now

        self.author.image_count += 1
        self.album.image_count += 1
        self.author.active = now

        return super(Image, self).save()

    def remove(self):
        now = int(time.time())

        self.author.image_count -= 1
        self.album.image_count -= 1
        self.author.active = now

        try:
            os.system('rm -f %s%s' % (sys.path[0], self.path))
            return True
        except:
            return False

        super(Image, self).remove()

    def get_uppers(self, after_date=None, before_date=None):
        if after_date:
            user_ids = select(rv.user_id for rv in m.Up if rv.image_id ==
                    self.id and rv.created_at >
                    after_date)
        elif before_date:
            user_ids = select(rv.user_id for rv in m.Up if rv.image_id ==
                    self.id and rv.created_at <
                    before_date)
        else:
            user_ids = select(rv.user_id for rv in m.Up if rv.image_id ==
                    self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda rv: desc(rv.created_at))

            users = select(rv for rv in m.User if rv.id in user_ids)
        return users

    def get_thankers(self, after_date=None, before_date=None):
        if after_date:
            user_ids = select(rv.user_id for rv in m.Thank if rv.image_id ==
                    self.id and rv.created_at >
                    after_date)
        elif before_date:
            user_ids = select(rv.user_id for rv in m.Thank if rv.image_id ==
                    self.id and rv.created_at <
                    before_date)
        else:
            user_ids = select(rv.user_id for rv in m.Thank if rv.image_id ==
                    self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda rv: desc(rv.created_at))

            users = select(rv for rv in m.User if rv.id in user_ids)
        return users
