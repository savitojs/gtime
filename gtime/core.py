#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Core logic for Global Time Utility (gtime) lookup, fuzzy search, helpers
"""

import datetime
import json
import os
from pathlib import Path
from typing import List, Tuple, Optional
import random
from functools import lru_cache

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from pytz import timezone as ZoneInfo

from .data import CITY_DB, COUNTRY_CAPITALS

FAV_FILE = Path.home() / ".gtime_favorites.json"

def _is_terminal_compatible() -> bool:
    """Check if the current terminal supports complex emojis with variation selectors."""
    term_program = os.environ.get('TERM_PROGRAM', '').lower()
    term = os.environ.get('TERM', '').lower()

    problematic_terminals = {'kitty', 'ghostty', 'terminal.app'}

    if term_program in problematic_terminals:
        return False

    # Check TERM environment variable for kitty
    if 'kitty' in term:
        return False

    # Default to compatible for most terminals
    return True

def _get_safe_emoji(emoji_with_variation: str, fallback_emoji: str) -> str:
    """Get a safe emoji for the current terminal."""
    if _is_terminal_compatible():
        return emoji_with_variation
    else:
        return fallback_emoji

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
        json.dump(favs, f, indent=2)

def _get_city_names():
    names = [f"{city} ({country})" for city, country, _, _ in CITY_DB]
    name_to_idx = {name: i for i, name in enumerate(names)}
    return names, name_to_idx

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

    # Third priority: exact country match (case insensitive)
    # If searching for a country name, return the capital city
    for city, country, tz, emoji in CITY_DB:
        if country.lower() == query_lower:
            # Check if we have a specific capital for this country
            capital = COUNTRY_CAPITALS.get(country)
            if capital:
                # Find the capital city in the database
                for cap_city, cap_country, cap_tz, cap_emoji in CITY_DB:
                    if cap_city == capital and cap_country == country:
                        return (cap_city, cap_country, cap_tz, cap_emoji)
            # If no capital mapping or capital not found, return the first city
            return (city, country, tz, emoji)

    # Fourth priority: country starts with or contains query (case insensitive)
    for city, country, tz, emoji in CITY_DB:
        if country.lower().startswith(query_lower) or query_lower in country.lower():
            # Check if we have a specific capital for this country
            capital = COUNTRY_CAPITALS.get(country)
            if capital:
                # Find the capital city in the database
                for cap_city, cap_country, cap_tz, cap_emoji in CITY_DB:
                    if cap_city == capital and cap_country == country:
                        return (cap_city, cap_country, cap_tz, cap_emoji)
            # If no capital mapping or capital not found, return the first city
            return (city, country, tz, emoji)

    # Fifth priority: substring match (case insensitive) - only for queries with 5+ characters
    # This avoids false matches like "usa" matching "Busan"
    if len(query) >= 5:
        for name in names:
            city_name = name.split(" (")[0].lower()
            if query_lower in city_name:
                idx = name_to_idx[name]
                return CITY_DB[idx]

    # Sixth priority: fuzzy match on city names only (not including country)
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

    # First, check if the query exactly matches a country name
    query_lower = city_name.lower()
    country_matches = []
    for city, country, tz, emoji in CITY_DB:
        if country.lower() == query_lower:
            country_matches.append(f"{city} ({country})")

    # If we found exact country matches, return them
    if country_matches:
        return country_matches[:3]

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

    # If we don't have good city suggestions, try partial country matches
    if not suggestions or (suggestions and max(score for _, score in matches) < 60):
        # Check if query partially matches any country name
        partial_country_matches = []
        for city, country, tz, emoji in CITY_DB:
            if (country.lower().startswith(query_lower) or
                query_lower in country.lower()):
                partial_country_matches.append(f"{city} ({country})")

        # Add up to 3 cities from matching countries
        if partial_country_matches:
            suggestions.extend(partial_country_matches[:3])

    return suggestions

def get_time_emoji(hour: int) -> str:
    if 5 <= hour < 12:
        return "🌅"
    elif 12 <= hour < 17:
        # Use safe emoji for sun - some terminals have issues with ☀️ (U+2600 + U+FE0F)
        return _get_safe_emoji("☀️", "🌞")
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
        f"Sweet dreams, {city}! 😴",
        f"It's late in {city}. Don't let the bed bugs bite! 🛌",
        f"Time to count sheep in {city}! 🐑",
        f"The night owls in {city} are just getting started! 🦉",
        f"Midnight snack time in {city}? 🍕",
        f"The stars are shining bright over {city}! ✨",
        f"Sleepy time in {city}. Rest well! 😴",
        f"Night shift workers in {city}, we see you! 👷‍♂️",
        f"The moon is beautiful in {city} tonight! 🌙",
        f"Time to recharge in {city}! 🔋",
        f"Late night coding session in {city}? 💻",
        f"The city never sleeps in {city}! 🌃",
        f"Dreaming of tomorrow in {city}! 💭",
        f"Night time is the right time in {city}! 🎵",
        f"Insomniacs unite in {city}! ☕",
        f"The witching hour in {city}! 🧙‍♀️",
        f"Time for some deep thoughts in {city}! 🤔",
        f"Night photography time in {city}! 📸",
        f"The city lights are magical in {city}! 💡",
        f"Time to embrace the darkness in {city}! 🌑",
        f"Night shift snacks in {city}? 🌮",
        f"The moon is your nightlight in {city}! 🌙",
        f"Time for some late-night reading in {city}! 📚",
        f"Night owls of {city}, this is your time! 🦉",
        f"The world is quiet in {city}... shh! 🤫",
        f"Time to let your dreams run wild in {city}! 🌟",
        f"Night time serenity in {city}! 🧘‍♂️",
        f"The darkness is your friend in {city}! 🌑",
    ]

    # Get safe sun emoji for use in messages
    safe_sun_emoji = _get_safe_emoji("☀️", "🌞")

    morning_jokes = [
        f"Rise and shine, {city}! {safe_sun_emoji}",
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
        f"The sun is at its peak in {city}! {safe_sun_emoji}",
        f"Productivity mode activated in {city}! 📈",
        f"Ice cream weather in {city}? 🍦",
        f"Working hard or hardly working in {city}? 💼",
        f"The afternoon hustle in {city} is real! 🏃‍♀️",
        f"Time flies when you're having fun in {city}! ⏰",
        f"Midday energy boost needed in {city}? ⚡",
        f"The perfect time for outdoor activities in {city}! 🌳",
        f"Sunshine and productivity in {city}! 🌻",
        f"Take a refreshing break in {city}! 🌞",
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
        f"Sunshine therapy in {city}! {safe_sun_emoji}",
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
