<<<<<<< HEAD
﻿// Copyright (c) Microsoft. All rights reserved.
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.SemanticKernel.Agents.AzureAI.Internal;
using AzureAIP = Azure.AI.Projects;
=======
// Copyright (c) Microsoft. All rights reserved.
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Azure.AI.Projects;
using Microsoft.SemanticKernel.Agents.AzureAI.Internal;
using Microsoft.SemanticKernel.Agents.Extensions;
using Microsoft.SemanticKernel.Diagnostics;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

namespace Microsoft.SemanticKernel.Agents.AzureAI;

/// <summary>
/// A <see cref="AgentChannel"/> specialization for use with <see cref="AzureAIAgent"/>.
/// </summary>
<<<<<<< HEAD
internal sealed class AzureAIChannel(AzureAIP.AgentsClient client, string threadId)
=======
internal sealed class AzureAIChannel(AgentsClient client, string threadId)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
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
<<<<<<< HEAD
        agent.ThrowIfDeleted();

        // %%%
        //return AgentThreadActions.InvokeAsync(agent, client, threadId, invocationOptions: null, this.Logger, agent.Kernel, agent.Arguments, cancellationToken);
        return Array.Empty<(bool, ChatMessageContent)>().ToAsyncEnumerable();
=======
        return ActivityExtensions.RunWithActivityAsync(
            () => ModelDiagnostics.StartAgentInvocationActivity(agent.Id, agent.GetDisplayName(), agent.Description),
            () => AgentThreadActions.InvokeAsync(agent, client, threadId, invocationOptions: null, this.Logger, agent.Kernel, agent.Arguments, cancellationToken),
            cancellationToken);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <inheritdoc/>
    protected override IAsyncEnumerable<StreamingChatMessageContent> InvokeStreamingAsync(AzureAIAgent agent, IList<ChatMessageContent> messages, CancellationToken cancellationToken = default)
    {
<<<<<<< HEAD
        agent.ThrowIfDeleted();

        // %%%
        //return AgentThreadActions.InvokeStreamingAsync(agent, client, threadId, messages, invocationOptions: null, this.Logger, agent.Kernel, agent.Arguments, cancellationToken);
        return Array.Empty<StreamingChatMessageContent>().ToAsyncEnumerable();
=======
        return ActivityExtensions.RunWithActivityAsync(
            () => ModelDiagnostics.StartAgentInvocationActivity(agent.Id, agent.GetDisplayName(), agent.Description),
            () => AgentThreadActions.InvokeStreamingAsync(agent, client, threadId, messages, invocationOptions: null, this.Logger, agent.Kernel, agent.Arguments, cancellationToken),
            cancellationToken);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <inheritdoc/>
    protected override IAsyncEnumerable<ChatMessageContent> GetHistoryAsync(CancellationToken cancellationToken)
    {
<<<<<<< HEAD
        return AgentThreadActions.GetMessagesAsync(client, threadId, cancellationToken);
=======
        return AgentThreadActions.GetMessagesAsync(client, threadId, null, cancellationToken);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <inheritdoc/>
    protected override Task ResetAsync(CancellationToken cancellationToken = default)
    {
        return client.DeleteThreadAsync(threadId, cancellationToken);
    }

    /// <inheritdoc/>
    protected override string Serialize() { return threadId; }
<<<<<<< HEAD

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
=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
}
