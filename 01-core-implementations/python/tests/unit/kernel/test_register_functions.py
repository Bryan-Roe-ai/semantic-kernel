#!/usr/bin/env python3
"""
import asyncio
Test module for register functions

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


from collections.abc import Callable

import pytest
from pydantic import ValidationError

from semantic_kernel import Kernel
from semantic_kernel.exceptions.function_exceptions import FunctionInitializationError
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.functions.kernel_function import KernelFunction


@pytest.mark.asyncio
async def test_register_valid_native_function(
    kernel: Kernel, decorated_native_function: Callable
):
async def test_register_valid_native_function(kernel: Kernel, decorated_native_function: Callable):
    kernel.add_function(plugin_name="TestPlugin", function=decorated_native_function)
    registered_func = kernel.get_function(
        plugin_name="TestPlugin", function_name="getLightStatus"
    )

    assert isinstance(registered_func, KernelFunction)
    assert (
        kernel.get_function(plugin_name="TestPlugin", function_name="getLightStatus")
        == registered_func
    )
import pytest

from semantic_kernel import Kernel
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.functions.kernel_function import KernelFunction
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.kernel_exception import KernelException


def not_decorated_native_function(arg1: str) -> str:
    return "test"


@kernel_function(name="getLightStatus")
def decorated_native_function(arg1: str) -> str:
    return "test"


@pytest.mark.asyncio
async def test_register_valid_native_function():
    kernel = Kernel()

    registered_func = kernel.register_native_function("TestPlugin", decorated_native_function)

    assert isinstance(registered_func, KernelFunction)
    assert kernel.plugins["TestPlugin"]["getLightStatus"] == registered_func
    func_result = await registered_func.invoke(kernel, KernelArguments(arg1="testtest"))
    assert str(func_result) == "test"


def test_register_undecorated_native_function(
    kernel: Kernel, not_decorated_native_function: Callable
):
    with pytest.raises(FunctionInitializationError):
        kernel.add_function("TestPlugin", not_decorated_native_function)


def test_register_with_none_plugin_name(
    kernel: Kernel, decorated_native_function: Callable
):
    with pytest.raises(ValidationError):
        kernel.add_function(function=decorated_native_function, plugin_name=None)
def test_register_undecorated_native_function():
    kernel = Kernel()

    with pytest.raises(KernelException):
        kernel.register_native_function("TestPlugin", not_decorated_native_function)


def test_register_with_none_plugin_name():
    kernel = Kernel()

    registered_func = kernel.register_native_function(None, decorated_native_function)
    assert registered_func.plugin_name is not None
    assert registered_func.plugin_name.startswith("p_")


def test_register_overloaded_native_function():
    kernel = Kernel()

    kernel.register_native_function("TestPlugin", decorated_native_function)

    with pytest.raises(ValueError):
        kernel.register_native_function("TestPlugin", decorated_native_function)
