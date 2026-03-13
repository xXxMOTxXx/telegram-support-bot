from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo


def now_iso(timezone_name: str) -> str:
    return datetime.now(ZoneInfo(timezone_name)).isoformat(timespec="seconds")



def display_time(iso_value: str) -> str:
    return iso_value.replace("T", " ")
