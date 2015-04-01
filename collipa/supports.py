__author__ = 'yetone'


class Struct:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
