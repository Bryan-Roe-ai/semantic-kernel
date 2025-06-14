# Copyright (c) Microsoft. All rights reserved.

import sys

<<<<<<< HEAD
from semantic_kernel.services.ai_service_client_base import AIServiceClientBase
from semantic_kernel.utils.experimental_decorator import experimental_class

<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
if TYPE_CHECKING:
    from numpy import ndarray

    from semantic_kernel.connectors.ai.prompt_execution_settings import (
        PromptExecutionSettings,
    )
=======
from semantic_kernel.connectors.ai.embedding_generator_base import EmbeddingGeneratorBase as NewEmbeddingGeneratorBase
from semantic_kernel.utils.feature_stage_decorator import experimental
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

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

<<<<<<< HEAD
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
from semantic_kernel.services.ai_service_client_base import AIServiceClientBase

=======
from semantic_kernel.services.ai_service_client_base import AIServiceClientBase

>>>>>>> origin/main
=======
=======
from semantic_kernel.services.ai_service_client_base import AIServiceClientBase

>>>>>>> Stashed changes
=======
=======
from semantic_kernel.services.ai_service_client_base import AIServiceClientBase

<<<<<<< div
=======
from semantic_kernel.services.ai_service_client_base import AIServiceClientBase

>>>>>>> main
=======
>>>>>>> Stashed changes
>>>>>>> head
if TYPE_CHECKING:
    from numpy import ndarray

    from semantic_kernel.connectors.ai.prompt_execution_settings import (
        PromptExecutionSettings,
    )


@experimental_class
class EmbeddingGeneratorBase(AIServiceClientBase, ABC):
    """Base class for embedding generators."""

class EmbeddingGeneratorBase(AIServiceClientBase, ABC):
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> origin/main
>>>>>>> head
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
=======
    pass
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
