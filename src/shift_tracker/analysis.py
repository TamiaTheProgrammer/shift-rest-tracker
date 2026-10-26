"""Calculations on a list of shifts (assumed sorted by start time)."""
from datetime import date, timedelta

from .models import Shift


def rest_gaps(shifts: list[Shift]) -> list[timedelta]:
    """Rest time between each shift's end and the next shift's start.

    N shifts produce N - 1 gaps.
    """
    # TODO
    raise NotImplementedError


def short_turnarounds(
    shifts: list[Shift], min_rest_hours: float = 10
) -> list[tuple[Shift, Shift, timedelta]]:
    """Pairs of consecutive shifts with less rest than `min_rest_hours`.

    Each item is (earlier_shift, next_shift, rest_between_them).
    """
    # TODO: reuse rest_gaps
    raise NotImplementedError


def weekly_hours(shifts: list[Shift]) -> dict[date, float]:
    """Total hours worked per week, keyed by the Monday that starts the week.

    A shift counts toward the week in which it STARTS, even if it ends in
    the next week.

    Hint: date.weekday() returns 0 for Monday.
    """
    # TODO
    raise NotImplementedError
