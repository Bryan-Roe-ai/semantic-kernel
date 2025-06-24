#!/usr/bin/env python3
"""
Block Types module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from enum import Enum, auto


class BlockTypes(Enum):
    """Block types."""

    UNDEFINED = auto()
    TEXT = auto()
    CODE = auto()
    VARIABLE = auto()
    VALUE = auto()
    FUNCTION_ID = auto()
    NAMED_ARG = auto()
from enum import Enum


class BlockTypes(Enum):
    Undefined = 0
    Text = 1
    Code = 2
    Variable = 3
