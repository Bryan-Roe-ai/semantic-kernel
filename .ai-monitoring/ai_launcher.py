#!/usr/bin/env python3
"""
🚀 AI Monitoring Launcher
One-stop launcher for all AI monitoring and repository organization features
"""

import sys
import os
import subprocess
import time
from pathlib import Path
import argparse

# Add monitoring to path
monitoring_dir = Path(__file__).parent
sys.path.append(str(monitoring_dir))

def run_dashboard():
    """Run the real-time AI activity dashboard"""
    print("🎯 Starting Universal AI Activity Dashboard...")
    try:
        from universal_dashboard import main as dashboard_main
        dashboard_main()
    except ImportError:
        print("❌ Could not import dashboard. Running as subprocess...")
        subprocess.run([sys.executable, str(monitoring_dir / "universal_dashboard.py")])

def run_monitor():
    """Start the AI monitoring system"""
    print("🔍 Starting Universal AI Monitor...")
    try:
        from universal_ai_monitor import get_universal_monitor
        monitor = get_universal_monitor()
        print("✅ AI Monitor started successfully")
        print("   Monitor is now tracking all AI activities")
        print("   Run 'python ai_launcher.py dashboard' to view activities")
        
        # Keep running
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print("\n🛑 AI Monitor stopped")
            monitor.stop_monitoring()
    except ImportError:
        print("❌ Could not import monitor")

def organize_repository(dry_run=False):
    """Organize the repository structure"""
    action = "🧪 Simulating" if dry_run else "🗂️ Organizing"
    print(f"{action} repository structure...")
    
    try:
        from repository_organizer import RepositoryOrganizer
        
        workspace_root = monitoring_dir.parent
        organizer = RepositoryOrganizer(workspace_root)
        
        if not dry_run:
            confirm = input("⚠️  This will reorganize your repository. Continue? (yes/no): ")
            if confirm.lower() != 'yes':
                print("❌ Operation cancelled")
                return
        
        result = organizer.organize_repository(dry_run=dry_run)
        
        if result["success"]:
            print("✅ Repository organization completed!")
            if not dry_run:
                print("📊 Check ORGANIZATION_COMPLETE_REPORT.md for details")
        else:
            print(f"❌ Organization failed: {result.get('error', 'Unknown error')}")
            
    except ImportError:
        print("❌ Could not import repository organizer")

def generate_report(hours=24):
    """Generate activity report"""
    print(f"📊 Generating AI activity report for last {hours} hours...")
    
    try:
        from universal_ai_monitor import get_universal_monitor
        monitor = get_universal_monitor()
        report = monitor.generate_activity_report(hours=hours, save_to_file=True)
        
        print(f"✅ Report generated with {report['total_events']} events")
        print(f"📁 Report saved to: {monitoring_dir / 'reports'}")
        
        # Print summary
        print("\n📊 SUMMARY:")
        print(f"   Active Agents: {len(report['active_agents'])}")
        print(f"   Event Types: {len(report['event_types'])}")
        print(f"   File Changes: {report['file_changes']['total_changes']}")
        print(f"   Total Errors: {report['error_analysis']['total_errors']}")
        
    except ImportError:
        print("❌ Could not import monitor for report generation")

def test_system():
    """Test the monitoring system with sample activities"""
    print("🧪 Testing AI monitoring system...")
    
    try:
        from universal_ai_monitor import get_universal_monitor
        monitor = get_universal_monitor()
        
        # Generate test activities
        monitor.log_ai_thought("TestAgent", "Running system test to verify monitoring")
        monitor.log_ai_decision("TestAgent", "Use test data", "Testing system functionality", 
                               ["test", "skip", "manual"], confidence=0.95)
        
        event_id, start_time = monitor.log_ai_action("TestAgent", "system_validation", 
                                                    component="monitoring_system")
        time.sleep(0.1)  # Simulate work
        monitor.complete_ai_action(event_id, start_time, success=True, result="System working correctly")
        
        monitor.log_agent_communication("TestAgent", "SystemMonitor", "Test complete", "status_update")
        
        print("✅ Test activities generated successfully")
        print("🎯 Run 'python ai_launcher.py dashboard' to see them in the dashboard")
        
    except ImportError:
        print("❌ Could not import monitor for testing")

def show_status():
    """Show system status"""
    print("📊 AI Monitoring System Status")
    print("=" * 40)
    
    try:
        from universal_ai_monitor import get_universal_monitor
        monitor = get_universal_monitor()
        
        health = monitor._get_system_health()
        performance = monitor._get_performance_summary()
        
        print(f"🟢 Status: {health['monitoring_status'].upper()}")
        print(f"⏱️  Uptime: {health['uptime_hours']:.1f} hours")
        print(f"🤖 Active Agents: {health['active_agents']}")
        print(f"📦 Queue Size: {health['queue_size']}")
        print(f"💾 Cache Size: {health['cache_size']}")
        
        if performance:
            print(f"\n🏆 Top Agents:")
            for agent, metrics in list(performance.items())[:3]:
                print(f"   {agent}: {metrics['event_count']} events, {metrics['success_rate']:.1f}% success")
        
    except ImportError:
        print("❌ Could not import monitor")
    except Exception as e:
        print(f"❌ Error getting status: {e}")

def setup_system():
    """Set up the AI monitoring system"""
    print("🔧 Setting up AI Monitoring System...")
    
    # Create necessary directories
    dirs_to_create = [
        monitoring_dir / "logs",
        monitoring_dir / "reports", 
        monitoring_dir / "config",
        monitoring_dir / "agents",
        monitoring_dir / "dashboards"
    ]
    
    for dir_path in dirs_to_create:
        dir_path.mkdir(exist_ok=True)
        print(f"📁 Created: {dir_path}")
    
    # Install dependencies
    try:
        required_packages = ["watchdog", "psutil", "sqlite3"]
        for package in required_packages:
            if package != "sqlite3":  # sqlite3 is built-in
                try:
                    __import__(package)
                    print(f"✅ {package} already installed")
                except ImportError:
                    print(f"📦 Installing {package}...")
                    subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                 check=True, capture_output=True)
                    print(f"✅ {package} installed")
    except Exception as e:
        print(f"⚠️  Warning: Could not install all dependencies: {e}")
    
    # Create config file
    config = {
        "monitoring_enabled": True,
        "dashboard_refresh_interval": 3,
        "max_events_in_memory": 10000,
        "file_watch_enabled": True,
        "performance_monitoring": True,
        "setup_completed": True
    }
    
    import json
    config_file = monitoring_dir / "config" / "monitoring_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"⚙️  Config created: {config_file}")
    print("✅ AI Monitoring System setup complete!")
    print("\n🚀 Quick Start:")
    print("   python ai_launcher.py dashboard    # Start real-time dashboard")
    print("   python ai_launcher.py test         # Test the system")
    print("   python ai_launcher.py status       # Check system status")

def main():
    """Main launcher entry point"""
    parser = argparse.ArgumentParser(
        description="🚀 AI Monitoring System Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Commands:
  dashboard         Start real-time AI activity dashboard
  monitor          Start background AI monitoring
  organize         Organize repository structure  
  organize-dry     Simulate repository organization
  report [hours]   Generate activity report (default: 24 hours)
  test             Test system with sample activities
  status           Show system status
  setup            Set up the monitoring system

Examples:
  python ai_launcher.py dashboard          # Real-time dashboard
  python ai_launcher.py report 48          # 48-hour report
  python ai_launcher.py organize-dry       # Simulate organization
        """
    )
    
    parser.add_argument('command', nargs='?', default='dashboard',
                       help='Command to execute (default: dashboard)')
    parser.add_argument('value', nargs='?', type=int, default=24,
                       help='Value for command (e.g., hours for report)')
    
    args = parser.parse_args()
    
    print("🤖 AI Monitoring System Launcher")
    print("=" * 40)
    
    command = args.command.lower()
    
    if command == 'dashboard':
        run_dashboard()
    elif command == 'monitor':
        run_monitor()
    elif command == 'organize':
        organize_repository(dry_run=False)
    elif command == 'organize-dry':
        organize_repository(dry_run=True)
    elif command == 'report':
        generate_report(hours=args.value)
    elif command == 'test':
        test_system()
    elif command == 'status':
        show_status()
    elif command == 'setup':
        setup_system()
    else:
        print(f"❌ Unknown command: {command}")
        parser.print_help()

if __name__ == "__main__":
    main()
