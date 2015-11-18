#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EventDocument 中添加 `role` 字段
"""
__author__ = 'Liwink'

import traceback

from base import conn, print_summary
import time


# def upgrade():
#     """
#     修改本系统 EventDocument 中的数据
#     添加 role 字段，表示记录事件的统计员是主力还是替补
#     :return:
#     """
#
#     events = conn.EventDocument.find()
#
#     error_events = []
#
#     for event in events:
#         statistician_match = conn.StatisticianMatchesDocument.find_one({
#             "team_id": event.get("team_id"),
#             "match_id": event.get("match_id"),
#             "statistician_id": event.get("statistician_id")
#         })
#         if not statistician_match:
#             error_events.append(event)
#             continue
#         event["role"] = statistician_match.get("role")
#         event.save()


def upgrade():
    """
    修改本系统 EventDocument 中的数据
    添加 role 字段，表示记录事件的统计员是主力还是替补
    :return:
    """
    total = 0
    fails = []
    for event in conn.EventDocument.find():
        total += 1
        try:
            __upgrade_event(event)
        except:
            fails.append(event)
            print event
            print traceback.format_exc()
    print_summary(__file__, total, fails)


def __upgrade_event(event):
    """
    event 字段 role
    :param doc:
    :return:
    """
    role = __get_statistician_role(event)
    event["role"] = role
    event.save()


def __get_statistician_role(event):
    """
    获取统计员
    """
    statistician_match = conn.StatisticianMatchesDocument.find_one({
        "team_id": event.get("team_id"),
        "match_id": event.get("match_id"),
        "statistician_id": event.get("statistician_id")
    })
    return statistician_match.get("role")


def upgrade_by_stat():
    total = 0
    fails = []
    for statistician in conn.StatisticianMatchesDocument.find():
        total += 1
        try:
            for event in conn.EventDocument.find({
                "statistician_id": statistician.get("statistician_id"),
                "match_id": statistician.get("match_id"),
                "team_id": statistician.get("team_id"),
            }):
                event['role'] = statistician.get("role")
                event.save()
        except:
            fails.append(statistician)
            print statistician
            print traceback.format_exc()
    print_summary(__file__, total, fails)


if __name__ == '__main__':
    # time1 = time.time()
    # 50737 条数据，本地跑 89s，189 failed
    upgrade()
    # 50737 条数据，本地跑 59s
    # upgrade_by_stat()
    # time2 = time.time()
    # print ("Time Duration:", time2 - time1)
