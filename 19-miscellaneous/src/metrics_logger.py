#!/usr/bin/env python3
"""
Metrics Logger module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Advanced Metrics Logger - Auto-created by setup.py
import os
import time
import json
import psutil
import logging
import threading
from datetime import datetime
from pathlib import Path

class MetricsLogger:
    """Logs system and application metrics"""
    
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.metrics_dir = self.base_dir / "metrics"
        os.makedirs(self.metrics_dir, exist_ok=True)
        
        logging.basicConfig(level=logging.INFO, 
                         format='%(asctime)s - %(levelname)s - %(message)s',
                         handlers=[logging.FileHandler(self.metrics_dir / "metrics.log"),
                                   logging.StreamHandler()])
        self.stop_event = threading.Event()
        
    def collect_system_metrics(self):
        """Collect system-level metrics"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "network_io": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv
            }
        }
        return metrics
    
    def collect_process_metrics(self):
        """Collect process-specific metrics"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "processes": []
        }
        
        # Look for Python processes related to our app
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            if 'python' in proc.info['name'].lower():
                try:
                    cmdline = proc.cmdline()
                    if any(x in ' '.join(cmdline) for x in ['backend.py', 'start_chat', 'start_backend']):
                        proc_info = {
                            'pid': proc.info['pid'],
                            'cpu_percent': proc.info['cpu_percent'],
                            'memory_percent': proc.info['memory_percent'],
                            'cmdline': ' '.join(cmdline),
                            'connections': len(proc.connections())
                        }
                        metrics['processes'].append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        
        return metrics
    
    def log_metrics(self):
        """Log system and process metrics to file"""
        sys_metrics = self.collect_system_metrics()
        proc_metrics = self.collect_process_metrics()
        
        # Log to JSON files with timestamp in filename
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        with open(self.metrics_dir / f"system_metrics_{timestamp}.json", 'w') as f:
            json.dump(sys_metrics, f, indent=2)
        
        with open(self.metrics_dir / f"process_metrics_{timestamp}.json", 'w') as f:
            json.dump(proc_metrics, f, indent=2)
            
        # Also log summary to console/log file
        logging.info(f"System: CPU {sys_metrics['cpu_percent']}%, Memory {sys_metrics['memory_percent']}%")
        logging.info(f"Monitored {len(proc_metrics['processes'])} AI Chat processes")
        
        # Clean up old metrics (keep last 100)
        self._cleanup_old_metrics()
        
    def _cleanup_old_metrics(self):
        """Delete old metric files to prevent disk fill"""
        all_files = []
        for pattern in ["system_metrics_*.json", "process_metrics_*.json"]:
            all_files.extend(list(self.metrics_dir.glob(pattern)))
        
        # Sort by modification time (oldest first)
        all_files.sort(key=lambda x: x.stat().st_mtime)
        
        # Keep only the last 100 files
        if len(all_files) > 100:
            for old_file in all_files[:-100]:
                try:
                    old_file.unlink()
                except:
                    pass
    
    def run_periodic_logging(self, interval=300):
        """Run metrics logging at regular intervals"""
        logging.info(f"Metrics logger started, interval: {interval} seconds")
        while not self.stop_event.is_set():
            try:
                self.log_metrics()
            except Exception as e:
                logging.error(f"Error logging metrics: {e}")
            # Wait for interval or until stop event
            self.stop_event.wait(interval)
    
    def start(self, interval=300):
        """Start metrics logging in a background thread"""
        thread = threading.Thread(target=self.run_periodic_logging, args=(interval,))
        thread.daemon = True
        thread.start()
        return thread
    
    def stop(self):
        """Stop the metrics logging"""
        self.stop_event.set()

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    logger = MetricsLogger(base_dir)
    
    try:
        logging_thread = logger.start(interval=60)  # Log every minute
        logging_thread.join()
    except KeyboardInterrupt:
        logger.stop()
        print("Metrics logging stopped.")
