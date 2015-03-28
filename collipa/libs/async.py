# coding: utf-8

__author__ = 'yetone'

from threading import Thread
from functools import wraps
import random
import time


def _worker(func, args, kwargs):
    func(*args, **kwargs)


def async(func):
    """ async decorator """
    @wraps(func)
    def _wrap(*args, **kwargs):
        t = Thread(target=_worker, args=(func, args, kwargs))
        thread_id = abs(random.randrange(1000000))
        t.setName('collipa-async-thread-%d' % thread_id)
        t.start()
    return _wrap

__all__ = ['async']

if __name__ == '__main__':

    @async
    def test1():
        print('test1 start')
        time.sleep(3)
        print('test1 stop')

    @async
    def test2():
        print('test2 start')
        time.sleep(3)
        print('test2 stop')

    def test3():
        print('test3 start')
        print('test3 stop')


    test0()
    test1()
    test2()
    test3()
