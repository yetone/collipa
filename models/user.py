# coding: utf-8

import hashlib
from random import choice
import time
from pony.orm import *
from ._base import db, SessionMixin, ModelMixin
import config
import models as m
from helpers import format_date2, strip_tags
from extensions import mc, rd

config = config.rec()

class User(db.Entity, SessionMixin, ModelMixin):
    name = Required(unicode, 40, unique=True)
    email = Required(unicode, unique=True)
    password = Required(unicode, 100)

    urlname = Required(unicode, 80, unique=True)
    nickname = Required(unicode, 80)

    role = Required(unicode, 10, default='unverify')
    reputation = Required(int, default=0)
    active = Required(int, default=int(time.time()))
    edit_nickname_count = Required(int, default=config.user_edit_nickname_count)
    edit_urlname_count = Required(int, default=config.user_edit_urlname_count)

    topic_count = Required(int, default=0)
    reply_count = Required(int, default=0)

    """ 获得的 thank, up, down, report, collect 数目, 便于用户等级评估
    """
    thank_count = Required(int, default=0)
    up_count = Required(int, default=0)
    down_count = Required(int, default=0)
    report_count = Required(int, default=0)
    collect_count = Required(int, default=0)

    """ 自己的收藏数目, 与 collect_count 大大不同
    """
    collection_count = Required(int, default=0)

    """ following_count 正在关注的数目
        follower_count  关注者的数目
    """
    following_count = Required(int, default=0)
    follower_count = Required(int, default=0)

    balance = Required(int, default=config.user_init_coin)

    created_at = Required(int, default=int(time.time()))
    token = Required(unicode, 20)

    description = Optional(unicode, 400)
    address = Optional(unicode, 400)
    website = Optional(unicode, 400)
    style = Optional(unicode, 6000)

    avatar = Optional(unicode, 400)
    avatar_tmp = Optional(unicode, 400)
    head_img = Optional(unicode, 400)
    background_img = Optional(unicode, 400)

    @staticmethod
    @db_session
    def init(**kargs):
        token = User.create_token(16)
        kargs.update(dict(token=token))

        if 'name' in kargs:
            name = kargs.pop('name')
            kargs.update(dict(name=name.lower(),
                            urlname=name.lower(),
                            nickname=name))

        if 'email' in kargs:
            email = kargs.pop('email')
            kargs.update(dict(email=email.lower()))

        if 'password' in kargs:
            password = kargs.pop('password')
            kargs.update(dict(password=User.create_password(password)))

        return User(**kargs)

    def __str__(self):
        return self.nickname or self.name

    def __repr__(self):
        return '<User: %s>' % self.name

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
    def url(self):
        return '/' + self.urlname

    @property
    def created(self):
        return format_date2(self.created_at)

    @property
    def is_admin(self):
        return self.id == 1 or self.role == 'admin'

    def is_followed(self, user=None, topic=None, node=None):
        if user:
            if m.Follow.get(who_id=self.id, whom_id=user.id):
                return True
            else:
                return False
        if topic:
            if m.Follow.get(who_id=self.id, topic_id=topic.id):
                return True
            else:
                return False
        if node:
            if m.Follow.get(who_id=self.id, node_id=node.id):
                return True
            else:
                return False

    def income(self, coin, role="signup", topic_id=None, reply_id=None):
        self.balance += coin
        bill = m.Bill(user_id=self.id, coin=coin, balance=self.balance, role=role,
                category=1, topic_id=topic_id, reply_id=reply_id)
        if role in ["signup", "invite", "signup-invited", "active-gift"]:
            bank = m.Bank.get_one()
            bank.spend(coin=coin, role=role, incomer_id=self.id)
        bill.save()
        return

    def spend(self, coin, role="topic-create", topic_id=None, reply_id=None):
        self.balance -= coin
        bill = m.Bill(user_id=self.id, coin=coin, balance=self.balance, role=role,
                category=0, topic_id=topic_id, reply_id=reply_id)
        if role in ["topic-create", "reply-create", "topic-edit"]:
            bank = m.Bank.get_one()
            bank.income(coin=coin, role=role, topic_id=topic_id,
                    reply_id=reply_id, spender_id=self.id)
        bill.save()
        return

    def gravatar_url(self, size=48):
        return \
        'http://gravatar.com/avatar/%s?d=identicon&s=%d&d=%s%s' % \
                    (hashlib.md5(self.email.strip().lower().encode('utf-8')).hexdigest(),
                            size, config.site_url, config.user_avatar_url)

    def get_avatar(self, size=48):
        if self.avatar:
            avatar = self.avatar
        else:
            avatar = self.gravatar_url(size=size)
        ext = avatar.split('.').pop()
        length = len(ext) + 1
        avatar = avatar[:-length]
        return "%sx%s.%s" % (avatar, size, ext)

    @staticmethod
    def create_password(raw):
        salt = User.create_token(8)
        hsh = hashlib.sha1(salt + raw + config.password_secret).hexdigest()
        return "%s$%s" % (salt, hsh)

    @staticmethod
    def create_token(length=16):
        chars = ('0123456789'
                 'abcdefghijklmnopqrstuvwxyz'
                 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        salt = ''.join([choice(chars) for i in range(length)])
        return salt

    def check_password(self, raw):
        if '$' not in self.password:
            return False
        salt, hsh = self.password.split('$')
        verify = hashlib.sha1(salt + raw + config.password_secret).hexdigest()
        return verify == hsh

    def save(self, category='new'):
        now = int(time.time())
        self.created_at = now
        self.active = now

        if category == 'new':
            coin = config.user_init_coin
            role = 'signup'
        elif category == 'invited':
            coin = config.user_init_coin + config.invite_coin
            role = 'signup-invited'
        self.balance = coin
        m.Bill(user_id=self.id, coin=coin, balance=self.balance,
                role=role).save()
        bank = m.Bank.get_one()
        bank.spend(coin=coin, role=role, incomer_id=self.id)

        return super(User, self).save()

    def collect(self, collect_class_name=None, topic_id=None, reply_id=None):
        self.active = int(time.time())
        if collect_class_name:
            collect_class = m.CollectClass.get(name=collect_class_name, user_id=self.id)
            if not collect_class:
                collect_class = m.CollectClass(user_id=self.id,
                        name=collect_class_name)
                collect_class.save()
            collect_class_id = collect_class.id
        else:
            collect_class_id = None
        collect = m.Collect.get(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
        if not collect:
            collect = m.Collect(user_id=self.id, topic_id=topic_id,
                    reply_id=reply_id, collect_class_id=collect_class_id)
            collect.save()
            return {'status': 'success', 'message': '收藏成功', 'type': 1}
        else:
            collect.remove()
            return {'status': 'success', 'message': '取消收藏成功', 'type': 0}

    def follow(self, follow_class_name=None, whom_id=None, topic_id=None,
            node_id=None):
        self.active = int(time.time())
        if follow_class_name:
            follow_class = m.FollowClass.get(name=follow_class_name, user_id=self.id)
            if not follow_class:
                follow_class = m.FollowClass(user_id=self.id,
                        name=follow_class_name)
                follow_class.save()
            follow_class_id = follow_class.id
        else:
            follow_class_id = None
        follow = m.Follow.get(who_id=self.id, whom_id=whom_id,
                topic_id=topic_id, node_id=node_id)
        if not follow:
            follow = m.Follow(who_id=self.id, whom_id=whom_id,
                    topic_id=topic_id, node_id=node_id, follow_class_id=follow_class_id)
            follow.save()
            return {'status': 'success', 'message': '关注成功', 'type': 1}
        else:
            follow.remove()
            return {'status': 'success', 'message': '取消关注成功', 'type': 0}

    def thank(self, topic_id=None, reply_id=None):
        now = int(time.time())
        self.active = now
        thank = m.Thank.get(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
        if not thank:
            thank = m.Thank(user_id=self.id, topic_id=topic_id,
                    reply_id=reply_id)
            notification = m.Notification.get(topic_id=topic_id,
                    reply_id=reply_id, role='thank')
            if notification:
                if notification.switch == 1:
                    notification.status = 0
                    notification.updated_at = now
            else:
                notification = m.Notification(topic_id=topic_id,
                        reply_id=reply_id, role='thank').save()
            result = thank.save()
            if result:
                return {'status': 'success', 'message': '感谢成功', 'type': 1}
            else:
                return {'status': 'error', 'message': '感谢失败', 'type': -1}
        else:
            delta = int(time.time()) - thank.created_at
            if delta < config.thank_delta_time:
                thank.remove()
                return {'status': 'success', 'message': '取消感谢成功', 'type': 0}
            return {'status': 'info', 'message': '已超过取消感谢时间', 'type':
                    -1}

    def up(self, topic_id=None, reply_id=None):
        now = int(time.time())
        self.active = now
        up = m.Up.get(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
        if not up:
            down = m.Down.get(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
            if down:
                down.remove()
            up = m.Up(user_id=self.id, topic_id=topic_id,
                    reply_id=reply_id)
            notification = m.Notification.get(topic_id=topic_id,
                    reply_id=reply_id, role='up')
            if notification:
                if notification.switch == 1:
                    notification.status = 0
                    notification.updated_at = now
            else:
                notification = m.Notification(topic_id=topic_id,
                        reply_id=reply_id, role='up').save()
            result = up.save()
            if result:
                return {'status': 'success', 'message': '赞同成功', 'type': 1,
                        'category': 'up'}
            else:
                return {'status': 'error', 'message': '赞同失败', 'type': -1}
        else:
            up.remove()
            return {'status': 'success', 'message': '取消赞同成功', 'type': 0,
                    'category': 'up'}

    def down(self, topic_id=None, reply_id=None):
        self.active = int(time.time())
        down = m.Down.get(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
        if not down:
            up = m.Up.get(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
            if up:
                up.remove()
            down = m.Down(user_id=self.id, topic_id=topic_id,
                    reply_id=reply_id)
            result = down.save()
            if result:
                return {'status': 'success', 'message': '反对成功', 'type': 1,
                        'category': 'down'}
            else:
                return {'status': 'error', 'message': '反对失败', 'type': -1}
        else:
            down.remove()
            return {'status': 'success', 'message': '取消反对成功', 'type': 0,
                    'category': 'down'}

    def report(self, topic_id=None, reply_id=None):
        self.active = int(time.time())
        report = m.Report.get(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
        if not report:
            report = m.Report(user_id=self.id, topic_id=topic_id,
                    reply_id=reply_id)
            report.save()
            return {'status': 'success', 'message': '举报成功', 'type': 1}
        else:
            report.remove()
            return {'status': 'success', 'message': '取消举报成功', 'type': 0}

    def get_topics(self, page=1, category='all', order_by='created_at', limit=None):
        if limit:
            topics = select(rv for rv in m.Topic if rv.user_id == self.id).order_by(lambda rv: desc((rv.collect_count +
                rv.thank_count) * 10 +
                (rv.up_count - rv.down_count) * 5))
            return topics[:limit]

        if category == 'all':
            topics = select(rv for rv in m.Topic if rv.user_id == self.id)
        else:
            topics = select(rv for rv in m.Topic if rv.user_id == self.id and
                    rv.role == category)

        if order_by == 'created_at':
            topics = topics.order_by(lambda rv: desc(rv.created_at))
        elif order_by == 'up_count':
            topics = topics.order_by(lambda rv: desc(rv.up_count))
        elif order_by == 'thank_count':
            topics = topics.order_by(lambda rv: desc(rv.thank_count))
        elif order_by == 'smart':
            topics = topics.order_by(lambda rv: desc((rv.collect_count +
                rv.thank_count) * 10 +
                (rv.up_count - rv.down_count) * 5))

        if page:
            return topics[(page - 1) * config.paged: page * config.paged]
        else:
            return topics

    def get_replies(self, page=1, category='all', order_by='created_at', limit=None):
        if limit:
            replies = select(rv for rv in m.Reply if rv.user_id == self.id).order_by(lambda rv: desc((rv.collect_count +
                rv.thank_count) * 10 +
                (rv.up_count - rv.down_count) * 5))
            return replies[:limit]

        if category == 'all':
            replies = select(rv for rv in m.Reply if rv.user_id == self.id)
        else:
            replies = select(rv for rv in m.Reply if rv.user_id == self.id and
                    rv.role == category)

        if order_by == 'created_at':
            replies = replies.order_by(lambda rv: desc(rv.created_at))
        elif order_by == 'up_count':
            replies = replies.order_by(lambda rv: desc(rv.up_count))
        elif order_by == 'thank_count':
            replies = replies.order_by(lambda rv: desc(rv.thank_count))
        elif order_by == 'smart':
            replies = replies.order_by(lambda rv: desc((rv.collect_count +
                rv.thank_count) * 10 +
                (rv.up_count - rv.down_count) * 5 + rv.created_at / 4))

        if page:
            return replies[(page - 1) * config.paged: page * config.paged]
        else:
            return replies

    @property
    def followed_node_ids(self):
        return select(rv.node_id for rv in m.Follow if rv.who_id ==
                self.id and rv.node_id is not None)

    @property
    def followed_user_ids(self):
        return select(rv.whom_id for rv in m.Follow if rv.who_id ==
                self.id and rv.whom_id is not None)

    def get_timeline(self, role=None, category='all', order_by='created_at', page=1):
        node_ids = self.followed_node_ids
        user_ids = self.followed_user_ids
        if not node_ids:
            node_ids = [0]
        if not user_ids:
            user_ids = [0]
        if category == 'hot':
            now = int(time.time())
            ago = now - 60 * 60 * 24
            try:
                return select(rv for rv in m.Topic if (rv.node_id in node_ids or
                        rv.user_id in user_ids) and
                        rv.created_at > ago).order_by(lambda rv: desc((rv.collect_count +
                    rv.thank_count) * 10 +
                    (rv.up_count - rv.down_count) * 5))
            except:
                return None
        if category == 'all':
            topics = select(rv for rv in m.Topic if rv.node_id in
                    node_ids or rv.user_id in user_ids)
        if category == 'user':
            topics = select(rv for rv in m.Topic if rv.user_id in
                    user_ids)
        if category == 'node':
            topics = select(rv for rv in m.Topic if rv.node_id in
                    node_ids)

        if order_by == 'smart':
            topics = topics.order_by(lambda rv: desc((rv.collect_count +
                        rv.thank_count) * 10 + (rv.up_count -
                            rv.down_count) * 5 + rv.active / 4))
        else:
            topics = topics.order_by(lambda rv: desc(rv.last_reply_date))
        if page:
            return topics[(page - 1) * config.paged: page * config.paged]
        else:
            return topics

    def is_uped(self, topic=None, reply=None):
        if topic:
            if m.Up.get(user_id=self.id, topic_id=topic.id):
                return True
            return False
        if reply:
            if m.Up.get(user_id=self.id, reply_id=reply.id):
                return True
            return False

    def is_downed(self, topic=None, reply=None):
        if topic:
            if m.Down.get(user_id=self.id, topic_id=topic.id):
                return True
            return False
        if reply:
            if m.Down.get(user_id=self.id, reply_id=reply.id):
                return True
            return False

    def is_collected(self, topic=None, reply=None):
        if topic:
            if m.Collect.get(user_id=self.id, topic_id=topic.id):
                return True
            return False
        if reply:
            if m.Collect.get(user_id=self.id, reply_id=reply.id):
                return True
            return False

    def is_thanked(self, topic=None, reply=None):
        if topic:
            if m.Thank.get(user_id=self.id, topic_id=topic.id):
                return True
            return False
        if reply:
            if m.Thank.get(user_id=self.id, reply_id=reply.id):
                return True
            return False

    def is_reported(self, topic=None, reply=None):
        if topic:
            if m.Report.get(user_id=self.id, topic_id=topic.id):
                return True
            return False
        if reply:
            if m.Report.get(user_id=self.id, reply_id=reply.id):
                return True
            return False

    @property
    def unread_notification_count(self):
        return m.Notification.select(lambda rv: rv.receiver_id ==
                self.id and rv.status == 0 and rv.switch == 1).count()

    @property
    def notification_count(self):
        return m.Notification.select(lambda rv: rv.receiver_id ==
                self.id and rv.status == 0 and rv.switch == 1).count()

    def get_notifications(self, page=1, category='all'):
        if category == 'all':
            notifications = m.Notification.select(lambda rv: rv.receiver_id == self.id)
        elif category == 'unread':
            notifications = m.Notification.select(lambda rv: rv.receiver_id ==
                    self.id and rv.status == 0)
        notifications = notifications.order_by(lambda rv: desc(rv.updated_at))
        return notifications[(page - 1) * config.paged: page * config.paged]

    @property
    def notifications(self):
        notifications = m.Notification.select(lambda rv: rv.receiver_id == self.id)
        return notifications

    @property
    def unread_notifications(self):
        notifications = m.Notification.select(lambda rv: rv.receiver_id ==
                self.id and rv.status == 0)
        return notifications

    def read_notifications(self):
        notifications = self.unread_notifications
        for n in notifications:
            n.status = 1
        try:
            commit()
        except Exception, e:
            print type(e).__name__
            print e
            raise

    @property
    def unread_message_box_count(self):
        return m.MessageBox.select(lambda rv: rv.sender_id ==
                self.id and rv.status == 0).count()

    def get_message_boxes(self, page=1, category='all'):
        if category == 'all':
            message_boxes = m.MessageBox.select(lambda rv: rv.sender_id == self.id).order_by(lambda rv:
                            desc(rv.updated_at))
        elif category == 'unread':
            message_boxes = m.MessageBox.select(lambda rv: rv.sender_id == self.id
                     and rv.status == 0).order_by(lambda rv:
                            desc(rv.updated_at))
        return message_boxes[(page - 1) * config.paged: page *
                config.paged]

    def get_message_box(self, user=None):
        message_boxes = m.MessageBox.select(lambda rv: rv.sender_id == self.id and
            rv.receiver_id == user.id)
        if message_boxes:
            message_box = message_boxes[:][0]
        else:
            message_box = None
        return message_box

    def update(self, data):
        if data.get('nickname') != self.nickname:
            self.edit_nickname_count -= 1
        if data.get('urlname') != self.urlname:
            self.edit_urlname_count -= 1
        for k, v in data.iteritems():
            if not v and (k == 'address' or k == 'website' or k ==
                    'description' or k == 'style'):
                v = ''
            if k == 'style' and v:
                v = strip_tags(v)
            setattr(self, k, v)
        try:
            commit()
        except:
            pass
        return self

    @staticmethod
    def get_users(page=1, category='all', limit=None):
        if category == 'all':
            users = select(rv for rv in User).order_by(lambda rv:
                    desc(rv.created_at))
        if category == 'hot':
            users = mc.get('hot_users')
            if not users:
                if not limit:
                    limit = 8
                users = select(rv for rv in User).order_by(lambda rv:
                        desc(rv.thank_count * 4 + rv.up_count * 3 + rv.topic_count
                            * 2 + rv.reply_count))[:limit]
                mc.set('hot_users', list(users), 60 * 60 * 12)
        if category == 'new':
            users = select(rv for rv in User).order_by(lambda rv:
                    desc(rv.created_at))
        if limit:
            return users[:limit]
        if page:
            return users[(page - 1) * config.user_paged: page *
                    config.user_paged]
        else:
            return users

    def get_followers(self, page=1):
        follower_ids = select(rv.who_id for rv in m.Follow if rv.whom_id ==
                self.id).order_by(lambda rv: desc(rv)) or [0]
        followers = select(rv for rv in User if rv.id in follower_ids)
        if page:
            return followers[(page - 1) * config.user_paged: page *
                    config.user_paged]
        else:
            return followers

    def get_followings(self, page=1):
        following_ids = select(rv.whom_id for rv in m.Follow if rv.who_id ==
                self.id and rv.whom_id).order_by(lambda rv: desc(rv)) or [0]
        followings = select(rv for rv in User if rv.id in following_ids)
        if page:
            return followings[(page - 1) * config.user_paged: page *
                    config.user_paged]
        else:
            return followings

    @property
    def is_online(self):
        online = rd.smembers("online") or [0]
        online = [int(i) for i in online]
        return self.id in online
