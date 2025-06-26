#!/usr/bin/env python3
"""
import asyncio
Agent Channel module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from abc import ABC, abstractmethod
from collections.abc import AsyncIterable
from typing import TYPE_CHECKING, Any

from semantic_kernel.utils.feature_stage_decorator import experimental

if TYPE_CHECKING:
    from semantic_kernel.agents.agent import Agent
    from semantic_kernel.contents.chat_message_content import ChatMessageContent

@experimental
class AgentChannel(ABC):
    """Defines the communication protocol for a particular Agent type.

    An agent provides it own AgentChannel via CreateChannel.
    """

    # My Experiments

    This is a markdown file where I document my experiments.

    ## Experiment 1: Example Experiment

    ### Objective
    Describe the objective of the experiment.

    ### Method
    Outline the steps taken to perform the experiment.

    ### Results
    Document the results of the experiment.

    ### Conclusion
    Summarize the findings and conclusions drawn from the experiment.

    @abstractmethod
    async def receive(
        self,
        history: list["ChatMessageContent"],
    ) -> None:
        """Receive the conversation messages.

        Used when joining a conversation and also during each agent interaction.

        Args:
            history: The history of messages in the conversation.
        """
        ...

    @abstractmethod
    def invoke(
        self,
        agent: "Agent",
        **kwargs: Any,
    ) -> AsyncIterable[tuple[bool, "ChatMessageContent"]]:
        """Perform a discrete incremental interaction between a single Agent and AgentChat.

        Args:
            agent: The agent to interact with.
            kwargs: The keyword arguments.

        Returns:

            A async iterable of a bool, ChatMessageContent.

            A async iterable of a bool, ChatMessageContent.

            A async iterable of a bool, ChatMessageContent.

            A async iterable of a bool, ChatMessageContent.

            An async iterable of a bool, ChatMessageContent.
        """
        ...

    @abstractmethod
    def invoke_stream(
        self,
        agent: "Agent",
        messages: "list[ChatMessageContent]",
        **kwargs: Any,
    ) -> AsyncIterable["ChatMessageContent"]:
        """Perform a discrete incremental stream interaction between a single Agent and AgentChat.

        Args:
            agent: The agent to interact with.
            messages: The history of messages in the conversation.
            kwargs: The keyword arguments.

        Returns:
            An async iterable ChatMessageContent.

        """
        ...

    @abstractmethod
    def get_history(
        self,
    ) -> AsyncIterable["ChatMessageContent"]:
        """Retrieve the message history specific to this channel.

        Returns:
            An async iterable of ChatMessageContent.
        """
        ...

    @abstractmethod
    async def reset(self) -> None:
        """Reset any persistent state associated with the channel."""
        ...

