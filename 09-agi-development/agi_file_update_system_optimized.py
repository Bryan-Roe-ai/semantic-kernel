#!/usr/bin/env python3
"""
AGI module for agi file update system optimized

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import os
import sys
import json
import asyncio
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Set
from dataclasses import dataclass, field
from enum import Enum
import subprocess
import shutil
import hashlib
import uuid
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import lru_cache, wraps
import threading
from collections import defaultdict, deque
import gzip
import pickle
from weakref import WeakValueDictionary

# Performance imports
import multiprocessing as mp
from queue import Queue, PriorityQueue
import asyncio.locks

# Add semantic kernel path
sys.path.append('/home/broe/semantic-kernel/python')

# Lazy imports for better startup performance
_torch = None
_np = None
_sk = None

def get_torch():
    global _torch
    if _torch is None:
        import torch
        _torch = torch
    return _torch

def get_numpy():
    global _np
    if _np is None:
        import numpy as np
        _np = np
    return _np

def get_semantic_kernel():
    global _sk
    if _sk is None:
        import semantic_kernel as sk
        _sk = sk
    return _sk

@dataclass
class PerformanceMetrics:
    """Track system performance metrics"""
    tasks_processed: int = 0
    tasks_failed: int = 0
    avg_processing_time: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    total_files_processed: int = 0
    total_backups_created: int = 0

    def update_avg_time(self, new_time: float):
        if self.tasks_processed == 0:
            self.avg_processing_time = new_time
        else:
            self.avg_processing_time = (self.avg_processing_time * self.tasks_processed + new_time) / (self.tasks_processed + 1)

@dataclass
class FileUpdateTask:
    """Optimized file update task with priority and caching"""
    file_path: Path
    operation: str
    content: str = ""
    target_line: Optional[int] = None
    backup: bool = True
    priority: int = 5  # 1-10, lower is higher priority
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "pending"
    result: Any = None
    error: Optional[str] = None
    dependencies: Set[str] = field(default_factory=set)
    file_hash: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.file_path, str):
            self.file_path = Path(self.file_path)

    def __lt__(self, other):
        return self.priority < other.priority

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "file_path": str(self.file_path),
            "operation": self.operation,
            "content": self.content[:100] + "..." if len(self.content) > 100 else self.content,
            "target_line": self.target_line,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
            "priority": self.priority,
            "file_hash": self.file_hash
        }

class FileCache:
    """High-performance file caching system"""

    def __init__(self, max_size=1000, ttl_seconds=300):
        self.cache = {}
        self.access_times = {}
        self.file_hashes = {}
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.lock = threading.RLock()

    def _cleanup_expired(self):
        """Remove expired cache entries"""
        now = time.time()
        expired_keys = [
            key for key, access_time in self.access_times.items()
            if now - access_time > self.ttl
        ]
        for key in expired_keys:
            self._remove_entry(key)

    def _remove_entry(self, key):
        """Remove cache entry"""
        self.cache.pop(key, None)
        self.access_times.pop(key, None)
        self.file_hashes.pop(key, None)

    def get(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Get cached file analysis"""
        with self.lock:
            key = str(file_path)

            # Check if file has changed
            if key in self.file_hashes:
                current_hash = self._get_file_hash(file_path)
                if current_hash != self.file_hashes[key]:
                    self._remove_entry(key)
                    return None

            if key in self.cache:
                self.access_times[key] = time.time()
                return self.cache[key].copy()
            return None

    def set(self, file_path: Path, data: Dict[str, Any]):
        """Cache file analysis"""
        with self.lock:
            key = str(file_path)

            # Cleanup if needed
            if len(self.cache) >= self.max_size:
                self._cleanup_expired()

                # If still full, remove oldest
                if len(self.cache) >= self.max_size:
                    oldest_key = min(self.access_times.keys(), key=self.access_times.get)
                    self._remove_entry(oldest_key)

            self.cache[key] = data.copy()
            self.access_times[key] = time.time()
            self.file_hashes[key] = self._get_file_hash(file_path)

    def _get_file_hash(self, file_path: Path) -> str:
        """Get file hash for change detection"""
        try:
            if not file_path.exists():
                return ""
            stat = file_path.stat()
            return f"{stat.st_mtime}_{stat.st_size}"
        except:
            return ""

class OptimizedFileUpdater:
    """High-performance autonomous file updater with advanced optimization"""

    def __init__(self):
        self.workspace_path = Path("/home/broe/semantic-kernel")
        self.config_path = self.workspace_path / ".agi_file_config.json"
        self.backup_path = self.workspace_path / ".agi_backups"

        # Load configuration
        self.config = self._load_config()
        self.perf_settings = self.config.get("performance_settings", {})
        self.optimization_flags = self.config.get("optimization_flags", {})

        # Performance components
        self.file_cache = FileCache(
            max_size=1000,
            ttl_seconds=self.perf_settings.get("cache_ttl_seconds", 300)
        )
        self.metrics = PerformanceMetrics()

        # Task management
        self.task_queue = PriorityQueue()
        self.active_tasks = {}
        self.completed_tasks = deque(maxlen=1000)

        # Threading and async
        self.executor = ThreadPoolExecutor(
            max_workers=self.perf_settings.get("max_concurrent_tasks", 5)
        )
        self.task_lock = asyncio.Lock()

        # Safety constraints (loaded from config)
        self.safe_directories = self.config.get("safe_directories", [])
        self.restricted_files = self.config.get("restricted_files", [])

        # Optimization state
        self.file_watchers = {}
        self.batch_operations = defaultdict(list)
        self.last_batch_time = time.time()

        # Setup
        self.backup_path.mkdir(exist_ok=True)
        self.logger = self._setup_optimized_logger()

        self.logger.info("🚀 Optimized AGI File Updater initialized")
        self.logger.info(f"📁 Workspace: {self.workspace_path}")
        self.logger.info(f"💾 Backups: {self.backup_path}")
        self.logger.info(f"⚡ Performance mode: {'Enabled' if self.perf_settings.get('enable_parallel_processing', True) else 'Standard'}")

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration with caching"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._create_default_config()
        except Exception as e:
            self.logger.error(f"Config load error: {e}")
            return self._create_default_config()

    def _create_default_config(self) -> Dict[str, Any]:
        """Create optimized default configuration"""
        default_config = {
            "safe_directories": [str(self.workspace_path)],
            "restricted_files": [".git", ".env", "secrets", "credentials", "password"],
            "workspace_path": str(self.workspace_path),
            "backup_path": str(self.backup_path),
            "performance_settings": {
                "max_concurrent_tasks": 5,
                "batch_size": 10,
                "cache_ttl_seconds": 300,
                "enable_parallel_processing": True,
                "use_file_hashing": True,
                "lazy_load_models": True
            },
            "optimization_flags": {
                "skip_duplicate_operations": True,
                "compress_backups": True,
                "batch_file_operations": True,
                "cache_file_analysis": True,
                "use_incremental_updates": True
            }
        }

        # Save default config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save default config: {e}")

        return default_config

    def _setup_optimized_logger(self):
        """Setup high-performance logging"""
        logger = logging.getLogger("OptimizedAGI_FileUpdater")
        logger.setLevel(logging.INFO)

        # Clear existing handlers
        logger.handlers.clear()

        # Optimized file handler with buffering
        log_file = self.workspace_path / "agi_file_updates.log"
        fh = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        fh.setLevel(logging.INFO)

        # Optimized formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        return logger

    @lru_cache(maxsize=1000)
    def _is_safe_file_cached(self, file_path_str: str) -> tuple[bool, str]:
        """Cached safety check for better performance"""
        file_path = Path(file_path_str)

        # Check safe directories
        file_str = str(file_path.absolute())
        in_safe_dir = any(file_str.startswith(safe_dir) for safe_dir in self.safe_directories)

        if not in_safe_dir:
            return False, f"File not in approved directories"

        # Check restricted patterns
        for restricted in self.restricted_files:
            if restricted.lower() in str(file_path).lower():
                return False, f"Contains restricted pattern: {restricted}"

        return True, "Operation approved"

    def is_safe_operation(self, file_path: Path, operation: str) -> tuple[bool, str]:
        """Optimized safety check"""
        # Use cached check
        is_safe, reason = self._is_safe_file_cached(str(file_path))
        if not is_safe:
            return False, reason

        # Check file permissions for existing files
        if file_path.exists() and not os.access(file_path, os.W_OK):
            return False, "No write permission"

        # Additional safety checks
        if operation == "delete" and file_path.suffix in [".py", ".cs", ".ts", ".js"]:
            return False, "Source file deletion requires manual approval"

        return True, "Operation approved"

    def _get_file_hash(self, file_path: Path) -> Optional[str]:
        """Fast file hashing for change detection"""
        if not self.optimization_flags.get("use_file_hashing", True):
            return None

        try:
            if not file_path.exists():
                return None

            # Use file metadata for fast hashing - secure version
            stat = file_path.stat()
            # Use SHA256 for better security and include more entropy
            hash_input = f"{stat.st_mtime}_{stat.st_size}_{file_path}_{stat.st_ino}".encode()
            return hashlib.sha256(hash_input).hexdigest()[:16]
        except Exception:
            return None

    def create_optimized_backup(self, file_path: Path) -> Optional[Path]:
        """Optimized backup creation with compression"""
        if not file_path.exists():
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.backup"

        # Add compression if enabled
        if self.optimization_flags.get("compress_backups", True):
            backup_name += ".gz"
            backup_file = self.backup_path / backup_name

            try:
                with open(file_path, 'rb') as f_in:
                    with gzip.open(backup_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                self.logger.info(f"Created compressed backup: {backup_file}")
                self.metrics.total_backups_created += 1
                return backup_file
            except Exception as e:
                self.logger.error(f"Failed to create compressed backup: {e}")
                return None
        else:
            backup_file = self.backup_path / backup_name
            try:
                shutil.copy2(file_path, backup_file)
                self.logger.info(f"Created backup: {backup_file}")
                self.metrics.total_backups_created += 1
                return backup_file
            except Exception as e:
                self.logger.error(f"Failed to create backup: {e}")
                return None

    def analyze_file_optimized(self, file_path: Path) -> Dict[str, Any]:
        """Optimized file analysis with caching"""
        # Check cache first
        if self.optimization_flags.get("cache_file_analysis", True):
            cached_result = self.file_cache.get(file_path)
            if cached_result:
                self.metrics.cache_hits += 1
                return cached_result
            self.metrics.cache_misses += 1

        # Perform analysis
        start_time = time.time()

        if not file_path.exists():
            result = {"exists": False, "analysis": "File does not exist"}
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                stat = file_path.stat()
                result = {
                    "exists": True,
                    "size": len(content),
                    "lines": len(content.splitlines()),
                    "file_type": file_path.suffix,
                    "encoding": "utf-8",
                    "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "file_hash": self._get_file_hash(file_path),
                    "analysis_time": time.time() - start_time
                }

                # Language-specific fast analysis
                if file_path.suffix == ".py":
                    result.update(self._fast_analyze_python(content))
                elif file_path.suffix in [".cs", ".csx"]:
                    result.update(self._fast_analyze_csharp(content))
                elif file_path.suffix in [".js", ".ts"]:
                    result.update(self._fast_analyze_javascript(content))

            except Exception as e:
                result = {"exists": True, "error": str(e)}

        # Cache result
        if self.optimization_flags.get("cache_file_analysis", True):
            self.file_cache.set(file_path, result)

        return result

    def _fast_analyze_python(self, content: str) -> Dict[str, Any]:
        """Fast Python file analysis"""
        try:
            tree = ast.parse(content)
            return {
                "language": "python",
                "classes": [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)][:10],  # Limit for performance
                "functions": [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)][:20],  # Limit for performance
                "syntax_valid": True
            }
        except SyntaxError:
            return {"language": "python", "syntax_valid": False}

    def _fast_analyze_csharp(self, content: str) -> Dict[str, Any]:
        """Fast C# file analysis using simple regex"""
        import re
        return {
            "language": "csharp",
            "classes": re.findall(r'class\s+(\w+)', content)[:10],
            "methods": re.findall(r'(?:public|private|protected)?\s*\w+\s+(\w+)\s*\(', content)[:20]
        }

    def _fast_analyze_javascript(self, content: str) -> Dict[str, Any]:
        """Fast JavaScript/TypeScript analysis"""
        import re
        return {
            "language": "javascript",
            "functions": re.findall(r'function\s+(\w+)', content)[:20],
            "classes": re.findall(r'class\s+(\w+)', content)[:10]
        }

    async def add_task(self, task: FileUpdateTask) -> str:
        """Add task to optimized queue"""
        async with self.task_lock:
            # Check for duplicates if optimization enabled
            if self.optimization_flags.get("skip_duplicate_operations", True):
                task_signature = f"{task.operation}_{task.file_path}_{hash(task.content)}"
                if any(active_task.get("signature") == task_signature for active_task in self.active_tasks.values()):
                    self.logger.info(f"Skipping duplicate task: {task.task_id}")
                    return "skipped_duplicate"

            # Add file hash
            task.file_hash = self._get_file_hash(task.file_path)

            # Add to queue
            self.task_queue.put(task)
            self.active_tasks[task.task_id] = {
                "task": task,
                "signature": f"{task.operation}_{task.file_path}_{hash(task.content)}",
                "added_time": time.time()
            }

            self.logger.info(f"Added optimized task {task.task_id}: {task.operation} on {task.file_path}")
            return task.task_id

    async def process_tasks_batch(self):
        """Process tasks in optimized batches"""
        batch_size = self.perf_settings.get("batch_size", 10)
        batch = []

        # Collect batch
        while len(batch) < batch_size and not self.task_queue.empty():
            try:
                task = self.task_queue.get_nowait()
                batch.append(task)
            except:
                break

        if not batch:
            return

        # Process batch in parallel if enabled
        if self.perf_settings.get("enable_parallel_processing", True):
            tasks = [self._execute_task_optimized(task) for task in batch]
            await asyncio.gather(*tasks, return_exceptions=True)
        else:
            for task in batch:
                await self._execute_task_optimized(task)

    async def _execute_task_optimized(self, task: FileUpdateTask):
        """Execute single task with optimization"""
        start_time = time.time()

        try:
            # Safety check
            is_safe, reason = self.is_safe_operation(task.file_path, task.operation)
            if not is_safe:
                task.status = "failed"
                task.error = f"Safety check failed: {reason}"
                self.logger.error(f"Task {task.task_id} failed: {reason}")
                self.metrics.tasks_failed += 1
                return

            # Execute operation
            success = await self._perform_operation_optimized(task)

            if success:
                task.status = "completed"
                self.metrics.tasks_processed += 1
                self.metrics.total_files_processed += 1
            else:
                task.status = "failed"
                self.metrics.tasks_failed += 1

            # Update metrics
            processing_time = time.time() - start_time
            self.metrics.update_avg_time(processing_time)

        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            self.logger.error(f"Task {task.task_id} exception: {e}")
            self.metrics.tasks_failed += 1
        finally:
            # Cleanup
            self.active_tasks.pop(task.task_id, None)
            self.completed_tasks.append(task)

    async def _perform_operation_optimized(self, task: FileUpdateTask) -> bool:
        """Perform file operation with optimization"""
        try:
            if task.operation == "create":
                return await self._create_file_optimized(task)
            elif task.operation == "update":
                return await self._update_file_optimized(task)
            elif task.operation == "append":
                return await self._append_file_optimized(task)
            elif task.operation == "replace":
                return await self._replace_file_optimized(task)
            elif task.operation == "delete":
                return await self._delete_file_optimized(task)
            else:
                self.logger.error(f"Unknown operation: {task.operation}")
                return False
        except Exception as e:
            self.logger.error(f"Operation failed: {e}")
            return False

    async def _create_file_optimized(self, task: FileUpdateTask) -> bool:
        """Optimized file creation"""
        if task.file_path.exists():
            self.logger.warning(f"File already exists: {task.file_path}")
            return False

        try:
            # Ensure directory exists
            task.file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write content
            with open(task.file_path, 'w', encoding='utf-8') as f:
                f.write(task.content)

            self.logger.info(f"Created file: {task.file_path}")

            # Invalidate cache
            self.file_cache._remove_entry(str(task.file_path))

            return True
        except Exception as e:
            self.logger.error(f"Failed to create file: {e}")
            return False

    async def _update_file_optimized(self, task: FileUpdateTask) -> bool:
        """Optimized file update"""
        if not task.file_path.exists():
            self.logger.error(f"File does not exist: {task.file_path}")
            return False

        # Create backup if requested
        if task.backup:
            backup_file = self.create_optimized_backup(task.file_path)
            if not backup_file:
                return False

        try:
            with open(task.file_path, 'w', encoding='utf-8') as f:
                f.write(task.content)

            self.logger.info(f"Updated file: {task.file_path}")

            # Invalidate cache
            self.file_cache._remove_entry(str(task.file_path))

            return True
        except Exception as e:
            self.logger.error(f"Failed to update file: {e}")
            # Restore from backup if available
            if task.backup and backup_file:
                self._restore_from_backup(task.file_path, backup_file)
            return False

    async def _append_file_optimized(self, task: FileUpdateTask) -> bool:
        """Optimized file append"""
        try:
            with open(task.file_path, 'a', encoding='utf-8') as f:
                f.write(task.content)

            self.logger.info(f"Appended to file: {task.file_path}")

            # Invalidate cache
            self.file_cache._remove_entry(str(task.file_path))

            return True
        except Exception as e:
            self.logger.error(f"Failed to append to file: {e}")
            return False

    async def _replace_file_optimized(self, task: FileUpdateTask) -> bool:
        """Optimized content replacement"""
        if "|" not in task.content:
            self.logger.error("Replace operation requires content in format 'old_content|new_content'")
            return False

        old_content, new_content = task.content.split("|", 1)

        if not task.file_path.exists():
            self.logger.error(f"File does not exist: {task.file_path}")
            return False

        # Create backup if requested
        if task.backup:
            backup_file = self.create_optimized_backup(task.file_path)
            if not backup_file:
                return False

        try:
            with open(task.file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if old_content not in content:
                self.logger.warning(f"Content to replace not found in {task.file_path}")
                return False

            updated_content = content.replace(old_content, new_content)

            with open(task.file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            self.logger.info(f"Replaced content in file: {task.file_path}")

            # Invalidate cache
            self.file_cache._remove_entry(str(task.file_path))

            return True
        except Exception as e:
            self.logger.error(f"Failed to replace content: {e}")
            if task.backup and backup_file:
                self._restore_from_backup(task.file_path, backup_file)
            return False

    async def _delete_file_optimized(self, task: FileUpdateTask) -> bool:
        """Optimized file deletion"""
        if not task.file_path.exists():
            self.logger.warning(f"File does not exist: {task.file_path}")
            return True

        # Create backup before deletion
        backup_file = self.create_optimized_backup(task.file_path)

        try:
            task.file_path.unlink()
            self.logger.info(f"Deleted file: {task.file_path}")

            # Invalidate cache
            self.file_cache._remove_entry(str(task.file_path))

            return True
        except Exception as e:
            self.logger.error(f"Failed to delete file: {e}")
            return False

    def _restore_from_backup(self, file_path: Path, backup_file: Path):
        """Restore file from backup"""
        try:
            if backup_file.suffix == '.gz':
                with gzip.open(backup_file, 'rb') as f_in:
                    with open(file_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            else:
                shutil.copy2(backup_file, file_path)
            self.logger.info(f"Restored {file_path} from backup")
        except Exception as e:
            self.logger.error(f"Failed to restore from backup: {e}")

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics"""
        return {
            "tasks_processed": self.metrics.tasks_processed,
            "tasks_failed": self.metrics.tasks_failed,
            "success_rate": (self.metrics.tasks_processed / max(1, self.metrics.tasks_processed + self.metrics.tasks_failed)) * 100,
            "avg_processing_time": self.metrics.avg_processing_time,
            "cache_hit_rate": (self.metrics.cache_hits / max(1, self.metrics.cache_hits + self.metrics.cache_misses)) * 100,
            "total_files_processed": self.metrics.total_files_processed,
            "total_backups_created": self.metrics.total_backups_created,
            "active_tasks": len(self.active_tasks),
            "queue_size": self.task_queue.qsize(),
            "cache_size": len(self.file_cache.cache)
        }

    async def run_optimized_loop(self):
        """Main optimized processing loop"""
        self.logger.info("🚀 Starting optimized AGI file processing loop")

        while True:
            try:
                # Process batch of tasks
                await self.process_tasks_batch()

                # Small delay to prevent CPU overload
                await asyncio.sleep(0.1)

                # Periodic cleanup and stats
                if int(time.time()) % 60 == 0:  # Every minute
                    stats = self.get_performance_stats()
                    self.logger.info(f"📊 Performance stats: {stats}")

            except KeyboardInterrupt:
                self.logger.info("🛑 Shutting down optimized AGI file updater")
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(1)

        # Cleanup
        self.executor.shutdown(wait=True)

# Sample tasks for demonstration
async def create_sample_tasks(updater: OptimizedFileUpdater):
    """Create sample tasks to demonstrate optimization"""
    sample_tasks = [
        FileUpdateTask(
            file_path=Path("/home/broe/semantic-kernel/agi_optimization_test.md"),
            operation="create",
            content="# AGI Optimization Test\n\nThis file demonstrates the optimized AGI file update system.\n",
            priority=1
        ),
        FileUpdateTask(
            file_path=Path("/home/broe/semantic-kernel/test_performance.py"),
            operation="create",
            content='#!/usr/bin/env python3\n"""Performance test file"""\nprint("AGI Optimization Working!")\n',
            priority=2
        )
    ]

    for task in sample_tasks:
        await updater.add_task(task)

async def main():
    """Main function with optimized AGI file updater"""
    print("🚀 Starting Optimized AGI File Update System")

    updater = OptimizedFileUpdater()

    # Create sample tasks
    await create_sample_tasks(updater)

    # Start main processing loop
    await updater.run_optimized_loop()

if __name__ == "__main__":
    asyncio.run(main())
