#!/usr/bin/env python3
"""
Simplified self critique RAG example.
"""

import asyncio
import semantic_kernel as sk
from semantic_kernel.memory import SemanticTextMemory

COLLECTION_NAME = "about_me"


async def populate_memory(memory: SemanticTextMemory) -> None:
    await memory.save_information(COLLECTION_NAME, id="info1", text="My name is Andrea")
    await memory.save_information(COLLECTION_NAME, id="info2", text="I currently work as a tour guide")
    await memory.save_information(COLLECTION_NAME, id="info3", text="I've been living in Seattle since 2005")
    await memory.save_information(COLLECTION_NAME, id="info4", text="I visited France and Italy five times since 2015")
    await memory.save_information(COLLECTION_NAME, id="info5", text="My family is from New York")


async def main() -> None:
    kernel = sk.Kernel()
    memory = SemanticTextMemory(storage=sk.memory.VolatileMemoryStore())
    await populate_memory(memory)
    result = await memory.search(COLLECTION_NAME, "Where do I live?")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
