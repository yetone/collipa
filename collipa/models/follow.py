# coding: utf-8

import time
from pony import orm
from ._base import db, BaseModel
import collipa.models
from collipa.helpers import cached_property


class Follow(db.Entity, BaseModel):
    who_id = orm.Required(int)
    whom_id = orm.Optional(int)
    topic_id = orm.Optional(int)
    node_id = orm.Optional(int)

    created_at = orm.Required(int, default=int(time.time()))

    follow_class_id = orm.Optional(int)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Follow: %s>' % self.id

    @cached_property
    def who(self):
        return collipa.models.User.get(id=self.who_id)

    @cached_property
    def whom(self):
        return collipa.models.User.get(id=self.whom_id)

    @cached_property
    def follow_class(self):
        if self.follow_class_id:
            return collipa.models.FollowClass.get(self.follow_class_id)
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

    def delete(self):
        if self.whom_id:
            self.who.following_count -= 1
            self.whom.follower_count -= 1
            if self.follow_class:
                self.follow_class.follow_count -= 1
        if self.topic_id:
            self.topic.follow_count -= 1
        if self.node_id:
            self.node.follow_count -= 1

        super(Follow, self).delete()
