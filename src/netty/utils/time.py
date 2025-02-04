"""Copyright 2024 wangxin.jeffry@gmail.com
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http:www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic_extra_types.timezone_name import TimeZoneName


def get_timezone_hour_offset(tz: TimeZoneName) -> int:
    """
    Get the hour offset of the given timezone
    :param tz: the timezone to query
    :return: the hour offset of the timezone
    """
    now = datetime.now()  # noqa: DTZ005
    timezone = ZoneInfo(tz)
    localized_time = now.replace(tzinfo=timezone)
    if localized_time is None:
        msg = f"Localized time for timezone {tz} is None"
        raise ValueError(msg)
    utc_offset = localized_time.utcoffset()
    if utc_offset is None:
        msg = f"UTC offset for timezone {tz} is None"
        raise ValueError(msg)
    try:
        utc_offset_seconds = int(utc_offset.total_seconds())
        utc_offset_hours = utc_offset_seconds / 3600
        return int(utc_offset_hours)
    except AttributeError as e:
        msg = f"Error occurred while calculating utc offset for timezone {tz}"
        raise ValueError(msg) from e


def seconds_to_ruijie_lease_time(total_seconds: int) -> str:
    seconds_in_a_minute = 60
    seconds_in_an_hour = 60 * seconds_in_a_minute
    seconds_in_a_day = 24 * seconds_in_an_hour
    days = total_seconds // seconds_in_a_day
    remaining_seconds = total_seconds % seconds_in_a_day
    hours = remaining_seconds // seconds_in_an_hour
    remaining_seconds %= seconds_in_an_hour
    minutes = remaining_seconds // seconds_in_a_minute

    return f"{days} {hours} {minutes}"
