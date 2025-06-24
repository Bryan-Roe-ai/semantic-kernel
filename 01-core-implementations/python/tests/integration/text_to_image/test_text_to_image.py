#!/usr/bin/env python3
"""
Test module for text to image

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

from semantic_kernel.connectors.ai.text_to_image_client_base import TextToImageClientBase
from tests.integration.text_to_image.text_to_image_test_base import TextToImageTestBase

pytestmark = pytest.mark.parametrize(
    "service_id, prompt",
    [
        pytest.param(
            "openai",
            "A cute tuxedo cat driving a race car.",
            id="openai",
        ),
        pytest.param(
            "azure_openai",
            "A cute tuxedo cat driving a race car.",
            id="azure_openai",
            marks=[
                pytest.mark.xfail(
                    reason="Temporary failure due to Internal Server Error (500) from Azure OpenAI.",
                ),
            ],
        ),
    ],
)


class TestTextToImage(TextToImageTestBase):
    """Test text-to-image services."""

    async def test_text_to_image(
        self,
        services: dict[str, TextToImageClientBase],
        service_id: str,
        prompt: str,
    ):
        service = services[service_id]
        image_url = await service.generate_image(prompt, 1024, 1024)
        assert image_url
