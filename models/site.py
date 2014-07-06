# coding: utf-8

from pony import orm
from ._base import db, SessionMixin, ModelMixin
import config

config = config.Config()


class Site(db.Entity, SessionMixin, ModelMixin):
    name = orm.Optional(unicode)

    help = orm.Optional(orm.LongUnicode)
    about = orm.Optional(orm.LongUnicode)
    contact = orm.Optional(orm.LongUnicode)
    service = orm.Optional(orm.LongUnicode)
    pravicy = orm.Optional(orm.LongUnicode)
    law = orm.Optional(orm.LongUnicode)
    description = orm.Optional(orm.LongUnicode)

    ico_img = orm.Optional(unicode, 400)
    head_img = orm.Optional(unicode, 400)
    background_img = orm.Optional(unicode, 400)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Site: %s>' % self.id
