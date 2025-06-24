#!/usr/bin/env python3
"""
Food Ingredients module

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


class FoodIngredients(str, Enum):
    POTATOES = "Potatoes"
    FISH = "Fish"
    BUNS = "Buns"
    SAUCE = "Sauce"
    CONDIMENTS = "Condiments"
    NONE = "None"

    def to_friendly_string(self) -> str:
        return self.value
