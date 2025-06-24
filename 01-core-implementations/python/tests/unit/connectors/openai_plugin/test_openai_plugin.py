#!/usr/bin/env python3
"""
Test module for openai plugin

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


import pytest

from semantic_kernel.connectors.openai_plugin.openai_utils import OpenAIUtils
from semantic_kernel.exceptions import PluginInitializationError


def test_parse_openai_manifest_for_openapi_spec_url_valid():
    plugin_json = {
        "api": {"type": "openapi", "url": "https://example.com/openapi.json"}
    }
    result = OpenAIUtils.parse_openai_manifest_for_openapi_spec_url(plugin_json)
    assert result == "https://example.com/openapi.json"


def test_parse_openai_manifest_for_openapi_spec_url_missing_api_type():
    plugin_json = {"api": {}}
    with pytest.raises(
        PluginInitializationError, match="OpenAI manifest is missing the API type."
    ):
        OpenAIUtils.parse_openai_manifest_for_openapi_spec_url(plugin_json)


def test_parse_openai_manifest_for_openapi_spec_url_invalid_api_type():
    plugin_json = {"api": {"type": "other", "url": "https://example.com/openapi.json"}}
    with pytest.raises(
        PluginInitializationError, match="OpenAI manifest is not of type OpenAPI."
    ):
        OpenAIUtils.parse_openai_manifest_for_openapi_spec_url(plugin_json)


def test_parse_openai_manifest_for_openapi_spec_url_missing_url():
    plugin_json = {"api": {"type": "openapi"}}
    with pytest.raises(
        PluginInitializationError,
        match="OpenAI manifest is missing the OpenAPI Spec URL.",
    ):
        OpenAIUtils.parse_openai_manifest_for_openapi_spec_url(plugin_json)
