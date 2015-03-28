# coding: utf-8

import time
from pony import orm
from ._base import db, BaseModel


class Bill(db.Entity, BaseModel):
    coin = orm.Required(int)
    balance = orm.Required(int)

    """ 账单类型
        'signup':           注册                收入
        'invite':           邀请他人注册        收入
        'invited-signup':   被邀请注册          收入
        'topic-create':     新建主题            支出
        'topic-edit':       编辑主题            支出
        'topic-hot':        主题变为热门        收入
        'topic-report':     主题变为举报        支出
        'reply-create':     新建评论            收入/支出
        'reply-edit':       编辑评论            收入/支出
        'reply-hot':        评论变为热门        收入
        'reply-report':     评论变为举报        支出
        'thank':            主题/评论被感谢     收入/支出
        'thank-remove':     主题/评论感谢撤销   收入/支出
        'collect':          主题/评论被收藏     收入/支出
        'active-gift':      活跃赠送            收入
    """
    role = orm.Required(unicode, default='signup')

    """ 支收类型
        1   收入
        0   支出
    """
    category = orm.Required(int, default=1)
    created_at = orm.Required(int, default=int(time.time()))

    user_id = orm.Optional(int)

    topic_id = orm.Optional(int)
    reply_id = orm.Optional(int)

    spender_id = orm.Optional(int)
    incomer_id = orm.Optional(int)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Bill: %s>' % self.id

    def save(self):
        now = int(time.time())
        self.created_at = now

        return super(Bill, self).save()
