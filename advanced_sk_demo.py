#!/usr/bin/env python3
"""Advanced Semantic Kernel demo showcasing various features."""

import asyncio
from typing import Annotated

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import kernel_function


class MathPlugin:
    """A simple math plugin for demonstration."""

    @kernel_function(name="add", description="Adds two numbers together")
    def add(
        self,
        a: Annotated[float, "The first number"],
        b: Annotated[float, "The second number"],
    ) -> Annotated[float, "The sum of the two numbers"]:
        """Add two numbers."""
        result = a + b
        print(f"  [MathPlugin.add] {a} + {b} = {result}")
        return result

    @kernel_function(name="multiply", description="Multiplies two numbers together")
    def multiply(
        self,
        a: Annotated[float, "The first number"],
        b: Annotated[float, "The second number"],
    ) -> Annotated[float, "The product of the two numbers"]:
        """Multiply two numbers."""
        result = a * b
        print(f"  [MathPlugin.multiply] {a} * {b} = {result}")
        return result


class TimePlugin:
    """A simple time/date plugin for demonstration."""

    @kernel_function(
        name="get_current_time", description="Gets the current date and time"
    )
    def get_current_time(self) -> Annotated[str, "The current date and time"]:
        """Get current time."""
        from datetime import datetime

        result = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"  [TimePlugin.get_current_time] Current time: {result}")
        return result


async def demo_basic_chat():
    """Demo 1: Basic chat completion without plugins."""
    print("\n" + "=" * 60)
    print("DEMO 1: Basic Chat Completion")
    print("=" * 60)

    kernel = Kernel()
    service = OllamaChatCompletion(
        ai_model_id="llama3.2",
        host="http://localhost:11434",
    )
    kernel.add_service(service)

    chat_history = ChatHistory()
    chat_history.add_user_message("Write a haiku about coding.")

    print("\n📨 User: Write a haiku about coding.")

    response = await service.get_chat_message_contents(
        chat_history=chat_history,
        settings=service.get_prompt_execution_settings_class()(
            max_tokens=100, temperature=0.8
        ),
    )

    if response:
        print(f"🤖 Assistant: {response[0].content}\n")


async def demo_with_plugins():
    """Demo 2: Using plugins/functions with the agent."""
    print("\n" + "=" * 60)
    print("DEMO 2: Chat with Function Calling (Plugins)")
    print("=" * 60)

    # Import agent classes
    from semantic_kernel.agents import ChatCompletionAgent

    kernel = Kernel()
    service_id = "ollama-chat"
    kernel.add_service(
        OllamaChatCompletion(
            service_id=service_id,
            ai_model_id="llama3.2",
            host="http://localhost:11434",
        )
    )

    # Add plugins
    kernel.add_plugin(MathPlugin(), plugin_name="math")
    kernel.add_plugin(TimePlugin(), plugin_name="time")

    # Create agent with function calling enabled
    agent = ChatCompletionAgent(
        kernel=kernel,
        name="MathBot",
        instructions="You are a helpful assistant with access to math and time functions. Use them when needed.",
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
    )

    # Test with a calculation
    test_query = "What is 15 multiplied by 8, then add 42 to that result?"
    print(f"\n📨 User: {test_query}")
    print("\n[Function calls will be shown below]")

    try:
        response = await agent.get_response(messages=test_query)
        print(f"\n🤖 Assistant: {response.message}\n")
    except Exception as e:
        print(f"\n⚠️  Note: Function calling may not work with llama3.2")
        print(f"   Error: {e}\n")


async def demo_multi_turn_conversation():
    """Demo 3: Multi-turn conversation with context."""
    print("\n" + "=" * 60)
    print("DEMO 3: Multi-turn Conversation")
    print("=" * 60)

    kernel = Kernel()
    service = OllamaChatCompletion(
        ai_model_id="llama3.2",
        host="http://localhost:11434",
    )
    kernel.add_service(service)

    chat_history = ChatHistory()

    # Turn 1
    user_msg_1 = "My favorite color is blue."
    chat_history.add_user_message(user_msg_1)
    print(f"\n📨 User: {user_msg_1}")

    response_1 = await service.get_chat_message_contents(
        chat_history=chat_history,
        settings=service.get_prompt_execution_settings_class()(
            max_tokens=50, temperature=0.7
        ),
    )

    if response_1:
        assistant_msg_1 = response_1[0].content
        chat_history.add_assistant_message(assistant_msg_1)
        print(f"🤖 Assistant: {assistant_msg_1}")

    # Turn 2 - test context retention
    user_msg_2 = "What was my favorite color again?"
    chat_history.add_user_message(user_msg_2)
    print(f"\n📨 User: {user_msg_2}")

    response_2 = await service.get_chat_message_contents(
        chat_history=chat_history,
        settings=service.get_prompt_execution_settings_class()(
            max_tokens=50, temperature=0.7
        ),
    )

    if response_2:
        print(f"🤖 Assistant: {response_2[0].content}\n")


async def demo_streaming():
    """Demo 4: Streaming responses."""
    print("\n" + "=" * 60)
    print("DEMO 4: Streaming Response")
    print("=" * 60)

    kernel = Kernel()
    service = OllamaChatCompletion(
        ai_model_id="llama3.2",
        host="http://localhost:11434",
    )
    kernel.add_service(service)

    chat_history = ChatHistory()
    chat_history.add_user_message("Count from 1 to 5 slowly.")

    print("\n📨 User: Count from 1 to 5 slowly.")
    print("🤖 Assistant (streaming): ", end="", flush=True)

    try:
        async for chunk in service.get_streaming_chat_message_contents(
            chat_history=chat_history,
            settings=service.get_prompt_execution_settings_class()(
                max_tokens=100, temperature=0.7
            ),
        ):
            if chunk:
                for content in chunk:
                    if content.content:
                        print(content.content, end="", flush=True)
        print("\n")
    except Exception as e:
        print(f"\n⚠️  Streaming may not be fully supported: {e}\n")


async def main():
    """Run all demos."""
    print("\n" + "🎯" * 30)
    print("Advanced Semantic Kernel Demo Suite")
    print("🎯" * 30)

    try:
        # Run demos
        await demo_basic_chat()
        await demo_multi_turn_conversation()
        await demo_streaming()
        await demo_with_plugins()

        print("\n" + "=" * 60)
        print("✅ All demos completed!")
        print("=" * 60 + "\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Demos interrupted by user.\n")
    except Exception as e:
        print(f"\n\n❌ Error running demos: {e}\n")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
