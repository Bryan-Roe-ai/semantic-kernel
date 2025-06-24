#!/usr/bin/env python3
"""
Code Execution Plugin module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import Annotated

from ai_code_sandbox import AICodeSandbox

from semantic_kernel.functions import kernel_function


class CodeExecutionPlugin:
    """A plugin that runs Python code snippets."""

    @kernel_function(description="Run a Python code snippet. You can assume all the necessary packages are installed.")
    def run(
        self, code: Annotated[str, "The Python code snippet."]
    ) -> Annotated[str, "Returns the output of the code."]:
        """Run a Python code snippet."""
        sandbox: AICodeSandbox = AICodeSandbox(
            custom_image="python:3.12-slim",
            packages=["semantic_kernel"],
        )

        try:
            return sandbox.run_code(code)
        finally:
            sandbox.close()
