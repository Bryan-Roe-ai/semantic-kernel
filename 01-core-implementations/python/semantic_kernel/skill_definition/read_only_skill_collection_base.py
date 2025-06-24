#!/usr/bin/env python3
"""
Read Only Skill Collection Base module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from semantic_kernel.orchestration.sk_function_base import SKFunctionBase
    from semantic_kernel.skill_definition.functions_view import FunctionsView


class ReadOnlySkillCollectionBase(ABC):
    @abstractmethod
    def has_function(self, skill_name: Optional[str], function_name: str) -> bool:
        pass

    @abstractmethod
    def has_semantic_function(
        self, skill_name: Optional[str], function_name: str
    ) -> bool:
        pass

    @abstractmethod
    def has_native_function(
        self, skill_name: Optional[str], function_name: str
    ) -> bool:
        pass

    @abstractmethod
    def get_semantic_function(
        self, skill_name: Optional[str], function_name: str
    ) -> "SKFunctionBase":
        pass

    @abstractmethod
    def get_native_function(
        self, skill_name: Optional[str], function_name: str
    ) -> "SKFunctionBase":
        pass

    @abstractmethod
    def get_functions_view(
        self, include_semantic: bool = True, include_native: bool = True
    ) -> "FunctionsView":
        pass

    @abstractmethod
    def get_function(
        self, skill_name: Optional[str], function_name: str
    ) -> "SKFunctionBase":
        pass
