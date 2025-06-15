#!/usr/bin/env python3
"""
Improvement Dashboard
Real-time dashboard for monitoring the endless improvement loop.
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImprovementDashboard:
    """Real-time dashboard for improvement loop monitoring."""

    def __init__(self, workspace_root: str = "/workspaces/semantic-kernel/ai-workspace"):
        self.workspace_root = Path(workspace_root)
        self.logs_dir = self.workspace_root / "logs"
        self.running = False
        self.dashboard_data = {
            "status": "initialized",
            "current_cycle": 0,
            "total_cycles": 0,
            "agents": {},
            "recent_actions": [],
            "performance_trends": [],
            "alerts": []
        }

    def start_dashboard(self, refresh_interval: int = 5):
        """Start the real-time dashboard."""
        self.running = True

        print("📊 Improvement Dashboard Starting")
        print("=" * 50)
        print(f"📁 Monitoring: {self.logs_dir}")
        print(f"🔄 Refresh interval: {refresh_interval} seconds")
        print("📺 Dashboard will update automatically...")
        print("🛑 Press Ctrl+C to stop\n")

        try:
            while self.running:
                self._update_dashboard_data()
                self._display_dashboard()
                time.sleep(refresh_interval)

        except KeyboardInterrupt:
            print("\n🛑 Dashboard stopped by user")
            self.running = False

    def _update_dashboard_data(self):
        """Update dashboard data from log files."""
        try:
            # Update cycle information
            self._update_cycle_info()

            # Update agent performance
            self._update_agent_performance()

            # Update recent actions
            self._update_recent_actions()

            # Update performance trends
            self._update_performance_trends()

            # Check for alerts
            self._check_alerts()

        except Exception as e:
            logger.error(f"Error updating dashboard data: {e}")

    def _update_cycle_info(self):
        """Update current cycle information."""
        cycle_files = list(self.logs_dir.glob("improvement_cycle_*.json"))

        if cycle_files:
            # Get latest cycle file
            latest_cycle = max(cycle_files, key=lambda x: x.stat().st_mtime)

            try:
                with open(latest_cycle, 'r') as f:
                    cycle_data = json.load(f)

                self.dashboard_data["current_cycle"] = cycle_data.get("cycle_number", 0)
                self.dashboard_data["total_cycles"] = len(cycle_files)
                self.dashboard_data["last_update"] = datetime.now().isoformat()

                # Check if cycle is currently running
                end_time = cycle_data.get("end_time")
                if end_time:
                    self.dashboard_data["status"] = "waiting"
                else:
                    self.dashboard_data["status"] = "running"

            except Exception as e:
                logger.error(f"Error reading cycle file {latest_cycle}: {e}")
        else:
            self.dashboard_data["status"] = "idle"

    def _update_agent_performance(self):
        """Update agent performance metrics."""
        cycle_files = list(self.logs_dir.glob("improvement_cycle_*.json"))

        if not cycle_files:
            return

        # Analyze last 5 cycles
        recent_cycles = sorted(cycle_files, key=lambda x: x.stat().st_mtime)[-5:]
        agent_stats = {}

        for cycle_file in recent_cycles:
            try:
                with open(cycle_file, 'r') as f:
                    cycle_data = json.load(f)

                agent_results = cycle_data.get("agent_results", {})

                for agent_name, result in agent_results.items():
                    if agent_name not in agent_stats:
                        agent_stats[agent_name] = {
                            "total_cycles": 0,
                            "total_score": 0.0,
                            "errors": 0
                        }

                    agent_stats[agent_name]["total_cycles"] += 1

                    if "error" in result:
                        agent_stats[agent_name]["errors"] += 1
                    else:
                        score = result.get("score", 0.0)
                        agent_stats[agent_name]["total_score"] += score

            except Exception as e:
                logger.error(f"Error reading cycle file {cycle_file}: {e}")

        # Calculate averages
        for agent_name, stats in agent_stats.items():
            if stats["total_cycles"] > 0:
                avg_score = stats["total_score"] / max(stats["total_cycles"] - stats["errors"], 1)
                error_rate = stats["errors"] / stats["total_cycles"]

                self.dashboard_data["agents"][agent_name] = {
                    "average_score": avg_score,
                    "error_rate": error_rate,
                    "total_cycles": stats["total_cycles"],
                    "status": "error" if error_rate > 0.5 else "good" if avg_score > 0.8 else "warning"
                }

    def _update_recent_actions(self):
        """Update recent actions list."""
        cycle_files = list(self.logs_dir.glob("improvement_cycle_*.json"))

        if not cycle_files:
            return

        recent_actions = []

        # Get actions from last 3 cycles
        recent_cycles = sorted(cycle_files, key=lambda x: x.stat().st_mtime)[-3:]

        for cycle_file in recent_cycles:
            try:
                with open(cycle_file, 'r') as f:
                    cycle_data = json.load(f)

                actions = cycle_data.get("actions_executed", [])
                cycle_num = cycle_data.get("cycle_number", 0)

                for action_data in actions:
                    action = action_data.get("action", {})
                    result = action_data.get("result", {})

                    recent_actions.append({
                        "cycle": cycle_num,
                        "name": action.get("name", "Unknown"),
                        "success": result.get("success", False),
                        "timestamp": result.get("execution_time", ""),
                        "priority": action.get("priority", 0)
                    })

            except Exception as e:
                logger.error(f"Error reading actions from {cycle_file}: {e}")

        # Sort by timestamp and keep last 10
        recent_actions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        self.dashboard_data["recent_actions"] = recent_actions[:10]

    def _update_performance_trends(self):
        """Update performance trends."""
        cycle_files = list(self.logs_dir.glob("improvement_cycle_*.json"))

        if not cycle_files:
            return

        trends = []

        # Get trends from last 10 cycles
        recent_cycles = sorted(cycle_files, key=lambda x: x.stat().st_mtime)[-10:]

        for cycle_file in recent_cycles:
            try:
                with open(cycle_file, 'r') as f:
                    cycle_data = json.load(f)

                trends.append({
                    "cycle": cycle_data.get("cycle_number", 0),
                    "score": cycle_data.get("overall_improvement_score", 0.0),
                    "actions": len(cycle_data.get("actions_executed", [])),
                    "timestamp": cycle_data.get("start_time", "")
                })

            except Exception as e:
                logger.error(f"Error reading trends from {cycle_file}: {e}")

        self.dashboard_data["performance_trends"] = trends

    def _check_alerts(self):
        """Check for system alerts."""
        alerts = []

        # Check for recent errors
        for agent_name, stats in self.dashboard_data["agents"].items():
            if stats.get("error_rate", 0) > 0.3:
                alerts.append({
                    "type": "error",
                    "message": f"{agent_name} agent has high error rate ({stats['error_rate']:.1%})",
                    "severity": "high"
                })
            elif stats.get("average_score", 1.0) < 0.5:
                alerts.append({
                    "type": "warning",
                    "message": f"{agent_name} agent has low performance score ({stats['average_score']:.2f})",
                    "severity": "medium"
                })

        # Check for stalled cycles
        if self.dashboard_data["status"] == "running":
            cycle_files = list(self.logs_dir.glob("improvement_cycle_*.json"))
            if cycle_files:
                latest_cycle = max(cycle_files, key=lambda x: x.stat().st_mtime)
                cycle_age = datetime.now() - datetime.fromtimestamp(latest_cycle.stat().st_mtime)

                if cycle_age > timedelta(minutes=10):
                    alerts.append({
                        "type": "warning",
                        "message": f"Current cycle has been running for {cycle_age}",
                        "severity": "medium"
                    })

        # Check performance trends
        trends = self.dashboard_data.get("performance_trends", [])
        if len(trends) >= 3:
            recent_scores = [t["score"] for t in trends[-3:]]
            if all(score < 0.5 for score in recent_scores):
                alerts.append({
                    "type": "warning",
                    "message": "Performance scores have been consistently low",
                    "severity": "high"
                })

        self.dashboard_data["alerts"] = alerts

    def _display_dashboard(self):
        """Display the dashboard."""
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')

        # Header
        print("🤖 ENDLESS IMPROVEMENT LOOP - DASHBOARD")
        print("=" * 80)
        print(f"🕒 Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📍 Status: {self._get_status_emoji()} {self.dashboard_data['status'].upper()}")
        print(f"🔄 Cycle: {self.dashboard_data['current_cycle']} / {self.dashboard_data['total_cycles']} total")
        print()

        # Alerts
        alerts = self.dashboard_data.get("alerts", [])
        if alerts:
            print("🚨 ALERTS")
            print("-" * 20)
            for alert in alerts[:3]:  # Show top 3 alerts
                severity_emoji = "🔴" if alert["severity"] == "high" else "🟡"
                print(f"{severity_emoji} {alert['message']}")
            print()

        # Agent Performance
        print("🤖 AGENT PERFORMANCE")
        print("-" * 30)
        agents = self.dashboard_data.get("agents", {})
        if agents:
            for agent_name, stats in agents.items():
                status_emoji = self._get_agent_status_emoji(stats["status"])
                score = stats["average_score"]
                error_rate = stats["error_rate"]
                print(f"{status_emoji} {agent_name:15} | Score: {score:.2f} | Errors: {error_rate:.1%} | Cycles: {stats['total_cycles']}")
        else:
            print("   No agent data available")
        print()

        # Recent Actions
        print("⚡ RECENT ACTIONS")
        print("-" * 25)
        actions = self.dashboard_data.get("recent_actions", [])
        if actions:
            for action in actions[:5]:  # Show last 5 actions
                success_emoji = "✅" if action["success"] else "❌"
                cycle = action["cycle"]
                name = action["name"][:25]  # Truncate long names
                priority = action["priority"]
                print(f"{success_emoji} Cycle {cycle:3} | P{priority} | {name}")
        else:
            print("   No recent actions")
        print()

        # Performance Trends
        print("📈 PERFORMANCE TRENDS")
        print("-" * 30)
        trends = self.dashboard_data.get("performance_trends", [])
        if len(trends) >= 2:
            latest_score = trends[-1]["score"]
            prev_score = trends[-2]["score"]
            trend_emoji = "📈" if latest_score > prev_score else "📉" if latest_score < prev_score else "➡️"

            print(f"   Current Score: {latest_score:.2f} {trend_emoji}")
            print(f"   Last 5 cycles: ", end="")

            for trend in trends[-5:]:
                score = trend["score"]
                if score > 0.8:
                    print("🟢", end="")
                elif score > 0.6:
                    print("🟡", end="")
                else:
                    print("🔴", end="")
            print()
        else:
            print("   Insufficient data for trends")
        print()

        # Footer
        print("💡 TIP: Use Ctrl+C to stop monitoring")
        print("🔄 Dashboard refreshes automatically")

    def _get_status_emoji(self) -> str:
        """Get emoji for current status."""
        status = self.dashboard_data.get("status", "unknown")
        emoji_map = {
            "running": "🔄",
            "waiting": "⏳",
            "idle": "😴",
            "error": "❌",
            "initialized": "🚀"
        }
        return emoji_map.get(status, "❓")

    def _get_agent_status_emoji(self, status: str) -> str:
        """Get emoji for agent status."""
        emoji_map = {
            "good": "🟢",
            "warning": "🟡",
            "error": "🔴"
        }
        return emoji_map.get(status, "⚪")

    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate a comprehensive summary report."""
        self._update_dashboard_data()

        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_cycles": self.dashboard_data["total_cycles"],
                "current_status": self.dashboard_data["status"],
                "active_alerts": len(self.dashboard_data.get("alerts", [])),
                "agents_count": len(self.dashboard_data.get("agents", {}))
            },
            "agent_performance": self.dashboard_data.get("agents", {}),
            "recent_actions_summary": {
                "total_actions": len(self.dashboard_data.get("recent_actions", [])),
                "success_rate": self._calculate_success_rate(),
                "top_priorities": self._get_top_priority_actions()
            },
            "performance_trends": self.dashboard_data.get("performance_trends", []),
            "alerts": self.dashboard_data.get("alerts", [])
        }

        return report

    def _calculate_success_rate(self) -> float:
        """Calculate success rate of recent actions."""
        actions = self.dashboard_data.get("recent_actions", [])
        if not actions:
            return 0.0

        successful = sum(1 for action in actions if action.get("success", False))
        return successful / len(actions)

    def _get_top_priority_actions(self) -> List[str]:
        """Get most common high-priority actions."""
        actions = self.dashboard_data.get("recent_actions", [])
        high_priority = [action["name"] for action in actions if action.get("priority", 0) >= 8]

        # Count occurrences
        action_counts = {}
        for action in high_priority:
            action_counts[action] = action_counts.get(action, 0) + 1

        # Return top 3
        return sorted(action_counts.keys(), key=lambda x: action_counts[x], reverse=True)[:3]

def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="Improvement Loop Dashboard")
    parser.add_argument("--workspace", type=str,
                       default="/workspaces/semantic-kernel/ai-workspace",
                       help="Path to workspace root")
    parser.add_argument("--interval", type=int, default=5,
                       help="Dashboard refresh interval in seconds")
    parser.add_argument("--report", action="store_true",
                       help="Generate summary report and exit")

    args = parser.parse_args()

    dashboard = ImprovementDashboard(args.workspace)

    if args.report:
        # Generate and display summary report
        report = dashboard.generate_summary_report()
        print("📊 IMPROVEMENT LOOP SUMMARY REPORT")
        print("=" * 50)
        print(json.dumps(report, indent=2))
    else:
        # Start interactive dashboard
        dashboard.start_dashboard(args.interval)

if __name__ == "__main__":
    main()
