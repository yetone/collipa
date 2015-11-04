# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from script_manager import Manager

import tornado.httpserver
import tornado.ioloop
import tornado.web

from collipa.libs.tornadomail.backends.smtp import EmailBackend

from collipa import config
from collipa.controllers import uimodules
from collipa.models import db
from collipa.routers import routers


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            template_path=config.template_path,
            static_path=config.static_path,
            ui_modules=uimodules,
            xsrf_cookies=True,
            cookie_secret=config.cookie_secret,
            autoescape=None,
            site_url=config.site_url,
            site_title=config.site_name,
            site_name=config.site_name,
            login_url="/signin",
            debug=config.debug,
        )

        tornado.web.Application.__init__(self, routers, **settings)

    @property
    def mail_connection(self):
        return EmailBackend(
            config.smtp_host,
            int(config.smtp_port),
            config.smtp_user,
            config.smtp_pass,
            True
        )

app_manager = Manager()


@app_manager.command
def runserver(port=8080, address="127.0.0.1"):
    port = int(port)
    db.generate_mapping()
    tornado.httpserver.HTTPServer(Application(),
                                  xheaders=True).listen(port, address)
    print("App started. Listening on {}:{}".format(address, port))
    tornado.ioloop.IOLoop.instance().start()
