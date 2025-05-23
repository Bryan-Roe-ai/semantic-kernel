# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class RestApiExpectedResponse:
    """RestApiExpectedResponse."""

<<<<<<< HEAD:python/semantic_kernel/connectors/openapi_plugin/models/rest_api_operation_expected_response.py
    def __init__(
        self, description: str, media_type: str, schema: dict[str, str] | None = None
    ):
        """Initialize the RestApiOperationExpectedResponse."""
=======
    def __init__(self, description: str, media_type: str, schema: dict[str, str] | None = None):
        """Initialize the RestApiExpectedResponse."""
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377:python/semantic_kernel/connectors/openapi_plugin/models/rest_api_expected_response.py
        self.description = description
        self.media_type = media_type
        self.schema = schema
