#!/usr/bin/env python3
"""
Ollama Base module

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

from ollama import AsyncClient

from semantic_kernel.kernel_pydantic import KernelBaseModel


class OllamaBase(KernelBaseModel, ABC):
    """Ollama service base.

    Args:
        client [AsyncClient]: An Ollama client to use for the service.
    """

    MODEL_PROVIDER_NAME: ClassVar[str] = "ollama"

    client: AsyncClient
