#!/usr/bin/env python3
"""
Local Agent Launcher for Semantic Kernel AGI Systems
Comprehensive launcher for running various AGI agents and systems locally
"""

import os
import sys
import subprocess
import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import signal

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('local_agent_launcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LocalAgentLauncher:
    """Manages launching and monitoring local AGI agents"""

    def __init__(self, workspace_root: str = None):
        self.workspace_root = Path(workspace_root) if workspace_root else Path.cwd()
        self.running_processes = {}
        self.config = self.load_config()

    def load_config(self) -> Dict:
        """Load configuration for agents"""
        config_file = self.workspace_root / "agent_config.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return self.create_default_config()

    def create_default_config(self) -> Dict:
        """Create default configuration"""
        config = {
            "agents": {
                "agi_file_system": {
                    "script": "agi_file_update_system.py",
                    "description": "AGI File Update System",
                    "port": 8001,
                    "enabled": True
                },
                "agi_optimized": {
                    "script": "agi_file_update_system_optimized.py",
                    "description": "Optimized AGI File System",
                    "port": 8002,
                    "enabled": True
                },
                "agi_ultra_efficient": {
                    "script": "agi_ultra_efficient_file_system.py",
                    "description": "Ultra-Efficient AGI System",
                    "port": 8003,
                    "enabled": True
                },
                "agi_chat": {
                    "script": "agi_chat_integration.py",
                    "description": "AGI Chat Integration",
                    "port": 8004,
                    "enabled": True
                },
                "performance_monitor": {
                    "script": "agi_performance_monitor.py",
                    "description": "AGI Performance Monitor",
                    "port": 8005,
                    "enabled": True
                },
                "semantic_kernel_agents": {
                    "script": "01-core-implementations/python/samples/concepts/agents",
                    "description": "Semantic Kernel Example Agents",
                    "port": 8006,
                    "enabled": True
                }
            },
            "environment": {
                "python_path": ".venv/bin/python",
                "log_level": "INFO",
                "max_concurrent_agents": 5
            }
        }

        # Save default config
        config_file = self.workspace_root / "agent_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

        return config

    def check_environment(self) -> bool:
        """Check if environment is properly set up"""
        python_path = self.workspace_root / self.config["environment"]["python_path"]

        if not python_path.exists():
            logger.error(f"Python environment not found at {python_path}")
            return False

        # Check if semantic-kernel is installed
        try:
            result = subprocess.run(
                [str(python_path), "-c", "import semantic_kernel; print('OK')"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode != 0:
                logger.error("Semantic Kernel not installed in environment")
                return False
        except subprocess.TimeoutExpired:
            logger.error("Environment check timed out")
            return False

        logger.info("✅ Environment check passed")
        return True

    def list_available_agents(self):
        """List all available agents"""
        print("\n🤖 Available AGI Agents:")
        print("=" * 50)

        for agent_id, agent_config in self.config["agents"].items():
            status = "✅ Enabled" if agent_config["enabled"] else "❌ Disabled"
            script_path = self.workspace_root / agent_config["script"]
            exists = "📄 Found" if script_path.exists() else "❌ Missing"

            print(f"\n🔸 {agent_id}")
            print(f"   Description: {agent_config['description']}")
            print(f"   Script: {agent_config['script']}")
            print(f"   Port: {agent_config.get('port', 'N/A')}")
            print(f"   Status: {status}")
            print(f"   File: {exists}")

    def start_agent(self, agent_id: str) -> bool:
        """Start a specific agent"""
        if agent_id not in self.config["agents"]:
            logger.error(f"Agent {agent_id} not found")
            return False

        agent_config = self.config["agents"][agent_id]
        if not agent_config["enabled"]:
            logger.warning(f"Agent {agent_id} is disabled")
            return False

        script_path = self.workspace_root / agent_config["script"]
        if not script_path.exists():
            logger.error(f"Script not found: {script_path}")
            return False

        python_path = self.workspace_root / self.config["environment"]["python_path"]

        try:
            logger.info(f"🚀 Starting agent: {agent_id}")

            # Set environment variables
            env = os.environ.copy()
            env['PYTHONPATH'] = str(self.workspace_root)

            if script_path.is_file():
                # Start Python script
                process = subprocess.Popen(
                    [str(python_path), str(script_path)],
                    cwd=str(self.workspace_root),
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
            else:
                logger.info(f"Script directory found: {script_path}")
                return True

            self.running_processes[agent_id] = {
                'process': process,
                'config': agent_config,
                'started': datetime.now()
            }

            logger.info(f"✅ Agent {agent_id} started with PID {process.pid}")
            return True

        except Exception as e:
            logger.error(f"Failed to start agent {agent_id}: {e}")
            return False

    def stop_agent(self, agent_id: str) -> bool:
        """Stop a specific agent"""
        if agent_id not in self.running_processes:
            logger.warning(f"Agent {agent_id} is not running")
            return False

        try:
            process_info = self.running_processes[agent_id]
            process = process_info['process']

            logger.info(f"🛑 Stopping agent: {agent_id}")
            process.terminate()

            # Wait for graceful shutdown
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logger.warning(f"Force killing agent {agent_id}")
                process.kill()
                process.wait()

            del self.running_processes[agent_id]
            logger.info(f"✅ Agent {agent_id} stopped")
            return True

        except Exception as e:
            logger.error(f"Failed to stop agent {agent_id}: {e}")
            return False

    def status_agents(self):
        """Show status of all agents"""
        print("\n📊 Agent Status:")
        print("=" * 50)

        if not self.running_processes:
            print("No agents currently running")
            return

        for agent_id, process_info in self.running_processes.items():
            process = process_info['process']
            config = process_info['config']
            started = process_info['started']

            # Check if process is still running
            if process.poll() is None:
                status = "🟢 Running"
                uptime = datetime.now() - started
            else:
                status = "🔴 Stopped"
                uptime = "N/A"

            print(f"\n🔸 {agent_id}")
            print(f"   Status: {status}")
            print(f"   PID: {process.pid}")
            print(f"   Port: {config.get('port', 'N/A')}")
            print(f"   Uptime: {uptime}")

    def start_all_enabled(self):
        """Start all enabled agents"""
        logger.info("🚀 Starting all enabled agents...")

        started_count = 0
        for agent_id, agent_config in self.config["agents"].items():
            if agent_config["enabled"]:
                if self.start_agent(agent_id):
                    started_count += 1

        logger.info(f"✅ Started {started_count} agents")

    def stop_all(self):
        """Stop all running agents"""
        logger.info("🛑 Stopping all agents...")

        for agent_id in list(self.running_processes.keys()):
            self.stop_agent(agent_id)

        logger.info("✅ All agents stopped")

    def interactive_menu(self):
        """Interactive menu for managing agents"""
        while True:
            print("\n" + "="*60)
            print("🤖 Local AGI Agent Management System")
            print("="*60)
            print("1. List available agents")
            print("2. Start specific agent")
            print("3. Stop specific agent")
            print("4. Show agent status")
            print("5. Start all enabled agents")
            print("6. Stop all agents")
            print("7. Environment check")
            print("8. View logs")
            print("9. Exit")
            print("="*60)

            choice = input("\nSelect option (1-9): ").strip()

            if choice == "1":
                self.list_available_agents()
            elif choice == "2":
                self.list_available_agents()
                agent_id = input("\nEnter agent ID to start: ").strip()
                self.start_agent(agent_id)
            elif choice == "3":
                self.status_agents()
                agent_id = input("\nEnter agent ID to stop: ").strip()
                self.stop_agent(agent_id)
            elif choice == "4":
                self.status_agents()
            elif choice == "5":
                self.start_all_enabled()
            elif choice == "6":
                self.stop_all()
            elif choice == "7":
                self.check_environment()
            elif choice == "8":
                self.view_logs()
            elif choice == "9":
                self.stop_all()
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid option")

            input("\nPress Enter to continue...")

    def view_logs(self):
        """View recent logs"""
        log_file = self.workspace_root / "local_agent_launcher.log"
        if log_file.exists():
            print("\n📄 Recent Logs:")
            print("-" * 50)
            with open(log_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-20:]:  # Show last 20 lines
                    print(line.rstrip())
        else:
            print("No log file found")

def signal_handler(signum, frame, launcher):
    """Handle shutdown signals"""
    print("\n🛑 Shutdown signal received...")
    launcher.stop_all()
    sys.exit(0)

def main():
    """Main function"""
    print("🚀 Initializing Local AGI Agent Launcher...")

    launcher = LocalAgentLauncher()

    # Setup signal handlers
    signal.signal(signal.SIGINT, lambda s, f: signal_handler(s, f, launcher))
    signal.signal(signal.SIGTERM, lambda s, f: signal_handler(s, f, launcher))

    # Check environment
    if not launcher.check_environment():
        print("❌ Environment check failed. Please fix issues and try again.")
        sys.exit(1)

    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "list":
            launcher.list_available_agents()
        elif command == "start":
            if len(sys.argv) > 2:
                agent_id = sys.argv[2]
                launcher.start_agent(agent_id)
            else:
                launcher.start_all_enabled()
        elif command == "stop":
            if len(sys.argv) > 2:
                agent_id = sys.argv[2]
                launcher.stop_agent(agent_id)
            else:
                launcher.stop_all()
        elif command == "status":
            launcher.status_agents()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python local_agent_launcher.py [list|start|stop|status] [agent_id]")
    else:
        # Interactive mode
        launcher.interactive_menu()

if __name__ == "__main__":
    main()
