# Copyright (c) Microsoft. All rights reserved.

from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from semantic_kernel.diagnostics.verify import Verify
from semantic_kernel.kernel_base import KernelBase
from semantic_kernel.semantic_functions.prompt_template import PromptTemplate
from semantic_kernel.semantic_functions.prompt_template_config import (
    PromptTemplateConfig,
)
from semantic_kernel.semantic_functions.semantic_function_config import (
    SemanticFunctionConfig,
)

if TYPE_CHECKING:
    from semantic_kernel.orchestration.sk_function_base import SKFunctionBase


def create_semantic_function(
    kernel: KernelBase,
    prompt_template: str,
    function_name: Optional[str] = None,
    skill_name: Optional[str] = None,
    description: Optional[str] = None,
    max_tokens: int = 256,
    temperature: float = 0.0,
    top_p: float = 1.0,
    presence_penalty: float = 0.0,
    frequency_penalty: float = 0.0,
    stop_sequences: Optional[List[str]] = None,
) -> "SKFunctionBase":
    function_name = (
        function_name
        if function_name is not None
        else f"f_{str(uuid4()).replace('-', '_')}"
    )

    config = PromptTemplateConfig(
        description=(
            description
            if description is not None
            else "Generic function, unknown purpose"
        ),
        type="completion",
        completion=PromptTemplateConfig.CompletionConfig(
            temperature,
            top_p,
            presence_penalty,
            frequency_penalty,
            max_tokens,
            stop_sequences if stop_sequences is not None else [],
        ),
    )

    Verify.valid_function_name(function_name)
    if skill_name is not None:
        Verify.valid_skill_name(skill_name)

    template = PromptTemplate(prompt_template, kernel.prompt_template_engine, config)
    function_config = SemanticFunctionConfig(config, template)

    return kernel.register_semantic_function(skill_name, function_name, function_config)
