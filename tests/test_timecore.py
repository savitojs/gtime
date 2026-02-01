#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

from gtime.timecore import ZoneInfo, parse_meeting_time


def test_new_york_winter_offset():
    dt = datetime.datetime(2024, 1, 15, 12, 0, tzinfo=ZoneInfo("America/New_York"))
    assert dt.utcoffset() == datetime.timedelta(hours=-5)


def test_new_york_summer_offset():
    dt = datetime.datetime(2024, 7, 15, 12, 0, tzinfo=ZoneInfo("America/New_York"))
    assert dt.utcoffset() == datetime.timedelta(hours=-4)


def test_paris_offsets():
    winter = datetime.datetime(2024, 1, 15, 12, 0, tzinfo=ZoneInfo("Europe/Paris"))
    summer = datetime.datetime(2024, 7, 15, 12, 0, tzinfo=ZoneInfo("Europe/Paris"))
    assert winter.utcoffset() == datetime.timedelta(hours=1)
    assert summer.utcoffset() == datetime.timedelta(hours=2)


def test_kolkata_offset():
    dt = datetime.datetime(2024, 3, 1, 12, 0, tzinfo=ZoneInfo("Asia/Kolkata"))
    assert dt.utcoffset() == datetime.timedelta(hours=5, minutes=30)


def test_new_york_dst_spring_forward():
    before = datetime.datetime(2024, 3, 10, 1, 30, tzinfo=ZoneInfo("America/New_York"))
    after = datetime.datetime(2024, 3, 10, 3, 30, tzinfo=ZoneInfo("America/New_York"))
    assert before.utcoffset() == datetime.timedelta(hours=-5)
    assert after.utcoffset() == datetime.timedelta(hours=-4)


def test_parse_meeting_time_timezone_info():
    meeting_time, timezone_info = parse_meeting_time(["meeting", "at", "10:00", "AM", "UTC"])
    assert meeting_time is not None
    assert meeting_time.tzinfo is None
    assert timezone_info == "Coordinated Universal Time (UTC)"
