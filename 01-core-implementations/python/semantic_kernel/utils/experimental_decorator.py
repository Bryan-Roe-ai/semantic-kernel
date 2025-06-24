#!/usr/bin/env python3
"""
Experimental Decorator module

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
from typing import TypeVar

T = TypeVar("T", bound=type)


def experimental_function(func: Callable) -> Callable:
    """Decorator to mark a function as experimental."""
    if callable(func):
        if func.__doc__:
            func.__doc__ += (
                "\n\nNote: This function is experimental and may change in the future."
            )
        else:
            func.__doc__ = (
                "Note: This function is experimental and may change in the future."
            )

        setattr(func, "is_experimental", True)

    return func


def experimental_class(cls: T) -> T:
    """Decorator to mark a class as experimental."""
    if isinstance(cls, type):
        if cls.__doc__:
            cls.__doc__ += (
                "\n\nNote: This class is experimental and may change in the future."
            )
        else:
            cls.__doc__ = (
                "Note: This class is experimental and may change in the future."
            )

        setattr(cls, "is_experimental", True)

    return cls
