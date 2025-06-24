#!/usr/bin/env python3
"""
Async Utils module

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
from collections.abc import Callable
from functools import partial
from typing import Any


async def run_in_executor(executor: Any, func: Callable, *args, **kwargs) -> Any:
    """Run a function in an executor."""
    return await asyncio.get_event_loop().run_in_executor(executor, partial(func, *args, **kwargs))
