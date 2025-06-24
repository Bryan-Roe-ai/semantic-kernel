#!/usr/bin/env python3
"""
Memory With Pandas module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import asyncio
from uuid import uuid4

import pandas as pd

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIEmbeddingPromptExecutionSettings,
    OpenAITextEmbedding,
)
from semantic_kernel.connectors.ai.open_ai.services.open_ai_text_embedding import (
    OpenAITextEmbedding,
)
from semantic_kernel.connectors.memory.azure_ai_search.azure_ai_search_collection import (
    AzureAISearchCollection,
)
from semantic_kernel.data.vector_store_model_definition import (
    VectorStoreRecordDefinition,
)
from semantic_kernel.data.vector_store_record_fields import (
from semantic_kernel.connectors.memory.azure_ai_search import AzureAISearchCollection
from semantic_kernel.data import (
from semantic_kernel.connectors.memory.azure_ai_search import AzureAISearchCollection
from semantic_kernel.data import (
    VectorStoreRecordDataField,
    VectorStoreRecordDefinition,
    VectorStoreRecordKeyField,
    VectorStoreRecordVectorField,
)
from semantic_kernel.data.vector_search import add_vector_to_records

model_fields = VectorStoreRecordDefinition(
    container_mode=True,
    fields={
        "content": VectorStoreRecordDataField(
            has_embedding=True, embedding_property_name="vector"
        ),
        "id": VectorStoreRecordKeyField(),
        "vector": VectorStoreRecordVectorField(
            embedding_settings={
                "embedding": OpenAIEmbeddingPromptExecutionSettings(dimensions=1536)
            }
from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding
from semantic_kernel.connectors.azure_ai_search import AzureAISearchCollection
from semantic_kernel.data.vector import VectorStoreCollectionDefinition, VectorStoreField

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


async def main():
    # setup the kernel
    kernel = Kernel()
    kernel.add_service(
        OpenAITextEmbedding(
            service_id="embedding", ai_model_id="text-embedding-3-small"
        )
    )

    # create the record collection
    async with AzureAISearchCollection[str, pd.DataFrame](
        record_type=pd.DataFrame,
        definition=definition,
    ) as collection:
        await collection.ensure_collection_exists()
        # create some records
        records = [
            {
                "id": str(uuid4()),
                "title": "Document about Semantic Kernel.",
                "content": "Semantic Kernel is a framework for building AI applications.",
            },
            {
                "id": str(uuid4()),
                "title": "Document about Python",
                "content": "Python is a programming language that lets you work quickly.",
            },
        ]

    # create the dataframe and add the embeddings
    df = pd.DataFrame(records)
    df = await VectorStoreRecordUtils(kernel).add_vector_to_records(
        df, None, data_model_definition=model_fields
    )
    print("Records with embeddings:")
    print(df.shape)
    print(df.head(5))
        # create the dataframe and add the embeddings
        df = pd.DataFrame(records)
        df = await add_vector_to_records(kernel, df, None, data_model_definition=model_fields)
        print("Records with embeddings:")
        print(df.shape)
        print(df.head(5))
        # create the dataframe and add the content you want to embed to a new column
        df = pd.DataFrame(records)
        df["vector"] = df.apply(lambda row: f"title: {row['title']}, content: {row['content']}", axis=1)
        print(df.head(1))
        # upsert the records (for a container, upsert and upsert_batch are equivalent)
        await collection.upsert(df)

        # retrieve a record
        result = await collection.get(top=2)
        if result is None:
            print("No records found, this is sometimes because the get is too fast and the index is not ready yet.")
        else:
            print("Retrieved records:")
            print(result.to_string())

        await collection.ensure_collection_deleted()


if __name__ == "__main__":
    asyncio.run(main())
