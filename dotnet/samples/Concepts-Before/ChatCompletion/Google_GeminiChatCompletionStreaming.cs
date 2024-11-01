﻿// Copyright (c) Microsoft. All rights reserved.

using System.Text;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;

namespace ChatCompletion;

public sealed class Google_GeminiChatCompletionStreaming(ITestOutputHelper output) : BaseTest(output)
{
    [Fact]
    public async Task GoogleAIAsync()
    {
        Console.WriteLine("============= Google AI - Gemini Chat Completion =============");

        string geminiApiKey = TestConfiguration.GoogleAI.ApiKey;
        string geminiModelId = TestConfiguration.GoogleAI.Gemini.ModelId;

        if (geminiApiKey is null || geminiModelId is null)
        {
            Console.WriteLine("Gemini credentials not found. Skipping example.");
            return;
        }

        Kernel kernel = Kernel.CreateBuilder()
            .AddGoogleAIGeminiChatCompletion(
                modelId: geminiModelId,
                apiKey: geminiApiKey)
            .Build();

        await RunSampleAsync(kernel);
    }

    [Fact]
    public async Task VertexAIAsync()
    {
        Console.WriteLine("============= Vertex AI - Gemini Chat Completion =============");

        string geminiBearerKey = TestConfiguration.VertexAI.BearerKey;
        string geminiModelId = TestConfiguration.VertexAI.Gemini.ModelId;
        string geminiLocation = TestConfiguration.VertexAI.Location;
        string geminiProject = TestConfiguration.VertexAI.ProjectId;

        if (geminiBearerKey is null || geminiModelId is null || geminiLocation is null || geminiProject is null)
        {
            Console.WriteLine("Gemini vertex ai credentials not found. Skipping example.");
            return;
        }

        Kernel kernel = Kernel.CreateBuilder()
            .AddVertexAIGeminiChatCompletion(
                modelId: geminiModelId,
                bearerKey: geminiBearerKey,
                location: geminiLocation,
                projectId: geminiProject)
            .Build();

        // To generate bearer key, you need installed google sdk or use google web console with command:
        //
        //   gcloud auth print-access-token
        //
        // Above code pass bearer key as string, it is not recommended way in production code,
        // especially if IChatCompletionService will be long lived, tokens generated by google sdk lives for 1 hour.
        // You should use bearer key provider, which will be used to generate token on demand:
        //
        // Example:
        //
        // Kernel kernel = Kernel.CreateBuilder()
        //     .AddVertexAIGeminiChatCompletion(
        //         modelId: TestConfiguration.VertexAI.Gemini.ModelId,
        //         bearerKeyProvider: () =>
        //         {
        //             // This is just example, in production we recommend using Google SDK to generate your BearerKey token.
        //             // This delegate will be called on every request,
        //             // when providing the token consider using caching strategy and refresh token logic when it is expired or close to expiration.
        //             return GetBearerKey();
        //         },
        //         location: TestConfiguration.VertexAI.Location,
        //         projectId: TestConfiguration.VertexAI.ProjectId);

        await RunSampleAsync(kernel);
    }

    private async Task RunSampleAsync(Kernel kernel)
    {
        await StreamingChatAsync(kernel);
    }

    private async Task StreamingChatAsync(Kernel kernel)
    {
        Console.WriteLine("======== Streaming Chat ========");

        var chatHistory = new ChatHistory("You are an expert in the tool shop.");
        var chat = kernel.GetRequiredService<IChatCompletionService>();

        // First user message
        chatHistory.AddUserMessage("Hi, I'm looking for alternative coffee brew methods, can you help me?");
        await MessageOutputAsync(chatHistory);

        // First bot assistant message
        var streamingChat = chat.GetStreamingChatMessageContentsAsync(chatHistory);
        var reply = await MessageOutputAsync(streamingChat);
        chatHistory.Add(reply);

        // Second user message
        chatHistory.AddUserMessage("Give me the best speciality coffee roasters.");
        await MessageOutputAsync(chatHistory);

        // Second bot assistant message
        streamingChat = chat.GetStreamingChatMessageContentsAsync(chatHistory);
        reply = await MessageOutputAsync(streamingChat);
        chatHistory.Add(reply);
    }

    /// <summary>
    /// Outputs the last message of the chat history
    /// </summary>
    private Task MessageOutputAsync(ChatHistory chatHistory)
    {
        var message = chatHistory.Last();

        Console.WriteLine($"{message.Role}: {message.Content}");
        Console.WriteLine("------------------------");

        return Task.CompletedTask;
    }

    private async Task<ChatMessageContent> MessageOutputAsync(IAsyncEnumerable<StreamingChatMessageContent> streamingChat)
    {
        bool first = true;
        StringBuilder messageBuilder = new();
        await foreach (var chatMessage in streamingChat)
        {
            if (first)
            {
                Console.Write($"{chatMessage.Role}: ");
                first = false;
            }

            Console.Write(chatMessage.Content);
            messageBuilder.Append(chatMessage.Content);
        }

        Console.WriteLine();
        Console.WriteLine("------------------------");
        return new ChatMessageContent(AuthorRole.Assistant, messageBuilder.ToString());
    }
}