#!/usr/bin/env python3
"""
Filter Context Base module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import TYPE_CHECKING

from semantic_kernel.kernel_pydantic import KernelBaseModel

if TYPE_CHECKING:
    from semantic_kernel.functions.kernel_arguments import KernelArguments
    from semantic_kernel.functions.kernel_function import KernelFunction
    from semantic_kernel.kernel import Kernel


class FilterContextBase(KernelBaseModel):
    """Base class for Kernel Filter Contexts."""

    function: "KernelFunction"
    kernel: "Kernel"
    arguments: "KernelArguments"
    is_streaming: bool = False
