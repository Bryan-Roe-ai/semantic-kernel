#!/usr/bin/env python3
"""Automate AGI website fixes with scheduled tasks.

This script periodically runs the GitHub Pages fix script to
keep the AGI website working. It uses the built-in ``sched``
module so no external dependencies are required.
"""
from __future__ import annotations

import argparse
import sched
import subprocess
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
FIX_SCRIPT = REPO_ROOT / "04-infrastructure/scripts/deployment/fix-github-pages.sh"

scheduler = sched.scheduler(time.time, time.sleep)


def run_fix() -> None:
    """Run the GitHub Pages fix script if it exists."""
    if not FIX_SCRIPT.exists():
        print(f"❌ Fix script not found: {FIX_SCRIPT}")
        return
    print(f"🔧 Running {FIX_SCRIPT} ...")
    try:
        subprocess.run(["bash", str(FIX_SCRIPT)], check=False)
    except Exception as exc:
        print(f"⚠️  Failed to run fix script: {exc}")


def _scheduled_task(interval: int) -> None:
    run_fix()
    scheduler.enter(interval, 1, _scheduled_task, (interval,))


def schedule_fixes(interval_hours: int) -> None:
    """Schedule periodic website fixes."""
    interval = interval_hours * 3600
    scheduler.enter(0, 1, _scheduled_task, (interval,))
    try:
        scheduler.run()
    except KeyboardInterrupt:
        print("\n🛑 Stopped scheduled website fixes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate AGI website fixes")
    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="Interval in hours between fix runs (default: 24)",
    )
    args = parser.parse_args()
    schedule_fixes(args.hours)
