#!/usr/bin/env python3
"""Automation Status Dashboard

This script provides a lightweight console dashboard to check the
status of the extended automation system. It summarizes system
resources, the automation process state and recent log entries.

The dashboard relies on the existing ExtendedMonitoringDashboard
utilities for gathering metrics where possible.
"""

from pathlib import Path
import json
import psutil
from datetime import datetime

# Import ExtendedMonitoringDashboard if available
import sys

ExtendedMonitoringDashboard = None
repo_root = Path(__file__).resolve().parent
import os

def get_dashboard_path(repo_root, args):
    """Determine the dashboard path from command-line arguments or environment variable."""
    if args.dashboard_path:
        return Path(args.dashboard_path)
    env_path = os.getenv("DASHBOARD_PATH")
    if env_path:
        return Path(env_path)
    return repo_root / "19-miscellaneous" / "src"

dashboard_path = get_dashboard_path(repo_root, None)  # Placeholder for args
if dashboard_path.exists():
    sys.path.append(str(dashboard_path))
    try:
        from extended_monitoring_dashboard import ExtendedMonitoringDashboard  # type: ignore
    except Exception:
        pass

LOG_FILE = Path('logs/extended/extended_automode.log')
STATE_DIR = Path('.extended_automode')


def load_recent_logs(log_path: Path, lines: int = 10):
    """Return last *lines* from the log file."""
    if not log_path.exists():
        return []
    try:
        with log_path.open('r') as f:
            content = f.readlines()
        return [line.strip() for line in content[-lines:]]
    except Exception:
        return []


def print_dashboard(base_dir: Path):
    """Display automation status information."""
    dashboard = None
    if ExtendedMonitoringDashboard is not None:
        dashboard = ExtendedMonitoringDashboard(base_dir)

    print("=" * 60)
    print("🤖 AUTOMATION STATUS DASHBOARD")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    if dashboard:
        overview = dashboard.get_system_overview()
        status = dashboard.get_automode_status()
    else:
        # Minimal info if dashboard class unavailable
        overview = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
        }
        status = {'running': False}
        pid_file = STATE_DIR / 'extended.pid'
        if pid_file.exists():
            try:
                pid = int(pid_file.read_text().strip())
                if psutil.pid_exists(pid):
                    proc = psutil.Process(pid)
                    status['running'] = True
                    status['pid'] = pid
                    status['startup_time'] = proc.create_time()
            except Exception:
                pass

    print("System Resources")
    print("-" * 30)
    print(f"CPU Usage:    {overview.get('cpu_percent', 0):6.1f}%")
    print(f"Memory Usage: {overview.get('memory_percent', 0):6.1f}%")
    print(f"Disk Usage:   {overview.get('disk_percent', 0):6.1f}%")
    print()

    print("Automation Process")
    print("-" * 30)
    if status.get('running'):
        uptime = 0
        if 'startup_time' in status:
            uptime = datetime.now().timestamp() - status['startup_time']
        print(f"Status:    RUNNING (PID {status.get('pid')})")
        print(f"Uptime:    {uptime/3600:.1f} hours")
    else:
        print("Status:    NOT RUNNING")
    print()

    print("Recent Log Entries")
    print("-" * 30)
    for line in load_recent_logs(base_dir / LOG_FILE):
        print(line)
    print()

    if dashboard:
        db = dashboard.get_database_stats()
        if db.get('available'):
            print("Metrics DB")
            print("-" * 30)
            size = db.get('size_mb', 0)
            print(f"Size: {size:.1f} MB")
            for table, count in db.get('tables', {}).items():
                print(f"{table:15s}: {count}")
            print()

    print("=" * 60)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Automation Status Dashboard")
    parser.add_argument('--base-dir', type=Path, default=Path.cwd(),
                        help='Base directory of automation state')
    parser.add_argument('--json', action='store_true',
                        help='Output data in JSON format')
    args = parser.parse_args()

    if args.json:
        data = {}
        if ExtendedMonitoringDashboard is not None:
            dashboard = ExtendedMonitoringDashboard(args.base_dir)
            data = {
                'system_overview': dashboard.get_system_overview(),
                'automode_status': dashboard.get_automode_status(),
                'database_stats': dashboard.get_database_stats(),
                'recent_logs': load_recent_logs(args.base_dir / LOG_FILE),
            }
        else:
            data = {
                'recent_logs': load_recent_logs(args.base_dir / LOG_FILE),
            }
        print(json.dumps(data, indent=2, default=str))
    else:
        print_dashboard(args.base_dir)


if __name__ == '__main__':
    main()
