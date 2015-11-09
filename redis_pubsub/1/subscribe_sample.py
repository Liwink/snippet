#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import sys
import os
import datetime
from redis import StrictRedis as Redis

subscriber = 'first_subscriber'


def _subscribe(channel):
    while True:
        try:
            msg = r.blpop(channel)
        except Exception, e:
            msg = e
        if msg:
            print("channel: {} \nmessage: {}".format(channel, msg[1]))


def _fork_and_subscribe(channel):
    r.sadd(channel, subscriber)

    child_pid = os.fork()
    if not child_pid:
        try:
            print("Processing work since {}".format(datetime.datetime.utcnow()))
            _subscribe("{channel}:{subscriber}".format(channel=channel, subscriber=subscriber))
        except Exception, e:
            print(e)
            sys.exit(1)
        sys.exit(0)
    else:
        print("Forked {} at {}".format(child_pid, datetime.datetime.utcnow()))
        # os.waitpid(child_pid, 0)


if __name__ == "__main__":
    r = Redis(host="localhost", port=6379, db=0)
    subscriber = sys.argv[1]
    print(sys.argv[2:])
    for channel in sys.argv[2:]:
        print(channel)
        _fork_and_subscribe(channel)
