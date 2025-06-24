#!/usr/bin/env python3
"""
Kernel Process Edge module

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
from semantic_kernel.processes.kernel_process.kernel_process_function_target import KernelProcessFunctionTarget
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class KernelProcessEdge(KernelBaseModel):
    """Represents an edge between steps."""

    source_step_id: str
    output_target: KernelProcessFunctionTarget
