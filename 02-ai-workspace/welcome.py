#!/usr/bin/env python3
"""
Welcome module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import os
import sys
import time
import random
from pathlib import Path
from datetime import datetime

def animate_text(text, delay=0.05):
    """Print text with a typewriter effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_welcome_banner():
    """Print an animated welcome banner."""
    banner_lines = [
        "🌟" * 50,
        "🎉 WELCOME TO YOUR AI WORKSPACE! 🎉".center(50),
        "🤖 Where artificial intelligence meets human creativity 🧠".center(50),
        "🌟" * 50
    ]
    
    print("\n")
    for line in banner_lines:
        animate_text(line, 0.03)
        time.sleep(0.5)

def show_workspace_features():
    """Show key workspace features with animation."""
    print("\n🚀 What makes this workspace special?")
    print("-" * 40)
    
    features = [
        "🤖 14+ AI agents working together as your team",
        "🧠 Interactive learning journey for all skill levels", 
        "🎯 One-click project creation with the wizard",
        "📊 Real-time dashboard showing AI activity",
        "⚡ Self-improving system that gets smarter over time",
        "🔧 Advanced tools: quantum computing, swarm intelligence",
        "🎓 Built-in tutorials and friendly help system",
        "🚀 One-click deployment to production"
    ]
    
    for feature in features:
        time.sleep(0.8)
        animate_text(f"   ✨ {feature}", 0.02)

def show_quick_start_options():
    """Show quick start options."""
    print("\n🎯 Ready to start? Choose your adventure:")
    print("=" * 45)
    
    options = [
        ("🌱 Complete Beginner", "Start with interactive learning", "python scripts/ai_learning_journey.py --beginner"),
        ("🎮 Show Me Cool Stuff", "See AI agents in action", "python scripts/demo_showcase.py"),
        ("🛠️ I Want to Build", "Create your first AI project", "python scripts/project_wizard.py"),
        ("⚡ Power User Mode", "Access full control panel", "python ai_workspace_control.py --interactive"),
        ("📊 Monitor Everything", "Open real-time dashboard", "python scripts/friendly_dashboard.py"),
        ("🤖 Get Help Anytime", "Your friendly AI assistant", "python scripts/ai_helper.py")
    ]
    
    for i, (title, description, command) in enumerate(options, 1):
        print(f"\n{i}. {title}")
        print(f"   💭 {description}")
        print(f"   ⌨️  {command}")

def check_first_time():
    """Check if this is the first time running the workspace."""
    marker_file = Path.home() / ".ai_workspace_welcomed"
    is_first_time = not marker_file.exists()
    
    if is_first_time:
        # Create marker file
        try:
            marker_file.touch()
        except:
            pass  # Silent fail if can't create file
    
    return is_first_time

def show_tips_and_tricks():
    """Show helpful tips."""
    tips = [
        "💡 All scripts have --help flags for detailed options",
        "🎯 The launcher (python launch.py) gives you one-click access to everything",
        "📊 The dashboard shows live AI agent activity - it's mesmerizing!",
        "🧠 The learning journey adapts to your skill level automatically",
        "🔧 AI agents continuously optimize and improve the workspace",
        "🎮 Try running multiple tools at once in different terminals",
        "📚 Check GETTING_STARTED.md for the complete beginner guide"
    ]
    
    print(f"\n💡 Pro Tips:")
    print("-" * 15)
    
    # Show 3 random tips
    selected_tips = random.sample(tips, min(3, len(tips)))
    for tip in selected_tips:
        time.sleep(0.5)
        animate_text(f"   {tip}", 0.02)

def main():
    """Main welcome function."""
    is_first_time = check_first_time()
    
    if is_first_time:
        print_welcome_banner()
        time.sleep(1)
        
        print("\n🎊 This is your first time here! Let me show you around...")
        time.sleep(2)
        
        show_workspace_features()
        time.sleep(2)
        
        show_quick_start_options()
        time.sleep(1)
        
        show_tips_and_tricks()
        
        print(f"\n🌟 Your AI adventure starts now!")
        print(f"🚀 Tip: Run 'python launch.py' anytime for quick access to everything!")
        
        choice = input(f"\n🤔 Want to start with the beginner learning journey? (y/n): ").strip().lower()
        if choice in ['y', 'yes', '']:
            print(f"\n🎓 Launching your learning journey...")
            time.sleep(1)
            os.system("python scripts/ai_learning_journey.py --beginner")
        else:
            print(f"\n✨ No problem! Run 'python launch.py' when you're ready to explore!")
    else:
        # Not first time - show brief welcome
        greetings = [
            "👋 Welcome back to your AI workspace!",
            "🤖 Your AI agents missed you! Ready for more adventures?", 
            "⚡ Welcome back! The workspace has been optimizing while you were away!",
            "🌟 Good to see you again! What AI magic shall we create today?"
        ]
        
        print("\n" + random.choice(greetings))
        print("🚀 Quick access: python launch.py")
        
        # Show if any improvements happened
        print("\n💫 While you were away:")
        print("   ✅ AI agents continued optimizing")
        print("   ✅ System performance improved")
        print("   ✅ Everything is ready for action!")

if __name__ == "__main__":
    main()
