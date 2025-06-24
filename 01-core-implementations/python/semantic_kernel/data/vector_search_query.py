#!/usr/bin/env python3
"""
Vector Search Query module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


from typing import Literal

from pydantic import Field

from semantic_kernel.data.const import VectorSearchQueryTypes
from semantic_kernel.data.vector_search_options import VectorSearchOptions
from semantic_kernel.kernel_pydantic import KernelBaseModel


class VectorSearchQuery(KernelBaseModel):
    """A query for vector search."""

    query_type: Literal[
        VectorSearchQueryTypes.VECTORIZED_SEARCH_QUERY,
        VectorSearchQueryTypes.VECTORIZABLE_TEXT_SEARCH_QUERY,
        VectorSearchQueryTypes.HYBRID_TEXT_VECTORIZED_SEARCH_QUERY,
        VectorSearchQueryTypes.HYBRID_VECTORIZABLE_TEXT_SEARCH_QUERY,
    ]
    search_options: VectorSearchOptions | None = Field(default_factory=VectorSearchOptions)
    query_text: str | None = None
    vector: list[float | int] | None = None
