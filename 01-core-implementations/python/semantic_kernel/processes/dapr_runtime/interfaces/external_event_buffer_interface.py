#!/usr/bin/env python3
"""
import asyncio
External Event Buffer Interface module

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
class ExternalEventBufferInterface(ActorInterface, ABC):
    """Abstract base class for an external event buffer that follows the ActorInterface."""

    @abstractmethod
    @actormethod(name="enqueue")
    async def enqueue(self, external_event: str) -> None:
        """Enqueues an external event into the buffer.

        Args:
            external_event: The external event to enqueue.
        """
        ...

    @abstractmethod
    @actormethod(name="dequeue_all")
    async def dequeue_all(self) -> list[str]:
        """Dequeues all external events from the buffer as.

        The list is of string representations of KernelProcessEvent.

        Returns:
            The dequeued external event.
        """
        ...
