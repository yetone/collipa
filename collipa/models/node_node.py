# coding: utf-8

import time
from pony import orm
from ._base import db, BaseModel


class NodeNode(db.Entity, BaseModel):
    parent_id = orm.Required(int)
    child_id = orm.Required(int)
    user_id = orm.Required(int, default=1)

    created_at = orm.Required(int, default=int(time.time()))

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<NodeNode: %s>' % self.id
