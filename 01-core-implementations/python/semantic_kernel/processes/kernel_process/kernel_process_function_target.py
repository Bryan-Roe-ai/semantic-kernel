#!/usr/bin/env python3
"""
Kernel Process Function Target module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class KernelProcessFunctionTarget(KernelBaseModel):
    """The target of a function call in a kernel process."""

    step_id: str
    function_name: str
    parameter_name: str | None = None
    target_event_id: str | None = None
