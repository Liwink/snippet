#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import sys
import os
import datetime
from redis import StrictRedis as Redis


if __name__ == "__main__":
    r = Redis(host="localhost", port=6379, db=0)
    subscriber = sys.argv[1]
    channel = sys.argv[2]
    r.srem(channel, subscriber)
    print("{subscriber} subscribe {channel}".format(subscriber=subscriber, channel=channel))
    print(r.smembers(channel))
