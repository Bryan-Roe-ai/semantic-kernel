# Copyright (c) Microsoft. All rights reserved.

import logging
from typing import Annotated, Any

from pydantic import Field, model_validator

from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceType
from semantic_kernel.connectors.ai.function_choice_type import FunctionChoiceType
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.exceptions import ServiceInvalidExecutionSettingsError

from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.exceptions import ServiceInvalidExecutionSettingsError

logger = logging.getLogger(__name__)

class AnthropicPromptExecutionSettings(PromptExecutionSettings):
    """Common request settings for Anthropic services."""

    ai_model_id: Annotated[str | None, Field(serialization_alias="model")] = None

class AnthropicChatPromptExecutionSettings(AnthropicPromptExecutionSettings):
    """Specific settings for the Chat Completion endpoint."""

    messages: list[dict[str, Any]] | None = None
    stream: bool | None = None
    system: str | None = None
    max_tokens: int | None = Field(None, gt=0)
    max_tokens: int = Field(default=1024, gt=0)
    max_tokens: int = Field(default=1024, gt=0)
    max_tokens: int = Field(default=1024, gt=0)
    max_tokens: int = Field(default=1024, gt=0)
    temperature: float | None = Field(None, ge=0.0, le=2.0)
    stop_sequences: list[str] | None = None
    top_p: float | None = Field(None, ge=0.0, le=1.0)
    top_k: int | None = Field(None, ge=0)
    tools: list[dict[str, Any]] | None = Field(
        None,
        max_length=64,
        description=("Do not set this manually. It is set by the service based on the function choice configuration."),
    )
    tool_choice: dict[str, str] | None = Field(
        None,
        description="Do not set this manually. It is set by the service based on the function choice configuration.",
    )
    max_tokens: Annotated[int, Field(gt=0)] = 1024
    temperature: Annotated[float | None, Field(ge=0.0, le=2.0)] = None
    stop_sequences: list[str] | None = None
    top_p: Annotated[float | None, Field(ge=0.0, le=1.0)] = None
    top_k: Annotated[int | None, Field(ge=0)] = None
    tools: Annotated[
        list[dict[str, Any]] | None,
        Field(
            description=(
                "Do not set this manually. It is set by the service based on the function choice configuration."
            ),
        ),
    ] = None
    tool_choice: Annotated[
        dict[str, str] | None,
        Field(
            description="Do not set this manually. It is set by the service based on the function choice configuration."
        ),
    ] = None

    @model_validator(mode="after")
    def check_function_call_behavior(self) -> "AnthropicChatPromptExecutionSettings":
        """Check if the user is requesting function call behavior."""
        if self.function_choice_behavior is not None:
            raise NotImplementedError("Anthropic does not support function call behavior.")

    def validate_tool_choice(self) -> "AnthropicChatPromptExecutionSettings":
        """Validate tool choice. Anthropic doesn't support NONE tool choice."""
        tool_choice = self.tool_choice

        if tool_choice and tool_choice.get("type") == FunctionChoiceType.NONE.value:
            raise ServiceInvalidExecutionSettingsError("Tool choice 'none' is not supported by Anthropic.")

        return self
