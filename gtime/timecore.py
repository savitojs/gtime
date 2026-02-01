#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Time and timezone helpers for Global Time Utility (gtime).
"""

import datetime
import os
from typing import List, Optional, Tuple

from zoneinfo import ZoneInfo


def _is_terminal_compatible() -> bool:
    """Check if the current terminal supports complex emojis with variation selectors."""
    term_program = os.environ.get("TERM_PROGRAM", "").lower()
    term = os.environ.get("TERM", "").lower()

    problematic_terminals = {"kitty", "ghostty", "terminal.app"}

    if term_program in problematic_terminals:
        return False

    # Check TERM environment variable for kitty
    if "kitty" in term:
        return False

    # Default to compatible for most terminals
    return True


def _get_safe_emoji(emoji_with_variation: str, fallback_emoji: str) -> str:
    """Get a safe emoji for the current terminal."""
    if _is_terminal_compatible():
        return emoji_with_variation
    return fallback_emoji


def get_time_emoji(hour: int) -> str:
    if 5 <= hour < 12:
        return "🌅"
    if 12 <= hour < 17:
        # Use safe emoji for sun - some terminals have issues with ☀️ (U+2600 + U+FE0F)
        return _get_safe_emoji("☀️", "🌞")
    if 17 <= hour < 21:
        return "🌆"
    return "🌙"


def get_greeting(hour: int) -> str:
    if 5 <= hour < 12:
        return "Good morning"
    if 12 <= hour < 17:
        return "Good afternoon"
    if 17 <= hour < 21:
        return "Good evening"
    return "Good night"


def get_work_label(hour: int) -> str:
    if 0 <= hour < 6:
        return "Sleep"
    if 6 <= hour < 9:
        return "Early"
    if 9 <= hour < 12:
        return "Work"
    if 12 <= hour < 14:
        return "Lunch"
    if 14 <= hour < 18:
        return "Work"
    if 18 <= hour < 22:
        return "Off"
    return "Late"


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
    if 12 <= hour < 17:
        return afternoon_jokes[hour % len(afternoon_jokes)]
    if 17 <= hour < 21:
        return evening_jokes[hour % len(evening_jokes)]
    return night_jokes[hour % len(night_jokes)]


def format_utc_offset(dt: datetime.datetime) -> str:
    offset = dt.utcoffset()
    if offset is not None:
        total_minutes = offset.total_seconds() / 60
        hours = int(total_minutes // 60)
        minutes = int(abs(total_minutes) % 60)
        sign = "+" if hours >= 0 else "-"
        return f"UTC{sign}{abs(hours)}" + (f":{minutes:02}" if minutes else "")
    return "UTC?"


def format_time_delta(base_dt: datetime.datetime, target_dt: datetime.datetime) -> str:
    base_offset = base_dt.utcoffset()
    target_offset = target_dt.utcoffset()
    if base_offset is None or target_offset is None:
        return "?"
    delta_minutes = int((target_offset - base_offset).total_seconds() // 60)
    sign = "+" if delta_minutes >= 0 else "-"
    minutes = abs(delta_minutes)
    hours, mins = divmod(minutes, 60)
    if mins:
        return f"{sign}{hours}:{mins:02}"
    return f"{sign}{hours}"


def to_local_aware(dt: datetime.datetime) -> datetime.datetime:
    if dt.tzinfo is not None:
        return dt
    local_tz = datetime.datetime.now().astimezone().tzinfo
    return dt.replace(tzinfo=local_tz)


def convert_meeting_time(meeting_time: datetime.datetime, tz_name: str) -> datetime.datetime:
    local_aware = to_local_aware(meeting_time)
    return local_aware.astimezone(ZoneInfo(tz_name))


def parse_meeting_time(args: List[str]) -> Tuple[Optional[datetime.datetime], Optional[str]]:
    if "at" in args:
        idx = args.index("at")
    elif "on" in args:
        idx = args.index("on")
    else:
        return None, None
    time_str = " ".join(args[idx + 1:])
    today = datetime.datetime.now()

    timezone_spec = None
    timezone_info = None
    # Common abbreviations only; keep this list intentionally small and well-known.
    timezone_aliases = {
        "UTC": ("UTC", "Coordinated Universal Time"),
        "GMT": ("UTC", "Greenwich Mean Time"),
        "BST": ("Europe/London", "British Summer Time"),
        "EST": ("America/New_York", "Eastern Standard Time"),
        "EDT": ("America/New_York", "Eastern Daylight Time"),
        "CST": ("America/Chicago", "Central Standard Time"),
        "CDT": ("America/Chicago", "Central Daylight Time"),
        "MST": ("America/Denver", "Mountain Standard Time"),
        "MDT": ("America/Denver", "Mountain Daylight Time"),
        "PST": ("America/Los_Angeles", "Pacific Standard Time"),
        "PDT": ("America/Los_Angeles", "Pacific Daylight Time"),
        "AKST": ("America/Anchorage", "Alaska Standard Time"),
        "AKDT": ("America/Anchorage", "Alaska Daylight Time"),
        "HST": ("Pacific/Honolulu", "Hawaii Standard Time"),
        "CET": ("Europe/Paris", "Central European Time"),
        "CEST": ("Europe/Paris", "Central European Summer Time"),
        "EET": ("Europe/Athens", "Eastern European Time"),
        "EEST": ("Europe/Athens", "Eastern European Summer Time"),
        "JST": ("Asia/Tokyo", "Japan Standard Time"),
        "IST": ("Asia/Kolkata", "India Standard Time"),
        "AEST": ("Australia/Sydney", "Australian Eastern Standard Time"),
        "AEDT": ("Australia/Sydney", "Australian Eastern Daylight Time"),
        "ACST": ("Australia/Adelaide", "Australian Central Standard Time"),
        "ACDT": ("Australia/Adelaide", "Australian Central Daylight Time"),
        "AWST": ("Australia/Perth", "Australian Western Standard Time"),
        "NZST": ("Pacific/Auckland", "New Zealand Standard Time"),
        "NZDT": ("Pacific/Auckland", "New Zealand Daylight Time"),
    }

    parts = time_str.split()
    if len(parts) > 1 and parts[-1].upper() in timezone_aliases:
        tz_abbr = parts[-1].upper()
        timezone_spec, tz_name = timezone_aliases[tz_abbr]
        timezone_info = f"{tz_name} ({tz_abbr})"
        time_str = " ".join(parts[:-1])

    formats = [
        "%I:%M %p",  # 12-hour format with AM/PM (e.g., "3:30 PM")
        "%H:%M",  # 24-hour format (e.g., "15:30")
        "%I %p",  # Hour only with AM/PM (e.g., "3 PM")
        "%H",  # Hour only 24-hour (e.g., "15")
    ]

    for fmt in formats:
        try:
            dt = datetime.datetime.strptime(time_str, fmt)
            meeting_time = today.replace(hour=dt.hour, minute=dt.minute, second=0, microsecond=0)

            if timezone_spec:
                specified_tz = ZoneInfo(timezone_spec)
                meeting_time_in_tz = meeting_time.replace(tzinfo=specified_tz)
                local_meeting_time = meeting_time_in_tz.astimezone()
                meeting_time = local_meeting_time.replace(tzinfo=None)

            return meeting_time, timezone_info
        except (ValueError, Exception):
            continue

    return None, None
