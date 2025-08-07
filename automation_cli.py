#!/usr/bin/env python3
"""CLI tool to trigger automation scripts."""
import argparse
import os
import subprocess
import sys

DEFAULT_SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), '19-miscellaneous', '11-automation-scripts')
SCRIPTS_DIR = os.getenv('SCRIPTS_DIR_ENV', DEFAULT_SCRIPTS_DIR)


def list_scripts() -> None:
    """Print available automation scripts."""
    if not os.path.isdir(SCRIPTS_DIR):
        print(f"Scripts directory not found: {SCRIPTS_DIR}", file=sys.stderr)
        sys.exit(1)
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
        pwsh_path = shutil.which('pwsh')
        if pwsh_path:
            cmd = [pwsh_path, path]
        else:
            cmd = ['powershell', '-File', path]
    else:
        cmd = [path]
    cmd.extend(args)

    subprocess.run(cmd, check=True, shell=False)


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

if __name__ == "__main__":
    main()
