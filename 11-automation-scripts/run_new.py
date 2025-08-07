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

if __name__ == "__main__":
    sys.exit(main())
