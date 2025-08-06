#!/usr/bin/env python3
"""
Simplified ChatGPT API function calling example.
"""

import asyncio
import os
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.functions import KernelArguments
from semantic_kernel.core_plugins import MathPlugin


async def main() -> None:
    kernel = Kernel()
    kernel.add_service(OpenAIChatCompletion(service_id="chat"))

    settings = OpenAIChatPromptExecutionSettings(service_id="chat", max_tokens=2000)

    plugins_directory = os.path.join(os.path.dirname(__file__), "../../plugins")
    kernel.import_plugin(MathPlugin(), plugin_name="math")

    chat_function = kernel.create_function_from_prompt(
        prompt="{{$chat_history}}{{$user_input}}",
        function_name="chat",
        plugin_name="chat",
        prompt_execution_settings=settings,
    )

    arguments = KernelArguments()
    arguments["chat_history"] = []
    arguments["user_input"] = "What is 3 + 3?"

    result = await kernel.invoke(chat_function, arguments=arguments)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
