# Copyright (c) Microsoft. All rights reserved.

from typing import TYPE_CHECKING

from typing import TYPE_CHECKING

from typing import TYPE_CHECKING

from typing import TYPE_CHECKING

from semantic_kernel.connectors.ai.open_ai.contents.azure_chat_message_content import AzureChatMessageContent
from typing import TYPE_CHECKING
from typing import TYPE_CHECKING, List

from semantic_kernel.contents.chat_history import ChatHistory

if TYPE_CHECKING:
    from semantic_kernel.contents.chat_message_content import ChatMessageContent

def store_results(chat_history: ChatHistory, results: list["ChatMessageContent"]):
    """Stores specific results in the context and chat prompt."""
    for message in results:

def store_results(chat_history: ChatHistory, results: list["ChatMessageContent"]):
    """Stores specific results in the context and chat prompt."""
    for message in results:

def store_results(chat_history: ChatHistory, results: list["ChatMessageContent"]):
    """Stores specific results in the context and chat prompt."""
    for message in results:

        chat_history.add_message(message=message)
    return chat_history
