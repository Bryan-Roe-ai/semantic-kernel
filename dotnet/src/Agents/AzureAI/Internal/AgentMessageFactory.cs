<<<<<<< HEAD
﻿// Copyright (c) Microsoft. All rights reserved.
using System;
using System.Collections.Generic;
using System.Linq;
using Azure.AI.Projects;
=======
// Copyright (c) Microsoft. All rights reserved.
using System.Collections.Generic;
using System.Linq;
using Azure.AI.Projects;
using Microsoft.SemanticKernel.ChatCompletion;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

namespace Microsoft.SemanticKernel.Agents.AzureAI.Internal;

/// <summary>
/// Factory for creating <see cref="MessageContent"/> based on <see cref="ChatMessageContent"/>.
/// </summary>
/// <remarks>
/// Improves testability.
/// </remarks>
internal static class AgentMessageFactory
{
    /// <summary>
<<<<<<< HEAD
    /// %%%
=======
    /// Translate metadata from a <see cref="ChatMessageContent"/> to be used for a <see cref="ThreadMessage"/> or
    /// <see cref="ThreadMessageOptions"/>.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    /// <param name="message">The message content.</param>
    public static Dictionary<string, string> GetMetadata(ChatMessageContent message)
    {
        return message.Metadata?.ToDictionary(kvp => kvp.Key, kvp => kvp.Value?.ToString() ?? string.Empty) ?? [];
    }

<<<<<<< HEAD
    ///// <summary>
    ///// Translates <see cref="ChatMessageContent.Items"/> into enumeration of <see cref="MessageContent"/>.
    ///// </summary>
    ///// <param name="message">The message content.</param>
    //public static IEnumerable<MessageContent> GetMessageContents(ChatMessageContent message) // %%%
    //{
    //    bool hasTextContent = message.Items.OfType<TextContent>().Any();
    //    foreach (KernelContent content in message.Items)
    //    {
    //        if (content is TextContent textContent)
    //        {
    //            yield return new MessageTextContent(content.ToString());
    //        }
    //        else if (content is ImageContent imageContent)
    //        {
    //            if (imageContent.Uri != null)
    //            {
    //                yield return MessageContent.FromImageUri(imageContent.Uri);
    //            }
    //            else if (!string.IsNullOrWhiteSpace(imageContent.DataUri))
    //            {
    //                yield return MessageContent.FromImageUri(new(imageContent.DataUri!));
    //            }
    //        }
    //        else if (content is FileReferenceContent fileContent)
    //        {
    //            yield return MessageContent.FromImageFileId(fileContent.FileId);
    //        }
    //        else if (content is FunctionResultContent resultContent && resultContent.Result != null && !hasTextContent)
    //        {
    //            // Only convert a function result when text-content is not already present
    //            yield return MessageContent.FromText(FunctionCallsProcessor.ProcessFunctionResult(resultContent.Result));
    //        }
    //    }
    //}

    internal static IEnumerable<ThreadMessageOptions> GetThreadMessages(IReadOnlyList<ChatMessageContent>? messages)
    {
        //if (options?.Messages is not null)
        //{
        //    foreach (ChatMessageContent message in options.Messages)
        //    {
        //        AzureAIP.ThreadMessageOptions threadMessage = new(
        //            role: message.Role == AuthorRole.User ? AzureAIP.MessageRole.User : AzureAIP.MessageRole.Agent,
        //            content: AgentMessageFactory.GetMessageContents(message));

        //        createOptions.InitialMessages.Add(threadMessage);
        //    }
        //}

        throw new NotImplementedException();
=======
    /// <summary>
    /// Translate attachments from a <see cref="ChatMessageContent"/> to be used for a <see cref="ThreadMessage"/> or
    /// </summary>
    /// <param name="message">The message content.</param>
    public static IEnumerable<MessageAttachment> GetAttachments(ChatMessageContent message)
    {
        return
            message.Items
                .OfType<FileReferenceContent>()
                .Select(
                    fileContent =>
                        new MessageAttachment(fileContent.FileId, GetToolDefinition(fileContent.Tools).ToList()));
    }

    /// <summary>
    /// Translates a set of <see cref="ChatMessageContent"/> to a set of <see cref="ThreadMessageOptions"/>."/>
    /// </summary>
    /// <param name="messages">A list of <see cref="ChatMessageContent"/> objects/</param>
    public static IEnumerable<ThreadMessageOptions> GetThreadMessages(IEnumerable<ChatMessageContent>? messages)
    {
        if (messages is not null)
        {
            foreach (ChatMessageContent message in messages)
            {
                string? content = message.Content;
                if (string.IsNullOrWhiteSpace(content))
                {
                    continue;
                }

                ThreadMessageOptions threadMessage = new(
                    role: message.Role == AuthorRole.User ? MessageRole.User : MessageRole.Agent,
                    content: message.Content)
                {
                    Attachments = GetAttachments(message).ToArray(),
                };

                if (message.Metadata != null)
                {
                    foreach (string key in message.Metadata.Keys)
                    {
                        threadMessage.Metadata = GetMetadata(message);
                    }
                }

                yield return threadMessage;
            }
        }
    }

    private static readonly Dictionary<string, ToolDefinition> s_toolMetadata = new()
    {
        { AzureAIAgent.Tools.CodeInterpreter, new CodeInterpreterToolDefinition() },
        { AzureAIAgent.Tools.FileSearch, new FileSearchToolDefinition() },
    };

    private static IEnumerable<ToolDefinition> GetToolDefinition(IEnumerable<string>? tools)
    {
        if (tools is null)
        {
            yield break;
        }

        foreach (string tool in tools)
        {
            if (s_toolMetadata.TryGetValue(tool, out ToolDefinition? toolDefinition))
            {
                yield return toolDefinition;
            }
        }
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }
}
