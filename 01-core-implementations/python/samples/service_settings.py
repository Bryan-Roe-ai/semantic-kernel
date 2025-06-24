#!/usr/bin/env python3
"""
Service Settings module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import Literal

from semantic_kernel.kernel_pydantic import KernelBaseSettings


class ServiceSettings(KernelBaseSettings):
    """The Learn Resources Service Settings.

    The settings are first loaded from environment variables. If the
    environment variables are not found, the settings can be loaded from a .env file with the
    encoding 'utf-8' as default or the specific encoding. If the settings are not found in the
    .env file, the settings are ignored; however, validation will fail alerting that the settings
    are missing.

    Args:
        global_llm_service: The LLM service to use for the samples, either "OpenAI" or "AzureOpenAI"
            If not provided, defaults to "AzureOpenAI".
    """

    global_llm_service: Literal["OpenAI", "AzureOpenAI"] = "AzureOpenAI"
