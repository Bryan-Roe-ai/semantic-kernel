#!/usr/bin/env python3
"""
Const module

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


class FilterClauseType(str, Enum):
    """Types of filter clauses for search queries."""

    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    ANY_TAG_EQUAL_TO = "any_tag_equal_to"
