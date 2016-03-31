#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

"""
Coroutines are tasks

Tasks have a few essential features
* Independent control flow
* Internal state
* Can be scheduled (suspended/resumed)
* Can communicate with other tasks
"""


def grep(pattern):
    # internal state: pattern
    print("Looking for ", pattern)
    while True:
        # yield: suspended
        line = yield
        if pattern in line:
            print(line)


"""
Multitasking using nothing but coroutines?
"""
