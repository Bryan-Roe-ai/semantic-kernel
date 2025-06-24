#!/usr/bin/env python3
"""
Rag With Text Memory Plugin module

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

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAITextEmbedding,
)
from semantic_kernel.core_plugins import TextMemoryPlugin
from semantic_kernel.memory import SemanticTextMemory, VolatileMemoryStore


async def main():
    kernel = Kernel()

    service_id = "default"
    kernel.add_service(
        OpenAIChatCompletion(service_id=service_id, ai_model_id="gpt-3.5-turbo")
    )
    embedding_gen = OpenAITextEmbedding(
        service_id="ada",
        ai_model_id="text-embedding-ada-002",
    )

    kernel.add_service(embedding_gen)

    memory = SemanticTextMemory(
        storage=VolatileMemoryStore(), embeddings_generator=embedding_gen
    )
    kernel.add_plugin(TextMemoryPlugin(memory), "memory")

    await memory.save_information(
        collection="generic", id="info1", text="My budget for 2024 is $100,000"
    )

    result = await kernel.invoke_prompt(
        function_name="budget",
        plugin_name="BudgetPlugin",
        prompt="{{memory.recall 'budget by year'}} What is my budget for 2024?",
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
