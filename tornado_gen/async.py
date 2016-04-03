#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import tornado.gen
import tornado.httpserver
import tornado.concurrent
import tornado.web

import time

from tornado.options import define, options

define("port", default=8888, help="run on the give port", type=int)


class SleepHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.task()
        self.write("when i sleep 5s")

    @tornado.concurrent.return_future
    def task(self, callback=None):
        print("1" * 8)
        # yield tornado.gen.Task(print, 5)
        time.sleep(0.5)
        callback(None)
        print("2" * 8)



class JustNowHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("i hope just now see you")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/sleep", SleepHandler),
        (r"/justnow", JustNowHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
