#!/usr/bin/env python3
"""
Demonstration of local AI agents and capabilities

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
import time
import json
from datetime import datetime
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalAGIAgent:
    """Simple local AGI agent for demonstration"""

    def __init__(self, name: str = "LocalAGI"):
        self.name = name
        self.start_time = datetime.now()
        self.task_count = 0

    @kernel_function(description="Process a user request locally")
    def process_request(self, request: str) -> str:
        """Process a user request and return a response"""
        self.task_count += 1
        logger.info(f"🤖 {self.name} processing: {request}")

        # Simple request processing logic
        if "hello" in request.lower():
            return f"👋 Hello! I'm {self.name}, your local AGI agent. How can I assist you today?"
        elif "status" in request.lower():
            uptime = datetime.now() - self.start_time
            return f"📊 Agent Status: Running for {uptime}, processed {self.task_count} tasks"
        elif "task" in request.lower():
            return f"✅ Task completed: {request}"
        elif "help" in request.lower():
            return "🆘 Available commands: hello, status, task [description], help, info"
        elif "info" in request.lower():
            return f"ℹ️ {self.name} - Local AGI Agent running on Semantic Kernel"
        else:
            return f"🔄 Processing: {request} - Task #{self.task_count} completed"

    @kernel_function(description="Get agent information")
    def get_info(self) -> str:
        """Get detailed agent information"""
        uptime = datetime.now() - self.start_time
        info = {
            "name": self.name,
            "type": "Local AGI Agent",
            "start_time": self.start_time.isoformat(),
            "uptime": str(uptime),
            "tasks_processed": self.task_count,
            "status": "running"
        }
        return json.dumps(info, indent=2)

    @kernel_function(description="Simulate file operations")
    def file_operation(self, operation: str, filename: str) -> str:
        """Simulate file operations"""
        self.task_count += 1
        operations = {
            "create": f"📝 Created file: {filename}",
            "read": f"📖 Reading file: {filename}",
            "update": f"✏️ Updated file: {filename}",
            "delete": f"🗑️ Deleted file: {filename}"
        }
        return operations.get(operation.lower(), f"❓ Unknown operation: {operation}")

    @kernel_function(description="Monitor system performance")
    def monitor_performance(self) -> str:
        """Return system performance metrics"""
        import psutil
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            return f"💻 Performance: CPU: {cpu_percent}%, Memory: {memory.percent}% used"
        except ImportError:
            return "💻 Performance monitoring not available (psutil not installed)"

class AGIWorkflowOrchestrator:
    """Orchestrates multiple AGI agents"""

    def __init__(self):
        self.kernel = Kernel()
        self.agents = {}

    def add_agent(self, agent_id: str, agent: LocalAGIAgent):
        """Add an agent to the orchestrator"""
        self.agents[agent_id] = agent
        self.kernel.add_plugin(agent, plugin_name=agent_id)
        logger.info(f"✅ Added agent: {agent_id}")

    async def process_workflow(self, workflow: list) -> dict:
        """Process a workflow of tasks across multiple agents"""
        results = {}

        for step in workflow:
            agent_id = step.get("agent")
            function_name = step.get("function")
            params = step.get("params", {})

            try:
                function = self.kernel.get_function(agent_id, function_name)
                result = await function.invoke(self.kernel, **params)
                results[f"{agent_id}_{function_name}"] = str(result)
                logger.info(f"✅ Completed: {agent_id}.{function_name}")
            except Exception as e:
                logger.error(f"❌ Failed: {agent_id}.{function_name} - {e}")
                results[f"{agent_id}_{function_name}"] = f"Error: {e}"

        return results

async def demo_local_agents():
    """Demonstrate local AGI agents"""
    print("🚀 Starting Local AGI Agent Demo")
    print("=" * 50)

    # Create orchestrator
    orchestrator = AGIWorkflowOrchestrator()

    # Create and add agents
    file_agent = LocalAGIAgent("FileAgent")
    chat_agent = LocalAGIAgent("ChatAgent")
    monitor_agent = LocalAGIAgent("MonitorAgent")

    orchestrator.add_agent("file_agent", file_agent)
    orchestrator.add_agent("chat_agent", chat_agent)
    orchestrator.add_agent("monitor_agent", monitor_agent)

    # Interactive demo
    while True:
        print("\n" + "="*50)
        print("🤖 Local AGI Agent System")
        print("="*50)
        print("1. Chat with agent")
        print("2. File operations")
        print("3. System monitoring")
        print("4. Agent information")
        print("5. Run workflow")
        print("6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        if choice == "1":
            message = input("Enter message: ")
            function = orchestrator.kernel.get_function("chat_agent", "process_request")
            result = await function.invoke(orchestrator.kernel, request=message)
            print(f"🤖 Response: {result}")

        elif choice == "2":
            operation = input("Enter operation (create/read/update/delete): ")
            filename = input("Enter filename: ")
            function = orchestrator.kernel.get_function("file_agent", "file_operation")
            result = await function.invoke(orchestrator.kernel, operation=operation, filename=filename)
            print(f"📁 Result: {result}")

        elif choice == "3":
            function = orchestrator.kernel.get_function("monitor_agent", "monitor_performance")
            result = await function.invoke(orchestrator.kernel)
            print(f"📊 Monitoring: {result}")

        elif choice == "4":
            agent_id = input("Enter agent ID (file_agent/chat_agent/monitor_agent): ")
            if agent_id in orchestrator.agents:
                function = orchestrator.kernel.get_function(agent_id, "get_info")
                result = await function.invoke(orchestrator.kernel)
                print(f"ℹ️ Agent Info:\n{result}")
            else:
                print("❌ Agent not found")

        elif choice == "5":
            # Demo workflow
            workflow = [
                {"agent": "monitor_agent", "function": "monitor_performance"},
                {"agent": "file_agent", "function": "file_operation", "params": {"operation": "create", "filename": "test.txt"}},
                {"agent": "chat_agent", "function": "process_request", "params": {"request": "status"}},
                {"agent": "file_agent", "function": "file_operation", "params": {"operation": "read", "filename": "test.txt"}}
            ]

            print("🔄 Running workflow...")
            results = await orchestrator.process_workflow(workflow)
            for step, result in results.items():
                print(f"  ✅ {step}: {result}")

        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option")

async def main():
    """Main function"""
    try:
        await demo_local_agents()
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
