#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Dylan'


import datetime
import logging
import traceback
import copy
from bson import ObjectId
import tornado.web
import tornado.gen
import validators


logger = logging.getLogger(__name__)


class SearchMixin(tornado.web.RequestHandler):

    """
    SearchMixin

    document = None
    search_fields = []
    """

    @property
    def sort(self):
        """
        排序参数
                /the/url/?sort=field1:desc,field2:asc
        :return:
        """
        orders = {
            'desc': -1,
            'asc': 1,
        }
        result, default = [], [('_id', -1)]
        arg = self.get_argument('sort', '').strip()
        if not arg:
            return result
        for item in arg.split(','):
            splits = item.split(':', 1)
            if len(splits) == 1:
                continue
            result.append((splits[0], orders.get(splits[1], -1)))
        return result or default

    @property
    def query(self):
        """
        查询条件
             /the/url/?q=query
                - q=keyword
                - q=field:keyword
                - q=field1:keyword AND field2:keyword
                - q=field1:keyword OR field2:keyword
        :return:
        """
        result = {}
        arg = self.get_argument('q', '').strip()
        if not arg:
            return result
        q = self.parse_query_conditions(arg)
        result.update(q)
        return result

    def parse_query_conditions(self, query):
        """
        解析查询条件
        :param query:
        :return:
        """
        result = {}
        conditions = {
            'AND': '$and',
            'OR': '$or',
        }
        conds = []
        separator, splits = 'AND', query.split(' AND ')
        if len(splits) == 1:
            separator, splits = 'OR', query.split(' OR ')
        for item in splits:
            splits = item.split(':', 1)
            # field:keyword
            try:
                if len(splits) == 1:
                    for f in self.search_fields:
                        try:
                            c = self.parse_query_conditions_for(f, splits[0])
                            if c:
                                conds.append(c)
                        except:
                            print traceback.format_exc()
                elif len(splits) == 2:
                    c = self.parse_query_conditions_for(splits[0], splits[1])
                    if c:
                        conds.append(c)
            except:
                print traceback.format_exc()
        if len(conds) > 1:
            result = {
                conditions.get(separator) or '$or': conds,
            }
        elif len(conds) == 1:
            result = conds[0]
        return result

    def parse_query_conditions_for(self, field, value):
        """
        解析查询条件 - 具体的字段
            - 优先通过 parse_query_conditions_for_{field} 解析
            - 处理默认的枚举类型字段：直接使用 k:v
            - 其他字符串使用正则表示匹配
            - 数值类型则自动转换
        :param field:
        :param value:
        :return:
        """
        func = getattr(self, 'parse_query_conditions_for_%s' % field, None)
        if func and callable(func):
            return func(value)

        from pylibs.models import conn
        result = {
            field: value,
        }
        field_type = conn[self.document].structure.get(field)
        if field in ['status', 'role', 'type']:
            result = {
                field: int(value) if field_type in [int] else value,
            }
        elif field_type in [basestring, unicode, str]:
            result = {
                field: {
                    '$regex': value,
                },
            }
        elif field_type in [int, float, ObjectId]:
            result = {
                field: field_type(value),
            }
        return result

    def parse_query_conditions_for_stats_mode(self, stats_mode):
        """
        :return:
        """
        result = {}
        try:
            result['stats_mode'] = int(stats_mode)
        except:
            pass
        return result

    def parse_query_conditions_for_name(self, value):
        """
        名字搜索
        :param value:
        :return:
        """
        return {'name': {'$regex': value}}

    def parse_query_conditions_for_op_id(self, value):
        """
        op_id搜索
        :param value:
        :return:
        """
        try:
            value = int(value)
            return {'op_id': value}
        except:
            return {}

    def parse_query_conditions_for_phone(self, value):
        """
        电话搜索
        :param value:
        :return:
        """
        try:
            int(value)
            return {'phone': {'$regex': value}}
        except:
            return {}

    def parse_query_conditions_for_start_at(self, value):
        """
        start_at 1天之内
        :param value:
        :return:
        """
        now = self.to_datetime(value)
        if not value:
            return {}
        s, e = now, now + datetime.timedelta(days=1)
        return {'$and': [{'start_at': {'$gte': s}}, {'start_at': {'$lt': e}}]}

    def parse_query_conditions_for_end_at(self, value):
        """
        end_at 1天之类
        :param value:
        :return:
        """
        now = self.to_datetime(value)
        if not value:
            return {}
        s, e = now, now + datetime.timedelta(days=1)
        return {'$and': [{'end_at': {'$gte': s}}, {'end_at': {'$lt': e}}]}

    def parse_query_conditions_for_type(self, value):
        """
        end_at 1天之类
        :param value:
        :return:
        """
        try:
            value = int(value)
            return {'type': value}
        except:
            return {}

    def parse_query_conditions_for_statistician_id(self, value):
        """
        statistician_id
        :param value:
        :return:
        """
        try:
            value = ObjectId(value)
            return {'statistician_id': value}
        except:
            return {}

    def to_datetime(self, value, fmt=None):
        """
        转换为 datetime
            - 若 fmt 为 日期 + 时间, 则 value 必须为 utc 格式
            - 若 fmt 为 日期, 则 value 为本地时间,服务端自行转换为 utc 格式
        :param value:
        :param fmt:
        :return:
        """
        fmt = fmt or validators.date_fmt
        if not value:
            return None
        try:
            value = datetime.datetime.strptime(value, fmt)
            if fmt == validators.date_fmt:
                value -= datetime.timedelta(hours=8)
            return value
        except:
            pass
