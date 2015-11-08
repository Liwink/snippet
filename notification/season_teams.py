#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

from ..base import BaseHandler
import validators
from settings import config
from bson import ObjectId
import tornado.web

from pylibs.decorators import token_required
from pylibs.decorators import request_body_validate
from pylibs.decorators import resource_check
from pylibs.decorators import need_permission
from pylibs.models import conn
from pylibs.pubsub import publish
from pylibs.services import sms
from pylibs.constants import lookup

import validators


class SeasonTeamsHandler(BaseHandler):
    """
    获取组织者的所有赛事列表
    """

    @token_required
    @resource_check(conn.SeasonDocument)
    def get(self, season_id):
        # TODO: 权限？
        season = self.resource[0]
        criteria = {
            'season_id': season.get("_id")
        }
        kwargs = {
            'include_fields': ('team', 'status'),
            "team_include_fields": ['name', 'logo_uri', 'team_players_number',
                                    'area', 'op_id', 'short_name', 'status'],
        }
        teams = conn.TeamSeasonDocument.find_by_page_with_builtin_pagination(criteria, **kwargs)

        result = teams
        self.write(result)

    @token_required
    @request_body_validate(validators.invitation_team_manager)
    @resource_check(conn.SeasonDocument)
    @need_permission('invite', 'team_manager')
    def post(self, season_id):
        """
        赛季添加球队
        - 确认用户信息
        - 确认关联球队信息
        - 确认邀请信息
        - 发送短信
        :param season_id:
        :return:
        """
        season = self.resource[0]
        competition = conn.CompetitionDocument.find_by_id(season.get("competition_id")) or {}

        # 获取用户信息
        account = self.get_receiver(self.body.get("phone"),
                                    self.body.get("country_code"),
                                    self.body.get("receiver_id"),
                                    name=self.body.get("name"))

        # 获取球队信息
        team = self.get_team_by_player_id(account.get("_id"),
                                          account.get("status"),
                                          name=self.body.get("team_name"), )

        # 建立球队关系
        team_season = self.get_team_season(team.get("_id"), season_id)

        # 获取邀请码
        criteria = {
            "type": lookup.InvitationCodeType.TEAM_MANAGER,
            "creator_id": ObjectId(self.user_id),
            "receiver_id": account.get("_id"),
            "team_id": team.get("_id"),
            "season_id": season.get("_id"),
            "competition_id": season.get("competition_id"),
        }
        invitation = self.get_invitation(criteria)

        # TODO: 用户在什么状态下发送邀请短信？ 发送站内通知？
        msg = (account.get("country_code"), account.get("phone"),
               invitation['code'], invitation['type'], competition.get('name'))
        sms.send_invitation_code([msg])

        publish("team.invite", invitation)

        # 返回客户端信息
        kwargs = {}
        kwargs['include_fields'] = ('team', 'status')
        kwargs['team_include_fields'] = kwargs.pop('team_include_fields', None) or \
                                        ['name', 'logo_uri', 'team_players_number',
                                         'area', 'op_id', 'short_name', 'status']
        result = team_season.to_dict_with_ref_docs(**kwargs)
        if config.env not in ['product']:
            result['code'] = invitation.get("code")

        self.write(result)
