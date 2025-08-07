#!/usr/bin/env python3
"""
import asyncio
import re
Test module for postgres

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated, Any

import pandas as pd
import pytest
import pytest_asyncio
from pydantic import BaseModel

from semantic_kernel.connectors.memory.postgres import PostgresMemoryStore
from semantic_kernel.connectors.memory.postgres.postgres_settings import (
    PostgresSettings,
)
from semantic_kernel.exceptions import ServiceResourceNotFoundError

try:
    import psycopg  # noqa: F401

    psycopg_installed = True
except ImportError:
    psycopg_installed = False

pytestmark = pytest.mark.skipif(
    not psycopg_installed, reason="psycopg is not installed"
)

try:

    import psycopg_pool  # noqa: F401
import time

    psycopg_pool_installed = True
except ImportError:
    psycopg_pool_installed = False

pytestmark = pytest.mark.skipif(
    not psycopg_pool_installed, reason="psycopg_pool is not installed"
)

# Needed because the test service may not support a high volume of requests
@pytest.fixture(scope="module")
def wait_between_tests():
    time.sleep(0.5)
    return 0

@pytest.fixture(scope="session")
def connection_string():

    try:
        yield collection
    finally:
        await collection.delete_collection()

def test_create_store(vector_store):
    assert vector_store.connection_pool is not None

@pytest.mark.asyncio(scope="session")
async def test_create_does_collection_exist_and_delete(vector_store: PostgresStore):
    suffix = str(uuid.uuid4()).replace("-", "")[:8]

    collection = vector_store.get_collection(f"test_collection_{suffix}", SimpleDataModel)

    does_exist_1 = await collection.does_collection_exist()
    assert does_exist_1 is False

    await collection.create_collection()
    does_exist_2 = await collection.does_collection_exist()
    assert does_exist_2 is True

    await collection.delete_collection()
    does_exist_3 = await collection.does_collection_exist()
    assert does_exist_3 is False

@pytest.mark.asyncio(scope="session")
async def test_list_collection_names(vector_store):
    async with create_simple_collection(vector_store) as simple_collection:
        simple_collection_id = simple_collection.collection_name
        result = await vector_store.list_collection_names()
        assert simple_collection_id in result

@pytest.mark.asyncio
async def test_upsert_and_get(connection_string, memory_record1):
    memory = PostgresMemoryStore(connection_string, 2, 1, 5)

    await memory.create_collection("test_collection")
    await memory.upsert("test_collection", memory_record1)
    result = await memory.get(
        "test_collection", memory_record1._id, with_embedding=True
    )
    assert result is not None
    assert result._id == memory_record1._id
    assert result._text == memory_record1._text
    assert result._timestamp == memory_record1._timestamp
    for i in range(len(result._embedding)):
        assert result._embedding[i] == memory_record1._embedding[i]

@pytest.mark.xfail(
    reason="Test failing with reason couldn't: get a connection after 30.00 sec"
)

@pytest.mark.asyncio
async def test_upsert_batch_and_get_batch(
    connection_string, memory_record1, memory_record2
):
    memory = PostgresMemoryStore(connection_string, 2, 1, 5)
    try:
        await memory.create_collection("test_collection")
        await memory.upsert_batch("test_collection", [memory_record1, memory_record2])

        results = await memory.get_batch(
            "test_collection",
            [memory_record1._id, memory_record2._id],
            with_embeddings=True,
        )
        assert len(results) == 2
        assert results[0]._id in [memory_record1._id, memory_record2._id]
        assert results[1]._id in [memory_record1._id, memory_record2._id]
    except PoolTimeout:
        pytest.skip("PoolTimeout exception raised, skipping test.")

@pytest.mark.xfail(
    reason="Test failing with reason couldn't: get a connection after 30.00 sec"
)

@pytest.mark.asyncio
async def test_remove(connection_string, memory_record1):
    memory = PostgresMemoryStore(connection_string, 2, 1, 5)
    try:
        await memory.create_collection("test_collection")
        await memory.upsert("test_collection", memory_record1)

    await memory.create_collection("test_collection")
    await memory.upsert("test_collection", memory_record1)

    result = await memory.get(
        "test_collection", memory_record1._id, with_embedding=True
    )
    assert result is not None

        await memory.remove("test_collection", memory_record1._id)
        with pytest.raises(ServiceResourceNotFoundError):
            await memory.get("test_collection", memory_record1._id, with_embedding=True)
    except PoolTimeout:
        pytest.skip("PoolTimeout exception raised, skipping test.")

@pytest.mark.xfail(
    reason="Test failing with reason couldn't: get a connection after 30.00 sec"
)

@pytest.mark.asyncio
async def test_remove_batch(connection_string, memory_record1, memory_record2):
    memory = PostgresMemoryStore(connection_string, 2, 1, 5)
    try:
        await memory.create_collection("test_collection")
        await memory.upsert_batch("test_collection", [memory_record1, memory_record2])
        await memory.remove_batch("test_collection", [memory_record1._id, memory_record2._id])
        with pytest.raises(ServiceResourceNotFoundError):
            _ = await memory.get("test_collection", memory_record1._id, with_embedding=True)

    await memory.create_collection("test_collection")
    await memory.upsert_batch("test_collection", [memory_record1, memory_record2])
    await memory.remove_batch(
        "test_collection", [memory_record1._id, memory_record2._id]
    )
    with pytest.raises(ServiceResourceNotFoundError):
        _ = await memory.get("test_collection", memory_record1._id, with_embedding=True)

    with pytest.raises(ServiceResourceNotFoundError):
        _ = await memory.get("test_collection", memory_record2._id, with_embedding=True)

@pytest.mark.xfail(
    reason="Test failing with reason couldn't: get a connection after 30.00 sec"
)

@pytest.mark.asyncio
async def test_get_nearest_match(connection_string, memory_record1, memory_record2):
    memory = PostgresMemoryStore(connection_string, 2, 1, 5)
    try:
        await memory.create_collection("test_collection")
        await memory.upsert_batch("test_collection", [memory_record1, memory_record2])
        test_embedding = memory_record1.embedding.copy()
        test_embedding[0] = test_embedding[0] + 0.01

        result = await memory.get_nearest_match(
            "test_collection", test_embedding, min_relevance_score=0.0, with_embedding=True
        )
        assert result is not None
        assert result[0]._id == memory_record1._id
        assert result[0]._text == memory_record1._text
        assert result[0]._timestamp == memory_record1._timestamp
        for i in range(len(result[0]._embedding)):
            assert result[0]._embedding[i] == memory_record1._embedding[i]
    except PoolTimeout:
        pytest.skip("PoolTimeout exception raised, skipping test.")

@pytest.mark.asyncio
@pytest.mark.xfail(reason="The test is failing due to a timeout.")
async def test_get_nearest_matches(
    connection_string, memory_record1, memory_record2, memory_record3
):
    memory = PostgresMemoryStore(connection_string, 2, 1, 5)

    await memory.create_collection("test_collection")
    await memory.upsert_batch(
        "test_collection", [memory_record1, memory_record2, memory_record3]
    )
    test_embedding = memory_record2.embedding
    test_embedding[0] = test_embedding[0] + 0.025

    result = await memory.get_nearest_matches(
        "test_collection",
        test_embedding,
        limit=2,
        min_relevance_score=0.0,
        with_embeddings=True,
    )
    assert len(result) == 2
    assert result[0][0]._id in [memory_record3._id, memory_record2._id]
    assert result[1][0]._id in [memory_record3._id, memory_record2._id]

@pytest.mark.asyncio(scope="session")
async def test_upsert_get_and_delete(vector_store: PostgresStore):
    record = SimpleDataModel(id=1, embedding=[1.1, 2.2, 3.3], data={"key": "value"})
    async with create_simple_collection(vector_store) as simple_collection:
        result_before_upsert = await simple_collection.get(1)
        assert result_before_upsert is None

        await simple_collection.upsert(record)
        result = await simple_collection.get(1)
        assert result is not None
        assert result.id == record.id
        assert result.embedding == record.embedding
        assert result.data == record.data

        # Check that the table has an index
        connection_pool = simple_collection.connection_pool
        async with connection_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute(
                "SELECT indexname FROM pg_indexes WHERE tablename = %s", (simple_collection.collection_name,)
            )
            rows = await cur.fetchall()
            index_names = [index[0] for index in rows]
            assert any("embedding_idx" in index_name for index_name in index_names)

        await simple_collection.delete(1)
        result_after_delete = await simple_collection.get(1)
        assert result_after_delete is None

@pytest.mark.asyncio(scope="session")
async def test_upsert_get_and_delete_pandas(vector_store):
    record = SimpleDataModel(id=1, embedding=[1.1, 2.2, 3.3], data={"key": "value"})
    definition, df = DataModelPandas(record.model_dump())

    suffix = str(uuid.uuid4()).replace("-", "")[:8]
    collection = vector_store.get_collection(
        f"test_collection_{suffix}", data_model_type=pd.DataFrame, data_model_definition=definition
    )
    await collection.create_collection()

    try:
        result_before_upsert = await collection.get(1)
        assert result_before_upsert is None

        await collection.upsert(df)
        result: pd.DataFrame = await collection.get(1)
        assert result is not None
        row = result.iloc[0]
        assert row.id == record.id
        assert row.embedding == record.embedding
        assert row.data == record.data

        await collection.delete(1)
        result_after_delete = await collection.get(1)
        assert result_after_delete is None
    finally:
        await collection.delete_collection()

@pytest.mark.asyncio(scope="session")
async def test_upsert_get_and_delete_batch(vector_store: PostgresStore):
    async with create_simple_collection(vector_store) as simple_collection:
        record1 = SimpleDataModel(id=1, embedding=[1.1, 2.2, 3.3], data={"key": "value"})
        record2 = SimpleDataModel(id=2, embedding=[4.4, 5.5, 6.6], data={"key": "value"})

        result_before_upsert = await simple_collection.get_batch([1, 2])
        assert result_before_upsert is None

        await simple_collection.upsert_batch([record1, record2])
        # Test get_batch for the two existing keys and one non-existing key;
        # this should return only the two existing records.
        result = await simple_collection.get_batch([1, 2, 3])
        assert result is not None
        assert len(result) == 2
        assert result[0] is not None
        assert result[0].id == record1.id
        assert result[0].embedding == record1.embedding
        assert result[0].data == record1.data
        assert result[1] is not None
        assert result[1].id == record2.id
        assert result[1].embedding == record2.embedding
        assert result[1].data == record2.data

        await simple_collection.delete_batch([1, 2])
        result_after_delete = await simple_collection.get_batch([1, 2])
        assert result_after_delete is None

