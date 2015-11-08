#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

from pymongo import MongoClient

from mongokit import Connection


class MongoSimpleHolder(MongoClient):
    """
    MangoDB holder
    """
    def __init__(self, **kwargs):
        kwargs = kwargs or {
            "host": "localhost",
            "port": 27017
        }
        kwargs = kwargs.copy()
        for k in kwargs.keys():
            if k not in ("host", "port"):
                kwargs.pop(k)
        super(MongoSimpleHolder, self).__init__(**kwargs)

    def auth(self, database, username, password):
        self[database].authenticate(username, password)
        return self[database]


class MongoKitHolder(Connection):
    """
    MongoKit
    """

    def __init__(self, **kwargs):

        # 配置 MongoDB 地址
        kwargs = kwargs or {
            "host": "localhost",
            "port": 27017
        }

        # 这里使用的是 copy，不改变传入参数的原始值
        kwargs = kwargs.copy()
        for k in kwargs.keys():
            if k not in ("host", "port"):
                kwargs.pop(k)
        super(MongoKitHolder, self).__init__(**kwargs)

    def auth(self, database, username, password):
        self[database].authenticate(username, password)
        return self
