#!/usr/bin/env python3
"""
Const module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import Literal

KERNEL_TEMPLATE_FORMAT_NAME_TYPE = Literal["semantic-kernel"]
KERNEL_TEMPLATE_FORMAT_NAME: KERNEL_TEMPLATE_FORMAT_NAME_TYPE = get_args(
    KERNEL_TEMPLATE_FORMAT_NAME_TYPE
)[0]
HANDLEBARS_TEMPLATE_FORMAT_NAME_TYPE = Literal["handlebars"]
HANDLEBARS_TEMPLATE_FORMAT_NAME: HANDLEBARS_TEMPLATE_FORMAT_NAME_TYPE = get_args(
    HANDLEBARS_TEMPLATE_FORMAT_NAME_TYPE
)[0]
JINJA2_TEMPLATE_FORMAT_NAME_TYPE = Literal["jinja2"]
JINJA2_TEMPLATE_FORMAT_NAME: JINJA2_TEMPLATE_FORMAT_NAME_TYPE = get_args(
    JINJA2_TEMPLATE_FORMAT_NAME_TYPE
)[0]

TEMPLATE_FORMAT_TYPES = Literal[
    KERNEL_TEMPLATE_FORMAT_NAME_TYPE,
    HANDLEBARS_TEMPLATE_FORMAT_NAME_TYPE,
    JINJA2_TEMPLATE_FORMAT_NAME_TYPE,
]

