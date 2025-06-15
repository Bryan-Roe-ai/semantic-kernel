#!/usr/bin/env python3
"""
AGI MCP Client

Client for interacting with the AGI Model Context Protocol server.
Provides a Python interface for accessing AGI capabilities.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
import subprocess

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AGIMCPClient:
    """Client for interacting with AGI MCP Server"""

    def __init__(self):
        self.session = None

    async def initialize(self):
        """Initialize the AGI MCP client"""
        try:
            # Get the server script path
            server_path = Path(__file__).parent / "mcp-agi-server.py"

            # Create server parameters
            server_params = StdioServerParameters(
                command="python",
                args=[str(server_path)]
            )

            # Connect to the server
            async with stdio_client(server_params) as (read, write):
                self.session = ClientSession(read, write)

                # Initialize the session
                await self.session.initialize()

                logger.info("✅ AGI MCP Client initialized successfully")
                return self.session

        except Exception as e:
            logger.error(f"❌ Failed to initialize AGI MCP client: {e}")
            raise

    async def _call_tool(self, tool_name: str, **kwargs) -> str:
        """Generic method to call AGI tools"""
        if not self.session:
            await self.initialize()

        try:
            # Get available tools
            tools_result = await self.session.list_tools()
            available_tools = [tool.name for tool in tools_result.tools]

            if tool_name not in available_tools:
                return f"Error: Tool '{tool_name}' not available. Available tools: {available_tools}"

            # Call the tool
            result = await self.session.call_tool(tool_name, kwargs)

            if result.content:
                return result.content[0].text if result.content else "No content returned"
            else:
                return f"Tool executed successfully"

        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return f"Error: {str(e)}"

    async def advanced_reasoning(
        self,
        problem: str,
        reasoning_type: str = "logical",
        depth: int = 3
    ) -> str:
        """Use advanced reasoning capabilities"""
        try:
            result = await self.kernel.invoke(
                "agi_server",
                "reasoning_engine",
                problem=problem,
                reasoning_type=reasoning_type,
                depth=depth
            )
            return str(result)
        except Exception as e:
            logger.error(f"Error in advanced reasoning: {e}")
            return f"Error: {str(e)}"

    async def process_multimodal(
        self,
        content_type: str,
        content_description: str,
        analysis_type: str = "comprehensive"
    ) -> str:
        """Process multimodal content"""
        try:
            result = await self.kernel.invoke(
                "agi_server",
                "multimodal_processor",
                content_type=content_type,
                content_description=content_description,
                analysis_type=analysis_type
            )
            return str(result)
        except Exception as e:
            logger.error(f"Error in multimodal processing: {e}")
            return f"Error: {str(e)}"

    async def execute_autonomous_task(
        self,
        task_description: str,
        priority: str = "normal",
        constraints: Optional[str] = None
    ) -> str:
        """Execute autonomous tasks"""
        try:
            result = await self.kernel.invoke(
                "agi_server",
                "autonomous_task_executor",
                task_description=task_description,
                priority=priority,
                constraints=constraints or ""
            )
            return str(result)
        except Exception as e:
            logger.error(f"Error in autonomous task execution: {e}")
            return f"Error: {str(e)}"

    async def synthesize_knowledge(
        self,
        sources: str,
        topic: str,
        synthesis_type: str = "comprehensive"
    ) -> str:
        """Synthesize knowledge from multiple sources"""
        try:
            result = await self.kernel.invoke(
                "agi_server",
                "knowledge_synthesizer",
                sources=sources,
                topic=topic,
                synthesis_type=synthesis_type
            )
            return str(result)
        except Exception as e:
            logger.error(f"Error in knowledge synthesis: {e}")
            return f"Error: {str(e)}"

    async def generate_creative_content(
        self,
        prompt: str,
        creativity_level: str = "balanced",
        output_format: str = "structured"
    ) -> str:
        """Generate creative content"""
        try:
            result = await self.kernel.invoke(
                "agi_server",
                "creative_generator",
                prompt=prompt,
                creativity_level=creativity_level,
                output_format=output_format
            )
            return str(result)
        except Exception as e:
            logger.error(f"Error in creative generation: {e}")
            return f"Error: {str(e)}"

    async def evaluate_ethics(
        self,
        scenario: str,
        ethical_framework: str = "comprehensive",
        stakeholders: Optional[str] = None
    ) -> str:
        """Evaluate ethical scenarios"""
        try:
            result = await self.kernel.invoke(
                "agi_server",
                "ethical_evaluator",
                scenario=scenario,
                ethical_framework=ethical_framework,
                stakeholders=stakeholders or ""
            )
            return str(result)
        except Exception as e:
            logger.error(f"Error in ethical evaluation: {e}")
            return f"Error: {str(e)}"

    async def analyze_metacognition(
        self,
        thinking_process: str,
        analysis_depth: str = "standard"
    ) -> str:
        """Analyze thinking processes"""
        try:
            result = await self.kernel.invoke(
                "agi_server",
                "meta_cognitive_analyzer",
                thinking_process=thinking_process,
                analysis_depth=analysis_depth
            )
            return str(result)
        except Exception as e:
            logger.error(f"Error in meta-cognitive analysis: {e}")
            return f"Error: {str(e)}"

    async def get_system_status(self) -> Dict[str, Any]:
        """Get AGI system status"""
        try:
            result = await self.kernel.invoke(
                "agi_server",
                "system_status"
            )
            return json.loads(str(result))
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {"error": str(e)}

async def demo_agi_capabilities():
    """Demonstrate AGI capabilities"""
    print("🤖 AGI MCP Client Demo")
    print("=" * 50)

    # Initialize client
    client = AGIMCPClient()
    await client.initialize()

    # Demo 1: Advanced Reasoning
    print("\n🧠 Demo 1: Advanced Reasoning")
    reasoning_result = await client.advanced_reasoning(
        problem="How can we achieve sustainable AI development that benefits humanity?",
        reasoning_type="ethical",
        depth=4
    )
    print(f"Reasoning Result:\n{reasoning_result[:500]}...")

    # Demo 2: Multimodal Processing
    print("\n🎭 Demo 2: Multimodal Processing")
    multimodal_result = await client.process_multimodal(
        content_type="mixed",
        content_description="A scientific paper with diagrams about neural networks and accompanying audio explanation",
        analysis_type="comprehensive"
    )
    print(f"Multimodal Analysis:\n{multimodal_result[:500]}...")

    # Demo 3: Autonomous Task Execution
    print("\n🤖 Demo 3: Autonomous Task Execution")
    task_result = await client.execute_autonomous_task(
        task_description="Develop a plan to improve AI workspace productivity",
        priority="high"
    )
    print(f"Task Execution:\n{task_result[:500]}...")

    # Demo 4: Knowledge Synthesis
    print("\n📚 Demo 4: Knowledge Synthesis")
    synthesis_result = await client.synthesize_knowledge(
        sources="Research papers, industry reports, expert interviews",
        topic="Future of Artificial General Intelligence",
        synthesis_type="comprehensive"
    )
    print(f"Knowledge Synthesis:\n{synthesis_result[:500]}...")

    # Demo 5: Creative Generation
    print("\n🎨 Demo 5: Creative Generation")
    creative_result = await client.generate_creative_content(
        prompt="Design an innovative AI-human collaboration framework",
        creativity_level="innovative",
        output_format="structured"
    )
    print(f"Creative Output:\n{creative_result[:500]}...")

    # Demo 6: Ethical Evaluation
    print("\n⚖️ Demo 6: Ethical Evaluation")
    ethics_result = await client.evaluate_ethics(
        scenario="Deploying AGI systems in critical infrastructure",
        ethical_framework="comprehensive"
    )
    print(f"Ethical Analysis:\n{ethics_result[:500]}...")

    # Demo 7: Meta-cognitive Analysis
    print("\n🤔 Demo 7: Meta-cognitive Analysis")
    meta_result = await client.analyze_metacognition(
        thinking_process="The process of solving complex multi-step problems",
        analysis_depth="deep"
    )
    print(f"Meta-cognitive Analysis:\n{meta_result[:500]}...")

    # Demo 8: System Status
    print("\n📊 Demo 8: System Status")
    status = await client.get_system_status()
    print(f"System Status:\n{json.dumps(status, indent=2)}")

async def main():
    """Main function"""
    try:
        await demo_agi_capabilities()
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
