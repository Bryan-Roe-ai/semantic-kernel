#!/usr/bin/env python3
"""
AI module for google ai base

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

from semantic_kernel.connectors.ai.google.google_ai.google_ai_settings import (
    GoogleAISettings,
)
from semantic_kernel.kernel_pydantic import KernelBaseModel


class GoogleAIBase(KernelBaseModel, ABC):
    """Google AI Service."""

    MODEL_PROVIDER_NAME: ClassVar[str] = "googleai"

    service_settings: GoogleAISettings
