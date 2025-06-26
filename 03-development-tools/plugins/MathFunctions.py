#!/usr/bin/env python3
"""
Mathfunctions module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

from typing import Union
import math

from semantic_kernel.functions.kernel_function_decorator import kernel_function

class MathFunctions:
    """A collection of mathematical functions."""

    @kernel_function(
        description="Calculate the square root of a number",
        name="sqrt"
    )
    def calculate_square_root(self, input_str: str) -> str:
        """
        Calculate the square root of the input number.

        Args:
            input_str: The input number as a string

        Returns:
            The square root as a string
        """
        try:
            # Try to convert to a number
            input_num = float(input_str.strip())

            # Handle negative numbers (complex square roots)
            if input_num < 0:
                result = math.sqrt(abs(input_num))
                return f"0 + {result}i (Complex number)"
            else:
                result = math.sqrt(input_num)
                if result.is_integer():
                    return str(int(result))
                return str(result)
        except ValueError:
            return "Error: Input must be a valid number"

    @kernel_function(
        description="Calculate the power of a number",
        name="power"
    )
    def calculate_power(self, base: str, exponent: str) -> str:
        """
        Calculate the power of a number.

        Args:
            base: The base number
            exponent: The exponent

        Returns:
            The result of base raised to the exponent
        """
        try:
            base_num = float(base.strip())
            exp_num = float(exponent.strip())

            result = math.pow(base_num, exp_num)
            if result.is_integer():
                return str(int(result))
            return str(result)
        except ValueError:
            return "Error: Inputs must be valid numbers"
        except OverflowError:
            return "Error: Result too large to compute"

    @kernel_function(
        description="Calculate sine of an angle in degrees",
        name="sin"
    )
    def calculate_sin(self, angle: str) -> str:
        """
        Calculate the sine of an angle in degrees.

        Args:
            angle: The angle in degrees

        Returns:
            The sine value
        """
        try:
            angle_degrees = float(angle.strip())
            angle_radians = math.radians(angle_degrees)
            result = math.sin(angle_radians)
            # Handle very small numbers near zero
            if abs(result) < 1e-10:
                return "0"
            return str(round(result, 8))
        except ValueError:
            return "Error: Input must be a valid number"
