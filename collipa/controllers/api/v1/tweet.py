__author__ = 'yetone'

from pony import orm
from collipa.models import Tweet
from collipa.controllers._base import BaseHandler


class ListHandler(BaseHandler):
    @orm.db_session
    def get(self):
        page = self.get_int('page', 1)
        from_id = self.get_int('from_id', 0)
        tweets = Tweet.get_timeline(page=page, from_id=from_id)
        return self.send_success_json(object_list=[tweet.to_dict() for tweet in tweets])
