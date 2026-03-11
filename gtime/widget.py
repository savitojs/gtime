#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Desktop widget output for Global Time Utility (gtime).
Generates Pango-markup formatted text for GNOME desktop widgets
(azclock Desktop Widgets extension CommandLabel element).

Usage:
  gtime widget [a|b|c]

Styles:
  a - Flags + color-coded time + status + day diff (default)
  b - Grouped by status (Working, Sleeping, etc.)
  c - Compact cards with flag, time, status, hour diff
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple
from zoneinfo import ZoneInfo

from .data import CITY_DB
from .storage import load_favorites
from .search import get_city_by_name

COUNTRY_FLAGS = {
    "USA": "\U0001f1fa\U0001f1f8", "UK": "\U0001f1ec\U0001f1e7",
    "Canada": "\U0001f1e8\U0001f1e6", "Germany": "\U0001f1e9\U0001f1ea",
    "France": "\U0001f1eb\U0001f1f7", "Japan": "\U0001f1ef\U0001f1f5",
    "India": "\U0001f1ee\U0001f1f3", "Australia": "\U0001f1e6\U0001f1fa",
    "China": "\U0001f1e8\U0001f1f3", "Brazil": "\U0001f1e7\U0001f1f7",
    "Czech Republic": "\U0001f1e8\U0001f1ff", "Latvia": "\U0001f1f1\U0001f1fb",
    "Singapore": "\U0001f1f8\U0001f1ec", "South Korea": "\U0001f1f0\U0001f1f7",
    "Mexico": "\U0001f1f2\U0001f1fd", "Netherlands": "\U0001f1f3\U0001f1f1",
    "Sweden": "\U0001f1f8\U0001f1ea", "Ireland": "\U0001f1ee\U0001f1ea",
    "Italy": "\U0001f1ee\U0001f1f9", "Spain": "\U0001f1ea\U0001f1f8",
    "Poland": "\U0001f1f5\U0001f1f1", "Switzerland": "\U0001f1e8\U0001f1ed",
    "UAE": "\U0001f1e6\U0001f1ea", "New Zealand": "\U0001f1f3\U0001f1ff",
    "Argentina": "\U0001f1e6\U0001f1f7", "Russia": "\U0001f1f7\U0001f1fa",
    "Belgium": "\U0001f1e7\U0001f1ea", "Norway": "\U0001f1f3\U0001f1f4",
    "Denmark": "\U0001f1e9\U0001f1f0", "Finland": "\U0001f1eb\U0001f1ee",
    "Austria": "\U0001f1e6\U0001f1f9", "Portugal": "\U0001f1f5\U0001f1f9",
    "Greece": "\U0001f1ec\U0001f1f7", "Hungary": "\U0001f1ed\U0001f1fa",
    "Romania": "\U0001f1f7\U0001f1f4", "Ukraine": "\U0001f1fa\U0001f1e6",
    "Estonia": "\U0001f1ea\U0001f1ea", "Lithuania": "\U0001f1f1\U0001f1f9",
    "Thailand": "\U0001f1f9\U0001f1ed", "Indonesia": "\U0001f1ee\U0001f1e9",
    "Taiwan": "\U0001f1f9\U0001f1fc", "Egypt": "\U0001f1ea\U0001f1ec",
    "South Africa": "\U0001f1ff\U0001f1e6", "Nigeria": "\U0001f1f3\U0001f1ec",
    "Kenya": "\U0001f1f0\U0001f1ea", "Colombia": "\U0001f1e8\U0001f1f4",
    "Peru": "\U0001f1f5\U0001f1ea", "Chile": "\U0001f1e8\U0001f1f1",
    "Iceland": "\U0001f1ee\U0001f1f8", "Croatia": "\U0001f1ed\U0001f1f7",
    "Serbia": "\U0001f1f7\U0001f1f8", "Bulgaria": "\U0001f1e7\U0001f1ec",
    "Luxembourg": "\U0001f1f1\U0001f1fa", "Belarus": "\U0001f1e7\U0001f1fe",
    "Moldova": "\U0001f1f2\U0001f1e9", "Bolivia": "\U0001f1e7\U0001f1f4",
    "Paraguay": "\U0001f1f5\U0001f1fe", "Uruguay": "\U0001f1fa\U0001f1fe",
    "Venezuela": "\U0001f1fb\U0001f1ea", "Ecuador": "\U0001f1ea\U0001f1e8",
    "Philippines": "\U0001f1f5\U0001f1ed", "Vietnam": "\U0001f1fb\U0001f1f3",
    "Malaysia": "\U0001f1f2\U0001f1fe", "Pakistan": "\U0001f1f5\U0001f1f0",
    "Bangladesh": "\U0001f1e7\U0001f1e9", "Sri Lanka": "\U0001f1f1\U0001f1f0",
}


def _get_period_icon(hour: int) -> str:
    if 6 <= hour < 12:
        return "\U0001f305"
    if 12 <= hour < 18:
        return "\U0001f31e"
    if 18 <= hour < 21:
        return "\U0001f307"
    return "\U0001f319"


def _get_work_status(hour: int) -> Tuple[str, str]:
    if 0 <= hour < 6:
        return ("Sleeping", "#8b9dc3")
    if 6 <= hour < 9:
        return ("Early", "#f0c75e")
    if 9 <= hour < 12:
        return ("Working", "#73c991")
    if 12 <= hour < 14:
        return ("Lunch", "#f0ad4e")
    if 14 <= hour < 18:
        return ("Working", "#73c991")
    if 18 <= hour < 22:
        return ("Off", "#c9a0dc")
    return ("Sleeping", "#8b9dc3")


def _get_status_icon(hour: int) -> str:
    if 0 <= hour < 6:
        return "\U0001f4a4"
    if 6 <= hour < 9:
        return "\u2615"
    if 9 <= hour < 12:
        return "\U0001f4bb"
    if 12 <= hour < 14:
        return "\U0001f372"
    if 14 <= hour < 18:
        return "\U0001f4bb"
    if 18 <= hour < 22:
        return "\U0001f3e0"
    return "\U0001f4a4"


def _get_time_color(hour: int) -> str:
    if 9 <= hour < 18:
        return "#73c991"
    if 6 <= hour < 9 or 18 <= hour < 22:
        return "#e8c36a"
    return "#7c8db5"


def _format_utc_offset(dt: datetime) -> str:
    offset = dt.utcoffset()
    if offset is not None:
        total_minutes = offset.total_seconds() / 60
        hours = int(total_minutes // 60)
        minutes = int(abs(total_minutes) % 60)
        sign = "+" if hours >= 0 else "-"
        return f"UTC{sign}{abs(hours)}" + (f":{minutes:02}" if minutes else "")
    return "UTC?"


def _format_hour_diff(local_now: datetime, city_now: datetime) -> str:
    local_off = local_now.utcoffset().total_seconds() / 3600
    city_off = city_now.utcoffset().total_seconds() / 3600
    diff = city_off - local_off
    if diff == 0:
        return "<span size='small' alpha='50%'>local</span>"
    sign = "+" if diff > 0 else ""
    if diff == int(diff):
        return f"<span size='small' alpha='40%'>{sign}{int(diff)}h</span>"
    return f"<span size='small' alpha='40%'>{sign}{diff:.1f}h</span>"


def _get_day_diff(local_now: datetime, city_now: datetime) -> str:
    diff = (city_now.date() - local_now.date()).days
    if diff == 1:
        return " <span size='small' foreground='#73c991'>+1d</span>"
    if diff == -1:
        return " <span size='small' foreground='#e86b6b'>-1d</span>"
    return ""


def _get_flag(country: str) -> str:
    return COUNTRY_FLAGS.get(country, "\U0001f30d")


def _get_city_data() -> Tuple[List[Tuple[str, str, datetime, str]], datetime]:
    favorites = load_favorites()
    now = datetime.now()
    city_times = []
    for city_name in favorites:
        info = get_city_by_name(city_name)
        if not info:
            continue
        display_name, country, tz_name, _ = info
        try:
            tz = ZoneInfo(tz_name)
            city_now = now.astimezone(tz)
            city_times.append((display_name, country, city_now, tz_name))
        except Exception:
            continue
    city_times.sort(key=lambda x: x[2].utcoffset().total_seconds())
    return city_times, now


def _style_a() -> str:
    """Flags + color-coded time + status + day diff"""
    city_times, now = _get_city_data()
    local_now = now.astimezone()
    lines = []
    for display_name, country, city_now, tz_name in city_times:
        hour = city_now.hour
        time_str = city_now.strftime("%H:%M")
        offset = _format_utc_offset(city_now)
        flag = _get_flag(country)
        status, status_color = _get_work_status(hour)
        time_color = _get_time_color(hour)
        day_diff = _get_day_diff(local_now, city_now)

        line = (
            f"{flag} "
            f"<b>{display_name}</b>"
            f"  "
            f"<span size='large' foreground='{time_color}'><b>{time_str}</b></span>"
            f"{day_diff}"
            f"  "
            f"<span foreground='{status_color}'>\u25cf {status}</span>"
            f"  "
            f"<span size='small' alpha='40%'>{offset}</span>"
        )
        lines.append(line)
    return "\n".join(lines)


def _style_b() -> str:
    """Grouped by status"""
    city_times, now = _get_city_data()
    local_now = now.astimezone()

    groups = {}
    for display_name, country, city_now, tz_name in city_times:
        hour = city_now.hour
        status, status_color = _get_work_status(hour)
        key = (status, status_color)
        if key not in groups:
            groups[key] = []
        groups[key].append((display_name, country, city_now, tz_name))

    status_order = ["Working", "Lunch", "Early", "Off", "Sleeping"]
    lines = []
    first = True
    for status_name in status_order:
        matching = [(k, v) for k, v in groups.items() if k[0] == status_name]
        if not matching:
            continue
        (status, status_color), cities = matching[0]
        status_icon = _get_status_icon(cities[0][2].hour)

        if not first:
            lines.append("")
        first = False

        lines.append(
            f"<span foreground='{status_color}'>"
            f"{status_icon} <b>{status}</b></span>"
        )
        for display_name, country, city_now, tz_name in cities:
            time_str = city_now.strftime("%H:%M")
            time_color = _get_time_color(city_now.hour)
            flag = _get_flag(country)
            day_diff = _get_day_diff(local_now, city_now)
            lines.append(
                f"  {flag} {display_name}"
                f"  <span foreground='{time_color}'><b>{time_str}</b></span>"
                f"{day_diff}"
            )
    return "\n".join(lines)


def _style_c() -> str:
    """Compact cards with flag, time, status, hour diff"""
    city_times, now = _get_city_data()
    local_now = now.astimezone()
    lines = []
    for i, (display_name, country, city_now, tz_name) in enumerate(city_times):
        hour = city_now.hour
        time_str = city_now.strftime("%H:%M")
        flag = _get_flag(country)
        icon = _get_period_icon(hour)
        status, status_color = _get_work_status(hour)
        time_color = _get_time_color(hour)
        day_diff = _get_day_diff(local_now, city_now)
        hour_diff = _format_hour_diff(local_now, city_now)

        row1 = (
            f"{flag} <b>{display_name}</b>  {icon}"
        )
        row2 = (
            f"   "
            f"<span size='large' foreground='{time_color}'><b>{time_str}</b></span>"
            f"{day_diff}"
            f"  "
            f"<span foreground='{status_color}'>\u25cf {status}</span>"
            f"  "
            f"{hour_diff}"
        )
        lines.append(row1)
        lines.append(row2)
        if i < len(city_times) - 1:
            lines.append("")
    return "\n".join(lines)


STYLES = {
    "a": _style_a,
    "b": _style_b,
    "c": _style_c,
}


def widget_output(style: str = "a") -> str:
    """Generate Pango-markup widget output for the given style."""
    func = STYLES.get(style.lower(), _style_a)
    return func()


def run_widget(args: Optional[List[str]] = None):
    """Entry point for 'gtime widget' command. Prints raw Pango markup to stdout."""
    style = "a"
    if args:
        style = args[0].lower()
    output = widget_output(style)
    if not output:
        print("No gtime favorites")
    else:
        print(output)
