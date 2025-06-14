// Copyright (c) Microsoft. All rights reserved.
using System;
using System.ClientModel;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Runtime.CompilerServices;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Azure;
using Azure.AI.Projects;
using Azure.AI.Agents.Persistent;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel.Agents.AzureAI.Extensions;
using Microsoft.SemanticKernel.Agents.Extensions;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.FunctionCalling;
using AAIP = Azure.AI.Projects;

namespace Microsoft.SemanticKernel.Agents.AzureAI.Internal;

/// <summary>
/// Actions associated with an Open Assistant thread.
/// </summary>
internal static class AgentThreadActions
{
    private static readonly HashSet<AzureAIP.RunStatus> s_pollingStatuses =
    [
        AzureAIP.RunStatus.Queued,
        AzureAIP.RunStatus.InProgress,
        AzureAIP.RunStatus.Cancelling,
    ];

    private static readonly HashSet<AzureAIP.RunStatus> s_failureStatuses =
    [
        AzureAIP.RunStatus.Expired,
        AzureAIP.RunStatus.Failed,
        AzureAIP.RunStatus.Cancelled,
    ];

    /// <summary>
    /// Create a new assistant thread.
    /// </summary>
    /// <param name="client">The assistant client</param>
    /// <param name="options">The options for creating the thread</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>The thread identifier</returns>
    public static async Task<string> CreateThreadAsync(AzureAIP.AgentsClient client, AzureAIThreadCreationOptions? options, CancellationToken cancellationToken = default)
    {
        AzureAIP.ThreadMessageOptions[] messages = AgentMessageFactory.GetThreadMessages(options?.Messages).ToArray();

        AzureAIP.AgentThread thread = await client.CreateThreadAsync(messages, options?.ToolResources, options?.Metadata, cancellationToken).ConfigureAwait(false);

        return thread.Id;
    }

    /// <summary>
    /// Create a message in the specified thread.
    /// </summary>
    /// <param name="client">The assistant client</param>
    /// <param name="threadId">The thread identifier</param>
    /// <param name="message">The message to add</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <throws><see cref="KernelException"/> if a system message is present, without taking any other action</throws>
    public static async Task CreateMessageAsync(AzureAIP.AgentsClient client, string threadId, ChatMessageContent message, CancellationToken cancellationToken)
    {
        if (message.Items.Any(i => i is FunctionCallContent))
        {
            return;
        }

        await client.Messages.CreateMessageAsync(
            threadId,
            message.Role == AuthorRole.User ? AzureAIP.MessageRole.User : AzureAIP.MessageRole.Agent,
            content,
            attachments: null, // %%%
            AgentMessageFactory.GetMetadata(message),
            role: message.Role == AuthorRole.User ? MessageRole.User : MessageRole.Agent,
            contentBlocks: AgentMessageFactory.GetMessageContent(message),
            attachments: AgentMessageFactory.GetAttachments(message),
            metadata: AgentMessageFactory.GetMetadata(message),
            cancellationToken).ConfigureAwait(false);
    }

    /// <summary>
    /// Retrieves the thread messages.
    /// </summary>
    /// <param name="client">The assistant client</param>
    /// <param name="threadId">The thread identifier</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of messages.</returns>
    public static async IAsyncEnumerable<ChatMessageContent> GetMessagesAsync(AzureAIP.AgentsClient client, string threadId, [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        Dictionary<string, string?> agentNames = []; // Cache agent names by their identifier

        string? lastId = null;
        AzureAIP.PageableList<AzureAIP.ThreadMessage>? messages = null;
        do
        {
            messages = await client.GetMessagesAsync(threadId, runId: null, limit: null, AzureAIP.ListSortOrder.Descending, after: lastId, before: null, cancellationToken).ConfigureAwait(false);
            foreach (AzureAIP.ThreadMessage message in messages)
            {
                lastId = message.Id;
                string? assistantName = null;
                if (!string.IsNullOrWhiteSpace(message.AssistantId) &&
                    !agentNames.TryGetValue(message.AssistantId, out assistantName))
                {
                    PersistentAgent assistant = await client.Administration.GetAgentAsync(message.AssistantId, cancellationToken).ConfigureAwait(false);
                    if (!string.IsNullOrWhiteSpace(assistant.Name))
                    {
                        agentNames.Add(assistant.Id, assistant.Name);
                    }
                }

                assistantName ??= message.AssistantId;

                ChatMessageContent content = message.ToChatMessageContent(assistantName);

                if (content.Items.Count > 0)
                {
                    yield return content;
                }
            }
        }
        while (messages.HasMorePages);
    }

    /// <summary>
    /// Invoke the assistant on the specified thread.
    /// In the enumeration returned by this method, a message is considered visible if it is intended to be displayed to the user.
    /// Example of a non-visible message is function-content for functions that are automatically executed.
    /// </summary>
    /// <param name="agent">The assistant agent to interact with the thread.</param>
    /// <param name="client">The assistant client</param>
    /// <param name="threadId">The thread identifier</param>
    /// <param name="invocationOptions">Options to utilize for the invocation</param>
    /// <param name="logger">The logger to utilize (might be agent or channel scoped)</param>
    /// <param name="kernel">The <see cref="Kernel"/> plugins and other state.</param>
    /// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of messages.</returns>
    public static async IAsyncEnumerable<(bool IsVisible, ChatMessageContent Message)> InvokeAsync(
        AzureAIAgent agent,
        AzureAIP.AgentsClient client,
        string threadId,
        AzureAIInvocationOptions? invocationOptions,
        ILogger logger,
        Kernel kernel,
        KernelArguments? arguments,
        [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        if (agent.IsDeleted)
        {
            throw new KernelException($"Agent Failure - {nameof(AzureAIAgent)} agent is deleted: {agent.Id}.");
        }

        logger.LogAzureAIAgentCreatingRun(nameof(InvokeAsync), threadId);

        AzureAIP.ToolDefinition[]? tools = [.. agent.Definition.Tools, .. kernel.Plugins.SelectMany(p => p.Select(f => f.ToToolDefinition(p.Name)))];
        // Add unique functions from the Kernel which are not already present in the agent's tools
        HashSet<string> functionToolNames = new(tools.OfType<FunctionToolDefinition>().Select(t => t.Name));
        IEnumerable<FunctionToolDefinition> functionTools = kernel.Plugins
            .SelectMany(kp => kp.Select(kf => kf.ToToolDefinition(kp.Name)))
            .Where(tool => !functionToolNames.Contains(tool.Name));
        tools.AddRange(functionTools);

        string? instructions = await agent.GetInstructionsAsync(kernel, arguments, cancellationToken).ConfigureAwait(false);

        AzureAIP.ThreadRun run = await client.CreateAsync(threadId, agent, instructions, tools, isStreaming: false, invocationOptions, cancellationToken).ConfigureAwait(false);

        logger.LogAzureAIAgentCreatedRun(nameof(InvokeAsync), run.Id, threadId);

        FunctionCallsProcessor functionProcessor = new(logger);
        // This matches current behavior.  Will be configurable upon integrating with `FunctionChoice` (#6795/#5200)
        FunctionChoiceBehaviorOptions functionOptions = new() { AllowConcurrentInvocation = true, AllowParallelCalls = true };

        // Evaluate status and process steps and messages, as encountered.
        HashSet<string> processedStepIds = [];
        Dictionary<string, FunctionResultContent> functionSteps = [];
        do
        {
            // Check for cancellation
            cancellationToken.ThrowIfCancellationRequested();

            // Poll run and steps until actionable
            await PollRunStatusAsync().ConfigureAwait(false);

            // Is in terminal state?
            if (s_failureStatuses.Contains(run.Status))
            {
                throw new KernelException($"Agent Failure - Run terminated: {run.Status} [{run.Id}]: {run.LastError?.Message ?? "Unknown"}");
            }

            AzureAIP.RunStep[] steps = await client.GetStepsAsync(run, cancellationToken).ToArrayAsync(cancellationToken).ConfigureAwait(false);

            // Is tool action required?
            if (run.Status == AzureAIP.RunStatus.RequiresAction)
            {
                logger.LogAzureAIAgentProcessingRunSteps(nameof(InvokeAsync), run.Id, threadId);

                // Execute functions in parallel and post results at once.
                FunctionCallContent[] functionCalls = [.. steps.SelectMany(step => ParseFunctionStep(agent, step))];
                if (functionCalls.Length > 0)
                {
                    // Emit function-call content
                    ChatMessageContent functionCallMessage = GenerateFunctionCallContent(agent.GetName(), functionCalls);
                    yield return (IsVisible: false, Message: functionCallMessage);

                    // Invoke functions for each tool-step
                    FunctionResultContent[] functionResults =
                        await functionProcessor.InvokeFunctionCallsAsync(
                            functionCallMessage,
                            (_) => true,
                            functionOptions,
                            kernel,
                            isStreaming: false,
                            cancellationToken).ToArrayAsync(cancellationToken).ConfigureAwait(false);

                    // Capture function-call for message processing
                    foreach (FunctionResultContent functionCall in functionResults)
                    {
                        functionSteps.Add(functionCall.CallId!, functionCall);
                    }

                    // Process tool output
                    AzureAIP.ToolOutput[] toolOutputs = GenerateToolOutputs(functionResults);

                    await client.SubmitToolOutputsToRunAsync(threadId, run.Id, toolOutputs, stream: false, cancellationToken).ConfigureAwait(false);
                }

                //logger.LogOpenAIAssistantProcessedRunSteps(nameof(InvokeAsync), functionCalls.Length, run.Id, threadId);
            }

            // Enumerate completed messages
            //logger.LogOpenAIAssistantProcessingRunMessages(nameof(InvokeAsync), run.Id, threadId);

            IEnumerable<AzureAIP.RunStep> completedStepsToProcess =
                steps
                    .Where(s => s.CompletedAt.HasValue && !processedStepIds.Contains(s.Id))
                    .OrderBy(s => s.CreatedAt);

            int messageCount = 0;
            foreach (AzureAIP.RunStep completedStep in completedStepsToProcess)
            {
                if (completedStep.Type == AzureAIP.RunStepType.ToolCalls)
                {
                    AzureAIP.RunStepToolCallDetails toolDetails = (AzureAIP.RunStepToolCallDetails)completedStep.StepDetails;
                    foreach (AzureAIP.RunStepToolCall toolCall in toolDetails.ToolCalls)
                    {
                        bool isVisible = false;
                        ChatMessageContent? content = null;

                        // Process code-interpreter content
                        if (toolCall is AzureAIP.RunStepCodeInterpreterToolCall codeTool)
                        {
                            content = GenerateCodeInterpreterContent(agent.GetName(), codeTool.Input, completedStep);
                            isVisible = true;
                        }
                        // Process function result content
                        else if (toolCall is AzureAIP.RunStepFunctionToolCall functionTool)
                        {
                            FunctionResultContent functionStep = functionSteps[functionTool.Id]; // Function step always captured on invocation
                            content = GenerateFunctionResultContent(agent.GetName(), [functionStep], completedStep);
                        }

                        if (content is not null)
                        {
                            ++messageCount;

                            yield return (isVisible, Message: content);
                        }
                    }
                }
                else if (completedStep.Type == AzureAIP.RunStepType.MessageCreation)
                {
                    // Retrieve the message
                    AzureAIP.RunStepMessageCreationDetails messageDetails = (AzureAIP.RunStepMessageCreationDetails)completedStep.StepDetails;
                    AzureAIP.ThreadMessage? message = await RetrieveMessageAsync(client, threadId, messageDetails.MessageCreation.MessageId, agent.PollingOptions.MessageSynchronizationDelay, cancellationToken).ConfigureAwait(false);

                    if (message is not null)
                    {
                        ChatMessageContent content = message.ToChatMessageContent(agent.GetName(), completedStep);

                        if (content.Items.Count > 0)
                        {
                            ++messageCount;

                            yield return (IsVisible: true, Message: content);
                        }
                    }
                }

                processedStepIds.Add(completedStep.Id);
            }

            //logger.LogOpenAIAssistantProcessedRunMessages(nameof(InvokeAsync), messageCount, run.Id, threadId);
        }
        while (AzureAIP.RunStatus.Completed != run.Status);

        //logger.LogOpenAIAssistantCompletedRun(nameof(InvokeAsync), run.Id, threadId);

        // Local function to assist in run polling (participates in method closure).
        async Task PollRunStatusAsync()
        {
            //logger.LogOpenAIAssistantPollingRunStatus(nameof(PollRunStatusAsync), run.Id, threadId);

            int count = 0;

            do
            {
                cancellationToken.ThrowIfCancellationRequested();

                if (count > 0)
                {
                    // Reduce polling frequency after a couple attempts
                    await Task.Delay(agent.PollingOptions.GetPollingInterval(count), cancellationToken).ConfigureAwait(false);
                }

                ++count;

                try
                {
                    run = await client.Runs.GetRunAsync(threadId, run.Id, cancellationToken).ConfigureAwait(false);
                }
                // The presence of a `Status` code means the server responded with error...always fail in that case
                catch (ClientResultException clientException) when (clientException.Status <= 0)
                {
                    // Check maximum retry count
                    if (count >= agent.PollingOptions.MaximumRetryCount)
                    {
                        throw;
                    }

                    // Retry for potential transient failure
                    continue;
                }
                catch (AggregateException aggregateException) when (aggregateException.InnerException is ClientResultException innerClientException)
                {
                    // The presence of a `Status` code means the server responded with error
                    if (innerClientException.Status > 0)
                    {
                        throw;
                    }

                    // Check maximum retry count
                    if (count >= agent.PollingOptions.MaximumRetryCount)
                    {
                        throw;
                    }

                    // Retry for potential transient failure
                    continue;
                }
            }
            while (s_pollingStatuses.Contains(run.Status));

            //logger.LogOpenAIAssistantPolledRunStatus(nameof(PollRunStatusAsync), run.Status, run.Id, threadId);
        }
    }

    /// <summary>
    /// Invoke the assistant on the specified thread using streaming.
    /// </summary>
    /// <param name="agent">The assistant agent to interact with the thread.</param>
    /// <param name="client">The assistant client</param>
    /// <param name="threadId">The thread identifier</param>
    /// <param name="messages">The receiver for the completed messages generated</param>
    /// <param name="invocationOptions">Options to utilize for the invocation</param>
    /// <param name="logger">The logger to utilize (might be agent or channel scoped)</param>
    /// <param name="kernel">The <see cref="Kernel"/> plugins and other state.</param>
    /// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of messages.</returns>
    /// <remarks>
    /// The `arguments` parameter is not currently used by the agent, but is provided for future extensibility.
    /// </remarks>
    public static async IAsyncEnumerable<StreamingChatMessageContent> InvokeStreamingAsync(
        AzureAIAgent agent,
        PersistentAgentsClient client,
        string threadId,
        IList<ChatMessageContent>? messages,
        AzureAIInvocationOptions? invocationOptions,
        ILogger logger,
        Kernel kernel,
        KernelArguments? arguments,
        [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        logger.LogAzureAIAgentCreatingRun(nameof(InvokeAsync), threadId);

        ToolDefinition[]? tools = [.. agent.Definition.Tools, .. kernel.Plugins.SelectMany(p => p.Select(f => f.ToToolDefinition(p.Name)))];

        string? instructions = await agent.GetInstructionsAsync(kernel, arguments, cancellationToken).ConfigureAwait(false);

        // Evaluate status and process steps and messages, as encountered.
        HashSet<string> processedStepIds = [];
        Dictionary<string, FunctionResultContent[]> stepFunctionResults = [];
        List<RunStep> stepsToProcess = [];

        FunctionCallsProcessor functionProcessor = new(logger);
        // This matches current behavior.  Will be configurable upon integrating with `FunctionChoice` (#6795/#5200)
        FunctionChoiceBehaviorOptions functionOptions = new() { AllowConcurrentInvocation = true, AllowParallelCalls = true };

        ThreadRun? run = null;
        IAsyncEnumerable<StreamingUpdate> asyncUpdates = client.CreateStreamingAsync(threadId, agent, instructions, tools, invocationOptions, cancellationToken);
        do
        {
            // Check for cancellation
            cancellationToken.ThrowIfCancellationRequested();

            stepsToProcess.Clear();

            await foreach (StreamingUpdate update in asyncUpdates.ConfigureAwait(false))
            {
                if (update is RunUpdate runUpdate)
                {
                    run = runUpdate.Value;
                }
                else if (update is MessageContentUpdate contentUpdate)
                {
                    switch (contentUpdate.UpdateKind)
                    {
                        case StreamingUpdateReason.MessageUpdated:
                            yield return GenerateStreamingMessageContent(agent.GetName(), run!, contentUpdate, logger);
                            break;
                    }
                }
                else if (update is RunStepDetailsUpdate detailsUpdate)
                {
                    StreamingChatMessageContent? toolContent = GenerateStreamingCodeInterpreterContent(agent.GetName(), detailsUpdate);
                    if (toolContent != null)
                    {
                        yield return toolContent;
                    }
                    else if (detailsUpdate.FunctionArguments != null)
                    {
                        yield return
                            new StreamingChatMessageContent(AuthorRole.Assistant, null)
                            {
                                AuthorName = agent.Name,
                                Items = [new StreamingFunctionCallUpdateContent(detailsUpdate.ToolCallId, detailsUpdate.FunctionName, detailsUpdate.FunctionArguments, detailsUpdate.ToolCallIndex ?? 0)],
                                InnerContent = detailsUpdate,
                            };
                    }
                }
                else if (update is RunStepUpdate stepUpdate)
                {
                    switch (stepUpdate.UpdateKind)
                    {
                        case StreamingUpdateReason.RunStepCompleted:
                            stepsToProcess.Add(stepUpdate.Value);
                            break;
                        default:
                            break;
                    }
                }
            }

            if (run == null)
            {
                throw new KernelException($"Agent Failure - Run not created for thread: ${threadId}");
            }

            // Is in terminal state?
            if (s_failureStatuses.Contains(run.Status))
            {
                throw new KernelException($"Agent Failure - Run terminated: {run.Status} [{run.Id}]: {run.LastError?.Message ?? "Unknown"}");
            }

            if (run.Status == RunStatus.RequiresAction)
            {
                RunStep[] activeSteps =
                    await client.GetStepsAsync(run, cancellationToken)
                    .Where(step => step.Status == RunStepStatus.InProgress)
                    .ToArrayAsync(cancellationToken).ConfigureAwait(false);

                // Capture map between the tool call and its associated step
                Dictionary<string, string> toolMap = [];
                foreach (RunStep step in activeSteps)
                {
                    RunStepToolCallDetails toolCallDetails = (RunStepToolCallDetails)step.StepDetails;
                    foreach (RunStepToolCall stepDetails in toolCallDetails.ToolCalls)
                    {
                        toolMap[stepDetails.Id] = step.Id;
                    }
                }

                // Execute functions in parallel and post results at once.
                FunctionCallContent[] functionCalls = [.. activeSteps.SelectMany(step => ParseFunctionStep(agent, step))];
                if (functionCalls.Length > 0)
                {
                    // Emit function-call content
                    ChatMessageContent functionCallMessage = GenerateFunctionCallContent(agent.GetName(), functionCalls);
                    messages?.Add(functionCallMessage);

                    FunctionResultContent[] functionResults =
                        await functionProcessor.InvokeFunctionCallsAsync(
                            functionCallMessage,
                            (_) => true,
                            functionOptions,
                            kernel,
                            isStreaming: true,
                            cancellationToken).ToArrayAsync(cancellationToken).ConfigureAwait(false);

                    // Process tool output
                    ToolOutput[] toolOutputs = GenerateToolOutputs(functionResults);
                    asyncUpdates = client.Runs.SubmitToolOutputsToStreamAsync(run, toolOutputs, cancellationToken);

                    foreach (RunStep step in activeSteps)
                    {
                        stepFunctionResults.Add(step.Id, [.. functionResults.Where(result => step.Id == toolMap[result.CallId!])]);
                    }
                }
            }

            if (stepsToProcess.Count > 0)
            {
                logger.LogAzureAIAgentProcessingRunMessages(nameof(InvokeAsync), run!.Id, threadId);

                foreach (RunStep step in stepsToProcess)
                {
                    if (step.StepDetails is RunStepMessageCreationDetails messageDetails)
                    {
                        PersistentThreadMessage? message =
                            await RetrieveMessageAsync(
                                client,
                                threadId,
                                messageDetails.MessageCreation.MessageId,
                                agent.PollingOptions.MessageSynchronizationDelay,
                                cancellationToken).ConfigureAwait(false);

                        if (message != null)
                        {
                            ChatMessageContent content = GenerateMessageContent(agent.GetName(), message, step, logger);
                            ChatMessageContent content = message.ToChatMessageContent(agent.GetName(), step);
                            messages?.Add(content);
                        }
                    }
                    else if (step.StepDetails is RunStepToolCallDetails toolDetails)
                    {
                        foreach (RunStepToolCall toolCall in toolDetails.ToolCalls)
                        {
                            if (toolCall is RunStepFunctionToolCall functionCall)
                            {
                                messages?.Add(GenerateFunctionResultContent(agent.GetName(), stepFunctionResults[step.Id], step));
                                stepFunctionResults.Remove(step.Id);
                                break;
                            }

                            if (toolCall is RunStepCodeInterpreterToolCall codeCall)
                            {
                                messages?.Add(GenerateCodeInterpreterContent(agent.GetName(), codeCall.Input, step));
                            }
                        }
                    }
                }

                logger.LogAzureAIAgentProcessedRunMessages(nameof(InvokeAsync), stepsToProcess.Count, run!.Id, threadId);
            }
        }
        while (run?.Status != RunStatus.Completed);

        logger.LogAzureAIAgentCompletedRun(nameof(InvokeAsync), run?.Id ?? "Failed", threadId);
    }

    private static ChatMessageContent GenerateMessageContent(string? assistantName, ThreadMessage message, RunStep? completedStep = null, ILogger? logger = null)
    {
        AuthorRole role = new(message.Role.ToString());

        Dictionary<string, object?>? metadata =
            new()
            {
                { nameof(AzureAIP.ThreadMessage.CreatedAt), message.CreatedAt },
                { nameof(AzureAIP.ThreadMessage.AssistantId), message.AssistantId },
                { nameof(AzureAIP.ThreadMessage.ThreadId), message.ThreadId },
                { nameof(AzureAIP.ThreadMessage.RunId), message.RunId },
                { nameof(AzureAIP.MessageContentUpdate.MessageId), message.Id },
            };

        if (completedStep != null)
        {
            metadata[nameof(AzureAIP.RunStepDetailsUpdate.StepId)] = completedStep.Id;
            metadata[nameof(AzureAIP.RunStep.Usage)] = completedStep.Usage;
        }

        ChatMessageContent content =
            new(role, content: null)
            {
                AuthorName = assistantName,
                Metadata = metadata,
            };

        foreach (AzureAIP.MessageContent itemContent in message.ContentItems)
        {
            // Process text content
            if (itemContent is AzureAIP.MessageTextContent textContent)
            {
                content.Items.Add(new TextContent(textContent.Text));

                foreach (AzureAIP.MessageTextAnnotation annotation in textContent.Annotations)
                {
                    content.Items.Add(GenerateAnnotationContent(annotation));
                }
            }
            // Process image content
            else if (itemContent is AzureAIP.MessageImageFileContent imageContent)
            {
                content.Items.Add(new FileReferenceContent(imageContent.FileId));
            }
        }

        return content;
    }

    //private static StreamingChatMessageContent GenerateStreamingMessageContent(string? assistantName, MessageContentUpdate update)
    //{
    //    StreamingChatMessageContent content =
    //        new(AuthorRole.Assistant, content: null)
    //        {
    //            AuthorName = assistantName,
    //        };

    //    // Process text content
    //    if (!string.IsNullOrEmpty(update.Text))
    //    {
    //        content.Items.Add(new StreamingTextContent(update.Text));
    //    }
    //    // Process image content
    //    else if (update.ImageFileId != null)
    //    {
    //        content.Items.Add(new StreamingFileReferenceContent(update.ImageFileId));
    //    }
    //    // Process annotations
    //    else if (update.TextAnnotation != null)
    //    {
    //        content.Items.Add(GenerateStreamingAnnotationContent(update.TextAnnotation));
    //    }

    //    if (update.Role.HasValue && update.Role.Value != MessageRole.User)
    //    {
    //        content.Role = new(update.Role.Value.ToString());
    //    }

    //    return content;
    //}

    //private static StreamingChatMessageContent? GenerateStreamingCodeInterpreterContent(string? assistantName, RunStepDetailsUpdate update)
    //{
    //    StreamingChatMessageContent content =
    //        new(AuthorRole.Assistant, content: null)
    //        {
    //            AuthorName = assistantName,
    //        };

    //    // Process text content
    //    if (update.CodeInterpreterInput != null)
    //    {
    //        content.Items.Add(new StreamingTextContent(update.CodeInterpreterInput));
    //        content.Metadata = new Dictionary<string, object?> { { OpenAIAssistantAgent.CodeInterpreterMetadataKey, true } };
    //    }

    //    if ((update.CodeInterpreterOutputs?.Count ?? 0) > 0)
    //    {
    //        foreach (var output in update.CodeInterpreterOutputs!)
    //        {
    //            if (output.ImageFileId != null)
    //            {
    //                content.Items.Add(new StreamingFileReferenceContent(output.ImageFileId));
    //            }
    //        }
    //    }

    //    return content.Items.Count > 0 ? content : null;
    //}

    private static AnnotationContent GenerateAnnotationContent(AzureAIP.MessageTextAnnotation annotation)
    {
        string? fileId = null;

        if (annotation is AzureAIP.MessageTextFileCitationAnnotation fileCitationAnnotation)
        {
            fileId = fileCitationAnnotation.FileId;
        }
        else if (annotation is AzureAIP.MessageTextFilePathAnnotation filePathAnnotation)
        {
            fileId = filePathAnnotation.FileId;
        }

        return
            new(annotation.Text)
            {
                Quote = annotation.Text,
    private static StreamingChatMessageContent GenerateStreamingMessageContent(string? assistantName, MessageContentUpdate update)
    {
        StreamingChatMessageContent content =
            new(AuthorRole.Assistant, content: null)
            {
                AuthorName = assistantName,
            };

        // Process text content
        if (!string.IsNullOrEmpty(update.Text))
        {
            content.Items.Add(new StreamingTextContent(update.Text));
        }
        // Process image content
        else if (update.ImageFileId != null)
        {
            content.Items.Add(new StreamingFileReferenceContent(update.ImageFileId));
        }
        // Process annotations
        else if (update.TextAnnotation != null)
        {
            content.Items.Add(GenerateStreamingAnnotationContent(update.TextAnnotation));
        }

        if (update.Role.HasValue && update.Role.Value != MessageRole.User)
        {
            content.Role = new(update.Role.Value.ToString() ?? MessageRole.Agent.ToString());
        }

        return content;
    }

    private static StreamingChatMessageContent? GenerateStreamingCodeInterpreterContent(string? assistantName, RunStepDetailsUpdate update)
    {
        StreamingChatMessageContent content =
            new(AuthorRole.Assistant, content: null)
            {
                AuthorName = assistantName,
            };

        // Process text content
        if (update.CodeInterpreterInput != null)
        {
            content.Items.Add(new StreamingTextContent(update.CodeInterpreterInput));
            content.Metadata = new Dictionary<string, object?> { { AzureAIAgent.CodeInterpreterMetadataKey, true } };
        }

        if ((update.CodeInterpreterOutputs?.Count ?? 0) > 0)
        {
            foreach (RunStepDeltaCodeInterpreterOutput output in update.CodeInterpreterOutputs!)
            {
                if (output is RunStepDeltaCodeInterpreterImageOutput imageOutput)
                {
                    content.Items.Add(new StreamingFileReferenceContent(imageOutput.Image.FileId));
                }
            }
        }

        return content.Items.Count > 0 ? content : null;
    }

    private static StreamingAnnotationContent GenerateStreamingAnnotationContent(TextAnnotationUpdate annotation)
    {
        string? fileId = null;

        if (!string.IsNullOrEmpty(annotation.OutputFileId))
        {
            fileId = annotation.OutputFileId;
        }
        else if (!string.IsNullOrEmpty(annotation.InputFileId))
        {
            fileId = annotation.InputFileId;
        }

        return
            new(annotation.TextToReplace)
            {
                StartIndex = annotation.StartIndex ?? 0,
                EndIndex = annotation.EndIndex ?? 0,
                FileId = fileId,
            };
    }

    //private static StreamingAnnotationContent GenerateStreamingAnnotationContent(TextAnnotationUpdate annotation)
    //{
    //    string? fileId = null;

    //    if (!string.IsNullOrEmpty(annotation.OutputFileId))
    //    {
    //        fileId = annotation.OutputFileId;
    //    }
    //    else if (!string.IsNullOrEmpty(annotation.InputFileId))
    //    {
    //        fileId = annotation.InputFileId;
    //    }

    //    return
    //        new(annotation.TextToReplace)
    //        {
    //            StartIndex = annotation.StartIndex ?? 0,
    //            EndIndex = annotation.EndIndex ?? 0,
    //            FileId = fileId,
    //        };
    //}

    private static ChatMessageContent GenerateCodeInterpreterContent(string agentName, string pythonCode, AzureAIP.RunStep completedStep)
    private static ChatMessageContent GenerateCodeInterpreterContent(string agentName, string pythonCode, RunStep completedStep)
    {
        Dictionary<string, object?> metadata = GenerateToolCallMetadata(completedStep);
        metadata[AzureAIAgent.CodeInterpreterMetadataKey] = true;

        return
            new ChatMessageContent(
                AuthorRole.Assistant,
                [
                    new TextContent(pythonCode)
                ])
            {
                AuthorName = agentName,
                Metadata = metadata,
            };
    }

    private static IEnumerable<FunctionCallContent> ParseFunctionStep(AzureAIAgent agent, AzureAIP.RunStep step)
    {
        if (step.Status == AzureAIP.RunStepStatus.InProgress && step.Type == AzureAIP.RunStepType.ToolCalls)
        {
            AzureAIP.RunStepToolCallDetails toolCallDetails = (AzureAIP.RunStepToolCallDetails)step.StepDetails;
            foreach (AzureAIP.RunStepToolCall toolCall in toolCallDetails.ToolCalls)
            {
                if (toolCall is AzureAIP.RunStepFunctionToolCall functionCall)
                {
                    (FunctionName nameParts, KernelArguments functionArguments) = ParseFunctionCall(functionCall.Name, functionCall.Arguments);

                    FunctionCallContent content = new(nameParts.Name, nameParts.PluginName, toolCall.Id, functionArguments);

                    yield return content;
                }
            }
        }
    }

    private static (FunctionName functionName, KernelArguments arguments) ParseFunctionCall(string functionName, string? functionArguments)
    {
        FunctionName nameParts = FunctionName.Parse(functionName);

        KernelArguments arguments = [];

        if (!string.IsNullOrWhiteSpace(functionArguments))
        {
            foreach (KeyValuePair<string, object> argumentKvp in JsonSerializer.Deserialize<Dictionary<string, object>>(functionArguments!) ?? [])
            {
                arguments[argumentKvp.Key] = argumentKvp.Value?.ToString();
            }
        }

        return (nameParts, arguments);
    }

    private static ChatMessageContent GenerateFunctionCallContent(string agentName, IList<FunctionCallContent> functionCalls)
    {
        ChatMessageContent functionCallContent = new(AuthorRole.Assistant, content: null)
        {
            AuthorName = agentName
        };

        functionCallContent.Items.AddRange(functionCalls);

        return functionCallContent;
    }

    private static ChatMessageContent GenerateFunctionResultContent(string agentName, IEnumerable<FunctionResultContent> functionResults, AzureAIP.RunStep completedStep)
    {
        ChatMessageContent functionResultContent = new(AuthorRole.Tool, content: null)
        {
            AuthorName = agentName,
            Metadata = GenerateToolCallMetadata(completedStep),
        };

        foreach (FunctionResultContent functionResult in functionResults)
        {
            functionResultContent.Items.Add(
                new FunctionResultContent(
                    functionResult.FunctionName,
                    functionResult.PluginName,
                    functionResult.CallId,
                    functionResult.Result));
        }

        return functionResultContent;
    }

    private static Dictionary<string, object?> GenerateToolCallMetadata(AzureAIP.RunStep completedStep)
    {
        return new()
            {
                { nameof(AzureAIP.RunStep.CreatedAt), completedStep.CreatedAt },
                { nameof(AzureAIP.RunStep.AssistantId), completedStep.AssistantId },
                { nameof(AzureAIP.RunStep.ThreadId), completedStep.ThreadId },
                { nameof(AzureAIP.RunStep.RunId), completedStep.RunId },
                { nameof(AzureAIP.RunStepDetailsUpdate.StepId), completedStep.Id },
                { nameof(AzureAIP.RunStep.Usage), completedStep.Usage },
            };
    }

    //private static Task<FunctionResultContent>[] ExecuteFunctionSteps(AzureAIAgent agent, FunctionCallContent[] functionCalls, CancellationToken cancellationToken)
    //{
    //    Task<FunctionResultContent>[] functionTasks = new Task<FunctionResultContent>[functionCalls.Length];

    //    for (int index = 0; index < functionCalls.Length; ++index)
    //    {
    //        functionTasks[index] = ExecuteFunctionStep(agent, functionCalls[index], cancellationToken);
    //    }

    //    return functionTasks;
    //}

    //private static Task<FunctionResultContent> ExecuteFunctionStep(AzureAIAgent agent, FunctionCallContent functionCall, CancellationToken cancellationToken)
    //{
    //    return functionCall.InvokeAsync(agent.Kernel, cancellationToken);
    //}

    private static AzureAIP.ToolOutput[] GenerateToolOutputs(FunctionResultContent[] functionResults)
    {
        AzureAIP.ToolOutput[] toolOutputs = new AzureAIP.ToolOutput[functionResults.Length];

        for (int index = 0; index < functionResults.Length; ++index)
        {
            FunctionResultContent functionResult = functionResults[index];

            object resultValue = functionResult.Result ?? string.Empty;

            if (resultValue is not string textResult)
            {
                textResult = JsonSerializer.Serialize(resultValue);
            }

            toolOutputs[index] = new AzureAIP.ToolOutput(functionResult.CallId, textResult!);
        }

        return toolOutputs;
    }

    private static async Task<AzureAIP.ThreadMessage?> RetrieveMessageAsync(AzureAIP.AgentsClient client, string threadId, string messageId, TimeSpan syncDelay, CancellationToken cancellationToken)
    {
        AzureAIP.ThreadMessage? message = null;

        bool retry = false;
        int count = 0;
        do
        {
            try
            {
                message = await client.Messages.GetMessageAsync(threadId, messageId, cancellationToken).ConfigureAwait(false);
            }
            catch (RequestFailedException exception)
            {
                // Step has provided the message-id.  Retry on of NotFound/404 exists.
                // Extremely rarely there might be a synchronization issue between the
                // assistant response and message-service.
                retry = exception.Status == (int)HttpStatusCode.NotFound && count < 3;
            }

            if (retry)
            {
                await Task.Delay(syncDelay, cancellationToken).ConfigureAwait(false);
            }

            ++count;
        }
        while (retry);

        return message;
    }
}
