import json
from pprint import pprint

import requests

base_url = "https://anc.ca.apm.activecommunities.com/burnaby/rest/activities/list"


def _get_header(page_num: int = 1):
    return {
        "page_info": json.dumps(
            {
                "order_by": "Date range",
                "page_number": page_num,
                # Seems to always be 20 no matter what this is set to?
                # "total_records_per_page": 20
            }
        )
    }


def _get_body():
    return {
        "activity_search_pattern": {
            "skills": [],
            "time_after_str": "",
            "days_of_week": None,
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
            "activity_keyword": "Open Workshop",
            "instructor_ids": [],
            "max_age": None,
            "custom_price_from": "",
            "custom_price_to": "",
        },
        "activity_transfer_pattern": {},
    }


def _get_params():
    return {
        "locale": "en-US",
    }


def main():
    print("Hello from webreg-calendar-gen!")
    r = requests.post(
        url=base_url,
        #params=_get_params(),
        json=_get_body(),
        headers=_get_header(),
    )
    pprint(r)
    pprint(r.json())


if __name__ == "__main__":
    main()
