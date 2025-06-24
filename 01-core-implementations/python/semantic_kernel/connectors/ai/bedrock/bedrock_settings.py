#!/usr/bin/env python3
"""
Bedrock Settings module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import ClassVar

from semantic_kernel.kernel_pydantic import KernelBaseSettings
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class BedrockSettings(KernelBaseSettings):
    """Amazon Bedrock service settings.

    The settings are first loaded from environment variables with
    the prefix 'BEDROCK_'.
    If the environment variables are not found, the settings can
    be loaded from a .env file with the encoding 'utf-8'.
    If the settings are not found in the .env file, the settings
    are ignored; however, validation will fail alerting that the
    settings are missing.

    Optional settings for prefix 'BEDROCK_' are:
        - chat_model_id: str | None - The Amazon Bedrock chat model ID to use.
            (Env var BEDROCK_CHAT_MODEL_ID)
        - text_model_id: str | None - The Amazon Bedrock text model ID to use.
            (Env var BEDROCK_TEXT_MODEL_ID)
        - embedding_model_id: str | None - The Amazon Bedrock embedding model ID to use.
            (Env var BEDROCK_EMBEDDING_MODEL_ID)
    """

    env_prefix: ClassVar[str] = "BEDROCK_"

    chat_model_id: str | None = None
    text_model_id: str | None = None
    embedding_model_id: str | None = None
