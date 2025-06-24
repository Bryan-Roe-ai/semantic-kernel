#!/usr/bin/env python3
"""
Extends Kernel module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import Protocol

from semantic_kernel.kernel_base import KernelBase


class ExtendsKernel(Protocol):
    def kernel(self) -> KernelBase:
        ...
