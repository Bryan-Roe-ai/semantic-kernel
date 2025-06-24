#!/usr/bin/env python3
"""
Types module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from collections.abc import Callable
from typing import Any, Union

from semantic_kernel.functions.kernel_function import KernelFunction

KERNEL_FUNCTION_TYPE = Union[KernelFunction, Callable[..., Any]]
