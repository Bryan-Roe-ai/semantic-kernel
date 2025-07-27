#!/usr/bin/env python3
"""CLI tool to trigger automation scripts."""
import argparse
import os
import subprocess
import sys

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), '19-miscellaneous', '11-automation-scripts')


def list_scripts() -> None:
    """Print available automation scripts."""
    for name in sorted(os.listdir(SCRIPTS_DIR)):
        if name.endswith(('.sh', '.py', '.ps1')):
            print(name)


def run_script(script: str, args: list[str]) -> None:
    """Run the given automation script with optional arguments."""
    path = os.path.join(SCRIPTS_DIR, script)
    if not os.path.isfile(path):
        print(f"Script not found: {script}", file=sys.stderr)
        sys.exit(1)

    if script.endswith('.sh'):
        cmd = ['bash', path]
    elif script.endswith('.py'):
        cmd = [sys.executable, path]
    elif script.endswith('.ps1'):
        cmd = ['pwsh', path]
    else:
        cmd = [path]
    cmd.extend(args)

    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Automation scripts CLI")
    subparsers = parser.add_subparsers(dest='command', required=True)

    subparsers.add_parser('list', help='List available scripts')

    run_parser = subparsers.add_parser('run', help='Run a script')
    run_parser.add_argument('script', help='Script name to run')
    run_parser.add_argument('script_args', nargs=argparse.REMAINDER, help='Arguments passed to the script')

    args = parser.parse_args()

    if args.command == 'list':
        list_scripts()
    elif args.command == 'run':
        run_script(args.script, args.script_args)


if __name__ == '__main__':
    main()
