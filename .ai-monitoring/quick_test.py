#!/usr/bin/env python3
"""
🎯 Quick AI Monitoring Test
Simple test to verify the AI monitoring system is working
"""

import sys
import time
from pathlib import Path

# Add monitoring to path
monitoring_dir = Path(__file__).parent
sys.path.append(str(monitoring_dir))

def quick_test():
    """Quick test of AI monitoring system"""
    print("🚀 QUICK AI MONITORING TEST")
    print("=" * 40)

    try:
        # Import and initialize
        from universal_ai_monitor import get_universal_monitor
        print("✅ Successfully imported AI monitor")

        monitor = get_universal_monitor()
        print("✅ Monitor initialized")

        # Test basic logging
        print("\n🧪 Testing basic logging...")
        monitor.log_ai_thought("TestAgent", "Testing the monitoring system")
        monitor.log_ai_decision("TestAgent", "Run test", "Verify system works", ["test", "skip"])

        event_id, start_time = monitor.log_ai_action("TestAgent", "system_test")
        time.sleep(0.1)
        monitor.complete_ai_action(event_id, start_time, success=True)

        print("✅ Basic logging test passed")

        # Test status
        print("\n📊 System Status:")
        health = monitor._get_system_health()
        print(f"   Monitoring: {health['monitoring_status']}")
        print(f"   Active Agents: {health['active_agents']}")
        print(f"   Queue Size: {health['queue_size']}")
        print(f"   Cache Size: {health['cache_size']}")

        # Test recent activities
        recent = monitor.get_recent_activities(3)
        print(f"\n📈 Recent Activities ({len(recent)} found):")
        for i, activity in enumerate(recent, 1):
            print(f"   {i}. {activity.agent_name} | {activity.event_type} | {activity.description[:40]}...")

        print("\n🎉 AI MONITORING SYSTEM IS WORKING!")
        print("=" * 40)
        print("🔥 Your AI activities are being tracked!")
        print("🎯 Next: Run 'python ai_launcher.py dashboard' for real-time view")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Try: python ai_launcher.py setup")
        return False

if __name__ == "__main__":
    quick_test()
