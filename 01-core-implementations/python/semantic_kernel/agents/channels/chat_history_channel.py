#!/usr/bin/env python3
"""Simplified chat history channel."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterable
from semantic_kernel.utils.feature_stage_decorator import experimental_class
from semantic_kernel.contents.streaming_chat_message_content import StreamingChatMessageContent
from semantic_kernel.contents.chat_history import ChatHistory


@experimental_class
class ChatHistoryChannel(ABC):
    """Base class for streaming chat history."""

    @abstractmethod
    async def invoke_stream(self, history: ChatHistory) -> AsyncIterable[StreamingChatMessageContent]:
        """Invoke the chat history agent protocol in streaming mode."""
        raise NotImplementedError
