#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

"""
Most asynchronous functions in Tornado return a Future; yielding this object returns its result.

http://stackoverflow.com/questions/27043076/tornado-coroutine

The `tornado.coroutine` decorator requires that you yield only `Future`
objects or certain containers containing `Future` objects.
When you call `yield something()`, `something` must either be a coroutine,
or return a `Future`.
"""

from tornado.gen import Return, Future
from tornado.web import RequestHandler
from tornado import gen


class HelloHandler(RequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        x = yield self.do_test()
        self.render("hello.html")

    @gen.coroutine
    def do_test(self):
        raise Return("test")

class AnotherHelloHandler(RequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        x = yield self.do_test()
        self.render("hello.html")

    def do_test(self):
        future = Future()
        future.set_result("test")
        return future
