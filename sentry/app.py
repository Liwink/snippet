#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options

from raven.contrib.tornado import AsyncSentryClient
from raven.contrib.tornado import SentryMixin

define("port", default=8888, help="Run server on a specific port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("Hello, world")

    def post(self, *args, **kwargs):
        print(self.request.body)


class UncaughtExceptionExampleHandler(SentryMixin, tornado.web.RequestHandler):
    def get(self):
        1 / 0


class AsyncMessageHandler(SentryMixin, tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, *args, **kwargs):
        self.write("You requested the main page served")
        yield tornado.gen.Task(
            self.captureMessage, "Request for main page served"
        )
        self.finish()


class AsyncExceptionHandler(SentryMixin, tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        try:
            raise ValueError()
        except Exception as e:
            response = yield tornado.gen.Task(
                self.captureException, exc_info=True
            )
        self.finish()


class SyncMessageHandler(SentryMixin, tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("SyncMessage")
        self.captureMessage("SyncRequest")

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/exception/?", UncaughtExceptionExampleHandler),
    (r"/async/message/?", AsyncMessageHandler),
    (r"/async/exception/?", AsyncExceptionHandler),
    (r"/sync/message/?", SyncMessageHandler),
])

application.sentry_client = AsyncSentryClient(
    # 'https://2afcb6260e8e435c90e6a9b6154ae1f9:b83dfe5eecbc47a69ba195a111887bc0@app.getsentry.com/58758',
    "http://b02bea74a19f401aaf49eb4b0b6a56b1:8c23c49fdac24364a68eeb0c7068a5f0@localhost:9000/1",

)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print options.port
    tornado.ioloop.IOLoop.instance().start()
