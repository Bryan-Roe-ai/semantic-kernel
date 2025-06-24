#!/usr/bin/env python3
"""
Process Event module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import Any

from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.processes.kernel_process.kernel_process_event import (
    KernelProcessEvent,
    KernelProcessEventVisibility,
)
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class ProcessEvent(KernelBaseModel):
    """A wrapper around KernelProcessEvent that helps to manage the namespace of the event."""

    namespace: str | None = None
    inner_event: KernelProcessEvent

    @property
    def id(self) -> str:
        """The Id of the event."""
        return f"{self.namespace}.{self.inner_event.id}"

    @property
    def data(self) -> Any | None:
        """The data of the event."""
        return self.inner_event.data

    @property
    def visibility(self) -> "KernelProcessEventVisibility":
        """The visibility of the event."""
        return self.inner_event.visibility
