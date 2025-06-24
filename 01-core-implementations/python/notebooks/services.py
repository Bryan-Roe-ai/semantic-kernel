#!/usr/bin/env python3
"""
Services module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

from enum import Enum


class Service(Enum):
    """
    Attributes:
        OpenAI (str): Represents the OpenAI service.
        AzureOpenAI (str): Represents the Azure OpenAI service.
        HuggingFace (str): Represents the HuggingFace service.
    """

    OpenAI = "openai"
    AzureOpenAI = "azureopenai"
    HuggingFace = "huggingface"
