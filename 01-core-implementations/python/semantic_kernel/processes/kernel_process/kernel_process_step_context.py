#!/usr/bin/env python3
"""
Kernel Process Step Context module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from enum import Enum

from semantic_kernel.exceptions.process_exceptions import ProcessEventUndefinedException
from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.processes.kernel_process.kernel_process_message_channel import KernelProcessMessageChannel
from semantic_kernel.processes.local_runtime.local_event import KernelProcessEvent
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class KernelProcessStepContext(KernelBaseModel):
    """The context of a step in a kernel process."""

    step_message_channel: KernelProcessMessageChannel

    def __init__(self, channel: KernelProcessMessageChannel):
        """Initialize the step context."""
        super().__init__(step_message_channel=channel)  # type: ignore

    async def emit_event(self, process_event: "KernelProcessEvent | str | Enum | None", **kwargs) -> None:
        """Emit an event from the current step.

        It is possible to either specify a `KernelProcessEvent` object or the ID of the event
        along with the `data` and optional `visibility` keyword arguments.

        Args:
            process_event (KernelProcessEvent | str): The event to emit.
            **kwargs: Additional keyword arguments to pass to the event.
        """
        from semantic_kernel.processes.kernel_process.kernel_process_event import KernelProcessEvent

        if process_event is None:
            raise ProcessEventUndefinedException("Process event cannot be None")

        if not isinstance(process_event, KernelProcessEvent):
            process_event = KernelProcessEvent(
                id=process_event.value if isinstance(process_event, Enum) else process_event, **kwargs
            )

        await self.step_message_channel.emit_event(process_event)
