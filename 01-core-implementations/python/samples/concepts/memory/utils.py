#!/usr/bin/env python3
"""
Utils module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import TypeVar

from samples.concepts.resources.utils import Colors, print_with_color
from semantic_kernel.data.vector import VectorSearchResult

_T = TypeVar("_T")


def print_record(result: VectorSearchResult[_T] | None = None, record: _T | None = None):
    if result:
        record = result.record
    print_with_color(f"  Found id: {record.id}", Colors.CGREEN)
    if result and result.score is not None:
        print_with_color(f"    Score: {result.score}", Colors.CWHITE)
    print_with_color(f"    Title: {record.title}", Colors.CWHITE)
    print_with_color(f"    Content: {record.content}", Colors.CWHITE)
    print_with_color(f"    Tag: {record.tag}", Colors.CWHITE)
