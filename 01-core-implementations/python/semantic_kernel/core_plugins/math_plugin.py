#!/usr/bin/env python3
"""
Math Plugin module

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
import sys

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function


class MathPlugin:
    """Description: MathPlugin provides a set of functions to make Math calculations.

    Usage:
        kernel.add_plugin(MathPlugin(), plugin_name="math")

    Examples:
        {{math.Add}} => Returns the sum of input and amount (provided in the KernelArguments)
        {{math.Subtract}} => Returns the difference of input and amount (provided in the KernelArguments)
    """

    def _parse_number(self, val: int | float | str) -> float:
        """Helper to parse a value as a float (supports int, float, str)."""
        if isinstance(val, (int, float)):
            return float(val)
        try:
            return float(val)
        except Exception as ex:
            raise ValueError(f"Cannot convert {val!r} to float for math operation") from ex

    @kernel_function(name="Add")
    def add(
        self,
        input: Annotated[int | float | str, "The first number to add"],
        amount: Annotated[int | float | str, "The second number to add"],
    ) -> Annotated[float, "The result"]:
        """Returns the addition result of the values provided (supports float and int)."""
        x = self._parse_number(input)
        y = self._parse_number(amount)
        return x + y

    @kernel_function(name="Subtract")
    @kernel_function(
        description="Subtracts value to a value",
        name="Subtract",
    )
    def subtract(
        self,
        input: Annotated[int, "the first number"],
        amount: Annotated[int, "the number to subtract"],
    ) -> int:
        input: Annotated[int | str, "The number to subtract from"],
        amount: Annotated[int | str, "The number to subtract"],
    ) -> Annotated[int, "The result"]:
        """
        Returns the difference of numbers provided.

        :param initial_value_text: Initial value as string to subtract the specified amount
        :param context: Contains the context to get the numbers from
        :return: The resulting subtraction as a string
        """
        if isinstance(input, str):
            input = int(input)
        if isinstance(amount, str):
            amount = int(amount)
    @staticmethod
    def add_or_subtract(input: int, amount: int, add: bool) -> int:
        """
        Helper function to perform addition or subtraction based on the add flag.

        :param initial_value_text: Initial value as string to add or subtract the specified amount
        :param context: Contains the context to get the numbers from
        :param add: If True, performs addition, otherwise performs subtraction
        :return: The resulting sum or subtraction as a string
        """
        return input + amount if add else input - amount
        return input - amount
        input: Annotated[int | float | str, "The number to subtract from"],
        amount: Annotated[int | float | str, "The number to subtract"],
    ) -> Annotated[float, "The result"]:
        """Returns the difference of numbers provided (supports float and int)."""
        x = self._parse_number(input)
        y = self._parse_number(amount)
        return x - y
