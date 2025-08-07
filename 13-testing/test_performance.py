#!/usr/bin/env python3
"""
Test module for performance

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import time
import statistics
from typing import List, Dict, Any


class PerformanceTester:
    """Basic performance testing framework."""

    def __init__(self):
        self.results: List[Dict[str, Any]] = []

    def run_test(self, name: str, test_func, iterations: int = 100):
        """Run a performance test."""
        times = []

        for _ in range(iterations):
            start_time = time.perf_counter()
            test_func()
            end_time = time.perf_counter()
            times.append(end_time - start_time)

        result = {
            'name': name,
            'iterations': iterations,
            'mean_time': statistics.mean(times),
            'median_time': statistics.median(times),
            'min_time': min(times),
            'max_time': max(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0
        }

        self.results.append(result)
        return result

    def print_results(self):
        """Print test results."""
        print("\n📊 Performance Test Results:")
        print("=" * 60)

        for result in self.results:
            print(f"\nTest: {result['name']}")
            print(f"  Iterations: {result['iterations']}")
            print(f"  Mean time: {result['mean_time']:.6f}s")
            print(f"  Median time: {result['median_time']:.6f}s")
            print(f"  Min time: {result['min_time']:.6f}s")
            print(f"  Max time: {result['max_time']:.6f}s")
            print(f"  Std deviation: {result['std_dev']:.6f}s")


def simple_computation():
    """Simple computation for testing."""
    return sum(range(1000))


def main():
    """Main test function."""
    print("🚀 AGI Optimization Performance Testing!")

    tester = PerformanceTester()

    # Run basic performance tests
    tester.run_test("Simple Computation", simple_computation, 1000)

    # Print results
    tester.print_results()

    print("\n✅ Performance testing complete!")


if __name__ == "__main__":
    main()
