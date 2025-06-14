# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os

from semantic_kernel import Kernel
from semantic_kernel.functions.kernel_arguments import KernelArguments


async def main():
    """Client"""
    kernel = sk.Kernel()

    openapi_plugin = kernel.add_plugin_from_openapi(
        plugin_name="openApiPlugin", openapi_document_path="./openapi.yaml"
    )

    arguments = {
        "request_body": '{"input": "hello world"}',
        "path_params": '{"name": "mark"}',
        "query_params": '{"q": "0.7"}',
        "headers": '{"Content-Type": "application/json", "Header": "example"}',
    }

    kernel_arguments = KernelArguments(**arguments)

    result = await kernel.invoke(
        openapi_plugin["helloWorld"], arguments=kernel_arguments
    )
    """OpenAPI Sample Client"""
    kernel = Kernel()

    spec_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
        "plugins",
        "openapi",
        "openapi.yaml",
    )

    openapi_plugin = kernel.add_plugin_from_openapi(plugin_name="openApiPlugin", openapi_document_path=spec_path)

    arguments = KernelArguments(
        input="hello world",
        name="John",
        q=0.7,
        Header="example-header",
    )

    result = await kernel.invoke(openapi_plugin["helloWorld"], arguments=arguments)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
