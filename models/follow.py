# coding: utf-8

import time
from pony.orm import *
from ._base import db, SessionMixin, ModelMixin
import models as m
import config
from helpers import cached_property

config = config.rec()

class Follow(db.Entity, SessionMixin, ModelMixin):
    who_id = Required(int)
    whom_id = Optional(int)
    topic_id = Optional(int)
    node_id = Optional(int)

    created_at = Required(int, default=int(time.time()))

    follow_class_id = Optional(int)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Follow: %s>' % self.id

    @cached_property
    def who(self):
        return m.User.get(id=self.who_id)

    @cached_property
    def whom(self):
        return m.User.get(id=self.whom_id)

    @cached_property
    def follow_class(self):
        if self.follow_class_id:
            return m.FollowClass.get(self.follow_class_id)
        return None

    def save(self):
        now = int(time.time())
        self.created_at = now

        if self.whom_id:
            self.who.following_count += 1
            self.whom.follower_count += 1
            if self.follow_class:
                self.follow_class.follow_count += 1
        if self.topic_id:
            self.topic.follow_count += 1
        if self.node_id:
            self.node.follow_count += 1

        return super(Follow, self).save()

    def remove(self):
        if self.whom_id:
            self.who.following_count -= 1
            self.whom.follower_count -= 1
            if self.follow_class:
                self.follow_class.follow_count -= 1
        if self.topic_id:
            self.topic.follow_count -= 1
        if self.node_id:
            self.node.follow_count -= 1

        super(Follow, self).remove()
