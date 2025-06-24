#!/usr/bin/env python3
"""
Function Calling Stepwise Planner Result module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import sys
from typing import Annotated

from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.kernel_pydantic import KernelBaseModel

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated


@deprecated("Will be removed in a future version.")
class FunctionCallingStepwisePlannerResult(KernelBaseModel):
    """The result of the function calling stepwise planner."""

    final_answer: str = ""
    chat_history: ChatHistory | None = None
    iterations: int = 0


@deprecated("Will be removed in a future version.")
class UserInteraction:
    """The Kernel Function used to interact with the user."""

    @kernel_function(
        description="The final answer to return to the user", name="SendFinalAnswer"
    )
    def send_final_answer(self, answer: Annotated[str, "The final answer"]) -> str:
        """Send the final answer to the user."""
        return "Thanks"
