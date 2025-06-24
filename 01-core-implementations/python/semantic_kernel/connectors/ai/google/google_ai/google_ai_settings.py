#!/usr/bin/env python3
"""
AI module for google ai settings

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

from pydantic import SecretStr

from semantic_kernel.kernel_pydantic import KernelBaseSettings


class GoogleAISettings(KernelBaseSettings):
    """Google AI settings.

    The settings are first loaded from environment variables with
    the prefix 'GOOGLE_AI_'.
    If the environment variables are not found, the settings can
    be loaded from a .env file with the encoding 'utf-8'.
    If the settings are not found in the .env file, the settings
    are ignored; however, validation will fail alerting that the
    settings are missing.

    Required settings for prefix 'GOOGLE_AI_' are:
    - gemini_model_id: str - The Gemini model ID for the Google AI service, i.e. gemini-1.5-pro
                This value can be found in the Google AI service deployment.
                (Env var GOOGLE_AI_GEMINI_MODEL_ID)
    - embedding_model_id: str - The embedding model ID for the Google AI service, i.e. text-embedding-004
                This value can be found in the Google AI service deployment.
                (Env var GOOGLE_AI_EMBEDDING_MODEL_ID)
    - api_key: SecretStr - The API key for the Google AI service deployment.
                This value can be found in the Google AI service deployment.
                (Env var GOOGLE_AI_API_KEY)
    """

    env_prefix: ClassVar[str] = "GOOGLE_AI_"

    gemini_model_id: str | None = None
    embedding_model_id: str | None = None
    api_key: SecretStr
