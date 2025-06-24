#!/usr/bin/env python3
"""
Null Logger module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from logging import Logger, getLogger
from functools import wraps
from typing import Any, Callable

logger: Logger = getLogger(__name__)


def _nullify(fn) -> Callable[[Any], None]:
    """General wrapper to not call wrapped function"""

    @wraps(fn)
    def _inner_nullify(*args, **kwargs) -> None:
        return

    return _inner_nullify


class _NullerMeta(type):
    def __new__(cls, classname, base_classes, class_dict):
        """Return a Class that nullifies all Logger object callbacks"""
        nullified_dict = {attr_name: _nullify(attr) for attr_name, attr in Logger.__dict__.items() if callable(attr)}
        return type.__new__(cls, classname, base_classes, {**class_dict, **nullified_dict})


class NullLogger(Logger, metaclass=_NullerMeta):
    pass
