#!/usr/bin/env python3
"""
AGI System Auto-Optimizer
Automatically applies performance optimizations based on system analysis
"""

import json
import os
import sys
import subprocess
import psutil
from pathlib import Path
from datetime import datetime
import logging

class AGISystemOptimizer:
    """Intelligent optimization system for AGI file updates"""

    def __init__(self):
        self.workspace_path = Path("/home/broe/semantic-kernel")
        self.config_path = self.workspace_path / ".agi_file_config.json"
        self.logger = self._setup_logger()
        self.optimizations_applied = []

    def _setup_logger(self):
        """Setup optimization logging"""
        logger = logging.getLogger("AGIOptimizer")
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler(
            self.workspace_path / "agi_optimization.log",
            mode='a',
            encoding='utf-8'
        )

        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def analyze_system_performance(self):
        """Analyze current system performance and identify bottlenecks"""
        analysis = {
            "cpu_cores": psutil.cpu_count(),
            "memory_total_gb": psutil.virtual_memory().total / (1024**3),
            "memory_available_gb": psutil.virtual_memory().available / (1024**3),
            "memory_usage_percent": psutil.virtual_memory().percent,
            "disk_usage_percent": psutil.disk_usage('.').percent,
            "load_average": os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0,
            "has_ssd": self._detect_ssd(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        }

        self.logger.info(f"System analysis: {analysis}")
        return analysis

    def _detect_ssd(self):
        """Detect if primary disk is SSD for I/O optimizations"""
        try:
            # Check disk scheduler - SSDs typically use 'noop' or 'deadline'
            with open('/sys/block/sda/queue/scheduler', 'r') as f:
                scheduler = f.read().strip()
                return 'noop' in scheduler or 'deadline' in scheduler
        except:
            return False

    def load_current_config(self):
        """Load current configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return {}

    def apply_cpu_optimizations(self, config, system_analysis):
        """Apply CPU-specific optimizations"""
        cpu_cores = system_analysis["cpu_cores"]
        load_avg = system_analysis["load_average"]

        # Optimize thread pools based on CPU cores
        if cpu_cores >= 16:  # High-end system
            max_concurrent = min(cpu_cores * 2, 64)
            batch_size = 50
            io_workers = min(cpu_cores, 16)
        elif cpu_cores >= 8:  # Mid-range system
            max_concurrent = cpu_cores * 2
            batch_size = 30
            io_workers = cpu_cores
        else:  # Lower-end system
            max_concurrent = cpu_cores + 2
            batch_size = 20
            io_workers = max(cpu_cores // 2, 2)

        # Adjust for current load
        if load_avg > cpu_cores * 0.8:  # High load
            max_concurrent = max(max_concurrent // 2, 4)
            batch_size = max(batch_size // 2, 10)
            self.logger.warning(f"High CPU load detected ({load_avg:.1f}), reducing concurrency")

        # Apply CPU optimizations
        if "performance_settings" not in config:
            config["performance_settings"] = {}

        config["performance_settings"]["max_concurrent_tasks"] = max_concurrent
        config["performance_settings"]["batch_size"] = batch_size

        if "ultra_performance" not in config:
            config["ultra_performance"] = {}

        config["ultra_performance"]["parallel_io_workers"] = io_workers
        config["ultra_performance"]["enable_process_pool"] = cpu_cores >= 4

        self.optimizations_applied.append(f"CPU optimization: {max_concurrent} max tasks, {batch_size} batch size")
        self.logger.info(f"Applied CPU optimizations for {cpu_cores} cores")

    def apply_memory_optimizations(self, config, system_analysis):
        """Apply memory-specific optimizations"""
        memory_gb = system_analysis["memory_total_gb"]
        memory_usage = system_analysis["memory_usage_percent"]

        # Optimize cache sizes based on available memory
        if memory_gb >= 16:  # High memory system
            cache_size_mb = 2048 if memory_usage < 60 else 1024
            io_buffer_size = 131072
        elif memory_gb >= 8:  # Medium memory system
            cache_size_mb = 1024 if memory_usage < 70 else 512
            io_buffer_size = 65536
        else:  # Lower memory system
            cache_size_mb = 512 if memory_usage < 80 else 256
            io_buffer_size = 32768

        # Apply memory optimizations
        if "ultra_performance" not in config:
            config["ultra_performance"] = {}

        config["ultra_performance"]["cache_size_mb"] = cache_size_mb
        config["ultra_performance"]["io_buffer_size"] = io_buffer_size
        config["ultra_performance"]["enable_memory_mapping"] = memory_gb >= 4

        # Enable compression if memory is limited
        if memory_gb < 8 or memory_usage > 80:
            config["ultra_performance"]["use_compression"] = "lzma"
            config["optimization_flags"]["compress_backups"] = True
            self.optimizations_applied.append("Memory optimization: enabled compression due to memory constraints")

        # Adjust cache TTL based on memory pressure
        if memory_usage > 85:
            config["performance_settings"]["cache_ttl_seconds"] = 300  # Shorter TTL
        else:
            config["performance_settings"]["cache_ttl_seconds"] = 600  # Longer TTL

        self.optimizations_applied.append(f"Memory optimization: {cache_size_mb}MB cache, {io_buffer_size} I/O buffer")
        self.logger.info(f"Applied memory optimizations for {memory_gb:.1f}GB RAM")

    def apply_storage_optimizations(self, config, system_analysis):
        """Apply storage-specific optimizations"""
        has_ssd = system_analysis["has_ssd"]
        disk_usage = system_analysis["disk_usage_percent"]

        if "ultra_performance" not in config:
            config["ultra_performance"] = {}

        if has_ssd:
            # SSD optimizations
            config["ultra_performance"]["enable_prefetching"] = True
            config["ultra_performance"]["atomic_writes"] = True
            config["optimization_flags"]["use_incremental_updates"] = True
            self.optimizations_applied.append("Storage optimization: SSD-specific optimizations enabled")
        else:
            # HDD optimizations
            config["ultra_performance"]["enable_prefetching"] = False
            config["ultra_performance"]["atomic_writes"] = False
            config["performance_settings"]["file_watch_debounce_ms"] = 1000  # Higher debounce for HDDs
            self.optimizations_applied.append("Storage optimization: HDD-specific optimizations enabled")

        # Enable aggressive compression if disk space is limited
        if disk_usage > 85:
            config["ultra_performance"]["use_compression"] = "lzma"
            config["optimization_flags"]["compress_backups"] = True
            self.optimizations_applied.append("Storage optimization: aggressive compression due to disk space")

        self.logger.info(f"Applied storage optimizations (SSD: {has_ssd}, usage: {disk_usage}%)")

    def apply_network_optimizations(self, config):
        """Apply network and I/O optimizations"""
        if "ultra_performance" not in config:
            config["ultra_performance"] = {}

        # Enable uvloop for better async performance
        config["ultra_performance"]["use_uvloop"] = True

        # Enable batch operations
        config["optimization_flags"]["batch_file_operations"] = True
        config["optimization_flags"]["skip_duplicate_operations"] = True

        self.optimizations_applied.append("Network optimization: uvloop and batching enabled")
        self.logger.info("Applied network and I/O optimizations")

    def enable_advanced_features(self, config):
        """Enable advanced performance features"""
        if "optimization_flags" not in config:
            config["optimization_flags"] = {}

        # Enable all optimization flags
        optimizations = {
            "enable_parallel_processing": True,
            "cache_file_analysis": True,
            "use_memory_mapping": True,
            "enable_fast_hashing": True,
            "use_incremental_updates": True,
            "skip_duplicate_operations": True,
            "batch_file_operations": True,
            "compress_backups": True
        }

        config["optimization_flags"].update(optimizations)

        # Enable ultra-performance mode
        if "ultra_performance" not in config:
            config["ultra_performance"] = {}

        ultra_features = {
            "enable_memory_mapping": True,
            "use_compression": "lzma",
            "enable_process_pool": True,
            "enable_prefetching": True,
            "use_uvloop": True,
            "atomic_writes": True
        }

        config["ultra_performance"].update(ultra_features)

        self.optimizations_applied.append("Advanced features: all optimization flags enabled")
        self.logger.info("Enabled all advanced performance features")

    def save_optimized_config(self, config):
        """Save the optimized configuration"""
        # Add optimization metadata
        config["optimization_metadata"] = {
            "last_optimized": datetime.now().isoformat(),
            "optimizations_applied": self.optimizations_applied,
            "optimizer_version": "1.0"
        }

        # Backup original config
        backup_path = self.config_path.with_suffix('.json.backup')
        if self.config_path.exists():
            import shutil
            shutil.copy2(self.config_path, backup_path)
            self.logger.info(f"Backed up original config to {backup_path}")

        # Save optimized config
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2, sort_keys=True)

        self.logger.info(f"Saved optimized configuration with {len(self.optimizations_applied)} optimizations")

    def optimize_system(self):
        """Main optimization workflow"""
        print("🔧 AGI System Auto-Optimizer")
        print("============================")
        print()

        # Analyze system
        print("📊 Analyzing system performance...")
        system_analysis = self.analyze_system_performance()

        print(f"   CPU Cores: {system_analysis['cpu_cores']}")
        print(f"   Memory: {system_analysis['memory_total_gb']:.1f}GB total, {system_analysis['memory_usage_percent']:.1f}% used")
        print(f"   Storage: SSD={system_analysis['has_ssd']}, {system_analysis['disk_usage_percent']:.1f}% used")
        print(f"   Load: {system_analysis['load_average']:.2f}")
        print()

        # Load config
        print("⚙️  Loading current configuration...")
        config = self.load_current_config()
        print()

        # Apply optimizations
        print("🚀 Applying intelligent optimizations...")

        self.apply_cpu_optimizations(config, system_analysis)
        self.apply_memory_optimizations(config, system_analysis)
        self.apply_storage_optimizations(config, system_analysis)
        self.apply_network_optimizations(config)
        self.enable_advanced_features(config)

        # Save optimized config
        print("💾 Saving optimized configuration...")
        self.save_optimized_config(config)
        print()

        # Report results
        print("✅ Optimization complete!")
        print(f"Applied {len(self.optimizations_applied)} optimizations:")
        for opt in self.optimizations_applied:
            print(f"   • {opt}")
        print()

        print("🚀 To use the optimized system:")
        print("   ./launch_agi_ultra_efficient.sh --daemon")
        print()

        return True

def main():
    """Main execution"""
    optimizer = AGISystemOptimizer()

    try:
        success = optimizer.optimize_system()
        if success:
            print("🎉 System optimization successful!")

            # Suggest next steps
            print("\n💡 Recommended next steps:")
            print("   1. ./launch_agi_ultra_efficient.sh --benchmark  # Test performance")
            print("   2. ./check_agi_ultra_status_dashboard.sh        # Monitor status")
            print("   3. ./launch_agi_ultra_efficient.sh --daemon     # Run optimized system")

        else:
            print("❌ Optimization failed")
            return 1

    except Exception as e:
        print(f"❌ Optimization error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
