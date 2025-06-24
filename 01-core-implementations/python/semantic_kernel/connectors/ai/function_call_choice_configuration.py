#!/usr/bin/env python3
"""
Function Call Choice Configuration module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


from pydantic.dataclasses import dataclass

from semantic_kernel.functions.kernel_function_metadata import KernelFunctionMetadata
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
@dataclass
class FunctionCallChoiceConfiguration:
    """Configuration for function call choice."""

    available_functions: list[KernelFunctionMetadata] | None = None
