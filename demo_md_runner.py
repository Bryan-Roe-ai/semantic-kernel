#!/usr/bin/env python3
"""
Simple example of running markdown files as AI
"""

import os
import sys


def main():
    print("🤖 AI Markdown Runner - Quick Demo")
    print("=" * 50)

    # Check if ai_markdown_runner.py exists
    if not os.path.exists("ai_markdown_runner.py"):
        print("❌ ai_markdown_runner.py not found")
        return

    # List available markdown files
    markdown_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))

    print(f"📁 Found {len(markdown_files)} markdown files")

    # Show some examples
    demo_files = [f for f in markdown_files if "demo" in f.lower()][:5]

    print("\n🎯 Demo files you can run:")
    for file in demo_files:
        print(f"  • {file}")

    print("\n🔧 How to run:")
    print("  python3 ai_markdown_runner.py <markdown_file>")

    print("\n💡 Examples:")
    if demo_files:
        print(f"  python3 ai_markdown_runner.py {demo_files[0]}")
    print("  python3 ai_markdown_runner.py docs/Getting_Started.md")

    print("\n🧠 AI Block Types:")
    print("  ```ai analyze")
    print("  Analyze this content")
    print("  ```")
    print()
    print("  ```ai generate")
    print("  Generate new content about...")
    print("  ```")
    print()
    print("  ```ai summarize")
    print("  Content to summarize...")
    print("  ```")
    print()
    print("  ```ai enhance")
    print("  Content to enhance...")
    print("  ```")
    print()
    print("  ```ai execute")
    print("  AI command to execute...")
    print("  ```")


if __name__ == "__main__":
    main()
