#!/usr/bin/env python3
"""
Client Example module

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
import aiohttp
import time
from typing import Dict, Any, List
import uuid

class AGIMCPClient:
    """Client for interacting with AGI MCP Server"""
    
    def __init__(self, host: str = "localhost", port: int = 8080):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a request to the AGI MCP Server"""
        if params is None:
            params = {}
        
        request_data = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": method,
            "params": params
        }
        
        # For this example, we'll simulate the server response
        # In a real implementation, this would make an HTTP request
        print(f"Sending request: {method}")
        print(f"Parameters: {json.dumps(params, indent=2)}")
        
        # Simulate server response
        response = await self._simulate_server_response(request_data)
        return response
    
    async def _simulate_server_response(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate server response for demonstration"""
        method = request["method"]
        params = request["params"]
        
        # Simulate different responses based on method
        if method == "capabilities/list":
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "capabilities": [
                        {
                            "name": "autonomous_reasoning",
                            "description": "Multi-step autonomous reasoning and problem solving",
                            "enabled": True,
                            "confidence": 0.9,
                            "usage_count": 156,
                            "success_rate": 0.87
                        },
                        {
                            "name": "adaptive_learning",
                            "description": "Real-time learning and adaptation from interactions",
                            "enabled": True,
                            "confidence": 0.8,
                            "usage_count": 243,
                            "success_rate": 0.91
                        },
                        {
                            "name": "memory_management",
                            "description": "Advanced episodic and semantic memory systems",
                            "enabled": True,
                            "confidence": 0.95,
                            "usage_count": 1024,
                            "success_rate": 0.98
                        },
                        {
                            "name": "goal_planning",
                            "description": "Hierarchical goal decomposition and planning",
                            "enabled": True,
                            "confidence": 0.85,
                            "usage_count": 89,
                            "success_rate": 0.82
                        },
                        {
                            "name": "metacognition",
                            "description": "Self-reflection and meta-cognitive processes",
                            "enabled": True,
                            "confidence": 0.7,
                            "usage_count": 67,
                            "success_rate": 0.79
                        },
                        {
                            "name": "creative_thinking",
                            "description": "Creative problem solving and novel idea generation",
                            "enabled": True,
                            "confidence": 0.6,
                            "usage_count": 34,
                            "success_rate": 0.74
                        },
                        {
                            "name": "ethical_reasoning",
                            "description": "Ethical decision making and moral reasoning",
                            "enabled": True,
                            "confidence": 0.75,
                            "usage_count": 23,
                            "success_rate": 0.85
                        }
                    ],
                    "total_count": 7
                }
            }
        
        elif method == "reasoning/solve":
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "problem": params.get("problem", ""),
                    "solution": {
                        "conclusion": "Multi-step reasoning solution generated",
                        "confidence": 0.85,
                        "combined_steps": [
                            "Applied deductive reasoning:",
                            "Problem: How to optimize machine learning model",
                            "Condition: Current accuracy is 85%",
                            "Applied inductive reasoning:",
                            "Analyzed 15 examples",
                            "Found common elements: ['regularization', 'feature_selection']",
                            "Applied creative reasoning:",
                            "Generated novel approach",
                            "Used approach: Combine unrelated concepts"
                        ],
                        "solution_count": 3
                    },
                    "reasoning_steps": [
                        {
                            "type": "deductive",
                            "result": {"conclusion": "Deductive reasoning applied", "confidence": 0.7},
                            "confidence": 0.7
                        },
                        {
                            "type": "inductive", 
                            "result": {"conclusion": "Pattern identified through inductive reasoning", "confidence": 0.6},
                            "confidence": 0.6
                        },
                        {
                            "type": "creative",
                            "result": {"conclusion": "Creative solution generated", "confidence": 0.5},
                            "confidence": 0.5
                        }
                    ],
                    "confidence": 0.85,
                    "timestamp": time.time(),
                    "used_memories": 8
                }
            }
        
        elif method == "memory/store":
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "success": True,
                    "memory_id": f"user_{uuid.uuid4()}"
                }
            }
        
        elif method == "memory/query":
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "memories": [
                        {
                            "id": "memory_123",
                            "content": "Machine learning models benefit from regularization techniques",
                            "type": "semantic",
                            "timestamp": time.time() - 3600,
                            "importance": 0.8,
                            "tags": ["machine_learning", "regularization"]
                        },
                        {
                            "id": "memory_456", 
                            "content": "Feature selection improves model interpretability",
                            "type": "semantic",
                            "timestamp": time.time() - 7200,
                            "importance": 0.7,
                            "tags": ["feature_selection", "interpretability"]
                        }
                    ],
                    "count": 2
                }
            }
        
        elif method == "goals/create":
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "success": True,
                    "goal_id": str(uuid.uuid4())
                }
            }
        
        elif method == "goals/list":
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "active_goals": [
                        {
                            "id": "goal_123",
                            "description": "Optimize memory system performance",
                            "priority": 5,
                            "status": "active",
                            "progress": 0.3,
                            "created_at": time.time() - 1800,
                            "deadline": time.time() + 86400
                        },
                        {
                            "id": "goal_456",
                            "description": "Learn new problem-solving patterns",
                            "priority": 6,
                            "status": "pending",
                            "progress": 0.1,
                            "created_at": time.time() - 900,
                            "deadline": None
                        }
                    ],
                    "completed_goals": [
                        {
                            "id": "goal_789",
                            "description": "Consolidate knowledge from recent interactions",
                            "progress": 1.0,
                            "completed_at": time.time() - 3600
                        }
                    ],
                    "active_count": 2,
                    "completed_count": 1
                }
            }
        
        elif method == "system/status":
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "server_id": "agi_server_123",
                    "uptime": 86400,
                    "is_running": True,
                    "autonomous_mode": True,
                    "metrics": {
                        "requests_processed": 1247,
                        "successful_operations": 1203,
                        "failed_operations": 44,
                        "average_response_time": 0.234,
                        "memory_usage": 512,
                        "cpu_usage": 23.4,
                        "goals_completed": 15,
                        "learning_events": 89
                    },
                    "capabilities": {
                        "autonomous_reasoning": {"enabled": True, "confidence": 0.9, "usage_count": 156},
                        "adaptive_learning": {"enabled": True, "confidence": 0.8, "usage_count": 243},
                        "memory_management": {"enabled": True, "confidence": 0.95, "usage_count": 1024}
                    },
                    "goals": {
                        "active": 2,
                        "completed": 15
                    }
                }
            }
        
        elif method == "creative/generate":
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "problem": params.get("prompt", ""),
                    "solution": {
                        "conclusion": "Creative solution for AI assistance in education generated",
                        "confidence": 0.65,
                        "combined_steps": [
                            "Applied creative reasoning:",
                            "Generated novel approach",
                            "Used approach: Combine unrelated concepts",
                            "Creative ideas: Gamified learning with AI tutors",
                            "Personalized curriculum adaptation",
                            "Virtual reality immersive experiences"
                        ],
                        "solution_count": 1
                    },
                    "reasoning_steps": [
                        {
                            "type": "creative",
                            "result": {
                                "conclusion": "Creative solution generated",
                                "confidence": 0.65,
                                "approach": "Combine unrelated concepts"
                            },
                            "confidence": 0.65
                        }
                    ],
                    "confidence": 0.65,
                    "timestamp": time.time(),
                    "used_memories": 5
                }
            }
        
        elif method == "ethical/evaluate":
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "scenario": params.get("scenario", ""),
                    "framework": params.get("framework", "utilitarian"),
                    "evaluation": "The scenario requires careful consideration of multiple stakeholders",
                    "confidence": 0.75,
                    "considerations": [
                        "Applied ethical reasoning:",
                        "Analyzed stakeholder impacts",
                        "Considered utilitarian outcomes",
                        "Evaluated potential harm vs benefit",
                        "Recommendation: Proceed with additional safeguards"
                    ],
                    "timestamp": time.time()
                }
            }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    # High-level methods for common operations
    
    async def list_capabilities(self) -> List[Dict[str, Any]]:
        """List all AGI capabilities"""
        response = await self.send_request("capabilities/list")
        return response["result"]["capabilities"]
    
    async def solve_problem(self, problem: str, reasoning_types: List[str] = None) -> Dict[str, Any]:
        """Solve a problem using AGI reasoning"""
        params = {"problem": problem}
        if reasoning_types:
            params["reasoning_types"] = reasoning_types
        
        response = await self.send_request("reasoning/solve", params)
        return response["result"]
    
    async def store_memory(self, content: str, memory_type: str = "episodic", 
                          importance: float = 0.5, tags: List[str] = None) -> str:
        """Store information in AGI memory"""
        params = {
            "content": content,
            "memory_type": memory_type,
            "importance": importance,
            "tags": tags or []
        }
        
        response = await self.send_request("memory/store", params)
        return response["result"]["memory_id"]
    
    async def query_memory(self, query: str, memory_type: str = None, 
                          limit: int = 10) -> List[Dict[str, Any]]:
        """Query AGI memory system"""
        params = {"query": query, "limit": limit}
        if memory_type:
            params["memory_type"] = memory_type
        
        response = await self.send_request("memory/query", params)
        return response["result"]["memories"]
    
    async def create_goal(self, description: str, priority: int = 5, 
                         deadline: float = None) -> str:
        """Create a new goal for autonomous operation"""
        params = {
            "description": description,
            "priority": priority
        }
        if deadline:
            params["deadline"] = deadline
        
        response = await self.send_request("goals/create", params)
        return response["result"]["goal_id"]
    
    async def list_goals(self) -> Dict[str, Any]:
        """List all goals (active and completed)"""
        response = await self.send_request("goals/list")
        return response["result"]
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        response = await self.send_request("system/status")
        return response["result"]
    
    async def generate_creative_ideas(self, prompt: str, creativity_level: float = 0.7) -> Dict[str, Any]:
        """Generate creative ideas using AGI"""
        params = {
            "prompt": prompt,
            "creativity_level": creativity_level
        }
        
        response = await self.send_request("creative/generate", params)
        return response["result"]
    
    async def evaluate_ethics(self, scenario: str, framework: str = "utilitarian") -> Dict[str, Any]:
        """Evaluate ethical implications of a scenario"""
        params = {
            "scenario": scenario,
            "framework": framework
        }
        
        response = await self.send_request("ethical/evaluate", params)
        return response["result"]

async def demonstrate_agi_capabilities():
    """Demonstrate the AGI MCP Server capabilities"""
    
    print("🧠 AGI MCP Server Demonstration")
    print("=" * 50)
    
    async with AGIMCPClient() as client:
        
        print("\n1. 📋 Listing AGI Capabilities")
        print("-" * 30)
        capabilities = await client.list_capabilities()
        for cap in capabilities:
            print(f"• {cap['name']}: {cap['description']}")
            print(f"  Confidence: {cap['confidence']:.2f}, Usage: {cap['usage_count']}, Success Rate: {cap['success_rate']:.2f}")
        
        print(f"\nTotal capabilities: {len(capabilities)}")
        
        print("\n2. 🧮 Advanced Problem Solving")
        print("-" * 30)
        problem = "How can I optimize a machine learning model for better accuracy and efficiency?"
        result = await client.solve_problem(problem, ["deductive", "inductive", "creative"])
        
        print(f"Problem: {problem}")
        print(f"Solution: {result['solution']['conclusion']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Reasoning steps: {len(result['reasoning_steps'])}")
        print(f"Used {result['used_memories']} memories")
        
        print("\n3. 🧠 Memory System Operations")
        print("-" * 30)
        
        # Store some knowledge
        memory_id = await client.store_memory(
            "Deep learning models require careful hyperparameter tuning for optimal performance",
            memory_type="semantic",
            importance=0.8,
            tags=["deep_learning", "optimization", "hyperparameters"]
        )
        print(f"Stored memory with ID: {memory_id}")
        
        # Query memory
        memories = await client.query_memory("machine learning optimization", limit=5)
        print(f"Found {len(memories)} relevant memories:")
        for memory in memories:
            print(f"  • {memory['content'][:80]}...")
            print(f"    Type: {memory['type']}, Importance: {memory['importance']}")
        
        print("\n4. 🎯 Goal Management")
        print("-" * 30)
        
        # Create a goal
        goal_id = await client.create_goal(
            "Research and implement advanced neural architecture search techniques",
            priority=7,
            deadline=time.time() + 7 * 24 * 3600  # 7 days from now
        )
        print(f"Created goal with ID: {goal_id}")
        
        # List goals
        goals = await client.list_goals()
        print(f"Active goals: {goals['active_count']}")
        for goal in goals['active_goals']:
            print(f"  • {goal['description']}")
            print(f"    Priority: {goal['priority']}, Progress: {goal['progress']:.1%}")
        
        print(f"Completed goals: {goals['completed_count']}")
        
        print("\n5. 🎨 Creative Idea Generation")
        print("-" * 30)
        
        creative_result = await client.generate_creative_ideas(
            "How can AI be used to revolutionize education?",
            creativity_level=0.8
        )
        
        print(f"Creative solutions:")
        print(f"• {creative_result['solution']['conclusion']}")
        print(f"Confidence: {creative_result['confidence']:.2f}")
        for step in creative_result['solution']['combined_steps']:
            if step.startswith("Creative ideas:"):
                print(f"• {step}")
        
        print("\n6. ⚖️ Ethical Reasoning")
        print("-" * 30)
        
        ethical_result = await client.evaluate_ethics(
            "Should AI systems be allowed to make medical diagnoses without human oversight?",
            framework="utilitarian"
        )
        
        print(f"Ethical evaluation:")
        print(f"• Scenario: {ethical_result['scenario'][:80]}...")
        print(f"• Framework: {ethical_result['framework']}")
        print(f"• Evaluation: {ethical_result['evaluation']}")
        print(f"• Confidence: {ethical_result['confidence']:.2f}")
        
        print("\n7. 📊 System Status")
        print("-" * 30)
        
        status = await client.get_system_status()
        print(f"Server ID: {status['server_id']}")
        print(f"Uptime: {status['uptime'] / 3600:.1f} hours")
        print(f"Autonomous Mode: {'✓' if status['autonomous_mode'] else '✗'}")
        print(f"Requests Processed: {status['metrics']['requests_processed']}")
        print(f"Success Rate: {(status['metrics']['successful_operations'] / status['metrics']['requests_processed'] * 100):.1f}%")
        print(f"Average Response Time: {status['metrics']['average_response_time']:.3f}s")
        print(f"Memory Usage: {status['metrics']['memory_usage']} MB")
        print(f"CPU Usage: {status['metrics']['cpu_usage']:.1f}%")
        print(f"Active Goals: {status['goals']['active']}")
        print(f"Completed Goals: {status['goals']['completed']}")
        
        print("\n🎉 Demonstration Complete!")
        print("\nThe AGI MCP Server showcases:")
        print("• Multi-type reasoning (deductive, inductive, creative, ethical)")
        print("• Advanced memory systems with semantic search")
        print("• Autonomous goal planning and execution")
        print("• Creative problem solving")
        print("• Ethical decision making")
        print("• Self-monitoring and metacognition")
        print("• Real-time learning and adaptation")

async def interactive_demo():
    """Interactive demonstration allowing user input"""
    
    print("\n🔄 Interactive AGI Demo")
    print("Type 'quit' to exit")
    print("-" * 30)
    
    async with AGIMCPClient() as client:
        while True:
            try:
                user_input = input("\nEnter a problem to solve: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye! 👋")
                    break
                
                if not user_input:
                    continue
                
                print(f"\n🧠 Processing: {user_input}")
                
                # Solve the problem
                result = await client.solve_problem(user_input)
                
                print(f"\n💡 Solution: {result['solution']['conclusion']}")
                print(f"📊 Confidence: {result['confidence']:.2f}")
                print(f"🔍 Used {result['used_memories']} memories")
                
                # Show reasoning steps
                print(f"\n🧩 Reasoning Process:")
                for i, step in enumerate(result['reasoning_steps'], 1):
                    print(f"  {i}. {step['type'].title()} Reasoning (confidence: {step['confidence']:.2f})")
                
                # Store the interaction as memory
                memory_id = await client.store_memory(
                    f"Problem: {user_input}\nSolution: {result['solution']['conclusion']}",
                    memory_type="episodic",
                    importance=result['confidence'],
                    tags=["user_interaction", "problem_solving"]
                )
                print(f"💾 Stored interaction in memory: {memory_id}")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

async def main():
    """Main entry point for the client demo"""
    
    print("🚀 AGI MCP Server Client Demo")
    print("=" * 40)
    
    # Run the capabilities demonstration
    await demonstrate_agi_capabilities()
    
    # Ask if user wants interactive demo
    try:
        choice = input("\nWould you like to try the interactive demo? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            await interactive_demo()
    except KeyboardInterrupt:
        print("\nGoodbye! 👋")

if __name__ == "__main__":
    asyncio.run(main())
