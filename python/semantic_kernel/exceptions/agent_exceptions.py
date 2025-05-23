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
<<<<<<< main
=======

    pass


class AgentChatException(AgentException):
    """An error occurred while invoking the agent chat."""

    pass
<<<<<<< HEAD
>>>>>>> Stashed changes
=======


class AgentChatHistoryReducerException(AgentException):
    """An error occurred while reducing the chat history."""

    pass


class AgentThreadInitializationException(AgentException):
    """An error occurred while initializing the agent thread."""

    pass


class AgentThreadOperationException(AgentException):
    """An error occurred while performing an operation on the agent thread."""

    pass
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
