# Copyright (c) Microsoft. All rights reserved.

import sys
from collections.abc import Awaitable, Callable
from copy import copy
from typing import TYPE_CHECKING, Any

from openai import AsyncAzureOpenAI
from pydantic import ValidationError

from semantic_kernel.agents.open_ai.open_ai_assistant_base import OpenAIAssistantBase
from semantic_kernel.connectors.ai.open_ai.settings.azure_open_ai_settings import (
    AzureOpenAISettings,
)
from semantic_kernel.const import DEFAULT_SERVICE_NAME
from semantic_kernel.agents import OpenAIAssistantAgent
from semantic_kernel.agents.agent import register_agent_type
from semantic_kernel.connectors.ai.open_ai.settings.azure_open_ai_settings import AzureOpenAISettings
from semantic_kernel.exceptions.agent_exceptions import AgentInitializationException
from semantic_kernel.utils.authentication.entra_id_authentication import get_entra_auth_token
from semantic_kernel.utils.experimental_decorator import experimental_class
from semantic_kernel.utils.telemetry.user_agent import (
    APP_INFO,
    prepend_semantic_kernel_to_user_agent,
)
from semantic_kernel.utils.feature_stage_decorator import release_candidate
from semantic_kernel.utils.telemetry.user_agent import APP_INFO, prepend_semantic_kernel_to_user_agent

if TYPE_CHECKING:
    from semantic_kernel.kernel_pydantic import KernelBaseSettings

if sys.version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

if sys.version < "3.11":
    from typing_extensions import Self  # pragma: no cover
else:
    from typing import Self  # type: ignore # pragma: no cover

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

logger: logging.Logger = logging.getLogger(__name__)

@experimental_class
class AzureAssistantAgent(OpenAIAssistantBase):
    """Azure OpenAI Assistant Agent class.

    Provides the ability to interact with Azure OpenAI Assistants.
    """

    # region Agent Initialization

    def __init__(
        self,
        kernel: "Kernel | None" = None,
        service_id: str | None = None,
        deployment_name: str | None = None,
        api_key: str | None = None,
        endpoint: HttpsUrl | None = None,
        api_version: str | None = None,
        ad_token: str | None = None,
        ad_token_provider: Callable[[], str | Awaitable[str]] | None = None,
        client: AsyncAzureOpenAI | None = None,
        default_headers: dict[str, str] | None = None,
        env_file_path: str | None = None,
        env_file_encoding: str | None = None,
        description: str | None = None,
        id: str | None = None,
        instructions: str | None = None,
        name: str | None = None,
        enable_code_interpreter: bool | None = None,
        enable_file_search: bool | None = None,
        enable_json_response: bool | None = None,
        file_ids: list[str] | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        vector_store_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        max_completion_tokens: int | None = None,
        max_prompt_tokens: int | None = None,
        parallel_tool_calls_enabled: bool | None = True,
        truncation_message_count: int | None = None,
        token_endpoint: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize an Azure OpenAI Assistant Agent.

        Args:
            kernel: The Kernel instance. (optional)
            service_id: The service ID. (optional)
            deployment_name: The deployment name. (optional)
            api_key: The Azure OpenAI API key. (optional)
            endpoint: The Azure OpenAI endpoint. (optional)
            api_version: The Azure OpenAI API version. (optional)
            ad_token: The Azure AD token. (optional)
            ad_token_provider: The Azure AD token provider. (optional)
            client: The Azure OpenAI client. (optional)
            default_headers: The default headers. (optional)
            env_file_path: The environment file path. (optional)
            env_file_encoding: The environment file encoding. (optional)
            description: The description. (optional)
            id: The Agent ID. (optional)
            instructions: The Agent instructions. (optional)
            name: The Agent name. (optional)
            enable_code_interpreter: Enable the code interpreter. (optional)
            enable_file_search: Enable the file search. (optional)
            enable_json_response: Enable the JSON response. (optional)
            file_ids: The file IDs. (optional)
            temperature: The temperature. (optional)
            top_p: The top p. (optional)
            vector_store_id: The vector store ID. (optional)
            metadata: The metadata. (optional)
            max_completion_tokens: The maximum completion tokens. (optional)
            max_prompt_tokens: The maximum prompt tokens. (optional)
            parallel_tool_calls_enabled: Enable parallel tool calls. (optional)
            truncation_message_count: The truncation message count. (optional)
            token_endpoint: The Azure AD token endpoint. (optional)
            **kwargs: Additional keyword arguments.

        Raises:
            AgentInitializationError: If the api_key is not provided in the configuration.
        """
        azure_openai_settings = self._create_azure_openai_settings(
            api_key=api_key,
            endpoint=endpoint,
            deployment_name=deployment_name,
            api_version=api_version,
            env_file_path=env_file_path,
            env_file_encoding=env_file_encoding,
            token_endpoint=token_endpoint,
        )

        if not azure_openai_settings.chat_deployment_name:
            raise AgentInitializationError(
                "The Azure OpenAI chat_deployment_name is required."
            )

        if not azure_openai_settings.api_key and not ad_token and not ad_token_provider:
            raise AgentInitializationError(
                "Please provide either api_key, ad_token or ad_token_provider."
            )
            raise AgentInitializationException("The Azure OpenAI chat_deployment_name is required.")

        if not azure_openai_settings.api_key and not ad_token and not ad_token_provider:
            raise AgentInitializationException("Please provide either api_key, ad_token or ad_token_provider.")
            raise AgentInitializationException("The Azure OpenAI chat_deployment_name is required.")

        if (
            client is None
            and azure_openai_settings.api_key is None
            and ad_token_provider is None
            and ad_token is None
            and azure_openai_settings.token_endpoint
        ):
            ad_token = get_entra_auth_token(azure_openai_settings.token_endpoint)

        if not client and not azure_openai_settings.api_key and not ad_token and not ad_token_provider:
            raise AgentInitializationException("Please provide either api_key, ad_token or ad_token_provider.")

        client = self._create_client(
            api_key=(
                azure_openai_settings.api_key.get_secret_value()
                if azure_openai_settings.api_key
                else None
            ),
            endpoint=azure_openai_settings.endpoint,
            api_version=azure_openai_settings.api_version,
            ad_token=ad_token,
            ad_token_provider=ad_token_provider,
            default_headers=default_headers,
        )
        if not client:
            client = self._create_client(
                api_key=azure_openai_settings.api_key.get_secret_value() if azure_openai_settings.api_key else None,
                endpoint=azure_openai_settings.endpoint,
                api_version=azure_openai_settings.api_version,
                ad_token=ad_token,
                ad_token_provider=ad_token_provider,
                default_headers=default_headers,
            )
        client, ad_token = self._setup_client_and_token(
            azure_openai_settings=azure_openai_settings,
            ad_token=ad_token,
            ad_token_provider=ad_token_provider,
            client=client,
            default_headers=default_headers,
        )

        service_id = service_id if service_id else DEFAULT_SERVICE_NAME

        args: dict[str, Any] = {
            "kernel": kernel,
            "ai_model_id": azure_openai_settings.chat_deployment_name,
            "service_id": service_id,
            "client": client,
            "name": name,
            "description": description,
            "instructions": instructions,
            "enable_code_interpreter": enable_code_interpreter,
            "enable_file_search": enable_file_search,
            "enable_json_response": enable_json_response,
            "file_ids": file_ids or [],
            "temperature": temperature,
            "top_p": top_p,
            "vector_store_id": vector_store_id,
            "metadata": metadata or {},
            "max_completion_tokens": max_completion_tokens,
            "max_prompt_tokens": max_prompt_tokens,
            "parallel_tool_calls_enabled": parallel_tool_calls_enabled,
            "truncation_message_count": truncation_message_count,
        }

        if id is not None:
            args["id"] = id
        if kernel is not None:
            args["kernel"] = kernel
        if kwargs:
            args.update(kwargs)

        super().__init__(**args)

    @classmethod
    async def create(
        cls,
        *,
        kernel: "Kernel | None" = None,
        service_id: str | None = None,
        deployment_name: str | None = None,
        api_key: str | None = None,
        endpoint: HttpsUrl | None = None,
        api_version: str | None = None,
        ad_token: str | None = None,
        ad_token_provider: Callable[[], str | Awaitable[str]] | None = None,
        client: AsyncAzureOpenAI | None = None,
        default_headers: dict[str, str] | None = None,
        env_file_path: str | None = None,
        env_file_encoding: str | None = None,
        description: str | None = None,
        id: str | None = None,
        instructions: str | None = None,
        name: str | None = None,
        enable_code_interpreter: bool | None = None,
        code_interpreter_filenames: list[str] | None = None,
        code_interpreter_file_ids: list[str] | None = None,
        enable_file_search: bool | None = None,
        vector_store_filenames: list[str] | None = None,
        vector_store_file_ids: list[str] | None = None,
        enable_json_response: bool | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        vector_store_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        max_completion_tokens: int | None = None,
        max_prompt_tokens: int | None = None,
        parallel_tool_calls_enabled: bool | None = True,
        truncation_message_count: int | None = None,
        token_endpoint: str | None = None,
        **kwargs: Any,
    ) -> "AzureAssistantAgent":
        """Asynchronous class method used to create the OpenAI Assistant Agent.

        Args:
            kernel: The Kernel instance. (optional)
            service_id: The service ID. (optional)
            deployment_name: The deployment name. (optional)
            api_key: The Azure OpenAI API key. (optional)
            endpoint: The Azure OpenAI endpoint. (optional)
            api_version: The Azure OpenAI API version. (optional)
            ad_token: The Azure AD token. (optional)
            ad_token_provider: The Azure AD token provider. (optional)
            client: The Azure OpenAI client. (optional)
            default_headers: The default headers. (optional)
            env_file_path: The environment file path. (optional)
            env_file_encoding: The environment file encoding. (optional)
            description: The description. (optional)
            id: The Agent ID. (optional)
            instructions: The Agent instructions. (optional)
            name: The Agent name. (optional)
            enable_code_interpreter: Enable the code interpreter. (optional)
            code_interpreter_filenames: The filenames/paths to use with the code interpreter. (optional)
            code_interpreter_file_ids: The existing file IDs to use with the code interpreter. (optional)
            enable_file_search: Enable the file search. (optional)
            vector_store_filenames: The filenames/paths for files to use with file search. (optional)
            vector_store_file_ids: The existing file IDs to use with file search. (optional)
            enable_json_response: Enable the JSON response. (optional)
            temperature: The temperature. (optional)
            top_p: The top p. (optional)
            vector_store_id: The vector store ID. (optional)
            metadata: The metadata. (optional)
            max_completion_tokens: The maximum completion tokens. (optional)
            max_prompt_tokens: The maximum prompt tokens. (optional)
            parallel_tool_calls_enabled: Enable parallel tool calls. (optional)
            truncation_message_count: The truncation message count. (optional)
            token_endpoint: The Azure AD token endpoint. (optional)
            **kwargs: Additional keyword arguments.

        Returns:
            An instance of the AzureAssistantAgent
        """
        agent = cls(
            kernel=kernel,
            service_id=service_id,
            deployment_name=deployment_name,
            api_key=api_key,
            endpoint=endpoint,
            api_version=api_version,
            ad_token=ad_token,
            ad_token_provider=ad_token_provider,
            client=client,
            default_headers=default_headers,
            env_file_path=env_file_path,
            env_file_encoding=env_file_encoding,
            description=description,
            id=id,
            instructions=instructions,
            name=name,
            enable_code_interpreter=enable_code_interpreter,
            enable_file_search=enable_file_search,
            enable_json_response=enable_json_response,
            temperature=temperature,
            top_p=top_p,
            vector_store_id=vector_store_id,
            metadata=metadata or {},
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            parallel_tool_calls_enabled=parallel_tool_calls_enabled,
            truncation_message_count=truncation_message_count,
            token_endpoint=token_endpoint,
            **kwargs,
        )

        assistant_create_kwargs: dict[str, Any] = {}

        code_interpreter_file_ids_combined: list[str] = []
        if code_interpreter_file_ids is not None:
            code_interpreter_file_ids_combined.extend(code_interpreter_file_ids)
        if code_interpreter_filenames is not None:
            for file_path in code_interpreter_filenames:
                try:
                    file_id = await agent.add_file(file_path=file_path, purpose="assistants")
                    code_interpreter_file_ids_combined.append(file_id)
                except FileNotFoundError as ex:
                    logger.error(
                        f"Failed to upload code interpreter file with path: `{file_path}` with exception: {ex}"
                    )
                    raise AgentInitializationException("Failed to upload code interpreter files.", ex) from ex
        if code_interpreter_file_ids_combined:
            agent.code_interpreter_file_ids = code_interpreter_file_ids_combined
            assistant_create_kwargs["code_interpreter_file_ids"] = code_interpreter_file_ids_combined

        vector_store_file_ids_combined: list[str] = []
        if vector_store_file_ids is not None:
            vector_store_file_ids_combined.extend(vector_store_file_ids)
        if vector_store_filenames is not None:
            for file_path in vector_store_filenames:
                try:
                    file_id = await agent.add_file(file_path=file_path, purpose="assistants")
                    vector_store_file_ids_combined.append(file_id)
                except FileNotFoundError as ex:
                    logger.error(f"Failed to upload vector store file with path: `{file_path}` with exception: {ex}")
                    raise AgentInitializationException("Failed to upload vector store files.", ex) from ex
        if vector_store_file_ids_combined:
            agent.file_search_file_ids = vector_store_file_ids_combined
            if enable_file_search or agent.enable_file_search:
                vector_store_id = await agent.create_vector_store(file_ids=vector_store_file_ids_combined)
                agent.vector_store_id = vector_store_id
                assistant_create_kwargs["vector_store_id"] = vector_store_id

        agent.assistant = await agent.create_assistant(**assistant_create_kwargs)
        return agent

    @classmethod
    async def retrieve(
        cls,
        *,
        id: str,
        api_key: str | None = None,
        endpoint: HttpsUrl | None = None,
        api_version: str | None = None,
        ad_token: str | None = None,
        ad_token_provider: Callable[[], str | Awaitable[str]] | None = None,
        client: AsyncAzureOpenAI | None = None,
        kernel: "Kernel | None" = None,
        default_headers: dict[str, str] | None = None,
        env_file_path: str | None = None,
        env_file_encoding: str | None = None,
        token_endpoint: str | None = None,
    ) -> "AzureAssistantAgent":
        """Retrieve an assistant by ID.

        Args:
            id: The assistant ID.
            api_key: The Azure OpenAI API key. (optional)
            endpoint: The Azure OpenAI endpoint. (optional)
            api_version: The Azure OpenAI API version. (optional)
            ad_token: The Azure AD token. (optional)
            ad_token_provider: The Azure AD token provider. (optional)
            client: The Azure OpenAI client. (optional)
            kernel: The Kernel instance. (optional)
            default_headers: The default headers. (optional)
            env_file_path: The environment file path. (optional)
            env_file_encoding: The environment file encoding. (optional)
            token_endpoint: The Azure AD token endpoint. (optional)

        Returns:
            An AzureAssistantAgent instance.
        """
        azure_openai_settings = cls._create_azure_openai_settings(
            api_key=api_key,
            endpoint=endpoint,
            deployment_name=None,  # Not required for retrieving an existing assistant
            api_version=api_version,
            env_file_path=env_file_path,
            env_file_encoding=env_file_encoding,
            token_endpoint=token_endpoint,
        )

        client, ad_token = cls._setup_client_and_token(
            azure_openai_settings=azure_openai_settings,
            ad_token=ad_token,
            ad_token_provider=ad_token_provider,
            client=client,
            default_headers=default_headers,
        )

        assistant = await client.beta.assistants.retrieve(id)
        assistant_definition = OpenAIAssistantBase._create_open_ai_assistant_definition(assistant)

        return AzureAssistantAgent(
            kernel=kernel,
            assistant=assistant,
            client=client,
            ad_token=ad_token,
            api_key=api_key,
            endpoint=endpoint,
            api_version=api_version,
            default_headers=default_headers,
            env_file_path=env_file_path,
            env_file_encoding=env_file_encoding,
            token_endpoint=token_endpoint,
            **assistant_definition,
        )
@release_candidate
@register_agent_type("azure_assistant")
class AzureAssistantAgent(OpenAIAssistantAgent):
    """An Azure Assistant Agent class that extends the OpenAI Assistant Agent class."""

    @staticmethod
    @deprecated(
        "setup_resources is deprecated. Use AzureAssistantAgent.create_client() instead. This method will be removed by 2025-06-15."  # noqa: E501
    )
    def setup_resources(
        *,
        ad_token: str | None = None,
        ad_token_provider: Callable[[], str | Awaitable[str]] | None = None,
        api_key: str | None = None,
        api_version: str | None = None,
        base_url: str | None = None,
        default_headers: dict[str, str] | None = None,
        deployment_name: str | None = None,
        endpoint: str | None = None,
        env_file_path: str | None = None,
        env_file_encoding: str | None = None,
        token_scope: str | None = None,
        **kwargs: Any,
    ) -> tuple[AsyncAzureOpenAI, str]:
        """A method to create the Azure OpenAI client and the deployment name/model from the provided arguments.

        Any arguments provided will override the values in the environment variables/environment file.

        Args:
            ad_token: The Microsoft Entra (previously Azure AD) token represented as a string
            ad_token_provider: The Microsoft Entra (previously Azure AD) token provider provided as a callback
            api_key: The API key
            api_version: The API version
            base_url: The base URL in the form https://<resource>.azure.openai.com/openai/deployments/<deployment_name>
            default_headers: The default headers to add to the client
            deployment_name: The deployment name
            endpoint: The endpoint in the form https://<resource>.azure.openai.com
            env_file_path: The environment file path
            env_file_encoding: The environment file encoding, defaults to utf-8
            token_scope: The token scope
            kwargs: Additional keyword arguments

        Returns:
            An Azure OpenAI client instance and the configured deployment name (model)
        """
        try:
            azure_openai_settings = AzureOpenAISettings(
                api_key=api_key,
                base_url=base_url,
                endpoint=endpoint,
                chat_deployment_name=deployment_name,
                api_version=api_version,
                env_file_path=env_file_path,
                env_file_encoding=env_file_encoding,
                token_endpoint=token_scope,
            )
        except ValidationError as exc:
            raise AgentInitializationException(f"Failed to create Azure OpenAI settings: {exc}") from exc

        if (
            azure_openai_settings.api_key is None
            and ad_token_provider is None
            and ad_token is None
            and azure_openai_settings.token_endpoint
        ):
            ad_token = get_entra_auth_token(azure_openai_settings.token_endpoint)

        # If we still have no credentials, we can't proceed
        if not azure_openai_settings.api_key and not ad_token and not ad_token_provider:
            raise AgentInitializationException(
                "Please provide either an api_key, ad_token or ad_token_provider for authentication."
            )

        merged_headers = dict(copy(default_headers)) if default_headers else {}
        if default_headers:
            merged_headers.update(default_headers)
        if APP_INFO:
            merged_headers.update(APP_INFO)
            merged_headers = prepend_semantic_kernel_to_user_agent(merged_headers)

        if not azure_openai_settings.endpoint:
            raise AgentInitializationException("Please provide an Azure OpenAI endpoint")

        if not azure_openai_settings.chat_deployment_name:
            raise AgentInitializationException("Please provide an Azure OpenAI deployment name")

        client = AsyncAzureOpenAI(
            azure_endpoint=str(azure_openai_settings.endpoint),
            api_version=azure_openai_settings.api_version,
            api_key=azure_openai_settings.api_key.get_secret_value() if azure_openai_settings.api_key else None,
            azure_ad_token=ad_token,
            azure_ad_token_provider=ad_token_provider,
            default_headers=merged_headers,
            **kwargs,
        )

    @staticmethod
    def _create_azure_openai_settings(
        api_key: str | None = None,
        endpoint: HttpsUrl | None = None,
        deployment_name: str | None = None,
        api_version: str | None = None,
        env_file_path: str | None = None,
        env_file_encoding: str | None = None,
        token_endpoint: str | None = None,
    ) -> AzureOpenAISettings:
        """Create the Azure OpenAI settings.

        Args:
            api_key: The Azure OpenAI API key.
            endpoint: The Azure OpenAI endpoint.
            deployment_name: The Azure OpenAI chat deployment name.
            api_version: The Azure OpenAI API version.
            env_file_path: The environment file path.
            env_file_encoding: The environment file encoding.
            token_endpoint: The Azure AD token endpoint.

        Returns:
            An instance of the AzureOpenAISettings.
        """
        try:
            azure_openai_settings = AzureOpenAISettings.create(
                api_key=api_key,
                endpoint=endpoint,
                chat_deployment_name=deployment_name,
                api_version=api_version,
                env_file_path=env_file_path,
                env_file_encoding=env_file_encoding,
                token_endpoint=token_endpoint,
            )
        except ValidationError as ex:
            raise AgentInitializationError(
                "Failed to create Azure OpenAI settings.", ex
            ) from ex
            raise AgentInitializationException("Failed to create Azure OpenAI settings.", ex) from ex

        return azure_openai_settings

    async def list_definitions(self) -> AsyncIterable[dict[str, Any]]:
        """List the assistant definitions.

        Yields:
            An AsyncIterable of dictionaries representing the OpenAIAssistantDefinition.
        """
        assistants = await self.client.beta.assistants.list(order="desc")
        for assistant in assistants.data:
            yield self._create_open_ai_assistant_definition(assistant)
            yield OpenAIAssistantBase._create_open_ai_assistant_definition(assistant)

    @classmethod
    async def retrieve(
        cls,
        *,
        id: str,
        api_key: str | None = None,
        endpoint: HttpsUrl | None = None,
        api_version: str | None = None,
        ad_token: str | None = None,
        ad_token_provider: Callable[[], str | Awaitable[str]] | None = None,
        client: AsyncAzureOpenAI | None = None,
        kernel: "Kernel | None" = None,
        default_headers: dict[str, str] | None = None,
        env_file_path: str | None = None,
        env_file_encoding: str | None = None,
    ) -> "AzureAssistantAgent":
        """Retrieve an assistant by ID.

        Args:
            id: The assistant ID.
            api_key: The Azure OpenAI API
            endpoint: The Azure OpenAI endpoint. (optional)
            api_version: The Azure OpenAI API version. (optional)
            ad_token: The Azure AD token. (optional)
            ad_token_provider: The Azure AD token provider. (optional)
            client: The Azure OpenAI client. (optional)
            kernel: The Kernel instance. (optional)
            default_headers: The default headers. (optional)
            env_file_path: The environment file path. (optional)
            env_file_encoding: The environment file encoding. (optional)

        Returns:
            An AzureAssistantAgent instance.
        """
        azure_openai_settings = AzureAssistantAgent._create_azure_openai_settings(
            api_key=api_key,
            endpoint=endpoint,
            api_version=api_version,
            env_file_path=env_file_path,
            env_file_encoding=env_file_encoding,
        )

        if not azure_openai_settings.chat_deployment_name:
            raise AgentInitializationError(
                "The Azure OpenAI chat_deployment_name is required."
            )
        if not azure_openai_settings.api_key and not ad_token and not ad_token_provider:
            raise AgentInitializationError(
                "Please provide either api_key, ad_token or ad_token_provider."
            )
            raise AgentInitializationException("The Azure OpenAI chat_deployment_name is required.")
        if not azure_openai_settings.api_key and not ad_token and not ad_token_provider:
            raise AgentInitializationException("Please provide either api_key, ad_token or ad_token_provider.")
            raise AgentInitializationException("The Azure OpenAI chat_deployment_name is required.")
        if not azure_openai_settings.api_key and not ad_token and not ad_token_provider:
            raise AgentInitializationException("Please provide either api_key, ad_token or ad_token_provider.")
            raise AgentInitializationException("The Azure OpenAI chat_deployment_name is required.")
        if not azure_openai_settings.api_key and not ad_token and not ad_token_provider:
            raise AgentInitializationException("Please provide either api_key, ad_token or ad_token_provider.")
            raise AgentInitializationException("The Azure OpenAI chat_deployment_name is required.")
        if not azure_openai_settings.api_key and not ad_token and not ad_token_provider:
            raise AgentInitializationException("Please provide either api_key, ad_token or ad_token_provider.")

        if not client:
            client = AzureAssistantAgent._create_client(
                api_key=api_key,
                endpoint=endpoint,
                api_version=api_version,
                ad_token=ad_token,
                ad_token_provider=ad_token_provider,
                default_headers=default_headers,
            )
        assistant = await client.beta.assistants.retrieve(id)
        assistant_definition = OpenAIAssistantBase._create_open_ai_assistant_definition(
            assistant
        )
        return AzureAssistantAgent(kernel=kernel, **assistant_definition)
        assistant_definition = OpenAIAssistantBase._create_open_ai_assistant_definition(assistant)
        return AzureAssistantAgent(kernel=kernel, assistant=assistant, **assistant_definition)
        assistant_definition = OpenAIAssistantBase._create_open_ai_assistant_definition(assistant)
        return AzureAssistantAgent(kernel=kernel, assistant=assistant, **assistant_definition)

    # endregion
        return client, azure_openai_settings.chat_deployment_name

    @staticmethod
    def create_client(
        *,
        ad_token: str | None = None,
        ad_token_provider: Callable[[], str | Awaitable[str]] | None = None,
        api_key: str | None = None,
        api_version: str | None = None,
        base_url: str | None = None,
        default_headers: dict[str, str] | None = None,
        deployment_name: str | None = None,
        endpoint: str | None = None,
        env_file_path: str | None = None,
        env_file_encoding: str | None = None,
        token_scope: str | None = None,
        **kwargs: Any,
    ) -> AsyncAzureOpenAI:
        """A method to create the Azure OpenAI client.

        Any arguments provided will override the values in the environment variables/environment file.

        Args:
            ad_token: The Microsoft Entra (previously Azure AD) token represented as a string
            ad_token_provider: The Microsoft Entra (previously Azure AD) token provider provided as a callback
            api_key: The API key
            api_version: The API version
            base_url: The base URL in the form https://<resource>.azure.openai.com/openai/deployments/<deployment_name>
            default_headers: The default headers to add to the client
            deployment_name: The deployment name
            endpoint: The endpoint in the form https://<resource>.azure.openai.com
            env_file_path: The environment file path
            env_file_encoding: The environment file encoding, defaults to utf-8
            token_scope: The token scope
            kwargs: Additional keyword arguments

        Returns:
            An Azure OpenAI client instance.
        """
        try:
            azure_openai_settings = AzureOpenAISettings(
                api_key=api_key,
                base_url=base_url,
                endpoint=endpoint,
                chat_deployment_name=deployment_name,
                api_version=api_version,
                env_file_path=env_file_path,
                env_file_encoding=env_file_encoding,
                token_endpoint=token_scope,
            )
        except ValidationError as exc:
            raise AgentInitializationException(f"Failed to create Azure OpenAI settings: {exc}") from exc

        if (
            azure_openai_settings.api_key is None
            and ad_token_provider is None
            and ad_token is None
            and azure_openai_settings.token_endpoint
        ):
            ad_token = get_entra_auth_token(azure_openai_settings.token_endpoint)

        # If we still have no credentials, we can't proceed
        if not azure_openai_settings.api_key and not ad_token and not ad_token_provider:
            raise AgentInitializationException(
                "Please provide either an api_key, ad_token or ad_token_provider for authentication."
            )

        merged_headers = dict(copy(default_headers)) if default_headers else {}
        if default_headers:
            merged_headers.update(default_headers)
        if APP_INFO:
            merged_headers.update(APP_INFO)
            merged_headers = prepend_semantic_kernel_to_user_agent(merged_headers)

        if not azure_openai_settings.endpoint:
            raise AgentInitializationException("Please provide an Azure OpenAI endpoint")

        if not azure_openai_settings.chat_deployment_name:
            raise AgentInitializationException("Please provide an Azure OpenAI deployment name")

        return AsyncAzureOpenAI(
            azure_endpoint=str(azure_openai_settings.endpoint),
            api_version=azure_openai_settings.api_version,
            api_key=azure_openai_settings.api_key.get_secret_value() if azure_openai_settings.api_key else None,
            azure_ad_token=ad_token,
            azure_ad_token_provider=ad_token_provider,
            default_headers=merged_headers,
            **kwargs,
        )

    @override
    @classmethod
    def resolve_placeholders(
        cls: type[Self],
        yaml_str: str,
        settings: "KernelBaseSettings | None" = None,
        extras: dict[str, Any] | None = None,
    ) -> str:
        """Substitute ${AzureOpenAI:Key} placeholders with fields from AzureOpenAIAgentSettings and extras."""
        import re

        pattern = re.compile(r"\$\{([^}]+)\}")

        # Build the mapping only if settings is provided and valid
        field_mapping: dict[str, Any] = {}

        if settings is None:
            settings = AzureOpenAISettings()

        if not isinstance(settings, AzureOpenAISettings):
            raise AgentInitializationException(f"Expected AzureOpenAISettings, got {type(settings).__name__}")

        field_mapping.update({
            "ChatModelId": cls._get_setting(getattr(settings, "chat_deployment_name", None)),
            "AgentId": cls._get_setting(getattr(settings, "agent_id", None)),
            "ApiKey": cls._get_setting(getattr(settings, "api_key", None)),
            "ApiVersion": cls._get_setting(getattr(settings, "api_version", None)),
            "BaseUrl": cls._get_setting(getattr(settings, "base_url", None)),
            "Endpoint": cls._get_setting(getattr(settings, "endpoint", None)),
            "TokenEndpoint": cls._get_setting(getattr(settings, "token_endpoint", None)),
        })

        if extras:
            field_mapping.update(extras)

        def replacer(match: re.Match[str]) -> str:
            """Replace the matched placeholder with the corresponding value from field_mapping."""
            full_key = match.group(1)  # for example, OpenAI:ApiKey
            section, _, key = full_key.partition(":")
            if section != "AzureOpenAI":
                return match.group(0)

            # Try short key first (ApiKey), then full (OpenAI:ApiKey)
            return str(field_mapping.get(key) or field_mapping.get(full_key) or match.group(0))

        result = pattern.sub(replacer, yaml_str)

        # Safety check for unresolved placeholders
        unresolved = pattern.findall(result)
        if unresolved:
            raise AgentInitializationException(
                f"Unresolved placeholders in spec: {', '.join(f'${{{key}}}' for key in unresolved)}"
            )

        return result

