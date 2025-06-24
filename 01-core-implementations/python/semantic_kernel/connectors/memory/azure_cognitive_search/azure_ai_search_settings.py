#!/usr/bin/env python3
"""
AI module for azure ai search settings

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import ClassVar

from pydantic import SecretStr

from semantic_kernel.kernel_pydantic import HttpsUrl, KernelBaseSettings
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class AzureAISearchSettings(KernelBaseSettings):
    """Azure AI Search model settings currently used by the AzureCognitiveSearchMemoryStore connector.

    Args:
    - api_key: SecretStr - Azure AI Search API key (Env var AZURE_AI_SEARCH_API_KEY)
    - endpoint: HttpsUrl - Azure AI Search endpoint (Env var AZURE_AI_SEARCH_ENDPOINT)
    - index_name: str - Azure AI Search index name (Env var AZURE_AI_SEARCH_INDEX_NAME)
    """

    env_prefix: ClassVar[str] = "AZURE_AI_SEARCH_"

    api_key: SecretStr | None = None
    endpoint: HttpsUrl
    index_name: str | None = None

    def model_dump(self) -> dict[str, str]:
        """Dump the model to a dictionary."""
        data = super().model_dump()
        data.update(
            {
                "api_key": self.api_key.get_secret_value(),
                "endpoint": str(self.endpoint),
            }
        )
        return data
