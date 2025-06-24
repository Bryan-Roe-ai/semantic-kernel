#!/usr/bin/env python3
"""
Test module for text to image base

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import pytest

from semantic_kernel.connectors.ai.open_ai.services.azure_text_to_image import AzureTextToImage
from semantic_kernel.connectors.ai.open_ai.services.open_ai_text_to_image import OpenAITextToImage
from semantic_kernel.connectors.ai.text_to_image_client_base import TextToImageClientBase


class TextToImageTestBase:
    """Base class for testing text-to-image services."""

    @pytest.fixture(scope="module")
    def services(self) -> dict[str, TextToImageClientBase]:
        """Return text-to-image services."""
        return {
            "openai": OpenAITextToImage(),
            "azure_openai": AzureTextToImage(),
        }
