# Copyright (c) Microsoft. All rights reserved.

import logging
from html import escape
from typing import Any
from collections.abc import AsyncIterable
from html import escape
from typing import TYPE_CHECKING, Any

from httpx import AsyncClient, HTTPStatusError, RequestError
from pydantic import ValidationError

from semantic_kernel.connectors.search.bing.bing_search_response import BingSearchResponse
from semantic_kernel.connectors.search.bing.bing_search_settings import BingSettings
from semantic_kernel.connectors.search.bing.bing_web_page import BingWebPage
from semantic_kernel.connectors.search.bing.const import (
    DEFAULT_CUSTOM_URL,
    DEFAULT_URL,
    QUERY_PARAMETERS,
)
from semantic_kernel.connectors.search_engine.bing_connector_settings import BingSettings
from semantic_kernel.data.filters.any_tags_equal_to_filter_clause import AnyTagsEqualTo
from semantic_kernel.data.filters.equal_to_filter_clause import EqualTo
from semantic_kernel.data.filters.not_equal_to_filter_clause import NotEqualTo
from semantic_kernel.data.filters.search_filter_base import SearchFilter
from semantic_kernel.data.kernel_search_result import KernelSearchResult
from semantic_kernel.data.text_search import TextSearch
from semantic_kernel.data.text_search_options import TextSearchOptions
from semantic_kernel.data.text_search_result import TextSearchResult
from semantic_kernel.exceptions import ServiceInitializationError, ServiceInvalidRequestError
from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.utils.telemetry.user_agent import SEMANTIC_KERNEL_USER_AGENT

logger: logging.Logger = logging.getLogger(__name__)


from semantic_kernel.data.filter_clauses.any_tags_equal_to_filter_clause import AnyTagsEqualTo
from semantic_kernel.data.filter_clauses.equal_to_filter_clause import EqualTo
from semantic_kernel.data.kernel_search_results import KernelSearchResults
from semantic_kernel.data.text_search import TextSearch
from semantic_kernel.data.text_search.text_search_filter import TextSearchFilter
from semantic_kernel.data.text_search.text_search_options import TextSearchOptions
from semantic_kernel.data.text_search.text_search_result import TextSearchResult
from semantic_kernel.data.text_search import (
    AnyTagsEqualTo,
    EqualTo,
    KernelSearchResults,
    SearchFilter,
    TextSearch,
    TextSearchOptions,
    TextSearchResult,
)
from semantic_kernel.exceptions import ServiceInitializationError, ServiceInvalidRequestError
from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.utils.feature_stage_decorator import experimental
from semantic_kernel.utils.telemetry.user_agent import SEMANTIC_KERNEL_USER_AGENT

if TYPE_CHECKING:
    from semantic_kernel.data.text_search import SearchOptions

logger: logging.Logger = logging.getLogger(__name__)


@experimental_class
@experimental
class BingSearch(KernelBaseModel, TextSearch):
    """A search engine connector that uses the Bing Search API to perform a web search."""

    settings: BingSettings

    def __init__(
        self,
        api_key: str | None = None,
        custom_config: str | None = None,
        env_file_path: str | None = None,
        env_file_encoding: str | None = None,
    ) -> None:
        """Initializes a new instance of the BingConnector class.
        """Initializes a new instance of the Bing Search class.

        Args:
            api_key: The Bing Search API key. If provided, will override
                the value in the env vars or .env file.
            custom_config: The Bing Custom Search instance's unique identifier.
                If provided, will override the value in the env vars or .env file.
            client: Provide a client to use for the Bing Search API.
            env_file_path: The optional path to the .env file. If provided,
                the settings are read from this file path location.
            env_file_encoding: The optional encoding of the .env file.
        """
        try:
            settings = BingSettings(
                api_key=api_key,
                custom_config=custom_config,
                env_file_path=env_file_path,
                env_file_encoding=env_file_encoding,
            )
        except ValidationError as ex:
            raise ServiceInitializationError("Failed to create Bing settings.") from ex

        super().__init__(settings=settings)  # type: ignore[call-arg]

    async def search(self, options: TextSearchOptions | None = None, **kwargs: Any) -> "KernelSearchResult[str]":
        """Search for text, returning a KernelSearchResult with a list of strings."""
        options = self._get_options(options, **kwargs)
        results = await self._inner_search(options=options)
        return KernelSearchResult(
    async def search(
        self, query: str, options: "SearchOptions | None" = None, **kwargs: Any
    ) -> "KernelSearchResults[str]":
        """Search for text, returning a KernelSearchResult with a list of strings."""
        options = self._get_options(options, **kwargs)
        results = await self._inner_search(query=query, options=options)
        return KernelSearchResults(
            results=self._get_result_strings(results),
            total_count=self._get_total_count(results, options),
            metadata=self._get_metadata(results),
        )

    async def get_text_search_result(
        self, options: TextSearchOptions | None = None, **kwargs
    ) -> "KernelSearchResult[TextSearchResult]":
        """Search for text, returning a KernelSearchResult with TextSearchResults."""
        options = self._get_options(options, **kwargs)
        results = await self._inner_search(options=options)
        return KernelSearchResult(
    async def get_text_search_results(
        self, query: str, options: "SearchOptions | None" = None, **kwargs
    ) -> "KernelSearchResults[TextSearchResult]":
        """Search for text, returning a KernelSearchResult with TextSearchResults."""
        options = self._get_options(options, **kwargs)
        results = await self._inner_search(query=query, options=options)
        return KernelSearchResults(
            results=self._get_text_search_results(results),
            total_count=self._get_total_count(results, options),
            metadata=self._get_metadata(results),
        )

    async def get_search_result(
        self, options: TextSearchOptions | None = None, **kwargs
    ) -> "KernelSearchResult[BingWebPage]":
        """Search for text, returning a KernelSearchResult with the results directly from the service."""
        options = self._get_options(options, **kwargs)
        results = await self._inner_search(options=options)
        return KernelSearchResult(
    async def get_search_results(
        self, query: str, options: "SearchOptions | None" = None, **kwargs
    ) -> "KernelSearchResults[BingWebPage]":
        """Search for text, returning a KernelSearchResult with the results directly from the service."""
        options = self._get_options(options, **kwargs)
        results = await self._inner_search(query=query, options=options)
        return KernelSearchResults(
            results=self._get_bing_web_pages(results),
            total_count=self._get_total_count(results, options),
            metadata=self._get_metadata(results),
        )

    def _get_result_strings(self, response: BingSearchResponse) -> list[str]:
        if response.web_pages is None:
            return []
        return [web_page.snippet for web_page in response.web_pages.value if web_page.snippet]

    def _get_text_search_results(self, response: BingSearchResponse) -> list[TextSearchResult]:
        if response.web_pages is None:
            return []
        return [
            TextSearchResult(
    async def _get_result_strings(self, response: BingSearchResponse) -> AsyncIterable[str]:
        if response.web_pages is None:
            return
        for web_page in response.web_pages.value:
            yield web_page.snippet or ""

    async def _get_text_search_results(self, response: BingSearchResponse) -> AsyncIterable[TextSearchResult]:
        if response.web_pages is None:
            return
        for web_page in response.web_pages.value:
            yield TextSearchResult(
                name=web_page.name,
                value=web_page.snippet,
                link=web_page.url,
            )
            for web_page in response.web_pages.value
        ]

    def _get_bing_web_pages(self, response: BingSearchResponse) -> list[BingWebPage]:
        if response.web_pages is None:
            return []
        return response.web_pages.value

    async def _get_bing_web_pages(self, response: BingSearchResponse) -> AsyncIterable[BingWebPage]:
        if response.web_pages is None:
            return
        for val in response.web_pages.value:
            yield val

    def _get_metadata(self, response: BingSearchResponse) -> dict[str, Any]:
        return {
            "altered_query": response.query_context.get("alteredQuery"),
        }

    def _get_total_count(self, response: BingSearchResponse, options: TextSearchOptions) -> int | None:
        return (
            None
            if not options.include_total_count
            else response.web_pages.total_estimated_matches or None
            if response.web_pages
            else None
        )

    def _get_options(self, options: TextSearchOptions | None, **kwargs: Any) -> TextSearchOptions:
        if options is not None:
    def _get_options(self, options: "SearchOptions | None", **kwargs: Any) -> TextSearchOptions:
        if options is not None and isinstance(options, TextSearchOptions):
            return options
        try:
            return TextSearchOptions(**kwargs)
        except ValidationError:
            return TextSearchOptions()

    async def _inner_search(self, options: TextSearchOptions) -> BingSearchResponse:
    async def _inner_search(self, query: str, options: TextSearchOptions) -> BingSearchResponse:
        self._validate_options(options)

        logger.info(
            f"Received request for bing web search with \
                params:\nquery: {options.query}\nnum_results: {options.count}\noffset: {options.offset}"
        )

        url = self._get_url()
        params = self._build_request_parameters(options)
                params:\nnum_results: {options.top}\noffset: {options.skip}"
        )

        url = self._get_url()
        params = self._build_request_parameters(query, options)

        logger.info(f"Sending GET request to {url}")

        headers = {
            "Ocp-Apim-Subscription-Key": self.settings.api_key.get_secret_value(),
            "user_agent": SEMANTIC_KERNEL_USER_AGENT,
        }
        try:
            async with AsyncClient() as client:
            async with AsyncClient(timeout=5) as client:

                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                return BingSearchResponse.model_validate_json(response.text)
        except HTTPStatusError as ex:
            logger.error(f"Failed to get search results: {ex}")
            raise ServiceInvalidRequestError("Failed to get search results.") from ex
        except RequestError as ex:
            logger.error(f"Client error occurred: {ex}")
            raise ServiceInvalidRequestError("A client error occurred while getting search results.") from ex
        except Exception as ex:
            logger.error(f"An unexpected error occurred: {ex}")
            raise ServiceInvalidRequestError("An unexpected error occurred while getting search results.") from ex

    def _validate_options(self, options: TextSearchOptions) -> None:
        if options.count >= 50:
            raise ServiceInvalidRequestError("count value must be less than 50.")
        if not options.query:
            raise ServiceInvalidRequestError("query cannot be 'None' or empty.")
        if options.top >= 50:
            raise ServiceInvalidRequestError("count value must be less than 50.")

    def _get_url(self) -> str:
        if not self.settings.custom_config:
            return DEFAULT_URL
        return f"{DEFAULT_CUSTOM_URL}&customConfig={self.settings.custom_config}"

    def _build_request_parameters(self, options: TextSearchOptions) -> dict[str, str | int]:
        params: dict[str, str | int] = {"count": options.count, "offset": options.offset}
        if not options.filter:
            params["q"] = options.query or ""
            return params
        extra_query_params = []
        for filter in options.filter.filters:
            if isinstance(filter, SearchFilter):
    def _build_request_parameters(self, query: str, options: TextSearchOptions) -> dict[str, str | int]:
        params: dict[str, str | int] = {"count": options.top, "offset": options.skip}
        if not options.filter:
            params["q"] = query or ""
            return params
        extra_query_params = []
        for filter in options.filter.filters:
            if isinstance(filter, TextSearchFilter):
            if isinstance(filter, SearchFilter):
                logger.warning("Groups are not supported by Bing search, ignored.")
                continue
            if isinstance(filter, EqualTo):
                if filter.field_name in QUERY_PARAMETERS:
                    params[filter.field_name] = escape(filter.value)
                else:
                    extra_query_params.append(f"{filter.field_name}:{filter.value}")
            if isinstance(filter, NotEqualTo):
                if filter.field_name in QUERY_PARAMETERS:
                    params[filter.field_name] = f"-{escape(filter.value)}"
                else:
                    extra_query_params.append(f"-{filter.field_name}:{filter.value}")
            if isinstance(filter, AnyTagsEqualTo):
                logger.debug("Any tag equals to filter is not supported by Bing Search API.")
        params["q"] = f"{options.query}+{f' {options.filter.group_type} '.join(extra_query_params)}".strip()
            elif isinstance(filter, AnyTagsEqualTo):
                logger.debug("Any tag equals to filter is not supported by Bing Search API.")
        params["q"] = f"{query}+{f' {options.filter.group_type} '.join(extra_query_params)}".strip()
        return params
