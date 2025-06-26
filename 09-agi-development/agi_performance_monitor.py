#!/usr/bin/env python3
"""
AGI module for agi performance monitor

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
import threading
from datetime import datetime
from typing import Dict, Any

class AGIPerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        self.monitoring = False
        self.monitor_thread = None

    def start_monitoring(self):
        '''Start performance monitoring'''
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def stop_monitoring(self):
        '''Stop performance monitoring'''
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()

    def _monitor_loop(self):
        '''Main monitoring loop'''
        while self.monitoring:
            self.metrics.update({
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_io': psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else {},
            })
            time.sleep(1)

    def get_current_metrics(self) -> Dict[str, Any]:
        '''Get current performance metrics'''
        return self.metrics.copy()

# Global monitor instance
performance_monitor = AGIPerformanceMonitor()
