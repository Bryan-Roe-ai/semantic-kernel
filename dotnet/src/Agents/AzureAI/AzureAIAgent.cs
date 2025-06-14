// Copyright (c) Microsoft. All rights reserved.
using System;
// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
using Azure.AI.Agents.Persistent;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel.Agents.AzureAI.Internal;
using Microsoft.SemanticKernel.Agents.Extensions;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Diagnostics;
using AAIP = Azure.AI.Projects;

namespace Microsoft.SemanticKernel.Agents.AzureAI;

/// <summary>
/// A <see cref="KernelAgent"/> specialization based on Open AI Assistant / GPT.
/// </summary>
public sealed class AzureAIAgent : KernelAgent
{
    /// <summary>
    /// Metadata key that identifies code-interpreter content.
    /// </summary>
    public const string CodeInterpreterMetadataKey = "code"; // %%%% RE-EVALUATE

    private readonly AzureAIClientProvider _provider;
    private readonly AzureAIP.AgentsClient _client;
    private readonly string[] _channelKeys;

    /// <summary>
    /// The assistant definition.
    /// </summary>
    public AzureAIP.Agent Definition { get; private init; }

    /// <summary>
    /// Set when the assistant has been deleted via <see cref="DeleteAsync(CancellationToken)"/>.
    /// An assistant removed by other means will result in an exception when invoked.
    /// </summary>
    public bool IsDeleted { get; private set; }

    /// <summary>
    /// Defines polling behavior for run processing
    /// </summary>
    public RunPollingOptions PollingOptions { get; } = new();

    /// <summary>
    /// Create a new assistant thread.
    /// </summary>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>The thread identifier</returns>
    public Task<string> CreateThreadAsync(CancellationToken cancellationToken = default) // %%% STATIC
    {
        return AgentThreadActions.CreateThreadAsync(this._client, options: null, cancellationToken);
    }

    /// <summary>
    /// Create a new assistant thread.
    /// </summary>
    /// <param name="options">The options for creating the thread</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>The thread identifier</returns>
    public Task<string> CreateThreadAsync(AzureAIThreadCreationOptions? options, CancellationToken cancellationToken = default) // %%% STATIC
    {
        return AgentThreadActions.CreateThreadAsync(this._client, options, cancellationToken);
    }

    /// <summary>
    /// Create a new assistant thread.
    /// </summary>
    /// <param name="threadId">The thread identifier</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>The thread identifier</returns>
    public async Task<bool> DeleteThreadAsync(
        string threadId,
        CancellationToken cancellationToken = default)
    {
        // Validate input
        Verify.NotNullOrWhiteSpace(threadId, nameof(threadId));

        bool isDeleted = await this._client.DeleteThreadAsync(threadId, cancellationToken).ConfigureAwait(false);

        return isDeleted;
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="AzureAIAgent"/> class.
    /// </summary>
    /// <param name="model">The agent model definition.</param>
    /// <param name="client">An <see cref="PersistentAgentsClient"/> instance.</param>
    /// <param name="plugins">Optional collection of plugins to add to the kernel.</param>
    /// <param name="templateFactory">An optional factory to produce the <see cref="IPromptTemplate"/> for the agent.</param>
    /// <param name="templateFormat">The format of the prompt template used when "templateFactory" parameter is supplied.</param>
    public AzureAIAgent(
        PersistentAgent model,
        PersistentAgentsClient client,
        IEnumerable<KernelPlugin>? plugins = null,
        IPromptTemplateFactory? templateFactory = null,
        string? templateFormat = null)
    {
        this.Client = client;
        this.Definition = model;
        this.Description = this.Definition.Description;
        this.Id = this.Definition.Id;
        this.Name = this.Definition.Name;
        this.Instructions = this.Definition.Instructions;

        if (templateFactory != null)
        {
            Verify.NotNullOrWhiteSpace(templateFormat);

            PromptTemplateConfig templateConfig = new(this.Instructions)
            {
                TemplateFormat = templateFormat
            };

            this.Template = templateFactory.Create(templateConfig);
        }

        if (plugins != null)
        {
            this.Kernel.Plugins.AddRange(plugins);
        }
    }

    /// <summary>
    /// The associated client.
    /// The Agent SDK client.
    /// </summary>
    public PersistentAgentsClient Client { get; }

    /// <summary>
    /// Adds a message to the specified thread.
    /// </summary>
    /// <param name="threadId">The thread identifier</param>
    /// <param name="message">A non-system message with which to append to the conversation.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <remarks>
    /// Only supports messages with role = User or Assistant:
    /// https://platform.openai.com/docs/api-reference/runs/createRun#runs-createrun-additional_messages
    /// </remarks>
    public Task AddChatMessageAsync(string threadId, ChatMessageContent message, CancellationToken cancellationToken = default)
    {
        this.ThrowIfDeleted();

        return AgentThreadActions.CreateMessageAsync(this._client, threadId, message, cancellationToken);
    }

    /// <summary>
    /// Gets messages for a specified thread.
    /// </summary>
    /// <param name="threadId">The thread identifier</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of messages.</returns>
    public IAsyncEnumerable<ChatMessageContent> GetThreadMessagesAsync(string threadId, CancellationToken cancellationToken = default)
    {
        this.ThrowIfDeleted();

        return AgentThreadActions.GetMessagesAsync(this._client, threadId, cancellationToken);
    }

    /// <summary>
    /// Delete the assistant definition.
    /// </summary>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>True if assistant definition has been deleted</returns>
    /// <remarks>
    /// Assistant based agent will not be useable after deletion.
    /// </remarks>
    public async Task<bool> DeleteAsync(CancellationToken cancellationToken = default)
    {
        if (!this.IsDeleted)
        {
            bool isDeleted = await this._client.DeleteAgentAsync(this.Id, cancellationToken).ConfigureAwait(false);
            this.IsDeleted = isDeleted;
        }

        return this.IsDeleted;
    }

    /// <summary>
    /// Invoke the assistant on the specified thread.
    /// </summary>
    /// <param name="threadId">The thread identifier</param>
    /// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use by the agent.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of response messages.</returns>
    /// <remarks>
    /// The `arguments` parameter is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>
    public IAsyncEnumerable<ChatMessageContent> InvokeAsync(
        string threadId,
        KernelArguments? arguments = null,
        Kernel? kernel = null,
        CancellationToken cancellationToken = default)
    {
        return this.InvokeAsync(threadId, options: null, arguments, kernel, cancellationToken);
    /// <inheritdoc/>
    public override IAsyncEnumerable<AgentResponseItem<ChatMessageContent>> InvokeAsync(
        ICollection<ChatMessageContent> messages,
        AgentThread? thread = null,
        AgentInvokeOptions? options = null,
        CancellationToken cancellationToken = default)
    {
        return this.InvokeAsync(
            messages,
            thread,
            options is null ?
                null :
                options is AzureAIAgentInvokeOptions azureAIAgentInvokeOptions ? azureAIAgentInvokeOptions : new AzureAIAgentInvokeOptions(options),
            cancellationToken);
    }

    /// <summary>
    /// Invoke the assistant on the specified thread.
    /// </summary>
    /// <param name="threadId">The thread identifier</param>
    /// <param name="options">Optional invocation options</param>
    /// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use by the agent.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of response messages.</returns>
    /// <remarks>
    /// The `arguments` parameter is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>
    public async IAsyncEnumerable<ChatMessageContent> InvokeAsync(
        string threadId,
        AzureAIInvocationOptions? options,
        KernelArguments? arguments = null,
        Kernel? kernel = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        this.ThrowIfDeleted();

        kernel = (options?.Kernel ?? kernel ?? this.Kernel).Clone();
        arguments = this.MergeArguments(arguments);

        // Get the context contributions from the AIContextProviders if available
        AzureAIAgentInvocationOptions? extensionsContextOptions = null;

        if (options != null && options is AzureAIAgentInvokeOptions agentOptions &&
            agentOptions.Thread != null && agentOptions.Thread is AzureAIAgentThread azureAIAgentThread)
        {
#pragma warning disable SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
            var providersContext = await azureAIAgentThread.AIContextProviders.ModelInvokingAsync(null, cancellationToken).ConfigureAwait(false);
            kernel.Plugins.AddFromAIContext(providersContext, "Tools");
#pragma warning restore SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed

            var mergedAdditionalInstructions = MergeAdditionalInstructions(options?.AdditionalInstructions, providersContext.Instructions);
            extensionsContextOptions = options is null ?
                new AzureAIAgentInvokeOptions() { AdditionalInstructions = mergedAdditionalInstructions } :
                new AzureAIAgentInvokeOptions(options) { AdditionalInstructions = mergedAdditionalInstructions };
        }
        AzureAIAgentThread azureAIAgentThread = await this.EnsureThreadExistsWithMessagesAsync(
            messages,
            thread,
            () => new AzureAIAgentThread(this.Client),
            cancellationToken).ConfigureAwait(false);

        Kernel kernel = (options?.Kernel ?? this.Kernel).Clone();

        // Get the context contributions from the AIContextProviders.
#pragma warning disable SKEXP0110, SKEXP0130 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
        AIContext providersContext = await azureAIAgentThread.AIContextProviders.ModelInvokingAsync(messages, cancellationToken).ConfigureAwait(false);
        kernel.Plugins.AddFromAIContext(providersContext, "Tools");
#pragma warning restore SKEXP0110, SKEXP0130 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.

        string mergedAdditionalInstructions = FormatAdditionalInstructions(providersContext, options);
        var extensionsContextOptions = options is null ?
            new AzureAIAgentInvokeOptions() { AdditionalInstructions = mergedAdditionalInstructions } :
            new AzureAIAgentInvokeOptions(options) { AdditionalInstructions = mergedAdditionalInstructions };

        var invokeResults = ActivityExtensions.RunWithActivityAsync(
            () => ModelDiagnostics.StartAgentInvocationActivity(this.Id, this.GetDisplayName(), this.Description),
            () => InternalInvokeAsync(),
            cancellationToken);

        await foreach ((bool isVisible, ChatMessageContent message) in AgentThreadActions.InvokeAsync(
            this,
            this._client,
            threadId,
            extensionsContextOptions ?? options,
            this.Logger,
            kernel,
            arguments,
            cancellationToken).ConfigureAwait(false))
        {
            // The thread and the caller should be notified of all messages regardless of visibility.
            await this.NotifyThreadOfNewMessage(azureAIAgentThread, message, cancellationToken).ConfigureAwait(false);
            if (options?.OnIntermediateMessage is not null)
            {
                await options.OnIntermediateMessage(message).ConfigureAwait(false);
            }

            if (isVisible)
            {
                yield return message;
            }
        }
    }

    /// <summary>
    /// Invokes the assistant on the specified thread.
    /// </summary>
    /// <param name="threadId">The thread identifier.</param>
    /// <param name="options">Optional invocation options.</param>
    /// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use by the agent.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of response messages.</returns>
    /// <remarks>
    /// The `arguments` parameter is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>
    public async IAsyncEnumerable<ChatMessageContent> InvokeAsync(
        string threadId,
        AzureAIInvocationOptions? options,
        KernelArguments? arguments = null,
        Kernel? kernel = null,
    /// <inheritdoc/>
    public override IAsyncEnumerable<AgentResponseItem<StreamingChatMessageContent>> InvokeStreamingAsync(
        ICollection<ChatMessageContent> messages,
        AgentThread? thread = null,
        AgentInvokeOptions? options = null,
        CancellationToken cancellationToken = default)
    {
        return this.InvokeStreamingAsync(
            messages,
            thread,
            options is null ?
                null :
                options is AzureAIAgentInvokeOptions azureAIAgentInvokeOptions ? azureAIAgentInvokeOptions : new AzureAIAgentInvokeOptions(options),
            cancellationToken);
    }

    /// <summary>
    /// Invoke the agent with the provided message and arguments.
    /// </summary>
    /// <param name="messages">The messages to pass to the agent.</param>
    /// <param name="thread">The conversation thread to continue with this invocation. If not provided, creates a new thread.</param>
    /// <param name="options">Optional parameters for agent invocation.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>An async list of response items that each contain a <see cref="StreamingChatMessageContent"/> and an <see cref="AgentThread"/>.</returns>
    /// <remarks>
    /// To continue this thread in the future, use an <see cref="AgentThread"/> returned in one of the response items.
    /// </remarks>
    public async IAsyncEnumerable<AgentResponseItem<StreamingChatMessageContent>> InvokeStreamingAsync(
        ICollection<ChatMessageContent> messages,
        AgentThread? thread = null,
        AzureAIAgentInvokeOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        this.ThrowIfDeleted();

        kernel = (options?.Kernel ?? kernel ?? this.Kernel).Clone();
        arguments = this.MergeArguments(arguments);
        AzureAIAgentThread azureAIAgentThread = await this.EnsureThreadExistsWithMessagesAsync(
            messages,
            thread,
            () => new AzureAIAgentThread(this.Client),
            cancellationToken).ConfigureAwait(false);

        // Get the context contributions from the AIContextProviders if available
        AzureAIAgentInvocationOptions? extensionsContextOptions = null;

        if (options != null && options is AzureAIAgentInvokeOptions agentOptions &&
            agentOptions.Thread != null && agentOptions.Thread is AzureAIAgentThread azureAIAgentThread)
        // Get the context contributions from the AIContextProviders.
#pragma warning disable SKEXP0110, SKEXP0130 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
        AIContext providersContext = await azureAIAgentThread.AIContextProviders.ModelInvokingAsync(messages, cancellationToken).ConfigureAwait(false);
        kernel.Plugins.AddFromAIContext(providersContext, "Tools");
#pragma warning restore SKEXP0110, SKEXP0130 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.

        string mergedAdditionalInstructions = FormatAdditionalInstructions(providersContext, options);
        var extensionsContextOptions = options is null ?
            new AzureAIAgentInvokeOptions() { AdditionalInstructions = mergedAdditionalInstructions } :
            new AzureAIAgentInvokeOptions(options) { AdditionalInstructions = mergedAdditionalInstructions };

        // Invoke the Agent with the thread that we already added our message to, and with
        // a chat history to receive complete messages.
        ChatHistory newMessagesReceiver = [];
        var invokeResults = ActivityExtensions.RunWithActivityAsync(
            () => ModelDiagnostics.StartAgentInvocationActivity(this.Id, this.GetDisplayName(), this.Description),
            () => AgentThreadActions.InvokeStreamingAsync(
                this,
                this.Client,
                azureAIAgentThread.Id!,
                newMessagesReceiver,
                extensionsContextOptions.ToAzureAIInvocationOptions(),
                this.Logger,
                kernel,
                options?.KernelArguments,
                cancellationToken),
            cancellationToken);

        // Return the chunks to the caller.
        await foreach (var result in invokeResults.ConfigureAwait(false))
        {
#pragma warning disable SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
            var providersContext = await azureAIAgentThread.AIContextProviders.ModelInvokingAsync(null, cancellationToken).ConfigureAwait(false);
            kernel.Plugins.AddFromAIContext(providersContext, "Tools");
#pragma warning restore SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed

            var mergedAdditionalInstructions = MergeAdditionalInstructions(options?.AdditionalInstructions, providersContext.Instructions);
            extensionsContextOptions = options is null ?
                new AzureAIAgentInvokeOptions() { AdditionalInstructions = mergedAdditionalInstructions } :
                new AzureAIAgentInvokeOptions(options) { AdditionalInstructions = mergedAdditionalInstructions };
        }

        await foreach ((bool isVisible, ChatMessageContent message) in AgentThreadActions.InvokeAsync(
            this,
            this._client,
            threadId,
            extensionsContextOptions ?? options,
            this.Logger,
            kernel,
            arguments,
            cancellationToken).ConfigureAwait(false))
        {
            if (isVisible)
            {
                yield return message;
            }
        }
    }

    /// <summary>
    /// Invoke the assistant on the specified thread with streaming response.
    /// </summary>
    /// <param name="threadId">The thread identifier</param>
    /// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use by the agent.</param>
    /// <param name="messages">Optional receiver of the completed messages generated</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of messages.</returns>
    /// <remarks>
    /// The `arguments` parameter is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>
    public async IAsyncEnumerable<StreamingChatMessageContent> InvokeStreamingAsync(
        string threadId,
        KernelArguments? arguments = null,
        Kernel? kernel = null,
        ChatHistory? messages = null,
        CancellationToken cancellationToken = default)
    {
        return this.InvokeStreamingAsync(threadId, options: null, arguments, kernel, messages, cancellationToken);
    }

    /// <summary>
    /// Invoke the assistant on the specified thread with streaming response.
    /// </summary>
    /// <param name="threadId">The thread identifier</param>
    /// <param name="options">Optional invocation options</param>
    /// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use by the agent.</param>
    /// <param name="messages">Optional receiver of the completed messages generated</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of messages.</returns>
    /// <remarks>
    /// The `arguments` parameter is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>
    public async IAsyncEnumerable<StreamingChatMessageContent> InvokeStreamingAsync(
        string threadId,
        AzureAIInvocationOptions? options,
        KernelArguments? arguments = null,
        Kernel? kernel = null,
        ChatHistory? messages = null,
        CancellationToken cancellationToken = default)
    {
        this.ThrowIfDeleted();

        kernel ??= this.Kernel;
        arguments = this.MergeArguments(arguments);

        // %%% STREAMING
        //return AgentThreadActions.InvokeStreamingAsync(this, this._client, threadId, messages, options, this.Logger, kernel, arguments, cancellationToken);
        return Array.Empty<StreamingChatMessageContent>().ToAsyncEnumerable();
    }

    /// <inheritdoc/>
    protected override IEnumerable<string> GetChannelKeys()
    {
        // Distinguish from other channel types.
        yield return typeof(AzureAIChannel).FullName!;

        foreach (string key in this._channelKeys)
        {
            yield return key;
        }
    }

    /// <inheritdoc/>
    protected override async Task<AgentChannel> CreateChannelAsync(CancellationToken cancellationToken)
    {
        //this.Logger.LogAzureAIAgentCreatingChannel(nameof(CreateChannelAsync), nameof(AzureAIChannel)); // %%%

        string threadId = await AgentThreadActions.CreateThreadAsync(this._client, options: null, cancellationToken).ConfigureAwait(false);

        this.Logger.LogInformation("[{MethodName}] Created assistant thread: {ThreadId}", nameof(CreateChannelAsync), threadId);

        AzureAIChannel channel =
            new(this._client, threadId)
            {
                Logger = this.LoggerFactory.CreateLogger<AzureAIChannel>()
            };

        //this.Logger.LogAzureAIAgentCreatedChannel(nameof(CreateChannelAsync), nameof(AzureAIChannel), thread.Id); // %%%

        return channel;
    }

    internal void ThrowIfDeleted()
    {
        if (this.IsDeleted)
        {
            throw new KernelException($"Agent Failure - {nameof(AzureAIAgent)} agent is deleted: {this.Id}.");
        }
    }

    internal Task<string?> GetInstructionsAsync(Kernel kernel, KernelArguments? arguments, CancellationToken cancellationToken)
    {
        return this.FormatInstructionsAsync(kernel, arguments, cancellationToken);
    }

    /// <inheritdoc/>
    protected override async Task<AgentChannel> RestoreChannelAsync(string channelState, CancellationToken cancellationToken)
    {
        string threadId = channelState;

        //this.Logger.LogAzureAIAgentRestoringChannel(nameof(RestoreChannelAsync), nameof(AzureAIChannel), threadId);

        AzureAIP.AgentThread thread = await this._client.GetThreadAsync(threadId, cancellationToken).ConfigureAwait(false);

        //this.Logger.LogAzureAIAgentRestoredChannel(nameof(RestoreChannelAsync), nameof(AzureAIChannel), threadId);

        return new AzureAIChannel(this._client, thread.Id);
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="AzureAIAgent"/> class.
    /// </summary>
    public AzureAIAgent(
        AzureAIP.Agent model,
        AzureAIClientProvider clientProvider,
        IPromptTemplate? template = null) // %%% CONFLICTS WITH model
    {
        this._provider = clientProvider;
        this._client = clientProvider.Client.GetAgentsClient();
        this._channelKeys = [.. clientProvider.ConfigurationKeys];

        this.Definition = model;
        this.Description = this.Definition.Description;
        this.Id = this.Definition.Id;
        this.Name = this.Definition.Name;
        this.Instructions = this.Definition.Instructions;
        this.Template = template;
    }

    /// <summary>
    /// Interact with Azure Cognitive Services.
    /// </summary>
    /// <param name="input">The input data for the interaction.</param>
    /// <returns>The result of the interaction.</returns>
    public async Task<string> InteractWithAzureCognitiveServicesAsync(string input)
    {
        // Implement the logic to interact with Azure Cognitive Services here.
        // This is a placeholder implementation.
        await Task.Delay(100); // Simulate async operation
        return $"Processed input: {input}";
    }
}
