// Copyright (c) Microsoft. All rights reserved.
using System;
// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;

namespace SemanticKernel.Agents.UnitTests;

/// <summary>
/// Mock definition of <see cref="Agent"/> with a <see cref="ChatHistoryAgent"/> contract.
/// </summary>
internal class MockAgent : ChatHistoryKernelAgent
internal sealed class MockAgent : ChatHistoryAgent
{
    public int InvokeCount { get; private set; }

    public IReadOnlyList<ChatMessageContent> Response { get; set; } = [];

    public async override IAsyncEnumerable<AgentResponseItem<ChatMessageContent>> InvokeAsync(
        ICollection<ChatMessageContent> messages,
        AgentThread? thread = null,
        AgentInvokeOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        this.InvokeCount++;

        if (thread == null)
        {
            Mock<AgentThread> mockThread = new();
            thread = mockThread.Object;
        }

        foreach (ChatMessageContent response in this.Response)
        {
            AgentResponseItem<ChatMessageContent> responseItem = new(response, thread);
            if (options?.OnIntermediateMessage is not null)
            {
                await options.OnIntermediateMessage(responseItem);
                yield return responseItem;
            }
        }
    }

    protected internal override IAsyncEnumerable<ChatMessageContent> InvokeAsync(
        ChatHistory history,
        KernelArguments? arguments = null,
        Kernel? kernel = null,
        CancellationToken cancellationToken = default)
    {
        this.InvokeCount++;

        return this.Response.ToAsyncEnumerable();
    }

    /// <inheritdoc/>
    public async override IAsyncEnumerable<AgentResponseItem<StreamingChatMessageContent>> InvokeStreamingAsync(
        ICollection<ChatMessageContent> messages,
        AgentThread? thread = null,
        AgentInvokeOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        this.InvokeCount++;

        if (thread == null)
        {
            Mock<AgentThread> mockThread = new();
            thread = mockThread.Object;
        }

        foreach (ChatMessageContent response in this.Response)
        {
            if (options?.OnIntermediateMessage is not null)
            {
                await options.OnIntermediateMessage(new AgentResponseItem<ChatMessageContent>(response, thread));
                yield return new AgentResponseItem<StreamingChatMessageContent>(new StreamingChatMessageContent(response.Role, response.Content), thread);
            }
        }
    }

    protected internal override IAsyncEnumerable<StreamingChatMessageContent> InvokeStreamingAsync(
        ChatHistory history,
        KernelArguments? arguments = null,
        Kernel? kernel = null,
        CancellationToken cancellationToken = default)
    {
        this.InvokeCount++;
        return this.Response.Select(m => new StreamingChatMessageContent(m.Role, m.Content)).ToAsyncEnumerable();
    }

    /// <inheritdoc/>
    protected internal override IEnumerable<string> GetChannelKeys()
    {
        yield return typeof(ChatHistoryChannel).FullName!;
    }

    /// <inheritdoc/>
    protected internal override Task<AgentChannel> CreateChannelAsync(CancellationToken cancellationToken)
    {
        ChatHistoryChannel channel =
            new()
            {
                Logger = this.LoggerFactory.CreateLogger<ChatHistoryChannel>()
            };

        return Task.FromResult<AgentChannel>(channel);
    }

    protected internal override Task<AgentChannel> RestoreChannelAsync(string channelState, CancellationToken cancellationToken)
    {
        ChatHistory history =
            JsonSerializer.Deserialize<ChatHistory>(channelState) ??
            throw new KernelException("Unable to restore channel: invalid state.");
        return Task.FromResult<AgentChannel>(new ChatHistoryChannel(history));
    }

    // Expose protected method for testing
    public new KernelArguments? MergeArguments(KernelArguments? arguments)
    {
        return base.MergeArguments(arguments);
    }
}

// Unit tests for MockAgent
public class MockAgentTests
{
    [Fact]
    public async Task InvokeAsync_ShouldIncrementInvokeCountAndReturnExpectedResponse()
    {
        // Arrange
        var mockAgent = new MockAgent();
        var expectedResponse = new List<ChatMessageContent>
        {
            new ChatMessageContent("user", "Hello"),
            new ChatMessageContent("assistant", "Hi there!")
        };
        mockAgent.Response = expectedResponse;

        // Act
        var response = await mockAgent.InvokeAsync(new ChatHistory()).ToListAsync();

        // Assert
        Assert.Equal(1, mockAgent.InvokeCount);
        Assert.Equal(expectedResponse, response);
    }

    [Fact]
    public void MergeArguments_ShouldMergeKernelArgumentsCorrectly()
    {
        // Arrange
        var mockAgent = new MockAgent();
        var arguments1 = new KernelArguments
        {
            Parameters = new Dictionary<string, object>
            {
                { "param1", "value1" },
                { "param2", "value2" }
            }
        };
        var arguments2 = new KernelArguments
        {
            Parameters = new Dictionary<string, object>
            {
                { "param2", "new_value2" },
                { "param3", "value3" }
            }
        };

        // Act
        var mergedArguments = mockAgent.MergeArguments(arguments1);
        mergedArguments = mockAgent.MergeArguments(arguments2);

        // Assert
        Assert.NotNull(mergedArguments);
        Assert.Equal(3, mergedArguments.Parameters.Count);
        Assert.Equal("value1", mergedArguments.Parameters["param1"]);
        Assert.Equal("new_value2", mergedArguments.Parameters["param2"]);
        Assert.Equal("value3", mergedArguments.Parameters["param3"]);
   } 
    public new Task<string?> RenderInstructionsAsync(Kernel kernel, KernelArguments? arguments, CancellationToken cancellationToken)
    {
        return base.RenderInstructionsAsync(kernel, arguments, cancellationToken);
    }
}
