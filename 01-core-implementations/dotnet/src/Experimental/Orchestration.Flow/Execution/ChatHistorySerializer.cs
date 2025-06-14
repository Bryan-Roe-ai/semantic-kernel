

﻿// Copyright (c) Microsoft. All rights reserved.

// Copyright (c) Microsoft. All rights reserved.

// Copyright (c) Microsoft. All rights reserved.

using System.Linq;
using System.Text.Json;
using Microsoft.SemanticKernel.ChatCompletion;
using System;

using System.Linq;
using System.Text.Json;
using Microsoft.SemanticKernel.ChatCompletion;

namespace Microsoft.SemanticKernel.Experimental.Orchestration.Execution;

internal static class ChatHistorySerializer
{
    internal static ChatHistory? Deserialize(string input)
    {
        if (string.IsNullOrEmpty(input))
        {
            return null;
        }

        var messages = JsonSerializer.Deserialize<SerializableChatMessage[]>(input) ?? [];
        ChatHistory history = [];

        var messages = JsonSerializer.Deserialize<SerializableChatMessage[]>(input) ?? Array.Empty<SerializableChatMessage>();
        ChatHistory history = new();

        var messages = JsonSerializer.Deserialize<SerializableChatMessage[]>(input) ?? Array.Empty<SerializableChatMessage>();
        ChatHistory history = new();

        foreach (var message in messages)
        {
            history.AddMessage(new AuthorRole(message.Role!), message.Content!);
        }

        return history;
    }

    internal static string Serialize(ChatHistory? history)
    {
        if (history is null)
        {
            return string.Empty;
        }

        var messages = history.Select(m => new SerializableChatMessage()

        var messages = history.Messages.Select(m => new SerializableChatMessage()

        var messages = history.Messages.Select(m => new SerializableChatMessage()

        var messages = history.Messages.Select(m => new SerializableChatMessage()

        var messages = history.Messages.Select(m => new SerializableChatMessage()

        var messages = history.Messages.Select(m => new SerializableChatMessage()

        var messages = history.Messages.Select(m => new SerializableChatMessage()

        var messages = history.Messages.Select(m => new SerializableChatMessage()

        var messages = history.Messages.Select(m => new SerializableChatMessage()

        {
            Role = m.Role.Label,
            Content = m.Content,
        });

        return JsonSerializer.Serialize(messages);
    }

    private sealed class SerializableChatMessage

    private class SerializableChatMessage

    private class SerializableChatMessage

    {
        public string? Role { get; set; }

        public string? Content { get; set; }
    }
}
