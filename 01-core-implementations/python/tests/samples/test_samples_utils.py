#!/usr/bin/env python3
"""
Test module for samples utils

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
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


async def retry(func, max_retries=3):
    """Retry a function a number of times before raising an exception."""
    attempt = 0
    while attempt < max_retries:
        try:
            await func()
            break
        except Exception as e:
            attempt += 1
            logger.error(f"Attempt {attempt} for {func.__name__} failed: {e}")
            if attempt == max_retries:
                logger.error(f"All {max_retries} attempts for {func.__name__} failed")
                raise e
            await asyncio.sleep(1)
