<<<<<<< HEAD
﻿// Copyright (c) Microsoft. All rights reserved.
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace Microsoft.SemanticKernel.Agents.AzureAI;

/// <summary>
<<<<<<< HEAD
/// Defines per invocation execution options that override the assistant definition.
/// </summary>
/// <remarks>
/// Not applicable to <see cref="AgentChat"/> usage.
=======
/// Defines per-invocation execution options that override the assistant definition.
/// </summary>
/// <remarks>
/// This class is not applicable to <see cref="AgentChat"/> usage.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
/// </remarks>
public sealed class AzureAIInvocationOptions
{
    /// <summary>
<<<<<<< HEAD
    /// Override the AI model targeted by the agent.
=======
    /// Gets the AI model targeted by the agent.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public string? ModelName { get; init; }

    /// <summary>
<<<<<<< HEAD
    /// Appends additional instructions.
=======
    /// Gets the override instructions.
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public string? OverrideInstructions { get; init; }

    /// <summary>
    /// Gets the additional instructions.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public string? AdditionalInstructions { get; init; }

    /// <summary>
<<<<<<< HEAD
    /// Additional messages to add to the thread.
    /// </summary>
    /// <remarks>
    /// Only supports messages with role = User or Assistant:
    /// https://platform.openai.com/docs/api-reference/runs/createRun#runs-createrun-additional_messages
=======
    /// Gets the additional messages to add to the thread.
    /// </summary>
    /// <remarks>
    /// Only supports messages with <see href="https://platform.openai.com/docs/api-reference/runs/createRun#runs-createrun-additional_messages">role = User or Assistant</see>.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </remarks>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public IReadOnlyList<ChatMessageContent>? AdditionalMessages { get; init; }

    /// <summary>
<<<<<<< HEAD
    /// Set if code_interpreter tool is enabled.
=======
    /// Gets a value that indicates whether the code_interpreter tool is enabled.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingDefault)]
    public bool EnableCodeInterpreter { get; init; }

    /// <summary>
<<<<<<< HEAD
    /// Set if file_search tool is enabled.
=======
    /// Gets a value that indicates whether the file_search tool is enabled.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingDefault)]
    public bool EnableFileSearch { get; init; }

    /// <summary>
<<<<<<< HEAD
    /// Set if json response-format is enabled.
=======
    /// Gets a value that indicates whether the JSON response format is enabled.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public bool? EnableJsonResponse { get; init; }

    /// <summary>
<<<<<<< HEAD
    /// The maximum number of completion tokens that may be used over the course of the run.
=======
    /// Gets the maximum number of completion tokens that can be used over the course of the run.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public int? MaxCompletionTokens { get; init; }

    /// <summary>
<<<<<<< HEAD
    /// The maximum number of prompt tokens that may be used over the course of the run.
=======
    /// Gets the maximum number of prompt tokens that can be used over the course of the run.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public int? MaxPromptTokens { get; init; }

    /// <summary>
<<<<<<< HEAD
    /// Enables parallel function calling during tool use.  Enabled by default.
    /// Use this property to disable.
    /// </summary>
=======
    /// Gets a value that indicates whether the parallel function calling is enabled during tool use.
    /// </summary>
    /// <value>
    /// <see langword="true"/> if parallel function calling is enabled during tool use; otherwise, <see langword="false"/>. The default is <see langword="true"/>.
    /// </value>
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public bool? ParallelToolCallsEnabled { get; init; }

    /// <summary>
<<<<<<< HEAD
    /// When set, the thread will be truncated to the N most recent messages in the thread.
=======
    /// Gets the number of recent messages that the thread will be truncated to.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public int? TruncationMessageCount { get; init; }

    /// <summary>
<<<<<<< HEAD
    /// The sampling temperature to use, between 0 and 2.
=======
    /// Gets the sampling temperature to use, between 0 and 2.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public float? Temperature { get; init; }

    /// <summary>
<<<<<<< HEAD
    /// An alternative to sampling with temperature, called nucleus sampling, where the model
    /// considers the results of the tokens with top_p probability mass.
    /// So 0.1 means only the tokens comprising the top 10% probability mass are considered.
    /// </summary>
    /// <remarks>
    /// Recommended to set this or temperature but not both.
=======
    /// Gets the probability mass of tokens whose results are considered in nucleus sampling.
    /// </summary>
    /// <remarks>
    /// It's recommended to set this property or <see cref="Temperature"/>, but not both.
    ///
    /// Nucleus sampling is an alternative to sampling with temperature where the model
    /// considers the results of the tokens with <see cref="TopP"/> probability mass.
    /// For example, 0.1 means only the tokens comprising the top 10% probability mass are considered.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </remarks>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public float? TopP { get; init; }

    /// <summary>
<<<<<<< HEAD
    /// A set of up to 16 key/value pairs that can be attached to an agent, used for
    /// storing additional information about that object in a structured format.Keys
    /// may be up to 64 characters in length and values may be up to 512 characters in length.
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public IReadOnlyDictionary<string, string>? Metadata { get; init; }

    /// <summary>
    /// The endpoint for Azure Cognitive Services.
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public string? AzureCognitiveServicesEndpoint { get; init; }

    /// <summary>
    /// The API key for Azure Cognitive Services.
    /// </summary>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public string? AzureCognitiveServicesApiKey { get; init; }
=======
    /// Gets a set of up to 16 key/value pairs that can be attached to an agent, used for
    /// storing additional information about that object in a structured format.
    /// </summary>
    /// <remarks>
    /// Keys can be up to 64 characters in length, and values can be up to 512 characters in length.
    /// </remarks>
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public IReadOnlyDictionary<string, string>? Metadata { get; init; }
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
}
