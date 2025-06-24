#!/usr/bin/env python3
"""
Const module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


from enum import Enum

from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class OperationExtensions(Enum):
    """The operation extensions."""

    METHOD_KEY = "method"
    OPERATION_KEY = "operation"
    INFO_KEY = "info"
    SECURITY_KEY = "security"
    SERVER_URLS_KEY = "server-urls"
    METADATA_KEY = "operation-extensions"
