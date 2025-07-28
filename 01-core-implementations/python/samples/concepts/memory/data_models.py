#!/usr/bin/env python3
"""
Data Models module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.
"""

from dataclasses import dataclass, field
from typing import Annotated, Any
from uuid import uuid4

from pandas import DataFrame
from pydantic import BaseModel, Field

from semantic_kernel.data.vector import (
    VectorStoreCollectionDefinition,
    VectorStoreField,
)
from semantic_kernel.data.vector_store_model_decorator import vectorstoremodel
from semantic_kernel.data.vector_store_model_definition import (
    VectorStoreRecordDefinition,
)
from semantic_kernel.data.vector_store_record_fields import (
    VectorStoreRecordDataField,
    VectorStoreRecordKeyField,
    VectorStoreRecordVectorField,
)


@vectorstoremodel
@dataclass
class DataModelDataclass:
    vector: Annotated[list[float], VectorStoreRecordVectorField]
    key: Annotated[str, VectorStoreRecordKeyField()] = field(
        default_factory=lambda: str(uuid4())
    )
    content: Annotated[
        str,
        VectorStoreRecordDataField(
            has_embedding=True, embedding_property_name="vector"
        ),
    ] = "content1"
    other: str | None = None


@vectorstoremodel
class DataModelPydantic(BaseModel):
    vector: Annotated[list[float], VectorStoreRecordVectorField]
    key: Annotated[str, VectorStoreRecordKeyField()] = Field(
        default_factory=lambda: str(uuid4())
    )
    content: Annotated[
        str,
        VectorStoreRecordDataField(
            has_embedding=True, embedding_property_name="vector"
        ),
    ] = "content1"
    other: str | None = None


@vectorstoremodel
class DataModelPydanticComplex(BaseModel):
    vector: Annotated[list[float], VectorStoreRecordVectorField]
    key: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4())),
        VectorStoreRecordKeyField(),
    ]
    content: Annotated[
        str,
        VectorStoreRecordDataField(
            has_embedding=True, embedding_property_name="vector"
        ),
    ] = "content1"
    other: str | None = None


@vectorstoremodel
class DataModelPython:
    def __init__(
        self,
        vector: Annotated[list[float], VectorStoreRecordVectorField],
        key: Annotated[str, VectorStoreRecordKeyField] | None = None,
        content: Annotated[
            str,
            VectorStoreRecordDataField(
                has_embedding=True, embedding_property_name="vector"
            ),
        ] = "content1",
        other: str | None = None,
    ) -> None:
        self.vector = vector
        self.key = key or str(uuid4())
        self.content = content
        self.other = other

    def __str__(self) -> str:
        return (
            f"DataModelPython(vector={self.vector}, key={self.key}, "
            f"content={self.content}, other={self.other})"
        )

    def serialize(self) -> dict[str, Any]:
        return {"vector": self.vector, "key": self.key, "content": self.content}

    @classmethod
    def deserialize(cls, obj: dict[str, Any]) -> "DataModelPython":
        return cls(
            vector=obj["vector"],
            key=obj["key"],
            content=obj["content"],
        )


definition_pandas = VectorStoreCollectionDefinition(
    fields=[
        VectorStoreField("vector", name="vector", type="float", dimensions=3),
        VectorStoreField("key", name="key", type="str"),
        VectorStoreField("data", name="content", type="str"),
    ],
    container_mode=True,
    to_dict=lambda record, **_: record.to_dict(orient="records"),
    from_dict=lambda records, **_: DataFrame(records),
)


if __name__ == "__main__":
    data_item1 = DataModelDataclass(content="Hello, world!", vector=[1.0, 2.0, 3.0])
    data_item2 = DataModelPydantic(content="Hello, world!", vector=[1.0, 2.0, 3.0])
    data_item3 = DataModelPydanticComplex(content="Hello, world!", vector=[1.0, 2.0, 3.0])
    data_item4 = DataModelPython(content="Hello, world!", vector=[1.0, 2.0, 3.0])

    print("Example records:")
    print(f"DataClass:\n  {data_item1}\n")
    print(f"Pydantic:\n  {data_item2}\n")
    print(f"Pydantic Complex:\n  {data_item3}\n")
    print(f"Python:\n  {data_item4}\n")
