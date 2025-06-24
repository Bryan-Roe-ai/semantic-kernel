#!/usr/bin/env python3
"""
Food Order Item module

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


class FoodItem(str, Enum):
    POTATO_FRIES = "Potato Fries"
    FRIED_FISH = "Fried Fish"
    FISH_SANDWICH = "Fish Sandwich"
    FISH_AND_CHIPS = "Fish & Chips"

    def to_friendly_string(self) -> str:
        return self.value
