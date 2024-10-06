# Copyright (c) Microsoft. All rights reserved.

import logging
import sys
from collections.abc import AsyncGenerator, AsyncIterator, Mapping
from typing import TYPE_CHECKING, Any

if sys.version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from ollama import AsyncClient
from pydantic import ValidationError

from semantic_kernel.connectors.ai.ollama.ollama_prompt_execution_settings import (
    OllamaTextPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.ollama.ollama_settings import OllamaSettings
from semantic_kernel.connectors.ai.ollama.services.ollama_base import OllamaBase
from semantic_kernel.connectors.ai.text_completion_client_base import (
    TextCompletionClientBase,
)
from semantic_kernel.contents.streaming_text_content import StreamingTextContent
from semantic_kernel.contents.text_content import TextContent
<<<<<<< main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
<<<<<<< main
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
from semantic_kernel.exceptions.service_exceptions import (
    ServiceInitializationError,
    ServiceInvalidResponseError,
)
=======
from semantic_kernel.exceptions.service_exceptions import ServiceInitializationError, ServiceInvalidResponseError
from semantic_kernel.utils.telemetry.model_diagnostics.decorators import trace_text_completion
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> upstream/main
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
>>>>>>> upstream/main
=======
<<<<<<< main
>>>>>>> upstream/main
=======
>>>>>>> ms/features/bugbash-prep
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

if TYPE_CHECKING:
    from semantic_kernel.connectors.ai.prompt_execution_settings import (
        PromptExecutionSettings,
    )
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
=======
>>>>>>> ms/small_fixes
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

logger: logging.Logger = logging.getLogger(__name__)


<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
class OllamaTextCompletion(OllamaBase, TextCompletionClientBase):
    """Initializes a new instance of the OllamaTextCompletion class.
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
class OllamaTextCompletion(OllamaBase, TextCompletionClientBase):
    """Initializes a new instance of the OllamaTextCompletion class.
=======
<<<<<<< main
class OllamaTextCompletion(OllamaBase, TextCompletionClientBase):
    """Initializes a new instance of the OllamaTextCompletion class.
=======
class OllamaTextCompletion(TextCompletionClientBase):
    """
    Initializes a new instance of the OllamaTextCompletion class.
>>>>>>> ms/small_fixes
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

    Make sure to have the ollama service running either locally or remotely.
    """

    def __init__(
        self,
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
<<<<<<< main
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        service_id: str | None = None,
        ai_model_id: str | None = None,
        host: str | None = None,
        client: AsyncClient | None = None,
        env_file_path: str | None = None,
        env_file_encoding: str | None = None,
    ) -> None:
        """Initialize an OllamaChatCompletion service.

        Args:
            service_id (Optional[str]): Service ID tied to the execution settings. (Optional)
            ai_model_id (Optional[str]): The model name. (Optional)
            host (Optional[str]): URL of the Ollama server, defaults to None and
                will use the default Ollama service address: http://127.0.0.1:11434. (Optional)
            client (Optional[AsyncClient]): A custom Ollama client to use for the service. (Optional)
            env_file_path (str | None): Use the environment settings file as a fallback to using env vars.
            env_file_encoding (str | None): The encoding of the environment settings file, defaults to 'utf-8'.
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
=======
        prompt: str,
        settings: OllamaTextPromptExecutionSettings,
    ) -> List[TextContent]:
>>>>>>> ms/small_fixes
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        """
        try:
            ollama_settings = OllamaSettings.create(
                model=ai_model_id,
                host=host,
                env_file_path=env_file_path,
                env_file_encoding=env_file_encoding,
            )
        except ValidationError as ex:
            raise ServiceInitializationError(
                "Failed to create Ollama settings.", ex
            ) from ex

        super().__init__(
            service_id=service_id or ollama_settings.model,
            ai_model_id=ollama_settings.model,
            client=client or AsyncClient(host=ollama_settings.host),
        )

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
<<<<<<< main
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    # region Overriding base class methods

    # Override from AIServiceClientBase
    @override
    def get_prompt_execution_settings_class(self) -> type["PromptExecutionSettings"]:
        return OllamaTextPromptExecutionSettings

    @override
    @trace_text_completion(OllamaBase.MODEL_PROVIDER_NAME)
    async def _inner_get_text_contents(
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        self,
        prompt: str,
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
        self,
        prompt: str,
=======
=======
    @override
    @trace_text_completion(OllamaBase.MODEL_PROVIDER_NAME)
    async def get_text_contents(
>>>>>>> ms/features/bugbash-prep
        self,
        prompt: str,
<<<<<<< main
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        settings: "PromptExecutionSettings",
    ) -> list[TextContent]:
        if not isinstance(settings, OllamaTextPromptExecutionSettings):
            settings = self.get_prompt_execution_settings_from_settings(settings)
        assert isinstance(settings, OllamaTextPromptExecutionSettings)  # nosec

        response_object = await self.client.generate(
            model=self.ai_model_id,
            prompt=prompt,
            stream=False,
            **settings.prepare_settings_dict(),
        )

        if not isinstance(response_object, Mapping):
            raise ServiceInvalidResponseError(
                "Invalid response type from Ollama chat completion. "
                f"Expected Mapping but got {type(response_object)}."
            )

        inner_content = response_object
        text = inner_content["response"]
        return [
            TextContent(
                inner_content=inner_content, ai_model_id=self.ai_model_id, text=text
            )
        ]

    @override
    async def _inner_get_streaming_text_contents(
        self,
        prompt: str,
        settings: "PromptExecutionSettings",
    ) -> AsyncGenerator[list[StreamingTextContent], Any]:
        if not isinstance(settings, OllamaTextPromptExecutionSettings):
            settings = self.get_prompt_execution_settings_from_settings(settings)
        assert isinstance(settings, OllamaTextPromptExecutionSettings)  # nosec

        response_object = await self.client.generate(
            model=self.ai_model_id,
            prompt=prompt,
            stream=True,
            **settings.prepare_settings_dict(),
        )

        if not isinstance(response_object, AsyncIterator):
            raise ServiceInvalidResponseError(
                "Invalid response type from Ollama chat completion. "
                f"Expected AsyncIterator but got {type(response_object)}."
            )

        async for part in response_object:
            yield [
                StreamingTextContent(
                    choice_index=0,
                    inner_content=part,
                    ai_model_id=self.ai_model_id,
                    text=part.get("response"),
                )
            ]

    # endregion
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
=======
        settings: OllamaTextPromptExecutionSettings,
    ) -> AsyncIterable[List[StreamingTextContent]]:
        """
        Streams a text completion using a Ollama model.
        Note that this method does not support multiple responses,
        but the result will be a list anyway.

        Arguments:
            prompt {str} -- Prompt to complete.
            settings {OllamaTextPromptExecutionSettings} -- Request settings.

        Yields:
            List[StreamingTextContent] -- Completion result.
        """
        settings.prompt = prompt
        settings.stream = True
        async with AsyncSession(self.session) as session:
            async with session.post(self.url, json=settings.prepare_settings_dict()) as response:
                response.raise_for_status()
                async for line in response.content:
                    body = json.loads(line)
                    if body.get("done") and body.get("response") is None:
                        break
                    yield [
                        StreamingTextContent(
                            choice_index=0, inner_content=body, ai_model_id=self.ai_model_id, text=body.get("response")
                        )
                    ]
                    if body.get("done"):
                        break

    def get_prompt_execution_settings_class(self) -> "OllamaTextPromptExecutionSettings":
        """Get the request settings class."""
        return OllamaTextPromptExecutionSettings
>>>>>>> ms/small_fixes
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
