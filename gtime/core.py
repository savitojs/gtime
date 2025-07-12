#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Core logic for Global Time Utility (gtime) lookup, fuzzy search, helpers
"""

import datetime
import json
from pathlib import Path
from typing import List, Tuple, Optional
import random
from functools import lru_cache

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from pytz import timezone as ZoneInfo

from .data import CITY_DB

FAV_FILE = Path.home() / ".gtime_favorites.json"

def load_favorites() -> List[str]:
    if FAV_FILE.exists():
        try:
            with open(FAV_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_favorites(favs: List[str]) -> None:
    with open(FAV_FILE, "w") as f:
        json.dump(favs, f)

_city_names_cache = None
_city_name_to_index = None

def _get_city_names():
    global _city_names_cache, _city_name_to_index
    if _city_names_cache is None or len(_city_names_cache) != len(CITY_DB):
        _city_names_cache = [f"{city} ({country})" for city, country, _, _ in CITY_DB]
        _city_name_to_index = {name: idx for idx, name in enumerate(_city_names_cache)}
    return _city_names_cache, _city_name_to_index

@lru_cache(maxsize=256)
def fuzzy_search_city(query: str) -> Optional[Tuple[str, str, str, str]]:
    from thefuzz import process
    names, name_to_idx = _get_city_names()
    
    # First priority: exact match (case insensitive)
    query_lower = query.lower()
    for name in names:
        city_name = name.split(" (")[0].lower()
        if city_name == query_lower:
            idx = name_to_idx[name]
            return CITY_DB[idx]
    
    # Second priority: starts with (case insensitive)
    for name in names:
        city_name = name.split(" (")[0].lower()
        if city_name.startswith(query_lower):
            idx = name_to_idx[name]
            return CITY_DB[idx]
    
    # Third priority: substring match (case insensitive)
    for name in names:
        city_name = name.split(" (")[0].lower()
        if query_lower in city_name:
            idx = name_to_idx[name]
            return CITY_DB[idx]
    
    # Fourth priority: fuzzy match on city names only (not including country)
    city_names_only = [name.split(" (")[0] for name in names]
    match, score = process.extractOne(query, city_names_only)
    if score > 60:
        for name in names:
            if name.split(" (")[0] == match:
                idx = name_to_idx[name]
                return CITY_DB[idx]
    
    return None

@lru_cache(maxsize=256)
def get_city_by_name(city_name: str) -> Optional[Tuple[str, str, str, str]]:
    for city, country, tz, emoji in CITY_DB:
        if city.lower() == city_name.lower():
            return (city, country, tz, emoji)
    
    return fuzzy_search_city(city_name)

def suggest_cities(city_name: str) -> List[str]:
    from thefuzz import process
    names, _ = _get_city_names()
    
    # Use city names only for better suggestions
    city_names_only = [name.split(" (")[0] for name in names]
    matches = process.extract(city_name, city_names_only, limit=3)
    
    # Convert back to full names for suggestions
    suggestions = []
    for match, score in matches:
        if score > 40:
            for name in names:
                if name.split(" (")[0] == match:
                    suggestions.append(name)
                    break
    
    return suggestions

def get_time_emoji(hour: int) -> str:
    if 5 <= hour < 12:
        return "🌅"
    elif 12 <= hour < 17:
        return "☀️"
    elif 17 <= hour < 21:
        return "🌆"
    else:
        return "🌙"

def get_greeting(hour: int) -> str:
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    else:
        return "Good night"

def get_funny_footer(city: str, hour: int) -> str:
    night_jokes = [
        f"It's late in {city}. Don't let the bed bugs bite! 🛌",
        f"{city} is sleeping. Or are you a night owl? 🦉",
        f"Shhh... {city} is dreaming. 😴",
        f"The stars are shining bright over {city}! ✨",
        f"Midnight snack time in {city}? 🍕",
        f"The city that never sleeps? Not {city} right now! 💤",
        f"Late night thoughts from {city}... 💭",
        f"Even {city} needs beauty sleep! 💄",
        f"Night shift workers in {city} are keeping busy! 🌃",
        f"Sweet dreams from {city}! 🌙",
        f"Time for some beauty sleep in {city}! 💤",
        f"The moon is watching over {city} tonight! 🌛",
        f"Counting sheep in {city}... 1, 2, 3... 🐑",
        f"Pizza delivery is probably still open in {city}! 🍕",
        f"Time to binge-watch something in {city}! 📺",
        f"Late night coding session in {city}? 💻",
        f"The night is young in {city}! 🌃",
        f"Peaceful slumber awaits in {city}! 😴",
        f"Night photography weather in {city}! 📸",
        f"The city is tucked in for the night in {city}! 🛏️",
        f"Insomniacs unite in {city}! 😵",
        f"Time for a bedtime story in {city}! 📚",
        f"The witching hour in {city}! 🧙‍♀️",
        f"Dreaming of better days in {city}! 💭",
        f"Silent streets in {city} tell stories! 🏙️",
    ]
    morning_jokes = [
        f"Rise and shine, {city}! ☀️",
        f"Coffee time in {city}? ☕",
        f"Start your engines, {city}! 🚗",
        f"The early bird catches the worm in {city}! 🐦",
        f"Fresh morning air in {city}! 🌬️",
        f"Time to seize the day in {city}! 💪",
        f"Morning jog weather in {city}? 🏃",
        f"Breakfast is the most important meal in {city}! 🥞",
        f"The sun is greeting {city} with a smile! 😊",
        f"New day, new possibilities in {city}! 🌈",
        f"Rush hour is starting in {city}! 🚌",
        f"Morning news is on in {city}! 📺",
        f"Good morning sunshine from {city}! 🌞",
        f"Fresh croissants and coffee in {city}? 🥐",
        f"Morning yoga session in {city}? 🧘‍♀️",
        f"Alarm clocks are ringing in {city}! ⏰",
        f"Another beautiful morning in {city}! 🌸",
        f"Time to make your bed in {city}! 🛏️",
        f"Fresh start vibes in {city}! ✨",
        f"Morning commute begins in {city}! 🚇",
        f"Time to water the plants in {city}! 🪴",
        f"Birds are chirping in {city}! 🐦",
        f"Morning motivation mode in {city}! 💪",
        f"The world is your oyster in {city}! 🦪",
        f"Sunrise spectacular in {city}! 🌅",
        f"Fresh as a daisy in {city}! 🌼",
        f"Morning mindfulness in {city}! 🧠",
        f"Early bird specials in {city}! 🍳",
    ]
    afternoon_jokes = [
        f"Keep hustling, {city}! 💪",
        f"Perfect time for a siesta in {city}. 😴",
        f"Hope your day is going well in {city}! 🌞",
        f"Lunch break time in {city}? 🍽️",
        f"The sun is at its peak in {city}! ☀️",
        f"Productivity mode activated in {city}! 📈",
        f"Ice cream weather in {city}? 🍦",
        f"Working hard or hardly working in {city}? 💼",
        f"The afternoon hustle in {city} is real! 🏃‍♀️",
        f"Time flies when you're having fun in {city}! ⏰",
        f"Midday energy boost needed in {city}? ⚡",
        f"The perfect time for outdoor activities in {city}! 🌳",
        f"Sunshine and productivity in {city}! 🌻",
        f"Time to stretch those legs in {city}! 🤸‍♂️",
        f"Afternoon meeting marathon in {city}! 📊",
        f"Time for a quick power walk in {city}! 🚶‍♀️",
        f"Perfect weather for outdoor dining in {city}! 🍴",
        f"Getting things done in {city}! ✅",
        f"Halfway through the workday in {city}! 📈",
        f"Afternoon delight in {city}! 🎵",
        f"Keep calm and carry on in {city}! 🧘",
        f"The grind never stops in {city}! ⚙️",
        f"Peak performance hours in {city}! 🏆",
        f"Time for a coffee break in {city}! ☕",
        f"Afternoon adventures await in {city}! 🗺️",
        f"Sunshine therapy in {city}! ☀️",
        f"Power through the afternoon in {city}! 💪",
        f"The day is in full swing in {city}! 🎯",
    ]
    evening_jokes = [
        f"Time to relax in {city}. 🍷",
        f"Sunset vibes in {city}. 🌇",
        f"Netflix and chill in {city}? 🍿",
        f"Happy hour somewhere in {city}! 🍻",
        f"Dinner plans in {city}? 🍽️",
        f"The golden hour in {city} looks magical! ✨",
        f"Time to unwind in {city}! 🧘",
        f"Evening stroll weather in {city}? 🚶",
        f"The city lights are starting to twinkle in {city}! 💡",
        f"Date night in {city}? 💕",
        f"Rush hour traffic clearing up in {city}! 🚗",
        f"The workday is winding down in {city}! 📝",
        f"Time for some evening entertainment in {city}! 🎭",
        f"Time to cook dinner in {city}! 👨‍🍳",
        f"Golden hour photography in {city}! 📷",
        f"Winding down in {city}... 🛋️",
        f"Time for some evening exercise in {city}! 🏋️‍♀️",
        f"The day is coming to an end in {city}! 🌆",
        f"Perfect time for a walk in {city}! 🚶",
        f"Time to catch up with friends in {city}! 👥",
        f"Evening breeze in {city} feels nice! 🌬️",
        f"Cozy evening vibes in {city}! 🕯️",
        f"Time to unwind with a good book in {city}! 📚",
        f"Twilight magic in {city}! ✨",
        f"Time to reflect on the day in {city}! 💭",
        f"Perfect time for a romantic dinner in {city}! 🥂",
        f"Evening meditation time in {city}! 🧘‍♂️",
        f"Time to call it a day in {city}! 📞",
        f"The evening glow in {city} is stunning! 🌅",
        f"Time for some self-care in {city}! 💆‍♀️",
    ]
    if 5 <= hour < 12:
        return morning_jokes[hour % len(morning_jokes)]
    elif 12 <= hour < 17:
        return afternoon_jokes[hour % len(afternoon_jokes)]
    elif 17 <= hour < 21:
        return evening_jokes[hour % len(evening_jokes)]
    else:
        return night_jokes[hour % len(night_jokes)]
