#!/usr/bin/env python3
"""
Test module for agent decorated

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import pytest

from semantic_kernel.agents.chat_completion.chat_completion_agent import ChatCompletionAgent
from semantic_kernel.agents.open_ai.openai_assistant_agent import OpenAIAssistantAgent

pytestmark = pytest.mark.parametrize(
    "decorated_method, expected_attribute",
    [
        # region ChatCompletionAgent
        pytest.param(
            ChatCompletionAgent.invoke,
            "__agent_diagnostics__",
            id="ChatCompletionAgent.invoke",
        ),
        pytest.param(
            ChatCompletionAgent.invoke_stream,
            "__agent_diagnostics__",
            id="ChatCompletionAgent.invoke_stream",
        ),
        # endregion
        # region OpenAIAssistantAgent
        pytest.param(
            OpenAIAssistantAgent.invoke,
            "__agent_diagnostics__",
            id="OpenAIAssistantBase.invoke",
        ),
        pytest.param(
            OpenAIAssistantAgent.invoke_stream,
            "__agent_diagnostics__",
            id="OpenAIAssistantBase.invoke_stream",
        ),
        # endregion
    ],
)


def test_decorated(decorated_method, expected_attribute):
    """Test that the connectors are being decorated properly with the agent diagnostics decorators."""
    assert hasattr(decorated_method, expected_attribute) and getattr(decorated_method, expected_attribute), (
        f"{decorated_method} should be decorated with the appropriate agent diagnostics decorator."
    )
