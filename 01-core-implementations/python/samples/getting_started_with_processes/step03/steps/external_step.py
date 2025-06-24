#!/usr/bin/env python3
"""
External Step module

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

from semantic_kernel.functions import kernel_function
from semantic_kernel.processes.kernel_process import (
    KernelProcessEventVisibility,
    KernelProcessStep,
    KernelProcessStepContext,
)


class ExternalStep(KernelProcessStep):
    external_event_name: str

    def __init__(self, external_event_name: str):
        super().__init__(external_event_name=external_event_name)

    @kernel_function()
    async def emit_external_event(self, context: KernelProcessStepContext, data: Any):
        await context.emit_event(
            process_event=self.external_event_name, data=data, visibility=KernelProcessEventVisibility.Public
        )
