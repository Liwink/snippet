#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import functools
import sys
import types

from tornado.gen import Future
from tornado.ioloop import IOLoop
from tornado.gen import Return


def coroutine(func, replace_callback=True):
    return _make_coroutine_wrapper(func, replace_callback=True)


def _make_coroutine_wrapper(func, replace_callback):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        future = Future()

        # try:
        #     result = func(*args, **kwargs)
        # except (Return, StopIteration) as e:
        #     result = getattr(e, "value", None)
        # except Exception:
        #     future.set_exc_info(sys.exc_info())
        #     return future
        # else:
        #     if isinstance(result, types.GeneratorType):
        #         try except else
        #         yielded = next(result)
        #         Runner(result, future, yielded)
        #         return future

        result = func(*args, **kwargs)
        yielded = next(result)
        Runner(result, future, yielded)
        future.set_result(result)
        return future

    return wrapper


moment = Future()
_null_future = Future()


class Runner(object):
    def __init__(self, gen, result_future, first_yielded):
        self.gen = gen
        self.result_future = result_future

        self.future = _null_future
        self.io_loop = IOLoop.current()

        self.running = False
        self.finished = False

        if self.handle_yield(first_yielded):
            self.run()

    def handle_yield(self, yielded):
        self.future = yielded

        # wait and not block
        if not self.future.done() or self.future is moment:
            self.io_loop.add_future(
                self.future, lambda f: self.run()
            )
            return False
        return True

    def run(self):
        if self.running or self.finished:
            return
        self.running = True

        while True:
            future = self.future

            # Only deal with finished job
            if not future.done():
                return
            self.future = None

            value = future.result()

            # Task done and send result to main 'process'
            yielded = self.gen.send(value)

            if not self.handle_yield(yielded):
                return
