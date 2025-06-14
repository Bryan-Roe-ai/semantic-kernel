# Copyright (c) Microsoft. All rights reserved.

import sys
from collections.abc import AsyncGenerator, Callable
from typing import TYPE_CHECKING, Any, ClassVar, cast

from semantic_kernel.connectors.ai.function_call_choice_configuration import FunctionCallChoiceConfiguration
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.utils.telemetry.model_diagnostics.decorators import trace_chat_completion

if sys.version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from openai import AsyncStream
from openai.types.chat.chat_completion import ChatCompletion, Choice
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk, ChoiceDeltaFunctionCall, ChoiceDeltaToolCall
from openai.types.chat.chat_completion_chunk import Choice as ChunkChoice
from openai.types.chat.chat_completion_message import FunctionCall
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
from typing_extensions import deprecated

from semantic_kernel.connectors.ai.chat_completion_client_base import (
    ChatCompletionClientBase,
)
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.connectors.ai.function_calling_utils import (
from semantic_kernel.connectors.ai.function_calling_utils import (
    update_settings_from_function_call_configuration,
)
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.connectors.ai.function_calling_utils import (
    merge_function_results,
    update_settings_from_function_call_configuration,
)
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior

from semantic_kernel.connectors.ai.function_calling_utils import update_settings_from_function_call_configuration
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior, FunctionChoiceType
from semantic_kernel.connectors.ai.function_calling_utils import update_settings_from_function_call_configuration
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior, FunctionChoiceType
from semantic_kernel.connectors.ai.function_calling_utils import update_settings_from_function_call_configuration
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior, FunctionChoiceType
from semantic_kernel.connectors.ai.function_calling_utils import update_settings_from_function_call_configuration
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior, FunctionChoiceType
from semantic_kernel.connectors.ai.function_calling_utils import (
    update_settings_from_function_call_configuration,
)
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.connectors.ai.open_ai.contents import OpenAIChatMessageContent, OpenAIStreamingChatMessageContent
from semantic_kernel.connectors.ai.open_ai.models.chat_completion.function_call import FunctionCall
from semantic_kernel.connectors.ai.open_ai.models.chat_completion.tool_calls import ToolCall
from semantic_kernel.connectors.ai.open_ai.contents import OpenAIChatMessageContent, OpenAIStreamingChatMessageContent
from semantic_kernel.connectors.ai.open_ai.models.chat_completion.function_call import FunctionCall
from semantic_kernel.connectors.ai.open_ai.models.chat_completion.tool_calls import ToolCall
from semantic_kernel.connectors.ai.open_ai.contents import OpenAIChatMessageContent, OpenAIStreamingChatMessageContent
from semantic_kernel.connectors.ai.open_ai.models.chat_completion.function_call import FunctionCall
from semantic_kernel.connectors.ai.open_ai.models.chat_completion.tool_calls import ToolCall
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import (
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.open_ai.services.open_ai_handler import OpenAIHandler
from semantic_kernel.contents.annotation_content import AnnotationContent
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.file_reference_content import FileReferenceContent
from semantic_kernel.contents.function_call_content import FunctionCallContent
from semantic_kernel.contents.streaming_chat_message_content import (
    StreamingChatMessageContent,
)
from semantic_kernel.contents.streaming_text_content import StreamingTextContent
from semantic_kernel.contents.text_content import TextContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.contents.utils.finish_reason import FinishReason
from semantic_kernel.exceptions import (
    ServiceInvalidExecutionSettingsError,
    ServiceInvalidResponseError,
)
from semantic_kernel.filters.auto_function_invocation.auto_function_invocation_context import (
    AutoFunctionInvocationContext,
)
from semantic_kernel.utils.telemetry.decorators import trace_chat_completion
from semantic_kernel.exceptions import (
    ServiceInvalidExecutionSettingsError,
    ServiceInvalidResponseError,
)
from semantic_kernel.filters.auto_function_invocation.auto_function_invocation_context import (
    AutoFunctionInvocationContext,
)
from semantic_kernel.utils.telemetry.model_diagnostics import trace_chat_completion
from semantic_kernel.contents.chat_role import ChatRole
from semantic_kernel.contents.finish_reason import FinishReason
)
from semantic_kernel.contents.streaming_text_content import StreamingTextContent
from semantic_kernel.contents.text_content import TextContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.contents.utils.finish_reason import FinishReason
from semantic_kernel.exceptions import (
    ServiceInvalidExecutionSettingsError,
    ServiceInvalidResponseError,
)
from semantic_kernel.filters.auto_function_invocation.auto_function_invocation_context import (
    AutoFunctionInvocationContext,
)
from semantic_kernel.utils.telemetry.decorators import trace_chat_completion
from semantic_kernel.exceptions import (
    ServiceInvalidExecutionSettingsError,
    ServiceInvalidResponseError,
)
from semantic_kernel.filters.auto_function_invocation.auto_function_invocation_context import (
    AutoFunctionInvocationContext,
)
from semantic_kernel.utils.telemetry.model_diagnostics import trace_chat_completion
from semantic_kernel.contents.chat_role import ChatRole
from semantic_kernel.contents.finish_reason import FinishReason
)
from semantic_kernel.contents.streaming_text_content import StreamingTextContent
from semantic_kernel.contents.text_content import TextContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.contents.utils.finish_reason import FinishReason
from semantic_kernel.exceptions import (
    ServiceInvalidExecutionSettingsError,
    ServiceInvalidResponseError,
)
from semantic_kernel.filters.auto_function_invocation.auto_function_invocation_context import (
    AutoFunctionInvocationContext,
)
from semantic_kernel.utils.telemetry.decorators import trace_chat_completion
from semantic_kernel.exceptions import (
    ServiceInvalidExecutionSettingsError,
    ServiceInvalidResponseError,
)
from semantic_kernel.filters.auto_function_invocation.auto_function_invocation_context import (
    AutoFunctionInvocationContext,
)
from semantic_kernel.utils.telemetry.model_diagnostics import trace_chat_completion
from semantic_kernel.contents.chat_role import ChatRole
from semantic_kernel.contents.finish_reason import FinishReason

if TYPE_CHECKING:
    from semantic_kernel.connectors.ai.prompt_execution_settings import (
        PromptExecutionSettings,
    )

    from semantic_kernel.functions.kernel_arguments import KernelArguments
    from semantic_kernel.kernel import Kernel

logger: logging.Logger = logging.getLogger(__name__)

class InvokeTermination(Exception):
    """Exception for termination of function invocation."""

class OpenAIChatCompletionBase(OpenAIHandler, ChatCompletionClientBase):
    """OpenAI Chat completion class."""

    MODEL_PROVIDER_NAME: ClassVar[str] = "openai"
    SUPPORTS_FUNCTION_CALLING: ClassVar[bool] = True

    # region Overriding base class methods
    # most of the methods are overridden from the ChatCompletionClientBase class, otherwise it is mentioned

    # Override from AIServiceClientBase
    @override
    def get_prompt_execution_settings_class(self) -> type["PromptExecutionSettings"]:
        return OpenAIChatPromptExecutionSettings

    @override
    @trace_chat_completion(MODEL_PROVIDER_NAME)
    async def _inner_get_chat_message_contents(
        self,
        chat_history: "ChatHistory",
        settings: "PromptExecutionSettings",
    ) -> list["ChatMessageContent"]:
        if not isinstance(settings, OpenAIChatPromptExecutionSettings):
            settings = self.get_prompt_execution_settings_from_settings(settings)
        assert isinstance(settings, OpenAIChatPromptExecutionSettings)  # nosec

        # For backwards compatibility we need to convert the `FunctionCallBehavior` to `FunctionChoiceBehavior`
        # if this method is called with a `FunctionCallBehavior` object as part of the settings
        if hasattr(settings, "function_call_behavior") and isinstance(
            settings.function_call_behavior, FunctionCallBehavior
        ):
            settings.function_choice_behavior = (
                FunctionChoiceBehavior.from_function_call_behavior(
                    settings.function_call_behavior
                )
            )

    MODEL_PROVIDER_NAME: ClassVar[str] = "openai"
    SUPPORTS_FUNCTION_CALLING: ClassVar[bool] = True

    # region Overriding base class methods
    # most of the methods are overridden from the ChatCompletionClientBase class, otherwise it is mentioned

    # Override from AIServiceClientBase
    @override
    def get_prompt_execution_settings_class(self) -> type["PromptExecutionSettings"]:
        return OpenAIChatPromptExecutionSettings

    @override
    @trace_chat_completion(MODEL_PROVIDER_NAME)
    async def _inner_get_chat_message_contents(
        self,
        chat_history: "ChatHistory",
        settings: "PromptExecutionSettings",
    ) -> list["ChatMessageContent"]:
        if not isinstance(settings, OpenAIChatPromptExecutionSettings):
            settings = self.get_prompt_execution_settings_from_settings(settings)
        assert isinstance(settings, OpenAIChatPromptExecutionSettings)  # nosec

    @override
    @trace_chat_completion(MODEL_PROVIDER_NAME)
    async def _inner_get_chat_message_contents(
        self,
        chat_history: "ChatHistory",
        settings: "PromptExecutionSettings",
    ) -> list["ChatMessageContent"]:
        if not isinstance(settings, OpenAIChatPromptExecutionSettings):
            settings = self.get_prompt_execution_settings_from_settings(settings)
        assert isinstance(settings, OpenAIChatPromptExecutionSettings)  # nosec

        # For backwards compatibility we need to convert the `FunctionCallBehavior` to `FunctionChoiceBehavior`
        # if this method is called with a `FunctionCallBehavior` object as part of the settings
        if hasattr(settings, "function_call_behavior") and isinstance(
            settings.function_call_behavior, FunctionCallBehavior
        ):
            settings.function_choice_behavior = (
                FunctionChoiceBehavior.from_function_call_behavior(
                    settings.function_call_behavior
                )
            )
    def get_chat_message_content_class(self) -> type[ChatMessageContent]:
        """Get the chat message content types used by a class, default is ChatMessageContent."""
        return OpenAIChatMessageContent

    async def complete_chat(
        self,
        chat_history: ChatHistory,
        settings: OpenAIPromptExecutionSettings,
    ) -> List[OpenAIChatMessageContent]:
        """Executes a chat completion request and returns the result.

        Arguments:
            chat_history {ChatHistory} -- The chat history to use for the chat completion.
            settings {OpenAIChatPromptExecutionSettings | AzureChatPromptExecutionSettings} -- The settings to use
                for the chat completion request.

        kernel = kwargs.get("kernel", None)
        if settings.function_choice_behavior is not None:
            if kernel is None:
                raise ServiceInvalidExecutionSettingsError(
                    "The kernel is required for OpenAI tool calls."
                )
            if (
                settings.number_of_responses is not None
                and settings.number_of_responses > 1
            ):
                raise ServiceInvalidExecutionSettingsError("The kernel is required for OpenAI tool calls.")
        Returns:
            List[ChatMessageContent]: The completion result(s).
        """
        # For backwards compatibility we need to convert the `FunctionCallBehavior` to `FunctionChoiceBehavior`
        # if this method is called with a `FunctionCallBehavior` object as pat of the settings
        if hasattr(settings, "function_call_behavior") and isinstance(
            settings.function_call_behavior, FunctionCallBehavior
        ):
            settings.function_choice_behavior = FunctionChoiceBehavior.from_function_call_behavior(
                settings.function_call_behavior
            )

        kernel = kwargs.get("kernel", None)
        arguments = kwargs.get("arguments", None)
        if settings.function_choice_behavior is not None:
            if kernel is None:
                raise ServiceInvalidExecutionSettingsError("The kernel is required for OpenAI tool calls.")
            if arguments is None and settings.function_choice_behavior.auto_invoke_kernel_functions:
                raise ServiceInvalidExecutionSettingsError(
                    "The kernel arguments are required for auto invoking OpenAI tool calls."
                )
            if settings.number_of_responses is not None and settings.number_of_responses > 1:
                raise ServiceInvalidExecutionSettingsError(
                    "Auto-invocation of tool calls may only be used with a "
                    "OpenAIChatPromptExecutions.number_of_responses of 1."
                )

        kernel = kwargs.get("kernel", None)
        arguments = kwargs.get("arguments", None)
        if settings.function_choice_behavior is not None:
            if kernel is None:
                raise ServiceInvalidExecutionSettingsError("The kernel is required for OpenAI tool calls.")
            if arguments is None and settings.function_choice_behavior.auto_invoke_kernel_functions:
                raise ServiceInvalidExecutionSettingsError(
                    "The kernel arguments are required for auto invoking OpenAI tool calls."
                )
            if settings.number_of_responses is not None and settings.number_of_responses > 1:
                raise ServiceInvalidExecutionSettingsError(
                    "Auto-invocation of tool calls may only be used with a "
                    "OpenAIChatPromptExecutions.number_of_responses of 1."
                )

        kernel = kwargs.get("kernel", None)
        arguments = kwargs.get("arguments", None)
        if settings.function_choice_behavior is not None:
            if kernel is None:
                raise ServiceInvalidExecutionSettingsError("The kernel is required for OpenAI tool calls.")
            if arguments is None and settings.function_choice_behavior.auto_invoke_kernel_functions:
                raise ServiceInvalidExecutionSettingsError(
                    "The kernel arguments are required for auto invoking OpenAI tool calls."
                )
            if settings.number_of_responses is not None and settings.number_of_responses > 1:
                raise ServiceInvalidExecutionSettingsError(
                    "Auto-invocation of tool calls may only be used with a "
                    "OpenAIChatPromptExecutions.number_of_responses of 1."
                )

        # behavior for non-function calling or for enable, but not auto-invoke.
        self._prepare_settings(
            settings, chat_history, stream_request=False, kernel=kernel
        )
        if settings.function_choice_behavior is None or (
            settings.function_choice_behavior
            and not settings.function_choice_behavior.auto_invoke_kernel_functions
        ):
            return await self._send_chat_request(settings)

        # loop for auto-invoke function calls
        for request_index in range(
            settings.function_choice_behavior.maximum_auto_invoke_attempts
        ):
            completions = await self._send_chat_request(settings)
            # there is only one chat message, this was checked earlier
            chat_history.add_message(message=completions[0])
            # get the function call contents from the chat message
            function_calls = [
                item
                for item in chat_history.messages[-1].items
                if isinstance(item, FunctionCallContent)
            ]
            # get the function call contents from the chat message, there is only one chat message
            # this was checked earlier
            function_calls = [item for item in completions[0].items if isinstance(item, FunctionCallContent)]
            if (fc_count := len(function_calls)) == 0:
                return completions

            # Since we have a function call, add the assistant's tool call message to the history
            chat_history.add_message(message=completions[0])

            logger.info(f"processing {fc_count} tool calls in parallel.")

            # this function either updates the chat history with the function call results
            # or returns the context, with terminate set to True
            # in which case the loop will break and the function calls are returned.
            results = await asyncio.gather(
                *[
                    self._process_function_call(
                        function_call=function_call,
                        chat_history=chat_history,
                        kernel=kernel,
                        arguments=kwargs.get("arguments", None),
                        function_call_count=fc_count,
                        request_index=request_index,
                        function_call_behavior=settings.function_choice_behavior,
                    )
                    for function_call in function_calls
                ],
            )

            if any(result.terminate for result in results if result is not None):
                return merge_function_results(chat_history.messages[-len(results) :])
        settings.stream = False
        settings.messages = self._prepare_chat_history_for_request(chat_history)
        settings.ai_model_id = settings.ai_model_id or self.ai_model_id

            logger.info(f"processing {fc_count} tool calls in parallel.")

            # this function either updates the chat history with the function call results
            # or returns the context, with terminate set to True
            # in which case the loop will break and the function calls are returned.
            results = await asyncio.gather(
                *[
                    self._process_function_call(
                        function_call=function_call,
                        chat_history=chat_history,
                        kernel=kernel,
                        arguments=kwargs.get("arguments", None),
                        function_call_count=fc_count,
                        request_index=request_index,
                        function_call_behavior=settings.function_choice_behavior,
                    )
                    for function_call in function_calls
                ],
            )

            if any(result.terminate for result in results if result is not None):
                return merge_function_results(chat_history.messages[-len(results) :])
        settings.messages = self._prepare_chat_history_for_request(chat_history)
        settings.stream = False
        settings.messages = self._prepare_chat_history_for_request(chat_history)
        settings.ai_model_id = settings.ai_model_id or self.ai_model_id

        response = await self._send_request(request_settings=settings)
        response = await self._send_request(settings)
        assert isinstance(response, ChatCompletion)  # nosec
        response_metadata = self._get_metadata_from_chat_response(response)
        return [self._create_chat_message_content(response, choice, response_metadata) for choice in response.choices]

    @override
    async def _inner_get_streaming_chat_message_contents(
        self,
        chat_history: "ChatHistory",
        settings: "PromptExecutionSettings",
        function_invoke_attempt: int = 0,
    ) -> AsyncGenerator[list["StreamingChatMessageContent"], Any]:
        if not isinstance(settings, OpenAIChatPromptExecutionSettings):
            settings = self.get_prompt_execution_settings_from_settings(settings)
        assert isinstance(settings, OpenAIChatPromptExecutionSettings)  # nosec

    ) -> AsyncGenerator[list[StreamingChatMessageContent | None], Any]:
        """Executes a streaming chat completion request and returns the result.

        Args:
            chat_history (ChatHistory): The chat history to use for the chat completion.
            settings (OpenAIChatPromptExecutionSettings | AzureChatPromptExecutionSettings): The settings to use
                for the chat completion request.
            kwargs (Dict[str, Any]): The optional arguments.

    ) -> AsyncGenerator[list[StreamingChatMessageContent | None], Any]:
        """Executes a streaming chat completion request and returns the result.

        Args:
            chat_history (ChatHistory): The chat history to use for the chat completion.
            settings (OpenAIChatPromptExecutionSettings | AzureChatPromptExecutionSettings): The settings to use
        chat_history: ChatHistory,
        settings: OpenAIPromptExecutionSettings,
    ) -> AsyncIterable[List[OpenAIStreamingChatMessageContent]]:
        """Executes a streaming chat completion request and returns the result.

        Arguments:
            chat_history {ChatHistory} -- The chat history to use for the chat completion.
            settings {OpenAIChatPromptExecutionSettings | AzureChatPromptExecutionSettings} -- The settings to use
                for the chat completion request.
            kwargs (Dict[str, Any]): The optional arguments.

        Yields:
            List[StreamingChatMessageContent]: A stream of
                StreamingChatMessageContent when using Azure.
        """
        # For backwards compatibility we need to convert the `FunctionCallBehavior` to `FunctionChoiceBehavior`
        # if this method is called with a `FunctionCallBehavior` object as part of the settings
        if hasattr(settings, "function_call_behavior") and isinstance(
            settings.function_call_behavior, FunctionCallBehavior
        ):
            settings.function_choice_behavior = (
                FunctionChoiceBehavior.from_function_call_behavior(
                    settings.function_call_behavior
                )
            )

        kernel = kwargs.get("kernel", None)
        if settings.function_choice_behavior is not None:
            if kernel is None:
                raise ServiceInvalidExecutionSettingsError(
                    "The kernel is required for OpenAI tool calls."
                )
            if (
                settings.number_of_responses is not None
                and settings.number_of_responses > 1
            ):
                raise ServiceInvalidExecutionSettingsError("The kernel is required for OpenAI tool calls.")
        arguments = kwargs.get("arguments", None)
        if settings.function_choice_behavior is not None:
            if kernel is None:
                raise ServiceInvalidExecutionSettingsError("The kernel is required for OpenAI tool calls.")
            if arguments is None and settings.function_choice_behavior.auto_invoke_kernel_functions:
                raise ServiceInvalidExecutionSettingsError(
                    "The kernel arguments are required for auto invoking OpenAI tool calls."
                )
            if settings.number_of_responses is not None and settings.number_of_responses > 1:
                raise ServiceInvalidExecutionSettingsError(
                    "Auto-invocation of tool calls may only be used with a "
                    "OpenAIChatPromptExecutions.number_of_responses of 1."
                )

        # Prepare settings for streaming requests
        self._prepare_settings(
            settings, chat_history, stream_request=True, kernel=kernel
        )

        request_attempts = (
            settings.function_choice_behavior.maximum_auto_invoke_attempts
            if (
                settings.function_choice_behavior
                and settings.function_choice_behavior.auto_invoke_kernel_functions
            )
            else 1
        )
        # hold the messages, if there are more than one response, it will not be used, so we flatten
        for request_index in range(request_attempts):
            all_messages: list[StreamingChatMessageContent] = []
            function_call_returned = False
            async for messages in self._send_chat_stream_request(settings):
                for msg in messages:
                    if msg is not None:
                        all_messages.append(msg)
                        if any(
                            isinstance(item, FunctionCallContent) for item in msg.items
                        ):
                            function_call_returned = True
                yield messages

            if (
                settings.function_choice_behavior is None
                or (
                    settings.function_choice_behavior
                    and not settings.function_choice_behavior.auto_invoke_kernel_functions
                )
                or not function_call_returned
            ):
                # no need to process function calls
                # note that we don't check the FinishReason and instead check whether there are any tool calls,
                # as the service may return a FinishReason of "stop" even if there are tool calls to be made,
                # in particular if a required tool is specified.
                return

            # there is one response stream in the messages, combining now to create the full completion
            # depending on the prompt, the message may contain both function call content and others
            full_completion: StreamingChatMessageContent = reduce(
                lambda x, y: x + y, all_messages
            )
            function_calls = [
                item
                for item in full_completion.items
                if isinstance(item, FunctionCallContent)
            ]
            chat_history.add_message(message=full_completion)

            fc_count = len(function_calls)
            logger.info(f"processing {fc_count} tool calls in parallel.")

            # this function either updates the chat history with the function call results
            # or returns the context, with terminate set to True
            # in which case the loop will break and the function calls are returned.
            # Exceptions are not caught, that is up to the developer, can be done with a filter
            results = await asyncio.gather(
                *[
                    self._process_function_call(
                        function_call=function_call,
                        chat_history=chat_history,
                        kernel=kernel,
                        arguments=kwargs.get("arguments", None),
                        function_call_count=fc_count,
                        request_index=request_index,
                        function_call_behavior=settings.function_choice_behavior,
                    )
                    for function_call in function_calls
                ],
            )
            if any(result.terminate for result in results if result is not None):
                yield merge_function_results(chat_history.messages[-len(results) :])  # type: ignore
                break

        request_attempts = (
            settings.function_choice_behavior.maximum_auto_invoke_attempts
            if (
                settings.function_choice_behavior
                and settings.function_choice_behavior.auto_invoke_kernel_functions
            )
            else 1
        )
        # hold the messages, if there are more than one response, it will not be used, so we flatten
        for request_index in range(request_attempts):
            all_messages: list[StreamingChatMessageContent] = []
            function_call_returned = False
            async for messages in self._send_chat_stream_request(settings):
                for msg in messages:
                    if msg is not None:
                        all_messages.append(msg)
                        if any(
                            isinstance(item, FunctionCallContent) for item in msg.items
                        ):
                            function_call_returned = True
                yield messages

            if (
                settings.function_choice_behavior is None
                or (
                    settings.function_choice_behavior
                    and not settings.function_choice_behavior.auto_invoke_kernel_functions
                )
                or not function_call_returned
            ):
                # no need to process function calls
                # note that we don't check the FinishReason and instead check whether there are any tool calls,
                # as the service may return a FinishReason of "stop" even if there are tool calls to be made,
                # in particular if a required tool is specified.
                return

            # there is one response stream in the messages, combining now to create the full completion
            # depending on the prompt, the message may contain both function call content and others
            full_completion: StreamingChatMessageContent = reduce(
                lambda x, y: x + y, all_messages
            )
            function_calls = [
                item
                for item in full_completion.items
                if isinstance(item, FunctionCallContent)
            ]
            chat_history.add_message(message=full_completion)

            fc_count = len(function_calls)
            logger.info(f"processing {fc_count} tool calls in parallel.")

            # this function either updates the chat history with the function call results
            # or returns the context, with terminate set to True
            # in which case the loop will break and the function calls are returned.
            # Exceptions are not caught, that is up to the developer, can be done with a filter
            results = await asyncio.gather(
                *[
                    self._process_function_call(
                        function_call=function_call,
                        chat_history=chat_history,
                        kernel=kernel,
                        arguments=kwargs.get("arguments", None),
                        function_call_count=fc_count,
                        request_index=request_index,
                        function_call_behavior=settings.function_choice_behavior,
                    )
                    for function_call in function_calls
                ],
            )
            if any(result.terminate for result in results if result is not None):
                yield merge_function_results(chat_history.messages[-len(results) :])  # type: ignore
                break

            self._update_settings(settings, chat_history, kernel=kernel)

    # endregion
    # region internal handlers

    async def _send_chat_request(
        self, settings: OpenAIChatPromptExecutionSettings
    ) -> list["ChatMessageContent"]:
        """Send the chat request."""
        response = await self._send_request(request_settings=settings)
        assert isinstance(response, ChatCompletion)  # nosec
        response_metadata = self._get_metadata_from_chat_response(response)
        return [
            self._create_chat_message_content(response, choice, response_metadata)
            for choice in response.choices
        ]
        settings.stream = True
        settings.messages = self._prepare_chat_history_for_request(chat_history)
        settings.ai_model_id = settings.ai_model_id or self.ai_model_id
        settings.messages = self._prepare_chat_history_for_request(chat_history)
        settings.stream = True
        settings.stream_options = {"include_usage": True}
        settings.messages = self._prepare_chat_history_for_request(chat_history)
        settings.ai_model_id = settings.ai_model_id or self.ai_model_id

        response = await self._send_request(settings)
        if not isinstance(response, AsyncStream):
            raise ServiceInvalidResponseError(
                "Expected an AsyncStream[ChatCompletionChunk] response."
            )
        async for chunk in response:
            if len(chunk.choices) == 0:
                continue
            if len(chunk.choices) == 0 and chunk.usage is None:
                continue

        response = await self._send_request(request_settings=settings)
        if not isinstance(response, AsyncStream):
            raise ServiceInvalidResponseError(
                "Expected an AsyncStream[ChatCompletionChunk] response."
            )
        async for chunk in response:
            if len(chunk.choices) == 0 and chunk.usage is None:
                continue
            assert isinstance(chunk, ChatCompletionChunk)  # nosec
            chunk_metadata = self._get_metadata_from_streaming_chat_response(chunk)
            yield [
                self._create_streaming_chat_message_content(
                    chunk, choice, chunk_metadata
                )
                for choice in chunk.choices
            ]
            if chunk.usage is not None:
                # Usage is contained in the last chunk where the choices are empty
                # We are duplicating the usage metadata to all the choices in the response
                yield [
                    StreamingChatMessageContent(
                        role=AuthorRole.ASSISTANT,
                        content="",
                        choice_index=i,
                        inner_content=chunk,
                        ai_model_id=settings.ai_model_id,
                        metadata=chunk_metadata,
                        function_invoke_attempt=function_invoke_attempt,
                    )
                    for i in range(settings.number_of_responses or 1)
                ]
            else:
                yield [
                    self._create_streaming_chat_message_content(chunk, choice, chunk_metadata, function_invoke_attempt)
                    for choice in chunk.choices
                ]

    @override
    def _verify_function_choice_settings(self, settings: "PromptExecutionSettings") -> None:
        if not isinstance(settings, OpenAIChatPromptExecutionSettings):
            raise ServiceInvalidExecutionSettingsError("The settings must be an OpenAIChatPromptExecutionSettings.")
        if settings.number_of_responses is not None and settings.number_of_responses > 1:
            raise ServiceInvalidExecutionSettingsError(
                "Auto-invocation of tool calls may only be used with a "
                "OpenAIChatPromptExecutions.number_of_responses of 1."
            )

    @override
    def _update_function_choice_settings_callback(
        self,
    ) -> Callable[["FunctionCallChoiceConfiguration", "PromptExecutionSettings", FunctionChoiceType], None]:
        return update_settings_from_function_call_configuration

    @override
    def _reset_function_choice_settings(self, settings: "PromptExecutionSettings") -> None:
        if hasattr(settings, "tool_choice"):
            settings.tool_choice = None
        if hasattr(settings, "tools"):
            settings.tools = None
    # endregion

    # region content creation

    def _create_chat_message_content(
        self,
        response: ChatCompletion,
        choice: Choice,
        response_metadata: dict[str, Any],
    ) -> "ChatMessageContent":
        """Create a chat message content object from a choice."""
        metadata = self._get_metadata_from_chat_choice(choice)
        metadata.update(response_metadata)

        items: list[Any] = self._get_tool_calls_from_chat_choice(choice)
        items.extend(self._get_function_call_from_chat_choice(choice))
        if choice.message.content:
            items.append(TextContent(text=choice.message.content))
        elif hasattr(choice.message, "refusal") and choice.message.refusal:
            items.append(TextContent(text=choice.message.refusal))

        return ChatMessageContent(
            inner_content=response,
            ai_model_id=self.ai_model_id,
            metadata=metadata,
            role=AuthorRole(choice.message.role),
            items=items,
            finish_reason=(
                FinishReason(choice.finish_reason) if choice.finish_reason else None
            ),
        )

    def _create_streaming_chat_message_content(
        self,
        chunk: ChatCompletionChunk,
        choice: ChunkChoice,
        chunk_metadata: dict[str, Any],
    ) -> StreamingChatMessageContent:
        """Create a streaming chat message content object from a choice."""
        metadata = self._get_metadata_from_chat_choice(choice)
        metadata.update(chunk_metadata)

        items: list[Any] = self._get_tool_calls_from_chat_choice(choice)
        items.extend(self._get_function_call_from_chat_choice(choice))
            )
        async for chunk in response:
            if len(chunk.choices) == 0 and chunk.usage is None:
                continue
            assert isinstance(chunk, ChatCompletionChunk)  # nosec
            chunk_metadata = self._get_metadata_from_streaming_chat_response(chunk)
            yield [
                self._create_streaming_chat_message_content(
                    chunk, choice, chunk_metadata
                )
                for choice in chunk.choices
            ]
            if chunk.usage is not None:
                # Usage is contained in the last chunk where the choices are empty
                # We are duplicating the usage metadata to all the choices in the response
                yield [
                    StreamingChatMessageContent(
                        role=AuthorRole.ASSISTANT,
                        content="",
                        choice_index=i,
                        inner_content=chunk,
                        ai_model_id=settings.ai_model_id,
                        metadata=chunk_metadata,
                    )
                    for i in range(settings.number_of_responses or 1)
                ]
            else:
                yield [
                    self._create_streaming_chat_message_content(chunk, choice, chunk_metadata)
                    for choice in chunk.choices
                ]

    @override
    def _verify_function_choice_settings(self, settings: "PromptExecutionSettings") -> None:
        if not isinstance(settings, OpenAIChatPromptExecutionSettings):
            raise ServiceInvalidExecutionSettingsError("The settings must be an OpenAIChatPromptExecutionSettings.")
        if settings.number_of_responses is not None and settings.number_of_responses > 1:
            raise ServiceInvalidExecutionSettingsError(
                "Auto-invocation of tool calls may only be used with a "
                "OpenAIChatPromptExecutions.number_of_responses of 1."
            )

    @override
    def _update_function_choice_settings_callback(
        self,
    ) -> Callable[[FunctionCallChoiceConfiguration, "PromptExecutionSettings", FunctionChoiceType], None]:
        return update_settings_from_function_call_configuration

    @override
    def _reset_function_choice_settings(self, settings: "PromptExecutionSettings") -> None:
        if hasattr(settings, "tool_choice"):
            settings.tool_choice = None
        if hasattr(settings, "tools"):
            settings.tools = None

    # endregion

    # region content creation

    def _create_chat_message_content(
        self,
        response: ChatCompletion,
        choice: Choice,
        response_metadata: dict[str, Any],
    ) -> "ChatMessageContent":
        """Create a chat message content object from a choice."""
        metadata = self._get_metadata_from_chat_choice(choice)
        metadata.update(response_metadata)

        items: list[Any] = self._get_tool_calls_from_chat_choice(choice)
        items.extend(self._get_function_call_from_chat_choice(choice))
        if choice.message.content:
            items.append(TextContent(text=choice.message.content))
        elif hasattr(choice.message, "refusal") and choice.message.refusal:
            items.append(TextContent(text=choice.message.refusal))

        return ChatMessageContent(
            inner_content=response,
            ai_model_id=self.ai_model_id,
            metadata=metadata,
            role=AuthorRole(choice.message.role),
            items=items,
            finish_reason=(
                FinishReason(choice.finish_reason) if choice.finish_reason else None
            ),
        )

    def _create_streaming_chat_message_content(
        self,
        chunk: ChatCompletionChunk,
        choice: ChunkChoice,
        chunk_metadata: dict[str, Any],
        function_invoke_attempt: int,
    ) -> StreamingChatMessageContent:
        """Create a streaming chat message content object from a choice."""
        metadata = self._get_metadata_from_chat_choice(choice)
        metadata.update(chunk_metadata)

        items: list[Any] = self._get_tool_calls_from_chat_choice(choice)
        items.extend(self._get_function_call_from_chat_choice(choice))

    # endregion

    # region content creation

    def _create_chat_message_content(
        self,
        response: ChatCompletion,
        choice: Choice,
        response_metadata: dict[str, Any],
    ) -> "ChatMessageContent":
        """Create a chat message content object from a choice."""
        metadata = self._get_metadata_from_chat_choice(choice)
        metadata.update(response_metadata)

        items: list[Any] = self._get_tool_calls_from_chat_choice(choice)
        items.extend(self._get_function_call_from_chat_choice(choice))
        if choice.message.content:
            items.append(TextContent(text=choice.message.content))
        elif hasattr(choice.message, "refusal") and choice.message.refusal:
            items.append(TextContent(text=choice.message.refusal))

        return ChatMessageContent(
            inner_content=response,
            ai_model_id=self.ai_model_id,
            metadata=metadata,
            role=AuthorRole(choice.message.role),
            items=items,
            finish_reason=(
                FinishReason(choice.finish_reason) if choice.finish_reason else None
            ),
        )

    def _create_streaming_chat_message_content(
        self,
        chunk: ChatCompletionChunk,
        choice: ChunkChoice,
        chunk_metadata: dict[str, Any],
    ) -> StreamingChatMessageContent:
        """Create a streaming chat message content object from a choice."""
        metadata = self._get_metadata_from_chat_choice(choice)
        metadata.update(chunk_metadata)

        items: list[Any] = self._get_tool_calls_from_chat_choice(choice)
        items.extend(self._get_function_call_from_chat_choice(choice))
        if choice.delta.content is not None:
            items.append(
                StreamingTextContent(
                    choice_index=choice.index, text=choice.delta.content
                )
            )
        if choice.delta and choice.delta.content is not None:
            items.append(StreamingTextContent(choice_index=choice.index, text=choice.delta.content))
            
        return StreamingChatMessageContent(
            choice_index=choice.index,
            inner_content=chunk,
            ai_model_id=self.ai_model_id,
            metadata=metadata,
            role=(
                AuthorRole(choice.delta.role)
                if choice.delta.role
                else AuthorRole.ASSISTANT
            ),
            finish_reason=(
                FinishReason(choice.finish_reason) if choice.finish_reason else None
            ),
            role=(AuthorRole(choice.delta.role) if choice.delta and choice.delta.role else AuthorRole.ASSISTANT),
            finish_reason=(FinishReason(choice.finish_reason) if choice.finish_reason else None),
            items=items,
            role=(AuthorRole(choice.delta.role) if choice.delta and choice.delta.role else AuthorRole.ASSISTANT),
            finish_reason=(FinishReason(choice.finish_reason) if choice.finish_reason else None),
            items=items,
            role=ChatRole(choice.delta.role) if choice.delta.role else None,
            content=choice.delta.content,
            finish_reason=FinishReason(choice.finish_reason) if choice.finish_reason else None,
            function_call=self._get_function_call_from_chat_choice(choice),
            tool_calls=self._get_tool_calls_from_chat_choice(choice),
            function_invoke_attempt=function_invoke_attempt,
        )

    def _get_metadata_from_chat_response(
        self, response: ChatCompletion
    ) -> dict[str, Any]:
    def _get_metadata_from_chat_response(self, response: ChatCompletion) -> dict[str, Any]:
        """Get metadata from a chat response."""
        return {
            "id": response.id,
            "created": response.created,
            "system_fingerprint": response.system_fingerprint,
            "usage": response.usage if hasattr(response, "usage") else None,
        }

    def _get_metadata_from_streaming_chat_response(
        self, response: ChatCompletionChunk
    ) -> dict[str, Any]:
        """Get metadata from a streaming chat response."""
        return {
            "id": response.id,
            "created": response.created,
            "system_fingerprint": response.system_fingerprint,
            "usage": CompletionUsage.from_openai(response.usage) if response.usage is not None else None,
        }

    def _get_metadata_from_chat_choice(
        self, choice: Choice | ChunkChoice
    ) -> dict[str, Any]:
        """Get metadata from a chat choice."""
        return {
            "logprobs": getattr(choice, "logprobs", None),
        }

    def _get_tool_calls_from_chat_choice(
        self, choice: Choice | ChunkChoice
    ) -> list[FunctionCallContent]:
        """Get tool calls from a chat choice."""
        content = choice.message if isinstance(choice, Choice) else choice.delta
        if content and (tool_calls := getattr(content, "tool_calls", None)) is not None:
            return [
                FunctionCallContent(
                    id=tool.id,
                    index=getattr(tool, "index", None),
                    name=tool.function.name,
                    arguments=tool.function.arguments,
                )
                for tool in cast(list[ChatCompletionMessageToolCall] | list[ChoiceDeltaToolCall], tool_calls)
                if tool.function is not None
            ]
        # When you enable asynchronous content filtering in Azure OpenAI, you may receive empty deltas
        return []

    def _get_function_call_from_chat_choice(
        self, choice: Choice | ChunkChoice
    ) -> list[FunctionCallContent]:
        """Get a function call from a chat choice."""
        content = choice.message if isinstance(choice, Choice) else choice.delta
        assert hasattr(content, "function_call")  # nosec
        if content.function_call is None:
            return []
        return [
            FunctionCallContent(
                id="legacy_function_call",
                name=content.function_call.name,
                arguments=content.function_call.arguments,
            )
        ]
        if content and (function_call := getattr(content, "function_call", None)) is not None:
            function_call = cast(FunctionCall | ChoiceDeltaFunctionCall, function_call)
            return [
                FunctionCallContent(
                    id="legacy_function_call", name=function_call.name, arguments=function_call.arguments
                )
            ]
        # When you enable asynchronous content filtering in Azure OpenAI, you may receive empty deltas
        return []

    def _prepare_chat_history_for_request(
        self,
        chat_history: "ChatHistory",
        role_key: str = "role",
        content_key: str = "content",
    ) -> Any:
        """Prepare the chat history for a request.

        Allowing customization of the key names for role/author, and optionally overriding the role.

        ChatRole.TOOL messages need to be formatted different than system/user/assistant messages:
            They require a "tool_call_id" and (function) "name" key, and the "metadata" key should
            be removed. The "encoding" key should also be removed.

        Override this method to customize the formatting of the chat history for a request.

        Args:
            chat_history (ChatHistory): The chat history to prepare.
            role_key (str): The key name for the role/author.
            content_key (str): The key name for the content/message.

        Returns:
            prepared_chat_history (Any): The prepared chat history for a request.
        """
        return [
            {
                **message.to_dict(role_key=role_key, content_key=content_key),
                role_key: "developer"
                if self.instruction_role == "developer" and message.to_dict(role_key=role_key)[role_key] == "system"
                else message.to_dict(role_key=role_key)[role_key],
            }
            for message in chat_history.messages
            if not isinstance(message, (AnnotationContent, FileReferenceContent))
        ]

    # endregion

    def _prepare_settings(
        self,
        settings: OpenAIChatPromptExecutionSettings,
        chat_history: ChatHistory,
        stream_request: bool = False,
        kernel: "Kernel | None" = None,
    ) -> None:
        """Prepare the prompt execution settings for the chat request."""
        settings.stream = stream_request
        if not settings.ai_model_id:
            settings.ai_model_id = self.ai_model_id
        self._update_settings(
            settings=settings, chat_history=chat_history, kernel=kernel
        )

    def _update_settings(
        self,
        settings: OpenAIChatPromptExecutionSettings,
        chat_history: ChatHistory,
        kernel: "Kernel | None" = None,
    ) -> None:
        """Update the settings with the chat history."""
        settings.messages = self._prepare_chat_history_for_request(chat_history)
        if settings.function_choice_behavior and kernel:
            settings.function_choice_behavior.configure(
                kernel=kernel,
                update_settings_callback=update_settings_from_function_call_configuration,
                settings=settings,
            )

    # endregion
    # region function calling

    @deprecated(
        "Use `invoke_function_call` from the kernel instead with `FunctionChoiceBehavior`."
    )
    # region function calling
    @deprecated("Use `invoke_function_call` from the kernel instead with `FunctionChoiceBehavior`.")
    async def _process_function_call(
        self,
        function_call: FunctionCallContent,
        chat_history: ChatHistory,
        kernel: "Kernel",
        arguments: "KernelArguments | None",
        function_call_count: int,
        request_index: int,
        function_call_behavior: FunctionChoiceBehavior,
    ) -> "AutoFunctionInvocationContext | None":
        """Processes the tool calls in the result and update the chat history."""
        # deprecated and might not even be used anymore, hard to trigger directly
        if isinstance(function_call_behavior, FunctionCallBehavior):  # pragma: no cover
        if isinstance(function_call_behavior, FunctionCallBehavior):
            # We need to still support a `FunctionCallBehavior` input so it doesn't break current
            # customers. Map from `FunctionCallBehavior` -> `FunctionChoiceBehavior`
            function_call_behavior = FunctionChoiceBehavior.from_function_call_behavior(
                function_call_behavior
            )

        return await kernel.invoke_function_call(
            function_call=function_call,
            chat_history=chat_history,
            arguments=arguments,
            function_call_count=function_call_count,
            request_index=request_index,
            function_behavior=function_call_behavior,
        )

    # endregion
