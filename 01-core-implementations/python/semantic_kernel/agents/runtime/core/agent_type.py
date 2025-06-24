#!/usr/bin/env python3
"""
Agent Type module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
@runtime_checkable
class AgentType(Protocol):
    """Defines the minimal interface an AgentType."""

    @property
    def type(self) -> str:
        """Defines the 'type' or category of the agent."""
        ...


@experimental
@dataclass(eq=True, frozen=True)
class CoreAgentType:
    """Concrete immutable implementation of AgentType."""

    _type: str

    @property
    def type(self) -> str:
        """Defines the 'type' or category of the agent."""
        return self._type

    def __str__(self) -> str:
        """Return the string representation of the agent type."""
        return self._type
