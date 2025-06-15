// Copyright (c) Microsoft. All rights reserved.

using System;
using System.ClientModel;



using System;


using System.Collections.Generic;
using System.Diagnostics.CodeAnalysis;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel.Agents.Extensions;
using Microsoft.SemanticKernel.Agents.OpenAI.Internal;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Diagnostics;
using OpenAI.Assistants;

namespace Microsoft.SemanticKernel.Agents.OpenAI;

/// <summary>
/// Represents a <see cref="Agent"/> specialization based on Open AI Assistant / GPT.
/// </summary>
public sealed partial class OpenAIAssistantAgent : Agent
{
    /// <summary>
    /// The metadata key that identifies code-interpreter content.
    /// </summary>
    public const string CodeInterpreterMetadataKey = "code";

    internal const string OptionsMetadataKey = "__run_options";

    internal const string TemplateMetadataKey = "__template_format";

    /// <summary>

    /// Optional arguments for the agent.
    /// </summary>
    /// <remarks>
    /// This property is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>
    public KernelArguments? Arguments { get; init; }

    /// <summary>
    /// The assistant definition.

    /// Initializes a new instance of the <see cref="OpenAIAssistantAgent"/> class.

    /// </summary>
    /// <param name="definition">The assistant definition.</param>
    /// <param name="client">The OpenAI provider for accessing the Assistant API service.</param>
    /// <param name="plugins">Optional collection of plugins to add to the kernel.</param>
    /// <param name="templateFactory">An optional factory to produce the <see cref="IPromptTemplate"/> for the agent.</param>
    /// <param name="templateFormat">The format of the prompt template used when "templateFactory" parameter is supplied.</param>
    public OpenAIAssistantAgent(
        Assistant definition,
        AssistantClient client,
        IEnumerable<KernelPlugin>? plugins = null,
        IPromptTemplateFactory? templateFactory = null,
        string? templateFormat = null)
    {
        this.Client = client;

        this.Definition = definition;

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
    /// Expose client for additional use.
    /// </summary>
    public AssistantClient Client { get; }

    /// <summary>
    /// Gets the assistant definition.
    /// </summary>
    public Assistant Definition { get; }

    /// <summary>
    /// Gets the polling behavior for run processing.
    /// </summary>
    public RunPollingOptions PollingOptions { get; } = new();

    /// <summary>

    /// Expose predefined tools for run-processing.
    /// The assistant definition.
    /// </summary>
    public OpenAIAssistantDefinition Definition { get; private init; }

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
    /// Define a new <see cref="OpenAIAssistantAgent"/>.
    /// </summary>
    /// <param name="clientProvider">OpenAI client provider for accessing the API service.</param>
    /// <param name="capabilities">Defines the assistant's capabilities.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use throughout the operation.</param>
    /// <param name="defaultArguments">Optional default arguments, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="defaultArguments">Required arguments that provide default template parameters, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="templateConfig">Prompt template configuration</param>
    /// <param name="templateFactory">An optional factory to produce the <see cref="IPromptTemplate"/> for the agent</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>An <see cref="OpenAIAssistantAgent"/> instance</returns>
    public async static Task<OpenAIAssistantAgent> CreateFromTemplateAsync(
        OpenAIClientProvider clientProvider,
        OpenAIAssistantCapabilities capabilities,
        Kernel kernel,
        KernelArguments defaultArguments,
        PromptTemplateConfig templateConfig,
        IPromptTemplateFactory? templateFactory = null,
        CancellationToken cancellationToken = default)
    {
        // Validate input
        Verify.NotNull(kernel, nameof(kernel));
        Verify.NotNull(defaultArguments, nameof(defaultArguments));
        Verify.NotNull(clientProvider, nameof(clientProvider));
        Verify.NotNull(capabilities, nameof(capabilities));
        Verify.NotNull(templateConfig, nameof(templateConfig));

        // Ensure template is valid (avoid failure after posting assistant creation)
        IPromptTemplate? template = templateFactory?.Create(templateConfig);

        // Create the client
        AssistantClient client = CreateClient(clientProvider);

        // Create the assistant
        AssistantCreationOptions assistantCreationOptions = templateConfig.CreateAssistantCreationOptions(capabilities);
        AssistantCreationOptions assistantCreationOptions = templateConfig.CreateAssistantOptions(capabilities);
        Assistant model = await client.CreateAssistantAsync(capabilities.ModelId, assistantCreationOptions, cancellationToken).ConfigureAwait(false);

        // Instantiate the agent
        return
            new OpenAIAssistantAgent(model, clientProvider, client)
            {
                Kernel = kernel,
                Arguments = defaultArguments,
                Template = template,
            };
    }
    /// Expose predefined tools for run-processing.
    /// Expose predefined tools for run-processing.

    /// Gets or sets the run creation options for the assistant.

    /// </summary>
    public RunCreationOptions? RunOptions { get; init; }


    /// <summary>
    /// Create a new <see cref="OpenAIAssistantAgent"/>.
    /// </summary>

    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use throughout the operation.</param>
    /// <param name="clientProvider">OpenAI client provider for accessing the API service.</param>
    /// <param name="definition">The assistant definition.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>An <see cref="OpenAIAssistantAgent"/> instance</returns>
    public static async Task<OpenAIAssistantAgent> CreateAsync(
        Kernel kernel,
        OpenAIClientProvider clientProvider,
        OpenAIAssistantDefinition definition,
    /// <param name="clientProvider">OpenAI client provider for accessing the API service.</param>
    /// <param name="capabilities">Defines the assistant's capabilities.</param>

    /// <param name="clientProvider">The OpenAI client provider for accessing the API service.</param>
    /// <param name="capabilities">The assistant's capabilities.</param>

    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use throughout the operation.</param>
    /// <param name="defaultArguments">Required arguments that provide default template parameters, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="templateConfig">The prompt template configuration.</param>
    /// <param name="templateFactory">An prompt template factory to produce the <see cref="IPromptTemplate"/> for the agent.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>An <see cref="OpenAIAssistantAgent"/> instance.</returns>
    [Experimental("SKEXP0110")]
    [Obsolete("Use the OpenAI.Assistants.AssistantClient to create an assistant (CreateAssistantFromTemplateAsync). This method will be removed after May 1st 2025.")]
    public static async Task<OpenAIAssistantAgent> CreateFromTemplateAsync(
#pragma warning disable SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
        OpenAIClientProvider clientProvider,
#pragma warning restore SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
        OpenAIAssistantCapabilities capabilities,
        Kernel kernel,
        KernelArguments defaultArguments,
        PromptTemplateConfig templateConfig,
        IPromptTemplateFactory templateFactory,
        CancellationToken cancellationToken = default)
    {
        // Validate input
        Verify.NotNull(kernel, nameof(kernel));
        Verify.NotNull(defaultArguments, nameof(defaultArguments));
        Verify.NotNull(clientProvider, nameof(clientProvider));
        Verify.NotNull(capabilities, nameof(capabilities));
        Verify.NotNull(templateConfig, nameof(templateConfig));
        Verify.NotNull(templateFactory, nameof(templateFactory));

        // Ensure template is valid (avoid failure after posting assistant creation)
        IPromptTemplate template = templateFactory.Create(templateConfig);

        // Create the client
        AssistantClient client = clientProvider.Client.GetAssistantClient();

        // Create the assistant
        AssistantCreationOptions assistantCreationOptions = templateConfig.CreateAssistantOptions(capabilities);
        Assistant model = await client.CreateAssistantAsync(capabilities.ModelId, assistantCreationOptions, cancellationToken).ConfigureAwait(false);

        // Instantiate the agent
        return
            new OpenAIAssistantAgent(model, clientProvider.AssistantClient)
            {
                Kernel = kernel,
                Arguments = defaultArguments,
                Template = template,
            };
    }

    /// <summary>
    /// Create a new <see cref="OpenAIAssistantAgent"/>.
    /// </summary>
    /// <param name="clientProvider">The OpenAI client provider for accessing the API service.</param>
    /// <param name="definition">The assistant definition.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use throughout the operation.</param>
    /// <param name="defaultArguments">Optional default arguments, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>An <see cref="OpenAIAssistantAgent"/> instance.</returns>
    [Experimental("SKEXP0110")]
    [Obsolete("Use the OpenAI.Assistants.AssistantClient to create an assistant (CreateAssistantAsync). This method will be removed after May 1st 2025.")]
    public static async Task<OpenAIAssistantAgent> CreateAsync(
#pragma warning disable SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
        OpenAIClientProvider clientProvider,
#pragma warning restore SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
        OpenAIAssistantDefinition definition,
        Kernel kernel,
        KernelArguments? defaultArguments = null,
        CancellationToken cancellationToken = default)
    {
        // Validate input
        Verify.NotNull(kernel, nameof(kernel));
        Verify.NotNull(clientProvider, nameof(clientProvider));
        Verify.NotNull(definition, nameof(definition));

        // Create the client
        AssistantClient client = clientProvider.Client.GetAssistantClient();

        // Create the assistant
        AssistantCreationOptions assistantCreationOptions = CreateAssistantCreationOptions(definition);
        AssistantCreationOptions assistantCreationOptions = CreateAssistantCreationOptions(definition);
        AssistantCreationOptions assistantCreationOptions = CreateAssistantCreationOptions(definition);
        AssistantCreationOptions assistantCreationOptions = definition.CreateAssistantCreationOptions();
        AssistantCreationOptions assistantCreationOptions = definition.CreateAssistantOptions();
        AssistantCreationOptions assistantCreationOptions = CreateAssistantCreationOptions(definition);
        AssistantCreationOptions assistantCreationOptions = definition.CreateAssistantOptions();
        Assistant model = await client.CreateAssistantAsync(definition.ModelId, assistantCreationOptions, cancellationToken).ConfigureAwait(false);

        // Instantiate the agent
        return
            new OpenAIAssistantAgent(model, clientProvider.AssistantClient)
            {
                Kernel = kernel,
                Arguments = defaultArguments ?? [],
            };
    }

    /// <summary>
    /// Retrieves a list of assistant <see cref="OpenAIAssistantDefinition">definitions</see>.
    /// </summary>
    /// <param name="clientProvider">The configuration for accessing the API service.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>A list of <see cref="OpenAIAssistantDefinition"/> objects.</returns>
    [Experimental("SKEXP0110")]
    [Obsolete("Use the OpenAI.Assistants.AssistantClient to query for assistant definitions (GetAssistantsAsync). This method will be removed after May 1st 2025.")]
    public static async IAsyncEnumerable<OpenAIAssistantDefinition> ListDefinitionsAsync(
#pragma warning disable SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
        OpenAIClientProvider clientProvider,
#pragma warning restore SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        // Create the client
        AssistantClient client = clientProvider.Client.GetAssistantClient();

        // Query and enumerate assistant definitions
        await foreach (var page in client.GetAssistantsAsync(new AssistantCollectionOptions() { Order = ListOrder.NewestFirst }, cancellationToken).ConfigureAwait(false))
        await foreach (PageResult<Assistant> page in client.GetAssistantsAsync(new AssistantCollectionOptions() { Order = ListOrder.NewestFirst }, cancellationToken).ConfigureAwait(false))
        {
            foreach (Assistant model in page.Values)
            {
                yield return CreateAssistantDefinition(model);
            }
        await foreach (Assistant model in client.GetAssistantsAsync(new AssistantCollectionOptions() { Order = AssistantCollectionOrder.Descending }, cancellationToken).ConfigureAwait(false))
        {
            yield return CreateAssistantDefinition(model);
        await foreach (Assistant model in client.GetAssistantsAsync(new AssistantCollectionOptions() { Order = AssistantCollectionOrder.Descending }, cancellationToken).ConfigureAwait(false))
        {
            yield return CreateAssistantDefinition(model);
        await foreach (Assistant model in client.GetAssistantsAsync(new AssistantCollectionOptions() { Order = AssistantCollectionOrder.Descending }, cancellationToken).ConfigureAwait(false))
        {
        await foreach (var model in client.GetAssistantsAsync(new AssistantCollectionOptions() { Order = AssistantCollectionOrder.Descending }, cancellationToken).ConfigureAwait(false))
        {
            yield return CreateAssistantDefinition(model);
        }
    }

    /// <summary>
    /// Retrieves an <see cref="OpenAIAssistantAgent"/> by identifier.
    /// </summary>

    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use throughout the operation.</param>
    /// <param name="provider">Configuration for accessing the API service.</param>
    /// <param name="id">The agent identifier</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>An <see cref="OpenAIAssistantAgent"/> instance</returns>
    public static async Task<OpenAIAssistantAgent> RetrieveAsync(
        Kernel kernel,
        OpenAIClientProvider provider,
        string id,
        CancellationToken cancellationToken = default)
    {
        // Create the client
    /// <param name="clientProvider">Configuration for accessing the API service.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use throughout the operation.</param>
    /// <param name="provider">Configuration for accessing the API service.</param>
    /// <param name="id">The agent identifier</param>

    /// <param name="clientProvider">The configuration for accessing the API service.</param>
    /// <param name="id">The agent identifier.</param>

    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use throughout the operation.</param>
    /// <param name="defaultArguments">Optional default arguments, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="templateFactory">An optional factory to produce the <see cref="IPromptTemplate"/> for the agent.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>An <see cref="OpenAIAssistantAgent"/> instance.</returns>
    [Experimental("SKEXP0110")]
    [Obsolete("Use the OpenAI.Assistants.AssistantClient to retrieve an assistant definition (GetAssistantsAsync). This method will be removed after May 1st 2025.")]
    public static async Task<OpenAIAssistantAgent> RetrieveAsync(
#pragma warning disable SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
        OpenAIClientProvider clientProvider,

        Kernel kernel,
        OpenAIClientProvider provider,

#pragma warning restore SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.

        string id,
        Kernel kernel,
        KernelArguments? defaultArguments = null,
        IPromptTemplateFactory? templateFactory = null,
        CancellationToken cancellationToken = default)
    {
        // Validate input
        Verify.NotNull(kernel, nameof(kernel));
        Verify.NotNull(clientProvider, nameof(clientProvider));
        Verify.NotNullOrWhiteSpace(id, nameof(id));

        // Create the client

        AssistantClient client = CreateClient(clientProvider);
        AssistantClient client = CreateClient(provider);

        AssistantClient client = clientProvider.Client.GetAssistantClient();


        // Retrieve the assistant
        Assistant model = await client.GetAssistantAsync(id, cancellationToken).ConfigureAwait(false);

        // Instantiate the agent
        return
            new OpenAIAssistantAgent(model, provider, client)
            {
                Kernel = kernel,
        // Ensure template is valid (avoid failure after posting assistant creation)
        IPromptTemplate? template =
            !string.IsNullOrWhiteSpace(model.Instructions) ? templateFactory?.Create(new PromptTemplateConfig(model.Instructions!)) : null;

        // Instantiate the agent
        return

            new OpenAIAssistantAgent(model, clientProvider, client)
            new OpenAIAssistantAgent(model, provider, client)

            new OpenAIAssistantAgent(model, clientProvider.AssistantClient)

            {
                Kernel = kernel,
                Arguments = defaultArguments ?? [],
                Template = template,
            };
    }

    /// <summary>
    /// Creates a new assistant thread.
    /// </summary>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>The thread identifier.</returns>
    [Experimental("SKEXP0110")]
    [Obsolete("Use the OpenAIAssistantAgentThread to create a thread or use invoke without a thread to create a new one. This method will be removed after May 1st 2025.")]
    public Task<string> CreateThreadAsync(CancellationToken cancellationToken = default)
        => this.CreateThreadAsync(options: null, cancellationToken);

    /// <summary>
    /// Creates a new assistant thread.
    /// </summary>
    /// <param name="options">The options for creating the thread.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>The thread identifier.</returns>
    [Experimental("SKEXP0110")]
    [Obsolete("Use the OpenAIAssistantAgentThread to create a thread or use invoke without a thread to create a new one. This method will be removed after May 1st 2025.")]
    public Task<string> CreateThreadAsync(OpenAIThreadCreationOptions? options, CancellationToken cancellationToken = default)
        => this.Client.CreateThreadAsync(
            options?.Messages,
            options?.CodeInterpreterFileIds,
            options?.VectorStoreId,
            options?.Metadata,
            cancellationToken);

    /// <summary>
    /// Deletes an assistant thread.
    /// </summary>
    /// <param name="threadId">The thread identifier.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>The thread identifier.</returns>
    [Experimental("SKEXP0110")]
    [Obsolete("Use the OpenAIAssistantAgentThread to delete an existing thread. This method will be removed after May 1st 2025.")]
    public async Task<bool> DeleteThreadAsync(
        string threadId,
        CancellationToken cancellationToken = default)
    {
        // Validate input
        Verify.NotNullOrWhiteSpace(threadId, nameof(threadId));


        return await this._client.DeleteThreadAsync(threadId, cancellationToken).ConfigureAwait(false);

        ThreadDeletionResult result = await this._client.DeleteThreadAsync(threadId, cancellationToken).ConfigureAwait(false);

        ThreadDeletionResult result = await this.Client.DeleteThreadAsync(threadId, cancellationToken).ConfigureAwait(false);


        return result.Deleted;

        ThreadDeletionResult result = await this._client.DeleteThreadAsync(threadId, cancellationToken).ConfigureAwait(false);

        return result.Deleted;

        ThreadDeletionResult result = await this._client.DeleteThreadAsync(threadId, cancellationToken).ConfigureAwait(false);

        return result.Deleted;

        return (await this._client.DeleteThreadAsync(threadId, cancellationToken).ConfigureAwait(false)).Value.Deleted;
    }

    /// <summary>

    /// Uploads an file for the purpose of using with assistant.
    /// </summary>
    /// <param name="stream">The content to upload</param>
    /// <param name="name">The name of the file</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>The file identifier</returns>
    /// <remarks>
    /// Use the <see cref="FileClient"/> directly for more advanced file operations.
    /// </remarks>
    public async Task<string> UploadFileAsync(Stream stream, string name, CancellationToken cancellationToken = default)
    {
        FileClient client = this._provider.Client.GetFileClient();

        OpenAIFileInfo fileInfo = await client.UploadFileAsync(stream, name, FileUploadPurpose.Assistants, cancellationToken).ConfigureAwait(false);
    /// Use the <see cref="FileClient"/> directly for more advanced file operations.
    /// </remarks>
    public async Task<string> UploadFileAsync(Stream stream, string name, CancellationToken cancellationToken = default)
    {
        FileClient client = this._provider.Client.GetFileClient();

        OpenAIFileInfo fileInfo = await client.UploadFileAsync(stream, name, FileUploadPurpose.Assistants, cancellationToken).ConfigureAwait(false);
    /// Use the <see cref="OpenAIFileClient"/> directly for more advanced file operations.
    /// </remarks>
    public async Task<string> UploadFileAsync(Stream stream, string name, CancellationToken cancellationToken = default)
    {
        OpenAIFileClient client = this._provider.Client.GetOpenAIFileClient();

        OpenAIFile fileInfo = await client.UploadFileAsync(stream, name, FileUploadPurpose.Assistants, cancellationToken).ConfigureAwait(false);

        return fileInfo.Id;
    }

    /// <summary>


    /// Adds a message to the specified thread.
    /// </summary>
    /// <param name="threadId">The thread identifier.</param>
    /// <param name="message">A non-system message to append to the conversation.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <remarks>
    /// This method only supports messages with <see href="https://platform.openai.com/docs/api-reference/runs/createRun#runs-createrun-additional_messages">role = User or Assistant</see>.
    /// </remarks>
    [Obsolete("Pass messages directly to Invoke instead. This method will be removed after May 1st 2025.")]
    public Task AddChatMessageAsync(string threadId, ChatMessageContent message, CancellationToken cancellationToken = default)
    {
        return AssistantThreadActions.CreateMessageAsync(this.Client, threadId, message, cancellationToken);
    }

    /// <summary>
    /// Gets messages for a specified thread.
    /// </summary>
    /// <param name="threadId">The thread identifier.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>An asynchronous enumeration of messages.</returns>
    [Obsolete("Use the OpenAIAssistantAgentThread to retrieve messages instead. This method will be removed after May 1st 2025.")]
    public IAsyncEnumerable<ChatMessageContent> GetThreadMessagesAsync(string threadId, CancellationToken cancellationToken = default)
    {
        return AssistantThreadActions.GetMessagesAsync(this.Client, threadId, null, cancellationToken);
    }

    /// <summary>
    /// Deletes the assistant definition.
    /// </summary>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns><see langword="true"/> if the assistant definition was deleted.</returns>
    /// <remarks>
    /// An assistant-based agent is not usable after deletion.
    /// </remarks>
    [Experimental("SKEXP0110")]
    [Obsolete("Use the OpenAI.Assistants.AssistantClient to remove or otherwise modify the Assistant definition. This method will be removed after May 1st 2025.")]
    public async Task<bool> DeleteAsync(CancellationToken cancellationToken = default)
    {
        if (!this.IsDeleted)
        {

            this.IsDeleted = (await this._client.DeleteAssistantAsync(this.Id, cancellationToken).ConfigureAwait(false)).Value;
            AssistantDeletionResult result = await this._client.DeleteAssistantAsync(this.Id, cancellationToken).ConfigureAwait(false);

            AssistantDeletionResult result = await this.Client.DeleteAssistantAsync(this.Id, cancellationToken).ConfigureAwait(false);

            this.IsDeleted = result.Deleted;
            AssistantDeletionResult result = await this._client.DeleteAssistantAsync(this.Id, cancellationToken).ConfigureAwait(false);
            this.IsDeleted = result.Deleted;
            AssistantDeletionResult result = await this._client.DeleteAssistantAsync(this.Id, cancellationToken).ConfigureAwait(false);
            this.IsDeleted = result.Deleted;
            this.IsDeleted = (await this._client.DeleteAssistantAsync(this.Id, cancellationToken).ConfigureAwait(false)).Value.Deleted;
        }

        return this.IsDeleted;
    }



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
                options is OpenAIAssistantAgentInvokeOptions openAIAssistantAgentInvokeOptions ? openAIAssistantAgentInvokeOptions : new OpenAIAssistantAgentInvokeOptions(options),
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
        OpenAIAssistantAgentInvokeOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        Verify.NotNull(messages);

        OpenAIAssistantAgentThread openAIAssistantAgentThread = await this.EnsureThreadExistsWithMessagesAsync(
            messages,
            thread,
            () => new OpenAIAssistantAgentThread(this.Client),
            cancellationToken).ConfigureAwait(false);

        // Create options that use the RunCreationOptions from the options param if provided or
        // falls back to creating a new RunCreationOptions if additional instructions is provided
        // separately.
        var internalOptions = options?.RunCreationOptions ?? (string.IsNullOrWhiteSpace(options?.AdditionalInstructions) ? null : new RunCreationOptions()
        {
            AdditionalInstructions = options?.AdditionalInstructions,
        });

        Kernel kernel = (options?.Kernel ?? this.Kernel).Clone();

        // Get the context contributions from the AIContextProviders.
#pragma warning disable SKEXP0110, SKEXP0130 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
        AIContext providersContext = await openAIAssistantAgentThread.AIContextProviders.ModelInvokingAsync(messages, cancellationToken).ConfigureAwait(false);
        kernel.Plugins.AddFromAIContext(providersContext, "Tools");
#pragma warning restore SKEXP0110, SKEXP0130 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.

        var invokeResults = ActivityExtensions.RunWithActivityAsync(
            () => ModelDiagnostics.StartAgentInvocationActivity(this.Id, this.GetDisplayName(), this.Description),
            () => InternalInvokeAsync(),
            cancellationToken);

        async IAsyncEnumerable<ChatMessageContent> InternalInvokeAsync()
        {
            await foreach ((bool isVisible, ChatMessageContent message) in AssistantThreadActions.InvokeAsync(
                this,
                this.Client,
                openAIAssistantAgentThread.Id!,
                internalOptions,
                providersContext.Instructions,
                this.Logger,
                kernel,
                options?.KernelArguments,
                cancellationToken).ConfigureAwait(false))
            {
                // The thread and the caller should be notified of all messages regardless of visibility.
                await this.NotifyThreadOfNewMessage(openAIAssistantAgentThread, message, cancellationToken).ConfigureAwait(false);
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
            yield return new(result, openAIAssistantAgentThread);
        }
    }


    /// <summary>
    /// Invokes the assistant on the specified thread.
    /// </summary>
    /// <param name="threadId">The thread identifier.</param>
    /// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use by the agent.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>

    /// <returns>Asynchronous enumeration of messages.</returns>
    /// <returns>Asynchronous enumeration of response messages.</returns>

    /// <returns>An asynchronous enumeration of response messages.</returns>

    /// <remarks>
    /// The "arguments" parameter is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>
    [Obsolete("Use InvokeAsync with AgentThread instead. This method will be removed after May 1st 2025.")]
    public IAsyncEnumerable<ChatMessageContent> InvokeAsync(
        string threadId,
        KernelArguments? arguments = null,
        Kernel? kernel = null,
        CancellationToken cancellationToken = default)
        => this.InvokeAsync(threadId, options: null, arguments, kernel, cancellationToken);

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
    /// The "arguments" parameter is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>

    public IAsyncEnumerable<ChatMessageContent> InvokeAsync(
        string threadId,
        KernelArguments? arguments = null,
        Kernel? kernel = null,
        CancellationToken cancellationToken = default)
        => this.InvokeAsync(threadId, options: null, arguments, kernel, cancellationToken);

    /// <summary>
    /// Invoke the assistant on the specified thread.
    /// </summary>
    /// <param name="threadId">The thread identifier</param>
    /// <param name="options">Optional invocation options</param>
    /// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use by the agent.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of messages.</returns>
    /// <returns>Asynchronous enumeration of response messages.</returns>
    /// <remarks>
    /// The `arguments` parameter is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>
    public async IAsyncEnumerable<ChatMessageContent> InvokeAsync(

    [Obsolete("Use InvokeAsync with AgentThread instead. This method will be removed after May 1st 2025.")]
    public IAsyncEnumerable<ChatMessageContent> InvokeAsync(

        string threadId,
        RunCreationOptions? options,
        KernelArguments? arguments = null,
        Kernel? kernel = null,
        CancellationToken cancellationToken = default)
    {
        return ActivityExtensions.RunWithActivityAsync(
            () => ModelDiagnostics.StartAgentInvocationActivity(this.Id, this.GetDisplayName(), this.Description),
            () => InternalInvokeAsync(),
            cancellationToken);

        async IAsyncEnumerable<ChatMessageContent> InternalInvokeAsync()
        {
            kernel ??= this.Kernel;
            await foreach ((bool isVisible, ChatMessageContent message) in AssistantThreadActions.InvokeAsync(this, this.Client, threadId, options, null, this.Logger, kernel, arguments, cancellationToken).ConfigureAwait(false))
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
                options is OpenAIAssistantAgentInvokeOptions openAIAssistantAgentInvokeOptions ? openAIAssistantAgentInvokeOptions : new OpenAIAssistantAgentInvokeOptions(options),
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
        OpenAIAssistantAgentInvokeOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        Verify.NotNull(messages);



        kernel ??= this.Kernel;
        arguments ??= this.Arguments;
        arguments = this.MergeArguments(arguments);

        var openAIAssistantAgentThread = await this.EnsureThreadExistsWithMessagesAsync(

        OpenAIAssistantAgentThread openAIAssistantAgentThread = await this.EnsureThreadExistsWithMessagesAsync(

            messages,
            thread,
            () => new OpenAIAssistantAgentThread(this.Client),
            cancellationToken).ConfigureAwait(false);


        Kernel kernel = (options?.Kernel ?? this.Kernel).Clone();

        // Get the context contributions from the AIContextProviders.
#pragma warning disable SKEXP0110, SKEXP0130 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
        AIContext providersContext = await openAIAssistantAgentThread.AIContextProviders.ModelInvokingAsync(messages, cancellationToken).ConfigureAwait(false);
        kernel.Plugins.AddFromAIContext(providersContext, "Tools");
#pragma warning restore SKEXP0110, SKEXP0130 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.

        // Create options that use the RunCreationOptions from the options param if provided or
        // falls back to creating a new RunCreationOptions if additional instructions is provided
        // separately.
        var internalOptions = options?.RunCreationOptions ?? (string.IsNullOrWhiteSpace(options?.AdditionalInstructions) ? null : new RunCreationOptions()
        {
            AdditionalInstructions = options?.AdditionalInstructions,
        });

#pragma warning disable SKEXP0001 // ModelDiagnostics is marked experimental.
        ChatHistory newMessagesReceiver = [];
        var invokeResults = ActivityExtensions.RunWithActivityAsync(
            () => ModelDiagnostics.StartAgentInvocationActivity(this.Id, this.GetDisplayName(), this.Description),
            () => InternalInvokeStreamingAsync(),
            cancellationToken);
#pragma warning restore SKEXP0001 // ModelDiagnostics is marked experimental.

        IAsyncEnumerable<StreamingChatMessageContent> InternalInvokeStreamingAsync()
        {
            return AssistantThreadActions.InvokeStreamingAsync(
                this,
                this.Client,
                openAIAssistantAgentThread.Id!,
                newMessagesReceiver,
                internalOptions,
                providersContext.Instructions,
                this.Logger,
                kernel,
                options?.KernelArguments,
                cancellationToken);
        }

        // Return the chunks to the caller.
        await foreach (var result in invokeResults.ConfigureAwait(false))
        {
            yield return new(result, openAIAssistantAgentThread);
        }

        // Notify the thread of any new messages that were assembled from the streaming response.
        foreach (var newMessage in newMessagesReceiver)
        {
            await this.NotifyThreadOfNewMessage(openAIAssistantAgentThread, newMessage, cancellationToken).ConfigureAwait(false);

            if (options?.OnIntermediateMessage is not null)
            {
                await options.OnIntermediateMessage(newMessage).ConfigureAwait(false);
            }
        }
    }


    /// <summary>

    /// Invoke the assistant on the specified thread.
    /// </summary>
    /// <param name="threadId">The thread identifier</param>
    /// <param name="messages">The receiver for the completed messages generated</param>
    /// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use by the agent.</param>
    /// Invoke the assistant on the specified thread with streaming response.

    /// Invokes the assistant on the specified thread with streaming response.

    /// </summary>
    /// <param name="threadId">The thread identifier.</param>
    /// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use by the agent.</param>
    /// <param name="messages">Optional receiver of the completed messages that are generated.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>An asynchronous enumeration of messages.</returns>
    /// <remarks>
    /// The "arguments" parameter is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>
    [Obsolete("Use InvokeStreamingAsync with AgentThread instead. This method will be removed after May 1st 2025.")]
    public IAsyncEnumerable<StreamingChatMessageContent> InvokeStreamingAsync(
        string threadId,
        ChatHistory messages,
        KernelArguments? arguments = null,
        Kernel? kernel = null,
        CancellationToken cancellationToken = default)
            => this.InvokeStreamingAsync(threadId, messages, options: null, arguments, kernel, cancellationToken);

    /// <summary>
    /// Invoke the assistant on the specified thread.
    /// </summary>
    /// <param name="threadId">The thread identifier</param>
    /// <param name="messages">The receiver for the completed messages generated</param>
    /// <param name="options">Optional invocation options</param>
    /// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use by the agent.</param>
        KernelArguments? arguments = null,
        Kernel? kernel = null,
        ChatHistory? messages = null,
        CancellationToken cancellationToken = default)
        => this.InvokeStreamingAsync(threadId, options: null, arguments, kernel, messages, cancellationToken);

    /// <summary>
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
    /// The "arguments" parameter is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>
    [Obsolete("Use InvokeStreamingAsync with AgentThread instead. This method will be removed after May 1st 2025.")]
    public IAsyncEnumerable<StreamingChatMessageContent> InvokeStreamingAsync(
        string threadId,

        ChatHistory messages,
        OpenAIAssistantInvocationOptions? options,

        RunCreationOptions? options,

        KernelArguments? arguments = null,
        Kernel? kernel = null,
        ChatHistory? messages = null,
        CancellationToken cancellationToken = default)
    {
#pragma warning disable SKEXP0001 // ModelDiagnostics is marked experimental.
        return ActivityExtensions.RunWithActivityAsync(
            () => ModelDiagnostics.StartAgentInvocationActivity(this.Id, this.GetDisplayName(), this.Description),
            () => InternalInvokeStreamingAsync(),
            cancellationToken);
#pragma warning restore SKEXP0001 // ModelDiagnostics is marked experimental.


        kernel ??= this.Kernel;
        arguments ??= this.Arguments;
        arguments = this.MergeArguments(arguments);

        return AssistantThreadActions.InvokeStreamingAsync(this, this._client, threadId, messages, options, this.Logger, kernel, arguments, cancellationToken);
    }

    /// <inheritdoc/>
    protected override IEnumerable<string> GetChannelKeys()
    {
        // Distinguish from other channel types.
        yield return typeof(OpenAIAssistantChannel).FullName!;

        foreach (string key in this._channelKeys)

        IAsyncEnumerable<StreamingChatMessageContent> InternalInvokeStreamingAsync()

        {
            kernel ??= this.Kernel;
            return AssistantThreadActions.InvokeStreamingAsync(this, this.Client, threadId, messages, options, providersAdditionalInstructions: null, this.Logger, kernel, arguments, cancellationToken);
        }
    }



    /// <inheritdoc/>
    [Experimental("SKEXP0110")]
    protected override IEnumerable<string> GetChannelKeys()
    {
        // Distinguish from other channel types.
        yield return typeof(OpenAIAssistantChannel).FullName!;
        // Distinguish based on client instance.
        yield return this.Client.GetHashCode().ToString();
    }

    /// <inheritdoc/>
    [Experimental("SKEXP0110")]
    protected override async Task<AgentChannel> CreateChannelAsync(CancellationToken cancellationToken)
    {
        this.Logger.LogOpenAIAssistantAgentCreatingChannel(nameof(CreateChannelAsync), nameof(OpenAIAssistantChannel));

        AssistantThread thread = await this.Client.CreateThreadAsync(options: null, cancellationToken).ConfigureAwait(false);

        this.Logger.LogInformation("[{MethodName}] Created assistant thread: {ThreadId}", nameof(CreateChannelAsync), thread.Id);

        OpenAIAssistantChannel channel =
            new(this.Client, thread.Id)
            {
                Logger = this.ActiveLoggerFactory.CreateLogger<OpenAIAssistantChannel>()
            };

        this.Logger.LogOpenAIAssistantAgentCreatedChannel(nameof(CreateChannelAsync), nameof(OpenAIAssistantChannel), thread.Id);

        return channel;
    }
        this.Logger.LogDebug("[{MethodName}] Creating assistant thread", nameof(CreateChannelAsync));

        AssistantThread thread = await this._client.CreateThreadAsync(cancellationToken).ConfigureAwait(false);

        this.Logger.LogInformation("[{MethodName}] Created assistant thread: {ThreadId}", nameof(CreateChannelAsync), thread.Id);

    internal Task<string?> GetInstructionsAsync(Kernel kernel, KernelArguments? arguments, CancellationToken cancellationToken) =>

        this.FormatInstructionsAsync(kernel, arguments, cancellationToken);
    /// <inheritdoc/>
    protected override async Task<AgentChannel> RestoreChannelAsync(string channelState, CancellationToken cancellationToken)
    {
        string threadId = channelState;

        this.Logger.LogOpenAIAssistantAgentRestoringChannel(nameof(RestoreChannelAsync), nameof(OpenAIAssistantChannel), threadId);

        AssistantThread thread = await this._client.GetThreadAsync(threadId, cancellationToken).ConfigureAwait(false);

        this.Logger.LogOpenAIAssistantAgentRestoredChannel(nameof(RestoreChannelAsync), nameof(OpenAIAssistantChannel), threadId);

        return new OpenAIAssistantChannel(this._client, thread.Id);
    }

        this.RenderInstructionsAsync(kernel, arguments, cancellationToken);


    /// <inheritdoc/>
    [Experimental("SKEXP0110")]
    protected override async Task<AgentChannel> RestoreChannelAsync(string channelState, CancellationToken cancellationToken)
    {
        string threadId = channelState;

        this.Logger.LogOpenAIAssistantAgentRestoringChannel(nameof(RestoreChannelAsync), nameof(OpenAIAssistantChannel), threadId);

        AssistantThread thread = await this.Client.GetThreadAsync(threadId, cancellationToken).ConfigureAwait(false);

        this.Logger.LogOpenAIAssistantAgentRestoredChannel(nameof(RestoreChannelAsync), nameof(OpenAIAssistantChannel), threadId);

        return new OpenAIAssistantChannel(this.Client, thread.Id);
    }


    [Obsolete]
    private static OpenAIAssistantDefinition CreateAssistantDefinition(Assistant model)
    {
        OpenAIAssistantExecutionOptions? options = null;

        if (model.Metadata.TryGetValue(OptionsMetadataKey, out string? optionsJson))
        {
            options = JsonSerializer.Deserialize<OpenAIAssistantExecutionOptions>(optionsJson);
        }

        IReadOnlyList<string>? fileIds = (IReadOnlyList<string>?)model.ToolResources?.CodeInterpreter?.FileIds;
        string? vectorStoreId = model.ToolResources?.FileSearch?.VectorStoreIds?.SingleOrDefault();
        bool enableJsonResponse = model.ResponseFormat is not null && model.ResponseFormat == AssistantResponseFormat.JsonObject;

        return new(model.Model)
        {
            Id = model.Id,
            Name = model.Name,
            Description = model.Description,
            Instructions = model.Instructions,
            CodeInterpreterFileIds = fileIds,
            EnableCodeInterpreter = model.Tools.Any(t => t is CodeInterpreterToolDefinition),
            EnableFileSearch = model.Tools.Any(t => t is FileSearchToolDefinition),
            Metadata = model.Metadata,
            EnableJsonResponse = enableJsonResponse,
            TopP = model.NucleusSamplingFactor,
            Temperature = model.Temperature,
            VectorStoreId = string.IsNullOrWhiteSpace(vectorStoreId) ? null : vectorStoreId,
            ExecutionOptions = options,
        };
    }


    private static AssistantCreationOptions CreateAssistantCreationOptions(OpenAIAssistantDefinition definition)
    {
        AssistantCreationOptions assistantCreationOptions =
            new()
            {
                Description = definition.Description,
                Instructions = definition.Instructions,
                Name = definition.Name,
                ToolResources =
                    AssistantToolResourcesFactory.GenerateToolResources(
                        definition.EnableFileSearch ? definition.VectorStoreId : null,
                        definition.EnableCodeInterpreter ? definition.CodeInterpreterFileIds : null),
                ResponseFormat = definition.EnableJsonResponse ? AssistantResponseFormat.JsonObject : AssistantResponseFormat.Auto,
                Temperature = definition.Temperature,
                NucleusSamplingFactor = definition.TopP,
            };

        if (definition.Metadata != null)
        {
            foreach (KeyValuePair<string, string> item in definition.Metadata)
            {
                assistantCreationOptions.Metadata[item.Key] = item.Value;
            }
        }

        if (definition.ExecutionOptions != null)
        {
            string optionsJson = JsonSerializer.Serialize(definition.ExecutionOptions);
            assistantCreationOptions.Metadata[OptionsMetadataKey] = optionsJson;
        }

        if (definition.EnableCodeInterpreter)
        {
        if (model.Metadata.TryGetValue(OptionsMetadataKey, out string? optionsJson))
        {
            options = JsonSerializer.Deserialize<OpenAIAssistantExecutionOptions>(optionsJson);
        }

        IReadOnlyList<string>? fileIds = (IReadOnlyList<string>?)model.ToolResources?.CodeInterpreter?.FileIds;
        string? vectorStoreId = model.ToolResources?.FileSearch?.VectorStoreIds?.SingleOrDefault();
        bool enableJsonResponse = model.ResponseFormat is not null && model.ResponseFormat == AssistantResponseFormat.JsonObject;

        return new(model.Model)
        {
            Id = model.Id,
            Name = model.Name,
            Description = model.Description,
            Instructions = model.Instructions,
            CodeInterpreterFileIds = fileIds,
            EnableCodeInterpreter = model.Tools.Any(t => t is CodeInterpreterToolDefinition),
            EnableFileSearch = model.Tools.Any(t => t is FileSearchToolDefinition),
            Metadata = model.Metadata,
            EnableJsonResponse = enableJsonResponse,
            TopP = model.NucleusSamplingFactor,
            Temperature = model.Temperature,
            VectorStoreId = string.IsNullOrWhiteSpace(vectorStoreId) ? null : vectorStoreId,
            ExecutionOptions = options,
        };
    }

    private static AssistantClient CreateClient(OpenAIClientProvider config)
    {
        return config.Client.GetAssistantClient();
            assistantCreationOptions.Tools.Add(ToolDefinition.CreateCodeInterpreter());
        }

        if (definition.EnableFileSearch)
        {
            assistantCreationOptions.Tools.Add(ToolDefinition.CreateFileSearch());
        }

        return assistantCreationOptions;
    }

    private static AssistantClient CreateClient(OpenAIClientProvider config)
    {
        return config.Client.GetAssistantClient();
    }

    private static IEnumerable<string> DefineChannelKeys(OpenAIClientProvider config)
    {
        // Distinguish from other channel types.
        yield return typeof(AgentChannel<OpenAIAssistantAgent>).FullName!;

        foreach (string key in config.ConfigurationKeys)
        {
            yield return key;
        }
    }




}
