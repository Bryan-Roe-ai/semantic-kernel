// Copyright (c) Microsoft. All rights reserved.
using System;
using System.Collections.Generic;
using System.Diagnostics.CodeAnalysis;
using System.Text.Json.Serialization;

namespace Microsoft.SemanticKernel.Agents.OpenAI;

/// <summary>
/// Defines per-invocation execution options that override the assistant definition.
/// </summary>
/// <remarks>
/// This class is not applicable to <see cref="AgentChat"/> usage.
/// </remarks>
[Experimental("SKEXP0110")]
[Obsolete("Use RunCreationOptions to specify assistant invocation behavior.")]
public sealed class OpenAIAssistantInvocationOptions
{
    /// <summary>
    /// Gets the AI model targeted by the agent.
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public string? ModelName { get; init; }

    /// <summary>

    /// Appends additional instructions.

    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public string? AdditionalInstructions { get; init; }

    /// <summary>

    /// Additional messages to add to the thread.

    /// Gets additional messages to add to the thread.

    /// </summary>
    /// <remarks>
    /// This property only supports messages with <see href="https://platform.openai.com/docs/api-reference/runs/createRun#runs-createrun-additional_messages">role = User or Assistant</see>.
    /// </remarks>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public IReadOnlyList<ChatMessageContent>? AdditionalMessages { get; init; }

    /// <summary>

    /// Set if code_interpreter tool is enabled.

    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingDefault)]
    public bool EnableCodeInterpreter { get; init; }

    /// <summary>
    /// Gets a value that indicates if the file_search tool is enabled.
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingDefault)]
    public bool EnableFileSearch { get; init; }

    /// <summary>
    /// Gets a value that indicates if the JSON response format is enabled.
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public bool? EnableJsonResponse { get; init; }

    /// <summary>
    /// Gets the maximum number of completion tokens that can be used over the course of the run.
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public int? MaxCompletionTokens { get; init; }

    /// <summary>
    /// Gets the maximum number of prompt tokens that can be used over the course of the run.
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public int? MaxPromptTokens { get; init; }

    /// <summary>
    /// Gets a value that indicates whether parallel function calling is enabled during tool use.
    /// </summary>
    /// <value>
    /// <see langword="true"/> if parallel function calling is enabled during tool use; otherwise, <see langword="false"/>. The default is <see langword="true"/>.
    /// </value>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public bool? ParallelToolCallsEnabled { get; init; }

    /// <summary>
    /// Gets the number of recent messages that the thread will be truncated to.
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public int? TruncationMessageCount { get; init; }

    /// <summary>
    /// Gets the sampling temperature to use, between 0 and 2.
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public float? Temperature { get; init; }

    /// <summary>
    /// Gets the probability mass of tokens whose results are considered in nucleus sampling.
    /// </summary>
    /// <remarks>
    /// It's recommended to set this property or <see cref="Temperature"/>, but not both.
    ///
    /// Nucleus sampling is an alternative to sampling with temperature where the model
    /// considers the results of the tokens with <see cref="TopP"/> probability mass.
    /// For example, 0.1 means only the tokens comprising the top 10% probability mass are considered.
    /// </remarks>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public float? TopP { get; init; }

    /// <summary>
    /// Gets a set of up to 16 key/value pairs that can be attached to an agent, used for
    /// storing additional information about that object in a structured format.
    /// </summary>
    /// <remarks>
    /// Keys can be up to 64 characters in length, and values can be up to 512 characters in length.
    /// </remarks>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public IReadOnlyDictionary<string, string>? Metadata { get; init; }
}
