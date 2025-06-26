#!/usr/bin/env python3
"""
import asyncio
Message Buffer Interface module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from abc import ABC, abstractmethod

from dapr.actor import ActorInterface, actormethod

from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class MessageBufferInterface(ActorInterface, ABC):
    """Abstract base class for a message event buffer that follows the ActorInterface."""

    @abstractmethod
    @actormethod(name="enqueue")
    async def enqueue(self, message: str) -> None:
        """Enqueues a message event into the buffer.

        Args:
            message: The message event to enqueue.
        """
        ...

    @abstractmethod
    @actormethod(name="dequeue_all")
    async def dequeue_all(self) -> list[str]:
        """Dequeues all process events from the buffer.

        Returns:
            The dequeued message event as a list of string
            representing a ProcessEvent.
        """
        ...
