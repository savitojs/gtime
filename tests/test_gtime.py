#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import sys
import os
import json
from pathlib import Path
import pytest

SCRIPT = "gtime" # Entry point for the CLI

FAV_FILE = Path.home() / ".gtime_favorites.json"

@pytest.fixture(autouse=True)
def cleanup_favs():
    # Remove favorites file before and after each test
    if FAV_FILE.exists():
        FAV_FILE.unlink()
    yield
    if FAV_FILE.exists():
        FAV_FILE.unlink()

def run_cli(*args):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONPATH"] = os.path.abspath(os.path.dirname(__file__))
    # Always run in the workspace root so .gtime_favorites.json is consistent
    result = subprocess.run([SCRIPT, *args], capture_output=True, text=True, cwd=os.path.dirname(__file__), env=env)
    return result

def test_help():
    out = run_cli("-h")
    assert "Global Time" in out.stdout
    assert "Usage" in out.stdout

def test_add_and_list_favorite():
    run_cli("add", "London")
    out = run_cli("list")
    assert "London" in out.stdout
    assert "UK" in out.stdout

def test_remove_favorite():
    run_cli("add", "London")
    run_cli("remove", "London")
    out = run_cli("list")
    assert "London" not in out.stdout

def test_city_lookup():
    out = run_cli("Tokyo")
    assert "Tokyo" in out.stdout
    assert "Japan" in out.stdout

def test_fuzzy_search():
    out = run_cli("Londn")  # typo
    assert "London" in out.stdout or "Did you mean" in out.stdout

def test_compare():
    out = run_cli("compare", "London", "Tokyo")
    assert "London" in out.stdout and "Tokyo" in out.stdout

def test_meeting_time():
    out = run_cli("meeting", "at", "10:00", "AM")
    assert "Favorite Cities" in out.stdout or "No favorite cities" in out.stdout

def test_invalid_city():
    out = run_cli("NotACity")
    assert "Invalid command" in out.stdout or "Did you mean" in out.stdout

def test_no_favorites():
    out = run_cli("list")
    assert "No favorite cities" in out.stdout
