#!/usr/bin/env python3
"""
Creating Functions module

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
import os

from samples.sk_service_configurator import add_service
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from semantic_kernel.contents import ChatHistory


async def main():
    # Initialize the kernel
    kernel = Kernel()

    # Import the MathPlugin.
    # <RunningNativeFunction>
    plugins_directory = os.path.join(os.path.dirname(__file__), "plugins")
    math_plugin = kernel.add_plugin(
        parent_directory=plugins_directory, plugin_name="MathPlugin"
    )

    result = await kernel.invoke(
        math_plugin["Sqrt"],
        number1=12,
    )

    print(result)
    # </RunningNativeFunction>

    # <Chat>
    kernel = add_service(kernel, use_chat=True)
    kernel.add_function(
        prompt="""{{$chat_history}}{{$input}}""",
        execution_settings=OpenAIChatPromptExecutionSettings(
            service_id="default",
            temperature=0.0,
            max_tokens=1000,
            function_choice_behavior=FunctionChoiceBehavior.Auto(),
        ),
        plugin_name="Chat",
        function_name="Chat",
        description="Chat with the assistant",
    )
    chat_history = ChatHistory()
    while True:
        try:
            request = input("Your request: ")
        except (KeyboardInterrupt, EOFError):
            break
        if request.lower() == "exit":
            break
        result = await kernel.invoke(
            plugin_name="Chat",
            function_name="Chat",
            input=request,
            chat_history=chat_history,
        )
        print(result)
        chat_history.add_user_message(request)
        chat_history.add_assistant_message(str(result))

    print("\n\nExiting...")
    # </Chat>


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
