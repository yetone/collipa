# coding: utf-8

import os
import errno
import re
import time
import random
import logging
import math
from functools import wraps
from datetime import datetime
from HTMLParser import HTMLParser

from collipa import config
from collipa.libs import xss
from collipa.libs.pil import Image


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
    @wraps(func)
    def wrap(self, *args, **kwargs):
        if self.current_user and self.current_user.is_admin:
            return func(self, *args, **kwargs)
        result = {"status": "error", "message": "对不起，您没有相关权限"}
        self.send_result(result)
    return wrap


def require_permission(func):
    @wraps(func)
    def wrap(self, *args, **kwargs):
        if self.current_user and (self.current_user.role != 'unverify' or
                                  self.current_user.is_admin):
            return func(self, *args, **kwargs)
        if not self.current_user:
            result = {"status": "error",
                      "message": "请登陆"}
        elif self.current_user.role == 'unverify':
            result = {"status": "error",
                      "message": "对不起，您的账户尚未激活，请到注册邮箱检查激活邮件"}
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
    r_time = time.strftime(FORM, time.localtime(timestamp))
    h_time = time.strftime(FORH, time.localtime(timestamp))
    now = int(time.time())
    t = now - timestamp
    if t < 60:
        format_str = '刚刚'
    elif t < 60 * 60:
        min = t / 60
        format_str = '%d 分钟前' % min
    elif t < 60 * 60 * 24:
        h = t / (60 * 60)
        format_str = '%d 小时前 %s' % (h, h_time)
    elif t < 60 * 60 * 24 * 3:
        d = t / (60 * 60 * 24)
        if d == 1:
            format_str = '昨天 ' + r_time
        else:
            format_str = '前天 ' + r_time
    else:
        format_str = time.strftime(FORY, time.localtime(timestamp))
    return format_str


def format_date2(timestamp):
    FORY = '%Y-%m-%d @ %H:%M'
    os.environ["TZ"] = config.default_timezone
    time.tzset()
    format_str = time.strftime(FORY, time.localtime(timestamp))
    return format_str


def get_year():
    timestamp = int(time.time())
    FORY = '%Y'
    os.environ["TZ"] = config.default_timezone
    time.tzset()
    format_str = time.strftime(FORY, time.localtime(timestamp))
    return format_str


def get_month():
    timestamp = int(time.time())
    FORY = '%m'
    os.environ["TZ"] = config.default_timezone
    time.tzset()
    format_str = time.strftime(FORY, time.localtime(timestamp))
    return format_str


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


def get_mentions(content):
    username_re = re.compile(r'@(?P<username>[A-Za-z0-9]+)(</p>|&nbsp;|\n|\s|$)')
    match = username_re.finditer(content)
    return [(m.start(), m.group('username')) for m in match] if match else []


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
    return xss.parse_html(html)


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
    except TypeError:
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


def pattern_image_url(url):
    ret = {}
    m = re.findall(r"(.*)\.thumb\.(\d+)_(\d+)[_]?([tcb]?)\.(\w+)", url)
    if m:
        ret['thumb'] = True
        ori, w, h, crop, suffix = m[0]
        ret['resize'] = (int(w), int(h))
        ret['width'] = int(w)
        ret['height'] = int(h)
        ret['crop'] = crop
        ret['gaussian'] = True if crop == 'g' else False
        ret['origin'] = '%s.%s' % (ori, suffix)
    return ret


def gen_thumb_url(url, size, position='c'):
    width, height = size
    img_param = pattern_image_url(url)
    if img_param:
        url = img_param['origin']
    m = re.findall(r"(.*)\.(\w+)$", url)
    if not m:
        return url
    ori, suffix = m[0]
    return '%s.thumb.%d_%d_%s.%s' % (ori, width, height, position, suffix)


def save_image(image, path):
    image.save(path)


def rcd(x):
    return int(math.ceil(x))


def crop(url, size, position='c', force=False):
    url = "%s/%s" % (config.root_path, url.lstrip('/'))
    path = gen_thumb_url(url, size, position=position)
    width, height = size
    try:
        image = Image.open(url)
    except IOError:
        logging.error('cannot open %s' % url)
        return
    w, h = image.size
    if (w, h) == (width, height):
        return save_image(image, path)
    if force and (width >= w or height >= h):
        return save_image(image, path)

    hr = height * 1.0 / h
    wr = width * 1.0 / w
    if hr > wr:
        wf = rcd(w * hr)
        hf = height
    else:
        wf = width
        hf = rcd(h * wr)
    resize = (wf, hf)
    image = image.resize(resize, Image.ANTIALIAS)

    if width * height == 0:
        return save_image(image, path)

    coo = None
    if wf > width:
        if position == 't':
            coo = (0, 0, width, height)
        elif position == 'b':
            coo = (wf - width, 0, wf, height)
        else:
            coo = (rcd((wf - width) / 2.0), 0, rcd((wf + width) / 2.0), height)
    elif hf > height:
        if position == 't':
            coo = (0, 0, width, height)
        elif position == 'b':
            coo = (0, hf - height, width, hf)
        else:
            coo = (0, rcd((hf - height) / 2.0), width, rcd((hf + height) / 2.0))

    if coo:
        image = image.crop(coo)
    return save_image(image, path)


def gen_random_str(n=6):
    return ''.join(random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba', n))


def gen_upload_dir():
    now = datetime.now()
    upload_dir = os.path.join(config.root_path, 'static/upload/image', now.strftime("%Y/%m/"))
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return upload_dir


def gen_filename(suffix='jpeg'):
    timestamp = int(time.time())
    filename = '%d_%s.%s' % (timestamp, gen_random_str(), suffix)
    return filename


def gen_upload_path(suffix='jpeg'):
    upload_dir = gen_upload_dir()
    filename = gen_filename(suffix)
    upload_path = os.path.join(upload_dir, filename)
    return upload_path


def get_relative_path(absolute_path):
    return os.path.relpath(absolute_path, config.root_path)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_asset_path(relative_path):
    relative_path = relative_path.lstrip('/')
    if relative_path.startswith('static/'):
        return os.path.join(config.root_path, relative_path)
    return os.path.join(config.static_path, relative_path)


def remove_file(file_path):
    if not os.path.isfile(file_path):
        return
    os.remove(file_path)


def collect_items_from_query(query, from_id, limit, attr_name=None):
    can_append = False
    items = []
    i = 0

    for item in query:
        i += 1
        if i > 1000:
            break

        if len(items) >= limit:
            break

        if can_append:
            items.append(item)
            continue

        if (attr_name and getattr(item, attr_name) or item) == from_id:
            can_append = True

    return items


def extract_urls(content):
    iter_m = re.finditer('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
    return (m.string for m in iter_m)


def process_content(content):
    content = process_music(content)
    content = process_video(content)
    return content


def process_music(content):
    content = process_163music(content)
    return content


def process_video(content):
    content = process_youtube(content)
    return content


def process_163music(content):
    embed_tpl = '<div class="music-wrapper"><iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width="330" height="86" src="http://music.163.com/outchain/player?type=2&id={music_id}&auto=0&height=66"></iframe></div>'
    music_ids = re.findall(r'http://music\.163\.com/#/m/song\?id=(?P<music_id>\d+)', content)
    for music_id in music_ids:
        content = content.replace('http://music.163.com/#/m/song?id={}'.format(music_id), embed_tpl.format(music_id=music_id))
    return content


def process_youtube(content):
    embed_tpl = '<div class="video-wrapper youtube"><iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe></div>'
    for url in extract_urls(content):
        match = re.search(r'http[s]?://youtu.be/(?P<video_id>[^/]+)', url)
        if match:
            content = content.replace(url, embed_tpl.format(**match.groupdict()))
        match = re.search(r'http[s]?://www\.youtube\.com/watch\?(|.*&)v=(?P<video_id>[^&]+)', url)
        if match:
            content = content.replace(url, embed_tpl.format(**match.groupdict()))
    return content
