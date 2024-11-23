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


<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
>>>>>>> head
class VectorStoreSearchError(MemoryConnectorException):
    """An error occurred while searching the vector store model."""

    pass


<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< HEAD
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
=======
class VectorStoreSearchError(MemoryConnectorException):
    """An error occurred while searching the vector store model."""

    pass


>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
__all__ = [
    "MemoryConnectorConnectionException",
    "MemoryConnectorException",
    "MemoryConnectorInitializationError",
    "MemoryConnectorResourceNotFound",
    "VectorStoreModelDeserializationException",
    "VectorStoreModelException",
    "VectorStoreModelSerializationException",
    "VectorStoreModelValidationError",
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
    "VectorStoreSearchError",
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
    "VectorStoreSearchError",
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
    "VectorStoreSearchError",
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
    "VectorStoreSearchError",
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
=======
    "VectorStoreSearchError",
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
]
