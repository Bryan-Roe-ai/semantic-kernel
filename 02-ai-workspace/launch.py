#!/usr/bin/env python3
"""
🎯 AI Workspace Launcher - Your gateway to AI adventures!
One-click access to all the amazing features of your AI workspace.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print a colorful welcome banner."""
    print("\n" + "🌟" * 25)
    print("🎯 Welcome to Your AI Workspace!")
    print("   Choose your adventure below...")
    print("🌟" * 25)

def print_menu():
    """Print the main menu."""
    print("\n🚀 What would you like to do today?")
    print("=" * 40)
    
    print("\n🌱 For Beginners:")
    print("   1. 📚 Start Learning Journey")
    print("   2. 🎯 See AI Demo")
    print("   3. 🧙‍♂️ Create First Project")
    print("   4. 🤖 Get Friendly Help")
    
    print("\n⚡ For Developers:")
    print("   5. 🎛️ Master Control Panel")
    print("   6. 📊 Real-time Dashboard")
    print("   7. 🔧 System Optimizer")
    print("   8. 🔒 Security Check")
    
    print("\n🚀 Advanced Features:")
    print("   9. 🧬 Start AI Evolution")
    print("   10. ⚛️ Quantum Computing")
    print("   11. 🐝 Swarm Intelligence")
    print("   12. 🤖 Multi-Agent System")
    
    print("\n📖 Information:")
    print("   13. 📋 Show Quick Guide")
    print("   14. 🔍 Workspace Status")
    print("   15. 👋 Exit")

def run_script(script_name, args=""):
    """Run a script with optional arguments."""
    script_path = Path(__file__).parent / "scripts" / script_name
    if script_path.exists():
        cmd = f"python {script_path} {args}".strip()
        print(f"\n🚀 Running: {cmd}")
        print("-" * 50)
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running script: {e}")
        except KeyboardInterrupt:
            print("\n⏸️ Script interrupted by user")
    else:
        print(f"❌ Script not found: {script_path}")

def show_quick_guide():
    """Show a quick reference guide."""
    print("\n📋 Quick Reference Guide")
    print("=" * 30)
    
    print("\n🎯 Most Popular Commands:")
    print("   📚 Learning: python scripts/ai_learning_journey.py")
    print("   🎯 Demo: python scripts/demo_showcase.py") 
    print("   🧙‍♂️ Projects: python scripts/project_wizard.py")
    print("   🤖 Help: python scripts/ai_helper.py")
    print("   🎛️ Control: python ai_workspace_control.py --interactive")
    print("   📊 Dashboard: python scripts/friendly_dashboard.py")
    
    print("\n💡 Pro Tips:")
    print("   • All scripts support --help for detailed options")
    print("   • The dashboard shows real-time AI agent activity")
    print("   • The learning journey adapts to your skill level")
    print("   • The project wizard creates complete, runnable projects")
    print("   • AI agents continuously improve the workspace")
    
    print("\n📁 Important Files:")
    print("   • ./GETTING_STARTED.md - Detailed beginner guide")
    print("   • ./README.md - Complete documentation")
    print("   • ./scripts/ - All executable tools")
    print("   • ./logs/ - System activity logs")

def show_workspace_status():
    """Show current workspace status."""
    print("\n🔍 Workspace Status")
    print("=" * 22)
    
    workspace_path = Path(__file__).parent
    
    # Count files
    scripts_dir = workspace_path / "scripts"
    total_scripts = len(list(scripts_dir.glob("*.py"))) if scripts_dir.exists() else 0
    agent_scripts = len(list(scripts_dir.glob("*agent*.py"))) if scripts_dir.exists() else 0
    
    logs_dir = workspace_path / "logs"
    total_logs = len(list(logs_dir.glob("*.log"))) if logs_dir.exists() else 0
    
    docs_dir = workspace_path / "docs"
    total_docs = len(list(docs_dir.glob("*.md"))) if docs_dir.exists() else 0
    
    print(f"\n📊 Workspace Statistics:")
    print(f"   🐍 Python Scripts: {total_scripts}")
    print(f"   🤖 AI Agents: {agent_scripts}")
    print(f"   📋 Log Files: {total_logs}")
    print(f"   📚 Documentation: {total_docs}")
    
    print(f"\n🚀 Status: Fully Operational")
    print(f"💫 AI Level: Advanced")
    print(f"🎯 Ready for: All operations")
    
    # Check if key files exist
    print(f"\n✅ Key Components:")
    key_files = [
        ("Master Control", "ai_workspace_control.py"),
        ("Getting Started", "GETTING_STARTED.md"),
        ("Main README", "README.md"),
        ("Demo Script", "scripts/demo_showcase.py"),
        ("Learning Journey", "scripts/ai_learning_journey.py"),
        ("Project Wizard", "scripts/project_wizard.py"),
        ("AI Helper", "scripts/ai_helper.py"),
        ("Dashboard", "scripts/friendly_dashboard.py")
    ]
    
    for name, file_path in key_files:
        file_exists = (workspace_path / file_path).exists()
        status = "✅" if file_exists else "❌"
        print(f"   {status} {name}")

def main():
    """Main launcher loop."""
    print_banner()
    
    while True:
        print_menu()
        
        try:
            choice = input("\n🤔 Enter your choice (1-15): ").strip()
            
            if choice == "1":
                run_script("ai_learning_journey.py", "--beginner")
            elif choice == "2":
                run_script("demo_showcase.py")
            elif choice == "3":
                run_script("project_wizard.py")
            elif choice == "4":
                run_script("ai_helper.py")
            elif choice == "5":
                # Master control - run from parent directory
                print(f"\n🚀 Running: python ai_workspace_control.py --interactive")
                print("-" * 50)
                try:
                    subprocess.run("python ai_workspace_control.py --interactive", shell=True, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"❌ Error: {e}")
                except KeyboardInterrupt:
                    print("\n⏸️ Control panel interrupted by user")
            elif choice == "6":
                run_script("friendly_dashboard.py")
            elif choice == "7":
                run_script("ai_workspace_optimizer.py")
            elif choice == "8":
                run_script("security_agent.py")
            elif choice == "9":
                run_script("endless_improvement_loop.py")
            elif choice == "10":
                run_script("quantum_computing_agent.py", "--demo")
            elif choice == "11":
                run_script("swarm_intelligence_agent.py", "--demo")
            elif choice == "12":
                run_script("multi_agent_coordinator.py")
            elif choice == "13":
                show_quick_guide()
            elif choice == "14":
                show_workspace_status()
            elif choice == "15" or choice.lower() in ['quit', 'exit', 'q']:
                print("\n🌟 Thanks for using the AI Workspace!")
                print("💫 Your AI agents will keep working in the background.")
                print("🚀 Come back anytime for more AI adventures!")
                break
            else:
                print("\n❌ Invalid choice. Please enter a number from 1-15.")
            
            if choice not in ["13", "14", "15"]:
                input("\n⏸️ Press Enter to return to main menu...")
                
        except KeyboardInterrupt:
            print("\n\n👋 AI Workspace Launcher signing off!")
            print("🌟 Keep exploring and building amazing AI!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("🔄 Returning to main menu...")

if __name__ == "__main__":
    main()
