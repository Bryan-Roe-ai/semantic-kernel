#!/usr/bin/env python3
"""
Rest Api Security Requirement module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.connectors.openapi_plugin.models.rest_api_security_scheme import RestApiSecurityScheme
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class RestApiSecurityRequirement(dict[RestApiSecurityScheme, list[str]]):
    """Represents the security requirements used by the REST API."""

    def __init__(self, dictionary: dict[RestApiSecurityScheme, list[str]]):
        """Initializes a new instance of the RestApiSecurityRequirement class."""
        super().__init__(dictionary)
