// Copyright (c) Microsoft. All rights reserved.

using Azure.Identity;

using Azure.Identity;

using System.Text;
using Microsoft.SemanticKernel;

using System.Text;
using Microsoft.SemanticKernel;

using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.AzureOpenAI;
using Microsoft.SemanticKernel.Connectors.OpenAI;

namespace ChatCompletion;

// The following example shows how to use Semantic Kernel with OpenAI ChatGPT API
public class OpenAI_ChatCompletion(ITestOutputHelper output) : BaseTest(output)
{
    [Fact]
    public async Task OpenAIChatSampleAsync()
    {

// The following example shows how to use Semantic Kernel with OpenAI API

/// <summary>
/// These examples demonstrate different ways of using chat completion with OpenAI API.
/// </summary>

public class OpenAI_ChatCompletion(ITestOutputHelper output) : BaseTest(output)
{
    /// <summary>
    /// Sample showing how to use <see cref="IChatCompletionService"/> directly with a <see cref="ChatHistory"/>.
    /// </summary>
    [Fact]
    public async Task ServicePromptAsync()
    {
        Assert.NotNull(TestConfiguration.OpenAI.ChatModelId);
        Assert.NotNull(TestConfiguration.OpenAI.ApiKey);

        Console.WriteLine("======== Open AI - Chat Completion ========");

        OpenAIChatCompletionService chatService = new(TestConfiguration.OpenAI.ChatModelId, TestConfiguration.OpenAI.ApiKey);

        await StartChatAsync(chatCompletionService);

        /* Output:

        Chat content:
        ------------------------
        System: You are a librarian, expert about books
        ------------------------
        User: Hi, I'm looking for book suggestions
        ------------------------
        Assistant: Sure, I'd be happy to help! What kind of books are you interested in? Fiction or non-fiction? Any particular genre?
        ------------------------
        User: I love history and philosophy, I'd like to learn something new about Greece, any suggestion?
        ------------------------
        Assistant: Great! For history and philosophy books about Greece, here are a few suggestions:

        1. "The Greeks" by H.D.F. Kitto - This is a classic book that provides an overview of ancient Greek history and culture, including their philosophy, literature, and art.

        2. "The Republic" by Plato - This is one of the most famous works of philosophy in the Western world, and it explores the nature of justice and the ideal society.

        3. "The Peloponnesian War" by Thucydides - This is a detailed account of the war between Athens and Sparta in the 5th century BCE, and it provides insight into the political and military strategies of the time.

        4. "The Iliad" by Homer - This epic poem tells the story of the Trojan War and is considered one of the greatest works of literature in the Western canon.

        5. "The Histories" by Herodotus - This is a comprehensive account of the Persian Wars and provides a wealth of information about ancient Greek culture and society.

        I hope these suggestions are helpful!
        ------------------------
        */
    }

    [Fact]
    public async Task AzureOpenAIChatSampleAsync()
    {
        Console.WriteLine("======== Azure Open AI - Chat Completion ========");

        AzureOpenAIChatCompletionService chatCompletionService = new(
            deploymentName: TestConfiguration.AzureOpenAI.ChatDeploymentName,
            endpoint: TestConfiguration.AzureOpenAI.Endpoint,
            apiKey: TestConfiguration.AzureOpenAI.ApiKey,
            modelId: TestConfiguration.AzureOpenAI.ChatModelId);

        await StartChatAsync(chatCompletionService);
    }

    /// <summary>
    /// Sample showing how to use Azure Open AI Chat Completion with Azure Default Credential.
    /// If local auth is disabled in the Azure Open AI deployment, you can use Azure Default Credential to authenticate.
    /// </summary>
    [Fact]
    public async Task AzureOpenAIWithDefaultAzureCredentialSampleAsync()
    {
        Console.WriteLine("======== Azure Open AI - Chat Completion with Azure Default Credential ========");

        AzureOpenAIChatCompletionService chatCompletionService = new(
            deploymentName: TestConfiguration.AzureOpenAI.ChatDeploymentName,
            endpoint: TestConfiguration.AzureOpenAI.Endpoint,
            credentials: new DefaultAzureCredential(),
            modelId: TestConfiguration.AzureOpenAI.ChatModelId);

        await StartChatAsync(chatCompletionService);

        Console.WriteLine("Chat content:");
        Console.WriteLine("------------------------");

        var chatHistory = new ChatHistory("You are a librarian, expert about books");

        // First user message
        chatHistory.AddUserMessage("Hi, I'm looking for book suggestions");
        OutputLastMessage(chatHistory);

        // First assistant message
        var reply = await chatService.GetChatMessageContentAsync(chatHistory);
        chatHistory.Add(reply);
        OutputLastMessage(chatHistory);

        // Second user message
        chatHistory.AddUserMessage("I love history and philosophy, I'd like to learn something new about Greece, any suggestion");
        OutputLastMessage(chatHistory);

        // Second assistant message
        reply = await chatService.GetChatMessageContentAsync(chatHistory);
        chatHistory.Add(reply);
        OutputLastMessage(chatHistory);

    }

    /// <summary>
    /// Sample showing how to use <see cref="IChatCompletionService"/> directly with a <see cref="ChatHistory"/> also exploring the
    /// breaking glass approach capturing the underlying <see cref="OpenAI.Chat.ChatCompletion"/> instance via <see cref="KernelContent.InnerContent"/>.
    /// </summary>
    [Fact]
    public async Task ServicePromptWithInnerContentAsync()
    {
        Assert.NotNull(TestConfiguration.OpenAI.ChatModelId);
        Assert.NotNull(TestConfiguration.OpenAI.ApiKey);

        Console.WriteLine("======== Open AI - Chat Completion ========");

        OpenAIChatCompletionService chatService = new(TestConfiguration.OpenAI.ChatModelId, TestConfiguration.OpenAI.ApiKey);

        Console.WriteLine("Chat content:");
        Console.WriteLine("------------------------");

        var chatHistory = new ChatHistory("You are a librarian, expert about books");

        // First user message
        chatHistory.AddUserMessage("Hi, I'm looking for book suggestions");
        this.OutputLastMessage(chatHistory);

        // First assistant message
        var reply = await chatService.GetChatMessageContentAsync(chatHistory, new OpenAIPromptExecutionSettings { Logprobs = true, TopLogprobs = 3 });

        // Assistant message details
        var replyInnerContent = reply.InnerContent as OpenAI.Chat.ChatCompletion;

        OutputInnerContent(replyInnerContent!);
    }

    /// <summary>
    /// Sample showing how to use <see cref="Kernel"/> with chat completion and chat prompt syntax.
    /// </summary>
    [Fact]
    public async Task ChatPromptAsync()
    {
        Assert.NotNull(TestConfiguration.OpenAI.ChatModelId);
        Assert.NotNull(TestConfiguration.OpenAI.ApiKey);

        StringBuilder chatPrompt = new("""
                                       <message role="system">You are a librarian, expert about books</message>
                                       <message role="user">Hi, I'm looking for book suggestions</message>
                                       """);

        var kernel = Kernel.CreateBuilder()
            .AddOpenAIChatCompletion(TestConfiguration.OpenAI.ChatModelId, TestConfiguration.OpenAI.ApiKey)
            .Build();

        var reply = await kernel.InvokePromptAsync(chatPrompt.ToString());

        chatPrompt.AppendLine($"<message role=\"assistant\"><![CDATA[{reply}]]></message>");
        chatPrompt.AppendLine("<message role=\"user\">I love history and philosophy, I'd like to learn something new about Greece, any suggestion</message>");

        reply = await kernel.InvokePromptAsync(chatPrompt.ToString());

        Console.WriteLine(reply);
    }

    /// <summary>
    /// Demonstrates how you can template a chat history call and get extra information from the response while using the kernel for invocation.
    /// </summary>
    /// <remarks>
    /// This is a breaking glass scenario, any attempt on running with different versions of OpenAI SDK that introduces breaking changes
    /// may cause breaking changes in the code below.
    /// </remarks>
    [Fact]
    public async Task ChatPromptWithInnerContentAsync()
    {
        Assert.NotNull(TestConfiguration.OpenAI.ChatModelId);
        Assert.NotNull(TestConfiguration.OpenAI.ApiKey);

        StringBuilder chatPrompt = new("""
                                       <message role="system">You are a librarian, expert about books</message>
                                       <message role="user">Hi, I'm looking for book suggestions</message>
                                       """);

        var kernel = Kernel.CreateBuilder()
            .AddOpenAIChatCompletion(TestConfiguration.OpenAI.ChatModelId, TestConfiguration.OpenAI.ApiKey)
            .Build();

        var functionResult = await kernel.InvokePromptAsync(chatPrompt.ToString(),
            new(new OpenAIPromptExecutionSettings { Logprobs = true, TopLogprobs = 3 }));

        var messageContent = functionResult.GetValue<ChatMessageContent>(); // Retrieves underlying chat message content from FunctionResult.
        var replyInnerContent = messageContent!.InnerContent as OpenAI.Chat.ChatCompletion; // Retrieves inner content from ChatMessageContent.

        OutputInnerContent(replyInnerContent!);

    }

    /// <summary>
    /// Demonstrates how you can store the output of a chat completion request for use in the OpenAI model distillation or evals products.
    /// </summary>
    /// <remarks>
    /// This sample adds metadata to the chat completion request which allows the requests to be filtered in the OpenAI dashboard.
    /// </remarks>
    [Fact]
    public async Task ChatPromptStoreWithMetadataAsync()
    {
        Assert.NotNull(TestConfiguration.OpenAI.ChatModelId);
        Assert.NotNull(TestConfiguration.OpenAI.ApiKey);

        StringBuilder chatPrompt = new("""
                                       <message role="system">You are a librarian, expert about books</message>
                                       <message role="user">Hi, I'm looking for book suggestions about Artificial Intelligence</message>
                                       """);

        var kernel = Kernel.CreateBuilder()
            .AddOpenAIChatCompletion(TestConfiguration.OpenAI.ChatModelId, TestConfiguration.OpenAI.ApiKey)
            .Build();

        var functionResult = await kernel.InvokePromptAsync(chatPrompt.ToString(),
            new(new OpenAIPromptExecutionSettings { Store = true, Metadata = new Dictionary<string, string>() { { "concept", "chatcompletion" } } }));

        var messageContent = functionResult.GetValue<ChatMessageContent>(); // Retrieves underlying chat message content from FunctionResult.
        var replyInnerContent = messageContent!.InnerContent as OpenAI.Chat.ChatCompletion; // Retrieves inner content from ChatMessageContent.

        OutputInnerContent(replyInnerContent!);
    }

    private async Task StartChatAsync(IChatCompletionService chatGPT)
    {
        Console.WriteLine("Chat content:");
        Console.WriteLine("------------------------");

        var chatHistory = new ChatHistory("You are a librarian, expert about books");

        // First user message
        chatHistory.AddUserMessage("Hi, I'm looking for book suggestions");
        OutputLastMessage(chatHistory);

        // First assistant message
        var reply = await chatGPT.GetChatMessageContentAsync(chatHistory);
        chatHistory.Add(reply);
        OutputLastMessage(chatHistory);

        // Second user message
        chatHistory.AddUserMessage("I love history and philosophy, I'd like to learn something new about Greece, any suggestion");
        OutputLastMessage(chatHistory);

        // Second assistant message
        reply = await chatGPT.GetChatMessageContentAsync(chatHistory);
        chatHistory.Add(reply);
        OutputLastMessage(chatHistory);
    }

    /// <summary>
    /// Retrieve extra information from a <see cref="ChatMessageContent"/> inner content of type <see cref="OpenAI.Chat.ChatCompletion"/>.
    /// </summary>
    /// <param name="innerContent">An instance of <see cref="OpenAI.Chat.ChatCompletion"/> retrieved as an inner content of <see cref="ChatMessageContent"/>.</param>
    /// <remarks>
    /// This is a breaking glass scenario, any attempt on running with different versions of OpenAI SDK that introduces breaking changes
    /// may break the code below.
    /// </remarks>
    private void OutputInnerContent(OpenAI.Chat.ChatCompletion innerContent)
    {
        Console.WriteLine($$"""
            Message role: {{innerContent.Role}} // Available as a property of ChatMessageContent
            Message content: {{innerContent.Content[0].Text}} // Available as a property of ChatMessageContent

            Model: {{innerContent.Model}} // Model doesn't change per chunk, so we can get it from the first chunk only
            Created At: {{innerContent.CreatedAt}}

            Finish reason: {{innerContent.FinishReason}}
            Input tokens usage: {{innerContent.Usage.InputTokenCount}}
            Output tokens usage: {{innerContent.Usage.OutputTokenCount}}
            Total tokens usage: {{innerContent.Usage.TotalTokenCount}}
            Refusal: {{innerContent.Refusal}} 
            Id: {{innerContent.Id}}
            System fingerprint: {{innerContent.SystemFingerprint}}
            """);

        if (innerContent.ContentTokenLogProbabilities.Count > 0)
        {
            Console.WriteLine("Content token log probabilities:");
            foreach (var contentTokenLogProbability in innerContent.ContentTokenLogProbabilities)
            {
                Console.WriteLine($"Token: {contentTokenLogProbability.Token}");
                Console.WriteLine($"Log probability: {contentTokenLogProbability.LogProbability}");

                Console.WriteLine("   Top log probabilities for this token:");
                foreach (var topLogProbability in contentTokenLogProbability.TopLogProbabilities)
                {
                    Console.WriteLine($"   Token: {topLogProbability.Token}");
                    Console.WriteLine($"   Log probability: {topLogProbability.LogProbability}");
                    Console.WriteLine("   =======");
                }

                Console.WriteLine("--------------");
            }
        }

        if (innerContent.RefusalTokenLogProbabilities.Count > 0)
        {
            Console.WriteLine("Refusal token log probabilities:");
            foreach (var refusalTokenLogProbability in innerContent.RefusalTokenLogProbabilities)
            {
                Console.WriteLine($"Token: {refusalTokenLogProbability.Token}");
                Console.WriteLine($"Log probability: {refusalTokenLogProbability.LogProbability}");

                Console.WriteLine("   Refusal top log probabilities for this token:");
                foreach (var topLogProbability in refusalTokenLogProbability.TopLogProbabilities)
                {
                    Console.WriteLine($"   Token: {topLogProbability.Token}");
                    Console.WriteLine($"   Log probability: {topLogProbability.LogProbability}");
                    Console.WriteLine("   =======");
                }
            }
        }
    }

}
