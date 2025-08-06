#!/usr/bin/env python3
"""
Test module for local agent

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import asyncio
import logging
import sys
from pathlib import Path

# Allow running tests without installing the package
repo_root = Path(__file__).resolve().parent
local_package = repo_root / "01-core-implementations" / "python"
if local_package.exists():
    sys.path.insert(0, str(local_package))

from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function


def setup_logger() -> logging.Logger:
    """Configure and return a module logger."""
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

class TestAgent:
    """Simple test agent to verify setup"""

    @kernel_function(description="Simple test function")
    def test_function(self, message: str) -> str:
        """Test function that echoes the message"""
        return f"✅ Agent received: {message}"

    @kernel_function(description="Get system status")
    def get_status(self) -> str:
        """Returns system status"""
        return "🤖 AGI Agent System is running locally!"


def create_kernel() -> Kernel:
    """Create a kernel instance with the TestAgent plugin loaded."""
    kernel = Kernel()
    kernel.add_plugin(TestAgent(), plugin_name="test_agent")
    return kernel


async def run_echo_test(kernel: Kernel, logger: logging.Logger) -> None:
    """Run the echo function test and log the result."""
    echo_fn = kernel.get_function("test_agent", "test_function")
    echo_result = await echo_fn.invoke(kernel, message="Hello AGI!")
    logger.info("Echo test: %s", echo_result)


async def run_status_test(kernel: Kernel, logger: logging.Logger) -> None:
    """Run the status function test and log the result."""
    status_fn = kernel.get_function("test_agent", "get_status")
    status_result = await status_fn.invoke(kernel)
    logger.info("Status test: %s", status_result)

async def test_local_agent():
    """Run all local agent tests and return True if successful."""
    logger = setup_logger()
    try:
        kernel = create_kernel()

        logger.info("🧪 Testing agent functions...")
        await run_echo_test(kernel, logger)
        await run_status_test(kernel, logger)

    except Exception as e:
        logger.error("❌ Test failed: %s", e)
        return False

    logger.info("✅ Local agent test completed successfully!")
    return True

async def main():
    """Entry point for running the local agent tests."""
    print("🚀 Testing Local AGI Agent Setup...")
    print("=" * 50)

    success = await test_local_agent()

    if success:
        print("\n✅ Your local AGI agent setup is working!")
        print("🎯 You can now start your full AGI systems.")
    else:
        print("\n❌ Setup test failed. Check the logs for details.")

    return success

if __name__ == "__main__":
    asyncio.run(main())
