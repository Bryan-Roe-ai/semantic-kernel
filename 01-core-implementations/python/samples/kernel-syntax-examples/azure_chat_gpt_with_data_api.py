#!/usr/bin/env python3
"""
Simplified Azure ChatGPT with data example.
"""

import asyncio

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import KernelArguments


async def main() -> None:
    kernel = Kernel()
    kernel.add_service(OpenAIChatCompletion(service_id="chat"))

    settings = OpenAIChatPromptExecutionSettings(service_id="chat", max_tokens=2000)

    chat_function = kernel.create_function_from_prompt(
        prompt="{{$chat_history}}{{$user_input}}",
        function_name="chat",
        plugin_name="chat",
        prompt_execution_settings=settings,
    )

    chat = ChatHistory()
    chat.add_user_message("Hi there, who are you?")
    chat.add_assistant_message("I am an AI assistant here to answer your questions.")

    arguments = KernelArguments()
    arguments["chat_history"] = chat
    arguments["user_input"] = "What is Semantic Kernel?"

    result = await kernel.invoke(chat_function, arguments=arguments)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
