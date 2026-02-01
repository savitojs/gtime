#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rendering helpers for Global Time Utility (gtime).
"""

import datetime
import random
from typing import List, Optional

from rich.align import Align
from rich.box import ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

from .search import get_city_by_name
from .timecore import (
    ZoneInfo,
    convert_meeting_time,
    format_utc_offset,
    format_time_delta,
    get_funny_footer,
    get_greeting,
    get_time_emoji,
    to_local_aware,
)

console = Console()


def _format_local_time(dt: datetime.datetime, long_format: bool = False) -> str:
    if long_format:
        return dt.strftime("%A, %B %d, %Y %I:%M %p")
    return dt.strftime("%a, %b %d %I:%M %p")


def _format_day_shift(base_dt: datetime.datetime, target_dt: datetime.datetime) -> str:
    day_delta = (target_dt.date() - base_dt.date()).days
    if day_delta == 0:
        return ""
    if day_delta > 0:
        return f"+{day_delta} day" if day_delta == 1 else f"+{day_delta} days"
    return f"{day_delta} day" if day_delta == -1 else f"{day_delta} days"


def print_city_time(city, country, tz, emoji, meeting_time: Optional[datetime.datetime] = None):
    now = datetime.datetime.now(ZoneInfo(tz))
    dt = convert_meeting_time(meeting_time, tz) if meeting_time else now
    hour = dt.hour
    emoji_time = get_time_emoji(hour)
    greeting = get_greeting(hour)
    footer = get_funny_footer(city, hour)
    offset_str = format_utc_offset(dt)
    table = Table(show_header=False, box=None)
    table.add_row(f"[bold cyan]{emoji} {city}, {country}[/bold cyan]")
    table.add_row(f"[green]{dt.strftime('%A, %B %d, %Y')}[/green]")
    table.add_row(f"[yellow]{dt.strftime('%I:%M %p')} {emoji_time}  ([white]{offset_str}[/white])[/yellow]")
    table.add_row("")
    table.add_row(f"[italic magenta]{footer}[/italic magenta]")
    console.print(Align.center(Panel(table, title=f"{greeting}!", expand=False)))


def print_favorites(favs: List[str], meeting_time: Optional[datetime.datetime] = None):
    if not favs:
        console.print("[red]No favorite cities set. Use 'gtime add <city>' to add one.[/red]")
        console.print("[yellow]Use 'gtime <city>' to search one and 'gtime --help' for more info[/yellow]")
        return
    if meeting_time:
        local_meeting = to_local_aware(meeting_time)
        console.print(
            f"[bold cyan]Meeting: {_format_local_time(local_meeting, long_format=False)} (local)[/bold cyan]",
            justify="center",
        )
    base_local = (
        to_local_aware(meeting_time)
        if meeting_time
        else datetime.datetime.now().astimezone()
    )
    rows = []
    for fav in favs:
        city_info = get_city_by_name(fav)
        if not city_info:
            continue
        city, country, tz, emoji = city_info
        now = datetime.datetime.now(ZoneInfo(tz))
        dt = convert_meeting_time(meeting_time, tz) if meeting_time else now
        hour = dt.hour
        emoji_time = get_time_emoji(hour)
        phase = get_greeting(hour)
        offset_str = format_utc_offset(dt)
        delta_str = format_time_delta(base_local, dt)
        local_time = _format_local_time(dt, long_format=False)
        day_shift = _format_day_shift(base_local, dt)
        rows.append(
            {
                "emoji": emoji,
                "city": f"{city}, {country}",
                "local_time": f"{local_time} ({offset_str})",
                "day_shift": day_shift,
                "delta": delta_str,
                "phase": f"{emoji_time} {phase}",
            }
        )
    show_day = any(row["day_shift"] for row in rows)
    table = Table(title=None, show_lines=True, box=ROUNDED, expand=False)
    table.add_column("Flag", style="bold", justify="center")
    table.add_column("City", style="bold cyan")
    table.add_column("Local Time (UTC)", style="green")
    if show_day:
        table.add_column("Day", style="blue")
    table.add_column("Δ Local", style="cyan")
    table.add_column("Phase", style="magenta")
    for row in rows:
        cells = [
            row["emoji"],
            row["city"],
            row["local_time"].replace(" (", " • ").replace(")", ""),
        ]
        if show_day:
            cells.append(row["day_shift"] if row["day_shift"] else "[dim]same day[/dim]")
        cells.extend([row["delta"], row["phase"]])
        table.add_row(*cells)
    fun_facts = [
        "Did you know? There are 24 time zones in the world! 🌐",
        "UTC stands for Universal Time Coordinated! 🕒",
        "Some countries have 30 or 45 minute offsets! ⏰",
        "The world is a beautiful place—enjoy every timezone! 🌏",
        "Time flies like an arrow. Fruit flies like a banana! 🍌",
        "It's always 5 o'clock somewhere! 🍹",
        "China uses only one time zone despite spanning 5 geographical zones! 🇨🇳",
        "Russia has 11 time zones - the most of any country! 🇷🇺",
        "The International Date Line isn't straight - it zigzags! 📅",
        "Some Pacific islands are a full day ahead of others! 🏝️",
        "Nepal has a unique +5:45 UTC offset - not a round hour! 🏔️",
        "Australia's Lord Howe Island has a 30-minute daylight saving! ⏰",
        "The North and South Poles technically have all time zones! 🧭",
        "France has the most time zones (12) due to overseas territories! 🇫🇷",
        "Arizona (mostly) doesn't observe daylight saving time! 🌵",
        "Time zones were invented by railway companies! 🚂",
        "Before time zones, every city had its own local time! 🏙️",
        "The first country to see the new year is Kiribati! 🎉",
        "GMT and UTC are almost the same but not exactly! ⏱️",
        "Some countries have changed time zones for political reasons! 🗳️",
        "India uses a single time zone despite spanning 2,900+ km east to west. 🇮🇳",
        "There are time zones with 15-minute offsets, like UTC+12:45 in New Zealand’s Chatham Islands. ⏲️",
        "The UTC offset can change with daylight saving time, even in the same city. 🌞",
        "Not all countries observe daylight saving time. 🗓️",
        "The International Date Line roughly follows the 180° longitude. 🧭",
        "Some countries have moved time zones for political or economic reasons. 🗺️",
        "Half-hour time zones are common in places like India and Australia. ⏰",
        "UTC is based on atomic time, not the Sun. ⚛️",
        "Antarctica uses multiple time zones based on research stations. 🧊",
        "Local solar noon rarely matches 12:00 PM on the clock. ☀️",
        "Daylight saving time can shift clocks by one hour in summer. ⏳",
        "Time zones help keep noon close to when the Sun is highest in the sky. 🌤️",
        "Some islands use time zones to stay aligned with trading partners. 🏝️",
        "The Unix epoch starts at 1970-01-01 00:00:00 UTC. 🧮",
    ]
    footer = random.choice(fun_facts)
    panel = Panel(
        table,
        title="[bold magenta]Your Favorite Cities[/bold magenta]",
        subtitle=f"[italic cyan]{footer}",
        border_style="bright_magenta",
        box=ROUNDED,
        expand=False,
    )
    panel_width = console.measure(panel).maximum
    line_width = min(panel_width, console.width)
    left_pad = max((console.width - line_width) // 2, 0)
    console.print("[dim]" + (" " * left_pad) + ("─" * line_width) + "[/dim]")
    console.print(Align.center(panel))


def print_compare(cities: List[str]):
    found = []
    for name in cities:
        city_info = get_city_by_name(name)
        if city_info:
            found.append(city_info)
        else:
            console.print(f"[red]City not found:[/red] {name}")
    if not found:
        console.print("[red]No valid cities to compare.[/red]")
        return
    base_local = datetime.datetime.now().astimezone()
    rows = []
    for city, country, tz, emoji in found:
        now = datetime.datetime.now(ZoneInfo(tz))
        hour = now.hour
        emoji_time = get_time_emoji(hour)
        phase = get_greeting(hour)
        offset_str = format_utc_offset(now)
        delta_str = format_time_delta(base_local, now)
        local_time = _format_local_time(now, long_format=False)
        day_shift = _format_day_shift(base_local, now)
        rows.append(
            {
                "emoji": emoji,
                "city": f"{city}, {country}",
                "local_time": f"{local_time} ({offset_str})",
                "day_shift": day_shift,
                "delta": delta_str,
                "phase": f"{emoji_time} {phase}",
            }
        )
    show_day = any(row["day_shift"] for row in rows)
    table = Table(title=None, show_lines=True, box=ROUNDED, expand=False)
    table.add_column("Flag", style="bold", justify="center")
    table.add_column("City", style="bold cyan")
    table.add_column("Local Time (UTC)", style="green")
    if show_day:
        table.add_column("Day", style="blue")
    table.add_column("Δ Local", style="cyan")
    table.add_column("Phase", style="magenta")
    for row in rows:
        cells = [
            row["emoji"],
            row["city"],
            row["local_time"].replace(" (", " • ").replace(")", ""),
        ]
        if show_day:
            cells.append(row["day_shift"] if row["day_shift"] else "[dim]same day[/dim]")
        cells.extend([row["delta"], row["phase"]])
        table.add_row(*cells)
    fun_facts = [
        "Did you know? There are 24 time zones in the world! 🌐",
        "UTC stands for Universal Time Coordinated! 🕒",
        "Some countries have 30 or 45 minute offsets! ⏰",
        "The world is a beautiful place—enjoy every timezone! 🌏",
        "Time flies like an arrow. Fruit flies like a banana! 🍌",
        "It's always 5 o'clock somewhere! 🍹",
        "China uses only one time zone despite spanning 5 geographical zones! 🇨🇳",
        "Russia has 11 time zones - the most of any country! 🇷🇺",
        "The International Date Line isn't straight - it zigzags! 📅",
        "Some Pacific islands are a full day ahead of others! 🏝️",
        "Nepal has a unique +5:45 UTC offset - not a round hour! 🏔️",
        "Australia's Lord Howe Island has a 30-minute daylight saving! ⏰",
        "The North and South Poles technically have all time zones! 🧭",
        "France has the most time zones (12) due to overseas territories! 🇫🇷",
        "Arizona (mostly) doesn't observe daylight saving time! 🌵",
        "Time zones were invented by railway companies! 🚂",
        "Before time zones, every city had its own local time! 🏙️",
        "The first country to see the new year is Kiribati! 🎉",
        "GMT and UTC are almost the same but not exactly! ⏱️",
        "Some countries have changed time zones for political reasons! 🗳️",
        "India uses a single time zone despite spanning 2,900+ km east to west. 🇮🇳",
        "There are time zones with 15-minute offsets, like UTC+12:45 in New Zealand’s Chatham Islands. ⏲️",
        "The UTC offset can change with daylight saving time, even in the same city. 🌞",
        "Not all countries observe daylight saving time. 🗓️",
        "The International Date Line roughly follows the 180° longitude. 🧭",
        "Some countries have moved time zones for political or economic reasons. 🗺️",
        "Half-hour time zones are common in places like India and Australia. ⏰",
        "UTC is based on atomic time, not the Sun. ⚛️",
        "Antarctica uses multiple time zones based on research stations. 🧊",
        "Local solar noon rarely matches 12:00 PM on the clock. ☀️",
        "Daylight saving time can shift clocks by one hour in summer. ⏳",
        "Time zones help keep noon close to when the Sun is highest in the sky. 🌤️",
        "Some islands use time zones to stay aligned with trading partners. 🏝️",
        "The Unix epoch starts at 1970-01-01 00:00:00 UTC. 🧮",
    ]
    footer = random.choice(fun_facts)
    panel = Panel(
        table,
        title="[bold magenta]Global Time Compare[/bold magenta]",
        subtitle=f"[italic cyan]{footer}",
        border_style="bright_magenta",
        box=ROUNDED,
        expand=False,
    )
    panel_width = console.measure(panel).maximum
    line_width = min(panel_width, console.width)
    left_pad = max((console.width - line_width) // 2, 0)
    console.print("[dim]" + (" " * left_pad) + ("─" * line_width) + "[/dim]")
    console.print(Align.center(panel))
