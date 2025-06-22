#!/usr/bin/env python3
"""
Extended AutoMode Monitoring Dashboard
Real-time monitoring and analytics for ultra-long-term operation
"""

import os
import sys
import json
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
import psutil
import argparse
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import numpy as np


class ExtendedMonitoringDashboard:
    """Comprehensive monitoring dashboard for extended operation"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.state_dir = base_dir / ".extended_automode"
        self.db_path = self.state_dir / "metrics.db"
        self.reports_dir = self.state_dir / "analytics_reports"
    
    def get_system_overview(self) -> Dict[str, Any]:
        """Get current system overview"""
        # Current system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        boot_time = psutil.boot_time()
        
        # Process information
        process_count = len(psutil.pids())
        
        # Uptime calculation
        uptime_seconds = time.time() - boot_time
        uptime_days = uptime_seconds / (24 * 3600)
        
        return {
            "timestamp": time.time(),
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_total_gb": memory.total / (1024**3),
            "memory_available_gb": memory.available / (1024**3),
            "disk_percent": disk.percent,
            "disk_total_gb": disk.total / (1024**3),
            "disk_free_gb": disk.free / (1024**3),
            "process_count": process_count,
            "uptime_days": uptime_days
        }
    
    def get_automode_status(self) -> Dict[str, Any]:
        """Get Extended AutoMode status"""
        status = {
            "running": False,
            "pid": None,
            "uptime_seconds": 0,
            "uptime_days": 0,
            "startup_time": None
        }
        
        # Check PID file
        pid_file = self.state_dir / "extended.pid"
        if pid_file.exists():
            try:
                with open(pid_file) as f:
                    pid = int(f.read().strip())
                
                if psutil.pid_exists(pid):
                    status["running"] = True
                    status["pid"] = pid
                    
                    # Get process start time
                    process = psutil.Process(pid)
                    start_time = process.create_time()
                    status["startup_time"] = start_time
                    status["uptime_seconds"] = time.time() - start_time
                    status["uptime_days"] = status["uptime_seconds"] / (24 * 3600)
            except Exception as e:
                print(f"Error reading PID file: {e}")
        
        return status
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get metrics database statistics"""
        if not self.db_path.exists():
            return {"available": False}
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Count records in each table
                tables = ['system_metrics', 'process_metrics', 'events', 'predictions']
                stats = {"available": True, "tables": {}}
                
                for table in tables:
                    cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    stats["tables"][table] = count
                
                # Get database size
                stats["size_mb"] = self.db_path.stat().st_size / (1024 * 1024)
                
                # Get time range of data
                cursor = conn.execute("SELECT MIN(timestamp), MAX(timestamp) FROM system_metrics")
                min_time, max_time = cursor.fetchone()
                
                if min_time and max_time:
                    stats["data_range_days"] = (max_time - min_time) / (24 * 3600)
                    stats["earliest_record"] = datetime.fromtimestamp(min_time).isoformat()
                    stats["latest_record"] = datetime.fromtimestamp(max_time).isoformat()
                
                return stats
                
        except Exception as e:
            return {"available": False, "error": str(e)}
    
    def get_recent_trends(self, hours: int = 24) -> Dict[str, Any]:
        """Get recent system trends"""
        if not self.db_path.exists():
            return {}
        
        try:
            cutoff = time.time() - (hours * 3600)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT timestamp, cpu_percent, memory_percent, disk_percent, health_score
                    FROM system_metrics 
                    WHERE timestamp > ? 
                    ORDER BY timestamp
                """, (cutoff,))
                
                data = cursor.fetchall()
                
                if not data:
                    return {}
                
                # Calculate trends
                timestamps, cpu_data, memory_data, disk_data, health_data = zip(*data)
                
                trends = {
                    "data_points": len(data),
                    "time_range_hours": (max(timestamps) - min(timestamps)) / 3600,
                    "cpu": {
                        "current": cpu_data[-1],
                        "average": sum(cpu_data) / len(cpu_data),
                        "max": max(cpu_data),
                        "min": min(cpu_data)
                    },
                    "memory": {
                        "current": memory_data[-1],
                        "average": sum(memory_data) / len(memory_data),
                        "max": max(memory_data),
                        "min": min(memory_data)
                    },
                    "disk": {
                        "current": disk_data[-1],
                        "average": sum(disk_data) / len(disk_data),
                        "max": max(disk_data),
                        "min": min(disk_data)
                    },
                    "health_score": {
                        "current": health_data[-1],
                        "average": sum(health_data) / len(health_data),
                        "max": max(health_data),
                        "min": min(health_data)
                    }
                }
                
                return trends
                
        except Exception as e:
            return {"error": str(e)}
    
    def get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent system events"""
        if not self.db_path.exists():
            return []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT timestamp, event_type, severity, message, metadata
                    FROM events 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (limit,))
                
                events = []
                for row in cursor.fetchall():
                    timestamp, event_type, severity, message, metadata = row
                    events.append({
                        "timestamp": datetime.fromtimestamp(timestamp).isoformat(),
                        "event_type": event_type,
                        "severity": severity,
                        "message": message,
                        "metadata": json.loads(metadata) if metadata else None
                    })
                
                return events
                
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_analytics_reports(self) -> List[Dict[str, Any]]:
        """Get recent analytics reports"""
        if not self.reports_dir.exists():
            return []
        
        reports = []
        for report_file in sorted(self.reports_dir.glob("analytics_*.json"), reverse=True)[:5]:
            try:
                with open(report_file) as f:
                    report_data = json.load(f)
                    
                reports.append({
                    "filename": report_file.name,
                    "timestamp": report_data.get("timestamp", 0),
                    "uptime": report_data.get("uptime", 0),
                    "recommendations_count": len(report_data.get("recommendations", [])),
                    "predictions_count": len(report_data.get("predictions", {}))
                })
            except Exception as e:
                reports.append({
                    "filename": report_file.name,
                    "error": str(e)
                })
        
        return reports
    
    def print_dashboard(self):
        """Print comprehensive dashboard to console"""
        print("=" * 80)
        print("🔍 EXTENDED AUTOMODE MONITORING DASHBOARD")
        print("=" * 80)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # System Overview
        print("📊 SYSTEM OVERVIEW")
        print("-" * 40)
        overview = self.get_system_overview()
        print(f"CPU Usage:        {overview['cpu_percent']:6.1f}%")
        print(f"Memory Usage:     {overview['memory_percent']:6.1f}% ({overview['memory_available_gb']:.1f}GB available)")
        print(f"Disk Usage:       {overview['disk_percent']:6.1f}% ({overview['disk_free_gb']:.1f}GB free)")
        print(f"Process Count:    {overview['process_count']:6d}")
        print(f"System Uptime:    {overview['uptime_days']:6.1f} days")
        print()
        
        # AutoMode Status
        print("🤖 EXTENDED AUTOMODE STATUS")
        print("-" * 40)
        status = self.get_automode_status()
        if status["running"]:
            print(f"Status:           ✅ RUNNING (PID: {status['pid']})")
            print(f"AutoMode Uptime:  {status['uptime_days']:.1f} days")
            print(f"Started:          {datetime.fromtimestamp(status['startup_time']).strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("Status:           ❌ NOT RUNNING")
        print()
        
        # Database Statistics
        print("💾 METRICS DATABASE")
        print("-" * 40)
        db_stats = self.get_database_stats()
        if db_stats.get("available"):
            print(f"Database Size:    {db_stats['size_mb']:.1f} MB")
            print(f"Data Range:       {db_stats.get('data_range_days', 0):.1f} days")
            print("Record Counts:")
            for table, count in db_stats.get("tables", {}).items():
                print(f"  {table:15s}: {count:8,d}")
        else:
            print("Database:         ❌ NOT AVAILABLE")
            if "error" in db_stats:
                print(f"Error:            {db_stats['error']}")
        print()
        
        # Recent Trends
        print("📈 RECENT TRENDS (24 hours)")
        print("-" * 40)
        trends = self.get_recent_trends(24)
        if trends:
            print(f"Data Points:      {trends['data_points']:6d} ({trends['time_range_hours']:.1f} hours)")
            print()
            print("                  Current   Average   Min/Max")
            print(f"CPU Usage:        {trends['cpu']['current']:6.1f}%   {trends['cpu']['average']:6.1f}%   {trends['cpu']['min']:5.1f}%/{trends['cpu']['max']:5.1f}%")
            print(f"Memory Usage:     {trends['memory']['current']:6.1f}%   {trends['memory']['average']:6.1f}%   {trends['memory']['min']:5.1f}%/{trends['memory']['max']:5.1f}%")
            print(f"Disk Usage:       {trends['disk']['current']:6.1f}%   {trends['disk']['average']:6.1f}%   {trends['disk']['min']:5.1f}%/{trends['disk']['max']:5.1f}%")
            print(f"Health Score:     {trends['health_score']['current']:6.3f}    {trends['health_score']['average']:6.3f}    {trends['health_score']['min']:5.3f}/{trends['health_score']['max']:5.3f}")
        else:
            print("No trend data available")
        print()
        
        # Recent Events
        print("🚨 RECENT EVENTS")
        print("-" * 40)
        events = self.get_recent_events(5)
        if events:
            for event in events:
                if "error" in event:
                    print(f"Error retrieving events: {event['error']}")
                else:
                    timestamp = event['timestamp'][:19]  # Remove microseconds
                    severity_icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(event['severity'], "⚪")
                    print(f"{severity_icon} {timestamp} [{event['event_type']}] {event['message']}")
        else:
            print("No recent events")
        print()
        
        # Analytics Reports
        print("📋 ANALYTICS REPORTS")
        print("-" * 40)
        reports = self.get_analytics_reports()
        if reports:
            for report in reports:
                if "error" in report:
                    print(f"Error: {report['filename']} - {report['error']}")
                else:
                    timestamp = datetime.fromtimestamp(report['timestamp']).strftime('%Y-%m-%d %H:%M')
                    print(f"📄 {report['filename']}")
                    print(f"   Generated: {timestamp}")
                    print(f"   Recommendations: {report['recommendations_count']}, Predictions: {report['predictions_count']}")
        else:
            print("No analytics reports available")
        print()
        
        print("=" * 80)
        print("💡 Use './launch_extended_automode.sh health' for quick status")
        print("💡 Use '--plot' flag to generate trend graphs")
        print("=" * 80)
    
    def generate_plots(self, hours: int = 24):
        """Generate trend plots"""
        if not self.db_path.exists():
            print("❌ No database available for plotting")
            return
        
        try:
            cutoff = time.time() - (hours * 3600)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT timestamp, cpu_percent, memory_percent, disk_percent, health_score
                    FROM system_metrics 
                    WHERE timestamp > ? 
                    ORDER BY timestamp
                """, (cutoff,))
                
                data = cursor.fetchall()
                
                if not data:
                    print("❌ No data available for plotting")
                    return
                
                timestamps, cpu_data, memory_data, disk_data, health_data = zip(*data)
                
                # Convert timestamps to datetime objects
                dates = [datetime.fromtimestamp(ts) for ts in timestamps]
                
                # Create plots
                fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
                fig.suptitle(f'Extended AutoMode - System Trends (Last {hours} hours)', fontsize=16)
                
                # CPU Usage
                ax1.plot(dates, cpu_data, 'b-', linewidth=2)
                ax1.set_title('CPU Usage')
                ax1.set_ylabel('Percentage (%)')
                ax1.grid(True, alpha=0.3)
                ax1.tick_params(axis='x', rotation=45)
                
                # Memory Usage
                ax2.plot(dates, memory_data, 'g-', linewidth=2)
                ax2.set_title('Memory Usage')
                ax2.set_ylabel('Percentage (%)')
                ax2.grid(True, alpha=0.3)
                ax2.tick_params(axis='x', rotation=45)
                
                # Disk Usage
                ax3.plot(dates, disk_data, 'r-', linewidth=2)
                ax3.set_title('Disk Usage')
                ax3.set_ylabel('Percentage (%)')
                ax3.grid(True, alpha=0.3)
                ax3.tick_params(axis='x', rotation=45)
                
                # Health Score
                ax4.plot(dates, health_data, 'm-', linewidth=2)
                ax4.set_title('Health Score')
                ax4.set_ylabel('Score (0-1)')
                ax4.grid(True, alpha=0.3)
                ax4.tick_params(axis='x', rotation=45)
                
                plt.tight_layout()
                
                # Save plot
                plot_path = self.state_dir / f"trends_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                plt.savefig(plot_path, dpi=300, bbox_inches='tight')
                
                print(f"📊 Trend plot saved: {plot_path}")
                
                # Try to display if possible
                try:
                    plt.show()
                except Exception:
                    print("💡 Plot saved but cannot display (no GUI available)")
                
        except Exception as e:
            print(f"❌ Error generating plots: {e}")


def main():
    parser = argparse.ArgumentParser(description="Extended AutoMode Monitoring Dashboard")
    parser.add_argument("--base-dir", type=Path, default=Path.cwd(),
                       help="Base directory path")
    parser.add_argument("--plot", action="store_true",
                       help="Generate trend plots")
    parser.add_argument("--hours", type=int, default=24,
                       help="Hours of data to analyze (default: 24)")
    parser.add_argument("--json", action="store_true",
                       help="Output in JSON format")
    
    args = parser.parse_args()
    
    dashboard = ExtendedMonitoringDashboard(args.base_dir)
    
    if args.json:
        # Output JSON format for programmatic use
        data = {
            "system_overview": dashboard.get_system_overview(),
            "automode_status": dashboard.get_automode_status(),
            "database_stats": dashboard.get_database_stats(),
            "recent_trends": dashboard.get_recent_trends(args.hours),
            "recent_events": dashboard.get_recent_events(10),
            "analytics_reports": dashboard.get_analytics_reports()
        }
        print(json.dumps(data, indent=2, default=str))
    else:
        # Print human-readable dashboard
        dashboard.print_dashboard()
    
    if args.plot:
        dashboard.generate_plots(args.hours)


if __name__ == "__main__":
    main()
