# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.utils.settings import openai_settings_from_dot_env
from semantic_kernel.utils.null_logger import NullLogger
from semantic_kernel.utils.logging import setup_logging
from semantic_kernel.prompt_template.prompt_template_config import (
    PromptTemplateConfig,
)
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel import core_plugins, memory
from semantic_kernel.semantic_functions.semantic_function_config import (
    SemanticFunctionConfig,
)
from semantic_kernel.semantic_functions.prompt_template_config import (
    PromptTemplateConfig,
)
from semantic_kernel.semantic_functions.prompt_template import PromptTemplate
from semantic_kernel.orchestration.sk_function_base import SKFunctionBase
from semantic_kernel.orchestration.sk_context import SKContext
from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.memory.null_memory import NullMemory
from semantic_kernel.kernel_extensions import KernelExtensions as extensions
from semantic_kernel.kernel_builder import KernelBuilder
from semantic_kernel.kernel_base import KernelBase
from semantic_kernel.configuration.kernel_config import KernelConfig
import semantic_kernel.memory as memory
from semantic_kernel.kernel import Kernel

__version__ = "1.18.1"
__all__ = ["Kernel", "__version__"]

# from semantic_kernel.prompt_template.chat_prompt_template import ChatPromptTemplate
# from semantic_kernel.prompt_template.prompt_template import PromptTemplate


def create_kernel() -> KernelBase:
    return KernelBuilder.create_kernel()


def kernel_builder() -> KernelBuilder:
    return KernelBuilder(KernelConfig(), NullMemory(), NullLogger())


__all__ = [
    "create_kernel",
    "openai_settings_from_dot_env",
    "extensions",
    "PromptTemplateConfig",
    "PromptTemplate",
    "SemanticFunctionConfig",
    "ContextVariables",
    "SKFunctionBase",
    "SKContext",
    "memory",
]
    "KernelArguments",
    "memory",
]
__version__= "1.17.0"
__all__= ["Kernel", "__version__"]
