#!/usr/bin/env python3
"""
Metrics Exporter module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import time
import psutil
import logging
import threading
from pathlib import Path
from typing import Dict, Any

try:
    from prometheus_client import start_http_server, Gauge, Counter, Histogram, Info
    from prometheus_client.core import CollectorRegistry
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    print("Prometheus client not available. Install with: pip install prometheus-client")


class MetricsExporter:
    """Exports metrics to Prometheus"""

    def __init__(self, port: int = 8001, base_dir: Path = None):
        if not PROMETHEUS_AVAILABLE:
            raise ImportError("Prometheus client is required")

        self.port = port
        self.base_dir = base_dir or Path(__file__).parent
        self.registry = CollectorRegistry()

        # System metrics
        self.cpu_usage = Gauge('system_cpu_percent', 'CPU usage percentage', registry=self.registry)
        self.memory_usage = Gauge('system_memory_percent', 'Memory usage percentage', registry=self.registry)
        self.disk_usage = Gauge('system_disk_percent', 'Disk usage percentage', registry=self.registry)
        self.network_bytes_sent = Counter('system_network_bytes_sent_total', 'Network bytes sent', registry=self.registry)
        self.network_bytes_recv = Counter('system_network_bytes_recv_total', 'Network bytes received', registry=self.registry)

        # Process metrics
        self.process_cpu_usage = Gauge('process_cpu_percent', 'Process CPU usage percentage', registry=self.registry)
        self.process_memory_usage = Gauge('process_memory_percent', 'Process memory usage percentage', registry=self.registry)
        self.process_threads = Gauge('process_threads_count', 'Number of process threads', registry=self.registry)
        self.process_connections = Gauge('process_connections_count', 'Number of process connections', registry=self.registry)

        # Application metrics
        self.app_uptime = Gauge('app_uptime_seconds', 'Application uptime in seconds', registry=self.registry)
        self.app_restarts = Counter('app_restarts_total', 'Total number of application restarts', registry=self.registry)
        self.app_errors = Counter('app_errors_total', 'Total number of application errors', registry=self.registry)
        self.app_health_checks = Counter('app_health_checks_total', 'Total number of health checks', registry=self.registry)

        # Custom metrics
        self.backend_response_time = Histogram('backend_response_time_seconds', 'Backend response time', registry=self.registry)
        self.managed_processes = Gauge('managed_processes_count', 'Number of managed processes', registry=self.registry)

        # Info metrics
        self.app_info = Info('app_info', 'Application information', registry=self.registry)

        # State
        self.start_time = time.time()
        self.is_running = False
        self.update_thread = None

        # Initialize info
        self._update_app_info()

    def _update_app_info(self):
        """Update application info metrics"""
        import sys
        import platform

        self.app_info.info({
            'version': '1.0.0',  # Can be loaded from config
            'python_version': sys.version,
            'platform': platform.platform(),
            'hostname': platform.node(),
        })

    def start(self):
        """Start the metrics server"""
        try:
            start_http_server(self.port, registry=self.registry)
            logging.info(f"Metrics server started on port {self.port}")

            self.is_running = True
            self.update_thread = threading.Thread(target=self._update_metrics_loop, daemon=True)
            self.update_thread.start()

            logging.info("Metrics collection started")

        except Exception as e:
            logging.error(f"Failed to start metrics server: {e}")
            raise

    def stop(self):
        """Stop the metrics collection"""
        self.is_running = False
        if self.update_thread:
            self.update_thread.join(timeout=5)
        logging.info("Metrics collection stopped")

    def _update_metrics_loop(self):
        """Main metrics update loop"""
        while self.is_running:
            try:
                self._update_system_metrics()
                self._update_process_metrics()
                self._update_application_metrics()
                time.sleep(10)  # Update every 10 seconds
            except Exception as e:
                logging.error(f"Error updating metrics: {e}")
                time.sleep(10)

    def _update_system_metrics(self):
        """Update system-level metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.cpu_usage.set(cpu_percent)

            # Memory usage
            memory = psutil.virtual_memory()
            self.memory_usage.set(memory.percent)

            # Disk usage
            disk = psutil.disk_usage('/')
            self.disk_usage.set(disk.percent)

            # Network I/O
            network = psutil.net_io_counters()
            self.network_bytes_sent._value._value = network.bytes_sent
            self.network_bytes_recv._value._value = network.bytes_recv

        except Exception as e:
            logging.error(f"Error updating system metrics: {e}")

    def _update_process_metrics(self):
        """Update process-specific metrics"""
        try:
            current_process = psutil.Process()

            # Process CPU and memory
            self.process_cpu_usage.set(current_process.cpu_percent())
            self.process_memory_usage.set(current_process.memory_percent())

            # Process threads and connections
            self.process_threads.set(current_process.num_threads())

            try:
                connections = len(current_process.connections())
                self.process_connections.set(connections)
            except psutil.AccessDenied:
                # Some systems don't allow connection enumeration
                pass

        except Exception as e:
            logging.error(f"Error updating process metrics: {e}")

    def _update_application_metrics(self):
        """Update application-specific metrics"""
        try:
            # Uptime
            uptime = time.time() - self.start_time
            self.app_uptime.set(uptime)

            # Check backend health and response time
            self._check_backend_health()

            # Count managed processes (if state file exists)
            self._count_managed_processes()

        except Exception as e:
            logging.error(f"Error updating application metrics: {e}")

    def _check_backend_health(self):
        """Check backend health and measure response time"""
        try:
            import requests
            start_time = time.time()

            response = requests.get('http://localhost:8000/health', timeout=5)
            response_time = time.time() - start_time

            self.backend_response_time.observe(response_time)

            if response.status_code == 200:
                # Backend is healthy
                pass
            else:
                self.app_errors.inc()

        except Exception:
            # Backend is not responding
            self.app_errors.inc()

    def _count_managed_processes(self):
        """Count managed processes from state file"""
        try:
            state_file = self.base_dir / ".automode_state" / "automode_state.json"
            if state_file.exists():
                import json
                with open(state_file, 'r') as f:
                    state = json.load(f)

                managed_processes = state.get('managed_processes', {})
                self.managed_processes.set(len(managed_processes))

        except Exception as e:
            logging.debug(f"Could not read state file: {e}")

    def increment_restarts(self):
        """Increment restart counter"""
        self.app_restarts.inc()

    def increment_errors(self):
        """Increment error counter"""
        self.app_errors.inc()

    def increment_health_checks(self):
        """Increment health check counter"""
        self.app_health_checks.inc()


def main():
    """Main entry point"""
    import argparse
    import signal
    import sys

    parser = argparse.ArgumentParser(description="Prometheus Metrics Exporter")
    parser.add_argument("--port", type=int, default=8001, help="Metrics server port")
    parser.add_argument("--base-dir", type=Path, default=Path(__file__).parent,
                       help="Base directory")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       default="INFO", help="Log level")

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    if not PROMETHEUS_AVAILABLE:
        logging.error("Prometheus client not available. Install with: pip install prometheus-client")
        sys.exit(1)

    # Create metrics exporter
    exporter = MetricsExporter(args.port, args.base_dir)

    # Setup signal handlers
    def signal_handler(signum, frame):
        logging.info("Shutdown signal received")
        exporter.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Start metrics server
        exporter.start()

        logging.info(f"Metrics server running on http://localhost:{args.port}/metrics")
        logging.info("Press Ctrl+C to stop")

        # Keep running
        while exporter.is_running:
            time.sleep(1)

    except Exception as e:
        logging.error(f"Error running metrics exporter: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
