#!/usr/bin/env python3
"""Memory Store Base module.

Defines the abstract interface for concrete memory/vector store connectors.

NOTE: This class is currently marked deprecated and will be removed in a future
version in favor of newer store abstractions. Do not add new functionality
here; create a dedicated store implementation instead.
"""

# Copyright (c) Microsoft. All rights reserved.

import sys
from abc import ABC, abstractmethod

try:  # pragma: no cover - defensive import
    from numpy import ndarray  # type: ignore
except ImportError:  # pragma: no cover

    class ndarray:  # type: ignore
        """Fallback ndarray placeholder when numpy is unavailable."""

        __slots__ = ()


from semantic_kernel.memory.memory_record import MemoryRecord

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated


@deprecated("This class will be removed in a future version.")
class MemoryStoreBase(ABC):
    """Base class for memory store."""

    async def __aenter__(self):
        """Enter the context manager."""
        return self

    async def __aexit__(self, *args):
        """Exit the context manager."""
        await self.close()

    async def close(self):
        """Close the connection."""

    @abstractmethod
    async def create_collection(self, collection_name: str) -> None:
        """Creates a new collection in the data store.

        Args:
            collection_name (str): The name associated with a collection of
                embeddings.
        """

    @abstractmethod
    async def get_collections(
        self,
    ) -> list[str]:
        """Gets all collection names in the data store.

        Returns:
            List[str]: A group of collection names.
        """

    @abstractmethod
    async def delete_collection(self, collection_name: str) -> None:
        """Deletes a collection from the data store.

        Args:
            collection_name (str): The name associated with a collection of
                embeddings.
        """

    @abstractmethod
    async def does_collection_exist(self, collection_name: str) -> bool:
        """Determines if a collection exists in the data store.

        Args:
            collection_name (str): The name associated with a collection of
                embeddings.

        Returns:
            bool: True if given collection exists, False if not.
        """

    @abstractmethod
    async def upsert(self, collection_name: str, record: MemoryRecord) -> str:
        """Upserts a memory record into the data store.

        Does not guarantee that the collection exists. If the record already
        exists, it will be updated. If the record does not exist, it will be
        created.

        Args:
            collection_name (str): The name associated with a collection of
                embeddings.
            record (MemoryRecord): The memory record to upsert.

        Returns:
            str: The unique identifier for the memory record.
        """

    @abstractmethod
    async def upsert_batch(
        self, collection_name: str, records: list[MemoryRecord]
    ) -> list[str]:
        """Upserts a group of memory records into the data store.

        Does not guarantee that the collection exists. If the record already
        exists, it will be updated. If the record does not exist, it will be
        created.

        Args:
            collection_name (str): The name associated with a collection of
                embeddings.
            records (MemoryRecord): The memory records to upsert.

        Returns:
            List[str]: The unique identifiers for the memory records.
        """

    @abstractmethod
    async def get(
        self, collection_name: str, key: str, with_embedding: bool
    ) -> MemoryRecord:
        """Gets a memory record from the data store.

        Does not guarantee that the collection exists.

        Args:
            collection_name (str): The name associated with a collection of
                embeddings.
            key (str): The unique id associated with the memory record to get.
            with_embedding (bool): If true, the embedding will be returned in
                the memory record.

        Returns:
            MemoryRecord: The memory record if found.
        """

    @abstractmethod
    async def get_batch(
        self,
        collection_name: str,
        keys: list[str],
        with_embeddings: bool,
    ) -> list[MemoryRecord]:
        """Gets a batch of memory records from the data store.

        Does not guarantee that the collection exists.

        Args:
            collection_name (str): The name associated with a collection of
                embeddings.
            keys (List[str]): The unique ids of the memory records to get.
            with_embeddings (bool): If true, the embedding will be returned in
                the memory records.

        Returns:
            List[MemoryRecord]: The memory records for the keys provided.
        """

    @abstractmethod
    async def remove(self, collection_name: str, key: str) -> None:
        """Removes a memory record from the data store.

        Does not guarantee that the collection exists.

        Args:
            collection_name (str): The name associated with a collection of
                embeddings.
            key (str): The unique id of the memory record to remove.
        """

    @abstractmethod
    async def remove_batch(self, collection_name: str, keys: list[str]) -> None:
        """Removes a batch of memory records from the data store.

        Does not guarantee that the collection exists.

        Args:
            collection_name (str): The name associated with a collection of
                embeddings.
            keys (List[str]): The unique ids of the memory records to remove.
        """

    @abstractmethod
    async def get_nearest_matches(
        self,
        collection_name: str,
        embedding: ndarray,
        limit: int,
        min_relevance_score: float,
        with_embeddings: bool,
    ) -> list[tuple[MemoryRecord, float]]:
        """Gets nearest matches to an embedding.

        Does not guarantee that the collection exists.

        Args:
            collection_name (str): The name associated with a collection of
                embeddings.
            embedding (ndarray): Embedding to compare against the collection.
            limit (int): Max number of similarity results to return.
            min_relevance_score (float): Minimum relevance threshold.
            with_embeddings (bool): If true, embeddings are returned.

        Returns:
            List[Tuple[MemoryRecord, float]]: Tuples of record and score.
        """

    @abstractmethod
    async def get_nearest_match(
        self,
        collection_name: str,
        embedding: ndarray,
        min_relevance_score: float,
        with_embedding: bool,
    ) -> tuple[MemoryRecord, float]:
        """Gets the single nearest match to an embedding.

        Does not guarantee the collection exists.

        Args:
            collection_name (str): Name of the embeddings collection.
            embedding (ndarray): Embedding to compare against stored items.
            min_relevance_score (float): Minimum relevance threshold.
            with_embedding (bool): Whether to include embedding.

        Returns:
            Tuple[MemoryRecord, float]: (record, similarity score) or None.
        """


##
# The block above originally redefined MemoryStoreBase and wiped the abstract
# API. Duplicate removed to preserve legacy interface for connectors.
##
