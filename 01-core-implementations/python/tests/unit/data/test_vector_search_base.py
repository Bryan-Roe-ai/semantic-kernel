#!/usr/bin/env python3
"""
Test module for vector search base

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


import pytest

from semantic_kernel.data.vector import VectorSearch, VectorSearchOptions, VectorSearchProtocol


async def test_search(vector_store_record_collection: VectorSearch):
    assert isinstance(vector_store_record_collection, VectorSearchProtocol)
    record = {"id": "test_id", "content": "test_content", "vector": [1.0, 2.0, 3.0]}
    await vector_store_record_collection.upsert(record)
    results = await vector_store_record_collection.search(vector=[1.0, 2.0, 3.0])
    records = [rec async for rec in results.results]
    assert records[0].record == record


@pytest.mark.parametrize("include_vectors", [True, False])
async def test_get_vector_search_results(vector_store_record_collection: VectorSearch, include_vectors: bool):
    options = VectorSearchOptions(include_vectors=include_vectors)
    results = [{"id": "test_id", "content": "test_content", "vector": [1.0, 2.0, 3.0]}]
    async for result in vector_store_record_collection._get_vector_search_results_from_results(
        results=results, options=options
    ):
        assert result.record == results[0] if include_vectors else {"id": "test_id", "content": "test_content"}
        break
