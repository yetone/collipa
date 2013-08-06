import models as m
from pony.orm import *
import config

m.db.generate_mapping()
config = config.rec()

@db_session
def do_sth():
    users = select(rv for rv in m.User if rv.role == 'unverify')
    message_boxes = m.MessageBox.select()

    for user in users:
        print user.name, user.nickname, user.email
    for mb in message_boxes:
        print mb.id
        mb.delete()
        commit()


if __name__ == '__main__':
    do_sth()
