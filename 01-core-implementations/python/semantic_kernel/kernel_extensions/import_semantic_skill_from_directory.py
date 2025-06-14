# Copyright (c) Microsoft. All rights reserved.

import glob
import os
from typing import Dict

from semantic_kernel.diagnostics.verify import Verify
from semantic_kernel.kernel_base import KernelBase
from semantic_kernel.orchestration.sk_function_base import SKFunctionBase
from semantic_kernel.semantic_functions.prompt_template import PromptTemplate
from semantic_kernel.semantic_functions.prompt_template_config import (
    PromptTemplateConfig,
)
from semantic_kernel.semantic_functions.semantic_function_config import (
    SemanticFunctionConfig,
)


def import_semantic_skill_from_directory(
    kernel: KernelBase, parent_directory: str, skill_directory_name: str
) -> Dict[str, SKFunctionBase]:
    CONFIG_FILE = "config.json"
    PROMPT_FILE = "skprompt.txt"

    Verify.valid_skill_name(skill_directory_name)
    skill_directory = os.path.join(parent_directory, skill_directory_name)
    skill_directory = os.path.abspath(skill_directory)
    Verify.directory_exists(skill_directory)

    skill = {}

    directories = glob.glob(skill_directory + "/*/")
    for directory in directories:
        dir_name = os.path.dirname(directory)
        function_name = os.path.basename(dir_name)
        prompt_path = os.path.join(directory, PROMPT_FILE)

        # Continue only if the prompt template exists
        if not os.path.exists(prompt_path):
            continue

        config = PromptTemplateConfig()
        config_path = os.path.join(directory, CONFIG_FILE)
        with open(config_path, "r") as config_file:
            config.from_json(config_file.read())

        # Load Prompt Template
        with open(prompt_path, "r") as prompt_file:
            template = PromptTemplate(
                prompt_file.read(), kernel.prompt_template_engine, config
            )

        # Prepare lambda wrapping AI logic
        function_config = SemanticFunctionConfig(config, template)

        skill[function_name] = kernel.register_semantic_function(
            skill_directory_name, function_name, function_config
        )

    return skill
