"""Read shifts from a CSV file."""
import csv
from datetime import datetime, timedelta
from pathlib import Path

from .models import Shift

DATETIME_FORMAT = "%Y-%m-%d %H:%M"


def load_shifts(path: str | Path) -> list[Shift]:
    """Load shifts from a CSV with columns: date, start, end, notes.

    - `date` is YYYY-MM-DD, `start` and `end` are HH:MM (24-hour).
    - If `end` is earlier than `start`, the shift crosses midnight, so the
      end belongs to the next day.
    - A shift whose end equals its start is treated as a data error, since
      it is more likely a typo than a 24-hour shift.
    - Returns the shifts sorted by start time.
    """
    shifts = []

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        # Row 1 is the header, so data starts on line 2 of the file.
        for line_number, row in enumerate(reader, start=2):
            date = row["date"].strip()
            start = datetime.strptime(f"{date} {row['start'].strip()}", DATETIME_FORMAT)
            end = datetime.strptime(f"{date} {row['end'].strip()}", DATETIME_FORMAT)

            if end == start:
                raise ValueError(
                    f"Line {line_number}: shift starts and ends at the same time"
                )

            # An end time earlier than the start means the shift ran past midnight.
            if end < start:
                end += timedelta(days=1)

            notes = (row.get("notes") or "").strip()
            shifts.append(Shift(start=start, end=end, notes=notes))

    # The CSV might not be in order, and later calculations depend on it.
    return sorted(shifts, key=lambda shift: shift.start)