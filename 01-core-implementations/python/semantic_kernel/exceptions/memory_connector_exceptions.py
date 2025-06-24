#!/usr/bin/env python3
"""
Memory Connector Exceptions module

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


class MemoryConnectorException(KernelException):
    """Base class for all memory connector exceptions."""


class MemoryConnectorConnectionException(MemoryConnectorException):
    """An error occurred while connecting to the memory connector."""

    pass


class VectorStoreModelException(MemoryConnectorException):
    """Base class for all vector store model exceptions."""


class VectorStoreModelSerializationException(VectorStoreModelException):
    """An error occurred while serializing the vector store model."""


class VectorStoreModelDeserializationException(VectorStoreModelException):
    """An error occurred while deserializing the vector store model."""


class MemoryConnectorInitializationError(MemoryConnectorException):
    """An error occurred while initializing the memory connector."""


class MemoryConnectorResourceNotFound(MemoryConnectorException):
    """The requested resource was not found in the memory connector."""


class VectorStoreModelValidationError(VectorStoreModelException):
    """An error occurred while validating the vector store model."""


class VectorStoreSearchError(MemoryConnectorException):
    """An error occurred while searching the vector store model."""

    pass


class VectorStoreSearchError(MemoryConnectorException):
    """An error occurred while searching the vector store model."""

    pass


__all__ = [
    "MemoryConnectorConnectionException",
    "MemoryConnectorException",
    "MemoryConnectorInitializationError",
    "MemoryConnectorResourceNotFound",
    "VectorStoreModelDeserializationException",
    "VectorStoreModelException",
    "VectorStoreModelSerializationException",
    "VectorStoreModelValidationError",
    "VectorStoreSearchError",
]
