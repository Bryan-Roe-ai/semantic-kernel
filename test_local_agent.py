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

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

async def test_local_agent():
    """Test the local agent setup"""
    try:
        # Create kernel
        kernel = Kernel()

        # Create test agent
        test_agent = TestAgent()

        # Add agent functions to kernel
        kernel.add_plugin(test_agent, plugin_name="test_agent")

        # Test the functions
        logger.info("🧪 Testing agent functions...")

        # Test echo function
        echo_function = kernel.get_function("test_agent", "test_function")
        echo_result = await echo_function.invoke(kernel, message="Hello AGI!")
        logger.info(f"Echo test: {echo_result}")

        # Test status function
        status_function = kernel.get_function("test_agent", "get_status")
        status_result = await status_function.invoke(kernel)
        logger.info(f"Status test: {status_result}")

        logger.info("✅ Local agent test completed successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False

async def main():
    """Main test function"""
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
