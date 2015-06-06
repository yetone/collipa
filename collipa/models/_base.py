# coding: utf-8

import collipa.models
from collipa.helpers import format_date, cached_property, get_mentions
from collipa import config
from pony import orm

__all__ = ['db', 'BaseModel']

db = orm.Database('mysql', config.db_host, config.db_user, config.db_pass, config.db_name)


# Cannot inherited from db.Entity, because the fucking design of Pony!!!
class BaseModel(object):
    def save(self):
        try:
            orm.commit()
        except:
            pass
        return self

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

    @staticmethod
    def get_compiled_content_mention_users(content):
        mentions = get_mentions(content)
        user_map = {}
        dp = 0
        for m in mentions:
            pos, username = m
            user = user_map.get(username) or collipa.models.User.get(name=username)
            if not user:
                continue
            user_map[username] = user
            replacement = '''<a class="mention" data-username="{username}" href="{url}">@{nickname}</a>'''.format(
                url=user.url,
                username=user.name,
                nickname=user.nickname,
                )
            content = content[:pos + dp] + replacement + content[pos + dp + len(username) + 1:]
            dp += len(replacement) - len(username) - 1
        return content, user_map.values()
