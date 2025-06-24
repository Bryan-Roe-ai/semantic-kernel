#!/usr/bin/env python3
"""
Static Property module

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


class static_property(staticmethod):
    def __get__(self, obj: Any, obj_type: Any = None) -> Any:
        return super().__get__(obj, obj_type)()
