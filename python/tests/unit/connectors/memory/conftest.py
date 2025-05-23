# Copyright (c) Microsoft. All rights reserved.

<<<<<<< HEAD
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
=======
from pytest import fixture


@fixture()
def mongodb_atlas_unit_test_env(monkeypatch, exclude_list, override_env_param_dict):
    """Fixture to set environment variables for MongoDB Atlas Unit Tests."""
    if exclude_list is None:
        exclude_list = []

    if override_env_param_dict is None:
        override_env_param_dict = {}

    env_vars = {"MONGODB_ATLAS_CONNECTION_STRING": "mongodb://test", "MONGODB_ATLAS_DATABASE_NAME": "test-database"}

    env_vars.update(override_env_param_dict)

    for key, value in env_vars.items():
        if key not in exclude_list:
            monkeypatch.setenv(key, value)
        else:
            monkeypatch.delenv(key, raising=False)

    return env_vars


@fixture
def postgres_unit_test_env(monkeypatch, exclude_list, override_env_param_dict):
    """Fixture to set environment variables for Postgres connector."""
    if exclude_list is None:
        exclude_list = []

    if override_env_param_dict is None:
        override_env_param_dict = {}

    env_vars = {"POSTGRES_CONNECTION_STRING": "host=localhost port=5432 dbname=postgres user=testuser password=example"}

    env_vars.update(override_env_param_dict)

    for key, value in env_vars.items():
        if key not in exclude_list:
            monkeypatch.setenv(key, value)
        else:
            monkeypatch.delenv(key, raising=False)

    return env_vars


@fixture
def qdrant_unit_test_env(monkeypatch, exclude_list, override_env_param_dict):
    """Fixture to set environment variables for QdrantConnector."""
    if exclude_list is None:
        exclude_list = []

    if override_env_param_dict is None:
        override_env_param_dict = {}

    env_vars = {"QDRANT_LOCATION": "http://localhost:6333"}

    env_vars.update(override_env_param_dict)

    for key, value in env_vars.items():
        if key not in exclude_list:
            monkeypatch.setenv(key, value)
        else:
            monkeypatch.delenv(key, raising=False)

    return env_vars


@fixture
def redis_unit_test_env(monkeypatch, exclude_list, override_env_param_dict):
    """Fixture to set environment variables for Redis."""
    if exclude_list is None:
        exclude_list = []

    if override_env_param_dict is None:
        override_env_param_dict = {}

    env_vars = {"REDIS_CONNECTION_STRING": "redis://localhost:6379"}

    env_vars.update(override_env_param_dict)

    for key, value in env_vars.items():
        if key not in exclude_list:
            monkeypatch.setenv(key, value)
        else:
            monkeypatch.delenv(key, raising=False)

    return env_vars


@fixture
def pinecone_unit_test_env(monkeypatch, exclude_list, override_env_param_dict):
    """Fixture to set environment variables for Pinecone."""
    if exclude_list is None:
        exclude_list = []

    if override_env_param_dict is None:
        override_env_param_dict = {}

    env_vars = {"PINECONE_API_KEY": "test_key"}

    env_vars.update(override_env_param_dict)

    for key, value in env_vars.items():
        if key not in exclude_list:
            monkeypatch.setenv(key, value)
        else:
            monkeypatch.delenv(key, raising=False)

    return env_vars


@fixture
def sql_server_unit_test_env(monkeypatch, exclude_list, override_env_param_dict):
    """Fixture to set environment variables for SQL Server."""
    if exclude_list is None:
        exclude_list = []

    if override_env_param_dict is None:
        override_env_param_dict = {}

    env_vars = {
        "SQL_SERVER_CONNECTION_STRING": "Driver={ODBC Driver 18 for SQL Server};Server=localhost;Database=testdb;User Id=testuser;Password=example;"  # noqa: E501
    }

    env_vars.update(override_env_param_dict)

    for key, value in env_vars.items():
        if key not in exclude_list:
            monkeypatch.setenv(key, value)
        else:
            monkeypatch.delenv(key, raising=False)

    return env_vars
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
