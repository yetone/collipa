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
    count = 0
    delete_count = 0

    for user in users:
        print user.name, user.nickname, user.email
    for ms in messages:
        print ms.receiver_id
        if not ms.message_box1:
            delete_count += 1
            ms.delete()
            continue
        if ms.receiver_id != ms.message_box1.receiver_id:
            print ms.id
            count += 1
            try:
                ms.receiver_id = ms.message_box1.receiver_id
            except:
                print "error"
    print("The mistake message count is %s" % count)
    print("The deleted message count is %s" % delete_count)
    """
    for mb in message_boxes:
        print mb.id
        mb.delete()
        commit()
    """


if __name__ == '__main__':
    do_sth()
