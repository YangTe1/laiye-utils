"""服务启动文件
多进程模式下, autoreload 必须为 False
"""
import os
import traceback

import tornado
import tornado.options
import tornado.web
import tornado.ioloop

import api
import api.platform

from tornado.log import access_log, app_log, gen_log
from tornado.options import define, options, parse_command_line
from common.logger import logger, loghd_info
from conf.config import DEBUG, multi_process_num

from tornado.web import StaticFileHandler


define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

# cookie_secret
# import base64
# import uuid
#
# base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)


def make_app():
    settings = {
        "debug": True if DEBUG else False,
        'autoreload': False,
        'static_path': os.path.join(os.path.dirname(__file__), "frontend"),
        "static_url_prefix": "/statics/",
        "cookie_secret": "gGhx6bgLRNOkJEwbIhDO0+apDZulwUxpnm4NchwjWTY=",
    }
    return tornado.web.Application([
        (r'/', IndexHandler),
        (r'/login', IndexHandler),

        # 平台消息路由
        (r'/api/v1/webhook/', api.platform.WebhookHandler),

        (r'/static/(.*)', StaticFileHandler,
         {"path": os.path.join(os.path.dirname(__file__), "frontend/static")})

    ], template_path=os.path.join(os.path.dirname(__file__), "frontend"), **settings)


# async def loop_task():
#     return


def enable_tornado_log():
    """开启 Tornado 内置日志信息
    * ``tornado.access``: Per-request logging for Tornado's HTTP servers (and
      potentially other servers in the future)
    * ``tornado.application``: Logging of errors from application code (i.e.
      uncaught exceptions from callbacks)
    * ``tornado.general``: General-purpose logging, including any errors
      or warnings from Tornado itself.
    """
    try:
        # access_log.addHandler(filehandler)
        access_log.addHandler(loghd_info)
        access_log.setLevel(logger.level)

        # app_log.addHandler(filehandler)
        app_log.addHandler(loghd_info)
        app_log.setLevel(logger.level)

        # gen_log.addHandler(filehandler)
        gen_log.addHandler(loghd_info)
        gen_log.setLevel(logger.level)
    except Exception:
        error_msg = traceback.format_exc()
        logger.warning(f'enable tornado log fail.\t{error_msg}')
        logger.error(f'enable tornado log fail.')


if __name__ == "__main__":
    parse_command_line()
    # port = sys.argv[1] if len(sys.argv) >= 2 else 8000
    port = options.port
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    enable_tornado_log()
    server.bind(port)
    server.start(multi_process_num)
    logger.info(f'listening on {port}')
    logger.info(f"DEBUG is: {'True' if DEBUG else 'False'}")
    # tornado.ioloop.IOLoop.current().spawn_callback(loop_task)
    tornado.ioloop.IOLoop.current().start()
