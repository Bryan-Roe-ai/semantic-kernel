# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.kernel import Kernel
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin
from semantic_kernel.connectors.ai.mistral_ai import MistralAITextEmbedding
from semantic_kernel.connectors.ai.embeddings.embedding_generator_base import (
    EmbeddingGeneratorBase,
)
import semantic_kernel as sk
import os

import pytest

<< << << < main
<< << << < main
== == == =
>>>>>> > origin/main

mistral_ai_setup: bool = False
try:
    if os.environ["MISTRALAI_API_KEY"] and os.environ["MISTRALAI_EMBEDDING_MODEL_ID"]:
        mistral_ai_setup = True
except KeyError:
    mistral_ai_setup = False

pytestmark = pytest.mark.parametrize(
    "embeddings_generator",
    [
        pytest.param(
            MistralAITextEmbedding() if mistral_ai_setup else None,
            marks=pytest.mark.skipif(
                not mistral_ai_setup, reason="Mistral AI environment variables not set"
            ),
            id="MistralEmbeddings",
        )
<< << << < main
== == == =
from semantic_kernel.connectors.ai.embeddings.embedding_generator_base import EmbeddingGeneratorBase

from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from tests.integration.embeddings.test_embedding_service_base import (
    EmbeddingServiceTestBase,
    google_ai_setup,
    mistral_ai_setup,
    vertex_ai_setup,
)

pytestmark= pytest.mark.parametrize(
    "service_id, execution_settings_kwargs, output_dimensionality",
    [
        pytest.param(
            "openai",
            {},
            1536,  # text-embedding-ada-002 doesn't support custom output dimensionality
            id="openai",
        ),
        pytest.param(
            "azure",
            {},
            1536,  # text-embedding-ada-002 doesn't support custom output dimensionality
            id="azure",
        ),
        pytest.param(
            "azure_custom_client",
            {},
            1536,  # text-embedding-ada-002 doesn't support custom output dimensionality
            id="azure_custom_client",
        ),
        pytest.param(
            "azure_ai_inference",
            {},
            1536,  # text-embedding-ada-002 doesn't support custom output dimensionality
            id="azure_ai_inference",
        ),
        pytest.param(
            "mistral_ai",
            {},
            1024,
            marks=pytest.mark.skipif(
                not mistral_ai_setup, reason="Mistral AI environment variables not set"),
            id="mistral_ai",
        ),
        pytest.param(
            "hugging_face",
            {},
            384,
            id="hugging_face",
        ),
        pytest.param(
            "ollama",
            {},
            768,
            id="ollama",
        ),
        pytest.param(
            "google_ai",
            {"output_dimensionality": 10},
            10,
            marks=pytest.mark.skipif(
                not google_ai_setup, reason="Google AI environment variables not set"),
            id="google_ai",
        ),
        pytest.param(
            "vertex_ai",
            {"output_dimensionality": 10},
            10,
            marks=pytest.mark.skipif(
                not vertex_ai_setup, reason="Vertex AI environment variables not set"),
            id="vertex_ai",
        ),
        pytest.param(
            "bedrock_amazon_titan-v1",
            {},
            1536,  # This model doesn't support custom output dimensionality
            id="bedrock_amazon_titan-v1",
        ),
        pytest.param(
            "bedrock_amazon_titan-v2",
            {"extension_data": {"dimensions": 256}},
            256,
            id="bedrock_amazon_titan-v2",
        ),
        pytest.param(
            "bedrock_cohere",
            {},
            1024,
            id="bedrock_cohere",
        ),
>>>>>> > upstream/main
== == == =
>>>>>> > origin/main
    ],
)

@ pytest.mark.asyncio(scope="module")
<< << << < main
<< << << < main
== == == =
>>>>>> > origin/main
async def test_embedding_service(
    kernel: Kernel, embeddings_generator: EmbeddingGeneratorBase
):
    kernel.add_service(embeddings_generator)

    memory= SemanticTextMemory(
        storage=sk.memory.VolatileMemoryStore(),
        embeddings_generator=embeddings_generator,
    )
    kernel.add_plugin(TextMemoryPlugin(memory), "TextMemoryPlugin")
<< << << < main
== == == =
class TestEmbeddingService(EmbeddingServiceTestBase):
    """Test embedding service with memory.

    This tests if the embedding service can be used with the semantic memory.
    """
>> >>>> > upstream/main
== == == =

    await memory.save_reference(
        "test",
        external_id="info1",
        text="this is a test",
        external_source_name="external source",
    )
>> >>>> > origin/main

    # Add some documents to the semantic memory
    await memory.save_information("test", id="info1", text="Sharks are fish.")
    await memory.save_information("test", id="info2", text="Whales are mammals.")
    await memory.save_information("test", id="info3", text="Penguins are birds.")
    await memory.save_information("test", id="info4", text="Dolphins are mammals.")
    await memory.save_information("test", id="info5", text="Flies are insects.")

    # Search for documents
    query= "What are mammals?"
    result= await memory.search("test", query, limit=2, min_relevance_score=0.0)
    print(f"Query: {query}")
    print(f"\tAnswer 1: {result[0].text}")
    print(f"\tAnswer 2: {result[1].text}\n")
    assert "mammals." in result[0].text
    assert "mammals." in result[1].text

    query= "What are fish?"
    result= await memory.search("test", query, limit=1, min_relevance_score=0.0)
    print(f"Query: {query}")
    print(f"\tAnswer: {result[0].text}\n")
    assert result[0].text == "Sharks are fish."

    query= "What are insects?"
    result= await memory.search("test", query, limit=1, min_relevance_score=0.0)
    print(f"Query: {query}")
    print(f"\tAnswer: {result[0].text}\n")
    assert result[0].text == "Flies are insects."

    query= "What are birds?"
    result= await memory.search("test", query, limit=1, min_relevance_score=0.0)
    print(f"Query: {query}")
    print(f"\tAnswer: {result[0].text}\n")
    assert result[0].text == "Penguins are birds."

# Copyright (c) Microsoft. All rights reserved.

from typing import Any

import pytest

from semantic_kernel.connectors.ai.embeddings.embedding_generator_base import EmbeddingGeneratorBase
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from tests.integration.embeddings.test_embedding_service_base import (
    EmbeddingServiceTestBase,
    google_ai_setup,
    mistral_ai_setup,
    ollama_setup,
    vertex_ai_setup,
)

pytestmark= pytest.mark.parametrize(
    "service_id, execution_settings_kwargs, output_dimensionality",
    [
        pytest.param(
            "openai",
            {},
            1536,  # text-embedding-ada-002 doesn't support custom output dimensionality
            id="openai",
        ),
        pytest.param(
            "azure",
            {},
            1536,  # text-embedding-ada-002 doesn't support custom output dimensionality
            id="azure",
        ),
        pytest.param(
            "azure_custom_client",
            {},
            1536,  # text-embedding-ada-002 doesn't support custom output dimensionality
            id="azure_custom_client",
        ),
        pytest.param(
            "azure_ai_inference",
            {},
            1536,  # text-embedding-ada-002 doesn't support custom output dimensionality
            id="azure_ai_inference",
        ),
        pytest.param(
            "mistral_ai",
            {},
            1024,
            marks=pytest.mark.skipif(
                not mistral_ai_setup, reason="Mistral AI environment variables not set"),
            id="mistral_ai",
        ),
        pytest.param(
            "hugging_face",
            {},
            384,
            id="hugging_face",
        ),
        pytest.param(
            "ollama",
            {},
            768,
            marks=pytest.mark.skipif(
                not ollama_setup, reason="Ollama environment variables not set"),
            marks=(
                pytest.mark.skipif(not ollama_setup, reason="Ollama not setup"),
                pytest.mark.ollama,
            ),
            id="ollama",
        ),
        pytest.param(
            "google_ai",
            {"output_dimensionality": 10},
            10,
            marks=pytest.mark.skipif(
                not google_ai_setup, reason="Google AI environment variables not set"),
            id="google_ai",
        ),
        pytest.param(
            "vertex_ai",
            {"output_dimensionality": 10},
            10,
            marks=pytest.mark.skipif(
                not vertex_ai_setup, reason="Vertex AI environment variables not set"),
            id="vertex_ai",
        ),
        pytest.param(
            "bedrock_amazon_titan-v1",
            {},
            1536,  # This model doesn't support custom output dimensionality
            id="bedrock_amazon_titan-v1",
        ),
        pytest.param(
            "bedrock_amazon_titan-v2",
            {"extension_data": {"dimensions": 256}},
            256,
            id="bedrock_amazon_titan-v2",
        ),
        pytest.param(
            "bedrock_cohere",
            {},
            1024,
            id="bedrock_cohere",
        ),
    ],
)

@ pytest.mark.asyncio(scope="module")
class TestEmbeddingService(EmbeddingServiceTestBase):
    """Test embedding service with memory.

    This tests if the embedding service can be used with the semantic memory.
    """

    async def test_embedding_service(
        self,
        service_id,
        services: dict[str, tuple[EmbeddingGeneratorBase, type[PromptExecutionSettings]]],
        execution_settings_kwargs: dict[str, Any],
        output_dimensionality: int,
    ):
        embedding_generator, settings_type= services[service_id]
        embeddings= await embedding_generator.generate_embeddings(
            texts=["Hello, world!", "Hello, universe!"],
            settings=settings_type(**execution_settings_kwargs),
        )

        assert embeddings.shape == (2, output_dimensionality)
