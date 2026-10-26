"""Calculations on a list of shifts (assumed sorted by start time)."""
from datetime import date, timedelta

from .models import Shift


def rest_gaps(shifts: list[Shift]) -> list[timedelta]:
    """Rest time between each shift's end and the next shift's start.

    N shifts produce N - 1 gaps.
    """
    # zip(shifts, shifts[1:]) pairs each shift with the one after it:
    # (shift1, shift2), (shift2, shift3), ...
    return [nxt.start - current.end for current, nxt in zip(shifts, shifts[1:])]


def short_turnarounds(
    shifts: list[Shift], min_rest_hours: float = 10
) -> list[tuple[Shift, Shift, timedelta]]:
    """Pairs of consecutive shifts with less rest than `min_rest_hours`.

    Each item is (earlier_shift, next_shift, rest_between_them).
    """
    minimum = timedelta(hours=min_rest_hours)
    pairs = zip(shifts, shifts[1:])

    # rest_gaps lines up one-to-one with the pairs, so zip them together.
    return [
        (current, nxt, rest)
        for (current, nxt), rest in zip(pairs, rest_gaps(shifts))
        if rest < minimum
    ]


def weekly_hours(shifts: list[Shift]) -> dict[date, float]:
    """Total hours worked per week, keyed by the Monday that starts the week.

    A shift counts toward the week in which it STARTS, even if it ends in
    the next week.
    """
    totals: dict[date, float] = {}

    for shift in shifts:
        start_day = shift.start.date()
        # weekday() is 0 for Monday, so stepping back that many days lands on Monday.
        week_start = start_day - timedelta(days=start_day.weekday())
        hours = shift.duration.total_seconds() / 3600
        totals[week_start] = totals.get(week_start, 0) + hours

    return totals
