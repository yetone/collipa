import models as m
from pony.orm import *
import config

m.db.generate_mapping()
config = config.rec()

@db_session
def do_sth():
    users = select(rv for rv in m.User if rv.role == 'unverify')
    message_boxes = m.MessageBox.select()
    messages = m.Message.select()

    for user in users:
        print user.name, user.nickname, user.email
    for ms in messages:
        print ms.id
        try:
            ms.receiver_id = ms.message_box1.receiver_id
            commit()
        except:
            print "error"
    """
    for mb in message_boxes:
        print mb.id
        mb.delete()
        commit()
    """


if __name__ == '__main__':
    do_sth()
