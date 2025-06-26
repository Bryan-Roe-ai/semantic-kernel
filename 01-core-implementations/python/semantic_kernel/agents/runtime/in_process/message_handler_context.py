#!/usr/bin/env python3
"""
import re
Message Handler Context module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, ClassVar

from semantic_kernel.agents.runtime.core.agent_id import AgentId
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class MessageHandlerContext:
    """Context for message handlers."""

    def __init__(self) -> None:
        """Instantiate the MessageHandlerContext class."""
        raise RuntimeError(
            "MessageHandlerContext cannot be instantiated. It is a static class that provides context management for "
            "message handling."
        )

    _MESSAGE_HANDLER_CONTEXT: ClassVar[ContextVar[AgentId]] = ContextVar("_MESSAGE_HANDLER_CONTEXT")

    @classmethod
    @contextmanager
    def populate_context(cls, ctx: AgentId) -> Generator[None, Any, None]:
        """Populate the context with the current agent ID."""
        token = MessageHandlerContext._MESSAGE_HANDLER_CONTEXT.set(ctx)
        try:
            yield
        finally:
            MessageHandlerContext._MESSAGE_HANDLER_CONTEXT.reset(token)

    @classmethod
    def agent_id(cls) -> AgentId:
        """Get the current agent ID."""
        try:
            return cls._MESSAGE_HANDLER_CONTEXT.get()
        except LookupError as e:
            raise RuntimeError("MessageHandlerContext.agent_id() must be called within a message handler.") from e
