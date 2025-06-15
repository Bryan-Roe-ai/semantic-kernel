// Copyright (c) Microsoft. All rights reserved.

using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.Ollama.ChatCompletion;

namespace Microsoft.SemanticKernel.Connectors.Ollama.AgentMode;

/// <summary>
/// Extension methods for adding Ollama agent capabilities to a Semantic Kernel instance.
/// </summary>
public static class OllamaAgentExtensions
{
    /// <summary>
    /// Creates an Ollama agent with the specified configuration.
    /// </summary>
    /// <param name="kernel">The kernel to use with the agent.</param>
    /// <param name="config">The agent configuration.</param>
    /// <param name="id">Optional ID for the agent. If not provided, a new GUID will be used.</param>
    /// <param name="endpoint">The Ollama API endpoint. Defaults to http://localhost:11434.</param>
    /// <returns>An Ollama agent instance.</returns>
    public static OllamaAgent CreateOllamaAgent(
        this Kernel kernel,
        OllamaAgentConfig config,
        string? id = null,
        string endpoint = "http://localhost:11434")
    {
        var chatService = new OllamaChatCompletionService(
            modelId: config.ModelName,
            endpoint: endpoint);

        return new OllamaAgent(
            id: id ?? Guid.NewGuid().ToString(),
            chatService: chatService,
            config: config,
            kernel: kernel,
            logger: kernel.Services.GetService<ILoggerFactory>());
    }

    /// <summary>
    /// Adds an Ollama chat completion service to the service collection.
    /// </summary>
    /// <param name="services">The service collection.</param>
    /// <param name="modelId">The model ID to use.</param>
    /// <param name="endpoint">The Ollama API endpoint. Defaults to http://localhost:11434.</param>
    /// <returns>The updated service collection.</returns>
    public static IServiceCollection AddOllamaChatCompletion(
        this IServiceCollection services,
        string modelId = "llama2",
        string endpoint = "http://localhost:11434")
    {
        return services.AddKeyedSingleton<IChatCompletionService>(
            modelId,
            (sp, _) => new OllamaChatCompletionService(modelId, endpoint));
    }
}
