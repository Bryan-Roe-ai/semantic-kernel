#!/usr/bin/env python3
"""
Async Default Azure Credential Wrapper module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import asyncio
import contextlib

from azure.identity.aio import DefaultAzureCredential


class AsyncDefaultAzureCredentialWrapper(DefaultAzureCredential):
    """Wrapper to make sure the async version of the DefaultAzureCredential is closed properly."""

    def __del__(self) -> None:
        """Close the DefaultAzureCredential."""
        with contextlib.suppress(Exception):
            asyncio.get_running_loop().create_task(self.close())
