#!/usr/bin/env python3
"""
Test module for rest api operation run options

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.connectors.openapi_plugin.models.rest_api_operation_run_options import (
    RestApiOperationRunOptions,
)

def test_initialization():
    server_url_override = "http://example.com"
    api_host_url = "http://example.com"
    timeout = 30.0

    rest_api_operation_run_options = RestApiOperationRunOptions(
        server_url_override, api_host_url
    )

    rest_api_operation_run_options = RestApiRunOptions(server_url_override, api_host_url, timeout)

    assert rest_api_operation_run_options.server_url_override == server_url_override
    assert rest_api_operation_run_options.api_host_url == api_host_url
    assert rest_api_operation_run_options.timeout == timeout

def test_initialization_no_params():
    rest_api_operation_run_options = RestApiRunOptions()

    assert rest_api_operation_run_options.server_url_override is None
    assert rest_api_operation_run_options.api_host_url is None
