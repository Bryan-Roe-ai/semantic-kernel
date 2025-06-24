#!/usr/bin/env python3
"""
Parameter View module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.diagnostics.verify import Verify
from semantic_kernel.utils.validation import validate_function_param_name


class ParameterView:
    _name: str
    _description: str
    _default_value: str

    def __init__(self, name: str, description: str, default_value: str) -> None:
        Verify.valid_function_param_name(name)
        validate_function_param_name(name)

        self._name = name
        self._description = description
        self._default_value = default_value

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def default_value(self) -> str:
        return self._default_value

    @name.setter
    def name(self, value: str) -> None:
        Verify.valid_function_param_name(value)
        validate_function_param_name(value)
        self._name = value

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @default_value.setter
    def default_value(self, value: str) -> None:
        self._default_value = value
