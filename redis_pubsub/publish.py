#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import sys
from redis import StrictRedis as Redis


def _publish(channel, msg):
    subscribers = r.smembers(channel) or []
    for subscriber in subscribers:
        r.rpush("{subscriber}.{channel}".format(channel=channel, subscriber=subscriber), msg)


if __name__ == "__main__":
    r = Redis(host="localhost", port=6379, db=0)
    _publish(sys.argv[1], sys.argv[2])
