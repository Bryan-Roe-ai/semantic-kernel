#!/usr/bin/env python3
"""
Test MCP Integration
Tests the Model Context Protocol server and tool coordination.
"""

import asyncio
import json
import aiohttp
import websockets
from pathlib import Path

class MCPTester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.ws_url = base_url.replace("http://", "ws://").replace("https://", "wss://")

    async def test_server_health(self):
        """Test if MCP server is running"""
        print("🔍 Testing MCP server health...")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/") as response:
                    data = await response.json()
                    print(f"✅ Server is running: {data['message']}")
                    print(f"📋 Available tools: {', '.join(data['tools'])}")
                    return True
        except Exception as e:
            print(f"❌ Server health check failed: {e}")
            return False

    async def test_list_tools(self):
        """Test listing available tools"""
        print("\n🛠️  Testing tool listing...")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/tools") as response:
                    data = await response.json()
                    tools = data["tools"]

                    print(f"✅ Found {len(tools)} tools:")
                    for tool in tools:
                        print(f"  📌 {tool['name']}: {tool['description']}")

                    return tools
        except Exception as e:
            print(f"❌ Tool listing failed: {e}")
            return []

    async def test_file_operations(self):
        """Test file read/write operations"""
        print("\n📁 Testing file operations...")

        test_file = Path("test_mcp_file.txt")
        test_content = "Hello from MCP testing!"

        try:
            # Test write
            async with aiohttp.ClientSession() as session:
                write_request = {
                    "tool_name": "write_file",
                    "parameters": {
                        "file_path": str(test_file),
                        "content": test_content
                    }
                }

                async with session.post(f"{self.base_url}/execute", json=write_request) as response:
                    result = await response.json()

                    if result["success"]:
                        print("✅ File write successful")
                    else:
                        print(f"❌ File write failed: {result['error']}")
                        return False

                # Test read
                read_request = {
                    "tool_name": "read_file",
                    "parameters": {
                        "file_path": str(test_file)
                    }
                }

                async with session.post(f"{self.base_url}/execute", json=read_request) as response:
                    result = await response.json()

                    if result["success"] and result["result"]["content"] == test_content:
                        print("✅ File read successful")
                    else:
                        print(f"❌ File read failed: {result.get('error', 'Content mismatch')}")
                        return False

            # Cleanup
            if test_file.exists():
                test_file.unlink()

            return True

        except Exception as e:
            print(f"❌ File operations test failed: {e}")
            return False

    async def test_code_analysis(self):
        """Test code analysis functionality"""
        print("\n🔍 Testing code analysis...")

        # Create a test Python file
        test_code = '''
def hello_world(name="World"):
    """A simple greeting function"""
    return f"Hello, {name}!"

class Greeter:
    def __init__(self, default_name="Friend"):
        self.default_name = default_name

    def greet(self, name=None):
        return hello_world(name or self.default_name)

if __name__ == "__main__":
    greeter = Greeter()
    print(greeter.greet("MCP"))
'''

        test_file = Path("test_analysis.py")

        try:
            # Write test file
            with open(test_file, 'w') as f:
                f.write(test_code)

            async with aiohttp.ClientSession() as session:
                analysis_request = {
                    "tool_name": "analyze_code",
                    "parameters": {
                        "file_path": str(test_file),
                        "language": "python"
                    }
                }

                async with session.post(f"{self.base_url}/execute", json=analysis_request) as response:
                    result = await response.json()

                    if result["success"]:
                        analysis = result["result"]
                        metrics = analysis["metrics"]

                        print("✅ Code analysis successful:")
                        print(f"  📊 Total lines: {metrics['lines_total']}")
                        print(f"  📊 Code lines: {metrics['lines_code']}")
                        print(f"  📊 Functions: {len(analysis['functions'])}")
                        print(f"  📊 Classes: {len(analysis['classes'])}")

                        for func in analysis["functions"]:
                            print(f"    🔧 Function: {func['name']} (line {func['line']})")

                        for cls in analysis["classes"]:
                            print(f"    🏗️  Class: {cls['name']} (line {cls['line']})")
                    else:
                        print(f"❌ Code analysis failed: {result['error']}")
                        return False

            # Cleanup
            if test_file.exists():
                test_file.unlink()

            return True

        except Exception as e:
            print(f"❌ Code analysis test failed: {e}")
            return False

    async def test_websocket_connection(self):
        """Test WebSocket connection and real-time communication"""
        print("\n🌐 Testing WebSocket connection...")

        try:
            uri = f"{self.ws_url}/ws/test_session"

            async with websockets.connect(uri) as websocket:
                print("✅ WebSocket connected")

                # Test context update
                context_message = {
                    "type": "context_update",
                    "data": {
                        "user": "test_user",
                        "session_info": "MCP testing session",
                        "timestamp": "2025-08-09"
                    }
                }

                await websocket.send(json.dumps(context_message))
                response = await websocket.recv()
                response_data = json.loads(response)

                if response_data["type"] == "context_ack":
                    print("✅ Context update successful")
                else:
                    print("❌ Context update failed")
                    return False

                # Test tool execution via WebSocket
                tool_message = {
                    "type": "tool_request",
                    "data": {
                        "tool_name": "get_context",
                        "parameters": {
                            "session_id": "test_session"
                        }
                    }
                }

                await websocket.send(json.dumps(tool_message))
                response = await websocket.recv()
                response_data = json.loads(response)

                if response_data["type"] == "tool_response" and response_data["data"]["success"]:
                    context_data = response_data["data"]["result"]["context"]
                    print("✅ Tool execution via WebSocket successful")
                    print(f"  📋 Retrieved context: {context_data}")
                else:
                    print("❌ Tool execution via WebSocket failed")
                    return False

            return True

        except Exception as e:
            print(f"❌ WebSocket test failed: {e}")
            return False

    async def test_ai_model_query(self):
        """Test AI model querying functionality"""
        print("\n🤖 Testing AI model query...")

        try:
            async with aiohttp.ClientSession() as session:
                query_request = {
                    "tool_name": "query_ai_model",
                    "parameters": {
                        "prompt": "What is the purpose of Model Context Protocol?",
                        "model": "test_model",
                        "parameters": {
                            "max_tokens": 100,
                            "temperature": 0.7
                        }
                    }
                }

                async with session.post(f"{self.base_url}/execute", json=query_request) as response:
                    result = await response.json()

                    if result["success"]:
                        print("✅ AI model query successful")
                        print(f"  🤖 Response: {result['result']['response']}")
                    else:
                        print(f"❌ AI model query failed: {result['error']}")
                        return False

            return True

        except Exception as e:
            print(f"❌ AI model query test failed: {e}")
            return False

    async def run_all_tests(self):
        """Run all MCP tests"""
        print("🚀 Starting MCP Integration Tests")
        print("=" * 50)

        test_results = []

        # Server health check
        test_results.append(await self.test_server_health())

        if not test_results[-1]:
            print("\n❌ Server is not running. Please start the MCP server first:")
            print("   python3 mcp_server.py")
            return False

        # Run all tests
        test_results.append(await self.test_list_tools())
        test_results.append(await self.test_file_operations())
        test_results.append(await self.test_code_analysis())
        test_results.append(await self.test_ai_model_query())
        test_results.append(await self.test_websocket_connection())

        # Summary
        passed = sum(1 for result in test_results if result)
        total = len(test_results)

        print(f"\n📊 Test Summary: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All tests passed! MCP integration is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the output above for details.")

        return passed == total

async def main():
    """Main test function"""
    tester = MCPTester()
    success = await tester.run_all_tests()

    if success:
        print("\n✅ MCP integration is ready for use!")
        print("\nNext steps:")
        print("1. Integrate MCP with Semantic Kernel agents")
        print("2. Create custom tools for your specific use cases")
        print("3. Use WebSocket connections for real-time AI coordination")
    else:
        print("\n❌ MCP integration tests failed.")
        print("\nTroubleshooting:")
        print("1. Ensure MCP server is running: python3 mcp_server.py")
        print("2. Check firewall and port settings")
        print("3. Verify dependencies are installed")

if __name__ == "__main__":
    asyncio.run(main())
