# Copyright (c) Microsoft. All rights reserved.

import logging

from collections.abc import Awaitable, Callable, Mapping
from copy import copy

from collections.abc import Awaitable, Callable, Mapping
from copy import copy

from collections.abc import Awaitable, Callable, Mapping
from copy import copy
from typing import Awaitable, Callable, Dict, Mapping, Optional, Union

from typing import Any

from openai import AsyncAzureOpenAI
from pydantic import ConfigDict, validate_call
from pydantic_core import Url

from semantic_kernel.connectors.ai.open_ai.const import DEFAULT_AZURE_API_VERSION
from semantic_kernel.connectors.ai.open_ai.services.open_ai_handler import (
    OpenAIHandler,
    OpenAIModelTypes,
)

from semantic_kernel.const import USER_AGENT
from semantic_kernel.exceptions import ServiceInitializationError
from semantic_kernel.kernel_pydantic import HttpsUrl
from semantic_kernel.utils.telemetry.user_agent import (
    APP_INFO,
    prepend_semantic_kernel_to_user_agent,
)

logger: logging.Logger = logging.getLogger(__name__)

class AzureOpenAIConfigBase(OpenAIHandler):
    """Internal class for configuring a connection to an Azure OpenAI service."""

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def __init__(
        self,
        deployment_name: str,
        ai_model_type: OpenAIModelTypes,
        endpoint: HttpsUrl | None = None,
        base_url: Url | None = None,
        api_version: str = DEFAULT_AZURE_API_VERSION,

        service_id: str | None = None,
        api_key: str | None = None,
        ad_token: str | None = None,
        ad_token_provider: Callable[[], str | Awaitable[str]] | None = None,
        token_endpoint: str | None = None,
        default_headers: Mapping[str, str] | None = None,
        client: AsyncAzureOpenAI | None = None,

    ) -> None:
        """Internal class for configuring a connection to an Azure OpenAI service.

    ) -> None:
        """Internal class for configuring a connection to an Azure OpenAI service.

    ) -> None:
        """Internal class for configuring a connection to an Azure OpenAI service.

        service_id: Optional[str] = None,
        api_key: Optional[str] = None,
        ad_token: Optional[str] = None,
        ad_token_provider: Optional[Callable[[], Union[str, Awaitable[str]]]] = None,
        default_headers: Union[Mapping[str, str], None] = None,
        async_client: Optional[AsyncAzureOpenAI] = None,
    ) -> None:
        """Internal class for configuring a connection to an Azure OpenAI service.

        Arguments:
            deployment_name {str} -- Name of the deployment.
            ai_model_type {OpenAIModelTypes} -- The type of OpenAI model to deploy.
            endpoint {Optional[HttpsUrl]} -- The specific endpoint URL for the deployment. (Optional)
            base_url {Optional[HttpsUrl]} -- The base URL for Azure services. (Optional)
            api_version {str} -- Azure API version. Defaults to the defined DEFAULT_AZURE_API_VERSION.
            api_key {Optional[str]} -- API key for Azure services. (Optional)
            ad_token {Optional[str]} -- Azure AD token for authentication. (Optional)
            ad_token_provider {Optional[Callable[[], Union[str, Awaitable[str]]]]} -- A callable
                or coroutine function providing Azure AD tokens. (Optional)
            default_headers {Union[Mapping[str, str], None]} -- Default headers for HTTP requests. (Optional)
            async_client {Optional[AsyncAzureOpenAI]} -- An existing client to use. (Optional)

        The `validate_call` decorator is used with a configuration that allows arbitrary types.
        This is necessary for types like `HttpsUrl` and `OpenAIModelTypes`.

        Args:
            deployment_name (str): Name of the deployment.
            ai_model_type (OpenAIModelTypes): The type of OpenAI model to deploy.
            endpoint (HttpsUrl): The specific endpoint URL for the deployment. (Optional)
            base_url (Url): The base URL for Azure services. (Optional)
            api_version (str): Azure API version. Defaults to the defined DEFAULT_AZURE_API_VERSION.
            service_id (str): Service ID for the deployment. (Optional)
            api_key (str): API key for Azure services. (Optional)
            ad_token (str): Azure AD token for authentication. (Optional)
            ad_token_provider (Callable[[], Union[str, Awaitable[str]]]): A callable
                or coroutine function providing Azure AD tokens. (Optional)
            token_endpoint (str): Azure AD token endpoint use to get the token. (Optional)
            default_headers (Union[Mapping[str, str], None]): Default headers for HTTP requests. (Optional)
            client (AsyncAzureOpenAI): An existing client to use. (Optional)
            instruction_role (str | None): The role to use for 'instruction' messages, for example, summarization
                prompts could use `developer` or `system`. (Optional)
            kwargs: Additional keyword arguments.

        """
        # Merge APP_INFO into the headers if it exists
        merged_headers = dict(copy(default_headers)) if default_headers else {}
        if APP_INFO:
            merged_headers.update(APP_INFO)
            merged_headers = prepend_semantic_kernel_to_user_agent(merged_headers)

        if not client:
            # If the client is None, the api_key is none, the ad_token is none, and the ad_token_provider is none,
            # then we will attempt to get the ad_token using the default endpoint specified in the Azure OpenAI
            # settings.
            if not api_key and not ad_token_provider and not ad_token and token_endpoint:
                ad_token = get_entra_auth_token(token_endpoint)

            if not api_key and not ad_token and not ad_token_provider:
                raise ServiceInitializationError(
                    "Please provide either api_key, ad_token or ad_token_provider or a client."

                )

            if not base_url:
                if not endpoint:
                    raise ServiceInitializationError(
                        "Please provide an endpoint or a base_url"
                    )
                base_url = HttpsUrl(
                    f"{str(endpoint).rstrip('/')}/openai/deployments/{deployment_name}"

                )

                )

                )

                )

                )

            if not base_url:
                if not endpoint:
                    raise ServiceInitializationError(
                        "Please provide an endpoint or a base_url"
                    )
                base_url = HttpsUrl(
                    f"{str(endpoint).rstrip('/')}/openai/deployments/{deployment_name}"
                )

            client = AsyncAzureOpenAI(
                base_url=str(base_url),
                api_version=api_version,
                api_key=api_key,
                azure_ad_token=ad_token,
                azure_ad_token_provider=ad_token_provider,
                default_headers=merged_headers,
            )

            if not endpoint and not base_url:
                raise ServiceInitializationError("Please provide an endpoint or a base_url")

            args: dict[str, Any] = {
                "default_headers": merged_headers,
            }
            if api_version:
                args["api_version"] = api_version
            if ad_token:
                args["azure_ad_token"] = ad_token
            if ad_token_provider:
                args["azure_ad_token_provider"] = ad_token_provider
            if api_key:
                args["api_key"] = api_key
            if base_url:
                args["base_url"] = str(base_url)
            if endpoint and not base_url:
                args["azure_endpoint"] = str(endpoint)
            # TODO (eavanvalkenburg): Remove the check on model type when the package fixes: https://github.com/openai/openai-python/issues/2120
            if deployment_name and ai_model_type != OpenAIModelTypes.REALTIME:
                args["azure_deployment"] = deployment_name

            if "websocket_base_url" in kwargs:
                args["websocket_base_url"] = kwargs.pop("websocket_base_url")

            client = AsyncAzureOpenAI(**args)

        args = {
            "ai_model_id": deployment_name,
            "client": client,

        args = {
            "ai_model_id": deployment_name,
            "client": async_client,

            "ai_model_type": ai_model_type,
        }
        if service_id:
            args["service_id"] = service_id
        if instruction_role:
            args["instruction_role"] = instruction_role
        super().__init__(**args, **kwargs)

    def to_dict(self) -> dict[str, str]:
        """Convert the configuration to a dictionary."""

    def to_dict(self) -> dict[str, str]:
        """Convert the configuration to a dictionary."""

    def to_dict(self) -> dict[str, str]:
        """Convert the configuration to a dictionary."""

        client_settings = {
            "base_url": str(self.client.base_url),
            "api_version": self.client._custom_query["api-version"],
            "api_key": self.client.api_key,
            "ad_token": getattr(self.client, "_azure_ad_token", None),
            "ad_token_provider": getattr(self.client, "_azure_ad_token_provider", None),
            "default_headers": {
                k: v for k, v in self.client.default_headers.items() if k != USER_AGENT
            },
        }
        base = self.model_dump(
            exclude={
                "prompt_tokens",
                "completion_tokens",
                "total_tokens",
                "api_type",
                "org_id",
                "ai_model_type",
                "service_id",
                "client",
            },
            by_alias=True,
            exclude_none=True,
        )
        base.update(client_settings)
        return base
