"""Data model for a single work shift."""
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class Shift:
    """One work shift with full start and end datetimes.

    Overnight shifts (e.g. 22:00 to 06:00) end on the day AFTER they start,
    so `end` is always later than `start`.
    """

    start: datetime
    end: datetime
    notes: str = ""

    @property
    def duration(self) -> timedelta:
        """How long the shift lasted."""
        # Subtracting two datetimes gives a timedelta (an amount of time).
        return self.end - self.start