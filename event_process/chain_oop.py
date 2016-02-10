#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'


class Handler(object):
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, message):
        self._handle(message)
        if hasattr(self._successor, 'handle'):
            self._successor.handle(message)

    def _handle(self, message):
        print("Error, to specify your _handler")
        return False


class Handler1(Handler):
    def _handle(self, message):
        if 0 < message < 10:
            print("request {message} handled in handler 1".format(message=message))
            return True
        return False


class Handler2(Handler):
    def _handle(self, message):
        if 10 <= message < 20:
            print("request {message} handled in handler 2".format(message=message))
            return True
        return False


class Handler3(Handler):
    def _handle(self, message):
        if 20 <= message < 30:
            print("request {message} handled in handler 3".format(message=message))
            return True
        return False


class Centre(object):
    def __init__(self, handler):
        self.handler = handler

    def delegate(self, requests):
        for request in requests:
            self.handler.handle(request)


if __name__ == "__main__":
    requests = [2, 5, 25, 14, 23]

    centre = Centre(Handler3(Handler2(Handler1())))
    centre.delegate(requests)


# ### OUTPUT ###
# request 2 handled in handler 1
# request 5 handled in handler 1
# request 25 handled in handler 3
# request 14 handled in handler 2
# request 13 handled in handler 3
