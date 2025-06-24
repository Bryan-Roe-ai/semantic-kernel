#!/usr/bin/env python3
"""
Kernel Process Step State module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import Generic, Literal, TypeVar

from pydantic import ConfigDict, Field

from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.utils.feature_stage_decorator import experimental

TState = TypeVar("TState")


@experimental
class KernelProcessStepState(KernelBaseModel, Generic[TState]):
    """The state of a step in a kernel process."""

    type: Literal["KernelProcessStepState"] = Field(default="KernelProcessStepState")  # type: ignore

    name: str
    version: str
    id: str | None = None
    state: TState | None = None

    model_config = ConfigDict(extra="ignore")
