#!/usr/bin/env python3
"""
Memory With Pandas module

Simplified sample demonstrating integration of a vector store with Pandas.
"""

import asyncio
from uuid import uuid4

import pandas as pd

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIEmbeddingPromptExecutionSettings,
    OpenAITextEmbedding,
)
from semantic_kernel.data.vector import VectorStoreCollectionDefinition, VectorStoreField
from semantic_kernel.connectors.memory.azure_ai_search import AzureAISearchCollection
from semantic_kernel.data.vector_store_record_fields import (
    VectorStoreRecordDataField,
    VectorStoreRecordKeyField,
    VectorStoreRecordVectorField,
)
from semantic_kernel.data.vector_search import VectorStoreRecordUtils

model_fields = VectorStoreCollectionDefinition(
    container_mode=True,
    fields={
        "content": VectorStoreRecordDataField(has_embedding=True, embedding_property_name="vector"),
        "id": VectorStoreRecordKeyField(),
        "vector": VectorStoreRecordVectorField(
            embedding_settings={"embedding": OpenAIEmbeddingPromptExecutionSettings(dimensions=1536)}
        ),
    },
)


definition = VectorStoreCollectionDefinition(
    collection_name="pandas_test_index",
    fields=[
        VectorStoreField("key", name="id", type="str"),
        VectorStoreField("data", name="title", type="str"),
        VectorStoreField("data", name="content", type="str", is_full_text_indexed=True),
        VectorStoreField(
            "vector",
            name="vector",
            type="float",
            dimensions=1536,
            embedding_generator=OpenAITextEmbedding(ai_model_id="text-embedding-3-small"),
        ),
    ],
    to_dict=lambda record, **_: record.to_dict(orient="records"),
    from_dict=lambda records, **_: pd.DataFrame(records),
    container_mode=True,
)


async def main() -> None:
    kernel = Kernel()
    kernel.add_service(OpenAITextEmbedding(service_id="embedding", ai_model_id="text-embedding-3-small"))

    async with AzureAISearchCollection[str, pd.DataFrame](
        record_type=pd.DataFrame,
        definition=definition,
    ) as collection:
        await collection.ensure_collection_exists()

        records = [
            {"id": str(uuid4()), "title": "Document about Semantic Kernel.", "content": "Semantic Kernel is a framework for building AI applications."},
            {"id": str(uuid4()), "title": "Document about Python", "content": "Python is a programming language that lets you work quickly."},
        ]

    df = pd.DataFrame(records)
    df = await VectorStoreRecordUtils(kernel).add_vector_to_records(df, None, data_model_definition=model_fields)
    print("Records with embeddings:")
    print(df.head())


if __name__ == "__main__":
    asyncio.run(main())
