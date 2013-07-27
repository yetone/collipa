# coding: utf-8

import os
import sys
import getopt
import MySQLdb
from pony.orm import *
import config

config = config.rec()

m = MySQLdb.Connect(host=config.db_host, user=config.db_user, passwd=\
    config.db_pass)
c = m.cursor()

@db_session
def init_node():
    from models import Node
    if not Node.get(id=1):
        Node(name=u'根节点', urlname='root',
                description=u'一切的根源').save()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "", ["install", "init",
            "iwanttodropdatabase"])
    except getopt.GetoptError:
        print("参数错误")
        sys.exit(2)

    for opt, val in opts:
        if opt == "--init":
            try:
                c.execute("create database %s" % config.db_name)
                c.execute("grant all privileges on %s.* to '%s'@'localhost' identified by '%s'" % (config.db_name, config.db_user, config.db_pass))
                c.execute("flush privileges")

                c.close()
                m.commit()
                m.close()
            except:
                pass
            from models import db
            db.generate_mapping(create_tables=True)
            init_node()
            print("数据库表初始化成功")
        if opt == '--iwanttodropdatabase':
            key = raw_input("你确定要删除数据库？所有数据将消失，且无法恢复！！！(若确定请输入yes i do,否则直接按回车键！):\n")
            if key == "yes i do":
                key = raw_input("你确定要删除数据库？所有数据将消失，且无法恢复！！！(若确定请输入yes i do,否则直接按回车键！):\n")
            if key == "yes i do":
                key = raw_input("你确定要删除数据库？所有数据将消失，且无法恢复！！！(若确定请输入yes i do,否则直接按回车键！):\n")
            if key == "yes i do":
                try:
                    c.execute("drop database %s" % config.db_name)
                except Exception as e:
                    print(e)
                finally:
                    pass

                c.close()
                m.commit()
                m.close()
                print("已清空数据库！")
            else:
                print("已取消操作！")

        if opt == "--install":
            base_path = sys.path[0]
            try:
                print(requirements_path)
                os.system('sudo python %s/libs/pony/setup.py install' %
                        base_path)
                os.system('sudo pip install -r %s/requirements.txt' %
                        base_path)
            except Exception as e:
                print(e)
            finally:
                print("依赖安装成功")

if __name__ == "__main__":
    main(sys.argv[1:])
