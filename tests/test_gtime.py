#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import sys
import os
import json
from pathlib import Path
import pytest
from datetime import datetime
import pytz

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

def test_fuzzy_exact_match_priority():
    out = run_cli("Paris")
    assert "Paris" in out.stdout
    assert "France" in out.stdout
    assert "Buenos Aires" not in out.stdout
    
def test_fuzzy_pairs_returns_paris():
    out = run_cli("pairs")
    assert "Paris" in out.stdout
    assert "France" in out.stdout
    assert "Buenos Aires" not in out.stdout
    
def test_fuzzy_starts_with_priority():
    out = run_cli("lond")
    assert "London" in out.stdout
    assert "UK" in out.stdout
    
def test_fuzzy_substring_match():
    out = run_cli("angel")
    assert "Los Angeles" in out.stdout or "Did you mean" in out.stdout
    
def test_fuzzy_match_with_typos():
    out = run_cli("toky")
    assert "Tokyo" in out.stdout or "Did you mean" in out.stdout
    
def test_fuzzy_case_insensitive_search():
    out = run_cli("LONDON")
    assert "London" in out.stdout
    assert "UK" in out.stdout

def test_24_hour_format_basic():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "15:30")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "London" in out.stdout
    
def test_24_hour_format_evening():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "21:00")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "London" in out.stdout
    
def test_24_hour_format_morning():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "09:00")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "London" in out.stdout
    
def test_12_hour_format_still_works():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "3:30", "PM")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "London" in out.stdout
    
def test_hour_only_24_format():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "15")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "London" in out.stdout
    
def test_hour_only_12_format():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "3", "PM")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "London" in out.stdout

def test_utc_timezone():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "15:30", "UTC")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "London" in out.stdout
    assert "converted from" in out.stdout
    assert "Coordinated Universal Time" in out.stdout
    
def test_est_timezone():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "10:00", "AM", "EST")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "London" in out.stdout
    assert "converted from" in out.stdout
    assert "Eastern Standard Time" in out.stdout
    
def test_pst_timezone():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "2:00", "PM", "PST")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "London" in out.stdout
    assert "converted from" in out.stdout
    assert "Pacific Standard Time" in out.stdout
    
def test_jst_timezone():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "9:00", "AM", "JST")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "London" in out.stdout
    assert "converted from" in out.stdout
    assert "Japan Standard Time" in out.stdout
    
def test_cet_timezone():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "14:00", "CET")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "London" in out.stdout
    assert "converted from" in out.stdout
    assert "Central European Time" in out.stdout
    
def test_timezone_conversion_message():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "10:00", "AM", "UTC")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "converted from" in out.stdout
    
def test_timezone_explanation_shown():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "15:30", "JST")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "converted from" in out.stdout
    assert "Japan Standard Time" in out.stdout

def test_24_hour_with_timezone():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "15:30", "UTC")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "converted from" in out.stdout
    
def test_12_hour_with_timezone():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "3:30", "PM", "EST")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "converted from" in out.stdout
    
def test_hour_only_with_timezone():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "15", "UTC")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    assert "converted from" in out.stdout
    
def test_invalid_timezone():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "15:30", "INVALID")
    assert out.returncode == 0
    assert "Invalid meeting command" in out.stdout

def test_invalid_24_hour_format():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "25:30")
    assert out.returncode == 0
    
def test_invalid_time_format():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "abc:def")
    assert out.returncode == 0

def test_original_meeting_format():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "10:00", "AM")
    assert out.returncode == 0
    assert "GLOBAL TIME FAVORITES" in out.stdout
    
def test_original_fuzzy_search():
    out = run_cli("Londn")
    assert "London" in out.stdout or "Did you mean" in out.stdout
    
def test_original_favorites_workflow():
    run_cli("add", "Tokyo")
    out = run_cli("list")
    assert "Tokyo" in out.stdout
    
    run_cli("remove", "Tokyo")
    out = run_cli("list")
    assert "Tokyo" not in out.stdout

def test_meeting_with_favorites_and_timezone():
    run_cli("add", "London", "Tokyo")
    out = run_cli("meeting", "at", "15:30", "UTC")
    assert out.returncode == 0
    
def test_fuzzy_search_with_favorites():
    run_cli("add", "London")
    out = run_cli("lond")
    assert "London" in out.stdout
    
def test_compare_with_improved_search():
    out = run_cli("compare", "pairs", "toky")
    assert out.returncode == 0
