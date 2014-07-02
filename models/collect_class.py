# coding: utf-8

import time
from pony.orm import Required, Optional
from ._base import db, SessionMixin, ModelMixin
import config

config = config.rec()


class CollectClass(db.Entity, SessionMixin, ModelMixin):
    user_id = Required(int)
    name = Required(unicode)

    collect_count = Required(int, default=0)

    created_at = Required(int, default=int(time.time()))
    active = Required(int, default=int(time.time()))

    description = Optional(unicode)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<CollectClass: %s>' % self.id
