#!/usr/bin/env python3
"""
Chat Completion Agent Summary History Reducer Single Agent module

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
import logging

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistorySummarizationReducer

"""
The following sample demonstrates how to implement a truncation chat 
history reducer as part of the Semantic Kernel Agent Framework. For 
this sample, a single ChatCompletionAgent is used.
"""


# Initialize the logger for debugging and information messages
logger = logging.getLogger(__name__)


async def main():
    # Setup necessary parameters
    reducer_msg_count = 10
    reducer_threshold = 10

    # Create a summarization reducer
    history_summarization_reducer = ChatHistorySummarizationReducer(
        service=AzureChatCompletion(), target_count=reducer_msg_count, threshold_count=reducer_threshold
    )

    thread: ChatHistoryAgentThread = ChatHistoryAgentThread(chat_history=history_summarization_reducer)

    # Create our agent
    agent = ChatCompletionAgent(
        name="NumeroTranslator",
        instructions="Add one to the latest user number and spell it in Spanish without explanation.",
        service=AzureChatCompletion(),
    )

    # Number of messages to simulate
    message_count = 50
    for index in range(1, message_count + 1, 2):
        print(f"# User: '{index}'")

        # Get agent response and store it
        response = await agent.get_response(messages=str(index), thread=thread)
        thread = response.thread
        print(f"# Agent - {response.name}: '{response.content}'")

        # Attempt reduction
        is_reduced = await thread.reduce()
        if is_reduced:
            print(f"@ History reduced to {len(thread)} messages.")

        print(f"@ Message Count: {len(thread)}\n")

        # If reduced, print summary if present
        if is_reduced:
            async for msg in thread.get_messages():
                if msg.metadata and msg.metadata.get("__summary__"):
                    print(f"\tSummary: {msg.content}")
                    break


if __name__ == "__main__":
    asyncio.run(main())
