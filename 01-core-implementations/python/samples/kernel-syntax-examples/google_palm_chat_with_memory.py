#!/usr/bin/env python3
"""
Simplified Google PaLM chat with memory example.
"""

import asyncio

import semantic_kernel as sk
import semantic_kernel.connectors.ai.google_palm as sk_gp
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import KernelArguments


async def main() -> None:
    kernel = sk.Kernel()
    apikey = sk.google_palm_settings_from_dot_env()
    palm_chat = sk_gp.GooglePalmChatCompletion("models/chat-bison-001", apikey)
    kernel.add_service(palm_chat)

    chat_function = kernel.create_function_from_prompt(
        prompt="{{$chat_history}}{{$user_input}}",
        function_name="chat",
        plugin_name="chat",
    )

    history = ChatHistory()
    history.add_user_message("Hi there, who are you?")
    history.add_assistant_message("I am an AI assistant.")

    arguments = KernelArguments()
    arguments["chat_history"] = history
    arguments["user_input"] = "Tell me about PaLM"

    result = await kernel.invoke(chat_function, arguments=arguments)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
