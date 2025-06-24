#!/usr/bin/env python3
"""
Sk Function Decorator module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


def sk_function(description: str):
def sk_function(
    *,
    description: str = "",
    name: str = None,
    input_description: str = None,
    input_default_value: str = None
):
    """
    Decorator for SK functions.

    Args:
        description -- The description of the function
        name -- The name of the function
        input_description -- The description of the input
        input_default_value -- The default value of the input
    """

    def decorator(func):
        func.__sk_function__ = True
        func.__sk_function_description__ = description
        func.__sk_function_name__ = name if name else func.__name__
        func.__sk_function_input_description__ = input_description
        func.__sk_function_input_default_value__ = input_default_value
        return func

    return decorator
