#!/usr/bin/env python3
"""
Rest Api Oauth Flow module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from dataclasses import dataclass

from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
@dataclass
class RestApiOAuthFlow:
    """Represents the OAuth flow used by the REST API."""

    authorization_url: str
    token_url: str
    scopes: dict[str, str]
    refresh_url: str | None = None
