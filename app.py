# coding: utf-8

import os.path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from libs.tornadomail.backends.smtp import EmailBackend

import config
from controllers import uimodules
from models import db
from routers import routers

config = config.Config()
define("port", default=8008, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "views"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
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
            config.smtp_host, int(config.smtp_port), config.smtp_user,
            config.smtp_password,
            True
        )


def main():
    db.generate_mapping()
    tornado.options.parse_command_line()
    tornado.httpserver.HTTPServer(Application(),
                                  xheaders=True).listen(options.port)
    print("App started. Listenning on %d" % options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
