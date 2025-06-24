#!/usr/bin/env python3
"""
Validation Utils module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import re

from semantic_kernel.utils.feature_stage_decorator import experimental

_AGENT_TYPE_REGEX = re.compile(r"^[\w\-\.]+\Z")


@experimental
def is_valid_agent_type(value: str) -> bool:
    """Check if the agent type is valid."""
    return bool(_AGENT_TYPE_REGEX.match(value))
