#!/usr/bin/env python3
"""
Native Function module

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

from semantic_kernel.functions.kernel_function_decorator import kernel_function


class TestNativeEchoBotPlugin:
    """Description: Test Native Plugin for testing purposes"""

    @kernel_function(
        description="Echo for input text",
        name="echoAsync",
    )
    async def echo(self, text: Annotated[str, "The text to echo"]) -> str:
        """Echo for input text

        Example:
            "hello world" => "hello world"
        Args:
            text -- The text to echo

        Returns:
            input text
        """
        return text
