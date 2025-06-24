#!/usr/bin/env python3
"""
Streaming Kernel Content module

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
from typing import Any, Dict, Optional

from pydantic import Field

from semantic_kernel.kernel_pydantic import KernelBaseModel


class StreamingKernelContent(KernelBaseModel, ABC):
    """Base class for all streaming kernel contents."""

    choice_index: int
    inner_content: Optional[Any] = None
    ai_model_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __bytes__(self) -> bytes:
        pass

    @abstractmethod
    def __add__(self, other: "StreamingKernelContent") -> "StreamingKernelContent":
        pass
