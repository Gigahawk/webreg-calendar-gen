from datetime import datetime

import dateutil.parser as dt_parser
# HACK: use local timezone to deal with daylight savings.
# In practice this would never be run outside the local timezone.
from webreg_calendar_gen.util import tzlocal

class WebregEvent:
    def __init__(self, data):
        self.__data = data

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def number(self) -> str:
        return self._number
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def activity_url(self) -> str:
        return self._detail_url
    
    @property
    def enroll_url(self) -> str:
        return self._enroll_now["href"]

    @property
    def registration_dt(self) -> datetime:
        return dt_parser.parse(
            self._activity_online_start_time,
            ignoretz=True,
            tzinfos=tzlocal,
            yearfirst=True
        )
    
    @property
    def _time_range_tuple(self) -> tuple[str, str]:
        return tuple(self._time_range.split(" - "))
    
    @property
    def _start_date_str(self) -> str:
        return self._date_range_start
    
    @property
    def _end_date_str(self) -> str:
        if self._date_range_end:
            return self._date_range_end
        return self._date_range_start
    
    @property
    def start_dt(self) -> datetime:
        dt_str = f"{self._date_range_start} {self._time_range_tuple[0]}"
        return dt_parser.parse(
            dt_str,
            ignoretz=True,
            tzinfos=tzlocal,
        )
    
    @property
    def end_dt(self) -> datetime:
        dt_str = f"{self._end_date_str} {self._time_range_tuple[1]}"
        return dt_parser.parse(
            dt_str,
            ignoretz=True,
            tzinfos=tzlocal,
        )
    
    @property
    def desc(self) -> str:
        return self._desc.strip()
        
    def __getattr__(self, name):
        if name.startswith("_"):
            out =  self.__data.get(name[1:])
            if out is not None:
                return out
        raise AttributeError(f"No attribute '{name}' in WebregEvent")
