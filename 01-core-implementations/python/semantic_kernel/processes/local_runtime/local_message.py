#!/usr/bin/env python3
"""
Local Message module

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

from pydantic import Field

from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class LocalMessage(KernelBaseModel):
    """A message that is local to a namespace."""

    source_id: str = Field(...)
    destination_id: str = Field(...)
    function_name: str = Field(...)
    values: dict[str, Any | None] = Field(...)
    target_event_id: str | None = Field(default=None)
    target_event_data: Any | None = Field(default=None)
