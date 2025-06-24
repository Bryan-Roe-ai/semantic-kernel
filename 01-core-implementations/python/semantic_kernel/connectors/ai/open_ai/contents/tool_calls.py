#!/usr/bin/env python3
"""
Tool Calls module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.
from typing import Literal, Optional

from semantic_kernel.connectors.ai.open_ai.contents.function_call import FunctionCall
from semantic_kernel.kernel_pydantic import KernelBaseModel


class ToolCall(KernelBaseModel):
    """Class to hold a tool call response."""

    id: Optional[str] = None
    type: Optional[Literal["function"]] = "function"
    function: Optional[FunctionCall] = None

    def __add__(self, other: Optional["ToolCall"]) -> "ToolCall":
        """Add two tool calls together, combines the function calls, ignores the id."""
        if not other:
            return self
        return ToolCall(
            id=self.id or other.id,
            type=self.type or other.type,
            function=self.function + other.function if self.function else other.function,
        )
