#!/usr/bin/env python3
"""
import asyncio
import re
Anthropic Chat Completion module

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
import json
import sys

if sys.version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from anthropic import AsyncAnthropic
from anthropic.types import (
    ContentBlockStopEvent,
    Message,
    RawContentBlockDeltaEvent,
    RawMessageDeltaEvent,
    RawMessageStartEvent,
    TextBlock,
from collections.abc import AsyncGenerator, Callable
from typing import TYPE_CHECKING, Any, ClassVar

if sys.version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from anthropic import AsyncAnthropic
from anthropic.lib.streaming._types import TextEvent
from anthropic.types import (
    ContentBlockStopEvent,
    Message,
    RawMessageDeltaEvent,
    RawMessageStartEvent,
    TextBlock,
    ToolUseBlock,
)
from pydantic import ValidationError

from semantic_kernel.connectors.ai.anthropic.prompt_execution_settings.anthropic_prompt_execution_settings import (
    AnthropicChatPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.anthropic.services.utils import (
    MESSAGE_CONVERTERS,
    update_settings_from_function_call_configuration,
)
from semantic_kernel.connectors.ai.anthropic.settings.anthropic_settings import AnthropicSettings
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.chat_message_content import ITEM_TYPES, ChatMessageContent
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.chat_message_content import ITEM_TYPES, ChatMessageContent
from semantic_kernel.connectors.ai.function_call_choice_configuration import FunctionCallChoiceConfiguration

from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceType
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.chat_message_content import CMC_ITEM_TYPES, ChatMessageContent
from semantic_kernel.contents.function_call_content import FunctionCallContent
from semantic_kernel.contents.function_result_content import FunctionResultContent
from semantic_kernel.contents.streaming_chat_message_content import ITEM_TYPES as STREAMING_ITEM_TYPES
from semantic_kernel.contents.streaming_chat_message_content import STREAMING_CMC_ITEM_TYPES as STREAMING_ITEM_TYPES

from semantic_kernel.contents.streaming_chat_message_content import StreamingChatMessageContent
from semantic_kernel.contents.streaming_text_content import StreamingTextContent
from semantic_kernel.contents.text_content import TextContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.contents.utils.finish_reason import FinishReason as SemanticKernelFinishReason
from semantic_kernel.exceptions.service_exceptions import ServiceInitializationError, ServiceResponseException
from semantic_kernel.utils.experimental_decorator import experimental_class
from semantic_kernel.utils.telemetry.model_diagnostics.decorators import trace_chat_completion
from semantic_kernel.exceptions.service_exceptions import ServiceInitializationError, ServiceResponseException
from semantic_kernel.exceptions.service_exceptions import (
    ServiceInitializationError,
    ServiceInvalidRequestError,
    ServiceInvalidResponseError,
    ServiceResponseException,
)
from semantic_kernel.utils.experimental_decorator import experimental_class
from semantic_kernel.utils.telemetry.model_diagnostics.decorators import trace_chat_completion
from semantic_kernel.exceptions.service_exceptions import (
    ServiceInitializationError,
    ServiceResponseException,

)
from semantic_kernel.utils.experimental_decorator import experimental_class
from semantic_kernel.exceptions.service_exceptions import ServiceInitializationError, ServiceResponseException
from semantic_kernel.utils.experimental_decorator import experimental_class
from semantic_kernel.utils.telemetry.model_diagnostics.decorators import trace_chat_completion
from semantic_kernel.exceptions.service_exceptions import ServiceInitializationError, ServiceResponseException
from semantic_kernel.utils.experimental_decorator import experimental_class
from semantic_kernel.utils.telemetry.model_diagnostics.decorators import trace_chat_completion
from semantic_kernel.exceptions.service_exceptions import ServiceInitializationError, ServiceResponseException
from semantic_kernel.utils.experimental_decorator import experimental_class
from semantic_kernel.utils.telemetry.model_diagnostics.decorators import trace_chat_completion

if TYPE_CHECKING:
    from semantic_kernel.connectors.ai.function_call_choice_configuration import FunctionCallChoiceConfiguration

# map finish reasons from Anthropic to Semantic Kernel
ANTHROPIC_TO_SEMANTIC_KERNEL_FINISH_REASON_MAP = {
    "end_turn": SemanticKernelFinishReason.STOP,
    "max_tokens": SemanticKernelFinishReason.LENGTH,
    "tool_use": SemanticKernelFinishReason.TOOL_CALLS,
}

logger: logging.Logger = logging.getLogger(__name__)

@experimental
class AnthropicChatCompletion(ChatCompletionClientBase):
    """Antropic ChatCompletion class."""
    MODEL_PROVIDER_NAME: ClassVar[str] = "anthropic"
    SUPPORTS_FUNCTION_CALLING: ClassVar[bool] = False

    async_client: AsyncAnthropic

    MODEL_PROVIDER_NAME: ClassVar[str] = "anthropic"
    SUPPORTS_FUNCTION_CALLING: ClassVar[bool] = False

    async_client: AsyncAnthropic
    MODEL_PROVIDER_NAME: ClassVar[str] = "anthropic"
    SUPPORTS_FUNCTION_CALLING: ClassVar[bool] = True

    async_client: AsyncAnthropic

    async_client: AsyncAnthropic

    MODEL_PROVIDER_NAME: ClassVar[str] = "anthropic"

    async_client: AsyncAnthropic

    def __init__(
        self,
        ai_model_id: str | None = None,
        service_id: str | None = None,
        api_key: str | None = None,
        async_client: AsyncAnthropic | None = None,
        env_file_path: str | None = None,
        env_file_encoding: str | None = None,
    ) -> None:
        """Initialize an AnthropicChatCompletion service.

        Args:
            ai_model_id: Anthropic model name, see
                https://docs.anthropic.com/en/docs/about-claude/models#model-names
            service_id: Service ID tied to the execution settings.
            api_key: The optional API key to use. If provided will override,
                the env vars or .env file value.
            async_client: An existing client to use.
            env_file_path: Use the environment settings file as a fallback
                to environment variables.
            env_file_encoding: The encoding of the environment settings file.
        """
        try:
            anthropic_settings = AnthropicSettings(
                api_key=api_key,
                chat_model_id=ai_model_id,
                env_file_path=env_file_path,
                env_file_encoding=env_file_encoding,
            )
        except ValidationError as ex:
            raise ServiceInitializationError("Failed to create Anthropic settings.", ex) from ex
        if not anthropic_settings.chat_model_id:
            raise ServiceInitializationError("The Anthropic chat model ID is required.")

        if not async_client:
            async_client = AsyncAnthropic(
                api_key=anthropic_settings.api_key.get_secret_value(),
            )

        super().__init__(
            async_client=async_client,
            service_id=service_id or anthropic_settings.chat_model_id,
            ai_model_id=anthropic_settings.chat_model_id,
        )

    @override
    @trace_chat_completion(MODEL_PROVIDER_NAME)
    async def get_chat_message_contents(
        self,
        chat_history: "ChatHistory",
        settings: "PromptExecutionSettings",
        **kwargs: Any,
    ) -> list["ChatMessageContent"]:
    async def get_chat_message_contents(
        self,
        chat_history: "ChatHistory",
        settings: "PromptExecutionSettings",
        **kwargs: Any,
    ) -> list["ChatMessageContent"]:
        """Executes a chat completion request and returns the result.

        Args:
            chat_history: The chat history to use for the chat completion.
            settings: The settings to use for the chat completion request.
            kwargs: The optional arguments.

        Returns:
            The completion result(s).
        """
    # region Overriding base class methods

    # Override from AIServiceClientBase
    @override
    def get_prompt_execution_settings_class(self) -> type["PromptExecutionSettings"]:
        return AnthropicChatPromptExecutionSettings

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

    @override
    @trace_chat_completion(MODEL_PROVIDER_NAME)
    async def _inner_get_chat_message_contents(
        self,
        chat_history: "ChatHistory",
        settings: "PromptExecutionSettings",
    ) -> list["ChatMessageContent"]:
        if not isinstance(settings, AnthropicChatPromptExecutionSettings):
            settings = self.get_prompt_execution_settings_from_settings(settings)
        assert isinstance(settings, AnthropicChatPromptExecutionSettings)  # nosec

        settings.ai_model_id = settings.ai_model_id or self.ai_model_id
        settings.messages = self._prepare_chat_history_for_request(chat_history)
        try:
            response = await self.async_client.messages.create(**settings.prepare_settings_dict())
        except Exception as ex:
            raise ServiceResponseException(
                f"{type(self)} service failed to complete the prompt",
                ex,
            ) from ex

        metadata: dict[str, Any] = {"id": response.id}
        # Check if usage exists and has a value, then add it to the metadata
        if hasattr(response, "usage") and response.usage is not None:
            metadata["usage"] = response.usage

        metadata: dict[str, Any] = {"id": response.id}
        # Check if usage exists and has a value, then add it to the metadata
        if hasattr(response, "usage") and response.usage is not None:
            metadata["usage"] = response.usage

        return [
            self._create_chat_message_content(response, content_block, metadata) for content_block in response.content
        ]
        settings.messages, parsed_system_message = self._prepare_chat_history_for_request(chat_history)
        if settings.system is None and parsed_system_message is not None:
            settings.system = parsed_system_message

        return await self._send_chat_request(settings)

    @override
    async def _inner_get_streaming_chat_message_contents(
        self,
        chat_history: ChatHistory,
        settings: PromptExecutionSettings,
        **kwargs: Any,
    ) -> AsyncGenerator[list[StreamingChatMessageContent], Any]:
        return [self._create_chat_message_content(response, content_block, metadata)
                for content_block in response.content]

    async def get_streaming_chat_message_contents(
        self,
        chat_history: ChatHistory,
        settings: PromptExecutionSettings,
        **kwargs: Any,
    ) -> AsyncGenerator[list[StreamingChatMessageContent], Any]:
        settings: PromptExecutionSettings,
        **kwargs: Any,
        """Executes a streaming chat completion request and returns the result.

        Args:
            chat_history: The chat history to use for the chat completion.
            settings: The settings to use for the chat completion request.
            kwargs: The optional arguments.

        Yields:
            A stream of StreamingChatMessageContent.
        """
        chat_history: "ChatHistory",
        settings: "PromptExecutionSettings",
    ) -> AsyncGenerator[list["StreamingChatMessageContent"], Any]:
        if not isinstance(settings, AnthropicChatPromptExecutionSettings):
            settings = self.get_prompt_execution_settings_from_settings(settings)
        assert isinstance(settings, AnthropicChatPromptExecutionSettings)  # nosec

        settings.messages, parsed_system_message = self._prepare_chat_history_for_request(chat_history, stream=True)
        settings.ai_model_id = settings.ai_model_id or self.ai_model_id
        settings.messages = self._prepare_chat_history_for_request(chat_history)
        try:
            async with self.async_client.messages.stream(**settings.prepare_settings_dict()) as stream:
                author_role = None
                metadata: dict[str, Any] = {"usage": {}, "id": None}
                content_block_idx = 0
                async for stream_event in stream:
                    if isinstance(stream_event, RawMessageStartEvent):
                        author_role = stream_event.message.role
                        metadata["usage"]["input_tokens"] = stream_event.message.usage.input_tokens
                        metadata["id"] = stream_event.message.id
                    elif isinstance(stream_event, (RawContentBlockDeltaEvent, RawMessageDeltaEvent)):
                        yield [
                            self._create_streaming_chat_message_content(
                                stream_event, content_block_idx, author_role, metadata
                            )
                        ]
                        yield [self._create_streaming_chat_message_content(stream_event,
                                                                           content_block_idx,
                                                                           author_role,
                                                                           metadata)]
        Yields:
            A stream of StreamingChatMessageContent.
        """
        chat_history: "ChatHistory",
        settings: "PromptExecutionSettings",
    ) -> AsyncGenerator[list["StreamingChatMessageContent"], Any]:
        chat_history: "ChatHistory",
        settings: "PromptExecutionSettings",
        function_invoke_attempt: int = 0,
    ) -> AsyncGenerator[list["StreamingChatMessageContent"], Any]:
        if not isinstance(settings, AnthropicChatPromptExecutionSettings):
            settings = self.get_prompt_execution_settings_from_settings(settings)
        assert isinstance(settings, AnthropicChatPromptExecutionSettings)  # nosec

        settings.messages, parsed_system_message = self._prepare_chat_history_for_request(chat_history, stream=True)
        settings.ai_model_id = settings.ai_model_id or self.ai_model_id
        settings.messages = self._prepare_chat_history_for_request(chat_history)
        try:
            async with self.async_client.messages.stream(**settings.prepare_settings_dict()) as stream:
                author_role = None
                metadata: dict[str, Any] = {"usage": {}, "id": None}
                content_block_idx = 0
                async for stream_event in stream:
                    if isinstance(stream_event, RawMessageStartEvent):
                        author_role = stream_event.message.role
                        metadata["usage"]["input_tokens"] = stream_event.message.usage.input_tokens
                        metadata["id"] = stream_event.message.id
                    elif isinstance(stream_event, (RawContentBlockDeltaEvent, RawMessageDeltaEvent)):
                        yield [
                            self._create_streaming_chat_message_content(
                                stream_event, content_block_idx, author_role, metadata
                            )
                        ]
                        yield [self._create_streaming_chat_message_content(stream_event,
                                                                           content_block_idx,
                                                                           author_role,
                                                                           metadata)]
                        yield [self._create_streaming_chat_message_content(stream_event,
                                                                           content_block_idx,
                                                                           author_role,
                                                                           metadata)]
                    elif isinstance(stream_event, ContentBlockStopEvent):
                        content_block_idx += 1
        except Exception as ex:
            raise ServiceResponseException(
                f"{type(self)} service failed to complete the request",
                ex,
            ) from ex

    # endregion

    def _create_chat_message_content(
        self, response: Message, content: TextBlock, response_metadata: dict[str, Any]
    ) -> "ChatMessageContent":
        """Create a chat message content object."""
        items: list[ITEM_TYPES] = []

        self, response: Message, content: TextBlock, response_metadata: dict[str, Any]
        if settings.system is None and parsed_system_message is not None:
            settings.system = parsed_system_message

        response = self._send_chat_stream_request(settings, function_invoke_attempt)
        if not isinstance(response, AsyncGenerator):
            raise ServiceInvalidResponseError("Expected an AsyncGenerator response.")

        async for message in response:
            yield message

    @override
    def _prepare_chat_history_for_request(
        self,
        chat_history: "ChatHistory",
        role_key: str = "role",
        content_key: str = "content",
        stream: bool = False,
    ) -> tuple[list[dict[str, Any]], str | None]:
        """Prepare the chat history for an Anthropic request.

        Allowing customization of the key names for role/author, and optionally overriding the role.

        Args:
            chat_history: The chat history to prepare.
            role_key: The key name for the role/author.
            content_key: The key name for the content/message.
            stream: Whether the request is for a streaming chat.

        Returns:
            A tuple containing the prepared chat history and the first SYSTEM message content.
        """
        system_message_content = None
        system_message_count = 0
        formatted_messages: list[dict[str, Any]] = []
        for i in range(len(chat_history)):
            prev_message = chat_history[i - 1] if i > 0 else None
            curr_message = chat_history[i]
            if curr_message.role == AuthorRole.SYSTEM:
                # Skip system messages after the first one is found
                if system_message_count == 0:
                    system_message_content = curr_message.content
                system_message_count += 1
            elif curr_message.role == AuthorRole.USER or curr_message.role == AuthorRole.ASSISTANT:
                formatted_messages.append(MESSAGE_CONVERTERS[curr_message.role](curr_message))
            elif curr_message.role == AuthorRole.TOOL:
                if prev_message is None:
                    # Under no circumstances should a tool message be the first message in the chat history
                    raise ServiceInvalidRequestError("Tool message found without a preceding message.")
                if prev_message.role == AuthorRole.USER or prev_message.role == AuthorRole.SYSTEM:
                    # A tool message should not be found after a user or system message
                    # Please NOTE that in SK there are the USER role and the TOOL role, but in Anthropic
                    # the tool messages are considered as USER messages. We are checking against the SK roles.
                    raise ServiceInvalidRequestError("Tool message found after a user or system message.")

                formatted_message = MESSAGE_CONVERTERS[curr_message.role](curr_message)
                if prev_message.role == AuthorRole.ASSISTANT:
                    # The first tool message after an assistant message should be a new message
                    formatted_messages.append(formatted_message)
                else:
                    # Append the tool message to the previous tool message.
                    # This indicates that the assistant message requested multiple parallel tool calls.
                    # Anthropic requires that parallel Tool messages are grouped together in a single message.
                    formatted_messages[-1][content_key] += formatted_message[content_key]
            else:
                raise ServiceInvalidRequestError(f"Unsupported role in chat history: {curr_message.role}")

        if system_message_count > 1:
            logger.warning(
                "Anthropic service only supports one system message, but %s system messages were found."
                " Only the first system message will be included in the request.",
                system_message_count,
            )

        return formatted_messages, system_message_content

    # endregion

    def _create_chat_message_content(
        self, response: Message, response_metadata: dict[str, Any]
    ) -> "ChatMessageContent":
        """Create a chat message content object."""
        items: list[CMC_ITEM_TYPES] = []
        items += self._get_tool_calls_from_message(response)

        self,
        response: Message,
        content: TextBlock,
        response_metadata: dict[str, Any]
    ) -> "ChatMessageContent":
        """Create a chat message content object."""
        items: list[ITEM_TYPES] = []

        if content.text:
            items.append(TextContent(text=content.text))
        self, response: Message, content: TextBlock, response_metadata: dict[str, Any]
    ) -> "ChatMessageContent":
        """Create a chat message content object."""
        items: list[ITEM_TYPES] = []

        if content.text:
            items.append(TextContent(text=content.text))
        for content_block in response.content:
            if isinstance(content_block, TextBlock):
                items.append(TextContent(text=content_block.text))
        finish_reason = None
        if response.stop_reason:
            finish_reason = ANTHROPIC_TO_SEMANTIC_KERNEL_FINISH_REASON_MAP[response.stop_reason]
        self, response: Message, response_metadata: dict[str, Any]
    ) -> "ChatMessageContent":
        """Create a chat message content object."""
        items: list[ITEM_TYPES] = []
        items += self._get_tool_calls_from_message(response)

        self,
        response: Message,
        content: TextBlock,
        response_metadata: dict[str, Any]
    ) -> "ChatMessageContent":
        """Create a chat message content object."""
        items: list[ITEM_TYPES] = []

        if content.text:
            items.append(TextContent(text=content.text))
        self, response: Message, content: TextBlock, response_metadata: dict[str, Any]
    ) -> "ChatMessageContent":
        """Create a chat message content object."""
        items: list[ITEM_TYPES] = []

        if content.text:
            items.append(TextContent(text=content.text))
        for content_block in response.content:
            if isinstance(content_block, TextBlock):
                items.append(TextContent(text=content_block.text))

        finish_reason = None
        if response.stop_reason:
            finish_reason = ANTHROPIC_TO_SEMANTIC_KERNEL_FINISH_REASON_MAP[response.stop_reason]
        return ChatMessageContent(
            inner_content=response,
            ai_model_id=self.ai_model_id,
            metadata=response_metadata,
            role=AuthorRole(response.role),
            role=AuthorRole.ASSISTANT,
            items=items,
            finish_reason=finish_reason,
        )

    def _create_streaming_chat_message_content(
        self,
        stream_event: RawContentBlockDeltaEvent | RawMessageDeltaEvent,
        content_block_idx: int,
        role: str | None = None,
        self,
        stream_event: TextEvent | ContentBlockStopEvent | RawMessageDeltaEvent,
        metadata: dict[str, Any] | None = None,
        function_invoke_attempt: int = 0,
    ) -> StreamingChatMessageContent:
        """Create a streaming chat message content object from a choice."""
        text_content = ""

        if stream_event.delta and hasattr(stream_event.delta, "text"):
            text_content = stream_event.delta.text

        items: list[STREAMING_ITEM_TYPES] = [StreamingTextContent(choice_index=content_block_idx, text=text_content)]

        self,
        stream_event: RawContentBlockDeltaEvent | RawMessageDeltaEvent,
        content_block_idx: int,
        role: str | None = None,
        metadata: dict[str, Any] = {}
    ) -> StreamingChatMessageContent:
        """Create a streaming chat message content object from a choice."""
        text_content = ""

        if stream_event.delta and hasattr(stream_event.delta, "text"):
            text_content = stream_event.delta.text

        items: list[STREAMING_ITEM_TYPES] = [StreamingTextContent(choice_index=content_block_idx, text=text_content)]

        finish_reason = None
        if isinstance(stream_event, RawMessageDeltaEvent):
            if stream_event.delta.stop_reason:
                finish_reason = ANTHROPIC_TO_SEMANTIC_KERNEL_FINISH_REASON_MAP[stream_event.delta.stop_reason]

            metadata["usage"]["output_tokens"] = stream_event.usage.output_tokens

        return StreamingChatMessageContent(
            choice_index=content_block_idx,
            inner_content=stream_event,
            ai_model_id=self.ai_model_id,
            metadata=metadata,
            role=AuthorRole(role) if role else AuthorRole.ASSISTANT,
            finish_reason=finish_reason,
            items=items,
        )

        if stream_event.delta and hasattr(stream_event.delta, "text"):
            text_content = stream_event.delta.text

        items: list[STREAMING_ITEM_TYPES] = [StreamingTextContent(choice_index=content_block_idx, text=text_content)]

        """Create a streaming chat message content object from a content block."""
        items: list[STREAMING_ITEM_TYPES] = []
        finish_reason = None

        if isinstance(stream_event, TextEvent):
            items.append(StreamingTextContent(choice_index=0, text=stream_event.text))
        elif (
            isinstance(stream_event, ContentBlockStopEvent)
            and hasattr(stream_event, "content_block")
            and stream_event.content_block.type == "tool_use"
        ):
            tool_use_block = stream_event.content_block
            items.append(
                FunctionCallContent(
                    id=tool_use_block.id,
                    index=stream_event.index,
                    name=tool_use_block.name,
                    arguments=json.dumps(tool_use_block.input) if tool_use_block.input else None,
                )
            )
        elif isinstance(stream_event, RawMessageDeltaEvent):
            finish_reason = ANTHROPIC_TO_SEMANTIC_KERNEL_FINISH_REASON_MAP[str(stream_event.delta.stop_reason)]
            output_tokens = stream_event.usage.output_tokens
            if metadata is None:
                metadata = {"usage": {"output_tokens": output_tokens}}
            else:
                metadata = metadata | {"usage": metadata.get("usage", {}) | {"output_tokens": output_tokens}}

        return StreamingChatMessageContent(
            choice_index=0,
            inner_content=stream_event,
            ai_model_id=self.ai_model_id,
            metadata=metadata,
            role=AuthorRole.ASSISTANT,
            finish_reason=finish_reason,
            items=items,
            function_invoke_attempt=function_invoke_attempt,
        )

    def get_prompt_execution_settings_class(self) -> "type[AnthropicChatPromptExecutionSettings]":
        """Create a request settings object."""
        return AnthropicChatPromptExecutionSettings

    async def _send_chat_request(self, settings: AnthropicChatPromptExecutionSettings) -> list["ChatMessageContent"]:
        """Send the chat request."""
        try:
            response = await self.async_client.messages.create(**settings.prepare_settings_dict())
        except Exception as ex:
            raise ServiceResponseException(
                f"{type(self)} service failed to complete the request",
                ex,
            ) from ex

        response_metadata: dict[str, Any] = {"id": response.id}
        if hasattr(response, "usage") and response.usage is not None:
            response_metadata["usage"] = response.usage

        return [self._create_chat_message_content(response, response_metadata)]

    async def _send_chat_stream_request(
        self,
        settings: AnthropicChatPromptExecutionSettings,
        function_invoke_attempt: int = 0,
    ) -> AsyncGenerator[list["StreamingChatMessageContent"], None]:
        """Send the chat stream request.

        The stream yields a sequence of stream events, which are used to create streaming chat message content:
        - RawMessageStartEvent is used to determine the message id and input tokens.
        - RawMessageDeltaEvent is used to determine the finish reason.
        - TextEvent is used to determine the text content and ContentBlockStopEvent is used to determine
            the tool use content.
        """
        try:
            async with self.async_client.messages.stream(**settings.prepare_settings_dict()) as stream:
                metadata: dict[str, Any] = {"usage": {}, "id": None}
                async for stream_event in stream:
                    if isinstance(stream_event, RawMessageStartEvent):
                        metadata["usage"]["input_tokens"] = stream_event.message.usage.input_tokens
                        metadata["id"] = stream_event.message.id
                    elif isinstance(stream_event, (TextEvent, RawMessageDeltaEvent)) or (
                        isinstance(stream_event, ContentBlockStopEvent)
                        and stream_event.content_block.type == "tool_use"
                    ):
                        yield [
                            self._create_streaming_chat_message_content(stream_event, metadata, function_invoke_attempt)
                        ]
        except Exception as ex:
            raise ServiceResponseException(
                f"{type(self)} service failed to complete the request",
                ex,
            ) from ex

    def _get_tool_calls_from_message(self, message: Message) -> list[FunctionCallContent]:
        """Get tool calls from a content blocks."""
        tool_calls: list[FunctionCallContent] = []

        for idx, content_block in enumerate(message.content):
            if isinstance(content_block, ToolUseBlock):
                tool_calls.append(
                    FunctionCallContent(
                        id=content_block.id,
                        index=idx,
                        name=content_block.name,
                        arguments=getattr(content_block, "input", None),
                    )
                )

        return tool_calls

    @override
    def _reset_function_choice_settings(self, settings: "PromptExecutionSettings") -> None:
        if hasattr(settings, "tool_choice"):
            settings.tool_choice = None
        if hasattr(settings, "tools"):
            settings.tools = None
