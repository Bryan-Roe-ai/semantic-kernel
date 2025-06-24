#!/usr/bin/env python3
"""
Code Renderer module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from semantic_kernel import Kernel
    from semantic_kernel.functions.kernel_arguments import KernelArguments
from typing import Protocol, runtime_checkable

from semantic_kernel.orchestration.sk_context import SKContext


@runtime_checkable
class CodeRenderer(Protocol):
    """Protocol for dynamic code blocks that need async IO to be rendered."""

    @abstractmethod
    async def render_code(self, kernel: "Kernel", arguments: "KernelArguments") -> str:
        """Render the block using the given context.
        """Render the block using the given context.
        """Render the block using the given context.
        """Render the block using the given context.
        """Render the block using the given context.
        """
        Render the block using the given context.

        :param context: kernel execution context
        :return: Rendered content
        """
    """
    Protocol for dynamic code blocks that need async IO to be rendered.
    """

    async def render_code_async(self, context: SKContext) -> str:
        """
        Render the block using the given context.

        :param context: SK execution context
        :return: Rendered content
        """
        ...
