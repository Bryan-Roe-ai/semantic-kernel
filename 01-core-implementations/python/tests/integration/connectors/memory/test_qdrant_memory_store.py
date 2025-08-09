#!/usr/bin/env python3
"""Integration tests for QdrantMemoryStore (sanitized).

These tests run only if qdrant-client is installed. They exercise the
public async API used by higher-level memory abstractions: create,
enumerate, upsert, fetch, similarity search, and deletion.
"""

from __future__ import annotations

from datetime import datetime
from typing import List

import pytest

try:  # pragma: no cover - optional dependency
    import numpy as np  # type: ignore
    from semantic_kernel.connectors.memory.qdrant.qdrant_memory_store import (
        QdrantMemoryStore,
    )  # type: ignore
    from semantic_kernel.memory.memory_record import (
        MemoryRecord,
    )  # type: ignore

    QDRANT_AVAILABLE = True
except (ModuleNotFoundError, ImportError):  # pragma: no cover
    QDRANT_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not QDRANT_AVAILABLE, reason="qdrant-client (or numpy) not installed"
)

VECTOR_SIZE = 2
COLLECTION = "test_collection"


def _record(idx: int, vec: List[float]) -> MemoryRecord:
    return MemoryRecord(
        is_reference=False,
        external_source_name=None,
        id=f"id{idx}",
        description="desc",
        text=f"text {idx}",
        additional_metadata="meta",
        embedding=np.array(vec, dtype=float),
        key=None,
        timestamp=datetime.now(),
    )


@pytest.mark.asyncio
async def test_collection_lifecycle():
    store = QdrantMemoryStore(vector_size=VECTOR_SIZE, local=True)
    await store.create_collection(COLLECTION)
    assert COLLECTION in await store.get_collections()
    assert await store.does_collection_exist(COLLECTION)

    await store.delete_collection(COLLECTION)
    assert COLLECTION not in await store.get_collections()


@pytest.mark.asyncio
async def test_upsert_and_get():
    store = QdrantMemoryStore(vector_size=VECTOR_SIZE, local=True)
    await store.create_collection(COLLECTION)
    rec = _record(1, [0.1, 0.2])
    await store.upsert(COLLECTION, rec)
    fetched = await store.get(COLLECTION, rec.id, with_embedding=True)
    assert fetched is not None and fetched.id == rec.id


@pytest.mark.asyncio
async def test_upsert_batch_and_get_batch():
    store = QdrantMemoryStore(vector_size=VECTOR_SIZE, local=True)
    await store.create_collection(COLLECTION)
    r1 = _record(1, [0.3, 0.4])
    r2 = _record(2, [0.5, 0.6])
    await store.upsert_batch(COLLECTION, [r1, r2])
    fetched = await store.get_batch(COLLECTION, [r1.id, r2.id], True)
    assert len(fetched) == 2


@pytest.mark.asyncio
async def test_similarity_search():
    store = QdrantMemoryStore(vector_size=VECTOR_SIZE, local=True)
    await store.create_collection(COLLECTION)
    base = _record(1, [0.8, 0.2])
    near = _record(2, [0.81, 0.19])
    far = _record(3, [0.0, 1.0])
    await store.upsert_batch(COLLECTION, [base, near, far])
    result = await store.get_nearest_match(COLLECTION, base.embedding, 0.0, True)
    assert result is not None
    best, _score = result
    assert best.id in {base.id, near.id}


@pytest.mark.asyncio
async def test_remove_and_remove_batch():
    store = QdrantMemoryStore(vector_size=VECTOR_SIZE, local=True)
    await store.create_collection(COLLECTION)
    r1 = _record(1, [0.11, 0.22])
    r2 = _record(2, [0.33, 0.44])
    await store.upsert_batch(COLLECTION, [r1, r2])
    await store.remove(COLLECTION, r1.id)
    still = await store.get(COLLECTION, r2.id, False)
    assert still is not None
    await store.remove_batch(COLLECTION, [r2.id])
    gone = await store.get(COLLECTION, r2.id, False)
    assert gone is None
