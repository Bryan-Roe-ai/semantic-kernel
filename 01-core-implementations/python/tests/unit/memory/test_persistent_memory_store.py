#!/usr/bin/env python3
"""Tests for PersistentMemoryStore."""

import numpy as np
from pytest import mark

from semantic_kernel.memory import PersistentMemoryStore, MemoryRecord


@mark.asyncio
async def test_persistence(tmp_path):
    """Ensure data is written to disk and reloaded."""
    db_file = tmp_path / "store.pkl"
    store = PersistentMemoryStore(str(db_file))
    await store.create_collection("test")
    record = MemoryRecord.local_record(
        id="1",
        text="hello",
        description=None,
        additional_metadata=None,
        embedding=np.array([1.0, 0.0, 1.0]),
    )
    await store.upsert("test", record)
    await store.close()

    store2 = PersistentMemoryStore(str(db_file))
    result = await store2.get("test", "1", with_embedding=True)
    assert result.text == "hello"
    await store2.close()
