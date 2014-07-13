# coding: utf-8

import os
import sys
import time
from pony import orm
from ._base import db, SessionMixin, ModelMixin
import models as m
import config
import helpers

config = config.Config()


class Image(db.Entity, SessionMixin, ModelMixin):
    user_id = orm.Required(int)
    topic_id = orm.Optional(int)
    reply_id = orm.Optional(int)
    album_id = orm.Required(int)
    tweet_id = orm.Optional(int)
    width = orm.Required(int)
    height = orm.Required(int)

    path = orm.Required(unicode, 400)

    role = orm.Required(unicode, 10, default='image')
    compute_count = orm.Required(int, default=config.reply_compute_count)

    thank_count = orm.Required(int, default=0)
    up_count = orm.Required(int, default=0)
    down_count = orm.Required(int, default=0)
    report_count = orm.Required(int, default=0)
    collect_count = orm.Required(int, default=0)

    created_at = orm.Required(int, default=int(time.time()))
    updated_at = orm.Required(int, default=int(time.time()))

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Image: %s>' % self.id

    @property
    def url(self):
        return '/image/%s' % self.id

    @property
    def small_path(self):
        return helpers.generate_thumb_url(self.path, (256, 0))

    @property
    def middle_path(self):
        return helpers.generate_thumb_url(self.path, (512, 0))

    @property
    def large_path(self):
        return helpers.generate_thumb_url(self.path, (1024, 0))

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
            user_ids = orm.select(rv.user_id for rv in m.Up if rv.image_id == self.id and rv.created_at > after_date)
        elif before_date:
            user_ids = orm.select(rv.user_id for rv in m.Up if rv.image_id == self.id and rv.created_at < before_date)
        else:
            user_ids = orm.select(rv.user_id for rv in m.Up if rv.image_id == self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda rv: orm.desc(rv.created_at))

            users = orm.select(rv for rv in m.User if rv.id in user_ids)
        return users

    def get_thankers(self, after_date=None, before_date=None):
        if after_date:
            user_ids = orm.select(rv.user_id for rv in m.Thank if rv.image_id == self.id and rv.created_at > after_date)
        elif before_date:
            user_ids = orm.select(rv.user_id for rv in m.Thank if rv.image_id == self.id and rv.created_at < before_date)
        else:
            user_ids = orm.select(rv.user_id for rv in m.Thank if rv.image_id == self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda rv: orm.desc(rv.created_at))

            users = orm.select(rv for rv in m.User if rv.id in user_ids)
        return users

    def crop(self):
        size_list = [(128, 128), (256, 256), (512, 512), (1024, 1024), (128, 0), (256, 0), (512, 0), (1024, 0)]
        for size in size_list:
            helpers.crop(self.path, size)
