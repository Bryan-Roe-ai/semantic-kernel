#!/usr/bin/env python3
"""
Bedrock Base module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from abc import ABC
from typing import Any, ClassVar

import boto3

from semantic_kernel.kernel_pydantic import KernelBaseModel


class BedrockBase(KernelBaseModel, ABC):
    """Amazon Bedrock Service Base Class."""

    MODEL_PROVIDER_NAME: ClassVar[str] = "bedrock"

    # Amazon Bedrock Clients
    # Runtime Client: Use for inference
    bedrock_runtime_client: Any
    # Client: Use for model management
    bedrock_client: Any

    def __init__(
        self,
        *,
        runtime_client: Any | None = None,
        client: Any | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the Amazon Bedrock Base Class.

        Args:
            runtime_client: The Amazon Bedrock runtime client to use.
            client: The Amazon Bedrock client to use.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(
            bedrock_runtime_client=runtime_client or boto3.client("bedrock-runtime"),
            bedrock_client=client or boto3.client("bedrock"),
            **kwargs,
        )
