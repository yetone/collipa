# coding: utf-8

import os
import sys
import time
from pony import orm
from functools import partial
from concurrent import futures

from ._base import db, BaseModel
import collipa.models
from collipa import config
from collipa import helpers


class Image(db.Entity, BaseModel):
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
        return helpers.gen_thumb_url(self.path, (256, 0))

    @property
    def middle_path(self):
        return helpers.gen_thumb_url(self.path, (512, 0))

    @property
    def large_path(self):
        return helpers.gen_thumb_url(self.path, (1024, 0))

    def __setattr__(self, key, value):
        old_album_id = None
        if key == 'album_id':
            old_album_id = self.album_id
        super(Image, self).__setattr__(key, value)

        if key == 'album_id':
            album = collipa.models.Album.get(id=value)
            if album:
                album.cover = self
                self.created_at = int(time.time())
                try:
                    old_album = collipa.models.Album.get(id=old_album_id)
                    old_album.update_cover()
                except (TypeError, orm.ConstraintError, AttributeError):
                    pass

    def save(self, category='create', user=None):
        now = int(time.time())
        self.created_at = now
        self.updated_at = now

        self.author.image_count += 1
        self.album.image_count += 1
        self.author.active = now

        if category == 'create':
            self.album.cover = self

        return super(Image, self).save()

    def remove(self):
        now = int(time.time())

        self.author.image_count -= 1
        self.album.image_count -= 1
        self.author.active = now

        try:
            if not self.topic_id:
                os.system('rm -f %s%s' % (sys.path[0], self.path))
            album = self.album
            image_id = self.id
            image_path = self.path
            super(Image, self).remove()
            # 某一夜，脑残用了 image.id 作为 album 的 cover
            if album.cover_id in (image_id, image_path):
                album.update_cover()
            return True
        except:
            return False

    def get_uppers(self, after_date=None, before_date=None):
        if after_date:
            user_ids = orm.select(rv.user_id for rv in collipa.models.Up if rv.image_id == self.id and rv.created_at > after_date)
        elif before_date:
            user_ids = orm.select(rv.user_id for rv in collipa.models.Up if rv.image_id == self.id and rv.created_at < before_date)
        else:
            user_ids = orm.select(rv.user_id for rv in collipa.models.Up if rv.image_id == self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda rv: orm.desc(rv.created_at))

            users = orm.select(rv for rv in collipa.models.User if rv.id in user_ids)
        return users

    def get_thankers(self, after_date=None, before_date=None):
        if after_date:
            user_ids = orm.select(rv.user_id for rv in collipa.models.Thank if rv.image_id == self.id and rv.created_at > after_date)
        elif before_date:
            user_ids = orm.select(rv.user_id for rv in collipa.models.Thank if rv.image_id == self.id and rv.created_at < before_date)
        else:
            user_ids = orm.select(rv.user_id for rv in collipa.models.Thank if rv.image_id == self.id)
        users = []
        if user_ids:
            user_ids = user_ids.order_by(lambda rv: orm.desc(rv.created_at))

            users = orm.select(rv for rv in collipa.models.User if rv.id in user_ids)
        return users

    def crop(self):
        size_list = [(128, 128), (256, 256), (512, 512), (1024, 1024), (128, 0), (256, 0), (512, 0), (1024, 0)]
        crop = partial(helpers.crop, self.path)
        with futures.ThreadPoolExecutor(max_workers=len(size_list)) as exe:
            list(exe.map(crop, size_list))

    def to_simple_dict(self):
        data = {
            'id': self.id,
            'url': self.url,
            'path': self.path,
            'small_path': self.small_path,
            'width': self.width,
            'height': self.height,
            'created_at': self.created_at,
            'created': self.created,
        }
        return data

    def to_dict(self):
        data = {
            'author': self.author.to_simple_dict(),
            'album': self.album.to_simple_dict(),
        }
        data.update(self.to_simple_dict())
        return data

    @staticmethod
    def query_by_album_id(album_id, from_id=None, limit=None, desc=True):
        limit = limit or config.paged
        images = orm.select(rv for rv in Image if rv.album_id == album_id)
        if desc:
            images = images.order_by(lambda rv: orm.desc(rv.created_at))
        else:
            images = images.order_by(lambda rv: rv.created_at)
        if from_id:
            i = -1
            for i, image in enumerate(images):
                if i == 1000:
                    return []
                if image.id == from_id:
                    break
            images = images[i + 1: i + 1 + limit]
            return images
        return images
