#!/usr/bin/env python3
"""
Null Memory module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import sys

from semantic_kernel.memory.memory_query_result import MemoryQueryResult
from semantic_kernel.memory.semantic_text_memory_base import SemanticTextMemoryBase

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated


@deprecated("This class will be removed in a future version.")
class NullMemory(SemanticTextMemoryBase):
    """Class for null memory."""

    async def save_information(
        self,
        collection: str,
        text: str,
        id: str,
        description: str | None = None,
        additional_metadata: str | None = None,
    ) -> None:
        """Nullifies behavior of SemanticTextMemoryBase save_information."""
        return

    async def save_reference(
from typing import List, Optional

from semantic_kernel.memory.memory_query_result import MemoryQueryResult
from semantic_kernel.memory.semantic_text_memory_base import SemanticTextMemoryBase


class NullMemory(SemanticTextMemoryBase):
    async def save_information_async(
        self, collection: str, text: str, id: str, description: Optional[str] = None
    ) -> None:
        return None

    async def save_reference_async(
        self,
        collection: str,
        text: str,
        external_id: str,
        external_source_name: str,
        description: str | None = None,
        additional_metadata: str | None = None,
    ) -> None:
        """Nullifies behavior of SemanticTextMemoryBase save_reference."""
        return

    async def get(self, collection: str, query: str) -> MemoryQueryResult | None:
        """Nullifies behavior of SemanticTextMemoryBase get."""
        return None

    async def search(
        description: Optional[str] = None,
    ) -> None:
        return None

    async def get_async(
        self, collection: str, query: str
    ) -> Optional[MemoryQueryResult]:
        return None

    async def search_async(
        self,
        collection: str,
        query: str,
        limit: int = 1,
        min_relevance_score: float = 0.7,
    ) -> list[MemoryQueryResult]:
        """Nullifies behavior of SemanticTextMemoryBase search."""
        return []

    async def get_collections(self) -> list[str]:
        """Nullifies behavior of SemanticTextMemoryBase get_collections."""
    ) -> List[MemoryQueryResult]:
        return []

    async def get_collections_async(self) -> List[str]:
        return []


NullMemory.instance = NullMemory()  # type: ignore
