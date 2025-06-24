#!/usr/bin/env python3
"""
Filter Exceptions module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.
from semantic_kernel.exceptions.kernel_exceptions import KernelException


class FilterException(KernelException):
    """Base class for all filter exceptions."""

    pass


class FilterManagementException(FilterException):
    """An error occurred while adding or removing the filter to/from the kernel."""

    pass


__all__ = [
    "FilterException",
    "FilterManagementException",
]
