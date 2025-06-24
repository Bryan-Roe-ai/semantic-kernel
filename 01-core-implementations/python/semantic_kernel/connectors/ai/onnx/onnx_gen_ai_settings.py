#!/usr/bin/env python3
"""
AI module for onnx gen ai settings

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


class OnnxGenAISettings(KernelBaseSettings):
    """Onnx Gen AI model settings.

    The settings are first loaded from environment variables with the prefix 'ONNX_GEN_AI_'. If the
    environment variables are not found, the settings can be loaded from a .env file with the
    encoding 'utf-8'. If the settings are not found in the .env file, the settings are ignored;
    however, validation will fail alerting that the settings are missing.

    Optional settings for prefix 'ONNX_GEN_AI_' are:
    - chat_model_folder: Path to the Onnx chat model folder (ENV: ONNX_GEN_AI_CHAT_MODEL_FOLDER).
    - text_model_folder: Path to the Onnx text model folder (ENV: ONNX_GEN_AI_TEXT_MODEL_FOLDER).
    """

    env_prefix: ClassVar[str] = "ONNX_GEN_AI_"
    chat_model_folder: str | None = None
    text_model_folder: str | None = None
