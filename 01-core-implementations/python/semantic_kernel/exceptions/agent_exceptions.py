#!/usr/bin/env python3
"""
Agent Exceptions module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.exceptions.kernel_exceptions import KernelException

class AgentException(KernelException):
    """Base class for all agent exceptions."""

class AgentFileNotFoundException(AgentException):
    """The requested file was not found."""

class AgentInitializationException(AgentException):
    """An error occurred while initializing the agent."""

class AgentExecutionException(AgentException):
    """An error occurred while executing the agent."""

class AgentInvokeException(AgentException):
    """An error occurred while invoking the agent."""

    pass

class AgentChatException(AgentException):
    """An error occurred while invoking the agent chat."""

    pass

class AgentChatHistoryReducerException(AgentException):
    """An error occurred while reducing the chat history."""

    pass

class AgentThreadInitializationException(AgentException):
    """An error occurred while initializing the agent thread."""

    pass

class AgentThreadOperationException(AgentException):
    """An error occurred while performing an operation on the agent thread."""

    pass

