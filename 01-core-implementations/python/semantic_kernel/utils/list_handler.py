#!/usr/bin/env python3
"""
List Handler module

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
from collections.abc import AsyncGenerator, AsyncIterable, Sequence
from typing import TypeVar

_T = TypeVar("_T")


async def desync_list(sync_list: Sequence[_T]) -> AsyncIterable[_T]:  # noqa: RUF029
    """De synchronize a list of synchronous objects."""
    for x in sync_list:
        yield x


async def empty_generator() -> AsyncGenerator[_T, None]:
    """An empty generator, can be used to return an empty generator."""
    if False:
        yield None
    await asyncio.sleep(0)
