import asyncio
import numpy as np
import pytest

from semantic_kernel.memory.volatile_memory_store import VolatileMemoryStore
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.connectors.ai.embedding_generator_base import EmbeddingGeneratorBase

class FakeEmbeddingGenerator(EmbeddingGeneratorBase):
    async def generate_embeddings(self, texts, settings=None, **kwargs) -> np.ndarray:
        vectors = []
        for text in texts:
            ascii_sum = sum(ord(c) for c in text)
            vec = np.array([
                len(text),
                ascii_sum % 10,
                ascii_sum % 100,
            ], dtype=float)
            vectors.append(vec)
        return np.vstack(vectors)

def create_memory() -> SemanticTextMemory:
    storage = VolatileMemoryStore()
    generator = FakeEmbeddingGenerator()
    return SemanticTextMemory(storage=storage, embeddings_generator=generator)

@pytest.mark.asyncio
async def test_retrieval_accuracy():
    memory = create_memory()

    await memory.save_information(collection="aboutMe", id="info1", text="I enjoy hiking")
    await memory.save_information(collection="aboutMe", id="info2", text="I work as a tour guide")
    await memory.save_information(collection="aboutMe", id="info3", text="I visited Iceland last year")

    result = await memory.search(collection="aboutMe", query="hiking", limit=1)
    assert result[0].text == "I enjoy hiking"

    result = await memory.search(collection="aboutMe", query="tour", limit=1)
    assert result[0].text == "I work as a tour guide"

    result = await memory.search(collection="aboutMe", query="Iceland", limit=1)
    assert result[0].text == "I visited Iceland last year"
