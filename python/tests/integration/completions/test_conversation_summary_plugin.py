# Copyright (c) Microsoft. All rights reserved.


import pytest
from test_utils import retry

import semantic_kernel.connectors.ai.open_ai as sk_oai
from semantic_kernel.connectors.ai.prompt_execution_settings import (
    PromptExecutionSettings,
)
from semantic_kernel.connectors.ai.prompt_execution_settings import (
    PromptExecutionSettings,
)
from semantic_kernel.connectors.ai.prompt_execution_settings import (
    PromptExecutionSettings,
)
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.core_plugins.conversation_summary_plugin import (
    ConversationSummaryPlugin,
)
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.prompt_template.prompt_template_config import PromptTemplateConfig
from tests.integration.utils import retry
from tests.integration.utils import retry
from tests.utils import retry


@pytest.mark.asyncio
async def test_azure_summarize_conversation_using_plugin(
    setup_summarize_conversation_using_plugin,
):
    kernel, chatTranscript = setup_summarize_conversation_using_plugin

CHAT_TRANSCRIPT = """John: Hello, how are you?
Jane: I'm fine, thanks. How are you?
John: I'm doing well, writing some example code.
Jane: That's great! I'm writing some example code too.
John: What are you writing?
Jane: I'm writing a chatbot.
John: That's cool. I'm writing a chatbot too.
Jane: What language are you writing it in?
John: I'm writing it in C#.
Jane: I'm writing it in Python.
John: That's cool. I need to learn Python.
Jane: I need to learn C#.
John: Can I try out your chatbot?
Jane: Sure, here's the link.
John: Thanks!
Jane: You're welcome.
Jane: Look at this poem my chatbot wrote:
Jane: Roses are red
Jane: Violets are blue
Jane: I'm writing a chatbot
Jane: What about you?
John: That's cool. Let me see if mine will write a poem, too.
John: Here's a poem my chatbot wrote:
John: The singularity of the universe is a mystery.
Jane: You might want to try using a different model.
John: I'm using the GPT-2 model. That makes sense.
John: Here is a new poem after updating the model.
John: The universe is a mystery.
John: The universe is a mystery.
John: The universe is a mystery.
Jane: Sure, what's the problem?
John: Thanks for the help!
Jane: I'm now writing a bot to summarize conversations.
Jane: I have some bad news, we're only half way there.
John: Maybe there is a large piece of text we can use to generate a long conversation.
Jane: That's a good idea. Let me see if I can find one. Maybe Lorem Ipsum?
John: Yeah, that's a good idea."""


async def test_azure_summarize_conversation_using_plugin(kernel):
    service_id = "text_completion"

    execution_settings = PromptExecutionSettings(
        service_id=service_id,
        max_tokens=ConversationSummaryPlugin._max_tokens,
        temperature=0.1,
        top_p=0.5,
    )
    prompt_template_config = PromptTemplateConfig(
        description="Given a section of a conversation transcript, summarize the part of the conversation.",
        execution_settings={service_id: execution_settings},
    )

    kernel.add_service(sk_oai.OpenAIChatCompletion(service_id=service_id))

    conversationSummaryPlugin = kernel.add_plugin(
        ConversationSummaryPlugin(prompt_template_config), "conversationSummary"
    )

    arguments = KernelArguments(input=chatTranscript)

    summary = await retry(
        lambda: kernel.invoke(
            conversationSummaryPlugin["SummarizeConversation"], arguments
        )
    )

    )

    if "Python_Integration_Tests" in os.environ:
        deployment_name = os.environ["AzureOpenAI__DeploymentName"]
        api_key = os.environ["AzureOpenAI__ApiKey"]
        endpoint = os.environ["AzureOpenAI__Endpoint"]
    else:
        # Load credentials from .env file
        deployment_name, api_key, endpoint = get_aoai_config
        deployment_name = "gpt-35-turbo-instruct"

    service_id = "text_completion"

    execution_settings = PromptExecutionSettings(
        service_id=service_id, max_tokens=ConversationSummaryPlugin._max_tokens, temperature=0.1, top_p=0.5
    )
    prompt_template_config = PromptTemplateConfig(
        template=ConversationSummaryPlugin._summarize_conversation_prompt_template,
        description="Given a section of a conversation transcript, summarize the part of" " the conversation.",
        execution_settings=execution_settings,
    )

    kernel.add_service(
        sk_oai.AzureTextCompletion(
            service_id=service_id, deployment_name=deployment_name, endpoint=endpoint, api_key=api_key
        ),
    )

    conversationSummaryPlugin = kernel.import_plugin(
        ConversationSummaryPlugin(kernel, prompt_template_config), "conversationSummary"
    )

    arguments = KernelArguments(input=chatTranscript)

    summary = await retry(lambda: kernel.invoke(conversationSummaryPlugin["SummarizeConversation"], arguments))

    output = str(summary).strip().lower()
    print(output)
    assert "john" in output and "jane" in output
    assert len(output) < len(chatTranscript)


@pytest.mark.asyncio
async def test_oai_summarize_conversation_using_plugin(
    setup_summarize_conversation_using_plugin,
):
    kernel, chatTranscript = setup_summarize_conversation_using_plugin

    execution_settings = PromptExecutionSettings(
        service_id="conversation_summary",
        max_tokens=ConversationSummaryPlugin._max_tokens,
        temperature=0.1,
        top_p=0.5,
    )
    prompt_template_config = PromptTemplateConfig(
        template=ConversationSummaryPlugin._summarize_conversation_prompt_template,
        description="Given a section of a conversation transcript, summarize the part of the conversation.",
        execution_settings=execution_settings,
    )

    kernel.add_service(sk_oai.OpenAITextCompletion(service_id="conversation_summary"))
    arguments = KernelArguments(input=CHAT_TRANSCRIPT)

    summary = await retry(
        lambda: kernel.invoke(conversationSummaryPlugin["SummarizeConversation"], arguments), retries=5
    )

    arguments = KernelArguments(input=chatTranscript)

    summary = await retry(
        lambda: kernel.invoke(
            conversationSummaryPlugin["SummarizeConversation"], arguments
        )
    )

    )

    _, chatTranscript = setup_summarize_conversation_using_plugin

    # Even though the kernel is scoped to the function, it appears that
    # it is shared because adding the same plugin throws an error.
    # Create a new kernel for this test.
    kernel = sk.Kernel()

    if "Python_Integration_Tests" in os.environ:
        api_key = os.environ["OpenAI__ApiKey"]
        org_id = None
    else:
        # Load credentials from .env file
        api_key, org_id = sk.openai_settings_from_dot_env()

    execution_settings = PromptExecutionSettings(
        service_id="conversation_summary", max_tokens=ConversationSummaryPlugin._max_tokens, temperature=0.1, top_p=0.5
    )
    prompt_template_config = PromptTemplateConfig(
        template=ConversationSummaryPlugin._summarize_conversation_prompt_template,
        description="Given a section of a conversation transcript, summarize the part of" " the conversation.",
        execution_settings=execution_settings,
    )

    kernel.add_service(
        sk_oai.OpenAITextCompletion(
            service_id="conversation_summary", ai_model_id="gpt-3.5-turbo-instruct", api_key=api_key, org_id=org_id
        ),
    )

    conversationSummaryPlugin = kernel.import_plugin(
        ConversationSummaryPlugin(kernel, prompt_template_config), "conversationSummary"
    )

    arguments = KernelArguments(input=chatTranscript)

    summary = await retry(lambda: kernel.invoke(conversationSummaryPlugin["SummarizeConversation"], arguments))

    output = str(summary).strip().lower()
    print(output)
    assert "john" in output and "jane" in output
    assert len(output) < len(CHAT_TRANSCRIPT)
