#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'glcsnz123, laurence@duitang.com'

import os
import commands
import subprocess
from StringIO import StringIO


class GifInfo:  # gifsicle -I

    def __init__(self, img_file=None):
        self.__rotate = ""
        self.__crops = ""
        self.__resizes = ""
        self.src = ""
        self.__args = []
        if img_file and os.path.isfile(img_file):
            self.src = img_file

    def resize_gif(self, width=None, height=None):
        if width is None and height is None:
            return False

        if width is None:
            self.__resizes = " --resize-height %d " % height
        elif height is None:
            self.__resizes = " --resize-width %d " % width
        else:
            self.__resizes = " --resize %dx%d" % (width, height)

        self.__args.append(self.__resizes)
        return True

    def resize_fit_gif(self, width=None, height=None):
        if width is None and height is None:
            return False

        if width is None:
            self.__resizes = " --resize-fit-height %d " % (height)
        elif height is None:
            self.__resizes = " --resize-fit-width %d " % (width)
        else:
            self.__resizes = " --resize-fit %dx%d " % (width, height)

        self.__args.append(self.__resizes)
        return True

    def fix_scale(self, x_scale, y_scale=None):
        self.__resizes = " --scale " + str(x_scale / 100.0)
        if y_scale is not None:
            self.__resizes += "x" + str(y_scale / 100.0)
        self.__resizes += " "

        self.__args.append(self.__resizes)
        return True

    def rotate_gif(self, degree=0):
        if degree == 90 or degree == "90":
            self.__rotate = " --rotate-90 "
        elif degree == 180 or degree == "180":
            self.__rotate = " --rotate-180 "
        elif degree == 270 or degree == "270":
            self.__rotate = " --rotate-270 "
        else:
            return False

        self.__args.append(self.__rotate)
        return True

    def crop_gif_bypos(self, left_top, right_down):
        if right_down[0] < left_top[0] or right_down[1] < left_top[1]:
            return False
        self.__crops = " --crop " + ','.join(map(str, left_top)) + "-" + ",".join(map(str, right_down)) + " "

        self.__args.append(self.__crops)
        return True

    def crop_gif_bywh(self, left_top, width_height):
        if width_height[0] <= 0 or width_height[1] <= 0:
            return False
        self.__crops = " --crop " + ",".join(map(str, left_top)) + "+" + "x".join(map(str, width_height)) + " "

        self.__args.append(self.__crops)
        return True

    def __str__(self):
        args = self.__args[:]
        args.append(self.src)
        return " ".join(args)

    @property
    def resizes(self):
        return self.__resizes

    @property
    def crops(self):
        return self.__crops


class GifSicle:

    def __init__(self):
        pass

    @staticmethod
    def convert(infile, outfile=None):
        if outfile is None:
            res = commands.getstatusoutput("gifsicle --batch " + str(infile))
            if res[0] == 0:
                return True
            return False
        res = commands.getstatusoutput("gifsicle " + str(infile) + " > " + outfile)
        if res[0] == 0:
            return True
        return False

    @staticmethod
    def convert_with_pipe(infile, img):
        p = subprocess.Popen(["gifsicle " + str(infile)], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.stdin.write(img)
        res = p.communicate()
        if p.returncode != 0:
            raise Exception('gifsicle cannot close')

        return res[0]

    @staticmethod
    def _c(infile, img):
        res = None
        if infile.resizes:
            p = subprocess.Popen(["gifsicle " + str(infile.resizes)], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            p.stdin.write(img)
            res = p.communicate()
            if p.returncode != 0:
                raise Exception('gifsicle cannot close')
        if infile.crops:
            if res is not None:
                img = StringIO(res[0]).getvalue()
            p = subprocess.Popen(["gifsicle " + str(infile.crops)], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            p.stdin.write(img)
            res = p.communicate()
            if p.returncode != 0:
                raise Exception('gifsicle cannot close')
        if res is None:
            p = subprocess.Popen(["gifsicle " + str(infile)], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            p.stdin.write(img)
            res = p.communicate()
            if p.returncode != 0:
                raise Exception('gifsicle cannot close')

        return res[0]
