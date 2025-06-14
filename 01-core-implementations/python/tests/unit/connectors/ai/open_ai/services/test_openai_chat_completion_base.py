# Copyright (c) Microsoft. All rights reserved.

from copy import deepcopy
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from openai import AsyncStream
from openai.resources.chat.completions import AsyncCompletions as AsyncChatCompletions
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion_chunk import Choice as ChunkChoice
from openai.types.chat.chat_completion_chunk import ChoiceDelta as ChunkChoiceDelta
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import (
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion import (
    OpenAIChatCompletion,
)
from semantic_kernel.connectors.ai.prompt_execution_settings import (
    PromptExecutionSettings,
)
from semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion import OpenAIChatCompletion
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.contents import StreamingChatMessageContent
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.streaming_text_content import StreamingTextContent
from semantic_kernel.contents.text_content import TextContent
from semantic_kernel.exceptions.service_exceptions import (
    ServiceInvalidExecutionSettingsError,
    ServiceInvalidResponseError,
    ServiceResponseException,
)
from semantic_kernel.filters.filter_types import FilterTypes
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.kernel import Kernel

async def mock_async_process_chat_stream_response(
    arg1, response, tool_call_behavior, chat_history, kernel, arguments
):
    mock_content = MagicMock(spec=StreamingChatMessageContent)
    yield [mock_content], None

@pytest.fixture
def mock_chat_completion_response() -> ChatCompletion:
    return ChatCompletion(
        id="test_id",
        choices=[
            Choice(
                index=0,
                message=ChatCompletionMessage(content="test", role="assistant"),
                finish_reason="stop",
            )
        ],
        created=0,
        model="test",
        object="chat.completion",
    )

@pytest.fixture
def mock_streaming_chat_completion_response() -> AsyncStream[ChatCompletionChunk]:
    content = ChatCompletionChunk(
        id="test_id",
        choices=[
            ChunkChoice(
                index=0,
                delta=ChunkChoiceDelta(content="test", role="assistant"),
                finish_reason="stop",
            )
        ],
        created=0,
        model="test",
        object="chat.completion.chunk",
    )
    stream = MagicMock(spec=AsyncStream)
    stream.__aiter__.return_value = [content]
    return stream

# region Chat Message Content

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_cmc(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_create.return_value = mock_chat_completion_response
    chat_history.add_user_message("hello world")
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id"
    )

    openai_chat_completion = OpenAIChatCompletion()
    await openai_chat_completion.get_chat_message_contents(
        chat_history=chat_history,
        settings=complete_prompt_execution_settings,
        kernel=kernel,
    )
    mock_create.assert_awaited_once_with(
        model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
        stream=False,
        messages=openai_chat_completion._prepare_chat_history_for_request(chat_history),
    )

    with (
        patch(
            "semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion_base.OpenAIChatCompletionBase._prepare_settings",
            return_value=settings,
        ) as prepare_settings_mock,
        patch(
            "semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion_base.OpenAIChatCompletionBase._send_chat_stream_request",
            return_value=mock_response,
        ) as mock_send_chat_stream_request,
    ):
        chat_completion_base = OpenAIChatCompletionBase(
            ai_model_id="test_model_id", service_id="test", client=MagicMock(spec=AsyncOpenAI)
        )

        async for content in chat_completion_base.get_streaming_chat_message_contents(
            chat_history, settings, kernel=kernel, arguments=arguments
        ):
            assert content is not None

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_cmc_singular(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_create.return_value = mock_chat_completion_response
    chat_history.add_user_message("hello world")
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id"
    )

    openai_chat_completion = OpenAIChatCompletion()
    await openai_chat_completion.get_chat_message_content(
        chat_history=chat_history,
        settings=complete_prompt_execution_settings,
        kernel=kernel,
    )
    mock_create.assert_awaited_once_with(
        model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
        stream=False,
        messages=openai_chat_completion._prepare_chat_history_for_request(chat_history),
    )

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_cmc_singular_with_developer_instruction_propagates(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_create.return_value = mock_chat_completion_response
    chat_history.add_user_message("hello world")
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(service_id="test_service_id")

    openai_chat_completion = OpenAIChatCompletion(instruction_role="developer")
    await openai_chat_completion.get_chat_message_content(
        chat_history=chat_history, settings=complete_prompt_execution_settings, kernel=kernel
    )
    mock_create.assert_awaited_once_with(
        model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
        stream=False,
        messages=openai_chat_completion._prepare_chat_history_for_request(chat_history),
    )
    assert openai_chat_completion.instruction_role == "developer"

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_cmc_prompt_execution_settings(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_create.return_value = mock_chat_completion_response
    chat_history.add_user_message("hello world")
    complete_prompt_execution_settings = PromptExecutionSettings(
        service_id="test_service_id"
    )

    openai_chat_completion = OpenAIChatCompletion()
    await openai_chat_completion.get_chat_message_contents(
        chat_history=chat_history,
        settings=complete_prompt_execution_settings,
        kernel=kernel,
    )
    mock_create.assert_awaited_once_with(
        model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
        stream=False,
        messages=openai_chat_completion._prepare_chat_history_for_request(chat_history),
async def test_complete_chat_function_call_behavior(tool_call, kernel: Kernel):
    chat_history = MagicMock(spec=ChatHistory)
    chat_history.messages = []
    settings = MagicMock(spec=OpenAIChatPromptExecutionSettings)
    settings.number_of_responses = 1
    settings.function_call_behavior = None
    settings.function_choice_behavior = None
    mock_function_call = MagicMock(spec=FunctionCallContent)
    mock_text = MagicMock(spec=TextContent)
    mock_message = ChatMessageContent(
        role=AuthorRole.ASSISTANT, items=[mock_function_call] if tool_call else [mock_text]
    )

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_cmc_function_call_behavior(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_chat_completion_response.choices = [
        Choice(
            index=0,
            message=ChatCompletionMessage(
                content=None,
                role="assistant",
                tool_calls=[
                    {
                        "id": "test id",
                        "function": {
                            "name": "test-tool",
                            "arguments": '{"key": "value"}',
                        },
                        "type": "function",
                    }
                ],
            ),
            finish_reason="stop",
        )
    ]
    mock_create.return_value = mock_chat_completion_response
    chat_history.add_user_message("hello world")
    orig_chat_history = deepcopy(chat_history)
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id",
        function_call_behavior=FunctionCallBehavior.AutoInvokeKernelFunctions(),

    )
    with patch(
        "semantic_kernel.kernel.Kernel.invoke_function_call",
        new_callable=AsyncMock,
    ) as mock_process_function_call:
        openai_chat_completion = OpenAIChatCompletion()
        await openai_chat_completion.get_chat_message_contents(
            chat_history=chat_history,
            settings=complete_prompt_execution_settings,
            kernel=kernel,
            arguments=KernelArguments(),
        )
        mock_create.assert_awaited_once_with(
            model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
            stream=False,
            messages=openai_chat_completion._prepare_chat_history_for_request(
                orig_chat_history
            ),
        )
        mock_process_function_call.assert_awaited()

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_cmc_function_choice_behavior(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_chat_completion_response.choices = [
        Choice(
            index=0,
            message=ChatCompletionMessage(
                content=None,
                role="assistant",
                tool_calls=[
                    {
                        "id": "test id",
                        "function": {
                            "name": "test-tool",
                            "arguments": '{"key": "value"}',
                        },
                        "type": "function",
                    }
                ],
            ),
            finish_reason="stop",
        )
    ]
    mock_create.return_value = mock_chat_completion_response
    chat_history.add_user_message("hello world")
    orig_chat_history = deepcopy(chat_history)
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id",
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
    )

    class MockPlugin:
        @kernel_function(name="test_tool")
        def test_tool(self, key: str):
            return "test"

    kernel.add_plugin(MockPlugin(), plugin_name="test_tool")

    with patch(
        "semantic_kernel.kernel.Kernel.invoke_function_call",
        new_callable=AsyncMock,
    ) as mock_process_function_call:
        openai_chat_completion = OpenAIChatCompletion()
        await openai_chat_completion.get_chat_message_contents(
            chat_history=chat_history,
            settings=complete_prompt_execution_settings,
            kernel=kernel,
            arguments=KernelArguments(),
        )
        mock_create.assert_awaited_once_with(
            model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
            stream=False,
            messages=openai_chat_completion._prepare_chat_history_for_request(
                orig_chat_history
            ),
            messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "test_tool-test_tool",
                        "description": "",
                        "parameters": {
                            "type": "object",
                            "properties": {"key": {"type": "string"}},
                            "required": ["key"],
                        },
                    },
                }
            ],
            tool_choice="auto",
        )
        mock_process_function_call.assert_awaited()

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_cmc_fcb_parallel_func_calling_disabled(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_chat_completion_response.choices = [
        Choice(
            index=0,
            message=ChatCompletionMessage(
                content=None,
                role="assistant",
                tool_calls=[
                    {
                        "id": "test id",
                        "function": {"name": "test-tool", "arguments": '{"key": "value"}'},
                        "type": "function",
                    }
                ],
            ),
            finish_reason="stop",
        )
    ]
    mock_create.return_value = mock_chat_completion_response
    chat_history.add_user_message("hello world")
    orig_chat_history = deepcopy(chat_history)
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id",
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
        parallel_tool_calls=False,
    )

    class MockPlugin:
        @kernel_function(name="test_tool")
        def test_tool(self, key: str):
            return "test"

    kernel.add_plugin(MockPlugin(), plugin_name="test_tool")

    with patch(
        "semantic_kernel.kernel.Kernel.invoke_function_call",
        new_callable=AsyncMock,
    ) as mock_process_function_call:
        openai_chat_completion = OpenAIChatCompletion()
        await openai_chat_completion.get_chat_message_contents(
            chat_history=chat_history,
            settings=complete_prompt_execution_settings,
            kernel=kernel,
            arguments=KernelArguments(),
        )
        mock_create.assert_awaited_once_with(
            model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
            stream=False,
            messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
            parallel_tool_calls=False,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "test_tool-test_tool",
                        "description": "",
                        "parameters": {
                            "type": "object",
                            "properties": {"key": {"type": "string"}},
                            "required": ["key"],
                        },
                    },
                }
            ],
            tool_choice="auto",
        )
        mock_process_function_call.assert_awaited()

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_cmc_function_choice_behavior_missing_kwargs(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_chat_completion_response.choices = [
        Choice(
            index=0,
            message=ChatCompletionMessage(
                content=None,
                role="assistant",
                tool_calls=[
                    {
                        "id": "test id",
                        "function": {
                            "name": "test-tool",
                            "arguments": '{"key": "value"}',
                        },
                        "type": "function",
                    }
                ],
            ),
            finish_reason="stop",
        )
    ]
    mock_create.return_value = mock_chat_completion_response
    chat_history.add_user_message("hello world")
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id",
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
    )
    openai_chat_completion = OpenAIChatCompletion()
    with pytest.raises(ServiceInvalidExecutionSettingsError):
        await openai_chat_completion.get_chat_message_contents(
            chat_history=chat_history,
            settings=complete_prompt_execution_settings,
            arguments=KernelArguments(),
        )
    with pytest.raises(ServiceInvalidExecutionSettingsError):
        complete_prompt_execution_settings.number_of_responses = 2
        await openai_chat_completion.get_chat_message_contents(
            chat_history=chat_history,
            settings=complete_prompt_execution_settings,
            kernel=kernel,
            arguments=KernelArguments(),
        )

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_cmc_no_fcc_in_response(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_create.return_value = mock_chat_completion_response
    chat_history.add_user_message("hello world")
    orig_chat_history = deepcopy(chat_history)
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id", function_choice_behavior="auto"
    )

    openai_chat_completion = OpenAIChatCompletion()
    await openai_chat_completion.get_chat_message_contents(
        chat_history=chat_history,
        settings=complete_prompt_execution_settings,
        kernel=kernel,
        arguments=KernelArguments(),
    )
    mock_create.assert_awaited_once_with(
        model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
        stream=False,
        messages=openai_chat_completion._prepare_chat_history_for_request(
            orig_chat_history
        ),
    )

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_cmc_structured_output_no_fcc(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_create.return_value = mock_chat_completion_response
    chat_history.add_user_message("hello world")
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(service_id="test_service_id")

    # Define a mock response format
    class Test:
        name: str

    complete_prompt_execution_settings.response_format = Test

    openai_chat_completion = OpenAIChatCompletion()
    await openai_chat_completion.get_chat_message_contents(
        chat_history=chat_history, settings=complete_prompt_execution_settings, kernel=kernel
    )
    mock_create.assert_awaited_once()

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_cmc_run_out_of_auto_invoke_loop(
    mock_create: MagicMock,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    kernel.add_function("test", kernel_function(lambda key: "test", name="test"))
    mock_chat_completion_response.choices = [
        Choice(
            index=0,
            message=ChatCompletionMessage(
                content=None,
                role="assistant",
                tool_calls=[
                    {
                        "id": "test id",
                        "function": {
                            "name": "test-test",
                            "arguments": '{"key": "value"}',
                        },
                        "type": "function",
                    }
                ],
            ),
            finish_reason="stop",
        )
    ]
    mock_create.return_value = mock_chat_completion_response
    chat_history.add_user_message("hello world")
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id", function_choice_behavior="auto"
    )

    openai_chat_completion = OpenAIChatCompletion()
    await openai_chat_completion.get_chat_message_contents(
        chat_history=chat_history,
        settings=complete_prompt_execution_settings,
        kernel=kernel,
        arguments=KernelArguments(),
    )
    # call count is the default number of auto_invoke attempts, plus the final completion
    # when there has not been a answer.
    mock_create.call_count == 6

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_scmc_prompt_execution_settings(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_streaming_chat_completion_response: AsyncStream[ChatCompletionChunk],
    openai_unit_test_env,
):
    mock_create.return_value = mock_streaming_chat_completion_response
    chat_history.add_user_message("hello world")
    complete_prompt_execution_settings = PromptExecutionSettings(
        service_id="test_service_id"
    )

    openai_chat_completion = OpenAIChatCompletion()
    async for msg in openai_chat_completion.get_streaming_chat_message_contents(
        chat_history=chat_history,
        settings=complete_prompt_execution_settings,
        kernel=kernel,
    ):
        assert isinstance(msg[0], StreamingChatMessageContent)
    mock_create.assert_awaited_once_with(
        model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
        stream=True,
        stream_options={"include_usage": True},
        stream_options={"include_usage": True},
        stream_options={"include_usage": True},
        stream_options={"include_usage": True},
        messages=openai_chat_completion._prepare_chat_history_for_request(chat_history),
    )

@pytest.mark.asyncio
@patch.object(
    AsyncChatCompletions, "create", new_callable=AsyncMock, side_effect=Exception
)
@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock, side_effect=Exception)
async def test_cmc_general_exception(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_create.return_value = mock_chat_completion_response
    chat_history.add_user_message("hello world")
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id"
    )

    openai_chat_completion = OpenAIChatCompletion()
    with pytest.raises(ServiceResponseException):
        await openai_chat_completion.get_chat_message_contents(
            chat_history=chat_history,
            settings=complete_prompt_execution_settings,
            kernel=kernel,
        )

# region Streaming

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_scmc(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    openai_unit_test_env,
):
    content1 = ChatCompletionChunk(
        id="test_id",
        choices=[],
        created=0,
        model="test",
        object="chat.completion.chunk",
    )
    content2 = ChatCompletionChunk(
        id="test_id",
        choices=[
            ChunkChoice(
                index=0,
                delta=ChunkChoiceDelta(content="test", role="assistant"),
                finish_reason="stop",
            )
        ],
        created=0,
        model="test",
        object="chat.completion.chunk",
    if tool_call:
        settings.function_call_behavior = MagicMock(spec=FunctionCallBehavior.AutoInvokeKernelFunctions())
        settings.function_call_behavior.auto_invoke_kernel_functions = True
        settings.function_call_behavior.max_auto_invoke_attempts = 5
        chat_history.messages = [mock_message]

    with (
        patch(
            "semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion_base.OpenAIChatCompletionBase._prepare_settings",
        ) as prepare_settings_mock,
        patch(
            "semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion_base.OpenAIChatCompletionBase._send_chat_request",
            return_value=mock_message_content,
        ) as mock_send_chat_request,
        patch(
            "semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion_base.OpenAIChatCompletionBase._process_function_call",
            new_callable=AsyncMock,
        ) as mock_process_function_call,
    ):
        chat_completion_base = OpenAIChatCompletionBase(
            ai_model_id="test_model_id", service_id="test", client=MagicMock(spec=AsyncOpenAI)
        )

        result = await chat_completion_base.get_chat_message_contents(
            chat_history, settings, kernel=kernel, arguments=arguments
        )

        assert result is not None
        prepare_settings_mock.assert_called_with(settings, chat_history, stream_request=False, kernel=kernel)
        mock_send_chat_request.assert_called_with(settings)

        if tool_call:
            mock_process_function_call.assert_awaited()
        else:
            mock_process_function_call.assert_not_awaited()

@pytest.mark.parametrize("tool_call", [False, True])
@pytest.mark.asyncio
async def test_complete_chat_function_choice_behavior(tool_call, kernel: Kernel):
    chat_history = MagicMock(spec=ChatHistory)
    chat_history.messages = []
    settings = MagicMock(spec=OpenAIChatPromptExecutionSettings)
    settings.number_of_responses = 1
    settings.function_choice_behavior = None
    mock_function_call = MagicMock(spec=FunctionCallContent)
    mock_text = MagicMock(spec=TextContent)
    mock_message = ChatMessageContent(
        role=AuthorRole.ASSISTANT, items=[mock_function_call] if tool_call else [mock_text]
    )
    mock_message_content = [mock_message]
    arguments = KernelArguments()

    if tool_call:
        settings.function_choice_behavior = MagicMock(spec=FunctionChoiceBehavior.Auto)
        settings.function_choice_behavior.auto_invoke_kernel_functions = True
        settings.function_choice_behavior.maximum_auto_invoke_attempts = 5
        chat_history.messages = [mock_message]

    with (
        patch(
            "semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion_base.OpenAIChatCompletionBase._prepare_settings",
        ) as prepare_settings_mock,
        patch(
            "semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion_base.OpenAIChatCompletionBase._send_chat_request",
            return_value=mock_message_content,
        ) as mock_send_chat_request,
        patch(
            "semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion_base.OpenAIChatCompletionBase._process_function_call",
            new_callable=AsyncMock,
        ) as mock_process_function_call,
    ):
        chat_completion_base = OpenAIChatCompletionBase(
            ai_model_id="test_model_id", service_id="test", client=MagicMock(spec=AsyncOpenAI)
        )

        result = await chat_completion_base.get_chat_message_contents(
            chat_history, settings, kernel=kernel, arguments=arguments
        )

        assert result is not None
        prepare_settings_mock.assert_called_with(settings, chat_history, stream_request=False, kernel=kernel)
        mock_send_chat_request.assert_called_with(settings)

        if tool_call:
            mock_process_function_call.assert_awaited()
        else:
            mock_process_function_call.assert_not_awaited()

@pytest.mark.asyncio
async def test_process_tool_calls():
    tool_call_mock = MagicMock(spec=FunctionCallContent)
    tool_call_mock.split_name_dict.return_value = {"arg_name": "arg_value"}
    tool_call_mock.to_kernel_arguments.return_value = {"arg_name": "arg_value"}
    tool_call_mock.name = "test_function"
    tool_call_mock.arguments = {"arg_name": "arg_value"}
    tool_call_mock.ai_model_id = None
    tool_call_mock.metadata = {}
    tool_call_mock.index = 0
    tool_call_mock.parse_arguments.return_value = {"arg_name": "arg_value"}
    tool_call_mock.id = "test_id"
    result_mock = MagicMock(spec=ChatMessageContent)
    result_mock.items = [tool_call_mock]
    chat_history_mock = MagicMock(spec=ChatHistory)

    func_mock = AsyncMock(spec=KernelFunction)
    func_meta = KernelFunctionMetadata(name="test_function", is_prompt=False)
    func_mock.metadata = func_meta
    func_mock.name = "test_function"
    func_result = FunctionResult(value="Function result", function=func_meta)
    func_mock.invoke = MagicMock(return_value=func_result)
    kernel_mock = MagicMock(spec=Kernel)
    kernel_mock.auto_function_invocation_filters = []
    kernel_mock.get_function.return_value = func_mock

    async def construct_call_stack(ctx):
        return ctx

    kernel_mock.construct_call_stack.return_value = construct_call_stack
    arguments = KernelArguments()

    chat_completion_base = OpenAIChatCompletionBase(
        ai_model_id="test_model_id", service_id="test", client=MagicMock(spec=AsyncOpenAI)
    )

    with patch("semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion_base.logger", autospec=True):
        await chat_completion_base._process_function_call(
            tool_call_mock,
            chat_history_mock,
            kernel_mock,
            arguments,
            1,
            0,
            FunctionCallBehavior.AutoInvokeKernelFunctions(),
        )

@pytest.mark.asyncio
async def test_process_tool_calls_with_continuation_on_malformed_arguments():
    tool_call_mock = MagicMock(spec=FunctionCallContent)
    tool_call_mock.parse_arguments.side_effect = FunctionCallInvalidArgumentsException("Malformed arguments")
    tool_call_mock.name = "test_function"
    tool_call_mock.arguments = {"arg_name": "arg_value"}
    tool_call_mock.ai_model_id = None
    tool_call_mock.metadata = {}
    tool_call_mock.index = 0
    tool_call_mock.parse_arguments.return_value = {"arg_name": "arg_value"}
    tool_call_mock.id = "test_id"
    result_mock = MagicMock(spec=ChatMessageContent)
    result_mock.items = [tool_call_mock]
    chat_history_mock = MagicMock(spec=ChatHistory)

    func_mock = MagicMock(spec=KernelFunction)
    func_meta = KernelFunctionMetadata(name="test_function", is_prompt=False)
    func_mock.metadata = func_meta
    func_mock.name = "test_function"
    func_result = FunctionResult(value="Function result", function=func_meta)
    func_mock.invoke = AsyncMock(return_value=func_result)
    kernel_mock = MagicMock(spec=Kernel)
    kernel_mock.auto_function_invocation_filters = []
    kernel_mock.get_function.return_value = func_mock
    arguments = KernelArguments()

    chat_completion_base = OpenAIChatCompletionBase(
        ai_model_id="test_model_id", service_id="test", client=MagicMock(spec=AsyncOpenAI)
    )
    stream = MagicMock(spec=AsyncStream)
    stream.__aiter__.return_value = [content1, content2]
    mock_create.return_value = stream
    chat_history.add_user_message("hello world")
    orig_chat_history = deepcopy(chat_history)
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id"
    )

    openai_chat_completion = OpenAIChatCompletion()
    async for msg in openai_chat_completion.get_streaming_chat_message_contents(
        chat_history=chat_history,
        settings=complete_prompt_execution_settings,
        kernel=kernel,
        arguments=KernelArguments(),
    ):
        assert isinstance(msg[0], StreamingChatMessageContent)
    mock_create.assert_awaited_once_with(
        model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
        stream=True,
        messages=openai_chat_completion._prepare_chat_history_for_request(
            orig_chat_history
        ),
        stream_options={"include_usage": True},
        messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
        stream_options={"include_usage": True},
        messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
        stream_options={"include_usage": True},
        messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
    )

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_scmc_singular(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    openai_unit_test_env,
):
    content1 = ChatCompletionChunk(
        id="test_id",
        choices=[],
        created=0,
        model="test",
        object="chat.completion.chunk",
    )
    content2 = ChatCompletionChunk(
        id="test_id",
        choices=[
            ChunkChoice(
                index=0,
                delta=ChunkChoiceDelta(content="test", role="assistant"),
                finish_reason="stop",
            )
        ],
        created=0,
        model="test",
        object="chat.completion.chunk",
    )
    stream = MagicMock(spec=AsyncStream)
    stream.__aiter__.return_value = [content1, content2]
    mock_create.return_value = stream
    chat_history.add_user_message("hello world")
    orig_chat_history = deepcopy(chat_history)
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id"
    )

    openai_chat_completion = OpenAIChatCompletion()
    async for msg in openai_chat_completion.get_streaming_chat_message_content(
        chat_history=chat_history,
        settings=complete_prompt_execution_settings,
        kernel=kernel,
        arguments=KernelArguments(),
    ):
        assert isinstance(msg, StreamingChatMessageContent)
    mock_create.assert_awaited_once_with(
        model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
        stream=True,
        messages=openai_chat_completion._prepare_chat_history_for_request(
            orig_chat_history
        ),
    )
    )
    )
    )
        stream_options={"include_usage": True},
        messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
    )

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_scmc_structured_output_no_fcc(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    openai_unit_test_env,
):
    content1 = ChatCompletionChunk(
        id="test_id",
        choices=[],
        created=0,
        model="test",
        object="chat.completion.chunk",
    )
    content2 = ChatCompletionChunk(
        id="test_id",
        choices=[ChunkChoice(index=0, delta=ChunkChoiceDelta(content="test", role="assistant"), finish_reason="stop")],
        created=0,
        model="test",
        object="chat.completion.chunk",
    )
    stream = MagicMock(spec=AsyncStream)
    stream.__aiter__.return_value = [content1, content2]
    mock_create.return_value = stream
    chat_history.add_user_message("hello world")
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(service_id="test_service_id")

    # Define a mock response format
    class Test:
        name: str

    complete_prompt_execution_settings.response_format = Test
    openai_chat_completion = OpenAIChatCompletion()
    async for msg in openai_chat_completion.get_streaming_chat_message_content(
        chat_history=chat_history,
        settings=complete_prompt_execution_settings,
        kernel=kernel,
        arguments=KernelArguments(),
    ):
        assert isinstance(msg, StreamingChatMessageContent)
    mock_create.assert_awaited_once()

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_scmc_function_call_behavior(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_streaming_chat_completion_response,
    openai_unit_test_env,
):
    mock_create.return_value = mock_streaming_chat_completion_response
    chat_history.add_user_message("hello world")
    orig_chat_history = deepcopy(chat_history)
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id",
        function_call_behavior=FunctionCallBehavior.AutoInvokeKernelFunctions(),

    )
    with patch(
        "semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion_base.OpenAIChatCompletionBase._process_function_call",
        new_callable=AsyncMock,
        return_value=None,
    ):
        openai_chat_completion = OpenAIChatCompletion()
        async for msg in openai_chat_completion.get_streaming_chat_message_contents(
            chat_history=chat_history,
            settings=complete_prompt_execution_settings,
            kernel=kernel,
            arguments=KernelArguments(),
        ):
            assert isinstance(msg[0], StreamingChatMessageContent)
        mock_create.assert_awaited_once_with(
            model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
            stream=True,
            messages=openai_chat_completion._prepare_chat_history_for_request(
                orig_chat_history
            ),
            stream_options={"include_usage": True},
            messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
            stream_options={"include_usage": True},
            messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
            stream_options={"include_usage": True},
            messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
        )

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_scmc_function_choice_behavior(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_streaming_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_create.return_value = mock_streaming_chat_completion_response
    chat_history.add_user_message("hello world")
    orig_chat_history = deepcopy(chat_history)
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id",
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
    )

    class MockPlugin:
        @kernel_function(name="test_tool")
        def test_tool(self, key: str):
            return "test"

    kernel.add_plugin(MockPlugin(), plugin_name="test_tool")

    with patch(
        "semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion_base.OpenAIChatCompletionBase._process_function_call",
        new_callable=AsyncMock,
        return_value=None,
    ):
        openai_chat_completion = OpenAIChatCompletion()
        async for msg in openai_chat_completion.get_streaming_chat_message_contents(
            chat_history=chat_history,
            settings=complete_prompt_execution_settings,
            kernel=kernel,
            arguments=KernelArguments(),
        ):
            assert isinstance(msg[0], StreamingChatMessageContent)
        mock_create.assert_awaited_once_with(
            model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
            stream=True,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "test_tool-test_tool",
                        "description": "",
                        "parameters": {
                            "type": "object",
                            "properties": {"key": {"type": "string"}},
                            "required": ["key"],
                        },
                    },
                }
            ],
            tool_choice="auto",
            stream_options={"include_usage": True},
            messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
        )

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_scmc_fcb_parallel_tool_call_disabled(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_streaming_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_create.return_value = mock_streaming_chat_completion_response
    chat_history.add_user_message("hello world")
    orig_chat_history = deepcopy(chat_history)
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id",
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
        parallel_tool_calls=False,
    )

    class MockPlugin:
        @kernel_function(name="test_tool")
        def test_tool(self, key: str):
            return "test"

    kernel.add_plugin(MockPlugin(), plugin_name="test_tool")

    with patch(
        "semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion_base.OpenAIChatCompletionBase._process_function_call",
        new_callable=AsyncMock,
        return_value=None,
    ):
        openai_chat_completion = OpenAIChatCompletion()
        async for msg in openai_chat_completion.get_streaming_chat_message_contents(
            chat_history=chat_history,
            settings=complete_prompt_execution_settings,
            kernel=kernel,
            arguments=KernelArguments(),
        ):
            assert isinstance(msg[0], StreamingChatMessageContent)
        mock_create.assert_awaited_once_with(
            model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
            stream=True,
            messages=openai_chat_completion._prepare_chat_history_for_request(
                orig_chat_history
            ),
            parallel_tool_calls=False,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "test_tool-test_tool",
                        "description": "",
                        "parameters": {
                            "type": "object",
                            "properties": {"key": {"type": "string"}},
                            "required": ["key"],
                        },
                    },
                }
            ],
            tool_choice="auto",
            stream_options={"include_usage": True},
            messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
            stream_options={"include_usage": True},
            messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
            stream_options={"include_usage": True},
            messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
        )

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_scmc_function_choice_behavior_missing_kwargs(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_streaming_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_create.return_value = mock_streaming_chat_completion_response
    chat_history.add_user_message("hello world")
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id",
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
    )
    openai_chat_completion = OpenAIChatCompletion()
    with pytest.raises(ServiceInvalidExecutionSettingsError):
        [
            msg
            async for msg in openai_chat_completion.get_streaming_chat_message_contents(
                chat_history=chat_history,
                settings=complete_prompt_execution_settings,
                arguments=KernelArguments(),
            )
        ]
    with pytest.raises(ServiceInvalidExecutionSettingsError):
        complete_prompt_execution_settings.number_of_responses = 2
        [
            msg
            async for msg in openai_chat_completion.get_streaming_chat_message_contents(
                chat_history=chat_history,
                settings=complete_prompt_execution_settings,
                kernel=kernel,
                arguments=KernelArguments(),
            )
        ]

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_scmc_no_fcc_in_response(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    mock_streaming_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_create.return_value = mock_streaming_chat_completion_response
    chat_history.add_user_message("hello world")
    orig_chat_history = deepcopy(chat_history)
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id", function_choice_behavior="auto"
    )

    openai_chat_completion = OpenAIChatCompletion()
    [
        msg
        async for msg in openai_chat_completion.get_streaming_chat_message_contents(
            chat_history=chat_history,
            settings=complete_prompt_execution_settings,
            kernel=kernel,
            arguments=KernelArguments(),
        )
    ]
    mock_create.assert_awaited_once_with(
        model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
        stream=True,
        messages=openai_chat_completion._prepare_chat_history_for_request(
            orig_chat_history
        ),
        stream_options={"include_usage": True},
        messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
        stream_options={"include_usage": True},
        messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
        stream_options={"include_usage": True},
        messages=openai_chat_completion._prepare_chat_history_for_request(orig_chat_history),
    )

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_scmc_run_out_of_auto_invoke_loop(
    mock_create: MagicMock,
    kernel: Kernel,
    chat_history: ChatHistory,
    openai_unit_test_env,
):
    kernel.add_function("test", kernel_function(lambda key: "test", name="test"))
    content = ChatCompletionChunk(
        id="test_id",
        choices=[
            ChunkChoice(
                index=0,
                finish_reason="tool_calls",
                delta=ChunkChoiceDelta(
                    role="assistant",
                    tool_calls=[
                        {
                            "index": 0,
                            "id": "test id",
                            "function": {
                                "name": "test-test",
                                "arguments": '{"key": "value"}',
                            },
                            "type": "function",
                        }
                    ],
                ),
            )
        ],
        created=0,
        model="test",
        object="chat.completion.chunk",
    )
    stream = MagicMock(spec=AsyncStream)
    stream.__aiter__.return_value = [content]
    mock_create.return_value = stream
    chat_history.add_user_message("hello world")
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id", function_choice_behavior="auto"
    )

    openai_chat_completion = OpenAIChatCompletion()
    [
        msg
        async for msg in openai_chat_completion.get_streaming_chat_message_contents(
            chat_history=chat_history,
            settings=complete_prompt_execution_settings,
            kernel=kernel,
            arguments=KernelArguments(),
        )
    ]
    # call count is the default number of auto_invoke attempts, plus the final completion
    # when there has not been a answer.
    mock_create.call_count == 6

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_scmc_no_stream(
    mock_create,
    kernel: Kernel,
    chat_history: ChatHistory,
    openai_unit_test_env,
    mock_chat_completion_response,
):
    mock_create.return_value = mock_chat_completion_response
    chat_history.add_user_message("hello world")
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id"
    )

    openai_chat_completion = OpenAIChatCompletion()
    with pytest.raises(ServiceInvalidResponseError):
        [
            msg
            async for msg in openai_chat_completion.get_streaming_chat_message_contents(
                chat_history=chat_history,
                settings=complete_prompt_execution_settings,
                kernel=kernel,
                arguments=KernelArguments(),
            )
        ]

# region TextContent

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_tc(
    mock_create,
    chat_history: ChatHistory,
    mock_chat_completion_response: ChatCompletion,
    openai_unit_test_env,
):
    mock_create.return_value = mock_chat_completion_response
    chat_history.add_user_message("hello world")
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id"
    )

    openai_chat_completion = OpenAIChatCompletion()
    tc = await openai_chat_completion.get_text_contents(
        prompt="test", settings=complete_prompt_execution_settings
    )
    assert isinstance(tc[0], TextContent)
    mock_create.assert_awaited_once_with(
        model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
        stream=False,
        messages=[{"role": "user", "content": "test"}],
    )

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_stc(
    mock_create,
    mock_streaming_chat_completion_response,
    openai_unit_test_env,
):
    mock_create.return_value = mock_streaming_chat_completion_response
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id"
    )
    openai_chat_completion = OpenAIChatCompletion()
    async for msg in openai_chat_completion.get_streaming_text_contents(
        prompt="test",
        settings=complete_prompt_execution_settings,
    ):
        assert isinstance(msg[0], StreamingTextContent)
    mock_create.assert_awaited_once_with(
        model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
        stream=True,
        messages=[{"role": "user", "content": "test"}],
    )

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_stc_with_msgs(
    mock_create,
    mock_streaming_chat_completion_response,
    openai_unit_test_env,
):
    mock_create.return_value = mock_streaming_chat_completion_response
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id",
        messages=[{"role": "system", "content": "system prompt"}],
    )
    openai_chat_completion = OpenAIChatCompletion()
    async for msg in openai_chat_completion.get_streaming_text_contents(
        prompt="test",
        settings=complete_prompt_execution_settings,
    ):
        assert isinstance(msg[0], StreamingTextContent)
    mock_create.assert_awaited_once_with(
        model=openai_unit_test_env["OPENAI_CHAT_MODEL_ID"],
        stream=True,
        messages=[
            {"role": "system", "content": "system prompt"},
            {"role": "user", "content": "test"},
        ],
    )

# region Autoinvoke

@patch.object(AsyncChatCompletions, "create", new_callable=AsyncMock)
async def test_scmc_terminate_through_filter(
    mock_create: MagicMock,
    kernel: Kernel,
    chat_history: ChatHistory,
    openai_unit_test_env,
):
    kernel.add_function("test", kernel_function(lambda key: "test", name="test"))

    @kernel.filter(FilterTypes.AUTO_FUNCTION_INVOCATION)
    async def auto_invoke_terminate(context, next):
        await next(context)
        context.terminate = True

    content = ChatCompletionChunk(
        id="test_id",
        choices=[
            ChunkChoice(
                index=0,
                finish_reason="tool_calls",
                delta=ChunkChoiceDelta(
                    role="assistant",
                    tool_calls=[
                        {
                            "index": 0,
                            "id": "test id",
                            "function": {
                                "name": "test-test",
                                "arguments": '{"key": "value"}',
                            },
                            "type": "function",
                        }
                    ],
                ),
            )
        ],
        created=0,
        model="test",
        object="chat.completion.chunk",
    )
    stream = MagicMock(spec=AsyncStream)
    stream.__aiter__.return_value = [content]
    mock_create.return_value = stream
    chat_history.add_user_message("hello world")
    complete_prompt_execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="test_service_id", function_choice_behavior="auto"
    )

    openai_chat_completion = OpenAIChatCompletion()
    [
        msg
        async for msg in openai_chat_completion.get_streaming_chat_message_contents(
            chat_history=chat_history,
            settings=complete_prompt_execution_settings,
            kernel=kernel,
            arguments=KernelArguments(),
        )
    ]
    # call count should be 1 here because we terminate
    mock_create.call_count == 1
    with patch("semantic_kernel.connectors.ai.function_calling_utils.logger", autospec=True):
        await chat_completion_base._process_function_call(
            tool_call_mock,
            chat_history_mock,
            kernel_mock,
            arguments,
            1,
            0,
            FunctionCallBehavior.AutoInvokeKernelFunctions(),
        )
