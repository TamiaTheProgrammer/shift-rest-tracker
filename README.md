# Shift Rest Tracker

<!-- One or two sentences: what this does and who it's for. -->
A command-line tool that analyzes work schedules for people on rotating shifts. It calculates rest time between shifts, flags short turnarounds, and charts weekly hours.

## Why I built this
This is a tester. I really want to solve the scheduling issues at my job, and hopefully create a job pick everyone (Supervisors and engineers and conductors) both love.

## Features
- Reads shifts from a CSV file, including overnight shifts that cross midnight
- Calculates rest between consecutive shifts
- Flags turnarounds below a configurable minimum rest (default 10 hours)
- Totals hours worked per week
- Saves a weekly-hours bar chart

## Demo
```
$ shift-tracker data/sample_shifts.csv --chart output/weekly.png
SHIFT SUMMARY
  Shifts:        11
  Date range:    Oct 05, 2026 to Oct 18, 2026
  Average rest:  22.15 h
  Shortest rest: 8 h

SHORT TURNAROUNDS (less than 10 h rest)
  Wed Oct 07 22:00 -> Thu Oct 08 06:00   only 8 h rest
  Tue Oct 13 06:00 -> Tue Oct 13 14:00   only 8 h rest

HOURS PER WEEK
  Week of Oct 05: 48.5 h
  Week of Oct 12: 42 h

Chart saved to output/weekly.png
```

![Weekly hours chart](docs/weekly.png)

## Getting started
```bash
git clone https://github.com/TamiaTheProgrammer/shift-rest-tracker.git
cd shift-rest-tracker
python -m venv .venv
.venv\Scripts\activate           # Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
shift-tracker data/sample_shifts.csv --chart output/weekly.png
```

Options:
- `--min-rest 12` changes the rest threshold (default 10 hours)
- `--chart path.png` saves the weekly-hours chart

## CSV format
| column | example | notes |
|---|---|---|
| date | 2026-10-05 | YYYY-MM-DD |
| start | 22:00 | 24-hour time |
| end | 06:00 | if earlier than start, the shift ends the next day |
| notes | Overnight | optional |

## Running tests
```bash
pytest -v
```

## Design decisions
- **Shifts store full datetimes, not separate dates and times.** That makes overnight shifts simple: an end time earlier than the start time moves to the next day, and every later calculation is plain subtraction.
- **A shift that starts and ends at the same time is rejected** with the line number, since that is more likely a typo than a 24-hour shift.
- **A shift counts toward the week it starts in**, even if it ends after midnight on Sunday, so each shift's hours are counted exactly once.
- **Logic is split into small modules** (loading, analysis, charts, CLI), so each part can be tested on its own.

## What I'd add next
<!-- e.g. a Streamlit web UI, calendar (.ics) import, sleep tracking -->
