﻿// Copyright (c) Microsoft. All rights reserved.

using System.Threading;
using System.Threading.Tasks;

namespace Microsoft.SemanticKernel.AI.TextCompletion;

/// <summary>
/// Interface for text completion backends/services/clients
/// </summary>
public interface ITextCompletion
{
    /// <summary>
    /// Creates a completion for the prompt and settings.
    /// </summary>
    /// <param name="text">The prompt to complete.</param>
    /// <param name="requestSettings">Request settings for the completion API</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>Text generated by the remote model</returns>
    public Task<string> CompleteAsync(
        string text,
        CompleteRequestSettings requestSettings,
        CancellationToken cancellationToken = default);
}