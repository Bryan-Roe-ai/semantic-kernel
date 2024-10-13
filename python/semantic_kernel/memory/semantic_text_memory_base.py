# Copyright (c) Microsoft. All rights reserved.

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, TypeVar

from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.utils.experimental_decorator import experimental_class

if TYPE_CHECKING:
    from semantic_kernel.memory.memory_query_result import MemoryQueryResult

SemanticTextMemoryT = TypeVar("SemanticTextMemoryT", bound="SemanticTextMemoryBase")


@experimental_class
class SemanticTextMemoryBase(KernelBaseModel):
    """Base class for semantic text memory."""

    @abstractmethod
    async def save_information(
from abc import ABC, abstractmethod
from typing import List, Optional

from semantic_kernel.memory.memory_query_result import MemoryQueryResult


class SemanticTextMemoryBase(ABC):
    @abstractmethod
    async def save_information_async(
        self,
        collection: str,
        text: str,
        id: str,
        description: str | None = None,
        additional_metadata: str | None = None,
        embeddings_kwargs: dict[str, Any] | None = None,
    ) -> None:
        """Save information to the memory (calls the memory store's upsert method).

        Args:
            collection (str): The collection to save the information to.
            text (str): The text to save.
            id (str): The id of the information.
            description (Optional[str]): The description of the information.
            additional_metadata (Optional[str]): Additional metadata of the information.
            embeddings_kwargs (Optional[Dict[str, Any]]): The embeddings kwargs of the information.

        """

    @abstractmethod
    async def save_reference(
        description: Optional[str] = None,
        # TODO: ctoken?
    ) -> None:
        pass

    @abstractmethod
    async def save_reference_async(
        self,
        collection: str,
        text: str,
        external_id: str,
        external_source_name: str,
        description: str | None = None,
        additional_metadata: str | None = None,
    ) -> None:
        """Save a reference to the memory (calls the memory store's upsert method).

        Args:
            collection (str): The collection to save the reference to.
            text (str): The text to save.
            external_id (str): The external id of the reference.
            external_source_name (str): The external source name of the reference.
            description (Optional[str]): The description of the reference.
            additional_metadata (Optional[str]): Additional metadata of the reference.

        """

    @abstractmethod
    async def get(
        self,
        collection: str,
        key: str,
<<<<<<< div
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    ) -> "MemoryQueryResult | None":
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
    ) -> "MemoryQueryResult | None":
=======
=======
>>>>>>> main
<<<<<<< main
    ) -> "MemoryQueryResult | None":
=======
        # TODO: with_embedding: bool,
    ) -> Optional[MemoryQueryResult]:
>>>>>>> ms/small_fixes
<<<<<<< div
>>>>>>> origin/main
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
>>>>>>> main
        """Get information from the memory (calls the memory store's get method).

        Args:
            collection (str): The collection to get the information from.
            key (str): The key of the information.

        Returns:
            Optional[MemoryQueryResult]: The MemoryQueryResult if found, None otherwise.
        """

    @abstractmethod
    async def search(
        description: Optional[str] = None,
        # TODO: ctoken?
    ) -> None:
        pass

    @abstractmethod
    async def get_async(
        self,
        collection: str,
        query: str,  # TODO: ctoken?
    ) -> Optional[MemoryQueryResult]:
        pass

    @abstractmethod
    async def search_async(
        self,
        collection: str,
        query: str,
        limit: int = 1,
        min_relevance_score: float = 0.7,
    ) -> list["MemoryQueryResult"]:
        """Search the memory (calls the memory store's get_nearest_matches method).

        Args:
            collection (str): The collection to search in.
            query (str): The query to search for.
            limit (int): The maximum number of results to return. (default: {1})
            min_relevance_score (float): The minimum relevance score to return. (default: {0.0})
            with_embeddings (bool): Whether to return the embeddings of the results. (default: {False})

        Returns:
            List[MemoryQueryResult]: The list of MemoryQueryResult found.
        """

    @abstractmethod
    async def get_collections(self) -> list[str]:
        """Get the list of collections in the memory (calls the memory store's get_collections method).

        Returns:
            List[str]: The list of all the memory collection names.
        """
        # TODO: ctoken?
    ) -> List[MemoryQueryResult]:
        pass

    @abstractmethod
    async def get_collections_async(self) -> List[str]:
        pass
