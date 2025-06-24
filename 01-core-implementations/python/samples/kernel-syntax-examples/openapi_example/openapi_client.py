#!/usr/bin/env python3
"""
Openapi Client module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import asyncio

import semantic_kernel as sk
from semantic_kernel.connectors.openapi import register_openapi_plugin

if __name__ == "__main__":
    """Client"""
    kernel = sk.Kernel()

    openapi_plugin = register_openapi_plugin(kernel, "openApiPlugin", "openapi.yaml")

    context_variables = sk.ContextVariables(
        variables={
            "request_body": '{"input": "hello world"}',
            "path_params": '{"name": "mark"}',
            "query_params": '{"q": "0.7"}',
            "headers": '{"Content-Type": "application/json", "Header": "example"}',
        }
    )
    result = asyncio.run(
        # Call the function defined in openapi.yaml
        openapi_plugin["helloWorld"].invoke(variables=context_variables)
    )
    print(result)
