# coding: utf-8

_DBUSER = "username" # 数据库用户名
_DBPASS = "password" # 数据库密码
_DBHOST = "localhost" # 数据库地址
_DBNAME = "collipa" # 数据库名称

_SMTPUSER = 'example@gmail.com' # 邮箱用户名
_SMTPPASS = 'password' # 邮箱密码
_SMTPHOST = 'smtp.gmail.com' # 邮箱地址
_SMTPPORT = '587' # 邮箱端口

_RDPORT = 6379 # Redis port

class rec:
    database = 'mysql://%s:%s@%s/%s?charset=utf8' % (_DBUSER, _DBPASS, _DBHOST, _DBNAME)

    db_user = _DBUSER
    db_pass = _DBPASS
    db_host = _DBHOST
    db_name = _DBNAME

    rd_port = _RDPORT

    cookie_secret = 'cookiesecret' # cookie secret
    password_secret = 'passwordsecret' # password secret

    site_name = 'Collipa'
    site_url = 'http://127.0.0.1:8008'
    site_description = 'Good'

    paged = 18
    reply_paged = 25
    user_paged = 30
    node_paged = 32
    default_timezone = 'Asia/Shanghai'

    user_avatar_url = '/static/public/img/avatar.png'
    user_head_url = '/static/public/img/user_head.jpg'
    user_background_url = '/static/public/img/user_background.jpg'

    node_icon_url = '/static/public/img/node_icon.png'
    node_head_url = '/static/public/img/node_head.jpg'
    node_background_url = '/static/public/img/node_background.jpg'

    smtp_user = _SMTPUSER
    smtp_password = _SMTPPASS
    smtp_host = _SMTPHOST
    smtp_port = _SMTPPORT
    smtp_ssl = True

    forbidden_name_list = ['start', 'about', 'links', 'contact', 'user',
            'users', 'admin', 'dashboard', 'setting', 'settings', 'topic',
            'topics', 'reply', 'replies', 'login', 'register', 'logout',
            'signin', 'signup', 'signout', 'static', 'statics',
            'public', 'publics', 'password',
            'account', 'accounts', 'node', 'nodes', 'post', 'posts',
            'comment', 'comments',
            'notification', 'notifications', 'api', 'apis', 'faq', 'help',
            'helps', 'helper', 'helpers', 'bot', 'bots', 'computer', 'compute',
            'collect', 'collects', 'collection', 'collections', 'thank', 'up',
            'down', 'give', 'news', 'hot', 'hots', 'timeline', 'goodnews',
            'other', 'ad', 'ads', 'site', 'sites', 'collipa', 'image',
            'images', 'upload', 'message', 'messages', 'bank', 'coin',
            'balance', 'new', 'some', 'controller', 'control', 'show',
            'friend', 'friends', '404', '502', '503', '302', 'test', 'success',
            'error', 'information', 'index', 'home', 'a', 'b', 'c', '0', '1',
            '2', 'status', 'inform', 'notice', 'notify', 'superman',
            'superwoman', 'superchild', 'god', 'photo', 'photos', 'city',
            'boy', 'boys', 'girl', 'girls', 'discussion', 'discussions',
            'note', 'book', 'music', 'movie', 'shop', 'life', 'live', 'baby',
            'love', 'me', 'mine', 'blog']

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
