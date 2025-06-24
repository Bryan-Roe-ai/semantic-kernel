#!/usr/bin/env python3
"""
Bedrock Action Group Model module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from pydantic import ConfigDict, Field

from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class BedrockActionGroupModel(KernelBaseModel):
    """Bedrock Action Group Model.

    Model field definitions for the Amazon Bedrock Action Group Service:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/client/create_agent_action_group.html
    """

    # This model_config will merge with the KernelBaseModel.model_config
    model_config = ConfigDict(extra="allow")

    action_group_id: str = Field(..., alias="actionGroupId", description="The unique identifier of the action group.")
    action_group_name: str = Field(..., alias="actionGroupName", description="The name of the action group.")
