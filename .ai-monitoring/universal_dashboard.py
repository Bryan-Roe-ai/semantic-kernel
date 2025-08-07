#!/usr/bin/env python3
"""
Universal Dashboard module

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
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import sqlite3
from collections import defaultdict, Counter

# Add monitoring to path
sys.path.append(str(Path(__file__).parent))

try:
    from universal_ai_monitor import get_universal_monitor, UniversalAIMonitor
except ImportError:
    print("❌ Error: Could not import universal_ai_monitor")
    sys.exit(1)

class UniversalAIDashboard:
    """Real-time dashboard for ALL AI activities across the repository"""

    def __init__(self):
        self.monitor = get_universal_monitor()
        self.workspace_root = self.monitor.workspace_root
        self.last_update = datetime.now()

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def display_header(self):
        """Display dashboard header"""
        print("🤖" + "="*76 + "🤖")
        print("🔍 UNIVERSAL AI ACTIVITY MONITORING DASHBOARD")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 🔄 Auto-refresh every 3 seconds")
        print("="*80)
        print()

    def display_overview(self):
        """Display system overview"""
        health = self.monitor._get_system_health()

        print("📊 SYSTEM OVERVIEW")
        print("-" * 40)
        print(f"🟢 Monitoring Status: {health['monitoring_status'].upper()}")
        print(f"⏱️  Uptime: {health['uptime_hours']:.1f} hours")
        print(f"🤖 Active Agents: {health['active_agents']}")
        print(f"📦 Event Queue: {health['queue_size']}")
        print(f"💾 Cache Size: {health['cache_size']}")
        print()

    def display_activity_summary(self):
        """Display activity summary"""
        # Get events from last 24 hours
        since = (datetime.now() - timedelta(hours=24)).isoformat()

        with sqlite3.connect(self.monitor.db_path) as conn:
            cursor = conn.execute("""
                SELECT event_type, COUNT(*) as count,
                       SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful
                FROM ai_events
                WHERE timestamp > ?
                GROUP BY event_type
                ORDER BY count DESC
            """, (since,))

            activities = cursor.fetchall()

            total_events = sum(row[1] for row in activities)
            total_successful = sum(row[2] for row in activities)
            success_rate = (total_successful / total_events * 100) if total_events > 0 else 0

            print("📈 ACTIVITY SUMMARY (24h)")
            print("-" * 35)
            print(f"📊 Total Events: {total_events:,}")
            print(f"✅ Success Rate: {success_rate:.1f}%")
            print(f"❌ Failed Events: {total_events - total_successful}")
            print()

            print("📋 Event Types:")
            for event_type, count, successful in activities[:8]:  # Top 8 types
                rate = (successful / count * 100) if count > 0 else 0
                emoji = self._get_event_emoji(event_type)
                print(f"  {emoji} {event_type:15} | {count:4d} | {rate:5.1f}%")
            print()

    def display_recent_activities(self, limit: int = 15):
        """Display recent AI activities"""
        recent_events = self.monitor._get_recent_events(limit)

        print("🕐 RECENT ACTIVITIES")
        print("-" * 60)

        if not recent_events:
            print("   No recent activities")
            print()
            return

        for event in recent_events:
            timestamp = datetime.fromisoformat(event["timestamp"].replace('Z', '+00:00'))
            time_str = timestamp.strftime("%H:%M:%S")

            # Status emoji
            status_emoji = "✅" if event["success"] else "❌" if event["success"] is False else "⏳"

            # Event type emoji
            type_emoji = self._get_event_emoji(event["event_type"])

            # Truncate description for display
            description = event["description"][:50] + "..." if len(event["description"]) > 50 else event["description"]

            # Agent name formatting
            agent_name = event["agent_name"][:15] + "..." if len(event["agent_name"]) > 15 else event["agent_name"]

            print(f"{status_emoji} {time_str} | {type_emoji} {agent_name:18} | {description}")

        print()

    def display_agent_performance(self):
        """Display agent performance metrics"""
        performance = self.monitor._get_performance_summary()

        print("🤖 AGENT PERFORMANCE")
        print("-" * 50)

        if not performance:
            print("   No performance data available")
            print()
            return

        # Sort by event count
        sorted_agents = sorted(performance.items(), key=lambda x: x[1]["event_count"], reverse=True)

        for agent_name, metrics in sorted_agents[:10]:  # Top 10 agents
            event_count = metrics["event_count"]
            success_rate = metrics["success_rate"]
            avg_duration = metrics["avg_duration_ms"]

            # Status indicator
            if success_rate >= 95:
                status = "🟢"
            elif success_rate >= 80:
                status = "🟡"
            else:
                status = "🔴"

            # Truncate agent name
            display_name = agent_name[:20] + "..." if len(agent_name) > 20 else agent_name

            print(f"{status} {display_name:23} | Events: {event_count:3d} | Success: {success_rate:5.1f}% | Avg: {avg_duration:6.1f}ms")

        print()

    def display_file_changes(self):
        """Display recent file changes"""
        since = (datetime.now() - timedelta(hours=2)).isoformat()

        with sqlite3.connect(self.monitor.db_path) as conn:
            cursor = conn.execute("""
                SELECT details, timestamp
                FROM ai_events
                WHERE event_type = 'file_change'
                AND timestamp > ?
                ORDER BY timestamp DESC
                LIMIT 10
            """, (since,))

            file_changes = cursor.fetchall()

        print("📝 FILE CHANGES (Last 2h)")
        print("-" * 40)

        if not file_changes:
            print("   No file changes in the last 2 hours")
            print()
            return

        for details_json, timestamp in file_changes:
            try:
                details = json.loads(details_json)
                timestamp_obj = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = timestamp_obj.strftime("%H:%M:%S")

                change_type = details.get("change_type", "unknown")
                file_path = details.get("file_path", "unknown")

                # Change type emoji
                emoji = {
                    "created": "➕",
                    "modified": "✏️",
                    "deleted": "🗑️"
                }.get(change_type, "📄")

                # Truncate path
                display_path = file_path[-35:] if len(file_path) > 35 else file_path

                print(f"{emoji} {time_str} | {change_type:8} | {display_path}")

            except (json.JSONDecodeError, ValueError):
                continue

        print()

    def display_agent_communications(self):
        """Display inter-agent communications"""
        with sqlite3.connect(self.monitor.db_path) as conn:
            cursor = conn.execute("""
                SELECT source_agent, target_agent, interaction_type, details, timestamp
                FROM agent_interactions
                WHERE timestamp > datetime('now', '-1 hour')
                ORDER BY timestamp DESC
                LIMIT 8
            """)

            communications = cursor.fetchall()

        print("📡 AGENT COMMUNICATIONS (1h)")
        print("-" * 45)

        if not communications:
            print("   No inter-agent communications")
            print()
            return

        for source, target, interaction_type, details_json, timestamp in communications:
            try:
                timestamp_obj = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = timestamp_obj.strftime("%H:%M:%S")

                details = json.loads(details_json)
                message = details.get("message", "No message")[:30]

                print(f"📡 {time_str} | {source} → {target} | {interaction_type}: {message}")

            except (json.JSONDecodeError, ValueError):
                continue

        print()

    def display_error_summary(self):
        """Display recent errors"""
        since = (datetime.now() - timedelta(hours=6)).isoformat()

        with sqlite3.connect(self.monitor.db_path) as conn:
            cursor = conn.execute("""
                SELECT agent_name, details, timestamp
                FROM ai_events
                WHERE event_type = 'error'
                AND timestamp > ?
                ORDER BY timestamp DESC
                LIMIT 5
            """, (since,))

            errors = cursor.fetchall()

        print("❌ RECENT ERRORS (6h)")
        print("-" * 30)

        if not errors:
            print("   🎉 No errors in the last 6 hours!")
            print()
            return

        for agent_name, details_json, timestamp in errors:
            try:
                timestamp_obj = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = timestamp_obj.strftime("%H:%M:%S")

                details = json.loads(details_json)
                error_type = details.get("error_type", "Unknown")
                error_msg = details.get("error_message", "No message")[:40]

                print(f"❌ {time_str} | {agent_name:15} | {error_type}: {error_msg}")

            except (json.JSONDecodeError, ValueError):
                continue

        print()

    def display_system_insights(self):
        """Display intelligent system insights"""
        print("🧠 SYSTEM INSIGHTS")
        print("-" * 25)

        # Get insights from recent data
        insights = self._generate_insights()

        for insight in insights[:5]:  # Top 5 insights
            print(f"💡 {insight}")

        if not insights:
            print("   🔍 Analyzing patterns...")

        print()

    def _generate_insights(self) -> List[str]:
        """Generate intelligent insights from activity data"""
        insights = []

        # Analyze recent activity patterns
        with sqlite3.connect(self.monitor.db_path) as conn:
            # Most active agents
            cursor = conn.execute("""
                SELECT agent_name, COUNT(*) as count
                FROM ai_events
                WHERE timestamp > datetime('now', '-1 hour')
                GROUP BY agent_name
                ORDER BY count DESC
                LIMIT 3
            """)

            top_agents = cursor.fetchall()
            if top_agents:
                insights.append(f"Most active agent: {top_agents[0][0]} ({top_agents[0][1]} events)")

            # Error patterns
            cursor = conn.execute("""
                SELECT COUNT(*) as error_count
                FROM ai_events
                WHERE event_type = 'error'
                AND timestamp > datetime('now', '-1 hour')
            """)

            error_count = cursor.fetchone()[0]
            if error_count > 5:
                insights.append(f"High error rate detected: {error_count} errors in last hour")
            elif error_count == 0:
                insights.append("System running smoothly - no errors in last hour")

            # Performance trends
            cursor = conn.execute("""
                SELECT AVG(duration_ms) as avg_duration
                FROM ai_events
                WHERE duration_ms IS NOT NULL
                AND timestamp > datetime('now', '-1 hour')
            """)

            avg_duration = cursor.fetchone()[0]
            if avg_duration and avg_duration > 1000:
                insights.append(f"Performance alert: Average action time {avg_duration:.0f}ms")

            # File activity
            cursor = conn.execute("""
                SELECT COUNT(*) as file_changes
                FROM ai_events
                WHERE event_type = 'file_change'
                AND timestamp > datetime('now', '-1 hour')
            """)

            file_changes = cursor.fetchone()[0]
            if file_changes > 20:
                insights.append(f"High file activity: {file_changes} changes in last hour")

        return insights

    def _get_event_emoji(self, event_type: str) -> str:
        """Get emoji for event type"""
        emoji_map = {
            "thought": "💭",
            "decision": "🎯",
            "action": "⚡",
            "analysis": "📊",
            "file_change": "📁",
            "error": "❌",
            "communication": "📡",
            "system": "🖥️",
            "completion": "✅",
            "performance_metrics": "📈"
        }
        return emoji_map.get(event_type, "🔍")

    def display_footer(self):
        """Display dashboard footer"""
        print("="*80)
        print("🔄 Press Ctrl+C to stop monitoring | Dashboard updates every 3 seconds")
        print("📊 For detailed reports, run: python universal_ai_monitor.py")

    def run_dashboard(self, refresh_interval: int = 3):
        """Run the real-time dashboard"""
        print("🚀 Starting Universal AI Activity Dashboard...")
        print("   Press Ctrl+C to stop")
        print()

        try:
            while True:
                self.clear_screen()
                self.display_header()
                self.display_overview()
                self.display_activity_summary()
                self.display_recent_activities()
                self.display_agent_performance()
                self.display_file_changes()
                self.display_agent_communications()
                self.display_error_summary()
                self.display_system_insights()
                self.display_footer()

                time.sleep(refresh_interval)

        except KeyboardInterrupt:
            print("\n\n🛑 Dashboard stopped by user")
            return
        except Exception as e:
            print(f"\n\n❌ Dashboard error: {e}")
            return

def main():
    """Main dashboard entry point"""
    dashboard = UniversalAIDashboard()

    if len(sys.argv) > 1:
        if sys.argv[1] == "report":
            # Generate and display report
            hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
            report = dashboard.monitor.generate_activity_report(hours=hours)
            print(json.dumps(report, indent=2))
        elif sys.argv[1] == "test":
            # Run test activities
            print("🧪 Running test activities...")
            dashboard.monitor.log_ai_thought("TestAgent", "Running dashboard test")
            dashboard.monitor.log_ai_decision("TestAgent", "Display test data", "Testing dashboard functionality")
            print("✅ Test activities logged")
        else:
            print("Usage: python universal_dashboard.py [report|test] [hours]")
    else:
        # Run real-time dashboard
        dashboard.run_dashboard()

if __name__ == "__main__":
    main()
