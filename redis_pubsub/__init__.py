#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import sys
from redis import StrictRedis as Redis


def _subscribe(channel):
    r = Redis(host="localhost", port=6379, db=0)

    while True:
        try:
            msg = r.rpop(channel)
        except Exception, e:
            msg = e
        if msg:
            print("channel: {} \nmessage: {}".format(channel, msg))


if __name__ == "__main__":
    print(sys.argv[1:])
    for channel in sys.argv[1:]:
        print(channel)
        _subscribe(channel)
