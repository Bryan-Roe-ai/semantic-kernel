#!/usr/bin/env python3
"""
Test module for direct ai

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import asyncio
from pathlib import Path


# Simple test
async def test_ai_processing():
    print("🧪 Testing AI Markdown Processing")

    # Test file
    test_content = """# Test Document

## Analysis Section
```ai analyze
Test this content for analysis.
```

## Generation Section
```ai generate
Generate some example content.
```
"""

    # Write test file
    test_file = Path("test_ai_processing.md")
    test_file.write_text(test_content)

    print(f"✅ Created test file: {test_file}")
    print(f"📄 Content:\n{test_content}")

    # Try to import and run
    try:
        from enhanced_ai_runner import EnhancedAIMarkdownRunner

        runner = EnhancedAIMarkdownRunner()

        print("🔄 Processing with enhanced runner...")
        result = await runner.run_markdown(str(test_file))

        print("📊 Result:")
        print(result)

    except Exception as e:
        print(f"❌ Error with enhanced runner: {e}")

        # Try basic runner
        try:
            from ai_markdown_runner import AIMarkdownRunner

            runner = AIMarkdownRunner()

            print("🔄 Processing with basic runner...")
            result = await runner.run_markdown(str(test_file))

            print("📊 Result:")
            print(result)

        except Exception as e2:
            print(f"❌ Error with basic runner: {e2}")

    # Cleanup
    if test_file.exists():
        test_file.unlink()
        print("🧹 Cleaned up test file")


if __name__ == "__main__":
    asyncio.run(test_ai_processing())
