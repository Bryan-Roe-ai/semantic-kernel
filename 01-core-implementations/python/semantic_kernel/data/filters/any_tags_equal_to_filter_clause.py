#!/usr/bin/env python3
"""
Any Tags Equal To Filter Clause module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


from pydantic import Field

from semantic_kernel.data.filters.filter_clause_base import FilterClauseBase
from semantic_kernel.kernel_pydantic import KernelBaseModel


class AnyTagsEqualTo(FilterClauseBase, KernelBaseModel):
    """A filter clause for a any tags equals comparison."""

    filter_clause_type: str = Field("any_tags_equal_to", init=False)  # type: ignore

    field_name: str
    value: str
