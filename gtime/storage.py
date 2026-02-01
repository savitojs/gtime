#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Storage helpers for Global Time Utility (gtime).
"""

import json
import os
from pathlib import Path
from typing import List


def _get_fav_file() -> Path:
    override = os.environ.get("GTIME_FAV_FILE")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".gtime_favorites.json"


FAV_FILE = _get_fav_file()


def load_favorites() -> List[str]:
    fav_file = _get_fav_file()
    if fav_file.exists():
        try:
            with open(fav_file, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_favorites(favs: List[str]) -> None:
    fav_file = _get_fav_file()
    with open(fav_file, "w") as f:
        json.dump(favs, f, indent=2)
