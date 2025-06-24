#!/usr/bin/env python3
"""
Nvidia Model Types module

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


class NvidiaModelTypes(Enum):
    """Nvidia model types, can be text, chat or embedding."""

    EMBEDDING = "embedding"
