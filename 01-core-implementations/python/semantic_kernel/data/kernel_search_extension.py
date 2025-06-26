#!/usr/bin/env python3
"""
import asyncio
Kernel Search Extension module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


from semantic_kernel.data.text_search import TextSearch
from semantic_kernel.data.text_search_options import TextSearchOptions


class KernelSearchExtension:
    """Extension for the kernel search service."""

    def create_function_from_search(self, search: TextSearch, options: TextSearchOptions) -> callable:
        """Create a function from a search service."""

        async def search_function(query: str):
            return await search.search(query, options)

        return search_function
