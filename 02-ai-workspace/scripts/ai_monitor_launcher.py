#!/usr/bin/env python3
"""
🚀 AI Activity Monitor Launcher
Easy setup and management of AI activity monitoring
"""

import sys
import os
import time
import subprocess
from pathlib import Path
import signal
import json
from datetime import datetime

# Add the scripts directory to Python path
sys.path.append(str(Path(__file__).parent))

try:
    from ai_activity_monitor import get_monitor, AIActivityMonitor
    from ai_activity_dashboard import AIActivityDashboard
    from ai_monitoring_integration import patch_existing_agents, get_logger
except ImportError as e:
    print(f"❌ Error importing monitoring modules: {e}")
    print("Make sure all monitoring scripts are in the same directory")
    sys.exit(1)

class AIMonitorLauncher:
    """Main launcher for AI monitoring system"""

    def __init__(self):
        self.workspace_root = Path(__file__).parent.parent.parent
        self.monitor = None
        self.dashboard = None
        self.is_running = False

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)

    def start_monitoring(self):
        """Start the AI activity monitoring system"""
        print("🚀 Starting AI Activity Monitoring System...")
        print(f"📁 Workspace: {self.workspace_root}")

        # Initialize monitor
        print("🔧 Initializing activity monitor...")
        self.monitor = get_monitor()

        # Patch existing agents
        print("🔌 Patching existing AI agents...")
        try:
            patch_existing_agents()
            print("✅ Agent patching completed")
        except Exception as e:
            print(f"⚠️  Warning: Could not patch all agents: {e}")

        # Log system startup
        system_logger = get_logger("MonitoringSystem")
        system_logger.action("system_startup", workspace=str(self.workspace_root))

        self.is_running = True
        print("✅ AI Activity Monitoring System is now running!")
        print()
        self._show_status()

    def start_dashboard(self):
        """Start the real-time dashboard"""
        if not self.is_running:
            self.start_monitoring()

        print("📊 Starting real-time dashboard...")
        self.dashboard = AIActivityDashboard(self.workspace_root)

        try:
            self.dashboard.display_live_dashboard()
        except KeyboardInterrupt:
            print("\n👋 Dashboard stopped")

    def stop(self):
        """Stop the monitoring system"""
        if self.is_running:
            print("🛑 Stopping AI Activity Monitoring System...")

            if self.monitor:
                self.monitor.stop()

            self.is_running = False
            print("✅ Monitoring system stopped")

    def _show_status(self):
        """Show current system status"""
        print("📊 SYSTEM STATUS")
        print("-" * 40)
        print(f"🔄 Monitoring: {'Running' if self.is_running else 'Stopped'}")
        print(f"📁 Workspace: {self.workspace_root}")
        print(f"💾 Database: {self.workspace_root}/02-ai-workspace/logs/ai_activities.db")
        print(f"📝 Logs: {self.workspace_root}/02-ai-workspace/logs/")
        print()

        # Show recent activity count
        if self.monitor:
            recent = self.monitor.get_recent_activities(5)
            print(f"📈 Recent activities: {len(recent)}")
            if recent:
                print("   Last 3 activities:")
                for activity in recent[:3]:
                    timestamp = activity.timestamp[-8:-3]  # Just time
                    print(f"   {timestamp} | {activity.agent_name:12} | {activity.description[:30]}")
        print()

    def generate_report(self, hours: int = 24):
        """Generate and save a comprehensive report"""
        if not self.is_running:
            self.start_monitoring()

        print(f"📊 Generating report for last {hours} hours...")

        dashboard = AIActivityDashboard(self.workspace_root)
        filepath = dashboard.save_report_to_file(hours)

        print(f"✅ Report saved to: {filepath}")

        # Show summary
        report = dashboard.export_report(hours)
        summary = report.get('summary', {})

        print("\n📈 REPORT SUMMARY")
        print("-" * 30)
        print(f"Total Activities: {summary.get('total_activities', 0)}")
        print(f"Success Rate: {summary.get('success_rate', 0):.1f}%")
        print(f"Most Active Agents:")

        most_active = summary.get('most_active_agents', {})
        for agent, count in list(most_active.items())[:3]:
            print(f"  {agent}: {count} activities")

        return filepath

    def show_live_feed(self, lines: int = 20):
        """Show live activity feed"""
        if not self.is_running:
            self.start_monitoring()

        print(f"📡 Live Activity Feed (showing last {lines} activities)")
        print("Press Ctrl+C to stop")
        print("-" * 60)

        try:
            last_seen = None
            while True:
                activities = self.monitor.get_recent_activities(lines)

                # Only show new activities
                new_activities = []
                for activity in activities:
                    if last_seen is None or activity.timestamp > last_seen:
                        new_activities.append(activity)

                if new_activities:
                    for activity in reversed(new_activities):  # Show oldest first
                        timestamp = datetime.fromisoformat(activity.timestamp.replace('Z', '+00:00'))
                        time_str = timestamp.strftime("%H:%M:%S")

                        # Status emoji
                        if activity.success is True:
                            status = "✅"
                        elif activity.success is False:
                            status = "❌"
                        else:
                            status = "⏳"

                        # Type emoji
                        type_emoji = {
                            "action": "🎯",
                            "thought": "💭",
                            "decision": "🤔",
                            "analysis": "📊",
                            "change": "📝"
                        }.get(activity.activity_type, "🔵")

                        desc = activity.description[:50] + "..." if len(activity.description) > 50 else activity.description

                        print(f"{status} {time_str} | {type_emoji} {activity.agent_name:15} | {desc}")

                    if activities:
                        last_seen = activities[0].timestamp

                time.sleep(2)  # Check every 2 seconds

        except KeyboardInterrupt:
            print("\n👋 Live feed stopped")

    def test_system(self):
        """Test the monitoring system with sample activities"""
        if not self.is_running:
            self.start_monitoring()

        print("🧪 Testing AI monitoring system...")

        # Create test logger
        test_logger = get_logger("TestAgent")

        # Generate test activities
        test_activities = [
            ("thought", "Analyzing system performance metrics"),
            ("decision", "Optimize memory usage", "High memory consumption detected", ["optimize", "ignore", "monitor"]),
            ("action", "cleanup_memory", {"memory_freed": "256MB", "files_processed": 47}),
            ("analysis", "performance_analysis", {"cpu_usage": 45.2, "memory_usage": 67.8, "disk_io": 23.4}),
            ("thought", "Planning next optimization cycle"),
            ("error", "Failed to access log file", {"error_code": "ENOENT", "file_path": "/tmp/missing.log"})
        ]

        for i, activity in enumerate(test_activities):
            print(f"  {i+1}/{len(test_activities)} Logging {activity[0]}...")

            if activity[0] == "thought":
                test_logger.thought(activity[1])
            elif activity[0] == "decision":
                test_logger.decision(activity[1], activity[2], activity[3])
            elif activity[0] == "action":
                test_logger.action(activity[1], **activity[2])
            elif activity[0] == "analysis":
                test_logger.analysis(activity[1], **activity[2])
            elif activity[0] == "error":
                test_logger.error(activity[1], **activity[2])

            time.sleep(0.5)  # Small delay between activities

        print("✅ Test activities generated")

        # Show results
        time.sleep(1)  # Allow processing
        recent = self.monitor.get_recent_activities(len(test_activities))
        print(f"\n📊 {len(recent)} activities recorded:")
        for activity in recent:
            print(f"  {activity.activity_type:10} | {activity.agent_name:12} | {activity.description[:40]}")

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="AI Activity Monitor Launcher")

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Start monitoring
    start_parser = subparsers.add_parser('start', help='Start monitoring system')

    # Dashboard
    dashboard_parser = subparsers.add_parser('dashboard', help='Start real-time dashboard')

    # Report
    report_parser = subparsers.add_parser('report', help='Generate activity report')
    report_parser.add_argument('--hours', type=int, default=24, help='Hours to include in report')

    # Live feed
    feed_parser = subparsers.add_parser('feed', help='Show live activity feed')
    feed_parser.add_argument('--lines', type=int, default=20, help='Number of activities to show')

    # Test
    test_parser = subparsers.add_parser('test', help='Test the monitoring system')

    # Status
    status_parser = subparsers.add_parser('status', help='Show system status')

    args = parser.parse_args()

    launcher = AIMonitorLauncher()

    if args.command == 'start':
        launcher.start_monitoring()
        print("✨ Use 'python ai_monitor_launcher.py dashboard' to view real-time data")
        print("💤 System will continue monitoring in background...")

        # Keep running
        try:
            while launcher.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            launcher.stop()

    elif args.command == 'dashboard':
        launcher.start_dashboard()

    elif args.command == 'report':
        launcher.generate_report(args.hours)

    elif args.command == 'feed':
        launcher.show_live_feed(args.lines)

    elif args.command == 'test':
        launcher.test_system()

    elif args.command == 'status':
        launcher.start_monitoring()
        launcher._show_status()

    else:
        # No command specified, show help and start dashboard
        parser.print_help()
        print("\n🚀 Starting dashboard by default...")
        launcher.start_dashboard()

if __name__ == "__main__":
    main()
