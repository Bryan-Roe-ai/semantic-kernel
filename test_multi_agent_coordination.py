#!/usr/bin/env python3
"""
Test scenarios for multi-agent coordination.

This module defines simple asynchronous tests that demonstrate how agents can
coordinate through a central orchestrator. The goal is to verify basic message
passing and coordination patterns between agents.
"""

import asyncio
import logging
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DummyAgent:
    """A minimal agent that can send and receive messages."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.received: List[str] = []

    async def send(self, message: str, recipient: "DummyAgent") -> None:
        logger.info("%s sending to %s: %s", self.name, recipient.name, message)
        await recipient.receive(f"{self.name}: {message}")

    async def receive(self, message: str) -> None:
        logger.info("%s received: %s", self.name, message)
        self.received.append(message)


class MultiAgentCoordinator:
    """Coordinates interactions between a group of agents."""

    def __init__(self, *agents: DummyAgent) -> None:
        self.agents = list(agents)

    async def ping_pong(self) -> bool:
        """Simple ping-pong between two agents."""
        if len(self.agents) < 2:
            raise ValueError("Ping-pong requires at least two agents")
        a, b = self.agents[0], self.agents[1]
        await a.send("ping", b)
        await b.send("pong", a)
        return a.received[-1] == f"{b.name}: pong" and b.received[-1] == f"{a.name}: ping"

    async def broadcast(self, message: str, sender: DummyAgent) -> bool:
        """Broadcast a message from one agent to all others."""
        tasks = [sender.send(message, agent) for agent in self.agents if agent is not sender]
        await asyncio.gather(*tasks)
        return all(agent.received and agent.received[-1] == f"{sender.name}: {message}"
                   for agent in self.agents if agent is not sender)

    async def chain(self, messages: List[str]) -> List[str]:
        """Pass messages through the agents in a round-robin fashion."""
        if not messages or len(messages) != len(self.agents):
            raise ValueError("Messages list must match number of agents")

        count = len(self.agents)
        for i in range(count):
            sender = self.agents[i]
            recipient = self.agents[(i + 1) % count]
            await sender.send(messages[i], recipient)

        return [agent.received[-1] for agent in self.agents]


async def main() -> None:
    agent_a = DummyAgent("A")
    agent_b = DummyAgent("B")
    agent_c = DummyAgent("C")

    coordinator = MultiAgentCoordinator(agent_a, agent_b, agent_c)

    logger.info("Running ping-pong scenario...")
    ping_pong_ok = await coordinator.ping_pong()
    assert ping_pong_ok, "Ping-pong scenario failed"

    logger.info("Running broadcast scenario...")
    broadcast_ok = await coordinator.broadcast("hello", sender=agent_a)
    assert broadcast_ok, "Broadcast scenario failed"

    logger.info("Running chain scenario...")
    chain_results = await coordinator.chain(["step1", "step2", "final"])
    expected = ["C: final", "A: step1", "B: step2"]
    assert chain_results == expected, f"Chain scenario failed: {chain_results}"

    print("\n✅ Multi-agent coordination scenarios passed")


if __name__ == "__main__":
    asyncio.run(main())
