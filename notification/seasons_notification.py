#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

from ..base import BaseHandler
import validators
import tornado.web
from pylibs.decorators import request_body_validate
from pylibs.decorators import resource_check
from pylibs.decorators import need_permission
from pylibs.decorators import token_required
from pylibs.models import conn
from pylibs.constants import lookup
from pylibs.constants import message_code

from settings import config

from bson import ObjectId

Logo_uri_prefix = config.qiniu.host + "/notification/"


class SeasonNotificationHandler(BaseHandler):
    """
    获取组织者的所有赛事列表
    """

    @property
    def current_competition_id(self):
        """
        当前用户操作的competition_id
        """
        season = conn.SeasonDocument.find_by_id(self.path_kwargs.get('season_id') or self.path_args[0])
        return season.get("competition_id")

    @token_required
    @request_body_validate(validators.season_notification_schema)
    @resource_check(conn.SeasonDocument)
    @need_permission("notify", "team")
    def post(self, season_id):
        season = self.resource[0]
        competition = conn.CompetitionDocument.find_by_id(season.get("competition_id"))

        for team_id in self.body.get("teams"):
            team_season = conn.TeamSeasonDocument.find_one({
                "team_id": ObjectId(team_id),
                "season_id": season.get("_id")
            })
            if not team_season:
                result = message_code.ResourceNotExist(message=u"请确认所选球队已加入联赛")
                self.write(result)
                return

        post = conn.PostDocument.add({
            "user_id": ObjectId(self.user_id),
            "delegation_id": ObjectId(season_id),
            "delegation_type": lookup.ObjectType.SEASON,
            "type": lookup.PostType.ANNOUNCEMENT,
            "body": self.body.get("notification_body"),
        })

        title = u"收到[competition({0}){1}]组织者的消息"

        # 向领队发送通知
        # FIXME: 这里NotificationType 是SEASON?
        for team_id in self.body.get("teams"):
            # team_id = ObjectId(team.get("id"))
            team_managers = conn.TeamPlayerDocument.find({
                "team_id": team_id,
                "roles": lookup.PlayerRole.TEAM_MANAGER
            })
            for team_manager in team_managers:
                conn.NotificationDocument.add({
                    "sender_id": ObjectId(self.user_id),
                    "delegation_type": lookup.ObjectType.SEASON,
                    "delegation_id": ObjectId(season_id),
                    "object_id": post.get("_id"),
                    "object_type": lookup.ObjectType.POST,
                    "verb": lookup.NotificationVerbType.ORGANIZER_NOTIFY_TEAM,
                    "type": lookup.NotificationType.SEASON,
                    "title": title.format(str(competition.get("_id")), competition.get("name")),
                    "user_id": team_manager.get("player_id"),
                    "logo_uri": Logo_uri_prefix + "Notification_Competition_Message@3x.png"
                })

        self.write(post.to_dict_with_ref_docs(include_fields=('body', 'created_at')))

    @token_required
    @resource_check(conn.SeasonDocument)
    @need_permission("notify", "team")
    def get(self, season_id):
        result = conn.PostDocument.find_posts_by_season_id(season_id,
                                                           limit=self.limit,
                                                           last_id=self.last_id)
        self.write(result)
