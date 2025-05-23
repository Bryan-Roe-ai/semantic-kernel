<<<<<<< HEAD
﻿// Copyright (c) Microsoft. All rights reserved.
=======
// Copyright (c) Microsoft. All rights reserved.
using System;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
<<<<<<< HEAD
using Microsoft.SemanticKernel.Agents.AzureAI.Internal;
using AzureAIP = Azure.AI.Projects;
=======
using Azure.AI.Projects;
using Microsoft.SemanticKernel.Agents.AzureAI.Internal;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

namespace Microsoft.SemanticKernel.Agents.AzureAI.Extensions;

/// <summary>
<<<<<<< HEAD
/// %%%
=======
/// Extensions associated with an Agent run processing.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
/// </summary>
/// <remarks>
/// Improves testability.
/// </remarks>
internal static class AgentRunExtensions
{
<<<<<<< HEAD
    public static async IAsyncEnumerable<AzureAIP.RunStep> GetStepsAsync(
        this AzureAIP.AgentsClient client,
        AzureAIP.ThreadRun run,
        [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        AzureAIP.PageableList<AzureAIP.RunStep>? steps = null;
        do
        {
            steps = await client.GetRunStepsAsync(run, cancellationToken: cancellationToken).ConfigureAwait(false);
            foreach (AzureAIP.RunStep step in steps)
=======
    public static async IAsyncEnumerable<RunStep> GetStepsAsync(
        this AgentsClient client,
        ThreadRun run,
        [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        PageableList<RunStep>? steps = null;
        do
        {
            steps = await client.GetRunStepsAsync(run, after: steps?.LastId, cancellationToken: cancellationToken).ConfigureAwait(false);
            foreach (RunStep step in steps)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            {
                yield return step;
            }
        }
        while (steps?.HasMore ?? false);
    }

<<<<<<< HEAD
    public static async Task<AzureAIP.ThreadRun> CreateAsync(
        this AzureAIP.AgentsClient client,
        string threadId,
        AzureAIAgent agent,
        string? instructions,
        AzureAIP.ToolDefinition[] tools,
        bool isStreaming,
        AzureAIInvocationOptions? invocationOptions,
        CancellationToken cancellationToken)
    {
=======
    public static async Task<ThreadRun> CreateAsync(
        this AgentsClient client,
        string threadId,
        AzureAIAgent agent,
        string? instructions,
        ToolDefinition[] tools,
        AzureAIInvocationOptions? invocationOptions,
        CancellationToken cancellationToken)
    {
        TruncationObject? truncationStrategy = GetTruncationStrategy(invocationOptions);
        BinaryData? responseFormat = GetResponseFormat(invocationOptions);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        return
            await client.CreateRunAsync(
                threadId,
                agent.Definition.Id,
                overrideModelName: invocationOptions?.ModelName,
<<<<<<< HEAD
                instructions,
                additionalInstructions: invocationOptions?.AdditionalInstructions,
                additionalMessages: AgentMessageFactory.GetThreadMessages(invocationOptions?.AdditionalMessages).ToArray(),
                overrideTools: tools,
                stream: isStreaming,
=======
                overrideInstructions: invocationOptions?.OverrideInstructions ?? instructions,
                additionalInstructions: invocationOptions?.AdditionalInstructions,
                additionalMessages: AgentMessageFactory.GetThreadMessages(invocationOptions?.AdditionalMessages).ToArray(),
                overrideTools: tools,
                stream: false,
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
                temperature: invocationOptions?.Temperature,
                topP: invocationOptions?.TopP,
                maxPromptTokens: invocationOptions?.MaxPromptTokens,
                maxCompletionTokens: invocationOptions?.MaxCompletionTokens,
<<<<<<< HEAD
                truncationStrategy: null, // %%%
                toolChoice: null, // %%%
                responseFormat: null, // %%%
                parallelToolCalls: invocationOptions?.ParallelToolCallsEnabled,
                metadata: invocationOptions?.Metadata,
                cancellationToken).ConfigureAwait(false);
    }
=======
                truncationStrategy,
                toolChoice: null,
                responseFormat,
                parallelToolCalls: invocationOptions?.ParallelToolCallsEnabled,
                metadata: invocationOptions?.Metadata,
                include: null,
                cancellationToken).ConfigureAwait(false);
    }

    private static BinaryData? GetResponseFormat(AzureAIInvocationOptions? invocationOptions)
    {
        return invocationOptions?.EnableJsonResponse == true ?
            BinaryData.FromString(ResponseFormat.JsonObject.ToString()) :
            null;
    }

    private static TruncationObject? GetTruncationStrategy(AzureAIInvocationOptions? invocationOptions)
    {
        return invocationOptions?.TruncationMessageCount == null ?
            null :
            new(TruncationStrategy.LastMessages)
            {
                LastMessages = invocationOptions.TruncationMessageCount
            };
    }

    public static IAsyncEnumerable<StreamingUpdate> CreateStreamingAsync(
        this AgentsClient client,
        string threadId,
        AzureAIAgent agent,
        string? instructions,
        ToolDefinition[] tools,
        AzureAIInvocationOptions? invocationOptions,
        CancellationToken cancellationToken)
    {
        TruncationObject? truncationStrategy = GetTruncationStrategy(invocationOptions);
        BinaryData? responseFormat = GetResponseFormat(invocationOptions);
        return
            client.CreateRunStreamingAsync(
                threadId,
                agent.Definition.Id,
                overrideModelName: invocationOptions?.ModelName,
                overrideInstructions: invocationOptions?.OverrideInstructions ?? instructions,
                additionalInstructions: invocationOptions?.AdditionalInstructions,
                additionalMessages: AgentMessageFactory.GetThreadMessages(invocationOptions?.AdditionalMessages).ToArray(),
                overrideTools: tools,
                temperature: invocationOptions?.Temperature,
                topP: invocationOptions?.TopP,
                maxPromptTokens: invocationOptions?.MaxPromptTokens,
                maxCompletionTokens: invocationOptions?.MaxCompletionTokens,
                truncationStrategy,
                toolChoice: null,
                responseFormat,
                parallelToolCalls: invocationOptions?.ParallelToolCallsEnabled,
                metadata: invocationOptions?.Metadata,
                cancellationToken);
    }
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
}
