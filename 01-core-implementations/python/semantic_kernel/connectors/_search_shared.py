#!/usr/bin/env python3
"""
 Search Shared module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


import ast
import sys
from urllib.parse import quote_plus

if sys.version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover


class SearchLambdaVisitor(ast.NodeVisitor):
    """Visitor to parse a lambda function for Brave and Google Search filters."""

    def __init__(self, valid_parameters: list[str]):
        """Initialize the visitor with a list of valid parameters."""
        self.filters: list[dict[str, str]] = []
        self.valid_parameters = valid_parameters

    @override
    def visit_Lambda(self, node):
        self.visit(node.body)

    @override
    def visit_Compare(self, node):
        # Only support x.FIELD == VALUE
        if not (isinstance(node.left, ast.Attribute) and isinstance(node.left.value, ast.Name)):
            raise NotImplementedError("Left side must be x.FIELD.")
        field = node.left.attr
        if not (len(node.ops) == 1 and isinstance(node.ops[0], ast.Eq)):
            raise NotImplementedError("Only == comparisons are supported.")
        right = node.comparators[0]
        if isinstance(right, ast.Constant):
            if right.value is None:
                raise NotImplementedError("None values are not supported.")
            value = str(right.value)
        else:
            raise NotImplementedError("Only constant values are supported on the right side.")
        if field not in self.valid_parameters:
            raise ValueError(f"Field '{field}' is not supported.")
        self.filters.append({field: quote_plus(value)})

    @override
    def visit_BoolOp(self, node):
        if not isinstance(node.op, ast.And):
            raise NotImplementedError("Only 'and' of == comparisons is supported.")
        for v in node.values:
            self.visit(v)
