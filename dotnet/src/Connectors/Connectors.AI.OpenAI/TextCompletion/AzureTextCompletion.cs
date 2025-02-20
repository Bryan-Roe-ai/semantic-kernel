﻿// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Generic;
using System.Net.Http;
using System.Text.Json.Nodes;
using System.Threading;
using System.Threading.Tasks;
using Azure.Core;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel.AI.TextCompletion;
using Microsoft.SemanticKernel.Connectors.AI.OpenAI.AzureSdk;
using Microsoft.SemanticKernel.Connectors.AI.OpenAI.Models;

namespace Microsoft.SemanticKernel.Connectors.AI.OpenAI.TextCompletion;

/// <summary>
/// Azure OpenAI text completion client.
/// TODO: forward ETW logging to ILogger, see https://learn.microsoft.com/en-us/dotnet/azure/sdk/logging
/// </summary>
public sealed class AzureTextCompletion : AzureOpenAIClientBase, ITextCompletion
{
    /// <summary>
    /// Creates a new AzureTextCompletion client instance using API Key auth
    /// </summary>
    /// <param name="modelId">Azure OpenAI model ID or deployment name, see https://learn.microsoft.com/azure/cognitive-services/openai/how-to/create-resource</param>
    /// <param name="endpoint">Azure OpenAI deployment URL, see https://learn.microsoft.com/azure/cognitive-services/openai/quickstart</param>
    /// <param name="apiKey">Azure OpenAI API key, see https://learn.microsoft.com/azure/cognitive-services/openai/quickstart</param>
    /// <param name="httpClient">Custom <see cref="HttpClient"/> for HTTP requests.</param>
    /// <param name="logger">Application logger</param>
    public AzureTextCompletion(
        string modelId,
        string endpoint,
        string apiKey,
        HttpClient? httpClient = null,
        ILogger? logger = null) : base(modelId, endpoint, apiKey, httpClient, logger)
    {
    }

    /// <summary>
    /// Creates a new AzureTextCompletion client instance supporting AAD auth
    /// </summary>
    /// <param name="modelId">Azure OpenAI model ID or deployment name, see https://learn.microsoft.com/azure/cognitive-services/openai/how-to/create-resource</param>
    /// <param name="endpoint">Azure OpenAI deployment URL, see https://learn.microsoft.com/azure/cognitive-services/openai/quickstart</param>
    /// <param name="credential">Token credentials, e.g. DefaultAzureCredential, ManagedIdentityCredential, EnvironmentCredential, etc.</param>
    /// <param name="httpClient">Custom <see cref="HttpClient"/> for HTTP requests.</param>
    /// <param name="logger">Application logger</param>
    public AzureTextCompletion(
        string modelId,
        string endpoint,
        TokenCredential credential,
        HttpClient? httpClient = null,
        ILogger? logger = null) : base(modelId, endpoint, credential, httpClient, logger)
    {
    }

    /// <inheritdoc/>
    public IAsyncEnumerable<ITextCompletionStreamingResult> GetStreamingCompletionsAsync(
        string text,
        JsonObject requestSettings,
        CancellationToken cancellationToken = default)
    {
        return this.InternalGetTextStreamingResultsAsync(text, requestSettings, cancellationToken);
        var settings = CompletionRequestSettings.FromJson(requestSettings);
        return this.InternalCompleteTextAsync(text, settings, cancellationToken);
    }

    /// <inheritdoc/>
    public Task<IReadOnlyList<ITextCompletionResult>> GetCompletionsAsync(
        string text,
        JsonObject requestSettings,
        CancellationToken cancellationToken = default)
    {
        return this.InternalGetTextResultsAsync(text, requestSettings, cancellationToken);
        var settings = CompletionRequestSettings.FromJson(requestSettings);
        return this.InternalCompletionStreamAsync(text, settings, cancellationToken);
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
