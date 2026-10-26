"""Command-line entry point.

Run from the project folder:
    python -m shift_tracker.cli data/sample_shifts.csv --min-rest 10 --chart output/weekly.png
(with src on your PYTHONPATH, or after `pip install -e .`)
"""
import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze rest between shifts.")
    parser.add_argument("csv", help="Path to a shifts CSV file")
    parser.add_argument("--min-rest", type=float, default=10,
                        help="Minimum rest in hours before a gap is flagged (default 10)")
    parser.add_argument("--chart", help="Optional path to save a weekly-hours chart")
    args = parser.parse_args()

    # TODO:
    # 1. Load the shifts.
    # 2. Print a summary: number of shifts, average rest, shortest rest.
    # 3. Print each short turnaround with dates and hours of rest.
    # 4. Print hours per week.
    # 5. If --chart was given, save the chart.


if __name__ == "__main__":
    main()
