#!/usr/bin/env python3
"""
Structured Output Schema module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import Any


def generate_structured_output_response_format_schema(name: str, schema: dict[str, Any]) -> dict[str, Any]:
    """Generate the structured output response format schema."""
    return {
        "type": "json_schema",
        "json_schema": {"name": name, "strict": True, "schema": schema},
    }
