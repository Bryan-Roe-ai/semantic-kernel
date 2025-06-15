#!/usr/bin/env python3
"""
AI Workspace Monitor
Real-time monitoring and alerting for the AI workspace.
"""

import os
import sys
import time
import json
import psutil
import threading
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AIWorkspaceMonitor:
    def __init__(self, workspace_root="/workspaces/semantic-kernel/ai-workspace"):
        self.workspace_root = Path(workspace_root)
        self.monitoring = True
        self.alerts = []
        self.metrics_history = []
        self.thresholds = {
            "cpu_percent": 80.0,
            "memory_percent": 85.0,
            "disk_percent": 90.0,
            "gpu_memory_percent": 95.0,
            "api_response_time": 5.0,
            "error_rate": 0.1
        }
        
    def start_monitoring(self, interval=30):
        """Start continuous monitoring."""
        print("🔍 AI Workspace Monitor Starting...")
        print("=" * 50)
        print(f"📊 Monitoring interval: {interval} seconds")
        print(f"📁 Workspace: {self.workspace_root}")
        print("🚨 Alert thresholds:")
        for metric, threshold in self.thresholds.items():
            print(f"   • {metric}: {threshold}")
        print("\n⏰ Starting monitoring loop...\n")
        
        try:
            while self.monitoring:
                metrics = self.collect_metrics()
                self.check_alerts(metrics)
                self.log_metrics(metrics)
                
                # Display current status
                self.display_status(metrics)
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
            self.stop_monitoring()
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive system metrics."""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "system": self.get_system_metrics(),
            "workspace": self.get_workspace_metrics(),
            "services": self.get_service_metrics(),
            "api": self.get_api_metrics()
        }
        
        self.metrics_history.append(metrics)
        
        # Keep only last 1000 entries
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]
            
        return metrics
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system-level metrics."""
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory metrics
        memory = psutil.virtual_memory()
        
        # Disk metrics
        disk = psutil.disk_usage(str(self.workspace_root))
        
        # GPU metrics (if available)
        gpu_metrics = self.get_gpu_metrics()
        
        return {
            "cpu_percent": cpu_percent,
            "cpu_count": cpu_count,
            "memory_total": memory.total,
            "memory_used": memory.used,
            "memory_percent": memory.percent,
            "disk_total": disk.total,
            "disk_used": disk.used,
            "disk_percent": (disk.used / disk.total) * 100,
            "gpu": gpu_metrics
        }
    
    def get_gpu_metrics(self) -> Dict[str, Any]:
        """Get GPU metrics if available."""
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]  # Primary GPU
                return {
                    "name": gpu.name,
                    "memory_used": gpu.memoryUsed,
                    "memory_total": gpu.memoryTotal,
                    "memory_percent": (gpu.memoryUsed / gpu.memoryTotal) * 100,
                    "temperature": gpu.temperature,
                    "load": gpu.load * 100
                }
        except ImportError:
            pass
        
        return {"available": False}
    
    def get_workspace_metrics(self) -> Dict[str, Any]:
        """Get workspace-specific metrics."""
        try:
            # File count and size
            total_files = 0
            total_size = 0
            
            for item in self.workspace_root.rglob("*"):
                if item.is_file():
                    total_files += 1
                    total_size += item.stat().st_size
            
            # Check for recent changes
            recent_changes = self.get_recent_changes()
            
            # Check log files for errors
            error_count = self.count_recent_errors()
            
            return {
                "total_files": total_files,
                "total_size": total_size,
                "recent_changes": recent_changes,
                "recent_errors": error_count,
                "last_backup": self.get_last_backup_time()
            }
        except Exception as e:
            logger.error(f"Error collecting workspace metrics: {e}")
            return {"error": str(e)}
    
    def get_service_metrics(self) -> Dict[str, Any]:
        """Get metrics for running services."""
        services = {
            "api_server": self.check_service_health("simple_api_server.py"),
            "training_service": self.check_service_health("advanced_llm_trainer.py"),
            "docker": self.check_docker_status()
        }
        
        return services
    
    def get_api_metrics(self) -> Dict[str, Any]:
        """Get API performance metrics."""
        try:
            import requests
            
            # Test API endpoints
            base_url = "http://localhost:8000"
            endpoints = ["/health", "/api/chat", "/api/models"]
            
            metrics = {}
            for endpoint in endpoints:
                try:
                    start_time = time.time()
                    response = requests.get(f"{base_url}{endpoint}", timeout=5)
                    response_time = time.time() - start_time
                    
                    metrics[endpoint] = {
                        "status_code": response.status_code,
                        "response_time": response_time,
                        "available": response.status_code == 200
                    }
                except Exception as e:
                    metrics[endpoint] = {
                        "error": str(e),
                        "available": False
                    }
            
            return metrics
        except ImportError:
            return {"error": "requests not available"}
    
    def check_alerts(self, metrics: Dict[str, Any]):
        """Check metrics against thresholds and generate alerts."""
        current_alerts = []
        
        # System alerts
        system = metrics.get("system", {})
        
        if system.get("cpu_percent", 0) > self.thresholds["cpu_percent"]:
            current_alerts.append({
                "type": "cpu_high",
                "severity": "warning",
                "message": f"High CPU usage: {system['cpu_percent']:.1f}%",
                "timestamp": metrics["timestamp"]
            })
        
        if system.get("memory_percent", 0) > self.thresholds["memory_percent"]:
            current_alerts.append({
                "type": "memory_high",
                "severity": "warning", 
                "message": f"High memory usage: {system['memory_percent']:.1f}%",
                "timestamp": metrics["timestamp"]
            })
        
        if system.get("disk_percent", 0) > self.thresholds["disk_percent"]:
            current_alerts.append({
                "type": "disk_full",
                "severity": "critical",
                "message": f"Disk nearly full: {system['disk_percent']:.1f}%",
                "timestamp": metrics["timestamp"]
            })
        
        # GPU alerts
        gpu = system.get("gpu", {})
        if gpu.get("memory_percent", 0) > self.thresholds["gpu_memory_percent"]:
            current_alerts.append({
                "type": "gpu_memory_high",
                "severity": "warning",
                "message": f"High GPU memory: {gpu['memory_percent']:.1f}%",
                "timestamp": metrics["timestamp"]
            })
        
        # API alerts
        api_metrics = metrics.get("api", {})
        for endpoint, data in api_metrics.items():
            if isinstance(data, dict):
                if not data.get("available", True):
                    current_alerts.append({
                        "type": "api_unavailable",
                        "severity": "critical",
                        "message": f"API endpoint {endpoint} unavailable",
                        "timestamp": metrics["timestamp"]
                    })
                elif data.get("response_time", 0) > self.thresholds["api_response_time"]:
                    current_alerts.append({
                        "type": "api_slow",
                        "severity": "warning",
                        "message": f"Slow API response for {endpoint}: {data['response_time']:.2f}s",
                        "timestamp": metrics["timestamp"]
                    })
        
        # Workspace alerts
        workspace = metrics.get("workspace", {})
        if workspace.get("recent_errors", 0) > 10:
            current_alerts.append({
                "type": "high_error_rate",
                "severity": "warning",
                "message": f"High error rate: {workspace['recent_errors']} errors in last hour",
                "timestamp": metrics["timestamp"]
            })
        
        # Add new alerts and notify
        for alert in current_alerts:
            if alert not in self.alerts:
                self.alerts.append(alert)
                self.send_alert(alert)
        
        # Clean old alerts (keep last 100)
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
    
    def display_status(self, metrics: Dict[str, Any]):
        """Display current system status."""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("🤖 AI Workspace Monitor - Live Status")
        print("=" * 60)
        print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # System metrics
        system = metrics.get("system", {})
        print("💻 System Resources:")
        print(f"   CPU: {system.get('cpu_percent', 0):.1f}% | Memory: {system.get('memory_percent', 0):.1f}% | Disk: {system.get('disk_percent', 0):.1f}%")
        
        # GPU if available
        gpu = system.get("gpu", {})
        if gpu.get("available", False):
            print(f"   GPU: {gpu.get('name', 'Unknown')} - {gpu.get('memory_percent', 0):.1f}% memory, {gpu.get('load', 0):.1f}% load")
        
        print()
        
        # Services
        services = metrics.get("services", {})
        print("🔧 Services:")
        for service, status in services.items():
            status_icon = "🟢" if status.get("running", False) else "🔴"
            print(f"   {status_icon} {service}")
        
        print()
        
        # Recent alerts
        recent_alerts = [a for a in self.alerts if self._is_recent(a["timestamp"])]
        if recent_alerts:
            print(f"🚨 Recent Alerts ({len(recent_alerts)}):")
            for alert in recent_alerts[-5:]:  # Show last 5
                severity_icon = "🔥" if alert["severity"] == "critical" else "⚠️"
                print(f"   {severity_icon} {alert['message']}")
        else:
            print("✅ No recent alerts")
        
        print(f"\n📊 Press Ctrl+C to stop monitoring")
    
    def check_service_health(self, service_name: str) -> Dict[str, Any]:
        """Check if a service is running."""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if service_name in cmdline:
                    return {
                        "running": True,
                        "pid": proc.info['pid'],
                        "cpu_percent": proc.cpu_percent(),
                        "memory_percent": proc.memory_percent()
                    }
            
            return {"running": False}
        except Exception as e:
            return {"error": str(e), "running": False}
    
    def check_docker_status(self) -> Dict[str, Any]:
        """Check Docker container status."""
        try:
            import subprocess
            result = subprocess.run(
                ["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}"],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                containers = []
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split('\t')
                        containers.append({
                            "name": parts[0],
                            "status": parts[1] if len(parts) > 1 else "unknown"
                        })
                
                return {
                    "available": True,
                    "containers": containers,
                    "count": len(containers)
                }
            else:
                return {"available": False, "error": result.stderr}
                
        except Exception as e:
            return {"available": False, "error": str(e)}
    
    def get_recent_changes(self) -> int:
        """Count recent file changes in workspace."""
        cutoff = datetime.now() - timedelta(hours=1)
        cutoff_timestamp = cutoff.timestamp()
        
        changes = 0
        try:
            for item in self.workspace_root.rglob("*"):
                if item.is_file() and item.stat().st_mtime > cutoff_timestamp:
                    changes += 1
        except Exception as e:
            logger.error(f"Error counting recent changes: {e}")
        
        return changes
    
    def count_recent_errors(self) -> int:
        """Count recent errors in log files."""
        error_count = 0
        logs_dir = self.workspace_root / "logs"
        
        if not logs_dir.exists():
            return 0
        
        cutoff = datetime.now() - timedelta(hours=1)
        
        try:
            for log_file in logs_dir.glob("*.log"):
                if log_file.stat().st_mtime > cutoff.timestamp():
                    with open(log_file, 'r') as f:
                        content = f.read().lower()
                        error_count += content.count('error')
                        error_count += content.count('exception')
                        error_count += content.count('traceback')
        except Exception as e:
            logger.error(f"Error counting errors: {e}")
        
        return error_count
    
    def get_last_backup_time(self) -> str:
        """Get timestamp of last backup."""
        backup_dir = self.workspace_root / "backups"
        
        if not backup_dir.exists():
            return "never"
        
        try:
            backup_files = list(backup_dir.glob("*"))
            if backup_files:
                latest = max(backup_files, key=lambda x: x.stat().st_mtime)
                return datetime.fromtimestamp(latest.stat().st_mtime).isoformat()
        except Exception as e:
            logger.error(f"Error getting backup time: {e}")
        
        return "unknown"
    
    def send_alert(self, alert: Dict[str, Any]):
        """Send alert notification."""
        print(f"\n🚨 ALERT: {alert['message']}")
        
        # Log to file
        self.log_alert(alert)
        
        # Could add email/Slack notifications here
        # self.send_email_alert(alert)
        # self.send_slack_alert(alert)
    
    def log_alert(self, alert: Dict[str, Any]):
        """Log alert to file."""
        logs_dir = self.workspace_root / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        alert_file = logs_dir / "alerts.log"
        with open(alert_file, 'a') as f:
            f.write(f"{alert['timestamp']} [{alert['severity'].upper()}] {alert['message']}\n")
    
    def log_metrics(self, metrics: Dict[str, Any]):
        """Log metrics to file."""
        logs_dir = self.workspace_root / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # Save detailed metrics
        metrics_file = logs_dir / f"metrics_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Load existing metrics for the day
        daily_metrics = []
        if metrics_file.exists():
            try:
                with open(metrics_file, 'r') as f:
                    daily_metrics = json.load(f)
            except Exception as e:
                logger.error(f"Error loading daily metrics: {e}")
                daily_metrics = []
        
        daily_metrics.append(metrics)
        
        # Keep only last 24 hours of data
        cutoff = datetime.now() - timedelta(hours=24)
        daily_metrics = [
            m for m in daily_metrics 
            if datetime.fromisoformat(m["timestamp"]) > cutoff
        ]
        
        with open(metrics_file, 'w') as f:
            json.dump(daily_metrics, f, indent=2)
    
    def _is_recent(self, timestamp_str: str, minutes: int = 10) -> bool:
        """Check if timestamp is within recent minutes."""
        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            cutoff = datetime.now() - timedelta(minutes=minutes)
            return timestamp > cutoff
        except Exception:
            return False
    
    def stop_monitoring(self):
        """Stop monitoring."""
        self.monitoring = False
        print("🛑 Monitoring stopped")
    
    def generate_report(self, hours: int = 24) -> Dict[str, Any]:
        """Generate monitoring report for last N hours."""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        # Filter metrics
        recent_metrics = [
            m for m in self.metrics_history
            if datetime.fromisoformat(m["timestamp"]) > cutoff
        ]
        
        # Filter alerts
        recent_alerts = [
            a for a in self.alerts
            if datetime.fromisoformat(a["timestamp"]) > cutoff
        ]
        
        # Calculate averages
        if recent_metrics:
            avg_cpu = sum(m["system"]["cpu_percent"] for m in recent_metrics) / len(recent_metrics)
            avg_memory = sum(m["system"]["memory_percent"] for m in recent_metrics) / len(recent_metrics)
            max_cpu = max(m["system"]["cpu_percent"] for m in recent_metrics)
            max_memory = max(m["system"]["memory_percent"] for m in recent_metrics)
        else:
            avg_cpu = avg_memory = max_cpu = max_memory = 0
        
        return {
            "period": f"Last {hours} hours",
            "metrics_count": len(recent_metrics),
            "alerts_count": len(recent_alerts),
            "averages": {
                "cpu_percent": avg_cpu,
                "memory_percent": avg_memory
            },
            "peaks": {
                "cpu_percent": max_cpu,
                "memory_percent": max_memory
            },
            "alerts_by_type": self._count_alerts_by_type(recent_alerts)
        }
    
    def _count_alerts_by_type(self, alerts: List[Dict]) -> Dict[str, int]:
        """Count alerts by type."""
        counts = {}
        for alert in alerts:
            alert_type = alert["type"]
            counts[alert_type] = counts.get(alert_type, 0) + 1
        return counts

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Workspace Monitor")
    parser.add_argument("--workspace", default="/workspaces/semantic-kernel/ai-workspace",
                       help="Workspace root directory")
    parser.add_argument("--interval", type=int, default=30,
                       help="Monitoring interval in seconds")
    parser.add_argument("--report", type=int,
                       help="Generate report for last N hours and exit")
    
    args = parser.parse_args()
    
    monitor = AIWorkspaceMonitor(args.workspace)
    
    if args.report:
        report = monitor.generate_report(args.report)
        print(json.dumps(report, indent=2))
    else:
        monitor.start_monitoring(args.interval)

if __name__ == "__main__":
    main()
