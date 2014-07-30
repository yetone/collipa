#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'glcsnz123, laurence@duitang.com'

import os
import commands
import subprocess

class GifInfo:  # gifsicle -I

    def __init__(self, imgfile=None):
        self.__rotate = ""
        self.__crops = ""
        self.__resizes = ""
        self.src = ""
        if imgfile and os.path.isfile(imgfile): 
            self.src = imgfile

    def resize_gif(self, width=None, height=None):
        if width is None and height is None: return False
        if width is None:
            self.__resizes = " --resize-height %d " % height
            return True
        if height is None:
            self.__resizes = " --resize-width %d " % width
            return True
        self.__resizes = " --resize %dx%d" % (width, height)
        return True

    def resize_fit_gif(self, width=None, height=None):
        if width is None and height is None: return False
        if width is None:
            self.__resizes = " --resize-fit-height %d " % (height)
            return True
        if height is None:
            self.__resizes = " --resize-fit-width %d " % (width)
            return True
        self.__resizes = " --resize-fit %dx%d " % (width, height)
        return True


    def fix_scale(self, Xscale, Yscale=None):
        self.__resizes = " --scale " + str(Xscale / 100.0)
        if Yscale is not None:
            self.__resizes += "x" + str(Yscale / 100.0)
        self.__resizes += " "

    def rotate_gif(self, degree=0):
        if degree == 90 or degree == "90":
            self.__rotate = " --rotate-90 "
        elif degree == 180 or degree == "180":
            self.__rotate = " --rotate-180 "
        elif degree == 270 or degree == "270":
            self.__rotate = " --rotate-270 "
        else:
            return False
        return True

    def crop_gif_bypos(self, lefttop, rightdown):
        if rightdown[0] < lefttop[0] or rightdown[1] < lefttop[1]: return False
        self.__crops = " --crop " + ','.join(map(str, lefttop)) + "-" + ",".join(map(str, rightdown)) + " "
        return True

    def crop_gif_bywh(self, lefttop, wh):
        if wh[0] <= 0 or wh[1] <= 0: return False
        self.__crops = " --crop " + ",".join(map(str, lefttop)) + "+" + "x".join(map(str, wh)) + " "
        return True

    def __str__(self):
        return " ".join([self.__crops, self.__rotate, self.__resizes, self.src if self.src else ''])


class Gifsicle:
    def __init__(self):
        pass

    def convert(self, infile, outfile=None):
        if outfile is None:
            res = commands.getstatusoutput("gifsicle --batch " + str(infile))
            if res[0] == 0:
                return True
            return False
        res = commands.getstatusoutput("gifsicle " + str(infile) + " > " + outfile)
        if res[0] == 0:
            return True
        return False
    
    def convert_with_pipe(self, infile, img):
        p = subprocess.Popen(["gifsicle " + str(infile)], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.stdin.write(img)
        res = p.communicate()
        if p.returncode != 0:
            raise Exception('gifsicle cannot close')
        return res[0]

if __name__ == '__main__':
    import sys
    import time
    src = sys.argv[1]
    dest = sys.argv[2]
#    gi = GifInfo(src)
    ts = time.time()
    gi = GifInfo()
#    gi.crop_gif_bywh((23, 23), (220, 220))
#    gi.rotate_gif(90)
#    gi.fix_scale(50, 50)
    gi.resize_fit_gif(100, 100)
    gf = Gifsicle()
#    gf.convert(gi, "/tmp/" + dest)
    ret = gf.convertWithPipe(gi, open(src).read())
    print time.time() - ts, "ms"
    print type(ret), len(ret)
    print str(gi)
    with open(dest, 'w') as fl:
        fl.write(ret)

