#!/usr/bin/env python
# encoding: utf-8

class Stats:
    def __init__(self, match_types, cities):
        self.city = ', '.join(cities)
        self.match_type = ', '.join(map(lambda i: str(i), match_types))
        
        self.match_types = match_types
        self.cities = cities
        self.match_ids = self.get_match_ids()
        self.match_end_at = self.get_match_end_at()
        self.match_goal_data = self.get_match_goal_data()

        self.fields = ["event_count", "goal_count", "interception_count",
                       "assist_count", "pass_count", "shotted_player_count",
                       "attended_player_count", "goaled_player_count",
                       "interception_per_goal", "pass_per_goal",
                       "event_per_goal", "event_per_assist",
                       "last_10_minutes_goals", "first_10_minutes_goals",
                       "two_goal_in_five_minutes",
                       "extra_time_count", "penalty_count",
                      ]
        self.all_fields = self.fields + ["city", "match_type"]
        
        self.t = {
            "event_count": "事件总数",
            "goal_count": "进球总数",
            "interception_count": "抢断总数",
            "assist_count": "助攻总数",
            "pass_count": "传球总数",
            "attended_player_count": "参数球员数",
            "goaled_player_count": "进球球员数",
            "shotted_player_count": "射门球员数",
            "interception_per_goal": "抢断/进球",
            "pass_per_goal": "传球/进球",
            "event_per_goal": "事件/进球",
            "event_per_assist": "事件/助攻",
            "city": "城市",
            "match_type": "几人制",
            "two_goal_in_five_minutes": "5分钟内同队失两球比赛数",
            "first_10_minutes_goals": "前10分钟进球数",
            "last_10_minutes_goals": "最后10分钟进球数",
            "extra_time_count": "加时比赛数",
            "penalty_count": "点球比赛数",
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
            "season_id": {"$in": season_ids},
            "status": "Played"
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
    
    def get_shotted_player_count(self):
        shotted_player_criteria = {
            "match_id": {"$in": self.match_ids},
            "attend_match_count": 1,
            "$or": [
                {"shot_on_target": {"$gt": 0}},
                {"shot_off_target": {"$gt": 0}},
            ],
        }
        return len(conn.PlayerMatchStatsDocument \
                   .find(shotted_player_criteria).distinct("player_id"))
    
    def get_interception_per_goal(self):
        return round(self.interception_count / self.goal_count, 2) if self.goal_count else 0
    
    def get_pass_per_goal(self):
        return round(self.pass_count / self.goal_count, 2) if self.goal_count else 0
    
    def get_event_per_goal(self):
        return round(self.event_count / self.goal_count, 2) if self.goal_count else 0
    
    def get_event_per_assist(self):
        return round(self.event_count / self.assist_count, 2) if self.assist_count else 0
    
    def get_match_end_at(self):
        _match_criteria = {"$match": {"match_id": {"$in": self.match_ids}, "code": 111, "role": "statistician"}}
        _project_criteria = {"$project": {"match_id": 1, "client_match_clock": 1}}
        _group_criteria = {"$group": 
                          {"_id": "$match_id",
                           "match_end_at": {"$max": "$client_match_clock"}}}
        _data = db.data_events.aggregate([_match_criteria,
                                          _project_criteria,
                                          _group_criteria])["result"]
        data = {}
        for item in _data:
            data.update({item["_id"]: item["match_end_at"]})
        return data
    
    def get_match_goal_data(self):
        match_criteria = {"$match": {"match_id": {"$in": self.match_ids}, "code": 71}}
        project_criteria = {"$project": {"code": 1, "match_id": 1, "team_id": 1, "client_match_clock": 1}}
        group_criteria = {"$group": 
                          {"_id": {"match_id": "$match_id", "team_id": "$team_id"}, 
                           "client_match_clocks": {"$push": "$client_match_clock"}}}
        data = db.data_events.aggregate([match_criteria,
                                         project_criteria,
                                         group_criteria])["result"]
        return data
    
    def get_two_goal_in_five_minutes(self):

        def check_within_five(array):
            array = sorted(array)
            for index in range(len(array)-1):
                if array[index] + 5 > array[index + 1]:
                    return True
            return False
        
        match_list = []
        
        for item in self.match_goal_data:
            if check_within_five(item["client_match_clocks"])\
            and item["_id"]["match_id"] not in match_list:
                match_list.append(item["_id"]["match_id"])
        
        return len(match_list)
    
    @staticmethod
    def count_by_condition(array, condition):
        sums = 0
        for item in array:
            if condition(item):
                sums += 1
        return sums
    
    def get_first_10_minutes_goals(self):
        sums = 0
        
        def first_10_minutes_condition(item):
            return item < 10
        
        for item in self.match_goal_data:
            sums += self.count_by_condition(item["client_match_clocks"], first_10_minutes_condition)
        return sums
    
    def get_last_10_minutes_goals(self):
        sums = 0
        
        def last_10_minutes_condition(end_at, item):
            return item > end_at - 10
        
        for item in self.match_goal_data:
            sums += self.count_by_condition(item["client_match_clocks"],
                                            partial(last_10_minutes_condition,
                                                    self.match_end_at[item["_id"]["match_id"]]))
        return sums
    
    def get_extra_time_count(self):
        return self.calculate_event_count(self.match_ids,
                                          lookup.EventCode.MATCH_EXTRA_TIME_FIRST_HALF_KICK_OFF.value)
    
    def get_penalty_count(self):
        return self.calculate_event_count(self.match_ids,
                                          lookup.EventCode.MATCH_PENALTY_SHOOT_OUT_BEGIN.value)
    
    def to_dict(self):
        result = {}
        for field in self.all_fields:
            result.update({self.t.get(field): getattr(self, field)})
        return(result)