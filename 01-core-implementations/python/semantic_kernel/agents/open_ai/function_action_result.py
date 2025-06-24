#!/usr/bin/env python3
"""
Function Action Result module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import logging
from dataclasses import dataclass

from semantic_kernel.contents.streaming_chat_message_content import StreamingChatMessageContent
from semantic_kernel.utils.feature_stage_decorator import experimental

logger: logging.Logger = logging.getLogger(__name__)


@experimental
@dataclass
class FunctionActionResult:
    """Function Action Result."""

    function_call_streaming_content: StreamingChatMessageContent
    function_result_streaming_content: StreamingChatMessageContent
    tool_outputs: list[dict[str, str]]
