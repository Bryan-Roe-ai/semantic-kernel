#!/usr/bin/env python3
"""
Test module for mongodb atlas store

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


from pymongo import AsyncMongoClient

from semantic_kernel.connectors.mongodb import MongoDBAtlasCollection, MongoDBAtlasStore


def test_mongodb_atlas_store_initialization(mongodb_atlas_unit_test_env):
    store = MongoDBAtlasStore()
    assert store.mongo_client is not None
    assert isinstance(store.mongo_client, AsyncMongoClient)


def test_mongodb_atlas_store_get_collection(mongodb_atlas_unit_test_env, definition):
    store = MongoDBAtlasStore()
    collection = store.get_collection(
        collection_name="test_collection",
        record_type=dict,
        definition=definition,
    )
    assert collection is not None
    assert isinstance(collection, MongoDBAtlasCollection)


async def test_mongodb_atlas_store_list_collection_names(mongodb_atlas_unit_test_env, mock_mongo_client):
    store = MongoDBAtlasStore(mongo_client=mock_mongo_client, database_name="test_db")
    store.mongo_client.get_database().list_collection_names.return_value = ["test_collection"]
    result = await store.list_collection_names()
    assert result == ["test_collection"]
