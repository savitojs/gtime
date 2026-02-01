#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Command routing for Global Time Utility (gtime).
"""

import datetime
import os
import sys
import time
from typing import List, Optional

from .render import console, print_city_time, print_compare, print_favorites
from .search import get_city_by_name, suggest_cities
from .storage import load_favorites, save_favorites
from .timecore import format_utc_offset, get_greeting, parse_meeting_time


def _print_header():
    local_now = datetime.datetime.now().astimezone()
    local_hour = local_now.hour
    greeting = get_greeting(local_hour)
    try:
        user = os.getlogin()
    except Exception:
        user = "user"
    local_compact = local_now.strftime("%a, %b %d %I:%M %p")
    console.print(
        f"[bold blue]{greeting}, {user}![/bold blue] "
        f"[dim]• Local: {local_compact} ({format_utc_offset(local_now)})[/dim]",
        justify="center",
    )


def watch_mode(func, *args, **kwargs):
    try:
        while True:
            os.system("clear")
            _print_header()
            func(*args, **kwargs)

            for seconds_left in range(60, 0, -1):
                console.print(
                    "[dim]Press Ctrl+C to exit watch mode. Next refresh in "
                    f"{seconds_left} seconds...[/dim]",
                    end="\r",
                )
                time.sleep(1)

    except KeyboardInterrupt:
        console.print("\n[green]Exited watch mode.[/green]")


def print_help():
    help_text = """
[bold cyan]gtime[/bold cyan]  [dim]— Global Time Utility[/dim]
[dim]Global time, minus the global headache. Compare, watch, and plan in one go.[/dim]

[bold yellow]Usage:[/bold yellow]
  gtime [command] [arguments]
  gtime <city name>

[bold yellow]Commands:[/bold yellow]
  [green]add <city>...[/green] / [green]remove <city>...[/green]  Add or remove favorite cities
  [green]meeting at / on <time>[/green]  Show favorite cities' times for a meeting (e.g. 'meeting at 10:00 AM', 'meeting at 15:30 UTC', or 'meeting on 3 PM EST')
  [green]compare <city1> <city2> ... [--watch][/green]  Compare times (use --watch for live refresh)
  [green]watch[/green]              Same as 'list --watch' - watch your favorites in real-time
  [green]<city name>[/green]        Show the current time for any city (fuzzy search supported)
  [green]-h, --help[/green]         Show this help message

[bold yellow]Watch Mode:[/bold yellow]
  Use [green]compare --watch[/green] for live comparison, or [green]watch[/green] / [green]--watch[/green]
  to continuously refresh your favorites every 60 seconds. Press Ctrl+C to exit.

[bold yellow]Notes:[/bold yellow]
  [green]Δ Local[/green] shows the time difference from your local timezone.
"""
    console.print(help_text)


def main(args: Optional[List[str]] = None):
    args = sys.argv[1:] if args is None else args
    if args and args[0] in ("-h", "--help"):
        print_help()
        return
    favs = load_favorites()
    _print_header()

    if not args:
        print_favorites(favs)
        return

    cmd = args[0].lower()

    if cmd == "watch":
        watch_mode(print_favorites, favs)
        return
    if cmd == "compare" and (len(args) > 2 and args[-1] == "--watch"):
        watch_mode(print_compare, [c for c in args[1:-1]])
        return

    if cmd == "add" and len(args) > 1:
        added_cities = []
        already_in_favs = []
        not_found = []

        for city_arg in args[1:]:
            city_info = get_city_by_name(city_arg)
            if city_info:
                city, *_ = city_info
                if city not in favs:
                    favs.append(city)
                    # Show mapping if user input differs from resolved city
                    if city_arg.lower() != city.lower():
                        added_cities.append(f"searched {city_arg}, added its capital city {city}")
                    else:
                        added_cities.append(city)
                else:
                    # Show mapping if user input differs from resolved city
                    if city_arg.lower() != city.lower():
                        already_in_favs.append(
                            f"searched {city_arg}, its capital city {city} is already in favorites"
                        )
                    else:
                        already_in_favs.append(city)
            else:
                not_found.append(city_arg)

        if added_cities:
            save_favorites(favs)
            for city_msg in added_cities:
                if city_msg.startswith("searched"):
                    console.print(f"[green]{city_msg}[/green]")
                else:
                    console.print(f"[green]Added {city_msg} to favorites![/green]")

        if already_in_favs:
            for city_msg in already_in_favs:
                if city_msg.startswith("searched"):
                    console.print(f"[yellow]{city_msg}[/yellow]")
                else:
                    console.print(f"[yellow]{city_msg} is already in favorites.[/yellow]")

        if not_found:
            for city_arg in not_found:
                console.print(f"[red]City not found:[/red] {city_arg}")
                suggestions = suggest_cities(city_arg)
                if suggestions:
                    console.print(f"[yellow]Did you mean:[/yellow] {', '.join(suggestions)}")

        return

    if cmd == "remove" and len(args) > 1:
        removed_cities = []
        not_in_favs = []

        for city_arg in args[1:]:
            if city_arg in favs:
                favs.remove(city_arg)
                removed_cities.append(city_arg)
            else:
                not_in_favs.append(city_arg)

        if removed_cities:
            save_favorites(favs)
            if len(removed_cities) == 1:
                console.print(f"[green]Removed {removed_cities[0]} from favorites.[/green]")
            else:
                console.print(
                    f"[green]Removed {len(removed_cities)} cities from favorites: "
                    f"{', '.join(removed_cities)}[/green]"
                )

        if not_in_favs:
            if len(not_in_favs) == 1:
                console.print(f"[yellow]{not_in_favs[0]} is not in favorites.[/yellow]")
            else:
                console.print(
                    f"[yellow]{len(not_in_favs)} cities not in favorites: "
                    f"{', '.join(not_in_favs)}[/yellow]"
                )

        return

    if cmd == "list":
        console.print("[red]The 'list' command has been removed.[/red]")
        console.print("[yellow]Use:[/yellow] gtime  |  gtime watch")
        return

    if cmd == "meeting":
        if len(args) == 1:
            print_favorites(favs)
            return
        meeting_time, timezone_info = parse_meeting_time(args)
        if meeting_time is None:
            console.print("[red]Invalid meeting command.[/red]")
            console.print("[yellow]Try:[/yellow] gtime meeting at \"10:00 AM\"  |  gtime meeting at \"15:30\" UTC")
            console.print("[yellow]Help:[/yellow] gtime -h")
            return
        print_favorites(favs, meeting_time)
        if timezone_info:
            console.print(
                f"\n[bold green]✓ Meeting time converted from {timezone_info} to local time[/bold green]\n",
                justify="center",
            )
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
        console.print("[red]Invalid command or city not found.[/red]")
        suggestions = suggest_cities(" ".join(args))
        if suggestions:
            console.print(f"[yellow]Did you mean:[/yellow] {', '.join(suggestions)}")
        else:
            console.print("[yellow]Try:[/yellow] gtime Tokyo  |  gtime add London  |  gtime list")
        console.print("[yellow]Help:[/yellow] gtime -h")
