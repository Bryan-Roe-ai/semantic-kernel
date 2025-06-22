#!/usr/bin/env python3
"""
Automated Test Runner for Semantic Kernel Python

This script provides comprehensive test automation including:
- Test discovery and execution
- Coverage reporting
- Test result analysis
- Parallel test execution
- Integration with CI/CD
"""

import argparse
import asyncio
import json
import logging
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import pytest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    """Test result data structure."""
    name: str
    status: str  # "passed", "failed", "skipped", "error"
    duration: float
    error_message: Optional[str] = None
    output: Optional[str] = None


@dataclass
class TestSuite:
    """Test suite configuration."""
    name: str
    path: Path
    pattern: str
    timeout: int = 300
    parallel: bool = True
    coverage: bool = True


class AutoTestRunner:
    """Automated test runner with advanced features."""

    def __init__(self, root_dir: Optional[Path] = None):
        """Initialize the test runner."""
        self.root_dir = root_dir or Path(__file__).parent.parent
        self.tests_dir = self.root_dir / "tests"
        self.reports_dir = self.root_dir / "test_reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        # Test suites configuration
        self.test_suites = [
            TestSuite("unit", self.tests_dir / "unit", "**/test_*.py"),
            TestSuite("integration", self.tests_dir / "integration", "**/test_*.py"),
            TestSuite("samples", self.tests_dir / "samples", "**/test_*.py"),
        ]
        
        self.results: List[TestResult] = []

    def discover_tests(self, pattern: str = "test_*.py") -> List[Path]:
        """Discover test files matching the pattern."""
        logger.info(f"Discovering tests with pattern: {pattern}")
        test_files = []
        
        for test_file in self.tests_dir.rglob(pattern):
            if test_file.is_file() and test_file.suffix == ".py":
                test_files.append(test_file)
        
        logger.info(f"Found {len(test_files)} test files")
        return sorted(test_files)

    def run_pytest_command(self, args: List[str], timeout: int = 300) -> Tuple[int, str, str]:
        """Run pytest with given arguments."""
        cmd = [sys.executable, "-m", "pytest"] + args
        logger.info(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.root_dir
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            logger.error(f"Test execution timed out after {timeout} seconds")
            return -1, "", "Test execution timed out"

    def run_unit_tests(self, coverage: bool = True, parallel: bool = True) -> TestResult:
        """Run unit tests with optional coverage and parallelization."""
        logger.info("Running unit tests...")
        start_time = time.time()
        
        args = [
            "tests/unit",
            "-v",
            "--tb=short",
            "-ra",
        ]
        
        if coverage:
            args.extend([
                "--cov=semantic_kernel",
                "--cov-report=term-missing",
                "--cov-report=xml:test_reports/coverage_unit.xml",
                "--cov-report=html:test_reports/htmlcov_unit",
            ])
        
        if parallel:
            # Use number of CPU cores for parallel execution
            import multiprocessing
            num_cores = multiprocessing.cpu_count()
            args.extend(["-n", str(num_cores)])
        
        # Add timeout for individual tests
        args.extend(["--timeout=60"])
        
        returncode, stdout, stderr = self.run_pytest_command(args)
        duration = time.time() - start_time
        
        status = "passed" if returncode == 0 else "failed"
        error_msg = stderr if returncode != 0 else None
        
        return TestResult(
            name="unit_tests",
            status=status,
            duration=duration,
            error_message=error_msg,
            output=stdout
        )

    def run_integration_tests(self, coverage: bool = True) -> TestResult:
        """Run integration tests."""
        logger.info("Running integration tests...")
        start_time = time.time()
        
        args = [
            "tests/integration",
            "-v",
            "--tb=short",
            "-ra",
            "--timeout=120",
        ]
        
        if coverage:
            args.extend([
                "--cov=semantic_kernel",
                "--cov-report=xml:test_reports/coverage_integration.xml",
                "--cov-report=html:test_reports/htmlcov_integration",
            ])
        
        returncode, stdout, stderr = self.run_pytest_command(args, timeout=600)
        duration = time.time() - start_time
        
        status = "passed" if returncode == 0 else "failed"
        error_msg = stderr if returncode != 0 else None
        
        return TestResult(
            name="integration_tests",
            status=status,
            duration=duration,
            error_message=error_msg,
            output=stdout
        )

    def run_sample_tests(self) -> TestResult:
        """Run sample tests."""
        logger.info("Running sample tests...")
        start_time = time.time()
        
        args = [
            "tests/samples",
            "-v",
            "--tb=short",
            "-ra",
            "--timeout=180",
        ]
        
        returncode, stdout, stderr = self.run_pytest_command(args, timeout=900)
        duration = time.time() - start_time
        
        status = "passed" if returncode == 0 else "failed"
        error_msg = stderr if returncode != 0 else None
        
        return TestResult(
            name="sample_tests",
            status=status,
            duration=duration,
            error_message=error_msg,
            output=stdout
        )

    def run_security_tests(self) -> TestResult:
        """Run security tests using bandit."""
        logger.info("Running security tests...")
        start_time = time.time()
        
        try:
            cmd = [
                sys.executable, "-m", "bandit",
                "-r", "semantic_kernel",
                "-f", "json",
                "-o", "test_reports/bandit_report.json"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.root_dir
            )
            
            duration = time.time() - start_time
            status = "passed" if result.returncode == 0 else "failed"
            error_msg = result.stderr if result.returncode != 0 else None
            
            return TestResult(
                name="security_tests",
                status=status,
                duration=duration,
                error_message=error_msg,
                output=result.stdout
            )
        except FileNotFoundError:
            logger.warning("Bandit not found, skipping security tests")
            return TestResult(
                name="security_tests",
                status="skipped",
                duration=0,
                error_message="Bandit not installed"
            )

    def run_linting(self) -> TestResult:
        """Run linting with ruff."""
        logger.info("Running linting...")
        start_time = time.time()
        
        try:
            cmd = [
                sys.executable, "-m", "ruff",
                "check",
                "semantic_kernel",
                "--output-format=json",
                "--output-file=test_reports/ruff_report.json"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.root_dir
            )
            
            duration = time.time() - start_time
            status = "passed" if result.returncode == 0 else "failed"
            error_msg = result.stderr if result.returncode != 0 else None
            
            return TestResult(
                name="linting",
                status=status,
                duration=duration,
                error_message=error_msg,
                output=result.stdout
            )
        except FileNotFoundError:
            logger.warning("Ruff not found, skipping linting")
            return TestResult(
                name="linting",
                status="skipped",
                duration=0,
                error_message="Ruff not installed"
            )

    def run_type_checking(self) -> TestResult:
        """Run type checking with mypy."""
        logger.info("Running type checking...")
        start_time = time.time()
        
        try:
            cmd = [
                sys.executable, "-m", "mypy",
                "semantic_kernel",
                "--strict",
                "--show-error-codes",
                "--junit-xml=test_reports/mypy_report.xml"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.root_dir
            )
            
            duration = time.time() - start_time
            status = "passed" if result.returncode == 0 else "failed"
            error_msg = result.stderr if result.returncode != 0 else None
            
            return TestResult(
                name="type_checking",
                status=status,
                duration=duration,
                error_message=error_msg,
                output=result.stdout
            )
        except FileNotFoundError:
            logger.warning("MyPy not found, skipping type checking")
            return TestResult(
                name="type_checking",
                status="skipped",
                duration=0,
                error_message="MyPy not installed"
            )

    def run_all_tests(self, include_integration: bool = True, include_samples: bool = True) -> List[TestResult]:
        """Run all test suites."""
        logger.info("Running all tests...")
        results = []
        
        # Run tests in order of importance
        test_functions = [
            ("unit", self.run_unit_tests),
            ("linting", self.run_linting),
            ("type_checking", self.run_type_checking),
            ("security", self.run_security_tests),
        ]
        
        if include_integration:
            test_functions.append(("integration", self.run_integration_tests))
        
        if include_samples:
            test_functions.append(("samples", self.run_sample_tests))
        
        for test_name, test_func in test_functions:
            try:
                result = test_func()
                results.append(result)
                logger.info(f"{test_name} tests: {result.status} ({result.duration:.2f}s)")
                
                if result.status == "failed":
                    logger.error(f"{test_name} tests failed: {result.error_message}")
            except Exception as e:
                logger.error(f"Error running {test_name} tests: {e}")
                results.append(TestResult(
                    name=test_name,
                    status="error",
                    duration=0,
                    error_message=str(e)
                ))
        
        self.results = results
        return results

    def generate_report(self, output_format: str = "json") -> None:
        """Generate test report in specified format."""
        if not self.results:
            logger.warning("No test results to report")
            return
        
        report_data = {
            "timestamp": time.time(),
            "total_tests": len(self.results),
            "passed": len([r for r in self.results if r.status == "passed"]),
            "failed": len([r for r in self.results if r.status == "failed"]),
            "skipped": len([r for r in self.results if r.status == "skipped"]),
            "errors": len([r for r in self.results if r.status == "error"]),
            "total_duration": sum(r.duration for r in self.results),
            "results": [
                {
                    "name": r.name,
                    "status": r.status,
                    "duration": r.duration,
                    "error_message": r.error_message
                }
                for r in self.results
            ]
        }
        
        if output_format == "json":
            report_file = self.reports_dir / "test_report.json"
            with open(report_file, "w") as f:
                json.dump(report_data, f, indent=2)
            logger.info(f"Test report saved to {report_file}")
        
        # Also print summary
        self.print_summary()

    def print_summary(self) -> None:
        """Print test results summary."""
        if not self.results:
            return
        
        passed = len([r for r in self.results if r.status == "passed"])
        failed = len([r for r in self.results if r.status == "failed"])
        skipped = len([r for r in self.results if r.status == "skipped"])
        errors = len([r for r in self.results if r.status == "error"])
        total_duration = sum(r.duration for r in self.results)
        
        print("\n" + "="*60)
        print("TEST RESULTS SUMMARY")
        print("="*60)
        print(f"Total tests: {len(self.results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Skipped: {skipped}")
        print(f"Errors: {errors}")
        print(f"Total duration: {total_duration:.2f}s")
        print("="*60)
        
        for result in self.results:
            status_emoji = {
                "passed": "✅",
                "failed": "❌",
                "skipped": "⚠️",
                "error": "💥"
            }
            print(f"{status_emoji.get(result.status, '❓')} {result.name}: {result.status} ({result.duration:.2f}s)")
            if result.error_message:
                print(f"   Error: {result.error_message}")
        
        print("="*60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Automated Test Runner for Semantic Kernel Python")
    parser.add_argument("--unit-only", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration-only", action="store_true", help="Run only integration tests")
    parser.add_argument("--samples-only", action="store_true", help="Run only sample tests")
    parser.add_argument("--no-coverage", action="store_true", help="Disable coverage reporting")
    parser.add_argument("--no-parallel", action="store_true", help="Disable parallel execution")
    parser.add_argument("--report-format", choices=["json", "xml"], default="json", help="Report format")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    runner = AutoTestRunner()
    
    try:
        if args.unit_only:
            results = [runner.run_unit_tests(coverage=not args.no_coverage, parallel=not args.no_parallel)]
        elif args.integration_only:
            results = [runner.run_integration_tests(coverage=not args.no_coverage)]
        elif args.samples_only:
            results = [runner.run_sample_tests()]
        else:
            results = runner.run_all_tests()
        
        runner.generate_report(output_format=args.report_format)
        
        # Exit with non-zero code if any tests failed
        if any(r.status in ["failed", "error"] for r in results):
            sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Test execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
