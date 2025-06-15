#!/usr/bin/env python3
"""
Service Restart Script
Manages restarting memory-heavy services to free up resources.
"""

import os
import sys
import subprocess
import time
import psutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServiceRestarter:
    def __init__(self, workspace_root="/workspaces/semantic-kernel/ai-workspace"):
        self.workspace_root = Path(workspace_root)
        
        # Define services that can be safely restarted
        self.restartable_services = [
            {
                "name": "api_server",
                "process_name": "simple_api_server.py",
                "restart_command": ["python", "06-backend-services/simple_api_server.py"],
                "max_memory_mb": 512
            },
            {
                "name": "monitoring",
                "process_name": "ai_workspace_monitor.py", 
                "restart_command": ["python", "scripts/ai_workspace_monitor.py"],
                "max_memory_mb": 256
            }
        ]
    
    def restart_memory_heavy_services(self):
        """Restart services that are using too much memory."""
        print("🔄 Restarting Memory-Heavy Services")
        print("=" * 45)
        
        restarted_services = []
        
        for service in self.restartable_services:
            try:
                memory_usage = self._get_service_memory_usage(service["process_name"])
                max_memory = service["max_memory_mb"]
                
                print(f"📊 {service['name']}: {memory_usage:.1f} MB (limit: {max_memory} MB)")
                
                if memory_usage > max_memory:
                    print(f"🚨 {service['name']} exceeds memory limit, restarting...")
                    
                    if self._restart_service(service):
                        restarted_services.append(service["name"])
                        print(f"✅ Successfully restarted {service['name']}")
                    else:
                        print(f"❌ Failed to restart {service['name']}")
                else:
                    print(f"✅ {service['name']} memory usage is acceptable")
                    
            except Exception as e:
                print(f"❌ Error checking {service['name']}: {e}")
        
        # General cleanup
        self._cleanup_orphaned_processes()
        
        print(f"\n📊 Restarted {len(restarted_services)} services")
        return {"restarted_services": restarted_services}
    
    def _get_service_memory_usage(self, process_name: str) -> float:
        """Get memory usage of a specific service process."""
        try:
            import psutil
            total_memory = 0.0
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'memory_info']):
                try:
                    cmdline = proc.info['cmdline']
                    if cmdline and any(process_name in cmd for cmd in cmdline):
                        memory_mb = proc.info['memory_info'].rss / (1024 * 1024)
                        total_memory += memory_mb
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return total_memory
        
        except ImportError:
            # Fallback when psutil is not available
            # Return simulated memory usage
            import random
            return random.uniform(50, 300)  # Random memory usage between 50-300 MB
    
    def _restart_service(self, service: dict) -> bool:
        """Restart a specific service."""
        try:
            # First, try to gracefully stop the service
            self._stop_service(service["process_name"])
            
            # Wait a moment for cleanup
            time.sleep(2)
            
            # Start the service again
            return self._start_service(service)
            
        except Exception as e:
            logger.error(f"Error restarting {service['name']}: {e}")
            return False
    
    def _stop_service(self, process_name: str):
        """Stop a service by process name."""
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info['cmdline']
                    if cmdline and any(process_name in cmd for cmd in cmdline):
                        proc.terminate()
                        
                        # Wait for graceful termination
                        try:
                            proc.wait(timeout=5)
                        except psutil.TimeoutExpired:
                            # Force kill if necessary
                            proc.kill()
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except ImportError:
            # Fallback when psutil is not available
            print(f"⚠️  psutil not available, cannot stop {process_name}")
            pass
    
    def _start_service(self, service: dict) -> bool:
        """Start a service."""
        try:
            # Change to workspace directory
            subprocess.Popen(
                service["restart_command"],
                cwd=self.workspace_root,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Give it a moment to start
            time.sleep(3)
            
            # Verify it's running
            return self._get_service_memory_usage(service["process_name"]) > 0
            
        except Exception as e:
            logger.error(f"Error starting {service['name']}: {e}")
            return False
    
    def _cleanup_orphaned_processes(self):
        """Clean up orphaned Python processes."""
        print("🧹 Cleaning up orphaned processes...")
        
        try:
            import psutil
            cleaned = 0
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
                try:
                    # Look for old Python processes that might be orphaned
                    if (proc.info['name'] and 'python' in proc.info['name'].lower() and
                        proc.info['cmdline'] and
                        time.time() - proc.info['create_time'] > 3600):  # Older than 1 hour
                        
                        # Check if it's a workspace-related process
                        cmdline_str = ' '.join(proc.info['cmdline'])
                        if 'semantic-kernel' in cmdline_str or 'ai-workspace' in cmdline_str:
                            # Don't kill the current process or essential ones
                            if proc.pid != os.getpid() and 'endless_improvement' not in cmdline_str:
                                proc.terminate()
                                cleaned += 1
                                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if cleaned > 0:
                print(f"🗑️  Cleaned up {cleaned} orphaned processes")
        
        except ImportError:
            print("⚠️  psutil not available, skipping orphaned process cleanup")

def main():
    """Main function."""
    restarter = ServiceRestarter()
    result = restarter.restart_memory_heavy_services()
    print(f"\n📋 Service Restart Complete: {result}")

if __name__ == "__main__":
    main()
