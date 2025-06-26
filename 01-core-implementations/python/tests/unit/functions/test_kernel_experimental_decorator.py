#!/usr/bin/env python3
"""
import re
Test module for kernel experimental decorator

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.utils.experimental_decorator import experimental_function


@experimental_function
def my_function() -> None:
    """This is a sample function docstring."""


@experimental_function
def my_function_no_doc_string() -> None:
    pass


def test_function_experimental_decorator() -> None:
    assert (
        my_function.__doc__
        == "This is a sample function docstring.\n\nNote: This function is experimental and may change in the future."
    )
    assert hasattr(my_function, "is_experimental")
    assert my_function.is_experimental is True


def test_function_experimental_decorator_with_no_doc_string() -> None:
    assert (
        my_function_no_doc_string.__doc__
        == "Note: This function is experimental and may change in the future."
    )
    assert hasattr(my_function_no_doc_string, "is_experimental")
    assert my_function_no_doc_string.is_experimental is True
