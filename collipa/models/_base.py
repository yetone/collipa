# coding: utf-8

import collipa.models
from collipa.helpers import format_date, cached_property
from collipa import config
from pony import orm

__all__ = ['db', 'BaseModel']

db = orm.Database('mysql', config.db_host, config.db_user, config.db_pass, config.db_name)


class SessionMixin(object):
    def save(self):
        try:
            orm.commit()
        except Exception:
            pass
        return self

    def remove(self):
        self.delete()
        try:
            orm.commit()
        except Exception:
            pass
        return self


class ModelMixin(object):
    @staticmethod
    def paginate(self, page, per_page):
        return self[(page - 1) * per_page, page * per_page]

    @cached_property
    def author(self):
        try:
            return collipa.models.User[self.user_id]
        except:
            return None

    @cached_property
    def topic(self):
        try:
            return collipa.models.Topic[self.topic_id]
        except:
            return None

    @cached_property
    def tweet(self):
        try:
            return collipa.models.Tweet[self.tweet_id]
        except:
            return None

    @cached_property
    def album(self):
        try:
            return collipa.models.Album[self.album_id]
        except:
            return None

    @cached_property
    def image(self):
        try:
            return collipa.models.Image[self.image_id]
        except:
            return None

    @cached_property
    def node(self):
        try:
            return collipa.models.Node[self.node_id]
        except:
            return None

    @cached_property
    def reply(self):
        try:
            return collipa.models.Reply[self.reply_id]
        except:
            return None

    @cached_property
    def created(self):
        try:
            return format_date(self.created_at)
        except:
            return None

    @cached_property
    def updated(self):
        try:
            return format_date(self.updated_at)
        except:
            return None

    @cached_property
    def actived(self):
        try:
            return format_date(self.active)
        except:
            return None

    @cached_property
    def collect_class(self):
        try:
            return collipa.models.CollectClass[self.collect_class_id]
        except:
            return None


class BaseModel(SessionMixin, ModelMixin):
    pass
