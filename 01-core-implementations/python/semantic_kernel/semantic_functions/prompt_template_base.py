#!/usr/bin/env python3
"""
import asyncio
Prompt Template Base module

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
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from semantic_kernel.orchestration.sk_context import SKContext
    from semantic_kernel.skill_definition.parameter_view import ParameterView


class PromptTemplateBase(ABC):
    @abstractmethod
    def get_parameters(self) -> List["ParameterView"]:
        pass

    @abstractmethod
    async def render_async(self, context: "SKContext") -> str:
        pass
