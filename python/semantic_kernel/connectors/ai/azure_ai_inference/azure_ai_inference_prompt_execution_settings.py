# Copyright (c) Microsoft. All rights reserved.

from typing import Any, Literal
from typing import Literal
from typing import Annotated, Any, Literal

from pydantic import Field

<<<<<<< HEAD
from semantic_kernel.connectors.ai.prompt_execution_settings import (
    PromptExecutionSettings,
)
from semantic_kernel.utils.experimental_decorator import experimental_class
=======
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.utils.feature_stage_decorator import experimental
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e


@experimental
class AzureAIInferencePromptExecutionSettings(PromptExecutionSettings):
    """Azure AI Inference Prompt Execution Settings.

    Note:
        `extra_parameters` is a dictionary to pass additional model-specific parameters to the model.
    """

    frequency_penalty: Annotated[float | None, Field(ge=-2.0, le=2.0)] = None
    max_tokens: Annotated[int | None, Field(gt=0)] = None
    presence_penalty: Annotated[float | None, Field(ge=-2.0, le=2.0)] = None
    seed: int | None = None
    stop: str | None = None
    temperature: Annotated[float | None, Field(ge=0.0, le=1.0)] = None
    top_p: Annotated[float | None, Field(ge=0.0, le=1.0)] = None
    extra_parameters: dict[str, Any] | None = None
    extra_parameters: dict[str, str] | None = None


<<<<<<< HEAD
@experimental_class
class AzureAIInferenceChatPromptExecutionSettings(
    AzureAIInferencePromptExecutionSettings
):
=======
@experimental
class AzureAIInferenceChatPromptExecutionSettings(AzureAIInferencePromptExecutionSettings):
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    """Azure AI Inference Chat Prompt Execution Settings."""

    tools: Annotated[
        list[dict[str, Any]] | None,
        Field(
            description="Do not set this manually. It is set by the service based "
            "on the function choice configuration.",
        ),
    ] = None
    tool_choice: Annotated[
        str | None,
        Field(
            description="Do not set this manually. It is set by the service based "
            "on the function choice configuration.",
        ),
    ] = None


@experimental
class AzureAIInferenceEmbeddingPromptExecutionSettings(PromptExecutionSettings):
    """Azure AI Inference Embedding Prompt Execution Settings.

    Note:
        `extra_parameters` is a dictionary to pass additional model-specific parameters to the model.
    """

    dimensions: int | None = Field(None, gt=0)
    encoding_format: (
        Literal["base64", "binary", "float", "int8", "ubinary", "uint8"] | None
    ) = None
    dimensions: Annotated[int | None, Field(gt=0)] = None
    encoding_format: Literal["base64", "binary", "float", "int8", "ubinary", "uint8"] | None = None
    input_type: Literal["text", "query", "document"] | None = None
    extra_parameters: dict[str, str] | None = None
