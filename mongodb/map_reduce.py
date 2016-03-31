#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import db

"""

https://docs.mongodb.org/manual/core/map-reduce/

"""

total_score = db.training_trainings.map_reduce(map="function() {emit(this.status, this.total_score)}",
                                               reduce="function(key, values){ return Array.sum( values ) }",
                                               out="reduce",
                                               query={
                                                   "project_id": {"$in": ['sample_id']},
                                                   "status": 1,
                                               },
                                               ).one().get("value")

"""
function() {emit(this.status, this.total_score)}
return {key: value}

[
    {"status": 1, "total_score": 3}
    {"status": 1, "total_score": 6}
    {"status": 0, "total_score": 9}
]

->

[
    {"status": 1, "total_score": [3, 6]}
    {"status": 0, "total_score": [9]}
]

"""

# query
# one

