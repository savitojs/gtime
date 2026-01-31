#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rendering helpers for Global Time Utility (gtime).
"""

import datetime
import random
from typing import List, Optional

from rich.box import ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .search import get_city_by_name
from .timecore import (
    ZoneInfo,
    convert_meeting_time,
    format_utc_offset,
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
    console.print(Panel(table, title=f"{greeting}!", expand=False))


def print_favorites(favs: List[str], meeting_time: Optional[datetime.datetime] = None):
    if not favs:
        console.print("[red]No favorite cities set. Use 'gtime add <city>' to add one.[/red]")
        console.print("[yellow]Use 'gtime <city>' to search one and 'gtime --help' for more info[/yellow]")
        return
    if meeting_time:
        local_meeting = to_local_aware(meeting_time)
        console.print(
            f"[dim]Meeting time (local): {_format_local_time(local_meeting, long_format=True)}[/dim]"
        )
    table = Table(title=None, show_lines=True, box=ROUNDED, expand=False)
    table.add_column("Flag", style="bold", justify="center")
    table.add_column("City", style="bold cyan")
    table.add_column("Local Time", style="green")
    table.add_column("Phase", style="magenta")
    table.add_column("UTC Offset", style="yellow")
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
        table.add_row(
            emoji,
            f"{city}, {country}",
            _format_local_time(dt, long_format=meeting_time is not None),
            f"{emoji_time} {phase}",
            offset_str,
        )
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
    console.print(panel)


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
    table = Table(title="[bold magenta]Global Time Compare[/bold magenta]", show_lines=True, box=ROUNDED, expand=False)
    table.add_column("Flag", style="bold", justify="center")
    table.add_column("City", style="bold cyan")
    table.add_column("Local Time", style="green")
    table.add_column("Phase", style="magenta")
    table.add_column("UTC Offset", style="yellow")
    for city, country, tz, emoji in found:
        now = datetime.datetime.now(ZoneInfo(tz))
        hour = now.hour
        emoji_time = get_time_emoji(hour)
        phase = get_greeting(hour)
        offset_str = format_utc_offset(now)
        table.add_row(
            emoji,
            f"{city}, {country}",
            f"{now.strftime('%a, %b %d %I:%M %p')}",
            f"{emoji_time} {phase}",
            offset_str,
        )
    console.print(table)
