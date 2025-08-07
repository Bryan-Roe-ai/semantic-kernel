#!/usr/bin/env python3
"""
Comprehensive performance benchmarking suite for sequential patterns

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Performance benchmarking and optimization validation.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import asyncio
import statistics
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import psutil

from semantic_kernel.agents.strategies.selection.batch_sequential_selection_strategy import (
    BatchSequentialSelectionStrategy
)
from semantic_kernel.agents.strategies.selection.sequential_selection_strategy import (
    SequentialSelectionStrategy
)
from semantic_kernel.contents.chat_message_content import ChatMessageContent


@dataclass
class BenchmarkResult:
    """Results from a performance benchmark test."""
    test_name: str
    total_operations: int
    total_time_seconds: float
    operations_per_second: float
    average_operation_time_ms: float
    min_operation_time_ms: float
    max_operation_time_ms: float
    memory_usage_mb: float
    cpu_usage_percent: float
    success_rate: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return (
            f"{self.test_name}:\n"
            f"  Operations/sec: {self.operations_per_second:.2f}\n"
            f"  Avg time: {self.average_operation_time_ms:.2f}ms\n"
            f"  Success rate: {self.success_rate:.1%}\n"
            f"  Memory: {self.memory_usage_mb:.1f}MB\n"
            f"  CPU: {self.cpu_usage_percent:.1f}%"
        )


class MockAgent:
    """Mock agent for benchmarking."""
    
    def __init__(self, agent_id: str, processing_delay_ms: float = 1.0):
        self.id = agent_id
        self.name = f"Agent_{agent_id}"
        self.plugins = []
        self.processing_delay_ms = processing_delay_ms
    
    async def process(self, input_data: Any) -> Any:
        """Simulate agent processing."""
        await asyncio.sleep(self.processing_delay_ms / 1000)
        return f"Processed by {self.id}: {input_data}"


class SequentialPatternsBenchmark:
    """Comprehensive benchmarking suite for sequential patterns."""
    
    def __init__(self):
        self.results: List[BenchmarkResult] = []
        self.baseline_metrics: Optional[Dict[str, float]] = None
    
    async def run_all_benchmarks(self) -> List[BenchmarkResult]:
        """Run all performance benchmarks."""
        print("🚀 Starting Sequential Patterns Performance Benchmarks")
        print("=" * 60)
        
        # Agent selection benchmarks
        await self.benchmark_basic_sequential_selection()
        await self.benchmark_cached_sequential_selection()
        await self.benchmark_batch_sequential_selection()
        
        # Scalability benchmarks
        await self.benchmark_agent_count_scalability()
        await self.benchmark_history_length_impact()
        
        # Stress tests
        await self.benchmark_concurrent_operations()
        await self.benchmark_memory_pressure()
        
        # Real-world scenarios
        await self.benchmark_conversation_simulation()
        await self.benchmark_enterprise_workflow()
        
        print("\n📊 Benchmark Summary")
        print("=" * 60)
        self.print_results_summary()
        
        return self.results
    
    async def benchmark_basic_sequential_selection(self):
        """Benchmark basic sequential selection strategy."""
        print("\n🔄 Benchmarking Basic Sequential Selection...")
        
        agents = [MockAgent(f"agent-{i}") for i in range(10)]
        strategy = SequentialSelectionStrategy()
        history = [ChatMessageContent(role="user", content="Test message")]
        
        await self._run_benchmark(
            "Basic Sequential Selection",
            self._selection_operation,
            iterations=1000,
            strategy=strategy,
            agents=agents,
            history=history
        )
    
    async def benchmark_cached_sequential_selection(self):
        """Benchmark cached sequential selection with various cache configurations."""
        print("\n💾 Benchmarking Cached Sequential Selection...")
        
        # Note: This would use CachedSequentialSelectionStrategy when available
        # For now, we'll simulate caching behavior
        agents = [MockAgent(f"agent-{i}") for i in range(10)]
        
        # Simulate cached strategy with manual caching
        cache = {}
        strategy = SequentialSelectionStrategy()
        history = [ChatMessageContent(role="user", content="Test message")]
        
        async def cached_selection_operation():
            cache_key = f"{len(agents)}_{len(history)}"
            if cache_key not in cache:
                result = await strategy.next(agents, history)
                cache[cache_key] = result
                return result
            return cache[cache_key]
        
        await self._run_benchmark(
            "Cached Sequential Selection",
            cached_selection_operation,
            iterations=1000
        )
    
    async def benchmark_batch_sequential_selection(self):
        """Benchmark batch sequential selection strategy."""
        print("\n📦 Benchmarking Batch Sequential Selection...")
        
        agents = [MockAgent(f"agent-{i}") for i in range(10)]
        strategy = BatchSequentialSelectionStrategy(
            initial_batch_size=5,
            enable_adaptive_batching=True,
            enable_caching=True
        )
        history = [ChatMessageContent(role="user", content="Test message")]
        
        await self._run_benchmark(
            "Batch Sequential Selection",
            self._selection_operation,
            iterations=1000,
            strategy=strategy,
            agents=agents,
            history=history
        )
    
    async def benchmark_agent_count_scalability(self):
        """Benchmark scalability with different agent counts."""
        print("\n📈 Benchmarking Agent Count Scalability...")
        
        agent_counts = [5, 10, 25, 50, 100]
        
        for count in agent_counts:
            print(f"  Testing with {count} agents...")
            
            agents = [MockAgent(f"agent-{i}") for i in range(count)]
            strategy = BatchSequentialSelectionStrategy(
                initial_batch_size=min(5, count // 2),
                max_batch_size=min(20, count),
                enable_adaptive_batching=True
            )
            history = [ChatMessageContent(role="user", content="Scalability test")]
            
            await self._run_benchmark(
                f"Scalability Test - {count} Agents",
                self._selection_operation,
                iterations=200,
                strategy=strategy,
                agents=agents,
                history=history
            )
    
    async def benchmark_history_length_impact(self):
        """Benchmark impact of conversation history length."""
        print("\n📜 Benchmarking History Length Impact...")
        
        agents = [MockAgent(f"agent-{i}") for i in range(10)]
        strategy = BatchSequentialSelectionStrategy()
        
        history_lengths = [1, 10, 50, 100, 500]
        
        for length in history_lengths:
            print(f"  Testing with {length} history messages...")
            
            history = [
                ChatMessageContent(role="user" if i % 2 == 0 else "assistant", 
                                 content=f"Message {i}")
                for i in range(length)
            ]
            
            await self._run_benchmark(
                f"History Length Test - {length} Messages",
                self._selection_operation,
                iterations=200,
                strategy=strategy,
                agents=agents,
                history=history
            )
    
    async def benchmark_concurrent_operations(self):
        """Benchmark concurrent selection operations."""
        print("\n🔀 Benchmarking Concurrent Operations...")
        
        agents = [MockAgent(f"agent-{i}") for i in range(20)]
        strategy = BatchSequentialSelectionStrategy(
            max_parallel_steps=10,
            enable_caching=True
        )
        history = [ChatMessageContent(role="user", content="Concurrent test")]
        
        async def concurrent_operation():
            tasks = [
                strategy.next(agents, history)
                for _ in range(10)  # 10 concurrent selections
            ]
            await asyncio.gather(*tasks)
        
        await self._run_benchmark(
            "Concurrent Operations (10 parallel)",
            concurrent_operation,
            iterations=50
        )
    
    async def benchmark_memory_pressure(self):
        """Benchmark performance under memory pressure."""
        print("\n💾 Benchmarking Memory Pressure...")
        
        # Create large number of agents with history
        agents = [MockAgent(f"agent-{i}") for i in range(100)]
        strategy = BatchSequentialSelectionStrategy(
            enable_caching=True,
            cache_ttl_seconds=300
        )
        
        # Create large conversation history
        history = [
            ChatMessageContent(role="user" if i % 2 == 0 else "assistant", 
                             content=f"Large conversation message {i} with extended content to increase memory usage")
            for i in range(200)
        ]
        
        await self._run_benchmark(
            "Memory Pressure Test",
            self._selection_operation,
            iterations=100,
            strategy=strategy,
            agents=agents,
            history=history
        )
    
    async def benchmark_conversation_simulation(self):
        """Benchmark realistic conversation simulation."""
        print("\n💬 Benchmarking Conversation Simulation...")
        
        # Simulate a multi-agent conversation
        agents = [
            MockAgent("researcher", 50),    # Slower research agent
            MockAgent("analyst", 30),       # Medium analysis agent
            MockAgent("writer", 20),        # Fast writing agent
            MockAgent("reviewer", 40)       # Medium review agent
        ]
        
        strategy = BatchSequentialSelectionStrategy(
            enable_adaptive_batching=True,
            priority_boost_factor=1.5
        )
        
        async def conversation_simulation():
            history = []
            
            # Simulate 20-turn conversation
            for turn in range(20):
                # Add user message
                history.append(ChatMessageContent(role="user", content=f"User input {turn}"))
                
                # Select agent and simulate response
                agent = await strategy.next(agents, history)
                await agent.process(f"Processing turn {turn}")
                
                # Add agent response
                history.append(ChatMessageContent(role="assistant", content=f"Response {turn}", name=agent.name))
                
                # Occasionally clean history to simulate real usage
                if len(history) > 50:
                    history = history[-30:]  # Keep last 30 messages
        
        await self._run_benchmark(
            "Conversation Simulation (20 turns)",
            conversation_simulation,
            iterations=10
        )
    
    async def benchmark_enterprise_workflow(self):
        """Benchmark enterprise-scale workflow simulation."""
        print("\n🏢 Benchmarking Enterprise Workflow...")
        
        # Large enterprise agent pool
        agent_types = ["planning", "research", "analysis", "validation", "reporting", "approval"]
        agents = []
        
        for agent_type in agent_types:
            for i in range(5):  # 5 agents per type
                processing_time = 100 if agent_type in ["analysis", "validation"] else 50
                agents.append(MockAgent(f"{agent_type}-{i}", processing_time))
        
        strategy = BatchSequentialSelectionStrategy(
            initial_batch_size=10,
            max_batch_size=30,
            enable_adaptive_batching=True,
            enable_caching=True
        )
        
        # Pre-optimize for the agent set
        await strategy.optimize_for_agents(agents)
        
        async def enterprise_workflow():
            # Simulate complex enterprise workflow
            workflows = [
                "document_review_workflow",
                "compliance_check_workflow", 
                "risk_assessment_workflow",
                "approval_workflow"
            ]
            
            for workflow in workflows:
                history = [ChatMessageContent(role="system", content=f"Starting {workflow}")]
                
                # Each workflow has multiple steps
                for step in range(8):
                    agent = await strategy.next(agents, history)
                    await agent.process(f"{workflow}_step_{step}")
                    
                    history.append(ChatMessageContent(
                        role="assistant", 
                        content=f"Completed {workflow} step {step}",
                        name=agent.name
                    ))
        
        await self._run_benchmark(
            "Enterprise Workflow (4 workflows x 8 steps)",
            enterprise_workflow,
            iterations=5
        )
    
    async def _selection_operation(self, strategy, agents, history):
        """Basic selection operation for benchmarking."""
        return await strategy.next(agents, history)
    
    async def _run_benchmark(
        self, 
        test_name: str, 
        operation_func, 
        iterations: int, 
        **kwargs
    ):
        """Run a benchmark test and collect metrics."""
        
        # Collect initial system metrics
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        operation_times = []
        successful_operations = 0
        
        # Warm-up runs
        try:
            for _ in range(min(10, iterations // 10)):
                await operation_func(**kwargs)
        except Exception:
            pass  # Ignore warm-up errors
        
        # Actual benchmark
        start_time = time.time()
        
        for i in range(iterations):
            operation_start = time.time()
            
            try:
                await operation_func(**kwargs)
                successful_operations += 1
            except Exception as e:
                print(f"    Operation {i} failed: {e}")
            
            operation_end = time.time()
            operation_times.append((operation_end - operation_start) * 1000)  # Convert to ms
            
            # Progress indicator
            if (i + 1) % (iterations // 10) == 0:
                progress = ((i + 1) / iterations) * 100
                print(f"    Progress: {progress:.0f}%")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Collect final system metrics
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        cpu_percent = process.cpu_percent()
        
        # Calculate statistics
        if operation_times:
            avg_operation_time = statistics.mean(operation_times)
            min_operation_time = min(operation_times)
            max_operation_time = max(operation_times)
        else:
            avg_operation_time = 0
            min_operation_time = 0
            max_operation_time = 0
        
        operations_per_second = successful_operations / total_time if total_time > 0 else 0
        success_rate = successful_operations / iterations if iterations > 0 else 0
        
        result = BenchmarkResult(
            test_name=test_name,
            total_operations=iterations,
            total_time_seconds=total_time,
            operations_per_second=operations_per_second,
            average_operation_time_ms=avg_operation_time,
            min_operation_time_ms=min_operation_time,
            max_operation_time_ms=max_operation_time,
            memory_usage_mb=final_memory - initial_memory,
            cpu_usage_percent=cpu_percent,
            success_rate=success_rate,
            metadata=kwargs
        )
        
        self.results.append(result)
        print(f"  ✅ {result}")
        
        return result
    
    def print_results_summary(self):
        """Print a summary of all benchmark results."""
        if not self.results:
            print("No benchmark results available.")
            return
        
        print("\n📋 Detailed Results:")
        print("-" * 80)
        
        for result in self.results:
            print(f"\n{result.test_name}:")
            print(f"  Operations/sec: {result.operations_per_second:8.2f}")
            print(f"  Avg time (ms):  {result.average_operation_time_ms:8.2f}")
            print(f"  Min time (ms):  {result.min_operation_time_ms:8.2f}")
            print(f"  Max time (ms):  {result.max_operation_time_ms:8.2f}")
            print(f"  Success rate:   {result.success_rate:8.1%}")
            print(f"  Memory (MB):    {result.memory_usage_mb:8.1f}")
            print(f"  CPU (%):        {result.cpu_usage_percent:8.1f}")
        
        # Performance comparison
        print("\n🏆 Performance Rankings (by operations/sec):")
        sorted_results = sorted(self.results, key=lambda r: r.operations_per_second, reverse=True)
        
        for i, result in enumerate(sorted_results[:5], 1):
            print(f"  {i}. {result.test_name}: {result.operations_per_second:.2f} ops/sec")
        
        # Memory efficiency
        print("\n💾 Memory Efficiency (lowest memory usage):")
        memory_sorted = sorted(self.results, key=lambda r: r.memory_usage_mb)
        
        for i, result in enumerate(memory_sorted[:5], 1):
            print(f"  {i}. {result.test_name}: {result.memory_usage_mb:.1f} MB")
        
        # Scalability insights
        print("\n📈 Scalability Insights:")
        scalability_tests = [r for r in self.results if "Scalability" in r.test_name]
        
        if scalability_tests:
            for result in scalability_tests:
                agent_count = result.metadata.get("agents", [])
                if hasattr(agent_count, '__len__'):
                    count = len(agent_count)
                    efficiency = result.operations_per_second / count if count > 0 else 0
                    print(f"  {count} agents: {efficiency:.2f} ops/sec per agent")
    
    def export_results_to_csv(self, filename: str = "benchmark_results.csv"):
        """Export benchmark results to CSV file."""
        import csv
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = [
                'test_name', 'total_operations', 'total_time_seconds',
                'operations_per_second', 'average_operation_time_ms',
                'min_operation_time_ms', 'max_operation_time_ms',
                'memory_usage_mb', 'cpu_usage_percent', 'success_rate'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in self.results:
                writer.writerow({
                    'test_name': result.test_name,
                    'total_operations': result.total_operations,
                    'total_time_seconds': result.total_time_seconds,
                    'operations_per_second': result.operations_per_second,
                    'average_operation_time_ms': result.average_operation_time_ms,
                    'min_operation_time_ms': result.min_operation_time_ms,
                    'max_operation_time_ms': result.max_operation_time_ms,
                    'memory_usage_mb': result.memory_usage_mb,
                    'cpu_usage_percent': result.cpu_usage_percent,
                    'success_rate': result.success_rate
                })
        
        print(f"📊 Results exported to {filename}")


async def main():
    """Run the complete benchmark suite."""
    benchmark = SequentialPatternsBenchmark()
    
    try:
        results = await benchmark.run_all_benchmarks()
        
        # Export results
        benchmark.export_results_to_csv()
        
        print(f"\n🎉 Benchmarking completed! {len(results)} tests executed.")
        
        # Summary statistics
        total_operations = sum(r.total_operations for r in results)
        avg_success_rate = sum(r.success_rate for r in results) / len(results) if results else 0
        
        print(f"📊 Total operations: {total_operations:,}")
        print(f"📊 Average success rate: {avg_success_rate:.1%}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Benchmarking interrupted by user")
    except Exception as e:
        print(f"\n❌ Benchmarking failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
