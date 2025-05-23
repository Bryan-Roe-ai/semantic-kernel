# Copyright (c) Microsoft. All rights reserved.

import logging
<<<<<<< HEAD
import sys
<<<<<<< Updated upstream
from typing import Annotated, Any, Literal

from mistralai import utils
=======
from typing import Any, Literal
>>>>>>> Stashed changes

if sys.version_info >= (3, 11):
    pass  # pragma: no cover
else:
    pass  # pragma: no cover

<<<<<<< Updated upstream
from pydantic import Field, field_validator
=======
from pydantic import Field
>>>>>>> Stashed changes
=======
from typing import Annotated, Any, Literal

from mistralai import utils
from pydantic import Field
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

from semantic_kernel.connectors.ai.prompt_execution_settings import (
    PromptExecutionSettings,
)

logger = logging.getLogger(__name__)


class MistralAIPromptExecutionSettings(PromptExecutionSettings):
    """Common request settings for MistralAI services."""

<<<<<<< Updated upstream
    ai_model_id: Annotated[str | None, Field(serialization_alias="model")] = None
=======
    ai_model_id: str | None = Field(None, serialization_alias="model")
>>>>>>> Stashed changes


class MistralAIChatPromptExecutionSettings(MistralAIPromptExecutionSettings):
    """Specific settings for the Chat Completion endpoint."""

    response_format: dict[Literal["type"], Literal["text", "json_object"]] | None = None
    messages: list[dict[str, Any]] | None = None
<<<<<<< HEAD
<<<<<<< Updated upstream
    safe_mode: Annotated[bool, Field(exclude=True)] = False
=======
    safe_mode: Annotated[
        bool,
        Field(
            exclude=True,
            deprecated="The 'safe_mode' setting is no longer supported and is being ignored, "
            "it will be removed in the Future.",
        ),
    ] = False
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    safe_prompt: bool = False
    max_tokens: Annotated[int | None, Field(gt=0)] = None
    seed: int | None = None
    temperature: Annotated[float | None, Field(ge=0.0, le=2.0)] = None
    top_p: Annotated[float | None, Field(ge=0.0, le=1.0)] = None
    random_seed: int | None = None
=======
    safe_mode: bool = False
    safe_prompt: bool = False
    max_tokens: int | None = Field(None, gt=0)
    seed: int | None = None
    temperature: float | None = Field(None, ge=0.0, le=2.0)
    top_p: float | None = Field(None, ge=0.0, le=1.0)
    random_seed: int | None = None
<<<<<<< main
>>>>>>> Stashed changes

    @model_validator(mode="after")
    def check_function_call_behavior(self) -> "MistralAIChatPromptExecutionSettings":
        """Check if the user is requesting function call behavior."""
        if self.function_choice_behavior is not None:
            raise NotImplementedError(
                "MistralAI does not support function call behavior."
            )

        return self
<<<<<<< Updated upstream
    presence_penalty: float | None = Field(None, gt=0)
    frequency_penalty: float | None = Field(None, gt=0)
    n: int | None = Field(None, gt=1)
    retries: utils.RetryConfig | None = None
    server_url: str | None = None
    timeout_ms: int | None = None
=======
=======
>>>>>>> Stashed changes
    tools: list[dict[str, Any]] | None = Field(
        None,
        max_length=64,
        description="Do not set this manually. It is set by the service based on the function choice configuration.",
    )
    tool_choice: str | None = Field(
        None,
        description="Do not set this manually. It is set by the service based on the function choice configuration.",
    )
<<<<<<< Updated upstream
    
    
    
    

    @field_validator("safe_mode")
    @classmethod
    def check_safe_mode(cls, v: bool) -> bool:
        """The safe_mode setting is no longer supported."""
        logger.warning(
            "The 'safe_mode' setting is no longer supported and is being ignored, it will be removed in the Future."
        )
        return v
    presence_penalty: Annotated[float | None, Field(gt=0)] = None
    frequency_penalty: Annotated[float | None, Field(gt=0)] = None
    n: Annotated[int | None, Field(gt=1)] = None
    retries: utils.RetryConfig | None = None
    server_url: str | None = None
    timeout_ms: int | None = None
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
<<<<<<< HEAD

    @field_validator("safe_mode")
    @classmethod
    def check_safe_mode(cls, v: bool) -> bool:
        """The safe_mode setting is no longer supported."""
        logger.warning(
            "The 'safe_mode' setting is no longer supported and is being ignored, it will be removed in the Future."
        )
        return v
=======
<<<<<<< main
    
    
>>>>>>> upstream/main
=======
>>>>>>> microsoft/main
>>>>>>> Stashed changes
=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
