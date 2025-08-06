#!/usr/bin/env python3
"""
Simplified memory sample.
"""

import asyncio
import semantic_kernel as sk
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import KernelArguments

async def main() -> None:
    kernel = sk.Kernel()
    kernel.use_memory(storage=sk.memory.VolatileMemoryStore())

    chat_function = kernel.create_function_from_prompt(
        prompt="{{$chat_history}}{{$user_input}}",
        function_name="chat",
        plugin_name="chat",
    )

    history = ChatHistory()
    history.add_user_message("Hi")
    history.add_assistant_message("Hello")

    arguments = KernelArguments()
    arguments["chat_history"] = history
    arguments["user_input"] = "How are you?"

    result = await kernel.invoke(chat_function, arguments=arguments)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
