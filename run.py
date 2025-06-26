#!/usr/bin/env python3
"""
Quick Runner Script for Semantic Kernel Workspace

This is a simple entry point that provides quick access to the unified launcher
and common tasks.
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Quick entry point to unified launcher"""
    workspace_root = Path(__file__).parent.absolute()
    unified_launcher = workspace_root / "unified_launcher.py"
    
    # Check if unified launcher exists
    if not unified_launcher.exists():
        print("❌ Unified launcher not found!")
        print("Please ensure unified_launcher.py exists in the workspace root.")
        return 1
    
    try:
        # Run the unified launcher with all arguments passed through
        subprocess.run([sys.executable, str(unified_launcher)] + sys.argv[1:])
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
        
    return 0
            subprocess.run([sys.executable, str(master_launcher), "--list"])
            
        elif command == "run":
            # Run specific script
            if len(sys.argv) > 2:
                script_name = sys.argv[2]
                args = sys.argv[3:] if len(sys.argv) > 3 else []
                cmd = [sys.executable, str(master_launcher), "--script", script_name]
                if args:
                    cmd.extend(["--args"] + args)
                subprocess.run(cmd)
            else:
                print("Usage: python run.py run <script_name> [args...]")
                
        elif command == "category":
            # List scripts by category
            if len(sys.argv) > 2:
                category = sys.argv[2]
                subprocess.run([sys.executable, str(master_launcher), "--category", category])
            else:
                print("Usage: python run.py category <category_name>")
                
        elif command == "help" or command == "-h" or command == "--help":
            print_help()
            
        else:
            print(f"Unknown command: {command}")
            print_help()
    else:
        # Interactive mode
        subprocess.run([sys.executable, str(master_launcher)])

def print_help():
    """Print help information"""
    print("""
🚀 Semantic Kernel Quick Runner

Commands:
  fix           Fix all Python files in the workspace
  setup         Setup environment and dependencies  
  list          List all available scripts
  run <name>    Run a specific script by name
  category <c>  List scripts in a specific category
  help          Show this help message
  
  (no args)     Start interactive menu

Examples:
  python run.py fix
  python run.py list
  python run.py run ai_launcher
  python run.py category demos
  python run.py run main.py --debug
  
Categories: core, demos, tools, servers, tests, automation, monitoring, setup
""")

if __name__ == "__main__":
    main()
