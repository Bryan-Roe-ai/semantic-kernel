#!/usr/bin/env python3
"""
Test module for utils

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
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


async def retry(func, retries=20):
    min_delay = 2
    max_delay = 7
    for i in range(retries):
        try:
            return await func()
        except Exception as e:
            logger.error(f"Retry {i + 1}: {e}")
            if i == retries - 1:  # Last retry
                raise
            await asyncio.sleep(max(min(i, max_delay), min_delay))
    return None


def is_service_setup_for_testing(env_var_name: str) -> bool:
    return env_var_name in os.environ and os.environ[env_var_name]
