#!/usr/bin/env python3
"""
Test module for changed files

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Set


def get_changed_files() -> List[str]:
    """Get list of changed files using git."""
    try:
        # Get staged files
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        staged_files = result.stdout.strip().split('\n') if result.stdout.strip() else []

        # Get unstaged files
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        unstaged_files = result.stdout.strip().split('\n') if result.stdout.strip() else []

        # Combine and filter Python files
        all_files = set(staged_files + unstaged_files)
        python_files = [f for f in all_files if f.endswith('.py') and Path(f).exists()]

        return python_files

    except subprocess.CalledProcessError:
        print("Error: Could not get changed files from git")
        return []


def find_test_files(changed_files: List[str]) -> Set[str]:
    """Find test files corresponding to changed source files."""
    test_files = set()

    for file_path in changed_files:
        path = Path(file_path)

        # If it's already a test file, include it
        if path.name.startswith('test_') or path.name.endswith('_test.py'):
            if path.exists():
                test_files.add(str(path))
            continue

        # If it's in the semantic_kernel directory, find corresponding tests
        if 'semantic_kernel' in path.parts:
            # Find the relative path within semantic_kernel
            try:
                sk_index = path.parts.index('semantic_kernel')
                relative_parts = path.parts[sk_index + 1:]

                if relative_parts:
                    # Try different test naming patterns
                    test_patterns = [
                        f"test_{path.stem}.py",
                        f"{path.stem}_test.py"
                    ]

                    # Search in different test directories
                    test_dirs = [
                        Path("tests/unit/semantic_kernel") / Path(*relative_parts[:-1]),
                        Path("tests/integration/semantic_kernel") / Path(*relative_parts[:-1]),
                        Path("tests/unit"),
                        Path("tests/integration")
                    ]

                    for test_dir in test_dirs:
                        for pattern in test_patterns:
                            test_file = test_dir / pattern
                            if test_file.exists():
                                test_files.add(str(test_file))

            except (ValueError, IndexError):
                continue

    return test_files


def run_tests(test_files: Set[str]) -> bool:
    """Run the specified test files."""
    if not test_files:
        print("No test files found for changed files")
        return True

    print(f"Running tests for {len(test_files)} test files:")
    for test_file in sorted(test_files):
        print(f"  - {test_file}")

    cmd = [
        sys.executable, "-m", "pytest",
        *sorted(test_files),
        "-v",
        "--tb=short",
        "-x"  # Stop on first failure
    ]

    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\nTest execution interrupted")
        return False


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Files passed as arguments (from pre-commit)
        changed_files = [f for f in sys.argv[1:] if f.endswith('.py')]
    else:
        # Detect changed files automatically
        changed_files = get_changed_files()

    if not changed_files:
        print("No Python files changed")
        return True

    print(f"Changed files: {', '.join(changed_files)}")

    test_files = find_test_files(changed_files)

    if not test_files:
        print("No corresponding test files found, running fast unit tests")
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/unit",
            "-x",
            "--tb=line",
            "-q",
            "-k", "not slow",
            "--maxfail=5"
        ]
        result = subprocess.run(cmd, check=False)
        return result.returncode == 0

    return run_tests(test_files)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
