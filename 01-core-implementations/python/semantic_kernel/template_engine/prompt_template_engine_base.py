#!/usr/bin/env python3
"""
import asyncio
Prompt Template Engine Base module

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
from typing import List, Optional

from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.orchestration.sk_context import SKContext
from semantic_kernel.template_engine.blocks.block import Block


class PromptTemplateEngineBase(ABC):
    @abstractmethod
    def extract_blocks(
        self, template_text: Optional[str], validate: bool = True
    ) -> List[Block]:
        pass

    @abstractmethod
    async def render_async(self, template_text: str, context: SKContext) -> str:
        pass

    @abstractmethod
    async def render_blocks_async(self, blocks: List[Block], context: SKContext) -> str:
        pass

    @abstractmethod
    async def render_variables(
        self, blocks: List[Block], context: Optional[ContextVariables]
    ) -> List[Block]:
        pass

    @abstractmethod
    async def render_code_async(
        self, blocks: List[Block], context: SKContext
    ) -> List[Block]:
        pass
