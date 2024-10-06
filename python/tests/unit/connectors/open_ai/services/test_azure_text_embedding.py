# Copyright (c) Microsoft. All rights reserved.

from unittest.mock import AsyncMock, call, patch

import pytest
from openai import AsyncAzureOpenAI
from openai.resources.embeddings import AsyncEmbeddings

<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
from semantic_kernel.connectors.ai.embeddings.embedding_generator_base import (
    EmbeddingGeneratorBase,
)
from semantic_kernel.connectors.ai.open_ai.services.azure_text_embedding import (
    AzureTextEmbedding,
)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
from semantic_kernel.connectors.ai.embeddings.embedding_generator_base import EmbeddingGeneratorBase
from semantic_kernel.connectors.ai.open_ai.services.azure_text_embedding import AzureTextEmbedding
from semantic_kernel.connectors.ai.open_ai.settings.azure_open_ai_settings import AzureOpenAISettings
>>>>>>> main
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
from semantic_kernel.exceptions.service_exceptions import ServiceInitializationError


def test_azure_text_embedding_init(azure_openai_unit_test_env) -> None:
    # Test successful initialization
    azure_text_embedding = AzureTextEmbedding()

    assert azure_text_embedding.client is not None
    assert isinstance(azure_text_embedding.client, AsyncAzureOpenAI)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
    assert (
        azure_text_embedding.ai_model_id
        == azure_openai_unit_test_env["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"]
    )
    assert isinstance(azure_text_embedding, EmbeddingGeneratorBase)


@pytest.mark.parametrize(
    "exclude_list", [["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"]], indirect=True
)
def test_azure_text_embedding_init_with_empty_deployment_name(
    azure_openai_unit_test_env,
) -> None:
    with pytest.raises(ServiceInitializationError):
        AzureTextEmbedding(
            env_file_path="test.env",
        )


@pytest.mark.parametrize("exclude_list", [["AZURE_OPENAI_API_KEY"]], indirect=True)
def test_azure_text_embedding_init_with_empty_api_key(
    azure_openai_unit_test_env,
) -> None:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
    assert azure_text_embedding.ai_model_id == azure_openai_unit_test_env["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"]
    assert isinstance(azure_text_embedding, EmbeddingGeneratorBase)


@pytest.mark.parametrize("exclude_list", [["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"]], indirect=True)
def test_azure_text_embedding_init_with_empty_deployment_name(azure_openai_unit_test_env) -> None:
>>>>>>> main
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    with pytest.raises(ServiceInitializationError):
        AzureTextEmbedding(
            env_file_path="test.env",
        )


<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
@pytest.mark.parametrize(
    "exclude_list", [["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_BASE_URL"]], indirect=True
)
def test_azure_text_embedding_init_with_empty_endpoint_and_base_url(
    azure_openai_unit_test_env,
) -> None:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
@pytest.mark.parametrize("exclude_list", [["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_BASE_URL"]], indirect=True)
def test_azure_text_embedding_init_with_empty_endpoint_and_base_url(azure_openai_unit_test_env) -> None:
    with pytest.raises(ServiceInitializationError):
        AzureTextEmbedding(
            env_file_path="test.env",
        )


<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
@pytest.mark.parametrize(
    "override_env_param_dict",
    [{"AZURE_OPENAI_ENDPOINT": "http://test.com"}],
    indirect=True,
)
def test_azure_text_embedding_init_with_invalid_endpoint(
    azure_openai_unit_test_env,
) -> None:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
@pytest.mark.parametrize("override_env_param_dict", [{"AZURE_OPENAI_ENDPOINT": "http://test.com"}], indirect=True)
def test_azure_text_embedding_init_with_invalid_endpoint(azure_openai_unit_test_env) -> None:
>>>>>>> main
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    with pytest.raises(ServiceInitializationError):
        AzureTextEmbedding()


@pytest.mark.parametrize(
    "override_env_param_dict",
    [{"AZURE_OPENAI_BASE_URL": "https://test_embedding_deployment.test-base-url.com"}],
    indirect=True,
)
def test_azure_text_embedding_init_with_from_dict(azure_openai_unit_test_env) -> None:
    default_headers = {"test_header": "test_value"}

    settings = {
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        "deployment_name": azure_openai_unit_test_env[
            "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"
        ],
=======
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
        "deployment_name": azure_openai_unit_test_env[
            "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"
        ],
=======
        "deployment_name": azure_openai_unit_test_env["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"],
>>>>>>> main
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        "endpoint": azure_openai_unit_test_env["AZURE_OPENAI_ENDPOINT"],
        "api_key": azure_openai_unit_test_env["AZURE_OPENAI_API_KEY"],
        "api_version": azure_openai_unit_test_env["AZURE_OPENAI_API_VERSION"],
        "default_headers": default_headers,
    }

    azure_text_embedding = AzureTextEmbedding.from_dict(settings=settings)

    assert azure_text_embedding.client is not None
    assert isinstance(azure_text_embedding.client, AsyncAzureOpenAI)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
    assert (
        azure_text_embedding.ai_model_id
        == azure_openai_unit_test_env["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"]
    )
    assert isinstance(azure_text_embedding, EmbeddingGeneratorBase)
    assert settings["deployment_name"] in str(azure_text_embedding.client.base_url)
    assert (
        azure_text_embedding.client.api_key
        == azure_openai_unit_test_env["AZURE_OPENAI_API_KEY"]
    )
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
    assert azure_text_embedding.ai_model_id == azure_openai_unit_test_env["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"]
    assert isinstance(azure_text_embedding, EmbeddingGeneratorBase)
    assert settings["deployment_name"] in str(azure_text_embedding.client.base_url)
    assert azure_text_embedding.client.api_key == azure_openai_unit_test_env["AZURE_OPENAI_API_KEY"]
>>>>>>> main
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

    # Assert that the default header we added is present in the client's default headers
    for key, value in default_headers.items():
        assert key in azure_text_embedding.client.default_headers
        assert azure_text_embedding.client.default_headers[key] == value


<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
@pytest.mark.asyncio
@patch.object(AsyncEmbeddings, "create", new_callable=AsyncMock)
async def test_azure_text_embedding_calls_with_parameters(
    mock_create, azure_openai_unit_test_env
) -> None:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
def test_azure_text_embedding_generates_no_token_with_api_key_in_env(azure_openai_unit_test_env) -> None:
    with (
        patch(
            f"{AzureOpenAISettings.__module__}.{AzureOpenAISettings.__qualname__}.get_azure_openai_auth_token",
        ) as mock_get_token,
    ):
        mock_get_token.return_value = "test_token"
        azure_text_embedding = AzureTextEmbedding()

        assert azure_text_embedding.client is not None
        # API key is provided in env var, so the ad_token should be None
        assert mock_get_token.call_count == 0


@pytest.mark.asyncio
@patch.object(AsyncEmbeddings, "create", new_callable=AsyncMock)
async def test_azure_text_embedding_calls_with_parameters(mock_create, azure_openai_unit_test_env) -> None:
>>>>>>> main
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    texts = ["hello world", "goodbye world"]
    embedding_dimensions = 1536

    azure_text_embedding = AzureTextEmbedding()

<<<<<<< Updated upstream
<<<<<<< Updated upstream
    await azure_text_embedding.generate_embeddings(
        texts, dimensions=embedding_dimensions
    )
=======
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
    await azure_text_embedding.generate_embeddings(
        texts, dimensions=embedding_dimensions
    )
=======
    await azure_text_embedding.generate_embeddings(texts, dimensions=embedding_dimensions)
>>>>>>> main
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

    mock_create.assert_awaited_once_with(
        input=texts,
        model=azure_openai_unit_test_env["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"],
        dimensions=embedding_dimensions,
    )


@pytest.mark.asyncio
@patch.object(AsyncEmbeddings, "create", new_callable=AsyncMock)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
async def test_azure_text_embedding_calls_with_batches(
    mock_create, azure_openai_unit_test_env
) -> None:
=======
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
async def test_azure_text_embedding_calls_with_batches(
    mock_create, azure_openai_unit_test_env
) -> None:
=======
async def test_azure_text_embedding_calls_with_batches(mock_create, azure_openai_unit_test_env) -> None:
>>>>>>> main
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    texts = [i for i in range(0, 5)]

    azure_text_embedding = AzureTextEmbedding()

    await azure_text_embedding.generate_embeddings(texts, batch_size=3)

    mock_create.assert_has_awaits(
        [
            call(
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
                model=azure_openai_unit_test_env[
                    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"
                ],
                input=texts[0:3],
            ),
            call(
                model=azure_openai_unit_test_env[
                    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"
                ],
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
                model=azure_openai_unit_test_env["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"],
                input=texts[0:3],
            ),
            call(
                model=azure_openai_unit_test_env["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"],
>>>>>>> main
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
                input=texts[3:5],
            ),
        ],
        any_order=False,
    )
