#!/usr/bin/env python3
"""
Delegate Types module

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


class DelegateTypes(Enum):
    Unknown = 0
    Void = 1
    OutString = 2
    OutTaskString = 3
    InSKContext = 4
    InSKContextOutString = 5
    InSKContextOutTaskString = 6
    ContextSwitchInSKContextOutTaskSKContext = 7
    InString = 8
    InStringOutString = 9
    InStringOutTaskString = 10
    InStringAndContext = 11
    InStringAndContextOutString = 12
    InStringAndContextOutTaskString = 13
    ContextSwitchInStringAndContextOutTaskContext = 14
    InStringOutTask = 15
    InContextOutTask = 16
    InStringAndContextOutTask = 17
    OutTask = 18
