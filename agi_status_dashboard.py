#!/usr/bin/env python3
"""
AGI Status Dashboard for system monitoring

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import subprocess
import json
import psutil
from datetime import datetime
from pathlib import Path

def get_running_processes():
    """Get running AGI-related processes"""
    agi_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
        try:
            cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
            if 'agi_' in cmdline.lower() or 'local_agent' in cmdline.lower():
                agi_processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cmdline': cmdline,
                    'started': datetime.fromtimestamp(proc.info['create_time']).strftime('%Y-%m-%d %H:%M:%S')
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return agi_processes

def check_agent_files():
    """Check which AGI agent files are available"""
    workspace = Path.cwd()
    agent_files = []

    agi_patterns = [
        'agi_*.py',
        'local_agent_*.py',
        'demo_*.py',
        '*_agent*.py'
    ]

    for pattern in agi_patterns:
        for file in workspace.glob(pattern):
            agent_files.append({
                'name': file.name,
                'path': str(file),
                'size': file.stat().st_size,
                'modified': datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })

    return agent_files

def get_system_resources():
    """Get system resource usage"""
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
        'load_avg': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else 'N/A'
    }

def main():
    """Display AGI agent status dashboard"""
    print("🤖 AGI Agent Status Dashboard")
    print("=" * 60)
    print(f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # System Resources
    print("💻 System Resources:")
    print("-" * 30)
    resources = get_system_resources()
    print(f"  CPU Usage: {resources['cpu_percent']:.1f}%")
    print(f"  Memory Usage: {resources['memory_percent']:.1f}%")
    print(f"  Disk Usage: {resources['disk_percent']:.1f}%")
    if resources['load_avg'] != 'N/A':
        print(f"  Load Average: {resources['load_avg']}")
    print()

    # Running Processes
    print("🏃 Running AGI Processes:")
    print("-" * 30)
    processes = get_running_processes()
    if processes:
        for proc in processes:
            print(f"  PID {proc['pid']}: {proc['name']}")
            print(f"    Started: {proc['started']}")
            print(f"    Command: {proc['cmdline'][:80]}...")
            print()
    else:
        print("  No AGI processes currently running")
    print()

    # Available Agent Files
    print("📁 Available AGI Agent Files:")
    print("-" * 30)
    agent_files = check_agent_files()
    if agent_files:
        for file in agent_files:
            size_kb = file['size'] / 1024
            print(f"  📄 {file['name']}")
            print(f"    Size: {size_kb:.1f} KB")
            print(f"    Modified: {file['modified']}")
            print()
    else:
        print("  No AGI agent files found")
    print()

    # Quick Start Commands
    print("🚀 Quick Start Commands:")
    print("-" * 30)
    print("  Start CLI:          python agi_cli.py help")
    print("  Run Demo:           python demo_local_agents.py")
    print("  Launch Manager:     python local_agent_launcher.py")
    print("  Test Setup:         python test_local_agent.py")
    print("  Monitor Performance: python agi_performance_monitor.py")
    print()

    print("✅ Dashboard update complete!")

if __name__ == "__main__":
    main()
