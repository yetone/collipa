# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pony import orm
from models import *
from IPython import embed


@orm.db_session
def runshell():
    embed()

if __name__ == '__main__':
    db.generate_mapping()
    runshell()
