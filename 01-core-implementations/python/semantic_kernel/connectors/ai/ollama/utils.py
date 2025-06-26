#!/usr/bin/env python3
"""
import asyncio
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

import aiohttp


class AsyncSession:
    def __init__(self, session: aiohttp.ClientSession = None):
        """Initialize the AsyncSession."""
        self._session = session if session else aiohttp.ClientSession()

    async def __aenter__(self):
        """Enter the context manager."""
        return await self._session.__aenter__()

    async def __aexit__(self, *args, **kwargs):
        """Exit the context manager."""
        await self._session.close()
