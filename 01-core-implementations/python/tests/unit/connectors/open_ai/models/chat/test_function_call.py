#!/usr/bin/env python3
"""
Test module for function call

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import pytest

from semantic_kernel.connectors.ai.open_ai.models.chat_completion.function_call import FunctionCall
from semantic_kernel.functions.kernel_arguments import KernelArguments


def test_function_call():
    # Test initialization with default values
    fc = FunctionCall(name="Test-Function", arguments="""{"input": "world"}""", id="1234")
    assert fc.name == "Test-Function"
    assert fc.arguments == """{"input": "world"}"""
    assert fc.id == "1234"


@pytest.mark.asyncio
async def test_function_call_to_kernel_arguments():
    # Test parsing arguments to variables
    arguments = KernelArguments()
    func_call = FunctionCall(
        name="Test-Function",
        arguments="""{"input": "world", "input2": "world2"}""",
        id="1234",
    )
    assert isinstance(func_call.to_kernel_arguments(), KernelArguments)

    arguments.update(func_call.to_kernel_arguments())
    assert arguments["input"] == "world"
    assert arguments["input2"] == "world2"
