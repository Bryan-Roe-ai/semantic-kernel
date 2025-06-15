#!/usr/bin/env python3
"""
AI Workspace Master Control
Central command center for all AI workspace operations.
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import argparse
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AIWorkspaceMasterControl:
    def __init__(self, workspace_root="/workspaces/semantic-kernel/ai-workspace"):
        self.workspace_root = Path(workspace_root)
        self.scripts_dir = self.workspace_root / "scripts"
        
        self.available_tools = {
            "optimizer": {
                "script": "ai_workspace_optimizer.py",
                "description": "Optimize workspace performance and clean up files",
                "commands": ["optimize", "quick-optimize"]
            },
            "monitor": {
                "script": "ai_workspace_monitor.py", 
                "description": "Real-time monitoring and alerting",
                "commands": ["monitor", "report"]
            },
            "deployment": {
                "script": "deployment_automator.py",
                "description": "Automated deployment to various environments",
                "commands": ["deploy", "validate", "list-deployments"]
            },
            "model-manager": {
                "script": "ai_model_manager.py",
                "description": "AI model lifecycle management",
                "commands": ["list-models", "download", "optimize-model", "benchmark"]
            },
            "mcp-test": {
                "script": "mcp_integration_test.py",
                "description": "Test MCP integration and GitHub connectivity",
                "commands": ["test-mcp", "validate-github"]
            },
            "api-test": {
                "script": "test_api_endpoints.sh",
                "description": "Test API endpoints and services",
                "commands": ["test-api", "health-check"]
            },
            "docker": {
                "script": "docker_manager.sh",
                "description": "Docker container management",
                "commands": ["docker-build", "docker-run", "docker-stop"]
            }
        }
    
    def show_dashboard(self):
        """Display interactive dashboard."""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("🤖 AI Workspace Master Control Center")
        print("=" * 60)
        print(f"📁 Workspace: {self.workspace_root}")
        print(f"🕐 Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # System status
        print("📊 System Status:")
        status = self._get_system_status()
        for component, state in status.items():
            icon = "🟢" if state else "🔴"
            print(f"   {icon} {component}")
        print()
        
        # Available tools
        print("🛠️  Available Tools:")
        for i, (tool_name, tool_info) in enumerate(self.available_tools.items(), 1):
            print(f"   {i}. {tool_name}: {tool_info['description']}")
        print()
        
        # Recent activity
        print("📈 Recent Activity:")
        recent_logs = self._get_recent_activity()
        for log_entry in recent_logs[-5:]:
            print(f"   • {log_entry}")
        print()
        
        print("💡 Type 'help' for commands or select a tool number (1-7)")
        print("   Or use: run <tool> <command> [args...]")
        print("   Example: run model-manager list-models")
        print()
    
    def interactive_mode(self):
        """Run interactive command mode."""
        self.show_dashboard()
        
        while True:
            try:
                user_input = input("🤖 ai-workspace> ").strip()
                
                if not user_input:
                    continue
                elif user_input.lower() in ['exit', 'quit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                elif user_input.lower() == 'dashboard':
                    self.show_dashboard()
                elif user_input.lower() == 'status':
                    self._show_detailed_status()
                elif user_input.isdigit():
                    tool_num = int(user_input)
                    self._run_tool_by_number(tool_num)
                elif user_input.startswith('run '):
                    self._parse_and_run_command(user_input[4:])
                else:
                    print(f"❓ Unknown command: {user_input}")
                    print("   Type 'help' for available commands")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def run_command(self, tool: str, command: str, args: List[str] = None):
        """Run a specific tool command."""
        if tool not in self.available_tools:
            raise ValueError(f"Unknown tool: {tool}")
        
        tool_info = self.available_tools[tool]
        script_path = self.scripts_dir / tool_info["script"]
        
        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")
        
        # Build command
        cmd = [sys.executable, str(script_path)]
        
        # Add command-specific arguments
        if command == "optimize" and tool == "optimizer":
            cmd.extend(["--workspace", str(self.workspace_root)])
        elif command == "quick-optimize" and tool == "optimizer":
            cmd.extend(["--workspace", str(self.workspace_root), "--quick"])
        elif command == "monitor" and tool == "monitor":
            cmd.extend(["--workspace", str(self.workspace_root)])
        elif command == "report" and tool == "monitor":
            cmd.extend(["--workspace", str(self.workspace_root), "--report", "24"])
        elif command == "deploy" and tool == "deployment":
            cmd.extend(["deploy", "--workspace", str(self.workspace_root)])
            if args:
                cmd.extend(args)
        elif command == "validate" and tool == "deployment":
            cmd.extend(["validate", "--workspace", str(self.workspace_root)])
        elif command == "list-deployments" and tool == "deployment":
            cmd.extend(["list", "--workspace", str(self.workspace_root)])
        elif command == "list-models" and tool == "model-manager":
            cmd.extend(["list", "--workspace", str(self.workspace_root)])
        elif command == "download" and tool == "model-manager":
            cmd.extend(["download", "--workspace", str(self.workspace_root)])
            if args:
                cmd.extend(args)
        elif tool == "mcp-test":
            # No additional args needed for MCP test
            pass
        elif tool == "api-test":
            # Shell script, different handling
            cmd = ["bash", str(script_path)]
        elif tool == "docker":
            cmd = ["bash", str(script_path)]
            if command == "docker-build":
                cmd.append("build")
            elif command == "docker-run":
                cmd.append("run")
            elif command == "docker-stop":
                cmd.append("stop")
        
        if args and tool not in ["api-test", "docker"]:
            cmd.extend(args)
        
        print(f"🚀 Running: {tool} {command}")
        print(f"📝 Command: {' '.join(cmd)}")
        print("-" * 50)
        
        # Execute command
        try:
            result = subprocess.run(cmd, cwd=self.workspace_root, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Error executing command: {e}")
            return False
    
    def batch_run(self, batch_file: str):
        """Run batch of commands from file."""
        batch_path = Path(batch_file)
        if not batch_path.exists():
            raise FileNotFoundError(f"Batch file not found: {batch_file}")
        
        print(f"📋 Running batch commands from: {batch_file}")
        
        with open(batch_path, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
        
        results = []
        for i, line in enumerate(lines, 1):
            print(f"\n🔄 Step {i}/{len(lines)}: {line}")
            
            # Parse command
            if line.startswith('run '):
                success = self._parse_and_run_command(line[4:])
            else:
                # Direct shell command
                result = subprocess.run(line, shell=True, cwd=self.workspace_root)
                success = result.returncode == 0
            
            results.append({"step": i, "command": line, "success": success})
            
            if not success:
                print(f"❌ Step {i} failed, stopping batch execution")
                break
            
            time.sleep(1)  # Brief pause between commands
        
        # Summary
        print(f"\n📊 Batch Execution Summary:")
        successful = sum(1 for r in results if r["success"])
        print(f"   ✅ Successful: {successful}/{len(results)}")
        print(f"   ❌ Failed: {len(results) - successful}/{len(results)}")
        
        return results
    
    def create_batch_file(self, commands: List[str], output_file: str):
        """Create batch file from list of commands."""
        with open(output_file, 'w') as f:
            f.write(f"# AI Workspace Batch Commands\n")
            f.write(f"# Created: {datetime.now().isoformat()}\n\n")
            
            for command in commands:
                f.write(f"{command}\n")
        
        print(f"📝 Batch file created: {output_file}")
    
    def _get_system_status(self) -> Dict[str, bool]:
        """Get current system status."""
        status = {}
        
        # Check workspace directory
        status["Workspace"] = self.workspace_root.exists()
        
        # Check Python environment
        status["Python"] = sys.version_info >= (3, 8)
        
        # Check Docker
        try:
            result = subprocess.run(["docker", "--version"], capture_output=True)
            status["Docker"] = result.returncode == 0
        except:
            status["Docker"] = False
        
        # Check API server
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=2)
            status["API Server"] = response.status_code == 200
        except:
            status["API Server"] = False
        
        # Check key directories
        required_dirs = ["scripts", "models", "logs", "06-backend-services"]
        status["Required Dirs"] = all((self.workspace_root / d).exists() for d in required_dirs)
        
        return status
    
    def _get_recent_activity(self) -> List[str]:
        """Get recent activity from logs."""
        logs_dir = self.workspace_root / "logs"
        if not logs_dir.exists():
            return ["No recent activity"]
        
        activities = []
        
        # Check recent log files
        for log_file in logs_dir.glob("*.log"):
            try:
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                if (datetime.now() - mtime).days < 1:
                    activities.append(f"{mtime.strftime('%H:%M')} - {log_file.stem}")
            except:
                pass
        
        return activities if activities else ["No recent activity"]
    
    def _show_help(self):
        """Show help information."""
        print("\n🆘 AI Workspace Master Control - Help")
        print("=" * 50)
        print("Available commands:")
        print("  help               - Show this help")
        print("  dashboard          - Show main dashboard")
        print("  status             - Show detailed system status")
        print("  exit/quit/q        - Exit the program")
        print("  1-7                - Select tool by number")
        print("  run <tool> <cmd>   - Run specific tool command")
        print()
        print("Available tools and commands:")
        
        for tool_name, tool_info in self.available_tools.items():
            print(f"\n🛠️  {tool_name}: {tool_info['description']}")
            for cmd in tool_info['commands']:
                print(f"     run {tool_name} {cmd}")
        
        print("\nExamples:")
        print("  run optimizer optimize")
        print("  run model-manager list-models")
        print("  run deployment deploy --environment staging")
        print()
    
    def _show_detailed_status(self):
        """Show detailed system status."""
        print("\n🔍 Detailed System Status")
        print("=" * 50)
        
        # System info
        print(f"🖥️  System: {os.name}")
        print(f"🐍 Python: {sys.version}")
        print(f"📁 Workspace: {self.workspace_root}")
        
        # Disk usage
        try:
            import shutil
            total, used, free = shutil.disk_usage(self.workspace_root)
            print(f"💾 Disk: {used/1024**3:.1f}GB used / {total/1024**3:.1f}GB total")
        except:
            print("💾 Disk: Unable to determine")
        
        # Directory sizes
        print("\n📊 Directory Sizes:")
        for item in self.workspace_root.iterdir():
            if item.is_dir():
                try:
                    size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                    print(f"   {item.name}: {size/1024**2:.1f} MB")
                except:
                    print(f"   {item.name}: Unable to calculate")
        
        # Service status
        print("\n🔧 Services:")
        status = self._get_system_status()
        for service, state in status.items():
            icon = "🟢" if state else "🔴"
            print(f"   {icon} {service}")
        
        print()
    
    def _run_tool_by_number(self, tool_num: int):
        """Run tool by number selection."""
        tools = list(self.available_tools.keys())
        
        if 1 <= tool_num <= len(tools):
            tool_name = tools[tool_num - 1]
            tool_info = self.available_tools[tool_name]
            
            print(f"\n🛠️  Selected: {tool_name}")
            print(f"📝 Description: {tool_info['description']}")
            print("Available commands:")
            
            for i, cmd in enumerate(tool_info['commands'], 1):
                print(f"   {i}. {cmd}")
            
            try:
                cmd_input = input(f"\nSelect command (1-{len(tool_info['commands'])}) or press Enter to cancel: ").strip()
                
                if cmd_input.isdigit():
                    cmd_num = int(cmd_input)
                    if 1 <= cmd_num <= len(tool_info['commands']):
                        command = tool_info['commands'][cmd_num - 1]
                        self.run_command(tool_name, command)
                    else:
                        print("❌ Invalid command number")
                elif cmd_input:
                    print("❌ Please enter a number")
                else:
                    print("🚫 Cancelled")
                    
            except KeyboardInterrupt:
                print("\n🚫 Cancelled")
        else:
            print(f"❌ Invalid tool number. Please select 1-{len(tools)}")
    
    def _parse_and_run_command(self, command_str: str) -> bool:
        """Parse and run command string."""
        parts = command_str.split()
        if len(parts) < 2:
            print("❌ Invalid command format. Use: <tool> <command> [args...]")
            return False
        
        tool = parts[0]
        command = parts[1]
        args = parts[2:] if len(parts) > 2 else []
        
        return self.run_command(tool, command, args)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="AI Workspace Master Control")
    parser.add_argument("--workspace", default="/workspaces/semantic-kernel/ai-workspace",
                       help="Workspace root directory")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Run in interactive mode")
    parser.add_argument("--batch", "-b", help="Run batch file")
    parser.add_argument("--tool", help="Tool to run")
    parser.add_argument("--command", help="Command to run")
    parser.add_argument("--args", nargs="*", help="Additional arguments")
    
    args = parser.parse_args()
    
    controller = AIWorkspaceMasterControl(args.workspace)
    
    try:
        if args.interactive or (not args.batch and not args.tool):
            controller.interactive_mode()
        elif args.batch:
            controller.batch_run(args.batch)
        elif args.tool and args.command:
            success = controller.run_command(args.tool, args.command, args.args)
            sys.exit(0 if success else 1)
        else:
            print("❌ Please specify --tool and --command, use --batch, or run in --interactive mode")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
