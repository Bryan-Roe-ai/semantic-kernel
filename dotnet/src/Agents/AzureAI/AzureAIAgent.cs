<<<<<<< HEAD
﻿// Copyright (c) Microsoft. All rights reserved.
using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel.Agents.AzureAI.Internal;
using Microsoft.SemanticKernel.ChatCompletion;
using AzureAIP = Azure.AI.Projects;
=======
// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
using Azure.AI.Projects;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel.Agents.AzureAI.Internal;
using Microsoft.SemanticKernel.Agents.Extensions;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Diagnostics;
using AAIP = Azure.AI.Projects;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

namespace Microsoft.SemanticKernel.Agents.AzureAI;

/// <summary>
<<<<<<< HEAD
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
=======
/// Provides a specialized <see cref="Agent"/> based on an Azure AI agent.
/// </summary>
public sealed partial class AzureAIAgent : Agent
{
    /// <summary>
    /// Provides tool definitions used when associating a file attachment to an input message:
    /// <see cref="FileReferenceContent.Tools"/>.
    /// </summary>
    public static class Tools
    {
        /// <summary>
        /// The code-interpreter tool.
        /// </summary>
        public static readonly string CodeInterpreter = "code_interpreter";

        /// <summary>
        /// The file-search tool.
        /// </summary>
        public const string FileSearch = "file_search";
    }

    /// <summary>
    /// The metadata key that identifies code-interpreter content.
    /// </summary>
    public const string CodeInterpreterMetadataKey = "code";

    /// <summary>
    /// Gets the assistant definition.
    /// </summary>
    public Azure.AI.Projects.Agent Definition { get; private init; }

    /// <summary>
    /// Gets the polling behavior for run processing.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    public RunPollingOptions PollingOptions { get; } = new();

    /// <summary>
<<<<<<< HEAD
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
=======
    /// Initializes a new instance of the <see cref="AzureAIAgent"/> class.
    /// </summary>
    /// <param name="model">The agent model definition.</param>
    /// <param name="client">An <see cref="AgentsClient"/> instance.</param>
    /// <param name="plugins">Optional collection of plugins to add to the kernel.</param>
    /// <param name="templateFactory">An optional factory to produce the <see cref="IPromptTemplate"/> for the agent.</param>
    /// <param name="templateFormat">The format of the prompt template used when "templateFactory" parameter is supplied.</param>
    public AzureAIAgent(
        Azure.AI.Projects.Agent model,
        AgentsClient client,
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
    /// </summary>
    public AgentsClient Client { get; }
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

    /// <summary>
    /// Adds a message to the specified thread.
    /// </summary>
<<<<<<< HEAD
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
=======
    /// <param name="threadId">The thread identifier.</param>
    /// <param name="message">A non-system message to append to the conversation.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <remarks>
    /// Only supports messages with <see href="https://platform.openai.com/docs/api-reference/runs/createRun#runs-createrun-additional_messages">role = User or agent</see>.
    /// </remarks>
    [Obsolete("Pass messages directly to Invoke instead. This method will be removed after May 1st 2025.")]
    public Task AddChatMessageAsync(string threadId, ChatMessageContent message, CancellationToken cancellationToken = default)
    {
        return AgentThreadActions.CreateMessageAsync(this.Client, threadId, message, cancellationToken);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <summary>
    /// Gets messages for a specified thread.
    /// </summary>
<<<<<<< HEAD
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
=======
    /// <param name="threadId">The thread identifier.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>An asynchronous enumeration of messages.</returns>
    [Obsolete("Use the AzureAIAgentThread to retrieve messages instead. This method will be removed after May 1st 2025.")]
    public IAsyncEnumerable<ChatMessageContent> GetThreadMessagesAsync(string threadId, CancellationToken cancellationToken = default)
    {
        return AgentThreadActions.GetMessagesAsync(this.Client, threadId, null, cancellationToken);
    }

    /// <summary>
    /// Invokes the assistant on the specified thread.
    /// </summary>
    /// <param name="threadId">The thread identifier.</param>
    /// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use by the agent.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>An asynchronous enumeration of response messages.</returns>
    /// <remarks>
    /// The `arguments` parameter is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>
    [Obsolete("Use InvokeAsync with AgentThread instead. This method will be removed after May 1st 2025.")]
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    public IAsyncEnumerable<ChatMessageContent> InvokeAsync(
        string threadId,
        KernelArguments? arguments = null,
        Kernel? kernel = null,
        CancellationToken cancellationToken = default)
    {
        return this.InvokeAsync(threadId, options: null, arguments, kernel, cancellationToken);
    }

<<<<<<< HEAD
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
=======
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
    /// Invoke the agent with the provided message and arguments.
    /// </summary>
    /// <param name="messages">The messages to pass to the agent.</param>
    /// <param name="thread">The conversation thread to continue with this invocation. If not provided, creates a new thread.</param>
    /// <param name="options">Optional parameters for agent invocation.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>An async list of response items that each contain a <see cref="ChatMessageContent"/> and an <see cref="AgentThread"/>.</returns>
    /// <remarks>
    /// To continue this thread in the future, use an <see cref="AgentThread"/> returned in one of the response items.
    /// </remarks>
    public async IAsyncEnumerable<AgentResponseItem<ChatMessageContent>> InvokeAsync(
        ICollection<ChatMessageContent> messages,
        AgentThread? thread = null,
        AzureAIAgentInvokeOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        Verify.NotNull(messages);

        var azureAIAgentThread = await this.EnsureThreadExistsWithMessagesAsync(
            messages,
            thread,
            () => new AzureAIAgentThread(this.Client),
            cancellationToken).ConfigureAwait(false);

        var invokeResults = ActivityExtensions.RunWithActivityAsync(
            () => ModelDiagnostics.StartAgentInvocationActivity(this.Id, this.GetDisplayName(), this.Description),
            () => InternalInvokeAsync(),
            cancellationToken);

        async IAsyncEnumerable<ChatMessageContent> InternalInvokeAsync()
        {
            await foreach ((bool isVisible, ChatMessageContent message) in AgentThreadActions.InvokeAsync(
                this,
                this.Client,
                azureAIAgentThread.Id!,
                options?.ToAzureAIInvocationOptions(),
                this.Logger,
                options?.Kernel ?? this.Kernel,
                options?.KernelArguments,
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

        // Notify the thread of new messages and return them to the caller.
        await foreach (var result in invokeResults.ConfigureAwait(false))
        {
            yield return new(result, azureAIAgentThread);
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
    /// <returns>An asynchronous enumeration of response messages.</returns>
    /// <remarks>
    /// The `arguments` parameter is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>
    [Obsolete("Use InvokeAsync with AgentThread instead. This method will be removed after May 1st 2025.")]
    public IAsyncEnumerable<ChatMessageContent> InvokeAsync(
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        string threadId,
        AzureAIInvocationOptions? options,
        KernelArguments? arguments = null,
        Kernel? kernel = null,
<<<<<<< HEAD
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        this.ThrowIfDeleted();

        kernel ??= this.Kernel;
        arguments = this.MergeArguments(arguments);

        await foreach ((bool isVisible, ChatMessageContent message) in AgentThreadActions.InvokeAsync(this, this._client, threadId, options, this.Logger, kernel, arguments, cancellationToken).ConfigureAwait(false))
        {
            if (isVisible)
            {
                yield return message;
=======
        CancellationToken cancellationToken = default)
    {
        return ActivityExtensions.RunWithActivityAsync(
            () => ModelDiagnostics.StartAgentInvocationActivity(this.Id, this.GetDisplayName(), this.Description),
            () => InternalInvokeAsync(),
            cancellationToken);

        async IAsyncEnumerable<ChatMessageContent> InternalInvokeAsync()
        {
            kernel ??= this.Kernel;
            await foreach ((bool isVisible, ChatMessageContent message) in AgentThreadActions.InvokeAsync(this, this.Client, threadId, options, this.Logger, kernel, arguments, cancellationToken).ConfigureAwait(false))
            {
                if (isVisible)
                {
                    yield return message;
                }
            }
        }
    }

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
        Verify.NotNull(messages);

        var azureAIAgentThread = await this.EnsureThreadExistsWithMessagesAsync(
            messages,
            thread,
            () => new AzureAIAgentThread(this.Client),
            cancellationToken).ConfigureAwait(false);

#pragma warning disable CS0618 // Type or member is obsolete
        // Invoke the Agent with the thread that we already added our message to.
        var newMessagesReceiver = new ChatHistory();
        var invokeResults = this.InvokeStreamingAsync(
            azureAIAgentThread.Id!,
            options?.ToAzureAIInvocationOptions(),
            options?.KernelArguments,
            options?.Kernel ?? this.Kernel,
            newMessagesReceiver,
            cancellationToken);
#pragma warning restore CS0618 // Type or member is obsolete

        // Return the chunks to the caller.
        await foreach (var result in invokeResults.ConfigureAwait(false))
        {
            yield return new(result, azureAIAgentThread);
        }

        // Notify the thread of any new messages that were assembled from the streaming response.
        foreach (var newMessage in newMessagesReceiver)
        {
            await this.NotifyThreadOfNewMessage(azureAIAgentThread, newMessage, cancellationToken).ConfigureAwait(false);

            if (options?.OnIntermediateMessage is not null)
            {
                await options.OnIntermediateMessage(newMessage).ConfigureAwait(false);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            }
        }
    }

    /// <summary>
<<<<<<< HEAD
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
=======
    /// Invokes the assistant on the specified thread with streaming response.
    /// </summary>
    /// <param name="threadId">The thread identifier.</param>
    /// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use by the agent.</param>
    /// <param name="messages">Optional receiver of the completed messages that are generated.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>An asynchronous enumeration of messages.</returns>
    /// <remarks>
    /// The `arguments` parameter is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>
    [Obsolete("Use InvokeStreamingAsync with AgentThread instead. This method will be removed after May 1st 2025.")]
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    public IAsyncEnumerable<StreamingChatMessageContent> InvokeStreamingAsync(
        string threadId,
        KernelArguments? arguments = null,
        Kernel? kernel = null,
        ChatHistory? messages = null,
        CancellationToken cancellationToken = default)
    {
        return this.InvokeStreamingAsync(threadId, options: null, arguments, kernel, messages, cancellationToken);
    }

    /// <summary>
<<<<<<< HEAD
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
=======
    /// Invokes the assistant on the specified thread with streaming response.
    /// </summary>
    /// <param name="threadId">The thread identifier.</param>
    /// <param name="options">Optional invocation options.</param>
    /// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use by the agent.</param>
    /// <param name="messages">Optional receiver of the completed messages that are generated.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>An asynchronous enumeration of messages.</returns>
    /// <remarks>
    /// The `arguments` parameter is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>
    [Obsolete("Use InvokeStreamingAsync with AgentThread instead. This method will be removed after May 1st 2025.")]
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    public IAsyncEnumerable<StreamingChatMessageContent> InvokeStreamingAsync(
        string threadId,
        AzureAIInvocationOptions? options,
        KernelArguments? arguments = null,
        Kernel? kernel = null,
        ChatHistory? messages = null,
        CancellationToken cancellationToken = default)
    {
<<<<<<< HEAD
        this.ThrowIfDeleted();

        kernel ??= this.Kernel;
        arguments = this.MergeArguments(arguments);

        // %%% STREAMING
        //return AgentThreadActions.InvokeStreamingAsync(this, this._client, threadId, messages, options, this.Logger, kernel, arguments, cancellationToken);
        return Array.Empty<StreamingChatMessageContent>().ToAsyncEnumerable();
=======
        return ActivityExtensions.RunWithActivityAsync(
            () => ModelDiagnostics.StartAgentInvocationActivity(this.Id, this.GetDisplayName(), this.Description),
            () => InternalInvokeStreamingAsync(),
            cancellationToken);

        IAsyncEnumerable<StreamingChatMessageContent> InternalInvokeStreamingAsync()
        {
            kernel ??= this.Kernel;
            return AgentThreadActions.InvokeStreamingAsync(this, this.Client, threadId, messages, options, this.Logger, kernel, arguments, cancellationToken);
        }
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <inheritdoc/>
    protected override IEnumerable<string> GetChannelKeys()
    {
        // Distinguish from other channel types.
        yield return typeof(AzureAIChannel).FullName!;
<<<<<<< HEAD

        foreach (string key in this._channelKeys)
        {
            yield return key;
        }
=======
        // Distinguish based on client instance.
        yield return this.Client.GetHashCode().ToString();
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <inheritdoc/>
    protected override async Task<AgentChannel> CreateChannelAsync(CancellationToken cancellationToken)
    {
<<<<<<< HEAD
        //this.Logger.LogAzureAIAgentCreatingChannel(nameof(CreateChannelAsync), nameof(AzureAIChannel)); // %%%

        string threadId = await AgentThreadActions.CreateThreadAsync(this._client, options: null, cancellationToken).ConfigureAwait(false);
=======
        this.Logger.LogAzureAIAgentCreatingChannel(nameof(CreateChannelAsync), nameof(AzureAIChannel));

        string threadId = await AgentThreadActions.CreateThreadAsync(this.Client, cancellationToken).ConfigureAwait(false);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        this.Logger.LogInformation("[{MethodName}] Created assistant thread: {ThreadId}", nameof(CreateChannelAsync), threadId);

        AzureAIChannel channel =
<<<<<<< HEAD
            new(this._client, threadId)
            {
                Logger = this.LoggerFactory.CreateLogger<AzureAIChannel>()
            };

        //this.Logger.LogAzureAIAgentCreatedChannel(nameof(CreateChannelAsync), nameof(AzureAIChannel), thread.Id); // %%%
=======
            new(this.Client, threadId)
            {
                Logger = this.ActiveLoggerFactory.CreateLogger<AzureAIChannel>()
            };

        this.Logger.LogAzureAIAgentCreatedChannel(nameof(CreateChannelAsync), nameof(AzureAIChannel), threadId);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        return channel;
    }

<<<<<<< HEAD
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
=======
    internal Task<string?> GetInstructionsAsync(Kernel kernel, KernelArguments? arguments, CancellationToken cancellationToken)
    {
        return this.RenderInstructionsAsync(kernel, arguments, cancellationToken);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <inheritdoc/>
    protected override async Task<AgentChannel> RestoreChannelAsync(string channelState, CancellationToken cancellationToken)
    {
        string threadId = channelState;

<<<<<<< HEAD
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
=======
        this.Logger.LogAzureAIAgentRestoringChannel(nameof(RestoreChannelAsync), nameof(AzureAIChannel), threadId);

        AAIP.AgentThread thread = await this.Client.GetThreadAsync(threadId, cancellationToken).ConfigureAwait(false);

        this.Logger.LogAzureAIAgentRestoredChannel(nameof(RestoreChannelAsync), nameof(AzureAIChannel), threadId);

        return new AzureAIChannel(this.Client, thread.Id);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }
}
