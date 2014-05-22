# coding: utf-8

from HTMLParser import HTMLParser
import os
import re
import time
import config
import models as m
from libs import xss

config = config.rec()


class UsernameParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.names = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == 'data-username':
                        self.names.append(value)

def require_admin(func):
    def wrap(self, *args, **kwargs):
        if self.current_user and self.current_user.is_admin:
            return func(self, *args, **kwargs)
        result = {"status": "error", "message": "对不起，您没有相关权限"}
        self.send_result(result)
    return wrap

def require_permission(func):
    def wrap(self, *args, **kwargs):
        if self.current_user and\
            (self.current_user.role != 'unverify' or self.current_user.is_admin):
            return func(self, *args, **kwargs)
        if self.current_user.role == 'unverify':
            result = {"status": "error", "message": "对不起，您的账户尚未激活，请到注册邮箱检查激活邮件"}
        else:
            result = {"status": "error", "message": "对不起，您没有相关权限"}
        self.send_result(result)
    return wrap

def get_day(timestamp):
    FORY = '%d'
    os.environ["TZ"] = config.default_timezone
    time.tzset()
    str = time.strftime(FORY, time.localtime(timestamp))
    return str

'''
def get_month(timestamp):
    FORY = '%b'
    os.environ["TZ"] = config.default_timezone
    time.tzset()
    str = time.strftime(FORY, time.localtime(timestamp))
    return str
'''

def format_date(timestamp):
    FORY = '%Y-%m-%d @ %H:%M'
    FORM = '%m-%d @ %H:%M'
    FORH = '%H:%M'
    os.environ["TZ"] = config.default_timezone
    time.tzset()
    rtime = time.strftime(FORM, time.localtime(timestamp))
    htime = time.strftime(FORH, time.localtime(timestamp))
    now = int(time.time())
    t = now - timestamp
    if t < 60:
        str = '刚刚'
    elif t < 60 * 60:
        min = t / 60
        str = '%d 分钟前' % min
    elif t < 60 * 60 * 24:
        h = t / (60 * 60)
        str = '%d 小时前 %s' % (h, htime)
    elif t < 60 * 60 * 24 * 3:
        d = t / (60 * 60 * 24)
        if d == 1:
            str = '昨天 ' + rtime
        else:
            str = '前天 ' + rtime
    else:
        str = time.strftime(FORY, time.localtime(timestamp))
    return str

def format_date2(timestamp):
    FORY = '%Y-%m-%d @ %H:%M'
    os.environ["TZ"] = config.default_timezone
    time.tzset()
    str = time.strftime(FORY, time.localtime(timestamp))
    return str

def get_year():
    timestamp = int(time.time())
    FORY = '%Y'
    os.environ["TZ"] = config.default_timezone
    time.tzset()
    str = time.strftime(FORY, time.localtime(timestamp))
    return str

def get_month():
    timestamp = int(time.time())
    FORY = '%m'
    os.environ["TZ"] = config.default_timezone
    time.tzset()
    str = time.strftime(FORY, time.localtime(timestamp))
    return str

def format_text(text):
    floor = ur'#(\d+)楼\s'
    for match in re.finditer(floor, text):
        url = match.group(1)
        floor = match.group(0)
        nurl = '<a class="toreply" href="#;">#<span class="tofloor">%s</span>楼 </a>' % (url)
        text = text.replace(floor, nurl)
    return text

def reply_content(text):
    return text[0:26]


def regex(pattern, data, flags=0):
    if isinstance(pattern, basestring):
        pattern = re.compile(pattern, flags)

    return pattern.match(data)


def email(data):
    pattern = r'^.+@[^.].*\.[a-z]{2,10}$'
    return regex(pattern, data, re.IGNORECASE)


def url(data):
    pattern = (
        r'(?i)^((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}'
        r'/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+'
        r'|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))$')
    return regex(pattern, data, re.IGNORECASE)


def username(data):
    pattern = r'^[a-zA-Z0-9]+$'
    return regex(pattern, data)

def get_mention_names(content):
    up = UsernameParser()
    up.feed(content)
    up.close()
    names1 = up.names
    names = {}.fromkeys(names1).keys()
    return names

def strip_tags(html):
    if html:
        html = html.strip()
        html = html.strip("\n")
        result = []
        parse = HTMLParser()
        parse.handle_data = result.append
        parse.feed(html)
        parse.close()
        return "".join(result)
    return ''

def strip_xss_tags(html):
    return xss.parsehtml(html)

def filter_img_tags(htmlstr):
    re_img = re.compile('<\s*img[^>]*>', re.L)
    re_br = re.compile('<br\s*?/?>')
    s = re_img.sub('', htmlstr)
    s = re_br.sub('', s)
    return s

def get_img_list(text):
    img_path = ur'\/static\/[^\s\"]*\.(jpg|jpeg|png|bmp|gif)'
    path_list = []
    for match in re.finditer(img_path, text):
        path = match.group(0)
        path_list += [path]
    return path_list

def force_int(value, default=1):
    try:
        return int(value)
    except:
        return default

class _Missing(object):

    def __repr__(self):
        return 'no value'

    def __reduce__(self):
        return '_missing'

_missing = _Missing()

class cached_property(object):
    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, _missing)
        if value is _missing:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value
