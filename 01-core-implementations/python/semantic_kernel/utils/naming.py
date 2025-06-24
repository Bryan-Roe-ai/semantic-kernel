#!/usr/bin/env python3
"""
Naming module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import random
import string


def generate_random_ascii_name(length: int = 16) -> str:
    """Generate a series of random ASCII characters of the specified length.

    As example, plugin/function names can contain upper/lowercase letters, and underscores

    Args:
        length (int): The length of the string to generate.

    Returns:
        A string of random ASCII characters of the specified length.
    """
    letters = string.ascii_letters
    return "".join(random.choices(letters, k=length))  # nosec
