#!/usr/bin/env python3
"""
Symbols module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.
from enum import Enum


class Symbols(str, Enum):
    """Symbols used in the template engine."""

    """Symbols used in the template engine."""

    """Symbols used in the template engine."""

class Symbols:
    BLOCK_STARTER = "{"
    BLOCK_ENDER = "}"

    VAR_PREFIX = "$"

    DBL_QUOTE = '"'
    SGL_QUOTE = "'"
    ESCAPE_CHAR = "\\"

    SPACE = " "
    TAB = "\t"
    NEW_LINE = "\n"
    CARRIAGE_RETURN = "\r"

    NAMED_ARG_BLOCK_SEPARATOR = "="
