// Copyright (c) Microsoft. All rights reserved.
using System;
using System.Collections.Generic;
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
using System.Threading;
using System.Threading.Tasks;
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
using System.Threading;
using System.Threading.Tasks;
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
using System.Threading;
using System.Threading.Tasks;
=======
>>>>>>> Stashed changes
=======
using System.Threading;
using System.Threading.Tasks;
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
using System.Diagnostics.CodeAnalysis;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.SemanticKernel.Agents.Serialization;
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< HEAD
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
=======
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.SemanticKernel.Agents.Serialization;
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377

namespace Microsoft.SemanticKernel.Agents;

/// <summary>
/// Defines the relationship between the internal aggregated chat and the chat
/// with which <see cref="AggregatorAgent"/> is participating.
/// </summary>
[Experimental("SKEXP0110")]
public enum AggregatorMode
{
    /// <summary>
    /// A flat embedding of the aggregated chat within another chat.
    /// </summary>
    Flat,

    /// <summary>
    /// A nested embedding the aggregated chat within another chat.
    /// </summary>
    Nested,
}

/// <summary>
/// Allows an <see cref="AgentChat"/> to participate in another <see cref="AgentChat"/> as an <see cref="Agent"/>.
/// </summary>
/// <param name="chatProvider">A factory method that produces a new <see cref="AgentChat"/> instance.</param>
[Experimental("SKEXP0110")]
public sealed class AggregatorAgent(Func<AgentChat> chatProvider) : Agent
{
    /// <summary>
    /// Gets the relationship between the internal aggregated chat and the chat
    /// with which <see cref="AggregatorAgent"/> is participating.
    /// </summary>
    /// <value>
    /// The relationship between the internal aggregated chat and the chat
    /// with which <see cref="AggregatorAgent"/> is participating. The default value is <see cref="AggregatorMode.Flat"/>.
    /// </value>
    public AggregatorMode Mode { get; init; } = AggregatorMode.Flat;

    /// <inheritdoc/>
    public override IAsyncEnumerable<AgentResponseItem<ChatMessageContent>> InvokeAsync(
        ICollection<ChatMessageContent> messages,
        AgentThread? thread = null,
        AgentInvokeOptions? options = null,
        CancellationToken cancellationToken = default)
    {
        // TODO: Need to determine the correct approach here.
        throw new NotImplementedException();
    }

    /// <inheritdoc/>
    public override IAsyncEnumerable<AgentResponseItem<StreamingChatMessageContent>> InvokeStreamingAsync(
        ICollection<ChatMessageContent> messages,
        AgentThread? thread = null,
        AgentInvokeOptions? options = null,
        CancellationToken cancellationToken = default)
    {
        // TODO: Need to determine the correct approach here.
        throw new NotImplementedException();
    }

    /// <inheritdoc/>
    /// <remarks>
    /// Different <see cref="AggregatorAgent"/> instances will never share the same channel.
    /// </remarks>
    protected internal override IEnumerable<string> GetChannelKeys()
    {
        yield return typeof(AggregatorChannel).FullName!;
        yield return this.Name ?? this.Id;
    }

    /// <inheritdoc/>
    protected internal override Task<AgentChannel> CreateChannelAsync(CancellationToken cancellationToken)
    {
        this.Logger.LogAggregatorAgentCreatingChannel(nameof(CreateChannelAsync), nameof(AggregatorChannel));
>>>>>>>-Updated upstrea
ebug("[{MethodName}] Creating channel {ChannelType}", nameof(CreateChannelAsync), nameof(AggregatorChannel));
        this.Logger.LogDebug("[{MethodName}] Creating channel {ChannelType}", nameof(CreateChannelAsync), nameof(AggregatorChannel));

        AgentChat chat = chatProvider.Invoke();
        AggregatorChannel channel = new(chat);

        this.Logger.LogAggregatorAgentCreatedChannel(nameof(CreateChannelAsync), nameof(AggregatorChannel), this.Mode, chat.GetType());
        this.Logger.LogInformation("[{MethodName}] Created channel {ChannelType} ({ChannelMode}) with: {AgentChatType}", nameof(CreateChannelAsync), nameof(AggregatorChannel), this.Mode, chat.GetType());

        return Task.FromResult<AgentChannel>(channel);
    }
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377

    /// <inheritdoc/>
    protected internal async override Task<AgentChannel> RestoreChannelAsync(string channelState, CancellationToken cancellationToken)
    {
        this.Logger.LogOpenAIAssistantAgentRestoringChannel(nameof(CreateChannelAsync), nameof(AggregatorChannel));

        AgentChat chat = chatProvider.Invoke();
        AgentChatState agentChatState =
            JsonSerializer.Deserialize<AgentChatState>(channelState) ??
            throw new KernelException("Unable to restore channel: invalid state.");

        await chat.DeserializeAsync(agentChatState).ConfigureAwait(false); ;
        AggregatorChannel channel = new(chat);

        this.Logger.LogOpenAIAssistantAgentRestoredChannel(nameof(CreateChannelAsync), nameof(AggregatorChannel));

        return channel;
    }
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< HEAD
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
}
