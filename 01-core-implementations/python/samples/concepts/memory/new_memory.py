#!/usr/bin/env python3
"""
Simplified example for memory stores.
"""

import asyncio
import argparse
from uuid import uuid4
from collections.abc import Callable

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai.services.open_ai_text_embedding import OpenAITextEmbedding
from semantic_kernel.connectors.memory.azure_ai_search import AzureAISearchCollection
from semantic_kernel.connectors.memory.qdrant import QdrantCollection
from semantic_kernel.connectors.memory.redis import RedisHashsetCollection, RedisJsonCollection
from semantic_kernel.connectors.memory.in_memory import InMemoryVectorCollection
from semantic_kernel.connectors.memory.weaviate import WeaviateCollection
from semantic_kernel.connectors.memory.postgres import PostgresCollection
from semantic_kernel.connectors.memory.azure_cosmos_db import AzureCosmosDBNoSQLCollection
from semantic_kernel.data import VectorStoreRecordCollection
from semantic_kernel.data.vector_store_record_fields import (
    VectorStoreRecordDataField,
    VectorStoreRecordKeyField,
    VectorStoreRecordVectorField,
)
from semantic_kernel.data.vector_store_model_decorator import vectorstoremodel


@vectorstoremodel
class DataModel:
    id: VectorStoreRecordKeyField
    content: VectorStoreRecordDataField
    vector: VectorStoreRecordVectorField


def build_kernel() -> Kernel:
    kernel = Kernel()
    kernel.add_service(OpenAITextEmbedding(service_id="embedding", ai_model_id="text-embedding-3-small"))
    return kernel


def get_collection(name: str) -> VectorStoreRecordCollection:
    collection_name = f"sample_{name}_collection"
    collections: dict[str, Callable[[], VectorStoreRecordCollection]] = {
        "ai_search": lambda: AzureAISearchCollection[DataModel](data_model_type=DataModel),
        "qdrant": lambda: QdrantCollection[DataModel](data_model_type=DataModel, collection_name=collection_name),
        "redis_json": lambda: RedisJsonCollection[DataModel](data_model_type=DataModel, collection_name=collection_name),
        "redis_hash": lambda: RedisHashsetCollection[DataModel](data_model_type=DataModel, collection_name=collection_name),
        "in_memory": lambda: InMemoryVectorCollection[DataModel](data_model_type=DataModel, collection_name=collection_name),
        "weaviate": lambda: WeaviateCollection[str, DataModel](data_model_type=DataModel, collection_name=collection_name),
        "postgres": lambda: PostgresCollection[str, DataModel](data_model_type=DataModel, collection_name=collection_name),
        "azure_cosmos_nosql": lambda: AzureCosmosDBNoSQLCollection(data_model_type=DataModel, collection_name=collection_name),
    }
    return collections[name]()


async def main(collection: str) -> None:
    kernel = build_kernel()
    store = get_collection(collection)
    async with store:
        await store.ensure_collection_exists()
        record = DataModel(id=str(uuid4()), content="hello", vector=[0.1, 0.2, 0.3])
        await store.upsert(record)
        print("Record stored successfully")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("collection", choices=[
        "ai_search",
        "qdrant",
        "redis_json",
        "redis_hash",
        "in_memory",
        "weaviate",
        "postgres",
        "azure_cosmos_nosql",
    ])
    args = parser.parse_args()
    asyncio.run(main(args.collection))
