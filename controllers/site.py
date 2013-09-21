# coding: utf-8

import tornado.web

import time
import config
from ._base import BaseHandler
from pony.orm import *

from models import Topic
from extensions import mc
from helpers import force_int

config = config.rec()

class HomeHandler(BaseHandler):
    @db_session
    def get(self):
        page = force_int(self.get_argument('page', 1), 1)
        category = self.get_argument('category', None)
        view = self.get_argument('view', 'all')
        user = self.current_user
        if not category:
            category = self.index_category
        else:
            self.set_index_category(category)
        if category == 'timeline' and not user:
            category = self.set_index_category('index')
        if category == 'hot':
            topics = mc.get('hot_topics')
            if not topics:
                now = int(time.time())
                ago = now - 60 * 60 * 24
                topics = select(rv for rv in Topic if rv.created_at > ago).order_by(lambda rv:
                        desc((rv.collect_count + rv.thank_count - rv.report_count) * 10 +
                        (rv.up_count - rv.down_count) * 5 + rv.reply_count *
                        3))
                mc.set('hot_topics', list(topics), 60 * 60 * 2)
        elif category == 'timeline':
            topics = user.get_timeline(page=None, category=view)
        elif category == 'latest':
            topics = select(rv for rv in Topic).order_by(lambda rv:
                    desc(rv.created_at))
        elif category == 'desert':
            topics = select(rv for rv in Topic if rv.reply_count == 0).order_by(lambda rv:
                    desc(rv.created_at))
        else:
            topics = select(rv for rv in Topic).order_by(lambda rv: desc(rv.last_reply_date))
        topic_count = count(topics)
        topics = topics[(page - 1) * config.paged: page * config.paged]
        page_count = (topic_count + config.paged - 1) // config.paged
        return self.render("site/index.html", topics=topics, category=category,
                page=page, view=view, page_count=page_count, url='/')

class PageNotFoundHandler(BaseHandler):
    def get(self):
        return self.render("site/404.html")

class PageErrorHandler(BaseHandler):
    def get(self):
        return self.render("site/502.html")

class OtherPageErrorHandler(BaseHandler):
    def get(self):
        raise tornado.web.HTTPError(302)
