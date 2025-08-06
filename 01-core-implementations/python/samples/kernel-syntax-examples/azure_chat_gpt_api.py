#!/usr/bin/env python3
"""
Simplified Azure ChatGPT API example.
"""

import asyncio

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import KernelArguments


async def main() -> None:
    kernel = Kernel()
    kernel.add_service(OpenAIChatCompletion(service_id="chat"))

    settings = OpenAIChatPromptExecutionSettings(service_id="chat", max_tokens=2000, temperature=0.7, top_p=0.8)

    chat_function = kernel.create_function_from_prompt(
        prompt="{{$chat_history}}{{$user_input}}",
        function_name="chat",
        plugin_name="chat",
        prompt_execution_settings=settings,
    )

    history = ChatHistory()
    history.add_user_message("Hi there, who are you?")
    history.add_assistant_message("I am Mosscap, a chat bot.")

    arguments = KernelArguments()
    arguments["chat_history"] = history
    arguments["user_input"] = "Tell me about Semantic Kernel"

    result = await kernel.invoke(chat_function, arguments=arguments)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
