#!/usr/bin/env python3
"""
Search module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import importlib

_IMPORTS = {
    "GoogleSearch": ".google",
    "GoogleSearchSettings": ".google",
    "GoogleSearchResult": ".google",
    "GoogleSearchResponse": ".google",
    "GoogleSearchInformation": ".google",
    "BraveSearch": ".brave",
    "BraveSettings": ".brave",
    "BraveWebPages": ".brave",
    "BraveWebPage": ".brave",
    "BraveSearchResponse": ".brave",
}


def __getattr__(name: str):
    if name in _IMPORTS:
        submod_name = _IMPORTS[name]
        module = importlib.import_module(submod_name, package=__name__)
        return getattr(module, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")


def __dir__():
    return list(_IMPORTS.keys())
