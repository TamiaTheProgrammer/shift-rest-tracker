"""Charts built with matplotlib."""
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # draw to files without needing a window to open
import matplotlib.pyplot as plt  # noqa: E402

REFERENCE_HOURS = 40


def plot_weekly_hours(weekly: dict[date, float], out_path: str | Path) -> None:
    """Save a bar chart of hours per week to `out_path` (e.g. a .png)."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    weeks = sorted(weekly)
    labels = [f"Week of\n{week:%b %d}" for week in weeks]
    values = [weekly[week] for week in weeks]

    fig, ax = plt.subplots(figsize=(max(6, len(weeks) * 1.5), 4.5))
    bars = ax.bar(labels, values, color="#3b6ea5")
    ax.bar_label(bars, labels=[f"{v:g} h" for v in values], padding=3)

    ax.axhline(REFERENCE_HOURS, color="#c0504d", linestyle="--", linewidth=1,
               label=f"{REFERENCE_HOURS}-hour week")
    ax.legend(loc="upper right", frameon=False)

    ax.set_title("Hours worked per week")
    ax.set_ylabel("Hours")
    ax.set_ylim(0, max(values + [REFERENCE_HOURS]) * 1.15)
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
