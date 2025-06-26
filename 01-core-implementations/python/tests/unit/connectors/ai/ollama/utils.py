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

import json


class MockResponse:
    def __init__(self, response, status=200):
        self._response = response
        self.status = status

    async def text(self):
        return self._response

    async def json(self):
        return self._response

    def raise_for_status(self):
        pass

    @property
    async def content(self):
        yield json.dumps(self._response).encode("utf-8")
        yield json.dumps({"done": True}).encode("utf-8")

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self
