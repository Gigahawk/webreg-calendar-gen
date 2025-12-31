class SearchPattern:
    def __init__(self, config):
        self.keyword = config.get("keyword", "")
        self.days = config.get("days", {})

    @property
    def _days_of_week(self):
        if not self.days:
            return None
        day_list = [
            "Sun",
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
        ]
        return "".join("1" if day in self.days else "0" for day in day_list)

    @property
    def request_data(self):
        return {
            "activity_search_pattern": {
                "skills": [],
                "time_after_str": "",
                "days_of_week": self._days_of_week,
                "activity_select_param": 2,
                "center_ids": [],
                "time_before_str": "",
                "open_spots": None,
                "activity_id": None,
                "activity_category_ids": [],
                "date_before": "",
                "min_age": None,
                "date_after": "",
                "activity_type_ids": [],
                "site_ids": [],
                "for_map": False,
                "geographic_area_ids": [],
                "season_ids": [],
                "activity_department_ids": [],
                "activity_other_category_ids": [],
                "child_season_ids": [],
                "activity_keyword": self.keyword,
                "instructor_ids": [],
                "max_age": None,
                "custom_price_from": "",
                "custom_price_to": "",
            },
            "activity_transfer_pattern": {},
        }
