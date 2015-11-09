#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import sys
import os
import datetime
from redis import StrictRedis as Redis


def channel_daemon(channel):
    while True:
        members = r.smembers(channel) or []
        subscribers = map(lambda member: "{subscriber}.{channel}".format(subscriber=member, channel=channel), members)
        try:
            msg = r.blpop(subscribers, 10)
            if msg:
                print("subscriber: {}".format(msg[0]))
                print("channel: {}".format(channel))
                print("message: {}".format(msg[1]))
                print("\n")
        except Exception, e:
            print(e)


if __name__ == "__main__":
    r = Redis(host="localhost", port=6379, db=0)
    channel = sys.argv[1]
    print(channel)
    channel_daemon(channel)
