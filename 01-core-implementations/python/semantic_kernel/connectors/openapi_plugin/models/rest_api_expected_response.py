#!/usr/bin/env python3
"""
Rest Api Expected Response module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.utils.feature_stage_decorator import experimental

@experimental
class RestApiExpectedResponse:
    """RestApiExpectedResponse."""

    def __init__(
        self, description: str, media_type: str, schema: dict[str, str] | None = None
    ):
        """Initialize the RestApiOperationExpectedResponse."""

        self.description = description
        self.media_type = media_type
        self.schema = schema
