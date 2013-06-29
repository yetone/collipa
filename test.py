import models as m
from pony.orm import *
import config

m.db.generate_mapping()
config = config.rec()

users = select(rv for rv in m.User if rv.urlname in config.forbidden_name_list)

for user in users:
    print user.name, user.urlname
