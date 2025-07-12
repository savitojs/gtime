#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CLI entry point for Global Time Utility (gtime)
This module provides the command line interface for the Global Time Utility (gtime) application,
allowing users to view current times in various cities, manage favorites, and more.
"""

import sys
import os
import json
import datetime
from pathlib import Path
from typing import List, Tuple, Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.box import ROUNDED
import random
import time

from .core import (
    load_favorites, save_favorites, get_city_by_name, fuzzy_search_city, suggest_cities,
    get_time_emoji, get_greeting, get_funny_footer
)
from .data import CITY_DB

console = Console()
FAV_FILE = Path.home() / ".gtime_favorites.json"

def print_city_time(city, country, tz, emoji, meeting_time: Optional[datetime.datetime] = None):
    from .core import ZoneInfo
    now = datetime.datetime.now(ZoneInfo(tz))
    dt = meeting_time.astimezone(ZoneInfo(tz)) if meeting_time else now
    hour = dt.hour
    emoji_time = get_time_emoji(hour)
    greeting = get_greeting(hour)
    footer = get_funny_footer(city, hour)
    offset = dt.utcoffset()
    if offset is not None:
        total_minutes = offset.total_seconds() / 60
        hours = int(total_minutes // 60)
        minutes = int(abs(total_minutes) % 60)
        sign = '+' if hours >= 0 else '-'
        offset_str = f'UTC{sign}{abs(hours)}' + (f':{minutes:02}' if minutes else '')
    else:
        offset_str = 'UTC?'
    table = Table(show_header=False, box=None)
    table.add_row(f"[bold cyan]{emoji} {city}, {country}[/bold cyan]")
    table.add_row(f"[green]{dt.strftime('%A, %B %d, %Y')}[/green]")
    table.add_row(f"[yellow]{dt.strftime('%I:%M %p')} {emoji_time}  ([white]{offset_str}[/white])[/yellow]")
    table.add_row("")
    table.add_row(f"[italic magenta]{footer}[/italic magenta]")
    console.print(Panel(table, title=f"{greeting}!", expand=False))

def print_favorites(favs: List[str], meeting_time: Optional[datetime.datetime] = None):
    from .core import ZoneInfo
    if not favs:
        console.print("[red]No favorite cities set. Use 'gtime add <city>' to add one.[/red]")
        console.print("[yellow]Use 'gtime <city>' to search one and 'gtime --help' for more info[/yellow]")
        return
    banner = Text("🌍 GLOBAL TIME FAVORITES 🌍", style="bold magenta on cyan", justify="center")
    console.print(Align.center(banner))
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
        if meeting_time:
            # Convert meeting time (assumed to be in local timezone) to the city's timezone
            local_dt = datetime.datetime.now().astimezone()
            local_tz = local_dt.tzinfo
            meeting_time_local = meeting_time.replace(tzinfo=local_tz)
            dt = meeting_time_local.astimezone(ZoneInfo(tz))
        else:
            dt = now
        hour = dt.hour
        emoji_time = get_time_emoji(hour)
        phase = get_greeting(hour)
        offset = dt.utcoffset()
        if offset is not None:
            total_minutes = offset.total_seconds() / 60
            hours = int(total_minutes // 60)
            minutes = int(abs(total_minutes) % 60)
            sign = '+' if hours >= 0 else '-'
            offset_str = f'UTC{sign}{abs(hours)}' + (f':{minutes:02}' if minutes else '')
        else:
            offset_str = 'UTC?'
        table.add_row(
            emoji, f"{city}, {country}", f"{dt.strftime('%a, %b %d %I:%M %p')}", f"{emoji_time} {phase}", offset_str
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
    panel = Panel(table, title="[bold magenta]Your Favorite Cities[/bold magenta]", subtitle=f"[italic cyan]{footer}", border_style="bright_magenta", box=ROUNDED)
    console.print(panel)

def print_compare(cities: List[str]):
    from .core import ZoneInfo
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
        offset = now.utcoffset()
        if offset is not None:
            total_minutes = offset.total_seconds() / 60
            hours = int(total_minutes // 60)
            minutes = int(abs(total_minutes) % 60)
            sign = '+' if hours >= 0 else '-'
            offset_str = f'UTC{sign}{abs(hours)}' + (f':{minutes:02}' if minutes else '')
        else:
            offset_str = 'UTC?'
        table.add_row(
            emoji, f"{city}, {country}", f"{now.strftime('%a, %b %d %I:%M %p')}", f"{emoji_time} {phase}", offset_str
        )
    console.print(table)

def watch_mode(func, *args, **kwargs):
    try:
        while True:
            os.system('clear')
            func(*args, **kwargs)

            for seconds_left in range(60, 0, -1):
                console.print(f"[dim]Press Ctrl+C to exit watch mode. Next refresh in {seconds_left} seconds...[/dim]", end="\r")
                time.sleep(1)

    except KeyboardInterrupt:
        console.print("\n[green]Exited watch mode.[/green]")

def parse_meeting_time(args: List[str]) -> Tuple[Optional[datetime.datetime], Optional[str]]:
    if "at" in args:
        idx = args.index("at")
    elif "on" in args:
        idx = args.index("on")
    else:
        return None, None
    time_str = " ".join(args[idx+1:])
    today = datetime.datetime.now()
    
    timezone_spec = None
    timezone_info = None
    timezone_aliases = {
        'UTC': ('UTC', 'Coordinated Universal Time'),
        'GMT': ('UTC', 'Greenwich Mean Time'),
        'EST': ('America/New_York', 'Eastern Standard Time'),
        'EDT': ('America/New_York', 'Eastern Daylight Time'), 
        'CST': ('America/Chicago', 'Central Standard Time'),
        'CDT': ('America/Chicago', 'Central Daylight Time'),
        'MST': ('America/Denver', 'Mountain Standard Time'),
        'MDT': ('America/Denver', 'Mountain Daylight Time'),
        'PST': ('America/Los_Angeles', 'Pacific Standard Time'),
        'PDT': ('America/Los_Angeles', 'Pacific Daylight Time'),
        'CET': ('Europe/Paris', 'Central European Time'),
        'CEST': ('Europe/Paris', 'Central European Summer Time'),
        'JST': ('Asia/Tokyo', 'Japan Standard Time'),
        'IST': ('Asia/Kolkata', 'India Standard Time'),
    }
    
    parts = time_str.split()
    if len(parts) > 1 and parts[-1].upper() in timezone_aliases:
        tz_abbr = parts[-1].upper()
        timezone_spec, tz_name = timezone_aliases[tz_abbr]
        timezone_info = f"{tz_name} ({tz_abbr})"
        time_str = " ".join(parts[:-1])
    
    formats = [
        "%I:%M %p",    # 12-hour format with AM/PM (e.g., "3:30 PM")
        "%H:%M",       # 24-hour format (e.g., "15:30")
        "%I %p",       # Hour only with AM/PM (e.g., "3 PM")
        "%H",          # Hour only 24-hour (e.g., "15")
    ]
    
    for fmt in formats:
        try:
            dt = datetime.datetime.strptime(time_str, fmt)
            meeting_time = today.replace(hour=dt.hour, minute=dt.minute, second=0, microsecond=0)
            
            if timezone_spec:
                from .core import ZoneInfo
                specified_tz = ZoneInfo(timezone_spec)
                meeting_time_in_tz = meeting_time.replace(tzinfo=specified_tz)
                local_meeting_time = meeting_time_in_tz.astimezone()
                meeting_time = local_meeting_time.replace(tzinfo=None)
            
            return meeting_time, timezone_info
        except (ValueError, Exception):
            continue
    
    return None, None

def print_help():
    help_text = """
[bold cyan]gtime - Global Time Utility[/bold cyan]

[bold yellow]Usage:[/bold yellow]
  gtime [command] [arguments]
  gtime <city name>

[bold yellow]Commands:[/bold yellow]
  [green]add <city>[/green]         Add a city to your favorites
  [green]remove <city>[/green]      Remove a city from your favorites
  [green]list[/green]               List your favorite cities and their current times
  [green]list --watch[/green]       Watch mode: continuously refresh your favorites list every 60 seconds
  [green]meeting at / on <time>[/green]  Show favorite cities' times for a meeting (e.g. 'meeting at 10:00 AM', 'meeting at 15:30 UTC', or 'meeting on 3 PM EST')
  [green]compare <city1> <city2> ...[/green]  Compare times for multiple cities
  [green]compare <city1> <city2> ... --watch[/green]  Watch mode: continuously refresh city comparison
  [green]watch[/green]              Same as 'list --watch' - watch your favorites in real-time
  [green]<city name>[/green]        Show the current time for any city (fuzzy search supported)
  [green]-h, --help[/green]         Show this help message

[bold yellow]Watch Mode:[/bold yellow]
  Use [green]--watch[/green] with list or compare commands, or use [green]watch[/green] alone to continuously 
  refresh the display every 60 seconds with a live countdown timer. Press Ctrl+C to exit.
"""
    console.print(help_text)

def main():
    args = sys.argv[1:]
    if args and args[0] in ('-h', '--help'):
        print_help()
        return
    favs = load_favorites()
    local_hour = datetime.datetime.now().hour
    greeting = get_greeting(local_hour)
    try:
        user = os.getlogin()
    except Exception:
        user = "user"
    console.print(f"[bold blue]{greeting}, {user}! Welcome to Global Time Utility 🌐[/bold blue]")

    if not args:
        print_favorites(favs)
        return

    cmd = args[0].lower()

    if cmd == "watch" or (cmd == "list" and len(args) > 1 and args[1] == "--watch"):
        watch_mode(print_favorites, favs)
        return
    if cmd == "compare" and (len(args) > 2 and args[-1] == "--watch"):
        watch_mode(print_compare, [c for c in args[1:-1]])
        return

    if cmd == "add" and len(args) > 1:
        city_info = get_city_by_name(" ".join(args[1:]))
        if city_info:
            city, *_ = city_info
            if city not in favs:
                favs.append(city)
                save_favorites(favs)
                console.print(f"[green]Added {city} to favorites![/green]")
            else:
                console.print(f"[yellow]{city} is already in favorites.[/yellow]")
        else:
            console.print("[red]City not found.[/red]")
            suggestions = suggest_cities(" ".join(args[1:]))
            if suggestions:
                console.print(f"[yellow]Did you mean:[/yellow] {', '.join(suggestions)}")
        return

    if cmd == "remove" and len(args) > 1:
        city = " ".join(args[1:])
        if city in favs:
            favs.remove(city)
            save_favorites(favs)
            console.print(f"[green]Removed {city} from favorites.[/green]")
        else:
            console.print(f"[yellow]{city} is not in favorites.[/yellow]")
        return

    if cmd == "list":
        print_favorites(favs)
        return

    if cmd == "meeting":
        if len(args) == 1:
            print_favorites(favs)
            return
        meeting_time, timezone_info = parse_meeting_time(args)
        if meeting_time is None:
            console.print("[red]Invalid meeting command. Use: 'meeting at/on <time>' (e.g. 'meeting at 10:00 AM', 'meeting at 15:30 UTC', or 'meeting on 3 PM EST').[/red]")
            console.print("[yellow]See 'gtime -h' for help.[/yellow]")
            return
        print_favorites(favs, meeting_time)
        if timezone_info:
            console.print(f"\n[dim]✓ Meeting time converted from {timezone_info}[/dim]")
        return

    if cmd == "compare" and len(args) > 1:
        not_found = []
        found = []
        for name in args[1:]:
            if name == "--watch":
                continue
            city_info = get_city_by_name(name)
            if city_info:
                found.append(city_info)
            else:
                not_found.append(name)
        if not_found:
            for nf in not_found:
                console.print(f"[red]City not found:[/red] {nf}")
                suggestions = suggest_cities(nf)
                if suggestions:
                    console.print(f"[yellow]Did you mean:[/yellow] {', '.join(suggestions)}")
        if found:
            print_compare([c[0] for c in found])
        else:
            console.print("[red]No valid cities to compare.[/red]")
        return

    city_info = get_city_by_name(" ".join(args))
    if city_info:
        print_city_time(*city_info)
    else:
        console.print("[red]Invalid command or city not found. See 'gtime -h' for help.[/red]")
        suggestions = suggest_cities(" ".join(args))
        if suggestions:
            console.print(f"[yellow]Did you mean:[/yellow] {', '.join(suggestions)}")

if __name__ == "__main__":
    main()
