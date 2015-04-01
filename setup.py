# coding: utf-8

import re
import sys
import getopt
import MySQLdb
from pony.orm import db_session
from collipa import config


@db_session
def init_node():
    from collipa.models import Node
    if not Node.get(id=1):
        Node(name=u'根节点', urlname='root',
             description=u'一切的根源').save()


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def merge():
    m = MySQLdb.connect(host=config.db_host, user=config.db_user,
                        passwd=config.db_pass, db=config.db_name)
    c = m.cursor()

    c.execute(r'show tables')
    old_table_names = [x[0] for x in c]

    try:
        for old_table_name in old_table_names:
            table_name = old_table_name.lower()
            sql = r'RENAME TABLE %s TO %s' % (old_table_name, table_name)
            print(sql)
            c.execute(sql)

        c.close()
        m.commit()
        m.close()
    except Exception as e:
        print(type(e).__name__)
        print(e)
        raise


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "", ["install", "init",
                                              "iwanttodropdatabase", 'merge'])
    except getopt.GetoptError:
        print("参数错误")
        sys.exit(2)

    for opt, val in opts:
        if opt == '--merge':
            merge()
            print('merge 成功！')

        if opt == "--init":
            m = MySQLdb.connect(host=config.db_host, user=config.db_user,
                                passwd=config.db_pass)
            c = m.cursor()

            # create database
            try:
                c.execute("create database %s" % config.db_name)
                c.execute("grant all privileges on %s.* to '%s'@'localhost' identified by '%s'" %
                          (config.db_name, config.db_user, config.db_pass))
                c.execute("flush privileges")

                c.close()
                m.commit()
                m.close()
            except Exception:
                pass

            # create tables
            from collipa.models import db
            db.generate_mapping(create_tables=True)
            init_node()
            print("数据库表初始化成功")


if __name__ == "__main__":
    main(sys.argv[1:])
