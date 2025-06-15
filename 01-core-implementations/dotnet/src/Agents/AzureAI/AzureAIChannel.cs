// Copyright (c) Microsoft. All rights reserved.
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Azure.AI.Agents.Persistent;
using Microsoft.SemanticKernel.Agents.AzureAI.Internal;
using Microsoft.SemanticKernel.Agents.Extensions;
using Microsoft.SemanticKernel.Diagnostics;
using AzureAIP = Azure.AI.Projects;

namespace Microsoft.SemanticKernel.Agents.AzureAI;

/// <summary>
/// A <see cref="AgentChannel"/> specialization for use with <see cref="AzureAIAgent"/>.
/// </summary>
internal sealed class AzureAIChannel(PersistentAgentsClient client, string threadId)
    : AgentChannel<AzureAIAgent>
{
    /// <inheritdoc/>
    protected override async Task ReceiveAsync(IEnumerable<ChatMessageContent> history, CancellationToken cancellationToken)
    {
        foreach (ChatMessageContent message in history)
        {
            await AgentThreadActions.CreateMessageAsync(client, threadId, message, cancellationToken).ConfigureAwait(false);
        }
    }

    /// <inheritdoc/>
    protected override IAsyncEnumerable<(bool IsVisible, ChatMessageContent Message)> InvokeAsync(
        AzureAIAgent agent,
        CancellationToken cancellationToken)
    {
        return ActivityExtensions.RunWithActivityAsync(
            () => ModelDiagnostics.StartAgentInvocationActivity(agent.Id, agent.GetDisplayName(), agent.Description),
            () => AgentThreadActions.InvokeAsync(agent, client, threadId, invocationOptions: null, this.Logger, agent.Kernel, agent.Arguments, cancellationToken),
            cancellationToken);
    }

    /// <inheritdoc/>
    protected override IAsyncEnumerable<StreamingChatMessageContent> InvokeStreamingAsync(AzureAIAgent agent, IList<ChatMessageContent> messages, CancellationToken cancellationToken = default)
    {
        return ActivityExtensions.RunWithActivityAsync(
            () => ModelDiagnostics.StartAgentInvocationActivity(agent.Id, agent.GetDisplayName(), agent.Description),
            () => AgentThreadActions.InvokeStreamingAsync(agent, client, threadId, messages, invocationOptions: null, this.Logger, agent.Kernel, agent.Arguments, cancellationToken),
            cancellationToken);
    }

    /// <inheritdoc/>
    protected override IAsyncEnumerable<ChatMessageContent> GetHistoryAsync(CancellationToken cancellationToken)
    {
        return AgentThreadActions.GetMessagesAsync(client, threadId, null, cancellationToken);
    }

    /// <inheritdoc/>
    protected override Task ResetAsync(CancellationToken cancellationToken = default)
    {
        return client.Threads.DeleteThreadAsync(threadId, cancellationToken);
    }

    /// <inheritdoc/>
    protected override string Serialize() { return threadId; }

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
