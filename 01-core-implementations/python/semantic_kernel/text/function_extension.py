#!/usr/bin/env python3
"""
Function Extension module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.functions.kernel_function import KernelFunction
from semantic_kernel.kernel import Kernel

async def aggregate_chunked_results(

    func: KernelFunction,
    chunked_results: list[str],
    kernel: Kernel,
    arguments: KernelArguments,
) -> str:
    """Aggregate the results from the chunked results."""

    func: KernelFunction, chunked_results: List[str], kernel: Kernel, arguments: KernelArguments
) -> str:
    """
    Aggregate the results from the chunked results.
    """

    results = []
    for chunk in chunked_results:
        arguments["input"] = chunk
        result = await func.invoke(kernel, arguments)

        results.append(str(result))

    return "\n".join(results)
