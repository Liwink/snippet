#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import sys
import os
import time
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


def _fork_and_subscribe(channel):
    child_pid = os.fork()
    if not child_pid:
        try:
            print("Processing work since {}".format(time.time()))
            _subscribe(channel)
        except Exception, e:
            print(e)
            # TODO: 参数的意义？
            sys.exit(1)
        sys.exit(0)
    else:
        print("Forked {} at {}".format(child_pid, time.time()))
        # TODO: 这是干嘛
        # os.waitpid(child_pid, 0)

if __name__ == "__main__":
    print(sys.argv[1:])
    for channel in sys.argv[1:]:
        print(channel)
        _fork_and_subscribe(channel)
