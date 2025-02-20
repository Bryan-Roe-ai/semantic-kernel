﻿// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Generic;
using System.Net.Http;
using System.Text.Json.Nodes;
using System.Threading;
using System.Threading.Tasks;
using Azure.Core;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel.AI.ChatCompletion;
using Microsoft.SemanticKernel.AI.TextCompletion;
using Microsoft.SemanticKernel.Connectors.AI.OpenAI.AzureSdk;
using Microsoft.SemanticKernel.Connectors.AI.OpenAI.Models;

namespace Microsoft.SemanticKernel.Connectors.AI.OpenAI.ChatCompletion;

/// <summary>
/// Azure OpenAI chat completion client.
/// TODO: forward ETW logging to ILogger, see https://learn.microsoft.com/en-us/dotnet/azure/sdk/logging
/// </summary>
public sealed class AzureChatCompletion : AzureOpenAIClientBase, IChatCompletion, ITextCompletion
{
    /// <summary>
    /// Create an instance of the Azure OpenAI chat completion connector with API key auth
    /// </summary>
    /// <param name="modelId">Azure OpenAI model ID or deployment name, see https://learn.microsoft.com/azure/cognitive-services/openai/how-to/create-resource</param>
    /// <param name="endpoint">Azure OpenAI deployment URL, see https://learn.microsoft.com/azure/cognitive-services/openai/quickstart</param>
    /// <param name="apiKey">Azure OpenAI API key, see https://learn.microsoft.com/azure/cognitive-services/openai/quickstart</param>
    /// <param name="httpClient">Custom <see cref="HttpClient"/> for HTTP requests.</param>
    /// <param name="logger">Application logger</param>
    public AzureChatCompletion(
        string modelId,
        string endpoint,
        string apiKey,
        HttpClient? httpClient = null,
        ILogger? logger = null) : base(modelId, endpoint, apiKey, httpClient, logger)
    {
    }

    /// <summary>
    /// Create an instance of the Azure OpenAI chat completion connector with AAD auth
    /// </summary>
    /// <param name="modelId">Azure OpenAI model ID or deployment name, see https://learn.microsoft.com/azure/cognitive-services/openai/how-to/create-resource</param>
    /// <param name="endpoint">Azure OpenAI deployment URL, see https://learn.microsoft.com/azure/cognitive-services/openai/quickstart</param>
    /// <param name="credentials">Token credentials, e.g. DefaultAzureCredential, ManagedIdentityCredential, EnvironmentCredential, etc.</param>
    /// <param name="httpClient">Custom <see cref="HttpClient"/> for HTTP requests.</param>
    /// <param name="logger">Application logger</param>
    public AzureChatCompletion(
        string modelId,
        string endpoint,
        TokenCredential credentials,
        HttpClient? httpClient = null,
        ILogger? logger = null) : base(modelId, endpoint, credentials, httpClient, logger)
    {
    }

    /// <inheritdoc/>
    public Task<IReadOnlyList<IChatResult>> GetChatCompletionsAsync(
        ChatHistory chat,
        ChatRequestSettings? requestSettings = null,
        CancellationToken cancellationToken = default)
    {
        return this.InternalGetChatResultsAsync(chat, requestSettings, cancellationToken);
    }

    /// <inheritdoc/>
    public IAsyncEnumerable<IChatStreamingResult> GetStreamingChatCompletionsAsync(
        ChatHistory chat,
        ChatRequestSettings? requestSettings = null,
        CancellationToken cancellationToken = default)
    {
        return this.InternalGetChatStreamingResultsAsync(chat, requestSettings, cancellationToken);
    }

    /// <inheritdoc/>
    public ChatHistory CreateNewChat(string? instructions = null)
    {
        return InternalCreateNewChat(instructions);
    }

    /// <inheritdoc/>
    public IAsyncEnumerable<ITextCompletionStreamingResult> GetStreamingCompletionsAsync(
        string text,
        CompleteRequestSettings? requestSettings = null,
        CancellationToken cancellationToken = default)
    {
        return this.InternalGetChatStreamingResultsAsTextAsync(text, requestSettings, cancellationToken);
    }

    /// <inheritdoc/>
    public Task<IReadOnlyList<ITextCompletionResult>> GetCompletionsAsync(
        string text,
        CompleteRequestSettings? requestSettings = null,
        CancellationToken cancellationToken = default)
    {
        return this.InternalGetChatResultsAsTextAsync(text, requestSettings, cancellationToken);
    }

    /// <inheritdoc/>
    public Task<IReadOnlyList<ITextCompletionResult>> GetCompletionsAsync(
        string text,
        JsonObject requestSettings,
        CancellationToken cancellationToken = default)
    {
        var settings = CompletionRequestSettings.FromJson(requestSettings);
        return this.InternalCompleteTextUsingChatAsync(text, settings, cancellationToken);
    }

    /// <inheritdoc/>
    public IAsyncEnumerable<string> CompleteStreamAsync(string text,
        JsonObject requestSettings,
        CancellationToken cancellationToken = default)
    {
        var settings = CompletionRequestSettings.FromJson(requestSettings);
        return this.InternalCompleteTextUsingChatStreamAsync(text, settings, cancellationToken);
    }

    /// <summary>
    /// Interact with Azure Cognitive Services.
    /// </summary>
    /// <param name="input">The input data for the interaction.</param>
    /// <returns>The result of the interaction.</returns>
    public async Task<string> InteractWithAzureCognitiveServicesAsync(string input)
    {
        // Implement the logic to interact with Azure Cognitive Services here.
        // This is a placeholder implementation.
        await Task.Delay(100); // Simulate async operation
        return $"Processed input: {input}";
    }
}
