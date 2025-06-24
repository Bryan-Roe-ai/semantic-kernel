#!/usr/bin/env python3
"""
Rest Api Uri module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from urllib.parse import urlparse

from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class Uri:
    """The Uri class that represents the URI."""

    def __init__(self, uri):
        """Initialize the Uri."""
        self.uri = uri

    def get_left_part(self):
        """Get the left part of the URI."""
        parsed_uri = urlparse(self.uri)
        return f"{parsed_uri.scheme}://{parsed_uri.netloc}"
