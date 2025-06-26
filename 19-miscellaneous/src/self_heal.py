#!/usr/bin/env python3
"""
Self Heal module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Self-Healing System - Auto-created by setup.py
import os
import sys
import time
import psutil
import logging
import subprocess
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s',
                   handlers=[logging.FileHandler("self_heal.log"),
                             logging.StreamHandler()])

class SelfHealer:
    """Monitors and restarts critical services when they fail"""

    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.backend_script = self.base_dir / "backend.py"
        self.backend_process = None
        self.max_memory_percent = 90  # Restart if memory usage > 90%
        self.max_failures = 0

    def check_backend(self):
        """Check if backend is running, start if not"""
        if self.backend_process is None or not psutil.pid_exists(self.backend_process.pid):
            logging.info("Backend not running. Starting...")
            try:
                self.backend_process = subprocess.Popen(
                    [sys.executable, str(self.backend_script)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                logging.info(f"Backend started with PID: {self.backend_process.pid}")
            except Exception as e:
                logging.error(f"Failed to start backend: {e}")
                self.max_failures += 1
        else:
            # Check resource usage
            try:
                process = psutil.Process(self.backend_process.pid)
                memory_percent = process.memory_percent()
                if memory_percent > self.max_memory_percent:
                    logging.warning(f"Backend using high memory: {memory_percent}%. Restarting...")
                    process.terminate()
                    time.sleep(2)
                    if psutil.pid_exists(self.backend_process.pid):
                        process.kill()
                    self.backend_process = None
            except Exception as e:
                logging.error(f"Error monitoring backend: {e}")

    def run_forever(self, check_interval=30):
        """Run continuous monitoring"""
        logging.info("Self-healer started...")
        while True:
            try:
                self.check_backend()
                if self.max_failures >= 5:
                    logging.critical("Too many failures. Please check system manually.")
                    break
                time.sleep(check_interval)
            except KeyboardInterrupt:
                logging.info("Self-healer stopped by user")
                break
            except Exception as e:
                logging.error(f"Error in self-healer: {e}")
                time.sleep(check_interval)

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    healer = SelfHealer(base_dir)
    healer.run_forever()
