#!/usr/bin/env python3
"""
Semantic Function Config module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from dataclasses import dataclass
from typing import TYPE_CHECKING

from semantic_kernel.semantic_functions.chat_prompt_template import ChatPromptTemplate

if TYPE_CHECKING:
    from semantic_kernel.semantic_functions.prompt_template import PromptTemplate
    from semantic_kernel.semantic_functions.prompt_template_config import (
        PromptTemplateConfig,
    )


@dataclass
class SemanticFunctionConfig:
    prompt_template_config: "PromptTemplateConfig"
    prompt_template: "PromptTemplate"

    @property
    def has_chat_prompt(self) -> bool:
        return isinstance(self.prompt_template, ChatPromptTemplate)
