#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'


def handler1(message):
    if 0 < message < 10:
        print("request {message} handled in handler 1".format(message=message))
    else:
        return message


def handler2(message):
    if 10 <= message < 20:
        print("request {message} handled in handler 2".format(message=message))
    else:
        return message


def handler3(message):
    if 20 <= message < 30:
        print("request {message} handled in handler 3".format(message=message))
    else:
        return message


def centre(messages):
    for message in messages:
        handler3(handler2(handler1(message)))


if __name__ == "__main__":
    requests = [2, 5, 25, 14, 23]

    centre(requests)


# ### OUTPUT ###
# request 2 handled in handler 1
# request 5 handled in handler 1
# request 25 handled in handler 3
# request 14 handled in handler 2
# request 13 handled in handler 3
