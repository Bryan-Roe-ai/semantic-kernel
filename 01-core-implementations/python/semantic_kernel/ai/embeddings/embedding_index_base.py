#!/usr/bin/env python3
"""
import asyncio
Embedding Index Base module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from abc import ABC, abstractmethod
from typing import List, Tuple

from numpy import ndarray

from semantic_kernel.memory.memory_record import MemoryRecord


class EmbeddingIndexBase(ABC):
    @abstractmethod
    async def get_nearest_matches_async(
        self,
        collection: str,
        embedding: ndarray,
        limit: int,
        min_relevance_score: float,
    ) -> List[Tuple[MemoryRecord, float]]:
        pass
