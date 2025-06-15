# Copyright (c) Microsoft. All rights reserved.

from dataclasses import dataclass, field
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel
from pytest import fixture

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import (
    OpenAIEmbeddingPromptExecutionSettings,
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

@fixture
def dataclass_vector_data_model() -> object:
    @vectorstoremodel
    @dataclass
    class MyDataModel:
        vector: Annotated[
            list[float] | None,
            VectorStoreRecordVectorField(
                embedding_settings={
                    "default": OpenAIEmbeddingPromptExecutionSettings(dimensions=1536)
                },
                index_kind="hnsw",
                dimensions=1536,
                distance_function="cosine",
                property_type="float",
            ),
        ] = None
        other: str | None = None
        id: Annotated[str, VectorStoreRecordKeyField()] = field(
            default_factory=lambda: str(uuid4())
        )
        content: Annotated[
            str,
            VectorStoreRecordDataField(
                has_embedding=True,
                embedding_property_name="vector",
                property_type="str",
            ),
        ] = "content1"

    return MyDataModel

@fixture
def data_model_definition() -> object:
    return VectorStoreRecordDefinition(
        fields={
            "id": VectorStoreRecordKeyField(),
            "content": VectorStoreRecordDataField(
                has_embedding=True,
                embedding_property_name="vector",
            ),
            "vector": VectorStoreRecordVectorField(dimensions=3),
        }
    )

@fixture
def data_model_type():
    @vectorstoremodel
    class DataModelClass(BaseModel):
        content: Annotated[
            str,
            VectorStoreRecordDataField(
                has_embedding=True, embedding_property_name="vector"
            ),
        ]
        vector: Annotated[list[float], VectorStoreRecordVectorField()]
        id: Annotated[str, VectorStoreRecordKeyField()]

    return DataModelClass
from pytest import fixture

def filter_lambda_list(store: str) -> list[ParameterSet]:
    """Fixture to provide a list of filter lambdas for testing."""
    sets = [
        (
            lambda x: x.content == "value",
            {
                "ai_search": "content eq 'value'",
            },
            "equal with string",
        ),
        (
            lambda x: x.id == 0,
            {
                "ai_search": "id eq 0",
            },
            "equal with int",
        ),
        (
            lambda x: x.content != "value",
            {
                "ai_search": "content ne 'value'",
            },
            "not equal",
        ),
        (
            lambda x: x.id > 0,
            {
                "ai_search": "id gt 0",
            },
            "greater than",
        ),
        (
            lambda x: x.id >= 0,
            {
                "ai_search": "id ge 0",
            },
            "greater than or equal",
        ),
        (
            lambda x: x.id == +0,
            {
                "ai_search": "id eq +0",
            },
            "equal with explicit positive",
        ),
        (
            lambda x: x.id < 0,
            {
                "ai_search": "id lt 0",
            },
            "less than",
        ),
        (
            lambda x: x.id <= 0,
            {
                "ai_search": "id le 0",
            },
            "less than or equal",
        ),
        (
            lambda x: -10 <= x.id <= 0,
            {
                "ai_search": "(-10 le id and id le 0)",
            },
            "between inclusive",
        ),
        (
            lambda x: -10 < x.id < 0,
            {
                "ai_search": "(-10 lt id and id lt 0)",
            },
            "between exclusive",
        ),
        (
            lambda x: x.content == "value" and x.id == 0,
            {
                "ai_search": "(content eq 'value' and id eq 0)",
            },
            "and",
        ),
        (
            lambda x: x.content == "value" or x.id == 0,
            {
                "ai_search": "(content eq 'value' or id eq 0)",
            },
            "or",
        ),
        (
            lambda x: not x.content,
            {
                "ai_search": "not content",
            },
            "not with truthy",
        ),
        (
            lambda x: not (x.content == "value"),  # noqa: SIM201
            {
                "ai_search": "not content eq 'value'",
            },
            "not with equal",
        ),
        (
            lambda x: not (x.content != "value"),  # noqa: SIM202
            {
                "ai_search": "not content ne 'value'",
            },
            "not with not equal",
        ),
        (
            lambda x: "value" in x.content,
            {
                "ai_search": "search.ismatch('value', 'content')",
            },
            "contains",
        ),
        (
            lambda x: "value" not in x.content,
            {
                "ai_search": "not search.ismatch('value', 'content')",
            },
            "not contains",
        ),
        (
            lambda x: (x.id > 0 and x.id < 3) or (x.id > 7 and x.id < 10),
            {
                "ai_search": "((id gt 0 and id lt 3) or (id gt 7 and id lt 10))",
            },
            "complex",
        ),
        (
            lambda x: x.unknown_field == "value",
            {
                "ai_search": VectorStoreOperationException,
            },
            "fail unknown field",
        ),
        (
            lambda x: any(x == "a" for x in x.content),
            {
                "ai_search": NotImplementedError,
            },
            "comprehension",
        ),
        (
            lambda x: ~x.id,
            {
                "ai_search": NotImplementedError,
            },
            "invert",
        ),
        (
            lambda x: constant,  # noqa: F821
            {
                "ai_search": NotImplementedError,
            },
            "constant",
        ),
        (
            lambda x: x.content.city == "Seattle",
            {
                "ai_search": "content/city eq 'Seattle'",
            },
            "nested property",
        ),
    ]
    return [param(s[0], s[1][store], id=s[2]) for s in sets if store in s[1]]
