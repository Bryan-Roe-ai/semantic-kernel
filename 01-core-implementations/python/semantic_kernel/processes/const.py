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

END_PROCESS_ID: str = "Microsoft.SemanticKernel.Process.EndStep"


@experimental
class ProcessSupportedComponents(str, Enum):
    """Supported Process Components."""

    Step = "Step"
    Process = "Process"
