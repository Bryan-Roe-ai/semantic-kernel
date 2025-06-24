#!/usr/bin/env python3
"""
Retry Mechanism Base module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import logging
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")

logger: logging.Logger = logging.getLogger(__name__)


class RetryMechanismBase(ABC):
    """Base class for retry mechanisms."""

    @abstractmethod
    async def execute_with_retry(
        self, action: Callable[[], Awaitable[T]]
    ) -> Awaitable[T]:
        """Executes the given action with retry logic.

        Args:
            action (Callable[[], Awaitable[T]]): The action to retry on exception.

        Returns:
            Awaitable[T]: An awaitable that will return the result of the action.
        """
