#!/usr/bin/env python3
"""
Kernel Types module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from collections.abc import Sequence
from typing import TypeVar, Union

from semantic_kernel.services.ai_service_client_base import AIServiceClientBase

AI_SERVICE_CLIENT_TYPE = TypeVar("AI_SERVICE_CLIENT_TYPE", bound=AIServiceClientBase)

T = TypeVar("T")

OneOrMany = Union[T, Sequence[T]]
OneOrList = Union[T, list[T]]
OptionalOneOrMany = Union[T, Sequence[T], None]
OptionalOneOrList = Union[T, list[T], None]

__all__ = ["AI_SERVICE_CLIENT_TYPE", "OneOrList", "OneOrMany", "OptionalOneOrList", "OptionalOneOrMany"]
