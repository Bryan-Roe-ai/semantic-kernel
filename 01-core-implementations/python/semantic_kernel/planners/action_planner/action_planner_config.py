#!/usr/bin/env python3
"""
Action Planner Config module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

from typing import List


class ActionPlannerConfig:
    def __init__(
        self,
        excluded_plugins: List[str] = None,
        excluded_functions: List[str] = None,
        max_tokens: int = 1024,
    ):
        self.excluded_plugins: List[str] = excluded_plugins or []
        self.excluded_functions: List[str] = excluded_functions or []
        self.max_tokens: int = max_tokens
