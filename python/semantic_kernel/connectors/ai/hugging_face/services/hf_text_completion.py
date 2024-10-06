# Copyright (c) Microsoft. All rights reserved.

import logging
import sys
from collections.abc import AsyncGenerator
from threading import Thread
from typing import Any, ClassVar, Literal

if sys.version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

import torch
from transformers import AutoTokenizer, TextIteratorStreamer, pipeline

<<<<<<< head
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
<<<<<<< main
=======
=======
>>>>>>> origin/main
<<<<<<< main
=======
from semantic_kernel.connectors.ai.ai_exception import AIException
>>>>>>> ms/small_fixes
<<<<<<< head
>>>>>>> origin/main
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
=======
>>>>>>> origin/main
from semantic_kernel.connectors.ai.hugging_face.hf_prompt_execution_settings import (
    HuggingFacePromptExecutionSettings,
)
from semantic_kernel.connectors.ai.prompt_execution_settings import (
    PromptExecutionSettings,
)
from semantic_kernel.connectors.ai.text_completion_client_base import (
    TextCompletionClientBase,
)
from semantic_kernel.contents.streaming_text_content import StreamingTextContent
from semantic_kernel.contents.text_content import TextContent
<<<<<<< main
<<<<<<< head
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
<<<<<<< main
=======
<<<<<<< main
>>>>>>> origin/main
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
=======
<<<<<<< main
>>>>>>> origin/main
from semantic_kernel.exceptions import (
    ServiceInvalidExecutionSettingsError,
    ServiceResponseException,
)
=======
from semantic_kernel.exceptions import ServiceInvalidExecutionSettingsError, ServiceResponseException
from semantic_kernel.utils.telemetry.model_diagnostics.decorators import trace_text_completion
>>>>>>> upstream/main
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream

logger: logging.Logger = logging.getLogger(__name__)


class HuggingFaceTextCompletion(TextCompletionClientBase):
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main

logger: logging.Logger = logging.getLogger(__name__)
=======
=======
>>>>>>> origin/main
=======

if TYPE_CHECKING:
    from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
>>>>>>> ms/small_fixes
<<<<<<< head
>>>>>>> origin/main

logger: logging.Logger = logging.getLogger(__name__)

<<<<<<< main
class HuggingFaceTextCompletion(TextCompletionClientBase):
=======

class HuggingFaceTextCompletion(TextCompletionClientBase):
<<<<<<< main
>>>>>>> origin/main
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
    """Hugging Face text completion service."""

    MODEL_PROVIDER_NAME: ClassVar[str] = "huggingface"

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
<<<<<<< main
=======
=======
>>>>>>> ms/small_fixes
>>>>>>> origin/main
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
=======

logger: logging.Logger = logging.getLogger(__name__)


class HuggingFaceTextCompletion(TextCompletionClientBase):
<<<<<<< main
    """Hugging Face text completion service."""

    MODEL_PROVIDER_NAME: ClassVar[str] = "huggingface"

=======
>>>>>>> ms/small_fixes
>>>>>>> origin/main
    task: Literal["summarization", "text-generation", "text2text-generation"]
    device: str
    generator: Any

    def __init__(
        self,
        ai_model_id: str,
<<<<<<< head
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
<<<<<<< main
=======
<<<<<<< main
>>>>>>> origin/main
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
=======
<<<<<<< main
>>>>>>> origin/main
        task: str | None = "text2text-generation",
        device: int = -1,
        service_id: str | None = None,
        model_kwargs: dict[str, Any] | None = None,
        pipeline_kwargs: dict[str, Any] | None = None,
<<<<<<< head
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
<<<<<<< main
=======
=======
>>>>>>> origin/main
=======
        task: Optional[str] = "text2text-generation",
        device: Optional[int] = -1,
        service_id: Optional[str] = None,
        model_kwargs: Optional[Dict[str, Any]] = None,
        pipeline_kwargs: Optional[Dict[str, Any]] = None,
>>>>>>> ms/small_fixes
<<<<<<< head
>>>>>>> origin/main
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
=======
>>>>>>> origin/main
    ) -> None:
        """Initializes a new instance of the HuggingFaceTextCompletion class.

        Args:
            ai_model_id (str): Hugging Face model card string, see
                https://huggingface.co/models
<<<<<<< head
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
<<<<<<< main
=======
<<<<<<< main
>>>>>>> origin/main
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
=======
<<<<<<< main
>>>>>>> origin/main
            device (int): Device to run the model on, defaults to CPU, 0+ for GPU,
                -- None if using device_map instead. (If both device and device_map
                are specified, device overrides device_map. If unintended,
                it can lead to unexpected behavior.) (optional)
            service_id (str): Service ID for the AI service. (optional)
            task (str): Model completion task type, options are:
<<<<<<< head
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
<<<<<<< main
=======
=======
>>>>>>> origin/main
=======
            device {Optional[int]} -- Device to run the model on, defaults to CPU, 0+ for GPU,
                                   -- None if using device_map instead. (If both device and device_map
                                      are specified, device overrides device_map. If unintended,
                                      it can lead to unexpected behavior.)
            service_id {Optional[str]} -- Service ID for the AI service.
            task {Optional[str]} -- Model completion task type, options are:
>>>>>>> ms/small_fixes
<<<<<<< head
>>>>>>> origin/main
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
=======
>>>>>>> origin/main
                - summarization: takes a long text and returns a shorter summary.
                - text-generation: takes incomplete text and returns a set of completion candidates.
                - text2text-generation (default): takes an input prompt and returns a completion.
                text2text-generation is the default as it behaves more like GPT-3+. (optional)
            model_kwargs (dict[str, Any]): Additional dictionary of keyword arguments
                passed along to the model's `from_pretrained(..., **model_kwargs)` function. (optional)
            pipeline_kwargs (dict[str, Any]): Additional keyword arguments passed along
                to the specific pipeline init (see the documentation for the corresponding pipeline class
                for possible values). (optional)

        Note that this model will be downloaded from the Hugging Face model hub.
        """
        generator = pipeline(
            task=task,
            model=ai_model_id,
            device=device,
            model_kwargs=model_kwargs,
            **pipeline_kwargs or {},
        )
        resolved_device = (
            f"cuda:{device}" if device >= 0 and torch.cuda.is_available() else "cpu"
        )
        super().__init__(
            service_id=service_id,
            ai_model_id=ai_model_id,
            task=task,
            device=resolved_device,
            generator=generator,
        )

    # region Overriding base class methods
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes

    # Override from AIServiceClientBase
    @override
    def get_prompt_execution_settings_class(self) -> type["PromptExecutionSettings"]:
        return HuggingFacePromptExecutionSettings

    @override
    @trace_text_completion(MODEL_PROVIDER_NAME)
    async def _inner_get_text_contents(
        self,
        prompt: str,
        settings: "PromptExecutionSettings",
    ) -> list[TextContent]:
        if not isinstance(settings, HuggingFacePromptExecutionSettings):
            settings = self.get_prompt_execution_settings_from_settings(settings)
        assert isinstance(settings, HuggingFacePromptExecutionSettings)  # nosec

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
=======

=======

>>>>>>> origin/main
    # Override from AIServiceClientBase
    @override
    def get_prompt_execution_settings_class(self) -> type["PromptExecutionSettings"]:
        return HuggingFacePromptExecutionSettings
<<<<<<< head

    @override
    @trace_text_completion(MODEL_PROVIDER_NAME)
    async def _inner_get_text_contents(
        self,
        prompt: str,
<<<<<<< main
        settings: "PromptExecutionSettings",
    ) -> list[TextContent]:
        if not isinstance(settings, HuggingFacePromptExecutionSettings):
            settings = self.get_prompt_execution_settings_from_settings(settings)
        assert isinstance(settings, HuggingFacePromptExecutionSettings)  # nosec

=======

    @override
    @trace_text_completion(MODEL_PROVIDER_NAME)
    async def _inner_get_text_contents(
        self,
        prompt: str,
<<<<<<< main
        settings: "PromptExecutionSettings",
    ) -> list[TextContent]:
        if not isinstance(settings, HuggingFacePromptExecutionSettings):
            settings = self.get_prompt_execution_settings_from_settings(settings)
        assert isinstance(settings, HuggingFacePromptExecutionSettings)  # nosec

>>>>>>> origin/main
=======
        settings: HuggingFacePromptExecutionSettings,
    ) -> List[TextContent]:
        """
        This is the method that is called from the kernel to get a response from a text-optimized LLM.

        Arguments:
            prompt {str} -- The prompt to send to the LLM.
            settings {HuggingFacePromptExecutionSettings} -- Settings for the request.

        Returns:
            List[TextContent] -- A list of TextContent objects representing the response(s) from the LLM.
        """
>>>>>>> ms/small_fixes
<<<<<<< head
>>>>>>> origin/main
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
=======
>>>>>>> origin/main
        try:
            results = self.generator(prompt, **settings.prepare_settings_dict())
        except Exception as e:
            raise ServiceResponseException("Hugging Face completion failed") from e

        if isinstance(results, list):
            return [self._create_text_content(results, result) for result in results]
        return [self._create_text_content(results, results)]
<<<<<<< head

<<<<<<< main
    def _create_text_content(
        self, response: Any, candidate: dict[str, str]
    ) -> TextContent:
        return TextContent(
            inner_content=response,
            ai_model_id=self.ai_model_id,
            text=candidate[
                "summary_text" if self.task == "summarization" else "generated_text"
            ],
        )

=======

<<<<<<< main
    def _create_text_content(
        self, response: Any, candidate: dict[str, str]
    ) -> TextContent:
        return TextContent(
            inner_content=response,
            ai_model_id=self.ai_model_id,
            text=candidate[
                "summary_text" if self.task == "summarization" else "generated_text"
            ],
        )

>>>>>>> origin/main
    async def get_streaming_text_contents(
=======
    @override
    async def _inner_get_streaming_text_contents(
>>>>>>> upstream/main
        self,
        prompt: str,
<<<<<<< head
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
<<<<<<< main
=======
<<<<<<< main
>>>>>>> origin/main
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
=======
<<<<<<< main
>>>>>>> origin/main
        settings: "PromptExecutionSettings",
    ) -> AsyncGenerator[list[StreamingTextContent], Any]:
        if not isinstance(settings, HuggingFacePromptExecutionSettings):
            settings = self.get_prompt_execution_settings_from_settings(settings)
        assert isinstance(settings, HuggingFacePromptExecutionSettings)  # nosec

<<<<<<< head
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
<<<<<<< main
=======
=======
>>>>>>> origin/main
=======
        settings: HuggingFacePromptExecutionSettings,
    ) -> AsyncIterable[List[StreamingTextContent]]:
        """
        Streams a text completion using a Hugging Face model.
        Note that this method does not support multiple responses.

        Arguments:
            prompt {str} -- Prompt to complete.
            settings {HuggingFacePromptExecutionSettings} -- Request settings.

        Yields:
            List[StreamingTextContent] -- List of StreamingTextContent objects.
        """
>>>>>>> ms/small_fixes
<<<<<<< head
>>>>>>> origin/main
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
=======
>>>>>>> origin/main
        if settings.num_return_sequences > 1:
            raise ServiceInvalidExecutionSettingsError(
                "HuggingFace TextIteratorStreamer does not stream multiple responses in a parsable format."
                " If you need multiple responses, please use the complete method.",
            )
        try:
            streamer = TextIteratorStreamer(
                AutoTokenizer.from_pretrained(self.ai_model_id)
            )
            # See https://github.com/huggingface/transformers/blob/main/src/transformers/generation/streamers.py#L159
            thread = Thread(
                target=self.generator,
                args={prompt},
                kwargs=settings.prepare_settings_dict(streamer=streamer),
            )
            thread.start()

            for new_text in streamer:
                yield [
                    StreamingTextContent(
                        choice_index=0,
                        inner_content=new_text,
                        text=new_text,
                        ai_model_id=self.ai_model_id,
                    )
                ]

            thread.join()
        except Exception as e:
            raise ServiceResponseException("Hugging Face completion failed") from e

    # endregion

    def _create_text_content(self, response: Any, candidate: dict[str, str]) -> TextContent:
        return TextContent(
            inner_content=response,
            ai_model_id=self.ai_model_id,
            text=candidate["summary_text" if self.task == "summarization" else "generated_text"],
        )
