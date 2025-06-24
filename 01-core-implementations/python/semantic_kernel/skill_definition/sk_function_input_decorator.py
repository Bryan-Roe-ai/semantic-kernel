#!/usr/bin/env python3
"""
Sk Function Input Decorator module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


def sk_function_input(*, description: str, default_value: str = ""):
    """
    Decorator for SK function inputs.

    Args:
        description -- The description of the input
    """

    def decorator(func):
        func.__sk_function_input_description__ = description
        func.__sk_function_input_default_value__ = default_value
        return func

    return decorator
