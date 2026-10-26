"""Charts built with matplotlib."""
from datetime import date
from pathlib import Path


def plot_weekly_hours(weekly: dict[date, float], out_path: str | Path) -> None:
    """Save a bar chart of hours per week to `out_path` (e.g. a .png).

    Ideas: label each bar with its value, and draw a horizontal line at 40
    hours for reference.
    """
    # TODO
    raise NotImplementedError
