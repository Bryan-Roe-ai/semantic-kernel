#!/usr/bin/env python3
"""
Filter Clause Base module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


from abc import ABC

from pydantic import Field

from semantic_kernel.kernel_pydantic import KernelBaseModel


class FilterClauseBase(ABC, KernelBaseModel):
    """A base for all filter clauses."""

    filter_clause_type: str = Field("BaseFilterClause", init=False)  # type: ignore
