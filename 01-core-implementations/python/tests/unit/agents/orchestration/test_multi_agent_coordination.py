#!/usr/bin/env python3
"""
Test scenarios for multi-agent coordination running multiple orchestrations concurrently.
"""

import asyncio

from semantic_kernel.agents.orchestration.sequential import SequentialOrchestration
from semantic_kernel.agents.runtime.in_process.in_process_runtime import InProcessRuntime
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from tests.unit.agents.orchestration.conftest import MockAgent


async def test_multiple_orchestrations_run_concurrently():
    """Ensure orchestrations run concurrently without interfering with each other."""
    agent_a1 = MockAgent()
    agent_a2 = MockAgent()
    orchestration_a = SequentialOrchestration(members=[agent_a1, agent_a2])

    agent_b1 = MockAgent()
    agent_b2 = MockAgent()
    orchestration_b = SequentialOrchestration(members=[agent_b1, agent_b2])

    runtime = InProcessRuntime()
    runtime.start()

    try:
        result_a_future, result_b_future = await asyncio.gather(
            orchestration_a.invoke(task="message_a", runtime=runtime),
            orchestration_b.invoke(task="message_b", runtime=runtime),
        )

        result_a = await result_a_future.get(1.0)
        result_b = await result_b_future.get(1.0)
    finally:
        await runtime.stop_when_idle()

    assert isinstance(result_a, ChatMessageContent)
    assert isinstance(result_b, ChatMessageContent)
    assert result_a.content == "mock_response"
    assert result_b.content == "mock_response"
