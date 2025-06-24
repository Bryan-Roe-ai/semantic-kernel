#!/usr/bin/env python3
"""
Kernel Search Result module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from collections.abc import Mapping, Sequence
from typing import Any, Generic, TypeVar

from semantic_kernel.kernel_pydantic import KernelBaseModel

T = TypeVar("T")


class KernelSearchResult(KernelBaseModel, Generic[T]):
    """The result of a kernel search."""

    results: Sequence[T]
    total_count: int | None = None
    metadata: Mapping[str, Any] | None = None
