#!/usr/bin/env python3
"""
import asyncio
Hf Text Embedding module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import logging
import sys
from typing import TYPE_CHECKING, Any

if sys.version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

import torch
from numpy import ndarray

from semantic_kernel.connectors.ai.ai_exception import AIException

from semantic_kernel.connectors.ai.embeddings.embedding_generator_base import (
    EmbeddingGeneratorBase,
)
from semantic_kernel.connectors.ai.embedding_generator_base import EmbeddingGeneratorBase
from semantic_kernel.exceptions import ServiceResponseException
from semantic_kernel.utils.feature_stage_decorator import experimental

if TYPE_CHECKING:
    from torch import Tensor

    from semantic_kernel.connectors.ai.prompt_execution_settings import (
        PromptExecutionSettings,
    )


logger: logging.Logger = logging.getLogger(__name__)

@experimental_class
@experimental
class HuggingFaceTextEmbedding(EmbeddingGeneratorBase):
    """Hugging Face text embedding service."""

class HuggingFaceTextEmbedding(EmbeddingGeneratorBase):
class HuggingFaceTextEmbedding(EmbeddingGeneratorBase):
    device: str
    generator: Any

    def __init__(
        self,
        ai_model_id: str,
        device: int = -1,
        service_id: str | None = None,
        device: int = -1,
        service_id: str | None = None,
        device: int = -1,
        service_id: str | None = None,
        device: Optional[int] = -1,
        service_id: Optional[str] = None,
    ) -> None:
        """Initializes a new instance of the HuggingFaceTextEmbedding class.

        Args:
            ai_model_id (str): Hugging Face model card string, see
                https://huggingface.co/sentence-transformers
            device (int): Device to run the model on, -1 for CPU, 0+ for GPU. (optional)
            service_id (str): Service ID for the model. (optional)

        Note that this model will be downloaded from the Hugging Face model hub.
        """
        resolved_device = (
            f"cuda:{device}" if device >= 0 and torch.cuda.is_available() else "cpu"
        )
        resolved_device = (
            f"cuda:{device}" if device >= 0 and torch.cuda.is_available() else "cpu"
        )
        from sentence_transformers import SentenceTransformer
        resolved_device = f"cuda:{device}" if device >= 0 and torch.cuda.is_available() else "cpu"
        super().__init__(
            ai_model_id=ai_model_id,
            service_id=service_id,
            device=resolved_device,

            generator=sentence_transformers.SentenceTransformer(
                model_name_or_path=ai_model_id, device=resolved_device
            generator=sentence_transformers.SentenceTransformer(  # type: ignore
            generator=SentenceTransformer(  # type: ignore
                model_name_or_path=ai_model_id,
                device=resolved_device,
            ),
        )

    @override
    async def generate_embeddings(
        self,
        texts: list[str],
        settings: "PromptExecutionSettings | None" = None,
        **kwargs: Any,
    ) -> ndarray:
        try:
            logger.info(f"Generating embeddings for {len(texts)} texts.")
            return self.generator.encode(
                sentences=texts, convert_to_numpy=True, **kwargs
            )
        except Exception as e:
            raise ServiceResponseException("Hugging Face embeddings failed", e) from e

    @override
    async def generate_raw_embeddings(
        self,
        texts: list[str],
        settings: "PromptExecutionSettings | None" = None,
        **kwargs: Any,
    ) -> "list[Tensor] | ndarray | Tensor":
        try:
            logger.info(f"Generating raw embeddings for {len(texts)} texts.")
            return self.generator.encode(sentences=texts, **kwargs)
        except Exception as e:
            raise ServiceResponseException("Hugging Face embeddings failed", e) from e
