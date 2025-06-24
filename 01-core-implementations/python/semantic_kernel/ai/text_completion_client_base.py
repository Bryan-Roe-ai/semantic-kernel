#!/usr/bin/env python3
"""
Text Completion Client Base module

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
from logging import Logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from semantic_kernel.ai.complete_request_settings import CompleteRequestSettings


class TextCompletionClientBase(ABC):
    @abstractmethod
    async def complete_simple_async(
        self,
        prompt: str,
        settings: "CompleteRequestSettings",
        logger: Logger,
    ) -> str:
        pass
