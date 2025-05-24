// Copyright (c) Microsoft. All rights reserved.
using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Xunit;

namespace SemanticKernel.Agents.UnitTests;

internal sealed class MockChannel : AgentChannel<MockAgent>
{
    public Exception? MockException { get; set; }

    public int InvokeCount { get; private set; }

    public int ReceiveCount { get; private set; }

    public TimeSpan ReceiveDuration { get; set; } = TimeSpan.FromSeconds(0.3);

    public List<ChatMessageContent> ReceivedMessages { get; } = [];

    protected internal override IAsyncEnumerable<ChatMessageContent> GetHistoryAsync(CancellationToken cancellationToken)
    {
        throw new NotImplementedException();
    }

    public IAsyncEnumerable<(bool IsVisible, ChatMessageContent Message)> InvokeAgentAsync(Agent agent, CancellationToken cancellationToken = default)
        => base.InvokeAsync(agent, cancellationToken);

#pragma warning disable CS1998 // Async method lacks 'await' operators and will run synchronously
    protected internal override async IAsyncEnumerable<(bool IsVisible, ChatMessageContent Message)> InvokeAsync(MockAgent agent, [EnumeratorCancellation] CancellationToken cancellationToken = default)
#pragma warning restore CS1998 // Async method lacks 'await' operators and will run synchronously
    {
        this.InvokeCount++;

        if (this.MockException is not null)
        {
            throw this.MockException;
        }

        yield break;
    }

    protected internal override IAsyncEnumerable<StreamingChatMessageContent> InvokeStreamingAsync(MockAgent agent, IList<ChatMessageContent> messages, CancellationToken cancellationToken = default)
    {
        throw new NotImplementedException();
    }

    protected internal override async Task ReceiveAsync(IEnumerable<ChatMessageContent> history, CancellationToken cancellationToken = default)
    {
        this.ReceivedMessages.AddRange(history);
        this.ReceiveCount++;

        await Task.Delay(this.ReceiveDuration, cancellationToken);

        if (this.MockException is not null)
        {
            throw this.MockException;
        }
    }

    protected internal override async Task ResetAsync(CancellationToken cancellationToken = default)
    {
        this.InvokeCount = 0;
        this.ReceiveCount = 0;
        this.ReceivedMessages.Clear();

        await Task.CompletedTask;
    }

    protected internal override string Serialize()
    {
        throw new NotImplementedException();
    }
}

public class MockChannelTests
{
    [Fact]
    public async Task VerifyInvokeAgentAsyncIncrementsInvokeCountAndHandlesDifferentAgentTypes()
    {
        // Arrange
        MockChannel channel = new();
        MockAgent mockAgent = new();
        MockAgent anotherMockAgent = new();

        // Act & Assert
        var messages = await channel.InvokeAgentAsync(mockAgent).ToArrayAsync();
        Assert.Equal(1, channel.InvokeCount);

        await Assert.ThrowsAsync<KernelException>(() => channel.InvokeAgentAsync(anotherMockAgent).ToArrayAsync().AsTask());
        Assert.Equal(1, channel.InvokeCount);
    }

    [Fact]
    public async Task VerifyReceiveAsyncIncrementsReceiveCountAndHandlesDifferentMessageHistories()
    {
        // Arrange
        MockChannel channel = new();
        List<ChatMessageContent> history1 = new() { new ChatMessageContent(AuthorRole.User, "Message 1") };
        List<ChatMessageContent> history2 = new() { new ChatMessageContent(AuthorRole.User, "Message 2") };

        // Act & Assert
        await channel.ReceiveAsync(history1);
        Assert.Equal(1, channel.ReceiveCount);
        Assert.Equal(1, channel.ReceivedMessages.Count);

        await channel.ReceiveAsync(history2);
        Assert.Equal(2, channel.ReceiveCount);
        Assert.Equal(2, channel.ReceivedMessages.Count);
    }

    [Fact]
    public async Task VerifyResetAsyncResetsChannelState()
    {
        // Arrange
        MockChannel channel = new();
        List<ChatMessageContent> history = new() { new ChatMessageContent(AuthorRole.User, "Message") };

        // Act
        await channel.ReceiveAsync(history);
        await channel.InvokeAgentAsync(new MockAgent()).ToArrayAsync();
        await channel.ResetAsync();

        // Assert
        Assert.Equal(0, channel.InvokeCount);
        Assert.Equal(0, channel.ReceiveCount);
        Assert.Empty(channel.ReceivedMessages);
    }
}
