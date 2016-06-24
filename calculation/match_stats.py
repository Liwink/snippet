#!/usr/bin/env python
# encoding: utf-8

class Stats:
    def __init__(self, match_types, cities):
        self.city = ', '.join(cities)
        self.match_type = ', '.join(map(lambda i: str(i), match_types))

        self.match_types = match_types
        self.cities = cities
        self.match_ids = self.get_match_ids()

        self.fields = ["event_count", "goal_count", "interception_count",
                       "assist_count", "pass_count",
                       "attended_player_count", "goaled_player_count",
                       "interception_per_goal", "pass_per_goal",
                       "event_per_goal", "event_per_assist",]
        self.all_fields = self.fields + ["city", "match_type"]

        self.t = {
            "event_count": "事件总数",
            "goal_count": "进球总数",
            "interception_count": "抢断总数",
            "assist_count": "助攻总数",
            "pass_count": "传球总数",
            "attended_player_count": "参数球员数",
            "goaled_player_count": "进球球员数",
            "interception_per_goal": "抢断/进球",
            "pass_per_goal": "传球/进球",
            "event_per_goal": "事件/进球",
            "event_per_assist": "事件/助攻",
            "city": "城市",
            "match_type": "几人制",
        }

        for field in self.fields:
            setattr(self, field, getattr(self, "get_{0}".format(field))())

    def get_match_ids(self):
        competition_criteria = {
            "op_id": {"$nin": ["C10012", "C10015"]},
            "area.city": {"$in": self.cities}
        }
        competition_ids = conn.CompetitionDocument.find(competition_criteria).distinct("_id")

        season_criteria = {
            "match_type": {"$in": self.match_types},
            "competition_id": {"$in": competition_ids}
        }
        season_ids = conn.SeasonDocument.find(season_criteria).distinct("_id")

        match_criteria = {
            "season_id": {"$in": season_ids}
        }
        match_ids = conn.MatchDocument.find(match_criteria).distinct("_id")
        return match_ids

    @staticmethod
    def calculate_event_count(match_ids, *codes):
        event_criteria = {
            "match_id": {"$in": match_ids},
            "code": {"$in": codes}
        }
        event_count = conn.EventDocument.find(event_criteria).count()
        return event_count

    def get_event_count(self):
        return self.calculate_event_count(self.match_ids,
                                            *range(90))

    def get_goal_count(self):
        return self.calculate_event_count(self.match_ids,
                                            lookup.EventCode.GOAL.value)

    def get_assist_count(self):
        return self.calculate_event_count(self.match_ids,
                                            lookup.EventCode.GOAL_ASSIST.value)

    def get_interception_count(self):
        return self.calculate_event_count(self.match_ids,
                                            lookup.EventCode.INTERCEPTION.value)

    def get_pass_count(self):
        return self.calculate_event_count(self.match_ids,
                                            lookup.EventCode.SUCCESSFUL_PASS.value,
                                            lookup.EventCode.UNSUCCESSFUL_PASS.value)

    def get_attended_player_count(self):
        attend_player_criteria = {
            "match_id": {"$in": self.match_ids},
            "attend_match_count": 1
        }
        return len(conn.PlayerMatchStatsDocument \
                    .find(attend_player_criteria).distinct("player_id"))

    def get_goaled_player_count(self):
        goaled_player_criteria = {
            "match_id": {"$in": self.match_ids},
            "goal": {"$gt": 0},
            "attend_match_count": 1
        }
        return len(conn.PlayerMatchStatsDocument \
                    .find(goaled_player_criteria).distinct("player_id"))

    def get_interception_per_goal(self):
        return self.interception_count / self.goal_count if self.goal_count else 0

    def get_pass_per_goal(self):
        return self.pass_count / self.goal_count if self.goal_count else 0

    def get_event_per_goal(self):
        return self.event_count / self.goal_count if self.goal_count else 0

    def get_event_per_assist(self):
        return self.event_count / self.assist_count if self.assist_count else 0

    def to_dict(self):
        result = {}
        for field in self.all_fields:
            result.update({self.t.get(field): getattr(self, field)})
            return(result)

