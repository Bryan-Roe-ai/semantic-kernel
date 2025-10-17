"""
Simple Semantic Kernel Demo
This demonstrates basic SK capabilities with Ollama
"""

import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion
from semantic_kernel.contents import ChatHistory

async def main():
    # Initialize the kernel
    kernel = Kernel()
    
    # Add Ollama chat service
    service_id = "ollama-chat"
    kernel.add_service(
        OllamaChatCompletion(
            service_id=service_id,
            ai_model_id="llama2",  # You can change this to your preferred model
            url="http://localhost:11434"
        )
    )
    
    # Create a chat history
    chat_history = ChatHistory()
    chat_history.add_system_message("You are a helpful AI assistant who specializes in Semantic Kernel.")
    
    print("=" * 50)
    print("Semantic Kernel Demo - Chat with Ollama")
    print("=" * 50)
    print()
    
    # Example conversation
    user_messages = [
        "What is Semantic Kernel?",
        "How does it help with AI integration?",
        "Can you give me a simple use case?"
    ]
    
    chat_service = kernel.get_service(service_id)
    
    for user_msg in user_messages:
        print(f"User: {user_msg}")
        chat_history.add_user_message(user_msg)
        
        # Get response
        response = await chat_service.get_chat_message_content(
            chat_history=chat_history,
            settings=None
        )
        
        print(f"Assistant: {response}")
        print("-" * 50)
        print()
        
        chat_history.add_assistant_message(str(response))

if __name__ == "__main__":
    asyncio.run(main())
