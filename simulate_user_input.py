#!/usr/bin/env python3
"""Simulate user input for agent robustness testing."""

from datetime import datetime

class SimulatedAgent:
    """Minimal agent that echoes basic commands."""

    def __init__(self, name: str = "TestAgent"):
        self.name = name
        self.start_time = datetime.now()
        self.task_count = 0

    def process_input(self, message: str) -> str:
        """Handle a single user message."""
        self.task_count += 1
        lower = message.lower()
        if "hello" in lower:
            return f"👋 Hello! I'm {self.name}."
        if "status" in lower:
            uptime = datetime.now() - self.start_time
            return f"📊 Running for {uptime}, processed {self.task_count} tasks"
        if "task" in lower:
            return f"✅ Task completed: {message}"
        if "help" in lower:
            return "🆘 Commands: hello, status, task <desc>, help"
        return f"🔄 Processing: {message} - Task #{self.task_count} completed"


def simulate_user_input(messages):
    """Send a list of messages to the agent and print responses."""
    agent = SimulatedAgent()
    for msg in messages:
        response = agent.process_input(msg)
        print(f"User: {msg}")
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    demo_messages = [
        "Hello agent!",
        "status",
        "task analyze dataset",
        "help",
        "<script>alert('test')</script>",
        "😃 emoji test"
    ]
    simulate_user_input(demo_messages)
