// Copyright (c) Microsoft. All rights reserved.

using Microsoft.SemanticKernel.ChatCompletion;

namespace Microsoft.SemanticKernel.Connectors.Ollama.AgentMode;

/// <summary>
/// Configuration options for <see cref="OllamaAgent"/>.
/// </summary>
public class OllamaAgentConfig
{
    /// <summary>
    /// Gets or sets the instructions for the agent.
    /// </summary>
    public string? Instructions { get; set; }

    /// <summary>
    /// Gets or sets the chat settings for the agent.
    /// </summary>
    public ChatCompletionOptions? ChatSettings { get; set; }

    /// <summary>
    /// Gets or sets the Ollama model to use.
    /// </summary>
    public string ModelName { get; set; } = "llama2";
}
