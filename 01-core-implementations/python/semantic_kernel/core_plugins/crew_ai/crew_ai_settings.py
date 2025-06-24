#!/usr/bin/env python3
"""
AI module for crew ai settings

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


class CrewAISettings(KernelBaseSettings):
    """The Crew.AI settings.

    Required:
    - endpoint: str - The API endpoint.
    """

    env_prefix: ClassVar[str] = "CREW_AI_"

    endpoint: str
    auth_token: SecretStr
    polling_interval: float = 1.0
    polling_timeout: float = 30.0
