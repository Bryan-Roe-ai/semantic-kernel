#!/usr/bin/env python3
"""Local AI Demo (migrated sample)
Original path: repo root (demo_local_ai.py)
This file retains original functionality; legacy root file now acts as a deprecation shim.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def print_demo_header():
    print(
        """
╔══════════════════════════════════════════════════════════════════════════════╗
║                            🎬 LOCAL AI DEMO 🎬                               ║
║                     Quick Demonstration of Your AI System                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎯 This demo will show you what your local AI system can do!

✅ What's been set up for you:
   • Universal local LLM support (LM Studio, Ollama, etc.)
   • Multiple chat interfaces with different features
   • Plugin system for file analysis and processing
   • Backend API for custom integrations
   • Cross-platform launch scripts

🚀 Available interfaces:
   1. Advanced Chat - Full-featured with model controls
   2. Plugin Chat - Enhanced with file upload and plugins
   3. Simple Chat - Minimal interface for quick tests
   4. SK Demo - Semantic Kernel feature showcase

🛠️ Quick launch options:
   • Interactive: python setup_local_ai.py
   • Command line: ./local-ai start (Linux) or local-ai.bat (Windows)
   • Manual: Open any HTML file in 07-resources/public/

📚 Documentation:
   • README_LOCAL_AI.md - Complete user guide
   • LOCAL_AI_GUIDE.md - Detailed setup instructions
   • LM_STUDIO_README.md - LM Studio specific guide

🔧 What you need to get started:
   1. Install an AI model provider (LM Studio recommended)
   2. Run the setup script
   3. Start chatting!

Ready to try it? Let's go! 🚀
"""
    )


def main():
    print_demo_header()

    workspace = Path("/workspaces/semantic-kernel")
    print("📁 Your local AI files are located at:")
    print(f"   Workspace: {workspace}")
    print(f"   Setup Script: {workspace}/setup_local_ai.py")
    print(f"   Quick Launch: {workspace}/local-ai")
    print(f"   Documentation: {workspace}/README_LOCAL_AI.md")

    print("\n🎯 To get started right now:")
    print("   1. Run: python setup_local_ai.py")
    print("   2. Choose 'Quick Start' from the menu")
    print("   3. Follow the prompts")

    print("\n💡 Pro tip: Install LM Studio first for the best experience!")
    print("   Download from: https://lmstudio.ai/")

    response = input("\n🚀 Would you like to run the setup script now? (y/N): ")
    if response.lower() in ["y", "yes"]:
        try:
            subprocess.run([sys.executable, str(workspace / "setup_local_ai.py")])
        except KeyboardInterrupt:
            print("\n👋 Setup cancelled. You can run it anytime with: python setup_local_ai.py")
        except Exception as e:  # noqa: BLE001
            print(f"\n❌ Error running setup: {e}")
            print("💡 Try running it manually: python setup_local_ai.py")
    else:
        print("\n👍 No problem! You can start the setup anytime with:")
        print("   python setup_local_ai.py")

    print("\n🎉 Your local AI system is ready to use!")
    print("   Happy coding! 🤖✨")


if __name__ == "__main__":  # pragma: no cover - runtime entry
    main()
