#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Core compatibility layer for Global Time Utility (gtime).
Existing imports from gtime.core remain supported.
"""

from .storage import FAV_FILE, load_favorites, save_favorites
from .search import _get_city_names, fuzzy_search_city, get_city_by_name, suggest_cities
from .timecore import (
    ZoneInfo,
    _get_safe_emoji,
    _is_terminal_compatible,
    get_funny_footer,
    get_greeting,
    get_time_emoji,
    format_utc_offset,
    to_local_aware,
    convert_meeting_time,
)

__all__ = [
    "FAV_FILE",
    "load_favorites",
    "save_favorites",
    "_get_city_names",
    "fuzzy_search_city",
    "get_city_by_name",
    "suggest_cities",
    "ZoneInfo",
    "_get_safe_emoji",
    "_is_terminal_compatible",
    "get_time_emoji",
    "get_greeting",
    "get_funny_footer",
    "format_utc_offset",
    "to_local_aware",
    "convert_meeting_time",
]
