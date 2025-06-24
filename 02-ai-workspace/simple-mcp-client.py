#!/usr/bin/env python3
"""
Simple-Mcp-Client module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import asyncio
import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleAGIMCPClient:
    """Simple client for testing AGI MCP Server"""

    def __init__(self):
        self.server_process = None

    async def test_server_startup(self):
        """Test that the AGI MCP server starts successfully"""
        try:
            server_path = Path(__file__).parent / "mcp-agi-server.py"
            venv_python = Path(__file__).parent / "agi-venv" / "bin" / "python"

            # Start the server process
            logger.info("🚀 Starting AGI MCP Server...")
            self.server_process = subprocess.Popen(
                [str(venv_python), str(server_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Wait a moment for startup
            await asyncio.sleep(2)

            # Check if process is running
            if self.server_process.poll() is None:
                logger.info("✅ AGI MCP Server started successfully!")
                return True
            else:
                stderr_output = self.server_process.stderr.read()
                logger.error(f"❌ Server failed to start: {stderr_output}")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to start AGI MCP server: {e}")
            return False

    def stop_server(self):
        """Stop the AGI MCP server"""
        if self.server_process:
            logger.info("🛑 Stopping AGI MCP Server...")
            self.server_process.terminate()
            self.server_process.wait()
            logger.info("✅ AGI MCP Server stopped")

async def demo_simple_startup_test():
    """Simple demonstration of AGI MCP server startup"""
    print("🤖 Simple AGI MCP Client Demo")
    print("=" * 50)

    client = SimpleAGIMCPClient()

    try:
        # Test server startup
        print("\n🚀 Testing AGI MCP Server startup...")
        startup_success = await client.test_server_startup()

        if startup_success:
            print("✅ AGI MCP Server is running successfully!")
            print("🔧 Available AGI Tools:")
            print("   • reasoning_engine - Advanced reasoning capabilities")
            print("   • multimodal_processor - Process multi-modal content")
            print("   • autonomous_task_executor - Execute autonomous tasks")
            print("   • knowledge_synthesizer - Synthesize knowledge from sources")
            print("   • creative_generator - Generate creative content")
            print("   • ethical_evaluator - Evaluate ethical scenarios")
            print("   • meta_cognitive_analyzer - Analyze thinking processes")
            print("   • system_status - Get system status")
            print("\n🎯 The AGI MCP Server is ready for client connections!")
        else:
            print("❌ AGI MCP Server failed to start")

    finally:
        # Clean up
        client.stop_server()

async def main():
    """Main function"""
    try:
        await demo_simple_startup_test()
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
