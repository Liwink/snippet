#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Liwink'

import logging

from pylibs.constants import lookup
import bee


def add(events):
    events = [event for event in events if event.get("role") == lookup.StatisticianMatchRole.STATISTICIAN]
    for event in events:
        process("CHECK_EVENT", event)

update = add
delete = add

message_map_doing = {
    "CHECK_EVENT": [bee.check_event],
    "MATCH_SCORE_CHANGE": [bee.update_match_score],
    "PLAYER_MATCH_STATS_EVENT": [bee.update_player_match_stats, bee.update_team_match_stats],
    "PLAYER_MATCH_STATS_CHANGE": [bee.update_player_year_stats],
    "TEAM_MATCH_STATS_CHANGE": [bee.update_team_year_stats],
    "MATCH_ALL_PLAYERS_STATS_CHANGE": [bee.update_match_players_stats],
    "MATCH_ALL_TEAMS_STATS_CHANGE": [bee.update_match_team_stats],
    "MATCH_PERIOD_EVENT": [bee.update_match_period],
    "MATCH_PERIOD_CHANGE": [bee.update_match_players_playing_minutes],
    "MATCH_FINISH_EVENT": [bee.update_match_status],
    "MATCH_STATUS_CHANGE": [bee.update_match_player_total_match_count, bee.update_match_team_total_match_count,
                            bee.update_statistician_statistics, bee.update_statistician_match_status],
    "CTRL_EVENT": [bee.update_match_ctrl],
    "FINISH": []
}


def process(message, event):
    # TODO: convert id to ObjectId
    doings = message_map_doing.get(message)
    messages = []
    for doing in doings:
        messages += doing(event)
    for m in messages:
        process(m, event)

