#!/usr/bin/env python3
import asyncio
import sys
from ai_markdown_runner import AIMarkdownRunner


async def test_runner():
    runner = AIMarkdownRunner()

    # Test with simple_ai_demo.md
    print("Testing simple_ai_demo.md...")
    try:
        result = await runner.run_markdown("simple_ai_demo.md")
        print("Result:", result)

        if result.get("status") == "processed":
            print(f"\n✅ Found {result['ai_blocks_found']} AI blocks")
            for i, ai_result in enumerate(result["results"], 1):
                print(f"\n🧠 AI Block {i}: {ai_result['type']}")
                print(f"Input: {ai_result['input'][:100]}...")
                print(f"Output: {ai_result['output'][:200]}...")
        else:
            print(f"Status: {result.get('status')}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_runner())
