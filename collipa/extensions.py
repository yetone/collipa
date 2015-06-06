# coding: utf-8

import re
from collipa import config
import memcache
import redis
import cPickle as pickle
from functools import wraps

mc = memcache.Client(['127.0.0.1:11211'], debug=1)

rd = redis.StrictRedis(host='127.0.0.1', port=config.rd_port, db=0)


def memcached(key, limit=86400):
    def wrap(func):
        @wraps(func)
        def get_value(*args, **kwargs):
            value = mc.get(key)
            if not value:
                value = func(*args, **kwargs)
                mc.set(key, value, limit)
            return value
        return get_value
    return wrap


def img_convert(text):
    img_url = ur'http[s]:\/\/[^\s\"]*\.(jpg|jpeg|png|bmp|gif)'
    for match in re.finditer(img_url, text):
        url = match.group(0)
        img_tag = '![](%s)' % url
        text = text.replace(url, img_tag)
    return text


def pk(name, value=None):
    if value:
        try:
            f = file('/dev/shm/' + name + '.pkl', 'wb')
            pickle.dump(value, f, 2)
            f.close()
            return True
        except Exception, e:
            print e
            return False
    try:
        f = file('/dev/shm/' + name + '.pkl', 'rb')
        value = pickle.load(f)
        f.close()
        return value
    except:
        return None
