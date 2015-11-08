#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import settings
from handlers import UserBaseInfoHandler
from handlers import StatisticianSubmissionHandler
from handlers import OrganizerInvitationHandler
from handlers import OrganizerInvitationCheckPhoneHandler
from handlers import OrganizerInvitationWithAccountHandler
from handlers import OrganizerInvitationsHandler
from handlers import OrganizerRemoveInvitation
from handlers import OrganizerInvitationVerifyHandler
from handlers import OrganizerInvitationActivateAccountHandler
from handlers import OrganizerInvitationConfirmHandler
from handlers import OrganizerInvitationsRejectHandler
from handlers import OrganizersHandler
from handlers import OrganizerHandler
from handlers import SeasonListHandler
from handlers import SeasonInfoHandler
from handlers import SeasonTeamsHandler
from handlers import SeasonApprovalHandler
from handlers import SeasonNotificationHandler
from handlers import TeamPlayersHandler
from handlers import TeamManagerInvitationCheckPhoneHandler
from handlers import TeamManagerInvitationHandler
from handlers import TeamManagerInvitationWithoutTeamHandler
from handlers import TeamManagerInvitationWithTeamHandler
from handlers import TeamManagerInvitationsHandler
from handlers import TeamHandler
from handlers import TeamInvitationHandler

url_patterns = [

    # 用户中心
    (r"/v1/common/dashboard/?", UserBaseInfoHandler),

    # 用户申请统计员
    (r"/v1/statisticians/approvals/?", StatisticianSubmissionHandler),

    # 赛事组织者系统
    (r"/v1/organizer/competitions/([0-9a-z]{24,})/organizers/?", OrganizersHandler),  # post 添加赛事组织者
    (r"/v1/organizer/competitions/([0-9a-z]{24,})/organizers/check_phone/?", OrganizerInvitationCheckPhoneHandler),
    (r"/v1/organizer/competitions/([0-9a-z]{24,})/organizers/([0-9a-z]{24,})/?", OrganizerHandler),  # delete 移除赛事组织者

    (r"/v1/organizer/seasons/?", SeasonListHandler),
    (r"/v1/organizer/seasons/([0-9a-z]{24,})/profile/?", SeasonInfoHandler),
    (r"/v1/organizer/seasons/([0-9a-z]{24,})/teams/?", SeasonTeamsHandler),  # post 添加球队
    (r"/v1/organizer/seasons/([0-9a-z]{24,})/teams/check_phone/?", TeamManagerInvitationCheckPhoneHandler),
    (r"/v1/organizer/seasons/([0-9a-z]{24,})/teams/([0-9a-z]{24,})/?", TeamHandler),  # delete 移除球队
    (r"/v1/organizer/seasons/([0-9a-z]{24,})/teams/([0-9a-z]{24,})/invitations/?", TeamInvitationHandler),  # post 重新发送
    (r"/v1/organizer/seasons/([0-9a-z]{24,})/approvals/?", SeasonApprovalHandler),
    (r"/v1/organizer/seasons/([0-9a-z]{24,})/notifications/?", SeasonNotificationHandler),

    # FIXME: url上需要加上 competition_id，season_id 吗？
    (r"/v1/organizer/teams/([0-9a-z]{24,})/players/?", TeamPlayersHandler),

    (r"/v1/organizer/invitations/?", OrganizerInvitationVerifyHandler),
    (r"/v1/organizer/invitations/activate/?", OrganizerInvitationActivateAccountHandler),
    (r"/v1/organizer/invitations/confirm/?", OrganizerInvitationConfirmHandler),
    (r"/v1/organizer/invitations/reject/?", OrganizerInvitationsRejectHandler),

    # TODO: ----------------  将废弃的  ----------------------

    (r"/v1/organizer/competitions/([0-9a-z]{24,})/invitation/check_phone/?", OrganizerInvitationCheckPhoneHandler),
    (r"/v1/organizer/competitions/([0-9a-z]{24,})/invitation/send_phone/?", OrganizerInvitationHandler),
    (r"/v1/organizer/competitions/([0-9a-z]{24,})/invitation/send_user/?", OrganizerInvitationWithAccountHandler),
    (r"/v1/organizer/competitions/([0-9a-z]{24,})/invitation/remove_user/?", OrganizerRemoveInvitation),
    (r"/v1/organizer/competitions/([0-9a-z]{24,})/invitations/?", OrganizerInvitationsHandler),

    (r"/v1/organizer/seasons/([0-9a-z]{24,})/invitation/check_phone/?", TeamManagerInvitationCheckPhoneHandler),
    (r"/v1/organizer/seasons/([0-9a-z]{24,})/invitation/send_phone/?", TeamManagerInvitationHandler),
    (r"/v1/organizer/seasons/([0-9a-z]{24,})/invitation/send_with_team/?", TeamManagerInvitationWithTeamHandler),
    (r"/v1/organizer/seasons/([0-9a-z]{24,})/invitation/send_without_team/?", TeamManagerInvitationWithoutTeamHandler),
    (r"/v1/organizer/seasons/([0-9a-z]{24,})/invitations/?", TeamManagerInvitationsHandler),

]
