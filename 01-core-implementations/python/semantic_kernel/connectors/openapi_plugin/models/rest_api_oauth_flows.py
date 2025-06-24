#!/usr/bin/env python3
"""
Rest Api Oauth Flows module

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

from semantic_kernel.connectors.openapi_plugin.models.rest_api_oauth_flow import RestApiOAuthFlow
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
@dataclass
class RestApiOAuthFlows:
    """Represents the OAuth flows used by the REST API."""

    implicit: RestApiOAuthFlow | None = None
    password: RestApiOAuthFlow | None = None
    client_credentials: RestApiOAuthFlow | None = None
    authorization_code: RestApiOAuthFlow | None = None
