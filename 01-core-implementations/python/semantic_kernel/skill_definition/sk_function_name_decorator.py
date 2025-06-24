#!/usr/bin/env python3
"""
Sk Function Name Decorator module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


def sk_function_name(name: str):
    """
    Decorator for SK function names.

    Args:
        name -- The name of the function
    """

    def decorator(func):
        func.__sk_function_name__ = name
        return func

    return decorator
