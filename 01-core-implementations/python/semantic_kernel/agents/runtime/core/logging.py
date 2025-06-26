#!/usr/bin/env python3
"""
import re
Logging module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import json
from enum import Enum
from typing import Any

from semantic_kernel.agents.runtime.core.agent_id import AgentId
from semantic_kernel.agents.runtime.core.topic import TopicId
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class MessageKind(Enum):
    """Message kind enum."""

    DIRECT = 1
    PUBLISH = 2
    RESPOND = 3


@experimental
class DeliveryStage(Enum):
    """Delivery stage enum."""

    SEND = 1
    DELIVER = 2


@experimental
class MessageEvent:
    """Base class for message events."""

    def __init__(
        self,
        *,
        payload: str,
        sender: AgentId | None,
        receiver: AgentId | TopicId | None,
        kind: MessageKind,
        delivery_stage: DeliveryStage,
        **kwargs: Any,
    ) -> None:
        """Initialize a message event."""
        self.kwargs = kwargs
        self.kwargs["payload"] = payload
        self.kwargs["sender"] = None if sender is None else str(sender)
        self.kwargs["receiver"] = None if receiver is None else str(receiver)
        self.kwargs["kind"] = str(kind)
        self.kwargs["delivery_stage"] = str(delivery_stage)
        self.kwargs["type"] = "Message"

    # This must output the event in a json serializable format
    def __str__(self) -> str:
        """Convert the event to a string."""
        return json.dumps(self.kwargs)


@experimental
class MessageDroppedEvent:
    """Event for dropped messages."""

    def __init__(
        self,
        *,
        payload: str,
        sender: AgentId | None,
        receiver: AgentId | TopicId | None,
        kind: MessageKind,
        **kwargs: Any,
    ) -> None:
        """Initialize a message dropped event."""
        self.kwargs = kwargs
        self.kwargs["payload"] = payload
        self.kwargs["sender"] = None if sender is None else str(sender)
        self.kwargs["receiver"] = None if receiver is None else str(receiver)
        self.kwargs["kind"] = str(kind)
        self.kwargs["type"] = "MessageDropped"

    # This must output the event in a json serializable format
    def __str__(self) -> str:
        """Convert the event to a string."""
        return json.dumps(self.kwargs)


@experimental
class MessageHandlerExceptionEvent:
    """Event for exceptions in message handlers."""

    def __init__(
        self,
        *,
        payload: str,
        handling_agent: AgentId,
        exception: BaseException,
        **kwargs: Any,
    ) -> None:
        """Initialize a message handler exception event."""
        self.kwargs = kwargs
        self.kwargs["payload"] = payload
        self.kwargs["handling_agent"] = str(handling_agent)
        self.kwargs["exception"] = str(exception)
        self.kwargs["type"] = "MessageHandlerException"

    # This must output the event in a json serializable format
    def __str__(self) -> str:
        """Convert the event to a string."""
        return json.dumps(self.kwargs)


@experimental
class AgentConstructionExceptionEvent:
    """Event for exceptions during agent construction."""

    def __init__(
        self,
        *,
        agent_id: AgentId,
        exception: BaseException,
        **kwargs: Any,
    ) -> None:
        """Initialize an agent construction exception event."""
        self.kwargs = kwargs
        self.kwargs["agent_id"] = str(agent_id)
        self.kwargs["exception"] = str(exception)
        self.kwargs["type"] = "AgentConstructionException"

    # This must output the event in a json serializable format
    def __str__(self) -> str:
        """Convert the event to a string."""
        return json.dumps(self.kwargs)
