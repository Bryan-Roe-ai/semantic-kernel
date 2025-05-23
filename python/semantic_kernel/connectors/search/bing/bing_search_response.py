# Copyright (c) Microsoft. All rights reserved.

from typing import Any

from pydantic import Field

from semantic_kernel.connectors.search.bing.bing_web_page import BingWebPage
from semantic_kernel.kernel_pydantic import KernelBaseModel
<<<<<<< HEAD
<<<<<<< HEAD


=======
from semantic_kernel.utils.experimental_decorator import experimental_class


@experimental_class
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
=======
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
class BingWebPages(KernelBaseModel):
    """The web pages from a Bing search."""

    id: str | None = None
    some_results_removed: bool | None = Field(default=None, alias="someResultsRemoved")
    total_estimated_matches: int | None = Field(default=None, alias="totalEstimatedMatches")
    web_search_url: str | None = Field(default=None, alias="webSearchUrl")
    value: list[BingWebPage] = Field(default_factory=list)


<<<<<<< HEAD
<<<<<<< HEAD
=======
@experimental_class
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
=======
@experimental
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
class BingSearchResponse(KernelBaseModel):
    """The response from a Bing search."""

    type_: str = Field(default="", alias="_type")
    query_context: dict[str, Any] = Field(default_factory=dict, validation_alias="queryContext")
    web_pages: BingWebPages | None = Field(default=None, alias="webPages")
