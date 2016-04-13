#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'


class Future(object):
    """
    Placeholder for an asynchronous result.

    A `Future` encapsulates the result of an asynchronous
    operation. In synchronous applications `Futures` are used
    to wait dor the result from a thread or process pool; in
    Tornado they normally used with `.IOLoop.add_future` or by
    yielding them in a `.gen.coroutine`.
    """

    def __init__(self):
        self._done = False
        self._result = None
        self._exc_info = None
        self._callbacks = []

    def set_result(self, result):
        self._result = result
        self._set_done()

    def _set_done(self):
        self._done = True
        for cd in self._callbacks:
            cd(self)
        self._callbacks = None
