#!/usr/bin/env python3
"""
Bing Search Response module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import Any

from pydantic import Field

from semantic_kernel.connectors.search.bing.bing_web_page import BingWebPage
from semantic_kernel.kernel_pydantic import KernelBaseModel


from semantic_kernel.utils.experimental_decorator import experimental_class


@experimental_class
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class BingWebPages(KernelBaseModel):
    """The web pages from a Bing search."""

    id: str | None = None
    some_results_removed: bool | None = Field(default=None, alias="someResultsRemoved")
    total_estimated_matches: int | None = Field(default=None, alias="totalEstimatedMatches")
    web_search_url: str | None = Field(default=None, alias="webSearchUrl")
    value: list[BingWebPage] = Field(default_factory=list)

@experimental_class
@experimental
class BingSearchResponse(KernelBaseModel):
    """The response from a Bing search."""

    type_: str = Field(default="", alias="_type")
    query_context: dict[str, Any] = Field(default_factory=dict, validation_alias="queryContext")
    web_pages: BingWebPages | None = Field(default=None, alias="webPages")
