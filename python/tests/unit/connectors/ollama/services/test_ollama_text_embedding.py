<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
<<<<<<< HEAD
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
<<<<<<< HEAD
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
# Copyright (c) Microsoft. All rights reserved.

from unittest.mock import patch

import numpy
import pytest
from numpy import array

from semantic_kernel.connectors.ai.ollama.ollama_prompt_execution_settings import (
    OllamaEmbeddingPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.ollama.services.ollama_text_embedding import (
    OllamaTextEmbedding,
)
from semantic_kernel.exceptions.service_exceptions import ServiceInitializationError


def test_init_empty_service_id(model_id):
    """Test that the service initializes correctly with an empty service id."""
    ollama = OllamaTextEmbedding(ai_model_id=model_id)
    assert ollama.service_id == model_id


def test_custom_client(model_id, custom_client):
    """Test that the service initializes correctly with a custom client."""
    ollama = OllamaTextEmbedding(ai_model_id=model_id, client=custom_client)
    assert ollama.client == custom_client


@pytest.mark.parametrize("exclude_list", [["OLLAMA_MODEL"]], indirect=True)
def test_init_empty_model_id(ollama_unit_test_env):
    """Test that the service initializes incorrectly with an empty model id."""
    with pytest.raises(ServiceInitializationError):
        _ = OllamaTextEmbedding(env_file_path="fake_env_file_path.env")


@pytest.mark.asyncio
@patch("ollama.AsyncClient.__init__", return_value=None)  # mock_client
@patch("ollama.AsyncClient.embeddings")  # mock_embedding_client
async def test_custom_host(mock_embedding_client, mock_client, model_id, host, prompt):
    """Test that the service initializes and generates embeddings correctly with a custom host."""
    mock_embedding_client.return_value = {"embedding": [0.1, 0.2, 0.3]}

    ollama = OllamaTextEmbedding(ai_model_id=model_id, host=host)
    _ = await ollama.generate_embeddings(
        [prompt],
    )

    mock_client.assert_called_once_with(host=host)


@pytest.mark.asyncio
@patch("ollama.AsyncClient.embeddings")
async def test_embedding(mock_embedding_client, model_id, prompt):
    """Test that the service initializes and generates embeddings correctly."""
    mock_embedding_client.return_value = {"embedding": [0.1, 0.2, 0.3]}
    settings = OllamaEmbeddingPromptExecutionSettings()
    settings.options = {"test_key": "test_value"}

    ollama = OllamaTextEmbedding(ai_model_id=model_id)
    response = await ollama.generate_embeddings(
        [prompt],
        settings=settings,
    )

    assert response.all() == array([0.1, 0.2, 0.3]).all()
    mock_embedding_client.assert_called_once_with(
        model=model_id, prompt=prompt, options=settings.options
    )


@pytest.mark.asyncio
@patch("ollama.AsyncClient.embeddings")
async def test_embedding_list_input(mock_embedding_client, model_id, prompt):
    """Test that the service initializes and generates embeddings correctly with a list of prompts."""
    mock_embedding_client.return_value = {"embedding": [0.1, 0.2, 0.3]}
    settings = OllamaEmbeddingPromptExecutionSettings()
    settings.options = {"test_key": "test_value"}

    ollama = OllamaTextEmbedding(ai_model_id=model_id)
    responses = await ollama.generate_embeddings(
        [prompt, prompt],
        settings=settings,
    )

    assert len(responses) == 2
    assert type(responses) is numpy.ndarray
    assert all(type(response) is numpy.ndarray for response in responses)
    assert mock_embedding_client.call_count == 2
    mock_embedding_client.assert_called_with(
        model=model_id, prompt=prompt, options=settings.options
    )


@pytest.mark.asyncio
@patch("ollama.AsyncClient.embeddings")
async def test_raw_embedding(mock_embedding_client, model_id, prompt):
    """Test that the service initializes and generates embeddings correctly."""
    mock_embedding_client.return_value = {"embedding": [0.1, 0.2, 0.3]}
    settings = OllamaEmbeddingPromptExecutionSettings()
    settings.options = {"test_key": "test_value"}

    ollama = OllamaTextEmbedding(ai_model_id=model_id)
    response = await ollama.generate_raw_embeddings(
        [prompt],
        settings=settings,
    )

    assert response == [[0.1, 0.2, 0.3]]
    mock_embedding_client.assert_called_once_with(
        model=model_id, prompt=prompt, options=settings.options
    )


@pytest.mark.asyncio
@patch("ollama.AsyncClient.embeddings")
async def test_raw_embedding_list_input(mock_embedding_client, model_id, prompt):
    """Test that the service initializes and generates embeddings correctly with a list of prompts."""
    mock_embedding_client.return_value = {"embedding": [0.1, 0.2, 0.3]}
    settings = OllamaEmbeddingPromptExecutionSettings()
    settings.options = {"test_key": "test_value"}

    ollama = OllamaTextEmbedding(ai_model_id=model_id)
    responses = await ollama.generate_raw_embeddings(
        [prompt, prompt],
        settings=settings,
    )

    assert responses == [[0.1, 0.2, 0.3], [0.1, 0.2, 0.3]]
    assert mock_embedding_client.call_count == 2
    mock_embedding_client.assert_called_with(
        model=model_id, prompt=prompt, options=settings.options
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
from unittest.mock import patch

import pytest
from numpy import array

from semantic_kernel.connectors.ai.ollama.services.ollama_text_embedding import (
    OllamaTextEmbedding,
)
from tests.unit.connectors.ollama.utils import MockResponse


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.post")
async def test_embedding(mock_post):
    mock_post.return_value = MockResponse(response=[0.1, 0.2, 0.3])
    ollama = OllamaTextEmbedding(ai_model_id="test_model")
    response = await ollama.generate_embeddings(
        ["test_prompt"],
    )
    assert response.all() == array([0.1, 0.2, 0.3]).all()
    mock_post.assert_called_once_with(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "test_model",
            "texts": ["test_prompt"],
            "options": {},
        },
>>>>>>> f40c1f2075e2443c31c57c34f5f66c2711a8db75
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< HEAD
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
    )
