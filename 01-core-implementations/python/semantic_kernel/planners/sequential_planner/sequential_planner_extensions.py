# Copyright (c) Microsoft. All rights reserved.

import logging
import sys
from typing import List, Optional

from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.functions.kernel_function_metadata import KernelFunctionMetadata
from semantic_kernel.kernel import Kernel
from semantic_kernel.kernel_exception import KernelException
from semantic_kernel.memory.memory_query_result import MemoryQueryResult
from semantic_kernel.memory.null_memory import NullMemory
from semantic_kernel.planners.sequential_planner.sequential_planner_config import (
    SequentialPlannerConfig,
)

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated
logger: logging.Logger = logging.getLogger(__name__)


@deprecated("Will be removed in a future version.")
class SequentialPlannerFunctionExtension:
    """Function extension for the sequential planner."""

    @staticmethod
    def to_manual_string(function: KernelFunctionMetadata):
        """Convert the function to a manual string."""
        inputs = [
            f"  - {parameter.name}: {parameter.description}"
            + (
                f" (default value: {parameter.default_value})"
                if parameter.default_value
                else ""
            )
            for parameter in function.parameters
        ]
        inputs = "\n".join(inputs)
        return f"{function.fully_qualified_name}:\n  description: {function.description}\n  inputs:\n  {inputs}"

    @staticmethod
    def to_embedding_string(function: KernelFunctionMetadata):
        """Convert the function to an embedding string."""
        inputs = "\n".join(
            [
                f"    - {parameter.name}: {parameter.description}"
                for parameter in function.parameters
            ]
        )
        return f"{function.name}:\n  description: {function.description}\n  inputs:\n{inputs}"


@deprecated("Will be removed in a future version.")
class SequentialPlannerKernelExtension:
    """Kernel extension for the sequential planner."""

    PLANNER_MEMORY_COLLECTION_NAME = " Planning.KernelFunctionManual"
    PLAN_KERNEL_FUNCTIONS_ARE_REMEMBERED = "Planning.KernelFunctionsAreRemembered"

    @staticmethod
    async def get_functions_manual(
        kernel: "Kernel",
        arguments: KernelArguments,
        semantic_query: str | None = None,
        config: SequentialPlannerConfig = None,
    ) -> str:
        """Get the functions manual."""
        config = config or SequentialPlannerConfig()

        if config.get_available_functions is None:
            functions = await SequentialPlannerKernelExtension.get_available_functions(
                kernel, arguments, config, semantic_query
            )
        else:
            functions = await config.get_available_functions(config, semantic_query)

        return "\n\n".join(
            [
                SequentialPlannerFunctionExtension.to_manual_string(func)
                for func in functions
            ]
        )

    @staticmethod
    async def get_available_functions(
        kernel: Kernel,
        arguments: KernelArguments,
        config: SequentialPlannerConfig,
        semantic_query: str | None = None,
    ):
        """Get the available functions based on the semantic query."""
        excluded_plugins = config.excluded_plugins or []
        excluded_functions = config.excluded_functions or []
        included_functions = config.included_functions or []

        available_functions = [
            func
            for func in kernel.get_list_of_function_metadata(
                {"excluded_plugins": excluded_plugins}
            )
            if func.name not in excluded_functions
        ]

        if semantic_query is None or config.relevancy_threshold is None:
            # If no semantic query is provided, return all available functions.
            # If a Memory provider has not been registered, return all available functions.
            return available_functions

        if kernel.plugins is None:
            raise KernelException(
                KernelException.ErrorCodes.PluginCollectionNotSet,
                "Plugin collection not found in the context",
            )

        available_functions = [
            func
            for func in kernel.plugins.get_list_of_function_metadata()
            if (func.plugin_name not in excluded_plugins and func.name not in excluded_functions)
        ]

        if (
            semantic_query is None
            or not kernel.memory
            or isinstance(kernel.memory, NullMemory)
            or config.relevancy_threshold is None
        ):
            # If no semantic query is provided, return all available functions.
            # If a Memory provider has not been registered, return all available functions.
            return available_functions

        # Add functions that were found in the search results.
        relevant_functions = (
            await SequentialPlannerKernelExtension.get_relevant_functions(
                kernel,
                available_functions,
            )
        )

        # Remember functions in memory so that they can be searched.
        await SequentialPlannerKernelExtension.remember_functions(kernel, arguments, available_functions)

        # Search for functions that match the semantic query.
        memories = await kernel.memory.search(
            SequentialPlannerKernelExtension.PLANNER_MEMORY_COLLECTION_NAME,
            semantic_query,
            config.max_relevant_functions,
            config.relevancy_threshold,
        )

        # Add functions that were found in the search results.
        relevant_functions = await SequentialPlannerKernelExtension.get_relevant_functions(
            kernel, available_functions, memories
        )

        # Add any missing functions that were included but not found in the search results.
        missing_functions = [
            func
            for func in included_functions
            if func not in [func.name for func in relevant_functions]
        ]

        relevant_functions += [
            func for func in available_functions if func.name in missing_functions
        ]

        return sorted(relevant_functions, key=lambda x: (x.plugin_name, x.name))

    @staticmethod
    async def get_relevant_functions(
        kernel: Kernel,
        available_functions: list[KernelFunctionMetadata],
        memories: list[MemoryQueryResult] | None = None,
    ) -> list[KernelFunctionMetadata]:
        """Get relevant functions from the memories."""
        relevant_functions = []
        # TODO (eavanvalkenburg): cancellation
        # https://github.com/microsoft/semantic-kernel/issues/5668
        if memories is None:
            return relevant_functions

        for memory_entry in memories:
            function = next(
                (
                    func
                    for func in available_functions
                    if func.fully_qualified_name == memory_entry.id
                ),
                None,
            )
            if function is not None:
                logger.debug(
                    "Found relevant function. Relevance Score: {}, Function: {}".format(
                        memory_entry.relevance,
                        function.fully_qualified_name,
                    )
                )
                relevant_functions.append(function)

        return relevant_functions

    @staticmethod
    async def remember_functions(
        kernel: Kernel, arguments: KernelArguments, available_functions: List[KernelFunctionMetadata]
    ):
        # Check if the functions have already been saved to memory.
        if arguments.get(SequentialPlannerKernelExtension.PLAN_KERNEL_FUNCTIONS_ARE_REMEMBERED, False):
            return

        if not kernel.memory or isinstance(kernel.memory, NullMemory):
            raise KernelException(
                KernelException.ErrorCodes.FunctionNotAvailable,
                "No memory registered in the kernel. Cannot remember functions.",
            )

        for function in available_functions:
            function_name = SequentialPlannerFunctionViewExtension.to_fully_qualified_name(function)
            key = function_name
            description = function.description or function_name
            text_to_embed = SequentialPlannerFunctionViewExtension.to_embedding_string(function)

            # It'd be nice if there were a saveIfNotExists method on the memory interface
            memory_entry = await kernel.memory.get(
                collection=SequentialPlannerKernelExtension.PLANNER_MEMORY_COLLECTION_NAME,
                key=key,
                with_embedding=False,
            )
            if memory_entry is None:
                # TODO It'd be nice if the minRelevanceScore could be a parameter for each item that was saved to memory
                # As folks may want to tune their functions to be more or less relevant.
                # Memory now supports these such strategies.
                await kernel.memory.save_information(
                    collection=SequentialPlannerKernelExtension.PLANNER_MEMORY_COLLECTION_NAME,
                    text=text_to_embed,
                    id=key,
                    description=description,
                    additional_metadata="",
                )

        # Set a flag to indicate that the functions have been saved to memory.
        arguments[SequentialPlannerKernelExtension.PLAN_KERNEL_FUNCTIONS_ARE_REMEMBERED] = True
