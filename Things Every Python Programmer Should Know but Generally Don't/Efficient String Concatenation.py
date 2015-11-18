#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'


def genstr(n):
    pass


# Bad
mystr = ""
for randstr in genstr(n):
    mystr += randstr

# Better
mystr = "".join([s for s in genstr(n)])
mystr = "".join(s for s in genstr(n))   # generator comprehension

# the next best
import io
sio = io.StringIO()

for randstr in genstr(n):
    sio.write(randstr)

mystr = sio.getvalue()


