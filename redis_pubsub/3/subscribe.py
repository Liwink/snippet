#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import sys
import os
import datetime
from redis import StrictRedis as Redis


def print_data(value, *args):
    print('work: '+value+'\n')


def subscribe(channel, work, subscriber):
    """
    一种和 redis pubsub listen() 更相似的结构
    :param channel:
    :param work:
    :param subscriber:
    :return:
    """
    r.sadd(channel, subscriber)
    for item in daemon(channel, subscriber):
        work(item)


def daemon(channel, subscriber):
    while True:
        try:
            msg = r.blpop("{subscriber}.{channel}".format(subscriber=subscriber, channel=channel), 10)
            if msg:
                print("subscriber: {}".format(msg[0]))
                print("channel: {}".format(channel))
                print("message: {}".format(msg[1]))
                yield msg[1]
        except Exception, e:
            print(e)


if __name__ == "__main__":
    r = Redis(host="localhost", port=6379, db=0)
    s = sys.argv[1]
    c = sys.argv[2]
    print("{subscriber} subscribe {channel}".format(subscriber=s, channel=c))
    print(r.smembers(c))
    subscribe(c, print_data, s)
