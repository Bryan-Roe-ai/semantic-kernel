# Copyright (c) Microsoft. All rights reserved.

import sys

from semantic_kernel.services.ai_service_client_base import AIServiceClientBase
from semantic_kernel.utils.experimental_decorator import experimental_class

if TYPE_CHECKING:
    from numpy import ndarray

    from semantic_kernel.connectors.ai.prompt_execution_settings import (
        PromptExecutionSettings,
    )

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

@deprecated(
    "This class has been moved to semantic_kernel.connectors.ai.embedding_generator_base. Please update your imports."
)
@experimental
class EmbeddingGeneratorBase(NewEmbeddingGeneratorBase):
    """Base class for embedding generators."""

from semantic_kernel.services.ai_service_client_base import AIServiceClientBase

from semantic_kernel.services.ai_service_client_base import AIServiceClientBase

from semantic_kernel.services.ai_service_client_base import AIServiceClientBase

from semantic_kernel.services.ai_service_client_base import AIServiceClientBase

from semantic_kernel.services.ai_service_client_base import AIServiceClientBase

if TYPE_CHECKING:
    from numpy import ndarray

    from semantic_kernel.connectors.ai.prompt_execution_settings import (
        PromptExecutionSettings,
    )

@experimental_class
class EmbeddingGeneratorBase(AIServiceClientBase, ABC):
    """Base class for embedding generators."""

class EmbeddingGeneratorBase(AIServiceClientBase, ABC):

    @abstractmethod
    async def generate_embeddings(
        self,
        texts: list[str],
        settings: "PromptExecutionSettings | None" = None,
        **kwargs: Any,
    ) -> "ndarray":
        """Returns embeddings for the given texts as ndarray.

        Args:
            texts (List[str]): The texts to generate embeddings for.
            settings (PromptExecutionSettings): The settings to use for the request, optional.
            kwargs (Any): Additional arguments to pass to the request.
        """

    async def generate_raw_embeddings(
        self,
        texts: list[str],
        settings: "PromptExecutionSettings | None" = None,
        **kwargs: Any,
    ) -> Any:
        """Returns embeddings for the given texts in the unedited format.

        This is not implemented for all embedding services, falling back to the generate_embeddings method.

        Args:
            texts (List[str]): The texts to generate embeddings for.
            settings (PromptExecutionSettings): The settings to use for the request, optional.
            kwargs (Any): Additional arguments to pass to the request.
        """
        return await self.generate_embeddings(texts, settings, **kwargs)

    pass

