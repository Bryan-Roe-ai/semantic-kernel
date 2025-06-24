#!/usr/bin/env python3
"""
Test module for rest api uri

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.connectors.openapi_plugin.models.rest_api_uri import Uri


def test_uri_initialization():
    test_uri = "https://example.com/path?query=param"
    uri_instance = Uri(test_uri)
    assert uri_instance.uri == test_uri


def test_get_left_part():
    test_uri = "https://example.com/path?query=param"
    expected_left_part = "https://example.com"
    uri_instance = Uri(test_uri)
    assert uri_instance.get_left_part() == expected_left_part


def test_get_left_part_no_scheme():
    test_uri = "example.com/path?query=param"
    expected_left_part = "://"
    uri_instance = Uri(test_uri)
    assert uri_instance.get_left_part() == expected_left_part


def test_get_left_part_no_netloc():
    test_uri = "https:///path?query=param"
    expected_left_part = "https://"
    uri_instance = Uri(test_uri)
    assert uri_instance.get_left_part() == expected_left_part
