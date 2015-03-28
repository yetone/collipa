# coding: utf-8

import time
from pony import orm
from ._base import db, BaseModel


class CollectClass(db.Entity, BaseModel):
    user_id = orm.Required(int)
    name = orm.Required(unicode)

    collect_count = orm.Required(int, default=0)

    created_at = orm.Required(int, default=int(time.time()))
    active = orm.Required(int, default=int(time.time()))

    description = orm.Optional(unicode)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<CollectClass: %s>' % self.id
