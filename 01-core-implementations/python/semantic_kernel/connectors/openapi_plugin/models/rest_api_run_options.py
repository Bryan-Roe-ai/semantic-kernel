#!/usr/bin/env python3
"""
Rest Api Run Options module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


class RestApiRunOptions:
    """The options for running the REST API operation."""

    def __init__(
        self, server_url_override: str | None = None, api_host_url: str | None = None, timeout: float | None = None
    ) -> None:
        """Initialize the REST API operation run options.

        Args:
            server_url_override: The server URL override, if any.
            api_host_url: The API host URL, if any.
            timeout: The timeout for the operation, if any.
        """
        self.server_url_override: str | None = server_url_override
        self.api_host_url: str | None = api_host_url
        self.timeout: float | None = timeout
