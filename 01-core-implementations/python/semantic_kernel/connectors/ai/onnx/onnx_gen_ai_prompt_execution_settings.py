#!/usr/bin/env python3
"""
AI module for onnx gen ai prompt execution settings

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


from typing import Annotated

from pydantic import Field

from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings


class OnnxGenAIPromptExecutionSettings(PromptExecutionSettings):
    """OnnxGenAI prompt execution settings."""

    diversity_penalty: Annotated[float | None, Field(ge=0.0, le=1.0)] = None
    do_sample: bool = False
    early_stopping: bool = True
    length_penalty: Annotated[float | None, Field(ge=0.0, le=1.0)] = None
    max_length: Annotated[int, Field(gt=0)] = 3072
    min_length: Annotated[int | None, Field(gt=0)] = None
    no_repeat_ngram_size: int = 0
    num_beams: Annotated[int | None, Field(gt=0)] = None
    num_return_sequences: Annotated[int | None, Field(gt=0)] = None
    past_present_share_buffer: int = True
    repetition_penalty: Annotated[float | None, Field(ge=0.0, le=1.0)] = None
    temperature: Annotated[float | None, Field(ge=0.0, le=2.0)] = None
    top_k: Annotated[int | None, Field(gt=0)] = None
    top_p: Annotated[float | None, Field(ge=0.0, le=1.0)] = None
