"""Command-line entry point.

After `pip install -e .`, run from the project folder:
    shift-tracker data/sample_shifts.csv --min-rest 10 --chart output/weekly.png
"""
import argparse
import sys
from datetime import timedelta

from .analysis import rest_gaps, short_turnarounds, weekly_hours
from .charts import plot_weekly_hours
from .loader import load_shifts


def format_hours(td: timedelta) -> str:
    """Show a timedelta as hours, e.g. 8.5 h."""
    return f"{td.total_seconds() / 3600:g} h"


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze rest between shifts.")
    parser.add_argument("csv", help="Path to a shifts CSV file")
    parser.add_argument("--min-rest", type=float, default=10,
                        help="Minimum rest in hours before a gap is flagged (default 10)")
    parser.add_argument("--chart", help="Optional path to save a weekly-hours chart")
    args = parser.parse_args()

    try:
        shifts = load_shifts(args.csv)
    except FileNotFoundError:
        sys.exit(f"Error: can't find the file '{args.csv}'")
    except (ValueError, KeyError) as error:
        sys.exit(f"Error reading '{args.csv}': {error}")

    if not shifts:
        sys.exit("No shifts found in the file.")

    # Summary
    gaps = rest_gaps(shifts)
    print("SHIFT SUMMARY")
    print(f"  Shifts:        {len(shifts)}")
    print(f"  Date range:    {shifts[0].start:%b %d, %Y} to {shifts[-1].end:%b %d, %Y}")
    if gaps:
        average = sum(gaps, timedelta()) / len(gaps)
        print(f"  Average rest:  {format_hours(average)}")
        print(f"  Shortest rest: {format_hours(min(gaps))}")

    # Short turnarounds
    flagged = short_turnarounds(shifts, args.min_rest)
    print(f"\nSHORT TURNAROUNDS (less than {args.min_rest:g} h rest)")
    if flagged:
        for current, nxt, rest in flagged:
            print(f"  {current.end:%a %b %d %H:%M} -> {nxt.start:%a %b %d %H:%M}"
                  f"   only {format_hours(rest)} rest")
    else:
        print("  None. Every gap met the minimum.")

    # Weekly hours
    weekly = weekly_hours(shifts)
    print("\nHOURS PER WEEK")
    for week in sorted(weekly):
        print(f"  Week of {week:%b %d}: {weekly[week]:g} h")

    if args.chart:
        plot_weekly_hours(weekly, args.chart)
        print(f"\nChart saved to {args.chart}")


if __name__ == "__main__":
    main()
