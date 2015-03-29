# coding: utf-8

import os

debug = True

db_user = "username"  # database username
db_pass = "password"  # database password
db_host = "localhost"  # database host
db_name = "collipa"  # database name

smtp_user = 'example@gmail.com'  # email username
smtp_pass = 'password'  # email password
smtp_host = 'smtp.gmail.com'  # email host
smtp_port = '587'  # email port
smtp_ssl = True

rd_port = 6379  # Redis port

cookie_secret = 'cookiesecret'  # cookie secret
password_secret = 'passwordsecret'  # password secret

site_name = 'Collipa'
site_url = 'http://127.0.0.1:8008'
site_description = 'Good'

paged = 18
reply_paged = 25
user_paged = 30
node_paged = 32
default_timezone = 'Asia/Shanghai'

root_path = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(root_path, 'views')
static_path = os.path.join(root_path, 'static')
upload_path = os.path.join(static_path, 'upload')
user_avatar_url = '/static/public/img/avatar.png'
user_head_url = '/static/public/img/user_head.jpg'
user_background_url = '/static/public/img/user_background.jpg'

node_icon_url = '/static/public/img/node_icon.png'
node_head_url = '/static/public/img/node_head.jpg'
node_background_url = '/static/public/img/node_background.jpg'

default_album_cover = '/static/public/img/cover.jpg'

forbidden_name_list = ['start', 'about', 'links', 'contact', 'user',
                       'users', 'admin', 'dashboard', 'setting',
                       'settings', 'topic', 'topics', 'reply', 'replies',
                       'login', 'register', 'logout', 'signin', 'signup',
                       'signout', 'static', 'statics', 'public', 'publics',
                       'password', 'account', 'accounts', 'node', 'nodes',
                       'post', 'posts', 'comment', 'comments',
                       'notification', 'notifications', 'api', 'apis',
                       'faq', 'help', 'helps', 'helper', 'helpers', 'bot',
                       'bots', 'computer', 'compute', 'collect',
                       'collects', 'collection', 'collections', 'thank',
                       'up', 'down', 'give', 'news', 'hot', 'hots',
                       'timeline', 'goodnews', 'other', 'ad', 'ads',
                       'site', 'sites', 'collipa', 'image', 'images',
                       'upload', 'message', 'messages', 'bank', 'coin',
                       'balance', 'new', 'some', 'controller', 'control',
                       'show', 'friend', 'friends', '404', '502', '503',
                       '302', 'test', 'success', 'error', 'information',
                       'index', 'home', 'a', 'b', 'c', '0', '1', '2',
                       'status', 'inform', 'notice', 'notify', 'superman',
                       'superwoman', 'superchild', 'god', 'photo',
                       'photos', 'city', 'boy', 'boys', 'girl', 'girls',
                       'discussion', 'discussions', 'note', 'book',
                       'music', 'movie', 'shop', 'life', 'live', 'baby',
                       'love', 'me', 'mine', 'blog', 't']

bank_init_coin = 6300000
user_init_coin = 2100
invite_coin = 60
topic_create_coin = 20
reply_create_coin = 5
topic_edit_coin = 10
reply_edit_coin = 5
topic_hot_coin = 40
reply_hot_coin = 15
topic_report_coin = 20
reply_report_coin = 10
thank_coin = 5
collect_coin = 5

thank_delta_time = 60 * 5

topic_compute_count = 6
reply_compute_count = 6

user_edit_nickname_count = 7
user_edit_urlname_count = 3

topic_compute_key_list = [20, 60, 140, 300, 620, 1260]
reply_compute_key_list = [20, 60, 140, 300, 620, 1260]

try:
    from collipa.local_config import *  # NOQA
except ImportError:
    pass

database = 'mysql://%s:%s@%s/%s?charset=utf8' % (db_user, db_pass, db_host,
                                                 db_name)

