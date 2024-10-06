# Copyright (c) Microsoft. All rights reserved.
from enum import Enum
from typing import Final

CHAT_MESSAGE_CONTENT_TAG: Final[str] = "message"
CHAT_HISTORY_TAG: Final[str] = "chat_history"
TEXT_CONTENT_TAG: Final[str] = "text"
IMAGE_CONTENT_TAG: Final[str] = "image"
ANNOTATION_CONTENT_TAG: Final[str] = "annotation"
<<<<<<< HEAD
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
BINARY_CONTENT_TAG: Final[str] = "binary"
FILE_REFERENCE_CONTENT_TAG: Final[str] = "file_reference"
BINARY_CONTENT_TAG: Final[str] = "binary"
=======
<<<<<<< Updated upstream
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
>>>>>>> Stashed changes
BINARY_CONTENT_TAG: Final[str] = "binary"
FILE_REFERENCE_CONTENT_TAG: Final[str] = "file_reference"
BINARY_CONTENT_TAG: Final[str] = "binary"
=======
<<<<<<< Updated upstream
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
STREAMING_ANNOTATION_CONTENT_TAG: Final[str] = "streaming_annotation"
BINARY_CONTENT_TAG: Final[str] = "binary"
FILE_REFERENCE_CONTENT_TAG: Final[str] = "file_reference"
BINARY_CONTENT_TAG: Final[str] = "binary"
STREAMING_FILE_REFERENCE_CONTENT_TAG: Final[str] = "streaming_file_reference"
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< HEAD
>>>>>>> main
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
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
FUNCTION_CALL_CONTENT_TAG: Final[str] = "function_call"
FUNCTION_RESULT_CONTENT_TAG: Final[str] = "function_result"
DISCRIMINATOR_FIELD: Final[str] = "content_type"


class ContentTypes(str, Enum):
    """Content types enumeration."""

    ANNOTATION_CONTENT = ANNOTATION_CONTENT_TAG
    BINARY_CONTENT = BINARY_CONTENT_TAG
    CHAT_MESSAGE_CONTENT = CHAT_MESSAGE_CONTENT_TAG
    IMAGE_CONTENT = IMAGE_CONTENT_TAG
    FILE_REFERENCE_CONTENT = FILE_REFERENCE_CONTENT_TAG
    BINARY_CONTENT = BINARY_CONTENT_TAG
    CHAT_MESSAGE_CONTENT = CHAT_MESSAGE_CONTENT_TAG
    IMAGE_CONTENT = IMAGE_CONTENT_TAG
    FUNCTION_CALL_CONTENT = FUNCTION_CALL_CONTENT_TAG
    FUNCTION_RESULT_CONTENT = FUNCTION_RESULT_CONTENT_TAG
<<<<<<< HEAD
<<<<<<< Updated upstream
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
<<<<<<< HEAD
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
    STREAMING_ANNOTATION_CONTENT = STREAMING_ANNOTATION_CONTENT_TAG
    STREAMING_FILE_REFERENCE_CONTENT = STREAMING_FILE_REFERENCE_CONTENT_TAG
>>>>>>> main
<<<<<<< Updated upstream
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
    STREAMING_ANNOTATION_CONTENT = STREAMING_ANNOTATION_CONTENT_TAG
    STREAMING_FILE_REFERENCE_CONTENT = STREAMING_FILE_REFERENCE_CONTENT_TAG
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    TEXT_CONTENT = TEXT_CONTENT_TAG
