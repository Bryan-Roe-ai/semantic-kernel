#!/usr/bin/env python3
"""
Kernel Process Event module

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
from typing import Any

from pydantic import ConfigDict

from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class KernelProcessEventVisibility(Enum):
    """Visibility of a kernel process event."""

    # The event is visible inside the process as well as outside the process. This is useful
    # when the event is intended to be consumed by other processes or external systems.
    Public = "Public"

    # The event is only visible to steps within the same process.
    Internal = "Internal"


@experimental
class KernelProcessEvent(KernelBaseModel):
    """A kernel process event."""

    id: str
    data: Any | None = None
    visibility: KernelProcessEventVisibility = KernelProcessEventVisibility.Internal

    model_config = ConfigDict(use_enum_values=False)
