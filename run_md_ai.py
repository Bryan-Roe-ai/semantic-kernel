#!/usr/bin/env python3
"""Simple wrapper for running markdown files as AI"""

import asyncio
import sys
from pathlib import Path


async def run_md_as_ai(file_path):
    """Run markdown file with AI processing"""
    try:
        from enhanced_ai_runner import EnhancedAIMarkdownRunner

        runner = EnhancedAIMarkdownRunner()
    except ImportError:
        from ai_markdown_runner import AIMarkdownRunner

        runner = AIMarkdownRunner()

    print(f"🤖 Processing: {file_path}")
    print("=" * 50)

    result = await runner.run_markdown(file_path)

    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return

    print(f"📊 Status: {result['status']}")
    if "ai_blocks_found" in result:
        print(f"🔍 AI blocks found: {result['ai_blocks_found']}")

    print("=" * 50)

    # Show results
    for i, ai_result in enumerate(result.get("results", []), 1):
        print(f"\n🧠 AI Block {i}: {ai_result['type']}")
        print("-" * 30)
        print(f"📝 Input: {ai_result['input'][:100]}...")
        print(f"🤖 Output:\n{ai_result['output']}")
        print("-" * 30)

    # Handle files without AI blocks
    if result.get("status") == "no_ai_blocks":
        print("\n💡 No AI blocks found. This file can still be processed!")
        print("Add AI blocks like this:")
        print(
            """
```ai analyze
Analyze this content
```

```ai generate
Generate new content about...
```

```ai summarize
Content to summarize...
```
"""
        )


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 run_md_ai.py <markdown_file>")
        print("\nExamples:")
        print("  python3 run_md_ai.py simple_ai_demo.md")
        print("  python3 run_md_ai.py docs/Getting_Started.md")
        return

    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        return

    asyncio.run(run_md_as_ai(file_path))


if __name__ == "__main__":
    main()
