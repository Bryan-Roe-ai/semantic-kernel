#!/usr/bin/env python3
"""
Test Watcher for Semantic Kernel Python

Watches for file changes and automatically runs relevant tests.
Provides intelligent test selection and continuous feedback.
"""

import asyncio
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
except ImportError:
    print("Error: watchdog not installed. Install with: pip install watchdog")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestWatcher(FileSystemEventHandler):
    """Intelligent test watcher that runs relevant tests on file changes."""

    def __init__(self, root_dir: Path, test_on_save: bool = True):
        """Initialize the test watcher."""
        self.root_dir = root_dir
        self.test_on_save = test_on_save
        self.src_dir = root_dir / "semantic_kernel"
        self.test_dir = root_dir / "tests"
        
        # Timing control
        self.last_run = 0
        self.debounce_seconds = 2
        
        # Test mapping cache
        self.test_cache: Dict[str, Set[str]] = {}
        
        # File patterns to watch
        self.watch_patterns = {'.py', '.yaml', '.yml', '.json'}
        self.ignore_patterns = {
            '__pycache__',
            '.pytest_cache', 
            '.git',
            '.venv',
            'node_modules',
            '.mypy_cache',
            'htmlcov',
            'test_reports'
        }
        
        logger.info(f"Initialized test watcher for {root_dir}")

    def should_ignore_path(self, path: str) -> bool:
        """Check if path should be ignored."""
        path_obj = Path(path)
        
        # Check ignore patterns
        for ignore in self.ignore_patterns:
            if ignore in path_obj.parts:
                return True
                
        # Check file extension
        if path_obj.suffix not in self.watch_patterns:
            return True
            
        return False

    def find_related_tests(self, changed_file: Path) -> List[Path]:
        """Find test files related to the changed source file."""
        related_tests = []
        
        if changed_file.is_relative_to(self.test_dir):
            # If it's already a test file, run it
            if changed_file.name.startswith('test_') or changed_file.name.endswith('_test.py'):
                related_tests.append(changed_file)
        
        elif changed_file.is_relative_to(self.src_dir):
            # Find corresponding test files
            relative_path = changed_file.relative_to(self.src_dir)
            module_parts = relative_path.with_suffix('').parts
            
            # Try different test naming conventions
            test_patterns = [
                f"test_{changed_file.stem}.py",
                f"{changed_file.stem}_test.py",
                f"test_{module_parts[-1]}.py" if len(module_parts) > 1 else None
            ]
            
            # Search in corresponding test directories
            search_dirs = [
                self.test_dir / "unit" / relative_path.parent,
                self.test_dir / "integration" / relative_path.parent,
                self.test_dir / "unit",
                self.test_dir / "integration"
            ]
            
            for search_dir in search_dirs:
                if search_dir.exists():
                    for pattern in test_patterns:
                        if pattern:
                            test_file = search_dir / pattern
                            if test_file.exists():
                                related_tests.append(test_file)
        
        # If no specific tests found, run unit tests as fallback
        if not related_tests:
            # Find all unit tests for the module
            if changed_file.is_relative_to(self.src_dir):
                relative_path = changed_file.relative_to(self.src_dir)
                module_name = relative_path.parts[0] if relative_path.parts else "core"
                
                unit_test_dir = self.test_dir / "unit" / "semantic_kernel" / module_name
                if unit_test_dir.exists():
                    related_tests.extend(unit_test_dir.glob("test_*.py"))
        
        return list(set(related_tests))  # Remove duplicates

    def run_tests(self, test_files: List[Path]) -> bool:
        """Run the specified test files."""
        if not test_files:
            logger.info("No tests to run")
            return True
        
        test_paths = [str(f) for f in test_files]
        logger.info(f"Running tests: {', '.join(test_paths)}")
        
        cmd = [
            sys.executable, "-m", "pytest",
            *test_paths,
            "-v",
            "--tb=short",
            "--no-header",
            "--quiet",
            "-x"  # Stop on first failure
        ]
        
        try:
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.root_dir,
                timeout=300
            )
            duration = time.time() - start_time
            
            if result.returncode == 0:
                logger.info(f"✅ Tests passed ({duration:.1f}s)")
                self.print_success_summary(len(test_files), duration)
            else:
                logger.error(f"❌ Tests failed ({duration:.1f}s)")
                self.print_failure_summary(result.stdout, result.stderr)
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            logger.error("⏰ Tests timed out")
            return False
        except Exception as e:
            logger.error(f"💥 Error running tests: {e}")
            return False

    def print_success_summary(self, test_count: int, duration: float) -> None:
        """Print success summary."""
        print("\n" + "="*50)
        print(f"✅ {test_count} test file(s) passed in {duration:.1f}s")
        print("="*50)

    def print_failure_summary(self, stdout: str, stderr: str) -> None:
        """Print failure summary."""
        print("\n" + "="*50)
        print("❌ Test failures detected:")
        print("="*50)
        
        # Extract and show key failure information
        lines = stdout.split('\n') + stderr.split('\n')
        failure_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['failed', 'error', 'assert']):
                failure_lines.append(line.strip())
        
        for line in failure_lines[:10]:  # Show first 10 failure lines
            if line:
                print(f"  {line}")
        
        if len(failure_lines) > 10:
            print(f"  ... and {len(failure_lines) - 10} more")
        
        print("="*50)

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return
            
        if self.should_ignore_path(event.src_path):
            return
        
        # Debounce rapid file changes
        current_time = time.time()
        if current_time - self.last_run < self.debounce_seconds:
            return
        
        self.last_run = current_time
        
        changed_file = Path(event.src_path)
        logger.info(f"📝 File changed: {changed_file.relative_to(self.root_dir)}")
        
        if self.test_on_save:
            related_tests = self.find_related_tests(changed_file)
            
            if related_tests:
                self.run_tests(related_tests)
            else:
                logger.info("No related tests found, running fast unit tests")
                self.run_fast_tests()

    def run_fast_tests(self) -> bool:
        """Run a fast subset of unit tests."""
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/unit",
            "-x",
            "--tb=line",
            "--quiet",
            "-k", "not slow",
            "--maxfail=3"
        ]
        
        try:
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.root_dir,
                timeout=60
            )
            duration = time.time() - start_time
            
            if result.returncode == 0:
                logger.info(f"⚡ Fast tests passed ({duration:.1f}s)")
            else:
                logger.error(f"⚡ Fast tests failed ({duration:.1f}s)")
            
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"Error running fast tests: {e}")
            return False

    def run_all_tests(self) -> bool:
        """Run all tests."""
        logger.info("🔄 Running all tests...")
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/unit",
            "-v",
            "--tb=short"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.root_dir,
                timeout=600
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Error running all tests: {e}")
            return False


class TestWatcherCLI:
    """Command line interface for the test watcher."""

    def __init__(self):
        """Initialize the CLI."""
        self.root_dir = Path.cwd()
        self.observer = None
        self.watcher = None

    def setup_watcher(self, test_on_save: bool = True) -> None:
        """Setup the file watcher."""
        self.watcher = TestWatcher(self.root_dir, test_on_save)
        self.observer = Observer()
        
        # Watch source and test directories
        watch_dirs = [
            self.root_dir / "semantic_kernel",
            self.root_dir / "tests"
        ]
        
        for watch_dir in watch_dirs:
            if watch_dir.exists():
                self.observer.schedule(
                    self.watcher, 
                    str(watch_dir), 
                    recursive=True
                )
                logger.info(f"👀 Watching: {watch_dir}")

    def start_watching(self) -> None:
        """Start watching for file changes."""
        if not self.observer or not self.watcher:
            raise RuntimeError("Watcher not setup")
        
        self.observer.start()
        print("\n" + "="*60)
        print("🚀 Test Watcher Started")
        print("="*60)
        print("Watching for changes in:")
        print(f"  📁 {self.root_dir / 'semantic_kernel'}")
        print(f"  📁 {self.root_dir / 'tests'}")
        print("\nCommands:")
        print("  [Enter] - Run all tests")
        print("  f       - Run fast tests")
        print("  q       - Quit")
        print("="*60)
        
        try:
            while True:
                try:
                    user_input = input().strip().lower()
                    
                    if user_input == 'q':
                        break
                    elif user_input == 'f':
                        self.watcher.run_fast_tests()
                    elif user_input == '':
                        self.watcher.run_all_tests()
                    else:
                        print("Unknown command. Use 'f' for fast tests, [Enter] for all tests, 'q' to quit.")
                        
                except KeyboardInterrupt:
                    break
                except EOFError:
                    break
                    
        finally:
            self.stop_watching()

    def stop_watching(self) -> None:
        """Stop watching for file changes."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            print("\n👋 Test watcher stopped")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Watcher for Semantic Kernel Python")
    parser.add_argument("--no-auto", action="store_true", help="Don't run tests automatically on file changes")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    cli = TestWatcherCLI()
    
    try:
        cli.setup_watcher(test_on_save=not args.no_auto)
        cli.start_watching()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
