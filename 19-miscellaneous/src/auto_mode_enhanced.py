#!/usr/bin/env python3
"""
Auto Mode Enhanced module

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
import time
import json
import asyncio
import logging
import threading
import signal
import subprocess
import traceback
import psutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from collections import deque
import socket
import requests
from aiohttp import web


@dataclass
class AutoModeConfig:
    """Configuration for enhanced AutoMode"""
    # Basic settings
    check_interval: int = 30  # seconds between health checks
    max_retries: int = 5
    retry_delay: int = 10  # seconds between retries

    # Resource limits
    max_memory_percent: float = 85.0
    max_cpu_percent: float = 90.0
    max_disk_percent: float = 95.0

    # Long-running settings
    enable_persistence: bool = True
    enable_auto_restart: bool = True
    enable_monitoring: bool = True
    enable_self_healing: bool = True

    # Logging and metrics
    log_level: str = "INFO"
    metrics_retention_days: int = 7
    backup_retention_days: int = 30

    # Network and external services
    health_check_urls: List[str] = None
    webhook_url: Optional[str] = None
    webhook_host: str = "0.0.0.0"
    webhook_port: int = 8081

    # Advanced features
    enable_graceful_degradation: bool = True
    enable_circuit_breaker: bool = True
    circuit_breaker_threshold: int = 3

    def __post_init__(self):
        if self.health_check_urls is None:
            self.health_check_urls = []


class CircuitBreaker:
    """Circuit breaker for external service calls"""

    def __init__(self, threshold: int = 3, timeout: int = 60):
        self.threshold = threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.threshold:
                self.state = "OPEN"

            raise e


class HealthMonitor:
    """Comprehensive health monitoring system"""

    def __init__(self, config: AutoModeConfig):
        self.config = config
        self.metrics_history = deque(maxlen=1000)
        self.alert_history = deque(maxlen=100)
        self.circuit_breakers = {}

    def collect_system_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive system metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()

            # Process-specific metrics
            current_process = psutil.Process()
            process_metrics = {
                'pid': current_process.pid,
                'cpu_percent': current_process.cpu_percent(),
                'memory_percent': current_process.memory_percent(),
                'memory_info': current_process.memory_info()._asdict(),
                'connections': len(current_process.connections()),
                'threads': current_process.num_threads(),
                'status': current_process.status()
            }

            metrics = {
                'timestamp': datetime.now().isoformat(),
                'system': {
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'memory_available': memory.available,
                    'disk_percent': disk.percent,
                    'disk_free': disk.free,
                    'network_sent': network.bytes_sent,
                    'network_recv': network.bytes_recv,
                },
                'process': process_metrics,
                'uptime': time.time() - psutil.boot_time()
            }

            # Add custom application metrics if available
            metrics['application'] = self._collect_app_metrics()

            return metrics

        except Exception as e:
            logging.error(f"Error collecting metrics: {e}")
            return {'timestamp': datetime.now().isoformat(), 'error': str(e)}

    def _collect_app_metrics(self) -> Dict[str, Any]:
        """Collect application-specific metrics"""
        app_metrics = {
            'threads_active': threading.active_count(),
            'tasks_pending': 0,  # Can be overridden by specific implementations
            'errors_last_hour': self._count_recent_errors(),
        }

        # Check if backend process is running
        try:
            response = requests.get('http://localhost:8000/health', timeout=5)
            app_metrics['backend_status'] = 'healthy' if response.status_code == 200 else 'unhealthy'
            app_metrics['backend_response_time'] = response.elapsed.total_seconds()
        except:
            app_metrics['backend_status'] = 'unreachable'
            app_metrics['backend_response_time'] = None

        return app_metrics

    def _count_recent_errors(self) -> int:
        """Count errors in the last hour"""
        cutoff = datetime.now() - timedelta(hours=1)
        return sum(1 for alert in self.alert_history
                  if alert.get('timestamp') and
                  datetime.fromisoformat(alert['timestamp']) > cutoff and
                  alert.get('level') == 'ERROR')

    def check_health(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        metrics = self.collect_system_metrics()
        health_status = {
            'overall': 'healthy',
            'checks': {},
            'metrics': metrics,
            'timestamp': datetime.now().isoformat()
        }

        # System resource checks
        if metrics['system']['cpu_percent'] > self.config.max_cpu_percent:
            health_status['checks']['cpu'] = 'warning'
            health_status['overall'] = 'degraded'

        if metrics['system']['memory_percent'] > self.config.max_memory_percent:
            health_status['checks']['memory'] = 'critical'
            health_status['overall'] = 'unhealthy'

        if metrics['system']['disk_percent'] > self.config.max_disk_percent:
            health_status['checks']['disk'] = 'critical'
            health_status['overall'] = 'unhealthy'

        # Application-specific checks
        app_metrics = metrics.get('application', {})
        if app_metrics.get('backend_status') != 'healthy':
            health_status['checks']['backend'] = 'unhealthy'
            health_status['overall'] = 'unhealthy'

        # Store metrics history
        self.metrics_history.append(metrics)

        return health_status


class PersistenceManager:
    """Manages state persistence and recovery"""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.state_dir = base_dir / ".automode_state"
        self.state_dir.mkdir(exist_ok=True)
        self.state_file = self.state_dir / "automode_state.json"
        self.backup_dir = self.state_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)

    def save_state(self, state: Dict[str, Any]) -> None:
        """Save current state with backup"""
        try:
            # Create backup of current state if it exists
            if self.state_file.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = self.backup_dir / f"state_backup_{timestamp}.json"
                self.state_file.rename(backup_file)

            # Save new state
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2, default=str)

            logging.debug(f"State saved to {self.state_file}")

        except Exception as e:
            logging.error(f"Failed to save state: {e}")

    def load_state(self) -> Dict[str, Any]:
        """Load state with fallback to backups"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                logging.info(f"State loaded from {self.state_file}")
                return state
        except Exception as e:
            logging.warning(f"Failed to load main state file: {e}")

        # Try to recover from backup
        backup_files = sorted(self.backup_dir.glob("state_backup_*.json"), reverse=True)
        for backup_file in backup_files[:3]:  # Try last 3 backups
            try:
                with open(backup_file, 'r') as f:
                    state = json.load(f)
                logging.info(f"State recovered from backup: {backup_file}")
                return state
            except Exception as e:
                logging.warning(f"Failed to load backup {backup_file}: {e}")

        logging.info("No valid state found, starting fresh")
        return {}

    def cleanup_old_backups(self, retention_days: int) -> None:
        """Remove old backup files"""
        cutoff = datetime.now() - timedelta(days=retention_days)
        for backup_file in self.backup_dir.glob("state_backup_*.json"):
            if backup_file.stat().st_mtime < cutoff.timestamp():
                try:
                    backup_file.unlink()
                    logging.debug(f"Removed old backup: {backup_file}")
                except Exception as e:
                    logging.warning(f"Failed to remove backup {backup_file}: {e}")


class EnhancedAutoMode:
    """Enhanced AutoMode with improved long-running capabilities"""

    def __init__(self, config: AutoModeConfig = None, base_dir: Path = None):
        self.config = config or AutoModeConfig()
        self.base_dir = base_dir or Path(__file__).parent

        # Initialize components
        self.health_monitor = HealthMonitor(self.config)
        self.persistence_manager = PersistenceManager(self.base_dir)
        self.circuit_breakers = {}

        # Runtime state
        self.is_running = False
        self.start_time = None
        self.last_health_check = None
        self.restart_count = 0
        self.error_count = 0
        self.managed_processes = {}

        # Async components
        self.event_loop = None
        self.tasks = []
        self.shutdown_event = asyncio.Event()
        self.external_trigger_queue: asyncio.Queue = asyncio.Queue()

        # Setup logging
        self._setup_logging()

        # Load persisted state
        self._load_state()

        # Setup signal handlers
        self._setup_signal_handlers()

    def _setup_logging(self) -> None:
        """Setup comprehensive logging"""
        log_dir = self.base_dir / "logs"
        log_dir.mkdir(exist_ok=True)

        # Main log file
        log_file = log_dir / f"automode_{datetime.now().strftime('%Y%m%d')}.log"

        # Configure logging
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )

        # Add custom handlers for different log levels
        error_handler = logging.FileHandler(log_dir / "errors.log")
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n%(exc_info)s'
        ))
        logging.getLogger().addHandler(error_handler)

        logging.info("Enhanced AutoMode logging initialized")

    def _setup_signal_handlers(self) -> None:
        """Setup graceful shutdown signal handlers"""
        def signal_handler(signum, frame):
            logging.info(f"Received signal {signum}, initiating graceful shutdown...")
            asyncio.create_task(self.graceful_shutdown())

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        if hasattr(signal, 'SIGHUP'):
            signal.signal(signal.SIGHUP, signal_handler)

    def _load_state(self) -> None:
        """Load and restore state"""
        try:
            state = self.persistence_manager.load_state()
            self.restart_count = state.get('restart_count', 0)
            self.error_count = state.get('error_count', 0)

            if state.get('was_running'):
                logging.info("Previous session was running, initiating recovery...")
                self.restart_count += 1

        except Exception as e:
            logging.error(f"Failed to load state: {e}")

    def _save_state(self) -> None:
        """Save current state"""
        try:
            state = {
                'timestamp': datetime.now().isoformat(),
                'restart_count': self.restart_count,
                'error_count': self.error_count,
                'was_running': self.is_running,
                'uptime': time.time() - self.start_time if self.start_time else 0,
                'managed_processes': {k: v.get('pid') for k, v in self.managed_processes.items()},
                'config': asdict(self.config)
            }
            self.persistence_manager.save_state(state)
        except Exception as e:
            logging.error(f"Failed to save state: {e}")

    async def start_managed_process(self, name: str, command: List[str], **kwargs) -> bool:
        """Start and manage a subprocess"""
        try:
            logging.info(f"Starting managed process: {name}")

            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                **kwargs
            )

            self.managed_processes[name] = {
                'process': process,
                'pid': process.pid,
                'command': command,
                'start_time': datetime.now(),
                'restart_count': 0
            }

            logging.info(f"Process {name} started with PID {process.pid}")

            # Monitor the process
            self.tasks.append(asyncio.create_task(self._monitor_process(name)))

            return True

        except Exception as e:
            logging.error(f"Failed to start process {name}: {e}")
            return False

    async def _monitor_process(self, name: str) -> None:
        """Monitor a managed process and restart if needed"""
        while self.is_running:
            try:
                if name not in self.managed_processes:
                    break

                process_info = self.managed_processes[name]
                process = process_info['process']

                # Check if process is still running
                if process.returncode is not None:
                    logging.warning(f"Process {name} has stopped with code {process.returncode}")

                    if self.config.enable_auto_restart:
                        await self._restart_process(name)
                    else:
                        del self.managed_processes[name]
                        break

                # Check resource usage
                try:
                    ps_process = psutil.Process(process.pid)
                    cpu_percent = ps_process.cpu_percent()
                    memory_percent = ps_process.memory_percent()

                    if memory_percent > self.config.max_memory_percent:
                        logging.warning(f"Process {name} using excessive memory: {memory_percent}%")
                        await self._restart_process(name)

                except psutil.NoSuchProcess:
                    logging.warning(f"Process {name} no longer exists")
                    if self.config.enable_auto_restart:
                        await self._restart_process(name)
                    else:
                        del self.managed_processes[name]
                        break

                await asyncio.sleep(self.config.check_interval)

            except Exception as e:
                logging.error(f"Error monitoring process {name}: {e}")
                await asyncio.sleep(self.config.check_interval)

    async def _restart_process(self, name: str) -> bool:
        """Restart a managed process"""
        try:
            if name not in self.managed_processes:
                return False

            process_info = self.managed_processes[name]
            process_info['restart_count'] += 1

            # Check restart limits
            if process_info['restart_count'] > self.config.max_retries:
                logging.error(f"Process {name} exceeded restart limit, giving up")
                del self.managed_processes[name]
                return False

            logging.info(f"Restarting process {name} (attempt {process_info['restart_count']})")

            # Terminate old process
            try:
                process_info['process'].terminate()
                await asyncio.wait_for(process_info['process'].wait(), timeout=10)
            except asyncio.TimeoutError:
                process_info['process'].kill()
            except:
                pass

            # Wait before restart
            await asyncio.sleep(self.config.retry_delay)

            # Start new process
            success = await self.start_managed_process(name, process_info['command'])

            if success:
                # Preserve restart count
                self.managed_processes[name]['restart_count'] = process_info['restart_count']
                logging.info(f"Process {name} restarted successfully")
                return True
            else:
                logging.error(f"Failed to restart process {name}")
                return False

        except Exception as e:
            logging.error(f"Error restarting process {name}: {e}")
            return False

    async def health_check_loop(self) -> None:
        """Main health check loop"""
        while self.is_running:
            try:
                health_status = self.health_monitor.check_health()
                self.last_health_check = datetime.now()

                # Log health status
                if health_status['overall'] != 'healthy':
                    logging.warning(f"Health check: {health_status['overall']}")
                    for check, status in health_status['checks'].items():
                        if status != 'healthy':
                            logging.warning(f"  {check}: {status}")

                # Send to webhook if configured
                if self.config.webhook_url:
                    await self._send_health_status(health_status)

                # Self-healing actions
                if self.config.enable_self_healing:
                    await self._perform_self_healing(health_status)

                # Save state periodically
                self._save_state()

            except Exception as e:
                logging.error(f"Error in health check loop: {e}")
                self.error_count += 1

            await asyncio.sleep(self.config.check_interval)

    async def _webhook_server(self) -> None:
        """Lightweight webhook server for external triggers"""
        app = web.Application()

        async def trigger(request: web.Request):
            try:
                data = await request.json()
            except Exception:
                data = await request.post()
            await self.external_trigger_queue.put(dict(data) if hasattr(data, 'items') else data)
            return web.json_response({"status": "accepted"})

        app.add_routes([web.post("/trigger", trigger)])

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self.config.webhook_host, self.config.webhook_port)
        await site.start()

        try:
            while self.is_running:
                await asyncio.sleep(1)
        finally:
            await runner.cleanup()

    async def _external_trigger_loop(self) -> None:
        """Process incoming external triggers"""
        while self.is_running:
            try:
                data = await asyncio.wait_for(self.external_trigger_queue.get(), timeout=5)
                logging.info(f"Received external trigger: {data}")
            except asyncio.TimeoutError:
                if not self.is_running:
                    break

    async def _send_health_status(self, health_status: Dict[str, Any]) -> None:
        """Send health status to webhook"""
        try:
            circuit_breaker = self.circuit_breakers.get('webhook')
            if not circuit_breaker:
                circuit_breaker = CircuitBreaker()
                self.circuit_breakers['webhook'] = circuit_breaker

            def send_request():
                return requests.post(
                    self.config.webhook_url,
                    json=health_status,
                    timeout=10
                )

            response = circuit_breaker.call(send_request)
            logging.debug(f"Health status sent to webhook: {response.status_code}")

        except Exception as e:
            logging.warning(f"Failed to send health status to webhook: {e}")

    async def _perform_self_healing(self, health_status: Dict[str, Any]) -> None:
        """Perform self-healing actions based on health status"""
        try:
            if health_status['overall'] == 'unhealthy':
                logging.info("Performing self-healing actions...")

                # Restart unhealthy processes
                for name, process_info in list(self.managed_processes.items()):
                    try:
                        ps_process = psutil.Process(process_info['pid'])
                        if ps_process.memory_percent() > self.config.max_memory_percent:
                            logging.info(f"Restarting {name} due to high memory usage")
                            await self._restart_process(name)
                    except:
                        pass

                # Clear caches, temporary files, etc.
                await self._cleanup_resources()

                # Graceful degradation
                if self.config.enable_graceful_degradation:
                    await self._enable_graceful_degradation()

        except Exception as e:
            logging.error(f"Error in self-healing: {e}")

    async def _cleanup_resources(self) -> None:
        """Clean up system resources"""
        try:
            # Clean up log files
            log_dir = self.base_dir / "logs"
            if log_dir.exists():
                cutoff = datetime.now() - timedelta(days=self.config.metrics_retention_days)
                for log_file in log_dir.glob("*.log.*"):
                    if log_file.stat().st_mtime < cutoff.timestamp():
                        log_file.unlink()

            # Clean up old backups
            self.persistence_manager.cleanup_old_backups(self.config.backup_retention_days)

            # Clean up temporary files
            temp_dir = self.base_dir / "temp"
            if temp_dir.exists():
                for temp_file in temp_dir.glob("*"):
                    try:
                        if temp_file.stat().st_mtime < (time.time() - 3600):  # 1 hour old
                            temp_file.unlink()
                    except:
                        pass

            logging.debug("Resource cleanup completed")

        except Exception as e:
            logging.error(f"Error in resource cleanup: {e}")

    async def _enable_graceful_degradation(self) -> None:
        """Enable graceful degradation mode"""
        try:
            # Reduce resource usage
            # Slow down monitoring intervals
            self.config.check_interval = min(self.config.check_interval * 2, 300)

            # Disable non-essential features
            self.config.enable_monitoring = False

            logging.info("Graceful degradation mode enabled")

        except Exception as e:
            logging.error(f"Error enabling graceful degradation: {e}")

    async def run(self) -> None:
        """Main run loop"""
        try:
            self.is_running = True
            self.start_time = time.time()

            logging.info("Enhanced AutoMode starting...")

            # Start core tasks
            self.tasks = [
                asyncio.create_task(self.health_check_loop()),
                asyncio.create_task(self._webhook_server()),
                asyncio.create_task(self._external_trigger_loop()),
            ]

            # Start default managed processes
            await self._start_default_processes()

            logging.info("Enhanced AutoMode is running")

            # Wait for shutdown signal
            await self.shutdown_event.wait()

        except Exception as e:
            logging.error(f"Critical error in main loop: {e}")
            logging.error(traceback.format_exc())
        finally:
            await self.graceful_shutdown()

    async def _start_default_processes(self) -> None:
        """Start default managed processes"""
        # Start backend if it exists
        backend_file = self.base_dir / "backend.py"
        if backend_file.exists():
            await self.start_managed_process(
                "backend",
                [sys.executable, str(backend_file)]
            )

        # Start other default processes as needed
        # This can be extended based on specific requirements

    async def graceful_shutdown(self) -> None:
        """Perform graceful shutdown"""
        if not self.is_running:
            return

        logging.info("Initiating graceful shutdown...")
        self.is_running = False

        try:
            # Stop all managed processes
            for name, process_info in self.managed_processes.items():
                try:
                    logging.info(f"Stopping process {name}...")
                    process_info['process'].terminate()
                    await asyncio.wait_for(process_info['process'].wait(), timeout=10)
                except asyncio.TimeoutError:
                    logging.warning(f"Force killing process {name}")
                    process_info['process'].kill()
                except Exception as e:
                    logging.error(f"Error stopping process {name}: {e}")

            # Cancel all tasks
            for task in self.tasks:
                if not task.done():
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass

            # Save final state
            self._save_state()

            logging.info("Graceful shutdown completed")

        except Exception as e:
            logging.error(f"Error during shutdown: {e}")

        finally:
            self.shutdown_event.set()


def create_automode_config(config_file: Path = None) -> AutoModeConfig:
    """Create AutoMode configuration from file or defaults"""
    if config_file and config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            return AutoModeConfig(**config_data)
        except Exception as e:
            logging.warning(f"Failed to load config from {config_file}: {e}")

    return AutoModeConfig()


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Enhanced AutoMode for Long-Running Operations")
    parser.add_argument("--config", type=Path, help="Configuration file path")
    parser.add_argument("--base-dir", type=Path, help="Base directory", default=Path(__file__).parent)
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       default="INFO", help="Log level")

    args = parser.parse_args()

    # Create configuration
    config = create_automode_config(args.config)
    config.log_level = args.log_level

    # Create and run AutoMode
    automode = EnhancedAutoMode(config, args.base_dir)

    try:
        asyncio.run(automode.run())
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        logging.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
