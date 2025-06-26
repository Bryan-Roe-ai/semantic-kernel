#!/usr/bin/env python3
"""
import asyncio
Embedding Generator Base module

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
from typing import List

from numpy import ndarray


class EmbeddingGeneratorBase(ABC):
    @abstractmethod
    async def generate_embeddings_async(self, texts: List[str]) -> ndarray:
        pass
