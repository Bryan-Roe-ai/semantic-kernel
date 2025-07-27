#!/usr/bin/env python3
"""Persistent Memory Store using pickle for storage."""

import os
import pickle
import logging
from typing import List


from semantic_kernel.memory.memory_record import MemoryRecord
from semantic_kernel.memory.volatile_memory_store import VolatileMemoryStore

logger: logging.Logger = logging.getLogger(__name__)


class PersistentMemoryStore(VolatileMemoryStore):
    """A memory store that persists data to disk."""

    def __init__(self, file_path: str = "semantic_memory.pkl") -> None:
        super().__init__()
        self._file_path = file_path
        if os.path.exists(self._file_path):
            try:
                with open(self._file_path, "rb") as f:
                    self._store = pickle.load(f)
            except Exception as exc:  # pragma: no cover - corruption case
                logger.warning("Failed to load memory store: %s", exc)
        else:
            self._store = {}

    def _persist(self) -> None:
        """Write the current store to disk."""
        with open(self._file_path, "wb") as f:
            pickle.dump(self._store, f)

    async def create_collection(self, collection_name: str) -> None:  # noqa: D401
        await super().create_collection(collection_name)
        self._persist()

    async def delete_collection(self, collection_name: str) -> None:  # noqa: D401
        await super().delete_collection(collection_name)
        self._persist()

    async def upsert(self, collection_name: str, record: MemoryRecord) -> str:  # noqa: D401
        key = await super().upsert(collection_name, record)
        self._persist()
        return key

    async def upsert_batch(self, collection_name: str, records: List[MemoryRecord]) -> List[str]:  # noqa: D401
        keys = await super().upsert_batch(collection_name, records)
        self._persist()
        return keys

    async def remove(self, collection_name: str, key: str) -> None:  # noqa: D401
        await super().remove(collection_name, key)
        self._persist()

    async def remove_batch(self, collection_name: str, keys: List[str]) -> None:  # noqa: D401
        await super().remove_batch(collection_name, keys)
        self._persist()

    async def close(self) -> None:  # noqa: D401
        self._persist()

