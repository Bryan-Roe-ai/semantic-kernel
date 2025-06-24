#!/usr/bin/env python3
"""
Skill Collection Base module

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
from typing import TYPE_CHECKING

from semantic_kernel.skill_definition.read_only_skill_collection_base import (
    ReadOnlySkillCollectionBase,
)

if TYPE_CHECKING:
    from semantic_kernel.orchestration.sk_function_base import SKFunctionBase


class SkillCollectionBase(ReadOnlySkillCollectionBase, ABC):
    @property
    @abstractmethod
    def read_only_skill_collection(self) -> ReadOnlySkillCollectionBase:
        pass

    @abstractmethod
    def add_semantic_function(
        self, semantic_function: "SKFunctionBase"
    ) -> "SkillCollectionBase":
        pass

    @abstractmethod
    def add_native_function(
        self, native_function: "SKFunctionBase"
    ) -> "SkillCollectionBase":
        pass
