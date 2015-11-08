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


logger = logging.getLogger(__name__)


class AdapterMixin(tornado.web.RequestHandler):
    """
    Adapter的Mixin
    """
    # 实体名
    entity = None

    # 默认的搜索字段列表
    search_fields = []

    # 全局的查询约束，适用于 get/put/delete
    all_restriction = {}
    
    # get 的查询约束
    get_restriction = {}
    
    # put 的查询约束
    put_restriction = {}
    
    # delete 的查询约束
    delete_restriction = {}

    # get 时包含/排除的字段列表
    get_include_fields = {}
    get_exclude_fields = {'created_by', 'updated_by', '_id'}

    # put 时包含/排除的字段列表
    put_include_fields = {}
    put_exclude_fields = {'created_at', 'updated_at', 'created_by', 'updated_by', '_id', 'op_id'}
    put_mapping_fields = {}

    # post 时包含/排除的字段列表
    post_include_fields = {}
    post_exclude_fields = {'created_at', 'updated_at', 'created_by', 'updated_by', '_id', 'op_id'}
    post_mapping_fields = {}

    filter_exclude_fields = {'created_at', 'updated_at', 'created_by', 'updated_by', '_id', 'op_id'}

    # entity 包含的字段列表
    # 账户、用户、球员、统计员、赛事组织者
    account_include_fields = {
        'country_code',
        'phone',
        'op_id',
        'email',
        'passport',
        'account_roles',
        'status',
        'id_card',
        'profile',
    }

    profile_include_fields = {
        'area',
        'avatar_uri',
        'birth',
        'created_at',
        'description',
        'gender',
        'height',
        'name',
        'nationality',
        'weight',
        'roles',
    }

    user_include_fields = (
        '_id',
        'op_id',
        'country_code',
        'id_card',
        'passport',
        'email',
        'phone',
        'created_at',
        'profile',
        'area',
        'avatar_uri',
        'birth',
        'description',
        'gender',
        'height',
        'name',
        'nationality',
        'account_roles',
        'roles',
        'weight',
        'status',
    )

    player_include_fields = {
        'player',
    }

    statistician_include_fields = {
        'statistician',
    }

    organizer_include_fields = {
        'organizer',
    }

    statistician_match_include_fields = {
        'competition',
        'match',
        'team_id',
        'role',
        'status',
        'description',
    }

    competition_include_fields = {
        'area',
        'description',
        'logo_uri',
        'name',
        'official_url',
        'organization',
        'short_name',
        'status',
        'op_id',
    }

    season_include_fields = {
        'competition',
        'end_at',
        'match_format',
        'match_type',
        'name',
        'area',
        'rule_extra_time',
        'rule_half_time',
        'rule_stopped_watch',
        'rule_round_robin',
        'rule_qualify_count',
        'rule_group_count',
        'start_at',
        'stats_mode',
        'status',
        'team_count',
        'year',
        'schedule_status',
    }

    round_include_fields = {
        'name',
    }

    group_include_fields = {
        'name',
    }

    match_include_fields = {
        'competition',
        'end_at',
        'fs_a',
        'fs_b',
        'group',
        'hs_a',
        'hs_b',
        's_a',
        's_b',
        'match_period',
        'match_type',
        'op_id',
        'referee',
        'referee_assist',
        'referee_fourth',
        'statisticians',
        'group',
        'round',
        'season',
        'start_at',
        'stats_mode',
        'status',
        'team_a',
        'team_b',
        'venue',
        'weather',
        'match_title',
        'rule_extra_time',
        'rule_half_time',
        'rule_stopped_watch',
    }

    team_include_fields = {
        'area',
        'logo_uri',
        'name',
        'op_id',
        'short_name',
        "team_players_number",
        "status",
    }

    team_player_include_fields = {
        "status",
        "player",
        "shirt_number",
        "roles",
    }

    venue_include_fields = {
        'address',
        'area',
        'capacity',
        'latitude',
        'longitude',
        'name',
        "type",
    }

    event_include_fields = {
        'code',
        'name',
        'event_key',
        'match',
        'player',
        'statistician',
        'status',
        'team',
        'value',
    }

    # Ref entity 包含的字段列表
    ref_competition_include_fields = ('name', "logo_uri", 'op_id')
    ref_season_include_fields = ('name',)
    ref_round_include_fields = ('name',)
    ref_group_include_fields = ('name',)
    ref_match_include_fields = ('team_a', 'team_b', 's_a', 's_b', 'status', 'start_at', 'end_at', 'op_id')
    ref_team_include_fields = ('name', 'logo_uri', 'status', 'op_id')
    ref_team_a_include_fields = ('name', 'logo_uri', 'status', 'op_id')
    ref_team_b_include_fields = ('name', 'logo_uri', 'status', 'op_id')
    ref_player_include_fields = ('name', 'avatar_uri', 'phone', 'country_code', 'status', 'op_id')
    ref_statistician_include_fields = ('name', 'avatar_uri', 'phone', 'country_code', 'status', 'op_id')
    ref_organizer_include_fields = ('name', 'avatar_uri', 'phone', 'country_code', 'status', 'op_id')
    ref_venue_include_fields = ('name', 'address', 'longitude', 'latitude', 'type', 'status')

    @property
    def criteria(self):
        """
        针对MongoDB的查询
        :return:
        """
        result = {}
        result.update(self.all_restriction)
        result.update(self.get_restriction)
        q = self.query
        result.update(q)
        return result

    @property
    def get_criteria(self):
        return self.criteria

    @property
    def put_criteria(self):
        """
        更新资源时的查询条件
        :return:
        """
        result = {}
        result.update(self.all_restriction)
        result.update(self.put_restriction)
        return result

    @property
    def delete_criteria(self):
        """
        删除资源时的查询条件
        :return:
        """
        result = {}
        result.update(self.all_restriction)
        result.update(self.delete_restriction)
        return result

    @property
    def include_fields(self):
        """
        展示的字段列表
        :return:
        """
        fields = set(getattr(self, '%s_include_fields' % (self.entity, ), None) or [])
        fields.update(set(self.get_include_fields))
        fields -= set(self.get_exclude_fields)
        return fields

    @property
    def updatable_fields(self):
        """
        允许更新的字段列表
        :return:
        """
        fields = set(self.put_include_fields) - set(self.put_exclude_fields)
        return fields

    @property
    def addable_fields(self):
        """
        新增资源时允许的字段列表
        :return:
        """
        fields = set(self.post_include_fields) - set(self.post_exclude_fields)
        return fields

    @property
    def ref_include_fields_kwargs(self):
        """
        Ref include fields
        :return:
        """
        result = {}

        mapping = {
            'get': self.include_fields,
            'put': self.updatable_fields,
            'post': self.addable_fields,
        }
        method = self.request.method.lower()
        fields = mapping.get(method) or self.include_fields
        self.parse_ref_include_fields_kwargs(result, fields)
        return result

    def parse_ref_include_fields_kwargs(self, result, fields):
        """
        Ref include fields
            - fields
            - nested-fields in fields
        :return:
        """
        for field in fields:
            ref_fields = getattr(self, 'ref_%s_include_fields' % field, None)
            if not ref_fields:
                continue
            result.update({
                '%s_include_fields' % field: ref_fields,
            })
            self.parse_ref_include_fields_kwargs(result, ref_fields)

    def filter_doc(self, doc, include_fields=None, exclude_fields=None):
        """
        过滤doc
        :param doc:
        :param include_fields:
        :return:
        """
        doc = copy.deepcopy(doc)
        fields = set(include_fields or set(doc.keys()))
        fields -= set(exclude_fields or ())
        fields -= set(self.filter_exclude_fields or ())
        for k in doc.keys():
            v = doc[k]
            if k not in fields:
                doc.pop(k)
            elif k.endswith('_id') and v:
                doc[k] = self.convert_to_object_id(v)
            elif isinstance(v, dict):
                if v.get('id'):
                    doc['%s_id' % k] = self.convert_to_object_id(v['id'])
            elif k in ('start_at', 'end_at', 'client_started_at', 'client_ended_at', 'birth') \
                    and v \
                    and not isinstance(v, datetime.datetime):
                    doc[k] = self.convert_to_datetime(doc[k])
        self.mapping_doc_fields(doc)
        return doc

    def mapping_doc_fields(self, doc):
        """
        字段名字转换
        :param doc:
        :return:
        """
        method = self.request.method.lower()
        mapping = getattr(self, '%s_mapping_fields' % method, None)
        if not mapping:
            return
        for field, to_field in mapping.iteritems():
            if doc.get(field) is not None:
                doc[to_field] = doc.pop(field)
        return

    def convert_to_object_id(self, value):
        """
        :param value:
        :return:
        """
        return ObjectId(value) if value else None

    def convert_to_datetime(self, value):
        """
        :param value:
        :return:
        """
        datetime_fmt = '%Y-%m-%d %H:%M:%S'
        if value and not isinstance(value, datetime.datetime):
                return datetime.datetime.strptime(value, datetime_fmt)
        return value
