#!/usr/bin/env python3
"""
Bedrock Agent Status module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


from enum import Enum

from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class BedrockAgentStatus(str, Enum):
    """Bedrock Agent Status.

    https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PrepareAgent.html#API_agent_PrepareAgent_ResponseElements
    """

    CREATING = "CREATING"
    PREPARING = "PREPARING"
    PREPARED = "PREPARED"
    NOT_PREPARED = "NOT_PREPARED"
    DELETING = "DELETING"
    FAILED = "FAILED"
    VERSIONING = "VERSIONING"
    UPDATING = "UPDATING"
