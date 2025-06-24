#!/usr/bin/env python3
"""
AI module for open ai text to audio execution settings

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import logging
from typing import Annotated, Literal

from pydantic import Field

from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings

logger = logging.getLogger(__name__)


class OpenAITextToAudioExecutionSettings(PromptExecutionSettings):
    """Request settings for OpenAI text to audio services."""

    ai_model_id: str | None = Field(None, serialization_alias="model")
    input: str | None = Field(
        None, description="Do not set this manually. It is set by the service based on the text content."
    )
    voice: Literal["alloy", "ash", "ballad", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer"] = "alloy"
    response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] | None = None
    speed: Annotated[float | None, Field(ge=0.25, le=4.0)] = None
