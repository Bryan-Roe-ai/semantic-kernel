#!/usr/bin/env python3
"""
Kernel Process Step module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from abc import ABC
from typing import TYPE_CHECKING, Generic, TypeVar

from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.utils.feature_stage_decorator import experimental

if TYPE_CHECKING:
    from semantic_kernel.processes.kernel_process.kernel_process_step_state import KernelProcessStepState

TState = TypeVar("TState")


@experimental
class KernelProcessStep(ABC, KernelBaseModel, Generic[TState]):
    """A KernelProcessStep Base class for process steps."""

    state: TState | None = None

    async def activate(self, state: "KernelProcessStepState[TState]"):
        """Activates the step and sets the state."""
        pass  # pragma: no cover
