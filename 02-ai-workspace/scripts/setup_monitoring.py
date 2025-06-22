#!/usr/bin/env python3
"""
🔧 AI Monitoring Setup
Sets up the AI activity monitoring system
"""

import os
import sys
from pathlib import Path
import subprocess

def setup_monitoring():
    """Set up the AI activity monitoring system"""
    
    print("🔧 Setting up AI Activity Monitoring System...")
    
    # Get workspace root
    workspace_root = Path(__file__).parent.parent.parent
    scripts_dir = Path(__file__).parent
    
    # Create necessary directories
    logs_dir = workspace_root / "02-ai-workspace" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Created logs directory: {logs_dir}")
    
    # Install dependencies
    requirements_file = workspace_root / "02-ai-workspace" / "requirements_monitoring.txt"
    
    if requirements_file.exists():
        print("📦 Installing dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                         check=True, capture_output=True, text=True)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: Could not install all dependencies: {e}")
            print("   You may need to install 'watchdog' manually: pip install watchdog")
    
    # Create a simple config file
    config = {
        "workspace_root": str(workspace_root),
        "logs_directory": str(logs_dir),
        "auto_monitor": True,
        "dashboard_refresh_interval": 5,
        "max_activities_in_memory": 1000
    }
    
    config_file = workspace_root / "02-ai-workspace" / "monitoring_config.json"
    import json
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"⚙️  Created config file: {config_file}")
    
    # Make launcher executable
    launcher_file = scripts_dir / "ai_monitor_launcher.py"
    if launcher_file.exists():
        os.chmod(launcher_file, 0o755)
        print(f"🚀 Made launcher executable: {launcher_file}")
    
    print("\n✅ AI Activity Monitoring System setup complete!")
    print("\n🎯 Quick Start:")
    print(f"   cd {scripts_dir}")
    print("   python ai_monitor_launcher.py dashboard")
    print("\n📊 Or generate a report:")
    print("   python ai_monitor_launcher.py report --hours 24")
    print("\n🧪 Test the system:")
    print("   python ai_monitor_launcher.py test")
    
    return True

if __name__ == "__main__":
    setup_monitoring()
