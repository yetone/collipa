# coding: utf-8

import tornado.web

import time
from ._base import BaseHandler
from pony import orm

from collipa.models import Topic, Tweet
from collipa.extensions import mc
from collipa.helpers import force_int
from collipa import config


class CommunityHandler(BaseHandler):
    @orm.db_session
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
                topics = orm.select(rv for rv in Topic if
                                    rv.created_at > ago).order_by(lambda:
                                                                  orm.desc((rv.collect_count + rv.thank_count
                                                                            - rv.report_count) * 10 +
                                                                           (rv.up_count - rv.down_count) * 5 +
                                                                           rv.reply_count * 3))
                mc.set('hot_topics', list(topics), 60 * 60 * 2)
        elif category == 'timeline':
            topics = user.get_followed_topics(page=None, category=view)
        elif category == 'latest':
            topics = orm.select(rv for rv in Topic).order_by(lambda:
                                                             orm.desc(rv.created_at))
        elif category == 'desert':
            topics = orm.select(rv for rv in Topic if rv.reply_count == 0).order_by(lambda:
                                                                                    orm.desc(rv.created_at))
        else:
            topics = orm.select(rv for rv in Topic).order_by(lambda: orm.desc(rv.last_reply_date))
        topic_count = orm.count(topics)
        topics = topics[(page - 1) * config.paged: page * config.paged]
        page_count = (topic_count + config.paged - 1) // config.paged
        return self.render("site/index.html", topics=topics, category=category,
                           page=page, view=view, page_count=page_count, url='/')


class TimelineHandler(BaseHandler):
    @orm.db_session
    def get(self):
        page = self.get_int('page', 1)
        from_id = self.get_int('from_id', 0)
        user = self.current_user
        if not user:
            return self.redirect('/timeline/public')
        tweets = user.get_timeline(page=page, from_id=from_id)
        return self.render("site/timeline.html",
                           tweets=tweets,
                           cate='private',
                           page=page)


class PublicTimelineHandler(BaseHandler):
    @orm.db_session
    def get(self):
        page = self.get_int('page', 1)
        from_id = self.get_int('from_id', 0)
        tweets = Tweet.get_timeline(page=page, from_id=from_id)
        return self.render("site/timeline.html",
                           tweets=tweets,
                           cate='public',
                           page=page)


class MeTimelineHandler(BaseHandler):
    @orm.db_session
    @tornado.web.authenticated
    def get(self):
        page = self.get_int('page', 1)
        from_id = self.get_int('from_id', 0)
        tweets = Tweet.get_timeline(page=page, from_id=from_id, user_id=self.current_user.id)
        return self.render("site/timeline.html",
                           tweets=tweets,
                           cate='me',
                           page=page)


class PageNotFoundHandler(BaseHandler):
    @orm.db_session
    def get(self):
        return self.render("site/404.html")


class PageErrorHandler(BaseHandler):
    @orm.db_session
    def get(self):
        return self.render("site/502.html")


class OtherPageErrorHandler(BaseHandler):
    def get(self):
        raise tornado.web.HTTPError(302)
