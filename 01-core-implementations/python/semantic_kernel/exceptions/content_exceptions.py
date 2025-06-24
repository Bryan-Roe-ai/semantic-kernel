#!/usr/bin/env python3
"""
Content Exceptions module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.exceptions.kernel_exceptions import KernelException


class ContentException(KernelException):
    """Base class for all content exceptions."""


class ContentInitializationError(ContentException):
    """An error occurred while initializing the content."""


class ContentSerializationError(ContentException):
    """An error occurred while serializing the content."""


class ContentAdditionException(ContentException):
    """An error occurred while adding content."""


class FunctionCallInvalidNameException(ContentException):
    """An error occurred while validating the function name."""


class FunctionCallInvalidArgumentsException(ContentException):
    """An error occurred while validating the function arguments."""


class ChatHistoryReducerException(ContentException):
    """An error occurred while reducing chat history."""

    pass


__all__ = [
    "ChatHistoryReducerException",
    "ContentAdditionException",
    "ContentException",
    "ContentInitializationError",
    "ContentSerializationError",
    "FunctionCallInvalidArgumentsException",
    "FunctionCallInvalidNameException",
]
