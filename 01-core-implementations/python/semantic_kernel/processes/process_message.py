#!/usr/bin/env python3
"""
Process Message module

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
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class ProcessMessage(KernelBaseModel):
    """Represents a message used in a process runtime."""

    source_id: str
    destination_id: str
    function_name: str
    values: dict[str, Any]

    target_event_id: str | None = None
    target_event_data: Any | None = None
