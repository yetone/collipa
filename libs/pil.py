# coding: utf-8

__author__ = 'yetone'

from StringIO import StringIO
from libs.async import async
from PIL import Image as Img
from libs.pysicle import GifInfo, GifSicle
import logging

logger = logging.getLogger()


class Image(object):

    ANTIALIAS = Img.ANTIALIAS

    def __init__(self, fp, mode='r'):
        img = Img.open(fp, mode)
        self.img = img
        self.format = img.format
        self.is_gif = img.format.lower() == 'gif'
        self.gi = GifInfo()
        self.gf = GifSicle()
        self.fp = fp
        self.size = img.size
        self.filename = img.filename
        self.tmp = None

    def get_raw(self):
        raw = self.fp
        if type(self.fp) in (str, unicode):
            f = open(self.fp, 'rb')
            raw = f.read()
            f.close()
        elif isinstance(self.fp, StringIO):
            raw = self.fp.getvalue()
        return raw

    def resize(self, size, resample=Img.ANTIALIAS):
        if self.is_gif:
            width, height = size
            self.gi.resize_fit_gif(width, height)
        self.img = self.img.resize(size, resample)
        return self

    def crop(self, box=None):
        if self.is_gif:
            x, y, w, h = box
            self.gi.crop_gif_bywh((x, y), (w, h))
        self.img = self.img.crop(box)
        return self

    def save(self, fp, format=None, **params):
        if 'quality' not in params:
            params['quality'] = 95
        if self.is_gif:
            self.get_data_and_write(fp, format=format, **params)
        else:
            self.img.save(fp, format, **params)

    def get_data_and_write(self, fp, format=None, **params):
        try:
            raw = self.tmp or self.get_raw()
            data = self.gf.convert_with_pipe(self.gi, raw)
            with open(fp, 'wb') as f:
                f.write(data)
        except Exception:
            logger.info('gif can not save. fp: %s' % fp)
            self.img.save(fp, format, **params)

    @staticmethod
    def open(fp, mode='r'):
        return Image(fp, mode)
