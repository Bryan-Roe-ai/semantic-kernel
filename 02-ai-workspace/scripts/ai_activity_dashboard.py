#!/usr/bin/env python3
"""
🎯 AI Activity Dashboard
Real-time dashboard for monitoring all AI activities, thoughts, and changes
"""

import json
import time
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import sqlite3
from collections import defaultdict, Counter
import sys
import os

# Add the scripts directory to Python path
sys.path.append(str(Path(__file__).parent))

try:
    from ai_activity_monitor import AIActivityMonitor, AIActivity, get_monitor
except ImportError:
    print("❌ Error: Could not import ai_activity_monitor. Make sure it's in the same directory.")
    sys.exit(1)

class AIActivityDashboard:
    """Real-time dashboard for AI activities"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.monitor = get_monitor()
        self.is_running = True
        
    def display_live_dashboard(self, refresh_interval: int = 5):
        """Display live updating dashboard"""
        try:
            while self.is_running:
                self._clear_screen()
                self._display_header()
                self._display_activity_summary()
                self._display_recent_activities()
                self._display_agent_performance()
                self._display_file_changes()
                self._display_activity_types()
                self._display_footer()
                
                time.sleep(refresh_interval)
        except KeyboardInterrupt:
            print("\n👋 Dashboard stopped by user")
    
    def _clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def _display_header(self):
        """Display dashboard header"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("🤖" + "="*70 + "🤖")
        print("🎯 AI ACTIVITY MONITORING DASHBOARD")
        print(f"📅 {now} | 🔄 Auto-refresh every 5 seconds")
        print("="*74)
        print()
    
    def _display_activity_summary(self):
        """Display activity summary statistics"""
        print("📊 ACTIVITY SUMMARY")
        print("-" * 30)
        
        # Get activities from last 24 hours
        since = (datetime.now() - timedelta(hours=24)).isoformat()
        recent_activities = self.monitor.db.get_activities(since=since)
        
        if not recent_activities:
            print("   No activities recorded in the last 24 hours")
            print()
            return
        
        # Calculate statistics
        total_activities = len(recent_activities)
        successful_activities = len([a for a in recent_activities if a.success is True])
        failed_activities = len([a for a in recent_activities if a.success is False])
        success_rate = (successful_activities / total_activities * 100) if total_activities > 0 else 0
        
        # Activity types count
        type_counts = Counter(a.activity_type for a in recent_activities)
        
        print(f"📈 Total Activities (24h): {total_activities}")
        print(f"✅ Successful: {successful_activities} ({success_rate:.1f}%)")
        print(f"❌ Failed: {failed_activities}")
        print(f"🔀 Activity Types: {', '.join(f'{t}({c})' for t, c in type_counts.most_common(3))}")
        print()
    
    def _display_recent_activities(self):
        """Display recent activities"""
        print("🕐 RECENT ACTIVITIES (Last 20)")
        print("-" * 50)
        
        recent = self.monitor.get_recent_activities(20)
        
        if not recent:
            print("   No recent activities found")
            print()
            return
        
        for activity in recent:
            # Format timestamp
            timestamp = datetime.fromisoformat(activity.timestamp.replace('Z', '+00:00'))
            time_str = timestamp.strftime("%H:%M:%S")
            
            # Status emoji
            if activity.success is True:
                status = "✅"
            elif activity.success is False:
                status = "❌"
            else:
                status = "⏳"
            
            # Activity type emoji
            type_emoji = {
                "action": "🎯",
                "thought": "💭",
                "decision": "🤔",
                "analysis": "📊",
                "change": "📝"
            }.get(activity.activity_type, "🔵")
            
            # Truncate description
            desc = activity.description[:45] + "..." if len(activity.description) > 45 else activity.description
            
            print(f"{status} {time_str} | {type_emoji} {activity.agent_name:12} | {desc}")
        
        print()
    
    def _display_agent_performance(self):
        """Display agent performance metrics"""
        print("🤖 AGENT PERFORMANCE")
        print("-" * 30)
        
        # Get activities from last hour
        since = (datetime.now() - timedelta(hours=1)).isoformat()
        recent_activities = self.monitor.db.get_activities(since=since)
        
        if not recent_activities:
            print("   No agent activities in the last hour")
            print()
            return
        
        # Group by agent
        agent_stats = defaultdict(lambda: {"total": 0, "success": 0, "failed": 0, "avg_duration": 0})
        
        for activity in recent_activities:
            agent = activity.agent_name
            agent_stats[agent]["total"] += 1
            
            if activity.success is True:
                agent_stats[agent]["success"] += 1
            elif activity.success is False:
                agent_stats[agent]["failed"] += 1
            
            if activity.duration_ms:
                agent_stats[agent]["avg_duration"] += activity.duration_ms
        
        # Calculate averages and display
        for agent, stats in list(agent_stats.items())[:8]:  # Top 8 agents
            total = stats["total"]
            success_rate = (stats["success"] / total * 100) if total > 0 else 0
            avg_duration = (stats["avg_duration"] / total) if total > 0 else 0
            
            # Status indicator
            if success_rate >= 90:
                status = "🟢"
            elif success_rate >= 70:
                status = "🟡"
            else:
                status = "🔴"
            
            print(f"{status} {agent:15} | Acts: {total:3} | Success: {success_rate:5.1f}% | Avg: {avg_duration:6.1f}ms")
        
        print()
    
    def _display_file_changes(self):
        """Display recent file changes"""
        print("📝 FILE CHANGES (Last 10)")
        print("-" * 35)
        
        # Get only file change activities
        since = (datetime.now() - timedelta(hours=1)).isoformat()
        all_activities = self.monitor.db.get_activities(since=since)
        file_changes = [a for a in all_activities if a.activity_type == "change"][:10]
        
        if not file_changes:
            print("   No file changes in the last hour")
            print()
            return
        
        for change in file_changes:
            timestamp = datetime.fromisoformat(change.timestamp.replace('Z', '+00:00'))
            time_str = timestamp.strftime("%H:%M:%S")
            
            change_type = change.details.get("change_type", "unknown")
            file_path = change.details.get("file_path", "unknown")
            
            # Change type emoji
            emoji = {
                "created": "➕",
                "modified": "✏️",
                "deleted": "🗑️"
            }.get(change_type, "📄")
            
            # Truncate path
            display_path = file_path[-40:] if len(file_path) > 40 else file_path
            
            print(f"{emoji} {time_str} | {change_type:8} | {display_path}")
        
        print()
    
    def _display_activity_types(self):
        """Display activity type breakdown"""
        print("📊 ACTIVITY TYPES (Last Hour)")
        print("-" * 40)
        
        since = (datetime.now() - timedelta(hours=1)).isoformat()
        recent_activities = self.monitor.db.get_activities(since=since)
        
        if not recent_activities:
            print("   No activities in the last hour")
            print()
            return
        
        type_counts = Counter(a.activity_type for a in recent_activities)
        total = len(recent_activities)
        
        for activity_type, count in type_counts.most_common():
            percentage = (count / total * 100) if total > 0 else 0
            bar_length = int(percentage / 2)  # Scale for display
            bar = "█" * bar_length + "░" * (50 - bar_length)
            
            emoji = {
                "action": "🎯",
                "thought": "💭",
                "decision": "🤔",
                "analysis": "📊",
                "change": "📝"
            }.get(activity_type, "🔵")
            
            print(f"{emoji} {activity_type:10} | {count:3} | {bar[:20]} {percentage:5.1f}%")
        
        print()
    
    def _display_footer(self):
        """Display dashboard footer"""
        print("="*74)
        print("🔄 Press Ctrl+C to stop monitoring | 📊 Live data updates every 5 seconds")
        print("💡 Tip: Use 'python ai_activity_dashboard.py --help' for more options")
    
    def export_report(self, hours: int = 24) -> Dict[str, Any]:
        """Export activity report for the last N hours"""
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        activities = self.monitor.db.get_activities(since=since)
        
        # Generate comprehensive report
        report = {
            "report_generated": datetime.now().isoformat(),
            "time_period_hours": hours,
            "total_activities": len(activities),
            "summary": self._generate_summary(activities),
            "agent_breakdown": self._generate_agent_breakdown(activities),
            "activity_timeline": self._generate_timeline(activities),
            "file_changes": self._generate_file_changes_report(activities),
            "performance_metrics": self._generate_performance_metrics(activities)
        }
        
        return report
    
    def _generate_summary(self, activities: List[AIActivity]) -> Dict[str, Any]:
        """Generate summary statistics"""
        if not activities:
            return {"message": "No activities found"}
        
        type_counts = Counter(a.activity_type for a in activities)
        agent_counts = Counter(a.agent_name for a in activities)
        
        successful = len([a for a in activities if a.success is True])
        failed = len([a for a in activities if a.success is False])
        
        return {
            "total_activities": len(activities),
            "success_rate": (successful / len(activities) * 100) if activities else 0,
            "activity_types": dict(type_counts),
            "most_active_agents": dict(agent_counts.most_common(5)),
            "time_range": {
                "earliest": min(a.timestamp for a in activities),
                "latest": max(a.timestamp for a in activities)
            }
        }
    
    def _generate_agent_breakdown(self, activities: List[AIActivity]) -> Dict[str, Any]:
        """Generate per-agent breakdown"""
        agent_data = defaultdict(lambda: {
            "total_activities": 0,
            "successful": 0,
            "failed": 0,
            "activity_types": defaultdict(int),
            "average_duration": 0,
            "total_duration": 0
        })
        
        for activity in activities:
            agent = activity.agent_name
            data = agent_data[agent]
            
            data["total_activities"] += 1
            data["activity_types"][activity.activity_type] += 1
            
            if activity.success is True:
                data["successful"] += 1
            elif activity.success is False:
                data["failed"] += 1
            
            if activity.duration_ms:
                data["total_duration"] += activity.duration_ms
        
        # Calculate averages
        for agent, data in agent_data.items():
            if data["total_activities"] > 0:
                data["average_duration"] = data["total_duration"] / data["total_activities"]
                data["success_rate"] = (data["successful"] / data["total_activities"]) * 100
        
        return dict(agent_data)
    
    def _generate_timeline(self, activities: List[AIActivity]) -> List[Dict[str, Any]]:
        """Generate activity timeline"""
        timeline = []
        for activity in sorted(activities, key=lambda a: a.timestamp)[-50:]:  # Last 50
            timeline.append({
                "timestamp": activity.timestamp,
                "agent": activity.agent_name,
                "type": activity.activity_type,
                "description": activity.description,
                "success": activity.success,
                "duration_ms": activity.duration_ms
            })
        return timeline
    
    def _generate_file_changes_report(self, activities: List[AIActivity]) -> Dict[str, Any]:
        """Generate file changes report"""
        file_changes = [a for a in activities if a.activity_type == "change"]
        
        if not file_changes:
            return {"message": "No file changes recorded"}
        
        change_types = Counter(a.details.get("change_type", "unknown") for a in file_changes)
        file_paths = Counter(a.details.get("file_path", "unknown") for a in file_changes)
        
        return {
            "total_changes": len(file_changes),
            "change_types": dict(change_types),
            "most_changed_files": dict(file_paths.most_common(10)),
            "recent_changes": [
                {
                    "timestamp": a.timestamp,
                    "type": a.details.get("change_type"),
                    "file": a.details.get("file_path"),
                    "size": a.details.get("file_size", 0)
                }
                for a in file_changes[-20:]
            ]
        }
    
    def _generate_performance_metrics(self, activities: List[AIActivity]) -> Dict[str, Any]:
        """Generate performance metrics"""
        durations = [a.duration_ms for a in activities if a.duration_ms is not None]
        
        if not durations:
            return {"message": "No duration data available"}
        
        return {
            "average_duration_ms": sum(durations) / len(durations),
            "min_duration_ms": min(durations),
            "max_duration_ms": max(durations),
            "total_processing_time_ms": sum(durations),
            "activities_with_timing": len(durations),
            "activities_without_timing": len(activities) - len(durations)
        }
    
    def save_report_to_file(self, hours: int = 24) -> str:
        """Save activity report to file"""
        report = self.export_report(hours)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_activity_report_{timestamp}.json"
        filepath = self.workspace_root / "02-ai-workspace" / "logs" / filename
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return str(filepath)

def main():
    """Main dashboard entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Activity Dashboard")
    parser.add_argument("--export", type=int, metavar="HOURS", 
                       help="Export report for last N hours instead of showing dashboard")
    parser.add_argument("--refresh", type=int, default=5, 
                       help="Dashboard refresh interval in seconds (default: 5)")
    
    args = parser.parse_args()
    
    # Get workspace root
    workspace_root = Path(__file__).parent.parent.parent
    
    dashboard = AIActivityDashboard(workspace_root)
    
    if args.export:
        print(f"📊 Generating AI activity report for last {args.export} hours...")
        filepath = dashboard.save_report_to_file(args.export)
        print(f"✅ Report saved to: {filepath}")
        
        # Also display summary
        report = dashboard.export_report(args.export)
        print(f"\n📈 Summary:")
        print(f"   Total Activities: {report['total_activities']}")
        print(f"   Success Rate: {report['summary'].get('success_rate', 0):.1f}%")
        print(f"   Most Active Agent: {list(report['summary']['most_active_agents'].keys())[0] if report['summary']['most_active_agents'] else 'None'}")
    else:
        print("🚀 Starting AI Activity Dashboard...")
        print("   Press Ctrl+C to stop")
        print()
        dashboard.display_live_dashboard(args.refresh)

if __name__ == "__main__":
    main()
