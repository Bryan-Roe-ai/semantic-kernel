#!/usr/bin/env python3
"""
Text Search module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import logging
from abc import abstractmethod
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, TypeVar

from semantic_kernel.data.kernel_search_result import KernelSearchResult
from semantic_kernel.data.search_base import SearchBase
from semantic_kernel.data.text_search_options import TextSearchOptions
from semantic_kernel.functions.kernel_parameter_metadata import KernelParameterMetadata
from semantic_kernel.utils.experimental_decorator import experimental_class

if TYPE_CHECKING:
    from semantic_kernel.data.search_options_base import SearchOptions
    from semantic_kernel.data.text_search_result import TextSearchResult

import json
import logging
from abc import abstractmethod
from collections.abc import Callable, Sequence
from copy import deepcopy
from typing import Any, Final, Literal, TypeVar, overload

from pydantic import BaseModel, ValidationError

from semantic_kernel.data._shared import (
    DEFAULT_FUNCTION_NAME,
    DEFAULT_PARAMETER_METADATA,
    DEFAULT_RETURN_PARAMETER_METADATA,
    DynamicFilterFunction,
    KernelSearchResults,
    SearchOptions,
    create_options,
    default_dynamic_filter_function,
)
from semantic_kernel.exceptions import TextSearchException
from semantic_kernel.functions.kernel_function import KernelFunction
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.functions.kernel_function_from_method import KernelFunctionFromMethod
from semantic_kernel.functions.kernel_parameter_metadata import KernelParameterMetadata
from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.utils.feature_stage_decorator import experimental

if sys.version_info >= (3, 11):
    from typing import Self  # pragma: no cover
else:
    from typing_extensions import Self  # pragma: no cover

TSearchResult = TypeVar("TSearchResult")
TSearchFilter = TypeVar("TSearchFilter", bound="SearchFilter")
TMapInput = TypeVar("TMapInput")

logger = logging.getLogger(__name__)

@experimental_class
class TextSearch(SearchBase):
    """The base class for all text searches."""

    @abstractmethod
    async def get_text_search_result(
        self, options: "SearchOptions | None" = None, **kwargs: Any
    ) -> "KernelSearchResult[TextSearchResult]":
        """Search for text, returning a KernelSearchResult with TextSearchResults."""
        ...

    @property
    def _search_function_map(self) -> dict[str, Callable[..., Awaitable[KernelSearchResult[Any]]]]:
        """Get the search function map.

        Can be overwritten by subclasses.
        """
        return {
            "search": self.search,
            "get_text_search_result": self.get_text_search_result,
            "get_text_search_results": self.get_text_search_result,
            "get_search_result": self.get_search_result,
            "get_search_results": self.get_search_result,
        }

    @property
    def _get_options_class(self) -> type["SearchOptions"]:
# region: Filters


@experimental
class FilterClauseBase(ABC, KernelBaseModel):
    """A base for all filter clauses."""

    filter_clause_type: ClassVar[str] = "FilterClauseBase"
    field_name: str
    value: Any

    def __str__(self) -> str:
        """Return a string representation of the filter clause."""
        return f"filter_clause_type='{self.filter_clause_type}' field_name='{self.field_name}' value='{self.value}'"


@experimental
class AnyTagsEqualTo(FilterClauseBase):
    """A filter clause for a any tags equals comparison.

    Args:
        field_name: The name of the field containing the list of tags.
        value: The value to compare against the list of tags.
    """

    filter_clause_type: ClassVar[str] = "any_tags_equal_to"


@experimental
class EqualTo(FilterClauseBase):
    """A filter clause for an equals comparison.

    Args:
        field_name: The name of the field to compare.
        value: The value to compare against the field.

    """

    filter_clause_type: ClassVar[str] = "equal_to"


@experimental
class SearchFilter:
    """A filter clause for a search."""

    def __init__(self) -> None:
        """Initialize a new instance of SearchFilter."""
        self.filters: list[FilterClauseBase] = []
        self.group_type = "AND"
        self.equal_to = self.__equal_to

    def __equal_to(self, field_name: str, value: str) -> Self:
        """Add an equals filter clause."""
        self.filters.append(EqualTo(field_name=field_name, value=value))
        return self

    @classmethod
    def equal_to(cls: type[TSearchFilter], field_name: str, value: str) -> TSearchFilter:
        """Add an equals filter clause."""
        filter = cls()
        filter.equal_to(field_name, value)
        return filter

    def __str__(self) -> str:
        """Return a string representation of the filter."""
        return f"{f' {self.group_type} '.join(f'({f!s})' for f in self.filters)}"


# region: Options


@experimental
class SearchOptions(ABC, KernelBaseModel):
    """Options for a search."""

    filter: SearchFilter = Field(default_factory=SearchFilter)
    include_total_count: bool = False


@experimental
class TextSearchOptions(SearchOptions):
    """Options for a text search."""

    top: Annotated[int, Field(gt=0)] = 5
    skip: Annotated[int, Field(ge=0)] = 0
from semantic_kernel.kernel_types import OptionalOneOrList
from semantic_kernel.utils.feature_stage_decorator import release_candidate

logger = logging.getLogger(__name__)

TSearchOptions = TypeVar("TSearchOptions", bound="SearchOptions")

DEFAULT_DESCRIPTION: Final[str] = (
    "Perform a search for content related to the specified query and return string results"
)

# region: Results


@release_candidate
class TextSearchResult(KernelBaseModel):
    """The result of a text search."""

    name: str | None = None
    value: str | None = None
    link: str | None = None


TSearchResult = TypeVar("TSearchResult")


@release_candidate
class TextSearch:
    """The base class for all text searchers."""

    @property
    def options_class(self) -> type["SearchOptions"]:
        """The options class for the search."""
        return TextSearchOptions

    @staticmethod
    def _default_parameter_metadata() -> list[KernelParameterMetadata]:
        """Default parameter metadata for text search functions.

        This function should be overridden when necessary.
        """
        return [
            KernelParameterMetadata(
                name="query",
                description="What to search for.",
                type="str",
                is_required=True,
                type_object=str,
            ),
            KernelParameterMetadata(
                name="count",
                name="top",
                description="Number of results to return.",
                type="int",
                is_required=False,
                default_value=2,
                type_object=int,
            ),
            KernelParameterMetadata(
                name="skip",
                description="Number of results to skip.",
                type="int",
                is_required=False,
                default_value=0,
                type_object=int,
            ),
        ]

    @staticmethod
    def _default_return_parameter_metadata() -> KernelParameterMetadata:
        """Default return parameter metadata for text search functions.

        This function should be overridden by subclasses.
        """
        return KernelParameterMetadata(
            name="results",
            description="The search results.",
            type="list[str]",
            type_object=list,
            is_required=True,
        )
        return SearchOptions

    # region: Public methods

    @overload
    def create_search_function(
        self,
        function_name: str = DEFAULT_FUNCTION_NAME,
        description: str = DEFAULT_DESCRIPTION,
        *,
        output_type: Literal["str"] = "str",
        parameters: list[KernelParameterMetadata] | None = None,
        return_parameter: KernelParameterMetadata | None = None,
        filter: OptionalOneOrList[Callable | str] = None,
        top: int = 5,
        skip: int = 0,
        include_total_count: bool = False,
        filter_update_function: DynamicFilterFunction | None = None,
        string_mapper: Callable[[TSearchResult], str] | None = None,
    ) -> KernelFunction:
        """Create a kernel function from a search function.

        Args:
            output_type: The type of the output, default is "str".
            function_name: The name of the function, to be used in the kernel, default is "search".
            description: The description of the function, a default is provided.
            parameters: The parameters for the function, a list of KernelParameterMetadata.
            return_parameter: The return parameter for the function.
            filter: The filter to use for the search.
            top: The number of results to return.
            skip: The number of results to skip.
            include_total_count: Whether to include the total count of results.
            filter_update_function: A function to update the search filters.
                The function should return the updated filter.
                The default function uses the parameters and the kwargs to update the options.
                Adding equal to filters to the options for all parameters that are not "query".
                As well as adding equal to filters for parameters that have a default value.
            string_mapper: The function to map the search results. (the inner part of the KernelSearchResults type,
                related to which search type you are using) to strings.

        Returns:
            KernelFunction: The kernel function.

        """
        ...

    @overload
    def create_search_function(
        self,
        function_name: str = DEFAULT_FUNCTION_NAME,
        description: str = DEFAULT_DESCRIPTION,
        *,
        output_type: Literal["TextSearchResult"],
        parameters: list[KernelParameterMetadata] | None = None,
        return_parameter: KernelParameterMetadata | None = None,
        filter: OptionalOneOrList[Callable | str] = None,
        top: int = 5,
        skip: int = 0,
        include_total_count: bool = False,
        filter_update_function: DynamicFilterFunction | None = None,
    ) -> KernelFunction:
        """Create a kernel function from a search function.

        Args:
            output_type: The type of the output, in this case TextSearchResult.
            function_name: The name of the function, to be used in the kernel, default is "search".
            description: The description of the function, a default is provided.
            parameters: The parameters for the function, a list of KernelParameterMetadata.
            return_parameter: The return parameter for the function.
            filter: The filter to use for the search.
            top: The number of results to return.
            skip: The number of results to skip.
            include_total_count: Whether to include the total count of results.
            filter_update_function: A function to update the search filters.
                The function should return the updated filter.
                The default function uses the parameters and the kwargs to update the options.
                Adding equal to filters to the options for all parameters that are not "query".
                As well as adding equal to filters for parameters that have a default value.
            string_mapper: The function to map the TextSearchResult  to strings.
                for instance taking the value out of the results and just returning that,
                otherwise a json-like string is returned.

        Returns:
            KernelFunction: The kernel function.

        """
        ...

    @overload
    def create_search_function(
        self,
        function_name: str = DEFAULT_FUNCTION_NAME,
        description: str = DEFAULT_DESCRIPTION,
        *,
        output_type: Literal["Any"],
        parameters: list[KernelParameterMetadata] | None = None,
        return_parameter: KernelParameterMetadata | None = None,
        filter: OptionalOneOrList[Callable | str] = None,
        top: int = 5,
        skip: int = 0,
        include_total_count: bool = False,
        filter_update_function: DynamicFilterFunction | None = None,
    ) -> KernelFunction:
        """Create a kernel function from a search function.

        Args:
            function_name: The name of the function, to be used in the kernel, default is "search".
            description: The description of the function, a default is provided.
            output_type: The type of the output, in this case Any.
                Any means that the results from the store are used directly.
                The string_mapper can then be used to extract certain fields.
            parameters: The parameters for the function, a list of KernelParameterMetadata.
            return_parameter: The return parameter for the function.
            filter: The filter to use for the search.
            top: The number of results to return.
            skip: The number of results to skip.
            include_total_count: Whether to include the total count of results.
            filter_update_function: A function to update the search filters.
                The function should return the updated filter.
                The default function uses the parameters and the kwargs to update the options.
                Adding equal to filters to the options for all parameters that are not "query".
                As well as adding equal to filters for parameters that have a default value.
            string_mapper: The function to map the raw search results to strings.
                When using this from a vector store, your results are of type
                VectorSearchResult[TModel],
                so the string_mapper can be used to extract the fields you want from the result.
                The default is to use the model_dump_json method of the result, which will return a json-like string.

        Returns:
            KernelFunction: The kernel function.
        """
        ...

    def create_search_function(
        self,
        function_name=DEFAULT_FUNCTION_NAME,
        description=DEFAULT_DESCRIPTION,
        *,
        output_type="str",
        parameters=None,
        return_parameter=None,
        filter=None,
        top=5,
        skip=0,
        include_total_count=False,
        filter_update_function=None,
        string_mapper=None,
    ) -> KernelFunction:
        """Create a kernel function from a search function."""
        options = SearchOptions(
            filter=filter,
            skip=skip,
            top=top,
            include_total_count=include_total_count,
        )
        match output_type:
            case "str":
                return self._create_kernel_function(
                    output_type=str,
                    options=options,
                    parameters=parameters,
                    filter_update_function=filter_update_function,
                    return_parameter=return_parameter,
                    function_name=function_name,
                    description=description,
                    string_mapper=string_mapper,
                )
            case "TextSearchResult":
                return self._create_kernel_function(
                    output_type=TextSearchResult,
                    options=options,
                    parameters=parameters,
                    filter_update_function=filter_update_function,
                    return_parameter=return_parameter,
                    function_name=function_name,
                    description=description,
                    string_mapper=string_mapper,
                )
            case "Any":
                return self._create_kernel_function(
                    output_type="Any",
                    options=options,
                    parameters=parameters,
                    filter_update_function=filter_update_function,
                    return_parameter=return_parameter,
                    function_name=function_name,
                    description=description,
                    string_mapper=string_mapper,
                )
            case _:
                raise TextSearchException(
                    f"Unknown output type: {output_type}. Must be 'str', 'TextSearchResult', or 'Any'."
                )

    # endregion
    # region: Private methods

    def _create_kernel_function(
        self,
        output_type: type[str] | type[TSearchResult] | Literal["Any"] = str,
        options: SearchOptions | None = None,
        parameters: list[KernelParameterMetadata] | None = None,
        filter_update_function: DynamicFilterFunction | None = None,
        return_parameter: KernelParameterMetadata | None = None,
        function_name: str = DEFAULT_FUNCTION_NAME,
        description: str = DEFAULT_DESCRIPTION,
        string_mapper: Callable[[TSearchResult], str] | None = None,
    ) -> KernelFunction:
        """Create a kernel function from a search function."""
        update_func = filter_update_function or default_dynamic_filter_function

        @kernel_function(name=function_name, description=description)
        async def search_wrapper(**kwargs: Any) -> Sequence[str]:
            query = kwargs.pop("query", "")
            try:
                inner_options = create_options(SearchOptions, deepcopy(options), **kwargs)
            except ValidationError:
                # this usually only happens when the kwargs are invalid, so blank options in this case.
                inner_options = SearchOptions()
            inner_options.filter = update_func(filter=inner_options.filter, parameters=parameters, **kwargs)
            try:
                results = await self.search(
                    query=query,
                    output_type=output_type,
                    **inner_options.model_dump(exclude_none=True, exclude_defaults=True, exclude_unset=True),
                )
            except Exception as e:
                msg = f"Exception in search function: {e}"
                logger.error(msg)
                raise TextSearchException(msg) from e
            return await self._map_results(results, string_mapper)

        return KernelFunctionFromMethod(
            method=search_wrapper,
            parameters=DEFAULT_PARAMETER_METADATA if parameters is None else parameters,
            return_parameter=return_parameter or DEFAULT_RETURN_PARAMETER_METADATA,
        )

    async def _map_results(
        self,
        results: KernelSearchResults[TSearchResult],
        string_mapper: Callable[[TSearchResult], str] | None = None,
    ) -> list[str]:
        """Map search results to strings."""
        if string_mapper:
            return [string_mapper(result) async for result in results.results]
        return [self._default_map_to_string(result) async for result in results.results]

    @staticmethod
    def _default_map_to_string(result: BaseModel | object) -> str:
        """Default mapping function for text search results."""
        if isinstance(result, BaseModel):
            return result.model_dump_json()
        return result if isinstance(result, str) else json.dumps(result)

    # region: Abstract methods

    @abstractmethod
    async def search(
        self,
        query: str,
        output_type: type[str] | type[TSearchResult] | Literal["Any"] = str,
        **kwargs: Any,
    ) -> "KernelSearchResults[TSearchResult]":
        """Search for text, returning a KernelSearchResult with a list of strings.

        Args:
            query: The query to search for.
            output_type: The type of the output, default is str.
                Can also be TextSearchResult or Any.
            **kwargs: Additional keyword arguments to pass to the search function.

        """
        ...


    @abstractmethod
    async def get_search_results(
        self,
        query: str,
        options: "SearchOptions | None" = None,
        **kwargs: Any,
    ) -> "KernelSearchResults[Any]":
        """Search for text, returning a KernelSearchResult with the results directly from the service."""
        ...
__all__ = [
    "DEFAULT_DESCRIPTION",
    "DEFAULT_FUNCTION_NAME",
    "DEFAULT_PARAMETER_METADATA",
    "DEFAULT_RETURN_PARAMETER_METADATA",
    "DynamicFilterFunction",
    "KernelSearchResults",
    "TextSearch",
    "TextSearchResult",
    "create_options",
    "default_dynamic_filter_function",
]
