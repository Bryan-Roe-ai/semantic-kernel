#!/usr/bin/env python3
"""
Kernel Process State module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import Literal

from pydantic import Field

from semantic_kernel.processes.kernel_process.kernel_process_step_state import KernelProcessStepState
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class KernelProcessState(KernelProcessStepState):
    """The state of a kernel process."""

    type: Literal["KernelProcessState"] = Field(default="KernelProcessState")  # type: ignore
