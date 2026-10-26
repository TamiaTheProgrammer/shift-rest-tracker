"""Read shifts from a CSV file."""
from pathlib import Path

from .models import Shift


def load_shifts(path: str | Path) -> list[Shift]:
    """Load shifts from a CSV with columns: date, start, end, notes.

    - `date` is YYYY-MM-DD, `start` and `end` are HH:MM (24-hour).
    - If `end` is earlier than `start`, the shift crosses midnight, so the
      end belongs to the next day.
    - Return the shifts sorted by start time.

    Hints: the `csv` module's DictReader, `datetime.strptime`, and
    `timedelta(days=1)`.
    """
    # TODO
    raise NotImplementedError
