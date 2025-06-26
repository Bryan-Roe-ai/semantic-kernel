#!/usr/bin/env python3
"""
import asyncio
Connector module

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


class ConnectorBase(ABC):
    """Base class for search engine connectors."""

    @abstractmethod
    async def search(
        self, query: str, num_results: int = 1, offset: int = 0
    ) -> list[str]:
        """Returns the search results of the query provided by pinging the search engine API."""
