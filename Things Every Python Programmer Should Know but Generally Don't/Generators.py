#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'


def generator():
    yield "one"
    yield "two"
    yield "three"


for num in generator():
    print num

gen = generator()
next(gen)  # "one"
next(gen)  # "two"
next(gen)  # "three"
next(gen)  # Throws "StopIteration" exception


########


def generator():
    x = 0
    while True:
        x = yield + 1


gen = generator()
next(gen)  # yields 1
gen.send(3)  # yields 4

# This allows the generator rto function as a coroutine.


########

f = open("something.txt")
for line in f:
    # dosomething(line)
    pass

    # This program will read a file in line bu line and do something to each line.
    # can function in constant memory no matter the size of the file.
f.close()
# free up nay system resources