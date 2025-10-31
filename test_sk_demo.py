#!/usr/bin/env python3
"""Quick test script for the Semantic Kernel demo."""

import asyncio

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion
from semantic_kernel.contents import ChatHistory


async def test_sk_demo():
    """Test the Semantic Kernel demo with a simple query."""

    print("🧪 Testing Semantic Kernel Demo...")
    print("=" * 50)

    # Set up kernel with simpler configuration
    kernel = Kernel()
    service_id = "ollama-chat"
    service = OllamaChatCompletion(
        service_id=service_id,
        ai_model_id="llama3.2",
        host="http://localhost:11434",
    )
    kernel.add_service(service)

    # Test query with direct chat completion (no agent, no tools)
    test_message = "Say only: Hello! 2+2=4"
    print(f"📨 Sending: {test_message}")
    print()

    try:
        chat_history = ChatHistory()
        chat_history.add_user_message(test_message)

        response = await service.get_chat_message_contents(
            chat_history=chat_history,
            settings=service.get_prompt_execution_settings_class()(
                max_tokens=50, temperature=0.7
            ),
        )

        if response and len(response) > 0:
            print(f"🤖 Response: {response[0].content}")
            print()
            print("✅ Test PASSED! Semantic Kernel is working correctly.")
            return True
        else:
            print("❌ Test FAILED: No response received")
            return False

    except Exception as e:
        print(f"❌ Test FAILED with error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_sk_demo())
    exit(0 if success else 1)
