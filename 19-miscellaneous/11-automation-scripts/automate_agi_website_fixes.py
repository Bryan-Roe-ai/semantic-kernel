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

# Traverse up the directory tree to find the repository root by locating the `.git` folder.
# This ensures the script works even if the directory structure changes.

REPO_ROOT = Path(__file__).resolve().parent
while not (REPO_ROOT / ".git").exists() and REPO_ROOT != REPO_ROOT.parent:
    REPO_ROOT = REPO_ROOT.parent
FIX_SCRIPT = REPO_ROOT / "04-infrastructure/scripts/deployment/fix-github-pages.sh"

scheduler = sched.scheduler(time.time, time.sleep)


def run_fix() -> None:
    """Run the GitHub Pages fix script if it exists."""
    if not FIX_SCRIPT.exists():
        print(f"❌ Fix script not found: {FIX_SCRIPT}")
        return
    print(f"🔧 Running {FIX_SCRIPT} ...")
    try:
        result = subprocess.run(["bash", str(FIX_SCRIPT)], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️  Fix script failed with return code {result.returncode}")
            print(f"⚠️  Error output: {result.stderr.strip()}")
        else:
            print(f"✅ Fix script completed successfully")
            print(f"ℹ️  Output: {result.stdout.strip()}")
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
