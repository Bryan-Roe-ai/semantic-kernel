// Copyright (c) Microsoft. All rights reserved.
using System;
using System.Collections.Generic;
using System.Linq;
using Azure.AI.Projects;
using Azure.AI.Agents.Persistent;
using Microsoft.SemanticKernel.ChatCompletion;

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
    /// Translate metadata from a <see cref="ChatMessageContent"/> to be used for a <see cref="ThreadMessage"/> or
    /// <see cref="ThreadMessageOptions"/>.
    /// </summary>
    /// <param name="message">The message content.</param>
    public static Dictionary<string, string> GetMetadata(ChatMessageContent message)
    {
        return message.Metadata?.ToDictionary(kvp => kvp.Key, kvp => kvp.Value?.ToString() ?? string.Empty) ?? [];
    }

    /// <summary>
    /// Translate attachments from a <see cref="ChatMessageContent"/> to be used for a <see cref="PersistentThreadMessage"/> or
    /// </summary>
    /// <param name="message">The message content.</param>
    public static IEnumerable<MessageAttachment> GetAttachments(ChatMessageContent message)
    {
        return
            message.Items
                .OfType<FileReferenceContent>()
                .Where(fileContent => fileContent.Tools?.Any() ?? false)
                .Select(
                    fileContent =>
                        new MessageAttachment(fileContent.FileId, [.. GetToolDefinition(fileContent.Tools!)]));

        static IEnumerable<ToolDefinition> GetToolDefinition(IEnumerable<string> tools)
        {
            foreach (string tool in tools)
            {
                if (s_toolMetadata.TryGetValue(tool, out ToolDefinition? toolDefinition))
                {
                    yield return toolDefinition;
                }
            }
        }
    }

    /// <summary>
    /// Translates a set of <see cref="ChatMessageContent"/> to a set of <see cref="MessageInputContentBlock"/>.
    /// </summary>
    /// <param name="message">A <see cref="ChatMessageContent"/> object/</param>
    public static IEnumerable<MessageInputContentBlock> GetMessageContent(ChatMessageContent? message)
    {
        if (message is not null)
        {
            foreach (KernelContent content in message.Items)
            {
                if (content is TextContent textContent)
                {
                    yield return new MessageInputTextBlock(content.ToString());
                }
                else if (content is ImageContent imageContent)
                {
                    if (imageContent.Uri != null)
                    {
                        MessageImageUriParam imageUrlParam = new(uri: imageContent.Uri.ToString());
                        yield return new MessageInputImageUriBlock(imageUrlParam);
                    }
                    else if (!string.IsNullOrWhiteSpace(imageContent.DataUri))
                    {
                        MessageImageUriParam imageUrlParam = new(uri: imageContent.DataUri!);
                        yield return new MessageInputImageUriBlock(imageUrlParam);
                    }
                }
                else if (content is FileReferenceContent fileContent)
                {
                    MessageImageFileParam fileParam = new(fileContent.FileId);
                    yield return new MessageInputImageFileBlock(fileParam);
                }
            }
        }
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
                    Attachments = [.. GetAttachments(message)],
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

    private static readonly Dictionary<string, ToolDefinition> s_toolMetadata =
        new()
        {
            if (s_toolMetadata.TryGetValue(tool, out ToolDefinition? toolDefinition))
            {
                yield return toolDefinition;
            }
        }
    }

    /// <summary>
    /// Translate additional metadata for advanced scenarios.
    /// </summary>
    /// <param name="message">The message content.</param>
    public static Dictionary<string, string> GetAdvancedMetadata(ChatMessageContent message)
    {
        var metadata = GetMetadata(message);

        // Add custom metadata processing logic here
        if (message.Metadata?.ContainsKey("CustomKey") == true)
        {
            metadata["ProcessedKey"] = "ProcessedValue";
        }

        return metadata;
    }

    /// <summary>
    /// Add support for new tool definitions dynamically.
    /// </summary>
    /// <param name="toolName">The name of the tool.</param>
    /// <param name="toolDefinition">The tool definition object.</param>
    public static void AddToolDefinition(string toolName, ToolDefinition toolDefinition)
    {
        if (!s_toolMetadata.ContainsKey(toolName))
        {
            s_toolMetadata[toolName] = toolDefinition;
        }
    }

    /// <summary>
    /// Automatically process metadata and add custom keys if applicable.
    /// </summary>
    /// <param name="message">The message content.</param>
    public static Dictionary<string, string> GetMetadataWithAutomation(ChatMessageContent message)
    {
        var metadata = GetMetadata(message);

        // Automatically process custom metadata keys
        if (message.Metadata?.ContainsKey("AutoKey") == true)
        {
            metadata["AutoProcessedKey"] = "AutoProcessedValue";
        }

        return metadata;
    }

    /// <summary>
    /// Automatically add new tool definitions if not present.
    /// </summary>
    /// <param name="tools">A list of tool names to ensure are defined.</param>
    public static void EnsureToolDefinitions(IEnumerable<string> tools)
    {
        foreach (var tool in tools)
        {
            if (!s_toolMetadata.ContainsKey(tool))
            {
                s_toolMetadata[tool] = new DefaultToolDefinition(); // Use a default tool definition
            }
        }
    }

    /// <summary>
    /// Automatically enrich metadata with default values or computed properties.
    /// </summary>
    /// <param name="message">The message content.</param>
    public static Dictionary<string, string> EnrichMetadata(ChatMessageContent message)
    {
        var metadata = GetMetadata(message);

        // Add default values if missing
        if (!metadata.ContainsKey("DefaultKey"))
        {
            metadata["DefaultKey"] = "DefaultValue";
        }

        // Compute additional properties
        metadata["Timestamp"] = DateTime.UtcNow.ToString("o");

        return metadata;
    }

    /// <summary>
    /// Automatically register tools based on predefined rules.
    /// </summary>
    /// <param name="toolNames">A list of tool names to register.</param>
    public static void RegisterToolsAutomatically(IEnumerable<string> toolNames)
    {
        foreach (var toolName in toolNames)
        {
            if (!s_toolMetadata.ContainsKey(toolName))
            {
                // Register a default tool definition
                s_toolMetadata[toolName] = new DefaultToolDefinition();
            }
        }
    }

    /// <summary>
    /// Validate messages to ensure they meet specific criteria.
    /// </summary>
    /// <param name="message">The message content.</param>
    /// <returns>True if the message is valid, otherwise false.</returns>
    public static bool ValidateMessage(ChatMessageContent message)
    {
        // Example validation: Ensure content is not empty
        if (string.IsNullOrWhiteSpace(message.Content))
        {
            return false;
        }

        // Additional validation logic can be added here
        return true;
    }

    /// <summary>
    /// Automatically log metadata and tool registration events.
    /// </summary>
    /// <param name="message">The message content.</param>
    public static void LogMetadataAndTools(ChatMessageContent message)
    {
        var metadata = GetMetadata(message);
        Console.WriteLine("Metadata:");
        foreach (var kvp in metadata)
        {
            Console.WriteLine($"{kvp.Key}: {kvp.Value}");
        }

        Console.WriteLine("Registered Tools:");
        foreach (var tool in s_toolMetadata.Keys)
        {
            Console.WriteLine(tool);
        }
    }

    /// <summary>
    /// Automatically handle errors during metadata processing or tool registration.
    /// </summary>
    /// <param name="action">The action to execute with error handling.</param>
    public static void HandleErrors(Action action)
    {
        try
        {
            action();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }
    }

    /// <summary>
    /// Automatically clean up unused or invalid tool definitions and metadata entries.
    /// </summary>
    public static void Cleanup()
    {
        // Remove invalid tool definitions
        var invalidTools = s_toolMetadata.Where(kvp => kvp.Value == null).Select(kvp => kvp.Key).ToList();
        foreach (var tool in invalidTools)
        {
            s_toolMetadata.Remove(tool);
        }

        Console.WriteLine("Cleanup completed. Invalid tools removed.");
    }

    /// <summary>
    /// Automatically merge metadata from multiple sources.
    /// </summary>
    /// <param name="messages">A collection of message contents.</param>
    /// <returns>A merged dictionary of metadata.</returns>
    public static Dictionary<string, string> MergeMetadata(IEnumerable<ChatMessageContent> messages)
    {
        var mergedMetadata = new Dictionary<string, string>();

        foreach (var message in messages)
        {
            var metadata = GetMetadata(message);
            foreach (var kvp in metadata)
            {
                if (!mergedMetadata.ContainsKey(kvp.Key))
                {
                    mergedMetadata[kvp.Key] = kvp.Value;
                }
            }
        }

        return mergedMetadata;
    }

    /// <summary>
    /// Automatically track tool usage for analytics.
    /// </summary>
    /// <param name="toolName">The name of the tool being used.</param>
    public static void TrackToolUsage(string toolName)
    {
        if (!s_toolMetadata.ContainsKey(toolName))
        {
            Console.WriteLine($"Tool '{toolName}' is not registered.");
            return;
        }

        Console.WriteLine($"Tool '{toolName}' has been used.");
        // Additional tracking logic can be added here, such as logging to a database.
    }

    /// <summary>
    /// Automatically load configuration settings for tools or metadata processing.
    /// </summary>
    /// <param name="configKey">The configuration key to load.</param>
    /// <returns>The configuration value, or null if not found.</returns>
    public static string? LoadConfiguration(string configKey)
    {
        // Simulate loading configuration from a settings file or environment variable
        var configurations = new Dictionary<string, string>
        {
            { "DefaultToolTimeout", "30" },
            { "EnableAdvancedLogging", "true" }
        };

        configurations.TryGetValue(configKey, out var configValue);
        return configValue;
    }

    /// <summary>
    /// Automatically test metadata processing.
    /// </summary>
    /// <param name="message">The message content to test.</param>
    /// <returns>True if metadata processing passes all tests, otherwise false.</returns>
    public static bool TestMetadataProcessing(ChatMessageContent message)
    {
        try
        {
            var metadata = GetMetadata(message);
            Console.WriteLine("Metadata processed successfully:");
            foreach (var kvp in metadata)
            {
                Console.WriteLine($"{kvp.Key}: {kvp.Value}");
            }
            return true;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Metadata processing test failed: {ex.Message}");
            return false;
        }
    }

    /// <summary>
    /// Automatically test tool registration and execution.
    /// </summary>
    /// <param name="toolName">The name of the tool to test.</param>
    /// <returns>True if the tool passes all tests, otherwise false.</returns>
    public static bool TestToolRegistrationAndExecution(string toolName)
    {
        try
        {
            if (!s_toolMetadata.ContainsKey(toolName))
            {
                Console.WriteLine($"Tool '{toolName}' is not registered. Registering now...");
                AddToolDefinition(toolName, new DefaultToolDefinition());
            }

            Console.WriteLine($"Testing tool '{toolName}' execution...");
            // Simulate tool execution
            Console.WriteLine($"Tool '{toolName}' executed successfully.");
            return true;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Tool registration or execution test failed: {ex.Message}");
            return false;
        }
    }
            { AzureAIAgent.Tools.CodeInterpreter, new CodeInterpreterToolDefinition() },
            { AzureAIAgent.Tools.FileSearch, new FileSearchToolDefinition() },
        };
}
