#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

from mongokit import Document
from mongokit import ObjectId

from settings import config
from ..database import MongoKitHolder

import datetime

conn = MongoKitHolder(**config.mongo_openplay)


class BaseDocument(Document):
    __database__ = config.mongodb_openplay.db

    structure = {
        "_id": ObjectId,
        "created_at": datetime.datetime,
        "updated_at": datetime.datetime,
        "created_by": ObjectId,
        "updated_by": ObjectId,
    }

    # 字段描述
    fields_descriptions = {
        "created_at": u"创建时间",
        "updated_at": u"更新时间",
    }

    default_values = {
        "_id": ObjectId,
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow(),
    }
