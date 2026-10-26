# Shift Rest Tracker

<!-- One or two sentences: what this does and who it's for. -->
A command-line tool that analyzes work schedules for people on rotating shifts. It calculates rest time between shifts, flags short turnarounds, and charts weekly hours.

## Why I built this
<!-- Your story, in your words. Example angle: as a locomotive engineer working
rotating shifts, I wanted a quick way to see when my schedule left too little
rest between shifts. Keep it to 2-4 sentences. -->

## Features
- Reads shifts from a CSV file, including overnight shifts that cross midnight
- Calculates rest between consecutive shifts
- Flags turnarounds below a configurable minimum rest (default 10 hours)
- Totals hours worked per week
- Saves a weekly-hours bar chart

## Demo
<!-- Paste sample terminal output here, and add the chart image:
![Weekly hours](docs/weekly.png) -->

## Getting started
```bash
git clone https://github.com/TamiaTheProgrammer/shift-rest-tracker.git
cd shift-rest-tracker
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=src python -m shift_tracker.cli data/sample_shifts.csv --chart output/weekly.png
```

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
<!-- Interviewers love this section. Examples to write about once you've built it:
- Why shifts store full datetimes instead of separate date and time
- How overnight shifts are handled
- Why a shift counts toward the week it starts in -->

## What I'd add next
<!-- e.g. a Streamlit web UI, calendar (.ics) import, sleep tracking -->
