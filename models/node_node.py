# coding: utf-8

import time
from pony.orm import Required
from ._base import db, SessionMixin, ModelMixin
import config

config = config.rec()


class NodeNode(db.Entity, SessionMixin, ModelMixin):
    parent_id = Required(int)
    child_id = Required(int)
    user_id = Required(int, default=1)

    created_at = Required(int, default=int(time.time()))

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<NodeNode: %s>' % self.id
