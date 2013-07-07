# coding: utf-8

import time
from pony.orm import *
from ._base import db, SessionMixin, ModelMixin
import config
import models as m

from helpers import strip_tags
from extensions import mc

config = config.rec()

class Node(db.Entity, SessionMixin, ModelMixin):
    user_id = Required(int, default=1)

    name = Required(unicode, 80, unique=True)
    urlname = Required(unicode, 80, unique=True)

    topic_count = Required(int, default=0)
    follow_count = Required(int, default=0)
    role = Required(unicode, 10, default='node')

    created_at = Required(int, default=int(time.time()))
    updated_at = Required(int, default=int(time.time()))
    active = Required(int, default=int(time.time()))

    description = Optional(LongUnicode)
    summary = Optional(LongUnicode)
    style = Optional(unicode, 6000)

    icon_img = Optional(unicode, 400)
    head_img = Optional(unicode, 400)
    background_img = Optional(unicode, 400)

    @property
    def url(self):
        return '/node/' + self.urlname

    @property
    def icon(self):
        if self.icon_img:
            return self.icon_img
        else:
            return config.node_icon_url

    @property
    def head(self):
        if self.head_img:
            return self.head_img
        else:
            return config.node_head_url

    @property
    def background(self):
        if self.background_img:
            return self.background_img
        else:
            return config.node_background_url

    @property
    def parent_node_ids(self):
        parent_ids = select(nn.parent_id for nn in m.NodeNode if
                nn.child_id == self.id)
        return parent_ids if parent_ids else [0]

    @property
    def parent_nodes(self):
        parent_id_list = select(nn.parent_id for nn in m.NodeNode if
                nn.child_id == self.id)[:]
        if parent_id_list:
            nodes = Node.get_items_by_id(parent_id_list)
            return nodes
        else:
            return []

    @property
    def child_nodes(self):
        child_id_list = select(nn.child_id for nn in m.NodeNode if
                nn.parent_id == self.id)[:]
        if child_id_list:
            nodes = Node.get_items_by_id(child_id_list)
            return nodes
        else:
            return []

    @property
    def sibling_nodes(self):
        parent_ids = self.parent_node_ids
        sibling_id_list = select(nn.child_id for nn in m.NodeNode if
                nn.parent_id in parent_ids and nn.child_id != self.id)[:]
        if sibling_id_list:
            nodes = Node.get_items_by_id(sibling_id_list)
            return nodes
        else:
            return []

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Node: %s>' % self.urlname

    @staticmethod
    def get_items_by_id(id_list):
        nodes = Node.select(lambda n: n.id in id_list)
        return nodes

    def get_topics(self, page=1, category='all', order_by='created_at'):
        if category == 'all':
            topics = select(rv for rv in m.Topic if rv.node_id ==
                    self.id)
            order_by = 'last_reply_date'

        else:
            if category == 'hot':
                topics = mc.get('node_%s_hot_topics' % self.id)
                if not topics:
                    now = int(time.time())
                    ago = now - 60 * 60 * 24
                    topics = select(rv for rv in m.Topic if rv.node_id == self.id
                            and rv.created_at > ago)
                    topics = topics.order_by(lambda rv: desc((rv.collect_count +
                            rv.thank_count - rv.report_count) * 10 + (rv.up_count -
                                rv.down_count) * 5 + rv.reply_count * 3))
                    mc.set('node_%s_hot_topics' % self.id, list(topics), 60 *
                            60 * 3)
                order_by = 'none'
            elif category == 'latest':
                topics = select(rv for rv in m.Topic if rv.node_id ==
                        self.id)
            elif category == 'desert':
                topics = select(rv for rv in m.Topic if rv.node_id ==
                        self.id and rv.reply_count == 0)
            else:
                topics = select(rv for rv in m.Topic if rv.node_id ==
                        self.id and rv.role == category)
                order_by = 'last_reply_date'

        if order_by == 'last_reply_date':
            topics = topics.order_by(lambda rv: desc(rv.last_reply_date))
        elif order_by == 'created_at':
            topics = topics.order_by(lambda rv: desc(rv.created_at))
        elif order_by == 'active':
            topics = topics.order_by(lambda rv: desc(rv.active))
        elif order_by == 'smart':
            topics = topics.order_by(lambda rv: desc((rv.collect_count +
                    rv.thank_count - rv.report_count) * 10 + (rv.up_count -
                        rv.down_count) * 5 + rv.reply_count * 3))

        if page:
            return topics[(page - 1) * config.paged: page * config.paged]
        else:
            return topics

    @staticmethod
    def get_node_choices():
        return select((n.name, n.name) for n in Node)

    def save(self, category='create', user=None):
        now = int(time.time())

        if category == 'create':
            self.created_at = now

        if not user:
            user = self.author

        if self.description:
            self.summary = strip_tags(self.description)

        self.updated_at = now
        self.active = now

        if user:
            user.active = now

        return super(Node, self).save()

    @staticmethod
    def get_nodes(page=1, category='all', limit=None):
        if category == 'all':
            nodes = select(rv for rv in Node).order_by(lambda rv:
                    desc(rv.created_at))
        elif category == 'hot':
            nodes = select(rv for rv in Node).order_by(lambda rv:
                    desc(rv.topic_count))
        elif category == 'new':
            nodes = select(rv for rv in Node).order_by(lambda rv:
                    desc(rv.created_at))
        if limit:
            return nodes[:limit]
        if page:
            return nodes[(page - 1) * config.node_paged: page * config.node_paged]
        else:
            return nodes

    def update(self, data):
        for k, v in data.iteritems():
            if not v and (k == 'description' or k == 'style'):
                v = ''
            if k == 'style' and v:
                v = strip_tags(v)
            setattr(self, k, v)
        self.summary = strip_tags(self.description)
        try:
            commit()
        except:
            pass
        return self
