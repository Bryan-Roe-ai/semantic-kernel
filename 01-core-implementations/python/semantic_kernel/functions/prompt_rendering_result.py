#!/usr/bin/env python3
"""
Prompt Rendering Result module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.connectors.ai.prompt_execution_settings import (
    PromptExecutionSettings,
)
from semantic_kernel.functions.function_result import FunctionResult
from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.services.ai_service_client_base import AIServiceClientBase

class PromptRenderingResult(KernelBaseModel):
    """Represents the result of rendering a prompt template.

from typing import Any, Optional

from pydantic import Field

from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.kernel_pydantic import KernelBaseModel

class PromptRenderingResult(KernelBaseModel):
    """
    Represents the result of rendering a prompt template.

    Attributes:
        rendered_prompt (str): The rendered prompt.
        ai_service (Any): The AI service that rendered the prompt.

        execution_settings (PromptExecutionSettings): The execution settings for the prompt.
        function_result (FunctionResult): The result of executing the prompt.
    """

    rendered_prompt: str
    ai_service: AIServiceClientBase
    execution_settings: PromptExecutionSettings
    function_result: FunctionResult | None = None

        prompt_template (PromptTemplateConfig): The prompt template used to render the prompt.
    """

    rendered_prompt: str
    ai_service: Any
    execution_settings: Optional[PromptExecutionSettings] = Field(default_factory=PromptExecutionSettings)

