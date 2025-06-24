#!/usr/bin/env python3
"""
Context Variables module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


from typing import Dict, Tuple

from semantic_kernel.diagnostics.verify import Verify


class ContextVariables:
    _variables: Dict[str, str] = {}
    _main_key = "input"

    def __init__(self, content: str = "") -> None:

class ContextVariables:
    def __init__(self, content: str = "", variables: Dict[str, str] = None) -> None:
        """
        Initialize the ContextVariables instance with an optional content string.

        :param content: The content string to be stored as the main variable,
            defaults to an empty string.
        """
        self._variables: Dict[str, str] = variables or {}
        self._main_key: str = "input"
        self._variables[self._main_key] = content

    @property
    def input(self) -> str:
        return self._variables[self._main_key]

    def update(self, content: str) -> "ContextVariables":
        self._variables[self._main_key] = content
        return self

    def merge_or_overwrite(
        self, new_context: "ContextVariables", merge: bool = True
    ) -> "ContextVariables":
        if not merge:
            self._variables = {}

        self._variables.update(new_context._variables)
        return self

    def set(self, name: str, value: str) -> "ContextVariables":
        Verify.not_empty(name, "The variable name is empty")
        if not name:
            raise ValueError("The variable name cannot be `None` or empty")
        name = name.lower()

        if value is not None:
            self._variables[name] = value
        else:
            self._variables.pop(name, None)

        return self

    def get(self, name: str) -> Tuple[bool, str]:
        name = name.lower()
        if name in self._variables:
            return True, self._variables[name]

        return False, ""

    def __getitem__(self, name: str) -> str:
        name = name.lower()
        return self._variables[name]

    def __setitem__(self, name: str, value: str) -> None:
        Verify.not_empty(name, "The variable name is empty")
        if not name:
            raise ValueError("The variable name cannot be `None` or empty")
        name = name.lower()
        self._variables[name] = value

    def contains_key(self, name: str) -> bool:
        name = name.lower()
        return name in self._variables

    def __str__(self) -> str:
        return self._variables[self._main_key]

    def clone(self) -> "ContextVariables":
        new_vars = ContextVariables()
        main_content = self._variables.get(self._main_key, "")
        new_vars = ContextVariables(main_content)
        new_vars._variables = self._variables.copy()
        return new_vars
