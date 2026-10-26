"""These tests describe the expected behavior. Make them pass one by one:
    pytest -v
"""
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest

from shift_tracker.analysis import rest_gaps, short_turnarounds, weekly_hours
from shift_tracker.loader import load_shifts
from shift_tracker.models import Shift

SAMPLE = Path(__file__).parent.parent / "data" / "sample_shifts.csv"


def hours(td: timedelta) -> float:
    return td.total_seconds() / 3600


# ---------- Step 1: models ----------
def test_duration():
    s = Shift(datetime(2026, 1, 1, 6), datetime(2026, 1, 1, 14, 30))
    assert s.duration == timedelta(hours=8, minutes=30)


# ---------- Step 2: loader ----------
def test_loads_all_shifts():
    assert len(load_shifts(SAMPLE)) == 11


def test_overnight_shift_ends_next_day():
    overnight = load_shifts(SAMPLE)[5]  # 2026-10-11 22:00 -> 06:00
    assert overnight.start == datetime(2026, 10, 11, 22, 0)
    assert overnight.end == datetime(2026, 10, 12, 6, 0)
    assert overnight.notes == "Overnight"


def test_shifts_are_sorted():
    shifts = load_shifts(SAMPLE)
    assert shifts == sorted(shifts, key=lambda s: s.start)


def test_same_start_and_end_is_rejected(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("date,start,end,notes\n2026-10-05,06:00,06:00,\n")
    with pytest.raises(ValueError, match="Line 2"):
        load_shifts(bad)


# ---------- Step 3: analysis ----------
def test_rest_gaps():
    gaps = [hours(g) for g in rest_gaps(load_shifts(SAMPLE))]
    assert gaps == [16, 24, 8, 16, 55.5, 16, 8, 32, 16, 30]


def test_rest_gaps_with_one_shift():
    s = Shift(datetime(2026, 1, 1, 6), datetime(2026, 1, 1, 14))
    assert rest_gaps([s]) == []


def test_short_turnarounds():
    shifts = load_shifts(SAMPLE)
    flagged = short_turnarounds(shifts, min_rest_hours=10)
    assert len(flagged) == 2
    first, nxt, rest = flagged[0]
    assert first.start == datetime(2026, 10, 7, 14, 0)
    assert nxt.start == datetime(2026, 10, 8, 6, 0)
    assert hours(rest) == 8


def test_threshold_is_configurable():
    shifts = load_shifts(SAMPLE)
    assert len(short_turnarounds(shifts, min_rest_hours=7)) == 0
    assert len(short_turnarounds(shifts, min_rest_hours=17)) == 6


def test_weekly_hours():
    assert weekly_hours(load_shifts(SAMPLE)) == {
        date(2026, 10, 5): 48.5,
        date(2026, 10, 12): 42.0,
    }