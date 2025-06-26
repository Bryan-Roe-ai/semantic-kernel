#!/usr/bin/env python3
"""
import asyncio
Test module for conversation summary plugin unit

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from unittest.mock import AsyncMock, Mock

import pytest

from semantic_kernel.connectors.ai.chat_completion_client_base import (
    ChatCompletionClientBase,
)
from semantic_kernel.connectors.ai.prompt_execution_settings import (
    PromptExecutionSettings,
)
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.core_plugins.conversation_summary_plugin import (
    ConversationSummaryPlugin,
)
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.kernel import Kernel
from semantic_kernel.prompt_template.prompt_template_config import PromptTemplateConfig


def test_conversation_summary_plugin():
    config = PromptTemplateConfig(name="test", description="test")
    plugin = ConversationSummaryPlugin(config)
    assert plugin._summarizeConversationFunction is not None
    assert plugin.return_key == "summary"


def test_conversation_summary_plugin_with_deprecated_value(kernel):
    config = PromptTemplateConfig(name="test", description="test")
    plugin = ConversationSummaryPlugin(config, kernel=kernel)
    assert plugin._summarizeConversationFunction is not None
    assert plugin.return_key == "summary"


async def test_summarize_conversation(kernel: Kernel):
    service = AsyncMock(spec=ChatCompletionClientBase)
    service.service_id = "default"
    service.get_chat_message_contents = AsyncMock(
        return_value=[ChatMessageContent(role="assistant", content="Hello World!")]
    )
    service.get_prompt_execution_settings_class = Mock(
        return_value=PromptExecutionSettings
    )
    kernel.add_service(service)
    config = PromptTemplateConfig(
        name="test",
        description="test",
        execution_settings={"default": PromptExecutionSettings()},
    )
    kernel.add_plugin(ConversationSummaryPlugin(config), "summarizer")
    args = KernelArguments(input="Hello World!")

    await kernel.invoke(
        plugin_name="summarizer", function_name="SummarizeConversation", arguments=args
    )
    args["summary"] == "Hello world"
    service.get_chat_message_contents.assert_called_once()
