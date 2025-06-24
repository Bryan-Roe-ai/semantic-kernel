#!/usr/bin/env python3
"""
AI module for mistral ai base

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from abc import ABC
from typing import ClassVar

from mistralai import Mistral

from semantic_kernel.kernel_pydantic import KernelBaseModel


class MistralAIBase(KernelBaseModel, ABC):
    """Mistral AI service base."""

    MODEL_PROVIDER_NAME: ClassVar[str] = "mistralai"

    async_client: Mistral
