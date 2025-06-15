// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel.Agents.Abstractions;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Contents;

namespace Microsoft.SemanticKernel.Connectors.Ollama.AgentMode;

/// <summary>
/// Agent implementation that uses an Ollama model to run locally
/// </summary>
public sealed class OllamaAgent : KernelAgent
{
    private readonly OllamaAgentConfig _config;
    private readonly IChatCompletionService _chatService;

    /// <summary>
    /// Initializes a new instance of the <see cref="OllamaAgent"/> class.
    /// </summary>
    /// <param name="id">The identifier for the agent.</param>
    /// <param name="chatService">The chat service to use for the agent.</param>
    /// <param name="config">Configuration for the agent.</param>
    /// <param name="kernel">Kernel to use for the agent.</param>
    /// <param name="logger">The logger to use.</param>
    public OllamaAgent(
        string id,
        IChatCompletionService chatService,
        OllamaAgentConfig config,
        Kernel? kernel = null,
        ILoggerFactory? logger = null)
        : base(id, kernel, logger)
    {
        this._chatService = chatService;
        this._config = config;
    }

    /// <inheritdoc/>
    public override async Task<AgentThread> CreateThreadAsync(CancellationToken cancellationToken = default)
    {
        return await Task.FromResult(new OllamaAgentThread()).ConfigureAwait(false);
    }

    /// <inheritdoc/>
    public override async IAsyncEnumerable<AgentResponseItem<ChatMessageContent>> InvokeAsync(
        ICollection<ChatMessageContent> messages,
        AgentThread? thread = null,
        object? options = null,
        CancellationToken cancellationToken = default)
    {
        thread ??= await this.CreateThreadAsync(cancellationToken).ConfigureAwait(false);
        var localThread = thread as OllamaAgentThread ?? throw new InvalidOperationException("Thread must be an OllamaAgentThread");

        // Apply the agent's instructions to the system message
        var systemMessage = messages.FirstOrDefault(m => m.Role == AuthorRole.System);
        var effectiveSystemMessage = systemMessage;

        if (systemMessage == null)
        {
            effectiveSystemMessage = new ChatMessageContent(
                AuthorRole.System,
                this._config.Instructions ?? "You are a helpful AI assistant.");

            var messageList = new List<ChatMessageContent>(messages)
            {
                effectiveSystemMessage
            };
            messages = messageList;
        }
        else if (!string.IsNullOrEmpty(this._config.Instructions))
        {
            effectiveSystemMessage = new ChatMessageContent(
                AuthorRole.System,
                $"{systemMessage.Content}\n\n{this._config.Instructions}");

            var messageList = new List<ChatMessageContent>(messages);
            int index = messageList.IndexOf(systemMessage);
            messageList[index] = effectiveSystemMessage;
            messages = messageList;
        }

        // Create chat history from messages
        var chatHistory = new ChatHistory(messages);

        // Use the chat service to get a response
        var chatSettings = this._config.ChatSettings ?? new ChatCompletionOptions { MaxTokens = 2000 };

        // Get the response from the local model
        var chatResults = await this._chatService.GetChatCompletionsAsync(
            chatHistory,
            chatSettings,
            cancellationToken).ConfigureAwait(false);

        // Update the thread with the messages
        localThread.AddMessages(messages);
        foreach (var result in chatResults)
        {
            localThread.AddMessage(result);
            yield return new AgentResponseItem<ChatMessageContent>(result, localThread);
        }
    }
}
