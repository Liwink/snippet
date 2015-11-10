#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

from redis import Redis
from rq import Queue

from task import print_job

import sys


def queue():
    q = Queue(connection=Redis())
    return q


def enqueue(job, value):
    q = queue()
    q.enqueue(job, value)


if __name__ == "__main__":
    enqueue(print_job, sys.argv[1])
