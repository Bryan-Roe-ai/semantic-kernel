#!/usr/bin/env python3
"""
Test module for bedrock agent status

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

from semantic_kernel.agents.bedrock.models.bedrock_agent_status import BedrockAgentStatus


def test_bedrock_agent_status_values():
    """Test case to verify the values of BedrockAgentStatus enum."""
    assert BedrockAgentStatus.CREATING == "CREATING"
    assert BedrockAgentStatus.PREPARING == "PREPARING"
    assert BedrockAgentStatus.PREPARED == "PREPARED"
    assert BedrockAgentStatus.NOT_PREPARED == "NOT_PREPARED"
    assert BedrockAgentStatus.DELETING == "DELETING"
    assert BedrockAgentStatus.FAILED == "FAILED"
    assert BedrockAgentStatus.VERSIONING == "VERSIONING"
    assert BedrockAgentStatus.UPDATING == "UPDATING"


def test_bedrock_agent_status_invalid_value():
    """Test case to verify error handling for invalid BedrockAgentStatus value."""
    with pytest.raises(ValueError):
        BedrockAgentStatus("INVALID_STATUS")
