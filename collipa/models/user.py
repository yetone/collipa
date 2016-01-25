# coding: utf-8

import hashlib
from random import choice
import time
from pony import orm

from ._base import db, BaseModel
from collipa import config
import collipa.models
from collipa.helpers import format_date2, strip_tags, remove_file, get_asset_path, collect_items_from_query
from collipa.extensions import mc, rd, memcached
from collipa.supports import Struct


class User(db.Entity, BaseModel):
    name = orm.Required(unicode, 40, unique=True)
    email = orm.Required(unicode, unique=True)
    password = orm.Required(unicode, 100)

    urlname = orm.Required(unicode, 80, unique=True)
    nickname = orm.Required(unicode, 80)

    role = orm.Required(unicode, 10, default='unverify')
    reputation = orm.Required(int, default=0)
    active = orm.Required(int, default=int(time.time()))
    edit_nickname_count = orm.Required(int, default=config.user_edit_nickname_count)
    edit_urlname_count = orm.Required(int, default=config.user_edit_urlname_count)

    topic_count = orm.Required(int, default=0)
    reply_count = orm.Required(int, default=0)
    tweet_count = orm.Required(int, default=0)
    album_count = orm.Required(int, default=0)
    image_count = orm.Required(int, default=0)

    """ 获得的 thank, up, down, report, collect 数目, 便于用户等级评估
    """
    thank_count = orm.Required(int, default=0)
    up_count = orm.Required(int, default=0)
    down_count = orm.Required(int, default=0)
    report_count = orm.Required(int, default=0)
    collect_count = orm.Required(int, default=0)

    """ 自己的收藏数目, 与 collect_count 大大不同
    """
    collection_count = orm.Required(int, default=0)

    """ following_count 正在关注的数目
        follower_count  关注者的数目
    """
    following_count = orm.Required(int, default=0)
    follower_count = orm.Required(int, default=0)

    balance = orm.Required(int, default=config.user_init_coin)

    created_at = orm.Required(int, default=int(time.time()))
    token = orm.Required(unicode, 20)

    description = orm.Optional(unicode, 400)
    address = orm.Optional(unicode, 400)
    website = orm.Optional(unicode, 400)
    style = orm.Optional(unicode, 6000)
    site_style = orm.Optional(unicode, 6000)

    avatar = orm.Optional(unicode, 400)
    avatar_tmp = orm.Optional(unicode, 400)
    head_img = orm.Optional(unicode, 400)
    background_img = orm.Optional(unicode, 400)

    KEY_ONLINE = 'online:{.id}'
    KEY_G_ONLINE = 'online'

    # roles
    UNVERIFY = 'unverify'
    FORBIDDEN = 'forbidden'
    ADMIN = 'admin'

    @classmethod
    def init(cls, **kwargs):
        token = cls.create_token(16)
        kwargs.update(dict(token=token))

        if 'name' in kwargs:
            name = kwargs.pop('name')
            kwargs.update(dict(name=name.lower(),
                               urlname=name.lower(),
                               nickname=name))

        if 'email' in kwargs:
            email = kwargs.pop('email')
            kwargs.update(dict(email=email.lower()))

        if 'password' in kwargs:
            password = kwargs.pop('password')
            kwargs.update(dict(password=User.create_password(password)))

        return cls(**kwargs)

    def to_simple_dict(self):
        data = {
            'id': self.id,
            'url': self.url,
            'name': self.nickname,
            'avatar': self.get_avatar(),
            }

        return data

    def to_dict(self):
        data = {
            'created': self.created,
            'topic_count': self.topic_count,
            'reply_count': self.reply_count,
            'tweet_count': self.tweet_count,
            'album_count': self.album_count,
            'image_count': self.image_count,
        }
        data.update(self.to_simple_dict())
        return data

    def __str__(self):
        return self.nickname or self.name

    def __repr__(self):
        return '<User: %s>' % self.name

    @property
    def head(self):
        if self.head_img:
            return self.head_img
        return config.node_head_url

    @property
    def background(self):
        if self.background_img:
            return self.background_img
        return config.node_background_url

    def reset_img(self, category):
        if category == 'background':
            path = self.background_img
            self.background_img = ''
        elif category == 'head':
            path = self.head_img
            self.head_img = ''
        else:
            return False
        try:
            remove_file(get_asset_path(path))
            return True
        except:
            return False

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
            if collipa.models.Follow.get(who_id=self.id, whom_id=user.id):
                return True
        if topic:
            if collipa.models.Follow.get(who_id=self.id, topic_id=topic.id):
                return True
        if node:
            if collipa.models.Follow.get(who_id=self.id, node_id=node.id):
                return True
        return False

    def income(self, coin, role="signup", topic_id=None, reply_id=None):
        self.balance += coin
        bill = collipa.models.Bill(user_id=self.id, coin=coin, balance=self.balance,
                                   role=role, category=1, topic_id=topic_id,
                                   reply_id=reply_id)
        if role in ["signup", "invite", "signup-invited", "active-gift"]:
            bank = collipa.models.Bank.get_one()
            bank.spend(coin=coin, role=role, incomer_id=self.id)
        bill.save()
        return

    def spend(self, coin, role="topic-create", topic_id=None, reply_id=None):
        self.balance -= coin
        bill = collipa.models.Bill(user_id=self.id, coin=coin, balance=self.balance,
                                   role=role, category=0, topic_id=topic_id,
                                   reply_id=reply_id)
        if role in ["topic-create", "reply-create", "topic-edit"]:
            bank = collipa.models.Bank.get_one()
            bank.income(coin=coin, role=role, topic_id=topic_id,
                        reply_id=reply_id, spender_id=self.id)
        bill.save()
        return

    def gravatar_url(self, size=48):
        return 'http://gravatar.com/avatar/%s?d=identicon&s=%d&d=%s%s' % (hashlib.md5(self.email.strip().lower().encode('utf-8')).hexdigest(),
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
        if not self.password or '$' not in self.password:
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
        else:
            return
        self.balance = coin
        collipa.models.Bill(user_id=self.id, coin=coin, balance=self.balance, role=role).save()
        bank = collipa.models.Bank.get_one()
        bank.spend(coin=coin, role=role, incomer_id=self.id)

        return super(User, self).save()

    def collect(self, collect_class_name=None, topic_id=None, reply_id=None):
        self.active = int(time.time())
        if collect_class_name:
            collect_class = collipa.models.CollectClass.get(name=collect_class_name,
                                                            user_id=self.id)
            if not collect_class:
                collect_class = collipa.models.CollectClass(user_id=self.id,
                                                            name=collect_class_name)
                collect_class.save()
            collect_class_id = collect_class.id
        else:
            collect_class_id = None
        collect = collipa.models.Collect.get(user_id=self.id, topic_id=topic_id,
                                             reply_id=reply_id)
        if not collect:
            collect = collipa.models.Collect(user_id=self.id,
                                             topic_id=topic_id,
                                             reply_id=reply_id,
                                             collect_class_id=collect_class_id)
            collect.save()
            return {'status': 'success', 'message': '收藏成功', 'type': 1}
        else:
            collect.delete()
            return {'status': 'success', 'message': '取消收藏成功', 'type': 0}

    def follow(self, follow_class_name=None, whom_id=None, topic_id=None,
               node_id=None):
        self.active = int(time.time())
        if follow_class_name:
            follow_class = collipa.models.FollowClass.get(name=follow_class_name,
                                                          user_id=self.id)
            if not follow_class:
                follow_class = collipa.models.FollowClass(user_id=self.id,
                                                          name=follow_class_name)
                follow_class.save()
            follow_class_id = follow_class.id
        else:
            follow_class_id = None
        follow = collipa.models.Follow.get(who_id=self.id, whom_id=whom_id,
                                           topic_id=topic_id, node_id=node_id)
        if not follow:
            follow = collipa.models.Follow(who_id=self.id, whom_id=whom_id,
                                           topic_id=topic_id, node_id=node_id,
                                           follow_class_id=follow_class_id)
            follow.save()
            return {'status': 'success', 'message': '关注成功', 'type': 1}
        else:
            follow.delete()
            return {'status': 'success', 'message': '取消关注成功', 'type': 0}

    def thank(self, topic_id=None, reply_id=None):
        now = int(time.time())
        self.active = now
        thank = collipa.models.Thank.get(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
        if not thank:
            thank = collipa.models.Thank(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
            notification = collipa.models.Notification.get(topic_id=topic_id, reply_id=reply_id, role='thank')
            if notification:
                if notification.switch == 1:
                    notification.status = 0
                    notification.updated_at = now
            else:
                collipa.models.Notification(topic_id=topic_id, reply_id=reply_id, role='thank').save()
            result = thank.save()
            if result:
                return {'status': 'success', 'message': '感谢成功', 'type': 1}
            else:
                return {'status': 'error', 'message': '感谢失败', 'type': -1}
        delta = int(time.time()) - thank.created_at
        if delta < config.thank_delta_time:
            thank.delete()
            return {'status': 'success', 'message': '取消感谢成功', 'type': 0}
        return {'status': 'info', 'message': '已超过取消感谢时间', 'type': -1}

    def up(self, topic_id=None, reply_id=None):
        now = int(time.time())
        self.active = now
        up = collipa.models.Up.get(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
        if not up:
            down = collipa.models.Down.get(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
            if down:
                down.delete()
            up = collipa.models.Up(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
            notification = collipa.models.Notification.get(topic_id=topic_id, reply_id=reply_id, role='up')
            if notification:
                if notification.switch == 1:
                    notification.status = 0
                    notification.updated_at = now
            else:
                collipa.models.Notification(topic_id=topic_id, reply_id=reply_id, role='up').save()
            result = up.save()
            if result:
                return {'status': 'success', 'message': '赞同成功', 'type': 1,
                        'category': 'up'}
            else:
                return {'status': 'error', 'message': '赞同失败', 'type': -1}
        up.delete()
        return {'status': 'success', 'message': '取消赞同成功', 'type': 0,
                'category': 'up'}

    def down(self, topic_id=None, reply_id=None):
        self.active = int(time.time())
        down = collipa.models.Down.get(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
        if not down:
            up = collipa.models.Up.get(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
            if up:
                up.delete()
            down = collipa.models.Down(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
            result = down.save()
            if result:
                return {'status': 'success', 'message': '反对成功', 'type': 1,
                        'category': 'down'}
            else:
                return {'status': 'error', 'message': '反对失败', 'type': -1}
        down.delete()
        return {'status': 'success', 'message': '取消反对成功', 'type': 0,
                'category': 'down'}

    def report(self, topic_id=None, reply_id=None):
        self.active = int(time.time())
        report = collipa.models.Report.get(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
        if not report:
            report = collipa.models.Report(user_id=self.id, topic_id=topic_id, reply_id=reply_id)
            report.save()
            return {'status': 'success', 'message': '举报成功', 'type': 1}
        report.delete()
        return {'status': 'success', 'message': '取消举报成功', 'type': 0}

    def get_topics(self, page=1, category='all', order_by='created_at',
                   limit=None):
        if limit:
            topics = orm.select(rv for rv in collipa.models.Topic if
                                rv.user_id == self.id).order_by(lambda:
                                                                orm.desc((rv.collect_count +
                                                                          rv.thank_count) * 10 +
                                                                         (rv.up_count -
                                                                          rv.down_count) * 5))
            return topics[:limit]

        if category == 'all':
            topics = orm.select(rv for rv in collipa.models.Topic if rv.user_id == self.id)
        else:
            topics = orm.select(rv for rv in collipa.models.Topic if rv.user_id == self.id and rv.role == category)

        if order_by == 'created_at':
            topics = topics.order_by(lambda: orm.desc(rv.created_at))
        elif order_by == 'up_count':
            topics = topics.order_by(lambda: orm.desc(rv.up_count))
        elif order_by == 'thank_count':
            topics = topics.order_by(lambda: orm.desc(rv.thank_count))
        elif order_by == 'smart':
            topics = topics.order_by(lambda:
                                     orm.desc((rv.collect_count +
                                               rv.thank_count) * 10 +
                                              (rv.up_count - rv.down_count) * 5))

        if page:
            return topics[(page - 1) * config.paged: page * config.paged]
        else:
            return topics

    def get_replies(self, page=1, category='all', order_by='created_at',
                    limit=None):
        if limit:
            replies = orm.select(rv for rv in collipa.models.Reply if
                                 rv.user_id == self.id).order_by(lambda:
                                                                 orm.desc((rv.collect_count +
                                                                           rv.thank_count) * 10 +
                                                                          (rv.up_count -
                                                                           rv.down_count) * 5))
            return replies[:limit]

        if category == 'all':
            replies = orm.select(rv for rv in collipa.models.Reply if rv.user_id == self.id)
        else:
            replies = orm.select(rv for rv in collipa.models.Reply if rv.user_id == self.id and rv.role == category)

        if order_by == 'created_at':
            replies = replies.order_by(lambda: orm.desc(rv.created_at))
        elif order_by == 'up_count':
            replies = replies.order_by(lambda: orm.desc(rv.up_count))
        elif order_by == 'thank_count':
            replies = replies.order_by(lambda: orm.desc(rv.thank_count))
        elif order_by == 'smart':
            replies = replies.order_by(lambda:
                                       orm.desc((rv.collect_count +
                                                 rv.thank_count) * 10 +
                                                (rv.up_count - rv.down_count) * 5 +
                                                rv.created_at / 4))

        if page:
            return replies[(page - 1) * config.paged: page * config.paged]
        else:
            return replies

    def get_tweets(self, page=1, category='all', order_by='created_at',
                   limit=None):
        if limit:
            tweets = orm.select(rv for rv in collipa.models.Tweet if
                                rv.user_id == self.id).order_by(lambda:
                                                                orm.desc((rv.collect_count +
                                                                          rv.thank_count) * 10 +
                                                                         (rv.up_count -
                                                                          rv.down_count) * 5))
            return tweets[:limit]

        if category == 'all':
            tweets = orm.select(rv for rv in collipa.models.Tweet if rv.user_id == self.id)
        else:
            tweets = orm.select(rv for rv in collipa.models.Tweet if rv.user_id == self.id and rv.role == category)

        if order_by == 'created_at':
            tweets = tweets.order_by(lambda: orm.desc(rv.created_at))
        elif order_by == 'up_count':
            tweets = tweets.order_by(lambda: orm.desc(rv.up_count))
        elif order_by == 'thank_count':
            tweets = tweets.order_by(lambda: orm.desc(rv.thank_count))
        elif order_by == 'smart':
            tweets = tweets.order_by(lambda:
                                     orm.desc((rv.collect_count +
                                               rv.thank_count) * 10 +
                                              (rv.up_count - rv.down_count) * 5 +
                                              rv.created_at / 4))

        if page:
            return tweets[(page - 1) * config.paged: page * config.paged]
        else:
            return tweets

    def get_albums(self, page=1, category='all', order_by='created_at', limit=None):
        if limit:
            albums = orm.select(rv for rv in collipa.models.Album if
                                rv.user_id == self.id).order_by(lambda:
                                                                orm.desc((rv.collect_count +
                                                                          rv.thank_count) * 10 +
                                                                         (rv.up_count -
                                                                          rv.down_count) * 5))
            return albums[:limit]

        if category == 'all':
            albums = orm.select(rv for rv in collipa.models.Album if rv.user_id == self.id)
        else:
            albums = orm.select(rv for rv in collipa.models.Album if rv.user_id == self.id and rv.role == category)

        if order_by == 'created_at':
            albums = albums.order_by(lambda: orm.desc(rv.created_at))
        elif order_by == 'up_count':
            albums = albums.order_by(lambda: orm.desc(rv.up_count))
        elif order_by == 'thank_count':
            albums = albums.order_by(lambda: orm.desc(rv.thank_count))
        elif order_by == 'smart':
            albums = albums.order_by(lambda:
                                     orm.desc((rv.collect_count +
                                               rv.thank_count) * 10 +
                                              (rv.up_count - rv.down_count) * 5))

        if page:
            return albums[(page - 1) * config.paged: page * config.paged]
        else:
            return albums

    def get_images(self, page=1, category='all', order_by='created_at', limit=None):
        if limit:
            images = orm.select(rv for rv in collipa.models.Image if
                                rv.user_id == self.id).order_by(lambda:
                                                                orm.desc((rv.collect_count +
                                                                          rv.thank_count) * 10 +
                                                                         (rv.up_count -
                                                                          rv.down_count) * 5))
            return images[:limit]

        if category == 'all':
            images = orm.select(rv for rv in collipa.models.Image if rv.user_id == self.id)
        else:
            images = orm.select(rv for rv in collipa.models.Image if rv.user_id == self.id and rv.role == category)

        if order_by == 'created_at':
            images = images.order_by(lambda: orm.desc(rv.created_at))
        elif order_by == 'up_count':
            images = images.order_by(lambda: orm.desc(rv.up_count))
        elif order_by == 'thank_count':
            images = images.order_by(lambda: orm.desc(rv.thank_count))
        elif order_by == 'smart':
            images = images.order_by(lambda:
                                     orm.desc((rv.collect_count +
                                               rv.thank_count) * 10 +
                                              (rv.up_count - rv.down_count) * 5 +
                                              rv.created_at / 4))

        if page:
            return images[(page - 1) * config.paged: page * config.paged]
        else:
            return images

    @property
    def default_album(self):
        album = collipa.models.Album.select(lambda rv: rv.user_id == self.id and rv.role == 'default').first()
        if not album:
            album = collipa.models.Album(user_id=self.id,
                                         name=u'默认专辑',
                                         role='default').save()
        return album

    @property
    def followed_node_ids(self):
        return orm.select(rv.node_id for rv in collipa.models.Follow if rv.who_id == self.id and rv.node_id is not None)

    @property
    def followed_user_ids(self):
        return orm.select(rv.whom_id for rv in collipa.models.Follow if rv.who_id == self.id and rv.whom_id is not None)

    def get_timeline(self, page=1, from_id=None, count=config.paged):
        user_ids = self.followed_user_ids[:] or [0]
        user_ids.append(self.id)
        if not from_id:
            tweets = (orm.select(rv for rv in collipa.models.Tweet if rv.user_id in user_ids)
                      .order_by(lambda: orm.desc(rv.created_at))
                      [(page - 1) * config.paged: page * config.paged])
            return tweets
        all_ids_q = orm.select(rv.id for rv in collipa.models.Tweet if
                               rv.user_id in user_ids).order_by(lambda: orm.desc(rv.created_at))

        tweet_ids = collect_items_from_query(all_ids_q, from_id, count)

        return orm.select(rv for rv in collipa.models.Tweet if rv.id in tweet_ids)[:][::-1]

    def get_followed_topics(self, role=None, category='all', order_by='created_at', page=1):
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
                return orm.select(rv for rv in collipa.models.Topic if
                                  (rv.node_id in node_ids or rv.user_id in user_ids) and
                                  rv.created_at > ago).order_by(lambda:
                                                                orm.desc((rv.collect_count +
                                                                          rv.thank_count) * 10 +
                                                                         (rv.up_count -
                                                                          rv.down_count) * 5))
            except:
                return None
        elif category == 'all':
            topics = orm.select(rv for rv in collipa.models.Topic if rv.node_id in node_ids or rv.user_id in user_ids)
        elif category == 'user':
            topics = orm.select(rv for rv in collipa.models.Topic if rv.user_id in user_ids)
        elif category == 'node':
            topics = orm.select(rv for rv in collipa.models.Topic if rv.node_id in node_ids)
        else:
            return []

        if order_by == 'smart':
            topics = topics.order_by(lambda:
                                     orm.desc((rv.collect_count +
                                               rv.thank_count) * 10 +
                                              (rv.up_count -
                                               rv.down_count) * 5 +
                                              rv.active / 4))
        else:
            topics = topics.order_by(lambda: orm.desc(rv.last_reply_date))

        if page:
            return topics[(page - 1) * config.paged: page * config.paged]
        else:
            return topics

    def is_upped(self, topic=None, reply=None, tweet=None):
        if topic and collipa.models.Up.get(user_id=self.id, topic_id=topic.id):
            return True
        if reply and collipa.models.Up.get(user_id=self.id, reply_id=reply.id):
            return True
        if tweet and collipa.models.Up.get(user_id=self.id, tweet_id=tweet.id):
            return True
        return False

    def is_downed(self, topic=None, reply=None, tweet=None):
        if topic and collipa.models.Down.get(user_id=self.id, topic_id=topic.id):
            return True
        if reply and collipa.models.Down.get(user_id=self.id, reply_id=reply.id):
            return True
        if tweet and collipa.models.Down.get(user_id=self.id, tweet_id=tweet.id):
            return True
        return False

    def is_collected(self, topic=None, reply=None, tweet=None):
        if topic and collipa.models.Collect.get(user_id=self.id, topic_id=topic.id):
            return True
        if reply and collipa.models.Collect.get(user_id=self.id, reply_id=reply.id):
            return True
        if tweet and collipa.models.Collect.get(user_id=self.id, tweet_id=tweet.id):
            return True
        return False

    def is_thanked(self, topic=None, reply=None, tweet=None):
        if topic and collipa.models.Thank.get(user_id=self.id, topic_id=topic.id):
            return True
        if reply and collipa.models.Thank.get(user_id=self.id, reply_id=reply.id):
            return True
        if tweet and collipa.models.Thank.get(user_id=self.id, tweet_id=tweet.id):
            return True
        return False

    def is_reported(self, topic=None, reply=None, tweet=None):
        if topic and collipa.models.Report.get(user_id=self.id, topic_id=topic.id):
            return True
        if reply and collipa.models.Report.get(user_id=self.id, reply_id=reply.id):
            return True
        if tweet and collipa.models.Report.get(user_id=self.id, tweet_id=tweet.id):
            return True
        return False

    @property
    def unread_notification_count(self):
        return collipa.models.Notification.select(lambda rv:
                                                  rv.receiver_id == self.id and
                                                  rv.status == 0 and
                                                  rv.switch == 1).count()

    @property
    def notification_count(self):
        return collipa.models.Notification.select(lambda rv:
                                                  rv.receiver_id == self.id and
                                                  rv.status == 0 and
                                                  rv.switch == 1).count()

    def get_notifications(self, page=1, category='all'):
        if category == 'all':
            notifications = collipa.models.Notification.select(lambda rv:
                                                  rv.receiver_id == self.id)
        elif category == 'unread':
            notifications = collipa.models.Notification.select(lambda rv:
                                                  rv.receiver_id == self.id and rv.status == 0)
        else:
            return []
        notifications = notifications.order_by(lambda: orm.desc(rv.updated_at))
        return notifications[(page - 1) * config.paged: page * config.paged]

    @property
    def notifications(self):
        notifications = collipa.models.Notification.select(lambda rv: rv.receiver_id == self.id)
        return notifications

    @property
    def unread_notifications(self):
        notifications = collipa.models.Notification.select(lambda rv: rv.receiver_id == self.id and rv.status == 0)
        return notifications

    def read_notifications(self):
        notifications = self.unread_notifications
        for n in notifications:
            n.status = 1
        try:
            orm.commit()
        except Exception, e:
            print type(e).__name__
            print e
            raise

    @property
    def unread_message_box_count(self):
        return (collipa.models.MessageBox
                .select(lambda rv: rv.sender_id == self.id and rv.status == 0)
                .count())

    def get_message_boxes(self, page=1, category='all'):
        if category == 'all':
            message_boxes = (collipa.models.MessageBox
                             .select(lambda rv: rv.sender_id == self.id)
                             .order_by(lambda: orm.desc(rv.updated_at)))
        elif category == 'unread':
            message_boxes = (collipa.models.MessageBox
                             .select(lambda rv: rv.sender_id == self.id and rv.status == 0)
                             .order_by(lambda: orm.desc(rv.updated_at)))
        else:
            return []
        return message_boxes[(page - 1) * config.paged: page *
                             config.paged]

    def get_message_box(self, user=None):
        message_boxes = collipa.models.MessageBox.select(lambda rv:
                                                         rv.sender_id == self.id and
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
            if not v and k in ['address', 'website', 'description', 'style',
                               'site_style']:
                v = ''
            if v and k in ['style', 'site_style']:
                v = strip_tags(v)
            setattr(self, k, v)
        try:
            orm.commit()
        except:
            pass
        return self

    @staticmethod
    def get_users(page=1, category='all', limit=None):
        if category == 'all':
            users = orm.select(rv for rv in User).order_by(lambda:
                                                           orm.desc(rv.created_at))
        elif category == 'hot':
            users = mc.get('hot_users')
            if not users:
                if not limit:
                    limit = 8
                users = orm.select(rv for rv in User).order_by(lambda:
                                                               orm.desc(rv.thank_count * 4 +
                                                                        rv.up_count * 3 +
                                                                        rv.topic_count * 2 +
                                                                        rv.reply_count))[:limit]
                mc.set('hot_users', list(users), 60 * 60 * 12)
        elif category == 'new':
            users = orm.select(rv for rv in User).order_by(lambda: orm.desc(rv.created_at))
        else:
            return []

        if limit:
            return users[:limit]
        if page:
            return users[(page - 1) * config.user_paged: page *
                         config.user_paged]
        else:
            return users

    @staticmethod
    def mention(word):
        @memcached('word_' + str(word), 3600)
        def _func():
            return word and orm.select(rv for rv in User if
                                       (word in rv.name or
                                        word in rv.nickname))[:8] or []

        return _func()

    def get_followers(self, page=1):
        follower_ids = (orm.select(rv.who_id for rv in collipa.models.Follow
                                   if rv.whom_id == self.id)
                        .order_by(lambda: orm.desc(rv.created_at)) or [0])
        followers = orm.select(rv for rv in User if rv.id in follower_ids)
        if page:
            return followers[(page - 1) * config.user_paged: page * config.user_paged]
        else:
            return followers

    def get_followings(self, page=1):
        following_ids = (orm.select(rv.whom_id for rv in collipa.models.Follow
                                    if rv.who_id == self.id and rv.whom_id)
                         .order_by(lambda: orm.desc(rv.created_at)) or [0])
        followings = orm.select(rv for rv in User if rv.id in following_ids)
        if page:
            return followings[(page - 1) * config.user_paged: page * config.user_paged]
        else:
            return followings

    @property
    def is_online(self):
        key = self.KEY_ONLINE.format(self)
        return not not rd.get(key)

    @classmethod
    def online(cls, user_id):
        key = cls.KEY_ONLINE.format(Struct(id=user_id))
        rd.set(key, True)
        rd.sadd(cls.KEY_G_ONLINE, user_id)

    @classmethod
    def offline(cls, user_id):
        key = cls.KEY_ONLINE.format(Struct(id=user_id))
        rd.delete(key)
        rd.srem(cls.KEY_G_ONLINE, user_id)

    @classmethod
    def get_online_members(cls):
        return rd.smembers(cls.KEY_G_ONLINE) or []

    @classmethod
    def get_online_count(cls):
        return len(cls.get_online_members())
