#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'


# Bad
class A:
    a = []


b = A()
c = A()

b.a.append("blah")

# now b.a and c.a are both ["blah"]


def something(a=[]):
    a.append("blah")
    return a

# calling something without arguments 5 times will cause "blah" to show up
# 5 times in the returned list


# Better
class A:
    def __init__(self):
        self.a = []
        self.a.append("blah")


def something(a=None):
    if a is None:
        a = []
        a.append("blah")
