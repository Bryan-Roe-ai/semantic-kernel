#!/usr/bin/env python3
"""
Kernel Process Message Channel module

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

from semantic_kernel.processes.local_runtime.local_event import KernelProcessEvent
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class KernelProcessMessageChannel(ABC):
    """Abstract base class for emitting events from a step."""

    @abstractmethod
    async def emit_event(self, process_event: "KernelProcessEvent") -> None:
        """Emits the specified event from the step."""
        pass
