#!/usr/bin/env python3
"""
AI module for open ai chat message

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

from typing import Optional

from semantic_kernel.connectors.ai.open_ai.models.chat_completion.function_call import (
    FunctionCall,
)
from semantic_kernel.connectors.ai.open_ai.models.chat_completion.tool_calls import ToolCall
from semantic_kernel.models.ai.chat_completion.chat_message import ChatMessage


class OpenAIChatMessage(ChatMessage):
    """Class to hold openai chat messages, which might include name, function_call and tool_calls fields."""

    name: Optional[str] = None
    function_call: Optional[FunctionCall] = None
    tool_calls: Optional[ToolCall] = None
    tool_call_id: Optional[str] = None
