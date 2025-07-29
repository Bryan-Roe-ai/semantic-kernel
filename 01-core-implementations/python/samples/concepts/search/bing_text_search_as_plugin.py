#!/usr/bin/env python3
"""
Simplified Bing text search plugin example.
"""

import asyncio

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.search.bing import BingSearch
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import KernelArguments, KernelPlugin, KernelParameterMetadata
from semantic_kernel.connectors.ai import FunctionChoiceBehavior, OpenAIChatPromptExecutionSettings


async def main() -> None:
    kernel = Kernel()
    kernel.add_service(OpenAIChatCompletion(service_id="chat"))

    kernel.add_plugin(
        KernelPlugin.from_text_search_with_search(
            BingSearch(),
            plugin_name="bing",
            description="Get details about Semantic Kernel concepts.",
            parameters=[
                KernelParameterMetadata(
                    name="query",
                    description="The search query.",
                    type="str",
                    is_required=True,
                    type_object=str,
                ),
            ],
        )
    )

    chat_function = kernel.add_function(
        prompt="{{$chat_history}}{{$user_input}}",
        plugin_name="ChatBot",
        function_name="Chat",
    )

    execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="chat",
        max_tokens=2000,
        temperature=0.7,
        top_p=0.8,
        function_choice_behavior=FunctionChoiceBehavior.Auto(auto_invoke=True),
    )

    history = ChatHistory()
    history.add_system_message("You are a chat bot specialized in Semantic Kernel.")
    history.add_user_message("Hi there, who are you?")
    history.add_assistant_message("I am Mosscap, a chat bot. I'm trying to figure out what people need.")

    arguments = KernelArguments(settings=execution_settings)

    user_input = "What is Semantic Kernel?"
    arguments["user_input"] = user_input
    arguments["chat_history"] = history

    result = await kernel.invoke(chat_function, arguments=arguments)
    print(f"Response: {result}")


if __name__ == "__main__":
    asyncio.run(main())
