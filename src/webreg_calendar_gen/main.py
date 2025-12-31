import argparse
import json
from pprint import pprint

import requests
import yaml

from webreg_calendar_gen.webreg_event import WebregEvent
from webreg_calendar_gen.search_pattern import SearchPattern

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


def _get_params():
    return {
        "locale": "en-US",
    }


def get_activities(config: SearchPattern) -> list[WebregEvent] | None:
    events = []
    page = 1
    total_page = None
    while True:
        print(f"Fetching page {page}...")
        r = requests.post(
            url=base_url,
            # params=_get_params(),
            json=config.request_data,
            headers=_get_header(page_num=page),
        )
        if r.status_code != 200:
            print("Error fetching data")
            return None
        headers = r.json().get("headers", None)
        if headers is None:
            print("No headers in response")
            return None
        if "successful" not in headers.get("response_message", "").lower():
            print("Response message not success")
            pprint(r.json())
            return None
        if total_page is None:
            page_info = headers.get("page_info", None)
            if page_info is None:
                print("No page_info in response headers")
                return None
            if (total_page := page_info.get("total_page", None)) is None:
                print("No total_page in response headers")
                return None

        body = r.json().get("body", None)
        if body is None:
            print("No body in response")
            return None
        items = body.get("activity_items", None)
        if items is None:
            print("No activity items in response")
            return None
        if not isinstance(items, list):
            print("Activity items is not a list?")
            return None
        events.extend([WebregEvent(item) for item in items])
        if page < total_page:
            page += 1
        else:
            break
    return events


def main():
    print("Hello from webreg-calendar-gen!")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="config.yaml",
    )
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = SearchPattern(yaml.safe_load(f))
    activities = get_activities(config)

    def filter_activities(act: WebregEvent) -> bool:
        # Example filter: only show activities with open spots
        start_dt = act.start_dt
        start_dow = start_dt.strftime("%a")
        dow_config = config.days.get(start_dow, None)
        if dow_config is None:
            return False
        time_start = dow_config.get("time_start", None)
        if time_start is None:
            return False
        # HACK: probably should create a class to store a min/max time start/end
        # instead of this
        if start_dt.strftime("%H:%M") != time_start:
            return False
        return True

    activities = [a for a in activities if filter_activities(a)]
    import pdb;pdb.set_trace()


if __name__ == "__main__":
    main()
