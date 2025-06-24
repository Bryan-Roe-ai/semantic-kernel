#!/usr/bin/env python3
"""
AI module for open ai model types

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from enum import Enum


class OpenAIModelTypes(Enum):
    """OpenAI model types, can be text, chat or embedding."""

    TEXT = "text"
    CHAT = "chat"
    EMBEDDING = "embedding"
    TEXT_TO_IMAGE = "text-to-image"
    AUDIO_TO_TEXT = "audio-to-text"
    TEXT_TO_AUDIO = "text-to-audio"
    REALTIME = "realtime"
    RESPONSE = "response"
