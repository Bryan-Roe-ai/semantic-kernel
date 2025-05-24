// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Generic;
using Microsoft.SemanticKernel.Agents.Abstractions;
using Microsoft.SemanticKernel.Contents;

namespace Microsoft.SemanticKernel.Connectors.Ollama.AgentMode;

/// <summary>
/// Thread implementation for the Ollama agent.
/// </summary>
public sealed class OllamaAgentThread : AgentThread
{
    private readonly List<ChatMessageContent> _messages = new();

    /// <summary>
    /// Gets the collection of messages in the thread.
    /// </summary>
    public IReadOnlyList<ChatMessageContent> Messages => this._messages.AsReadOnly();

    /// <summary>
    /// Adds a message to the thread.
    /// </summary>
    /// <param name="message">The message to add.</param>
    public void AddMessage(ChatMessageContent message)
    {
        this._messages.Add(message);
    }

    /// <summary>
    /// Adds a collection of messages to the thread.
    /// </summary>
    /// <param name="messages">The messages to add.</param>
    public void AddMessages(IEnumerable<ChatMessageContent> messages)
    {
        this._messages.AddRange(messages);
    }
}
