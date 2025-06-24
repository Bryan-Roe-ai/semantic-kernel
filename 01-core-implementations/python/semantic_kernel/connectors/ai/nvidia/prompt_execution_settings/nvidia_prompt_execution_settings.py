#!/usr/bin/env python3
"""
Nvidia Prompt Execution Settings module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import Annotated, Any, Literal

from pydantic import Field

from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings


class NvidiaPromptExecutionSettings(PromptExecutionSettings):
    """Settings for NVIDIA prompt execution."""

    format: Literal["json"] | None = None
    options: dict[str, Any] | None = None

    def prepare_settings_dict(self, **kwargs) -> dict[str, Any]:
        """Prepare the settings as a dictionary for sending to the AI service.

        By default, this method excludes the service_id and extension_data fields.
        As well as any fields that are None.
        """
        return self.model_dump(
            exclude={"service_id", "extension_data", "structured_json_response", "input_type", "truncate"},
            exclude_none=True,
            by_alias=True,
        )


class NvidiaEmbeddingPromptExecutionSettings(NvidiaPromptExecutionSettings):
    """Settings for NVIDIA embedding prompt execution."""

    input: str | list[str] | None = None
    ai_model_id: Annotated[str | None, Field(serialization_alias="model")] = None
    encoding_format: Literal["float", "base64"] = "float"
    truncate: Literal["NONE", "START", "END"] = "NONE"
    input_type: Literal["passage", "query"] = "query"  # required param with default value query
    user: str | None = None
    extra_headers: dict | None = None
    extra_body: dict | None = None
    timeout: float | None = None
    dimensions: Annotated[int | None, Field(gt=0)] = None
