<<<<<<< HEAD
﻿// Copyright (c) Microsoft. All rights reserved.
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
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
<<<<<<< HEAD
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel.Agents.AzureAI.Extensions;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.FunctionCalling;
using AzureAIP = Azure.AI.Projects;
=======
using Azure.AI.Projects;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel.Agents.AzureAI.Extensions;
using Microsoft.SemanticKernel.Agents.Extensions;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.FunctionCalling;
using AAIP = Azure.AI.Projects;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

namespace Microsoft.SemanticKernel.Agents.AzureAI.Internal;

/// <summary>
/// Actions associated with an Open Assistant thread.
/// </summary>
internal static class AgentThreadActions
{
<<<<<<< HEAD
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
=======
    private static readonly HashSet<RunStatus> s_pollingStatuses =
    [
        RunStatus.Queued,
        RunStatus.InProgress,
        RunStatus.Cancelling,
    ];

    private static readonly HashSet<RunStatus> s_failureStatuses =
    [
        RunStatus.Expired,
        RunStatus.Failed,
        RunStatus.Cancelled,
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    ];

    /// <summary>
    /// Create a new assistant thread.
    /// </summary>
    /// <param name="client">The assistant client</param>
<<<<<<< HEAD
    /// <param name="options">The options for creating the thread</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>The thread identifier</returns>
    public static async Task<string> CreateThreadAsync(AzureAIP.AgentsClient client, AzureAIThreadCreationOptions? options, CancellationToken cancellationToken = default)
    {
        AzureAIP.ThreadMessageOptions[] messages = AgentMessageFactory.GetThreadMessages(options?.Messages).ToArray();

        AzureAIP.AgentThread thread = await client.CreateThreadAsync(messages, options?.ToolResources, options?.Metadata, cancellationToken).ConfigureAwait(false);
=======
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>The thread identifier</returns>
    public static async Task<string> CreateThreadAsync(AgentsClient client, CancellationToken cancellationToken = default)
    {
        AAIP.AgentThread thread = await client.CreateThreadAsync(cancellationToken: cancellationToken).ConfigureAwait(false);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

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
<<<<<<< HEAD
    public static async Task CreateMessageAsync(AzureAIP.AgentsClient client, string threadId, ChatMessageContent message, CancellationToken cancellationToken)
=======
    public static async Task CreateMessageAsync(AgentsClient client, string threadId, ChatMessageContent message, CancellationToken cancellationToken)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        if (message.Items.Any(i => i is FunctionCallContent))
        {
            return;
        }

        string? content = message.Content;
<<<<<<< HEAD
        if (!string.IsNullOrWhiteSpace(content))
=======
        if (string.IsNullOrWhiteSpace(content))
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        {
            return;
        }

        await client.CreateMessageAsync(
            threadId,
<<<<<<< HEAD
            message.Role == AuthorRole.User ? AzureAIP.MessageRole.User : AzureAIP.MessageRole.Agent,
            content,
            attachments: null, // %%%
            AgentMessageFactory.GetMetadata(message),
=======
            role: message.Role == AuthorRole.User ? MessageRole.User : MessageRole.Agent,
            content,
            attachments: AgentMessageFactory.GetAttachments(message).ToArray(),
            metadata: AgentMessageFactory.GetMetadata(message),
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            cancellationToken).ConfigureAwait(false);
    }

    /// <summary>
    /// Retrieves the thread messages.
    /// </summary>
    /// <param name="client">The assistant client</param>
    /// <param name="threadId">The thread identifier</param>
<<<<<<< HEAD
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of messages.</returns>
    public static async IAsyncEnumerable<ChatMessageContent> GetMessagesAsync(AzureAIP.AgentsClient client, string threadId, [EnumeratorCancellation] CancellationToken cancellationToken)
=======
    /// <param name="messageOrder">The order to return messages in.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of messages.</returns>
    public static async IAsyncEnumerable<ChatMessageContent> GetMessagesAsync(AgentsClient client, string threadId, ListSortOrder? messageOrder, [EnumeratorCancellation] CancellationToken cancellationToken)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        Dictionary<string, string?> agentNames = []; // Cache agent names by their identifier

        string? lastId = null;
<<<<<<< HEAD
        AzureAIP.PageableList<AzureAIP.ThreadMessage>? messages = null;
        do
        {
            messages = await client.GetMessagesAsync(threadId, runId: null, limit: null, AzureAIP.ListSortOrder.Descending, after: lastId, before: null, cancellationToken).ConfigureAwait(false);
            foreach (AzureAIP.ThreadMessage message in messages)
=======
        PageableList<ThreadMessage>? messages = null;
        do
        {
            messages = await client.GetMessagesAsync(threadId, runId: null, limit: null, messageOrder ?? ListSortOrder.Descending, after: lastId, before: null, cancellationToken).ConfigureAwait(false);
            foreach (ThreadMessage message in messages)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            {
                lastId = message.Id;
                string? assistantName = null;
                if (!string.IsNullOrWhiteSpace(message.AssistantId) &&
                    !agentNames.TryGetValue(message.AssistantId, out assistantName))
                {
<<<<<<< HEAD
                    AzureAIP.Agent assistant = await client.GetAgentAsync(message.AssistantId, cancellationToken).ConfigureAwait(false);
=======
                    Azure.AI.Projects.Agent assistant = await client.GetAgentAsync(message.AssistantId, cancellationToken).ConfigureAwait(false);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
                    if (!string.IsNullOrWhiteSpace(assistant.Name))
                    {
                        agentNames.Add(assistant.Id, assistant.Name);
                    }
                }

                assistantName ??= message.AssistantId;

                ChatMessageContent content = GenerateMessageContent(assistantName, message);

                if (content.Items.Count > 0)
                {
                    yield return content;
                }
            }
        } while (messages?.HasMore ?? false);
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
<<<<<<< HEAD
        AzureAIP.AgentsClient client,
=======
        AgentsClient client,
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        string threadId,
        AzureAIInvocationOptions? invocationOptions,
        ILogger logger,
        Kernel kernel,
        KernelArguments? arguments,
        [EnumeratorCancellation] CancellationToken cancellationToken)
    {
<<<<<<< HEAD
        if (agent.IsDeleted)
        {
            throw new KernelException($"Agent Failure - {nameof(AzureAIAgent)} agent is deleted: {agent.Id}.");
        }

        //logger.LogOpenAIAssistantCreatingRun(nameof(InvokeAsync), threadId);

        AzureAIP.ToolDefinition[]? tools = [.. agent.Definition.Tools, .. kernel.Plugins.SelectMany(p => p.Select(f => f.ToToolDefinition(p.Name)))];

        string? instructions = await agent.GetInstructionsAsync(kernel, arguments, cancellationToken).ConfigureAwait(false);

        //RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(agent.Definition, instructions, invocationOptions);

        AzureAIP.ThreadRun run = await client.CreateAsync(threadId, agent, instructions, tools, isStreaming: false, invocationOptions, cancellationToken).ConfigureAwait(false);

        //logger.LogOpenAIAssistantCreatedRun(nameof(InvokeAsync), run.Id, threadId);
=======
        logger.LogAzureAIAgentCreatingRun(nameof(InvokeAsync), threadId);

        List<ToolDefinition> tools = new(agent.Definition.Tools);

        // Add unique functions from the Kernel which are not already present in the agent's tools
        var functionToolNames = new HashSet<string>(tools.OfType<FunctionToolDefinition>().Select(t => t.Name));
        var functionTools = kernel.Plugins
            .SelectMany(kp => kp.Select(kf => kf.ToToolDefinition(kp.Name)))
            .Where(tool => !functionToolNames.Contains(tool.Name));
        tools.AddRange(functionTools);

        string? instructions = await agent.GetInstructionsAsync(kernel, arguments, cancellationToken).ConfigureAwait(false);

        ThreadRun run = await client.CreateAsync(threadId, agent, instructions, [.. tools], invocationOptions, cancellationToken).ConfigureAwait(false);

        logger.LogAzureAIAgentCreatedRun(nameof(InvokeAsync), run.Id, threadId);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

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

<<<<<<< HEAD
            AzureAIP.RunStep[] steps = await client.GetStepsAsync(run, cancellationToken).ToArrayAsync(cancellationToken).ConfigureAwait(false);

            // Is tool action required?
            if (run.Status == AzureAIP.RunStatus.RequiresAction)
            {
                //logger.LogOpenAIAssistantProcessingRunSteps(nameof(InvokeAsync), run.Id, threadId);
=======
            RunStep[] steps = await client.GetStepsAsync(run, cancellationToken).ToArrayAsync(cancellationToken).ConfigureAwait(false);

            // Is tool action required?
            if (run.Status == RunStatus.RequiresAction)
            {
                logger.LogAzureAIAgentProcessingRunSteps(nameof(InvokeAsync), run.Id, threadId);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

                // Execute functions in parallel and post results at once.
                FunctionCallContent[] functionCalls = steps.SelectMany(step => ParseFunctionStep(agent, step)).ToArray();
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
<<<<<<< HEAD
                    AzureAIP.ToolOutput[] toolOutputs = GenerateToolOutputs(functionResults);

                    await client.SubmitToolOutputsToRunAsync(threadId, run.Id, toolOutputs, stream: false, cancellationToken).ConfigureAwait(false);
                }

                //logger.LogOpenAIAssistantProcessedRunSteps(nameof(InvokeAsync), functionCalls.Length, run.Id, threadId);
            }

            // Enumerate completed messages
            //logger.LogOpenAIAssistantProcessingRunMessages(nameof(InvokeAsync), run.Id, threadId);

            IEnumerable<AzureAIP.RunStep> completedStepsToProcess =
=======
                    ToolOutput[] toolOutputs = GenerateToolOutputs(functionResults);

                    await client.SubmitToolOutputsToRunAsync(run, toolOutputs, cancellationToken).ConfigureAwait(false);
                }

                logger.LogAzureAIAgentProcessedRunSteps(nameof(InvokeAsync), functionCalls.Length, run.Id, threadId);
            }

            // Enumerate completed messages
            logger.LogAzureAIAgentProcessingRunMessages(nameof(InvokeAsync), run.Id, threadId);

            IEnumerable<RunStep> completedStepsToProcess =
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
                steps
                    .Where(s => s.CompletedAt.HasValue && !processedStepIds.Contains(s.Id))
                    .OrderBy(s => s.CreatedAt);

            int messageCount = 0;
<<<<<<< HEAD
            foreach (AzureAIP.RunStep completedStep in completedStepsToProcess)
            {
                if (completedStep.Type == AzureAIP.RunStepType.ToolCalls)
                {
                    AzureAIP.RunStepToolCallDetails toolDetails = (AzureAIP.RunStepToolCallDetails)completedStep.StepDetails;
                    foreach (AzureAIP.RunStepToolCall toolCall in toolDetails.ToolCalls)
=======
            foreach (RunStep completedStep in completedStepsToProcess)
            {
                if (completedStep.Type == RunStepType.ToolCalls)
                {
                    RunStepToolCallDetails toolDetails = (RunStepToolCallDetails)completedStep.StepDetails;
                    foreach (RunStepToolCall toolCall in toolDetails.ToolCalls)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
                    {
                        bool isVisible = false;
                        ChatMessageContent? content = null;

                        // Process code-interpreter content
<<<<<<< HEAD
                        if (toolCall is AzureAIP.RunStepCodeInterpreterToolCall codeTool)
=======
                        if (toolCall is RunStepCodeInterpreterToolCall codeTool)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
                        {
                            content = GenerateCodeInterpreterContent(agent.GetName(), codeTool.Input, completedStep);
                            isVisible = true;
                        }
                        // Process function result content
<<<<<<< HEAD
                        else if (toolCall is AzureAIP.RunStepFunctionToolCall functionTool)
=======
                        else if (toolCall is RunStepFunctionToolCall functionTool)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
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
<<<<<<< HEAD
                else if (completedStep.Type == AzureAIP.RunStepType.MessageCreation)
                {
                    // Retrieve the message
                    AzureAIP.RunStepMessageCreationDetails messageDetails = (AzureAIP.RunStepMessageCreationDetails)completedStep.StepDetails;
                    AzureAIP.ThreadMessage? message = await RetrieveMessageAsync(client, threadId, messageDetails.MessageCreation.MessageId, agent.PollingOptions.MessageSynchronizationDelay, cancellationToken).ConfigureAwait(false);

                    if (message is not null)
                    {
                        ChatMessageContent content = GenerateMessageContent(agent.GetName(), message, completedStep);
=======
                else if (completedStep.Type == RunStepType.MessageCreation)
                {
                    // Retrieve the message
                    RunStepMessageCreationDetails messageDetails = (RunStepMessageCreationDetails)completedStep.StepDetails;
                    ThreadMessage? message = await RetrieveMessageAsync(client, threadId, messageDetails.MessageCreation.MessageId, agent.PollingOptions.MessageSynchronizationDelay, cancellationToken).ConfigureAwait(false);

                    if (message is not null)
                    {
                        ChatMessageContent content = GenerateMessageContent(agent.GetName(), message, completedStep, logger);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

                        if (content.Items.Count > 0)
                        {
                            ++messageCount;

                            yield return (IsVisible: true, Message: content);
                        }
                    }
                }

                processedStepIds.Add(completedStep.Id);
            }

<<<<<<< HEAD
            //logger.LogOpenAIAssistantProcessedRunMessages(nameof(InvokeAsync), messageCount, run.Id, threadId);
        }
        while (AzureAIP.RunStatus.Completed != run.Status);

        //logger.LogOpenAIAssistantCompletedRun(nameof(InvokeAsync), run.Id, threadId);
=======
            logger.LogAzureAIAgentProcessedRunMessages(nameof(InvokeAsync), messageCount, run.Id, threadId);
        }
        while (RunStatus.Completed != run.Status);

        logger.LogAzureAIAgentCompletedRun(nameof(InvokeAsync), run.Id, threadId);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Local function to assist in run polling (participates in method closure).
        async Task PollRunStatusAsync()
        {
<<<<<<< HEAD
            //logger.LogOpenAIAssistantPollingRunStatus(nameof(PollRunStatusAsync), run.Id, threadId);
=======
            logger.LogAzureAIAgentPollingRunStatus(nameof(PollRunStatusAsync), run.Id, threadId);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

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
                    run = await client.GetRunAsync(threadId, run.Id, cancellationToken).ConfigureAwait(false);
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

<<<<<<< HEAD
            //logger.LogOpenAIAssistantPolledRunStatus(nameof(PollRunStatusAsync), run.Status, run.Id, threadId);
        }
    }

    ///// <summary>
    ///// Invoke the assistant on the specified thread using streaming.
    ///// </summary>
    ///// <param name="agent">The assistant agent to interact with the thread.</param>
    ///// <param name="client">The assistant client</param>
    ///// <param name="threadId">The thread identifier</param>
    ///// <param name="messages">The receiver for the completed messages generated</param>
    ///// <param name="invocationOptions">Options to utilize for the invocation</param>
    ///// <param name="logger">The logger to utilize (might be agent or channel scoped)</param>
    ///// <param name="kernel">The <see cref="Kernel"/> plugins and other state.</param>
    ///// <param name="arguments">Optional arguments to pass to the agents's invocation, including any <see cref="PromptExecutionSettings"/>.</param>
    ///// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    ///// <returns>Asynchronous enumeration of messages.</returns>
    ///// <remarks>
    ///// The `arguments` parameter is not currently used by the agent, but is provided for future extensibility.
    ///// </remarks>
    //public static async IAsyncEnumerable<StreamingChatMessageContent> InvokeStreamingAsync(
    //    OpenAIAssistantAgent agent,
    //    AssistantClient client,
    //    string threadId,
    //    IList<ChatMessageContent>? messages,
    //    OpenAIAssistantInvocationOptions? invocationOptions,
    //    ILogger logger,
    //    Kernel kernel,
    //    KernelArguments? arguments,
    //    [EnumeratorCancellation] CancellationToken cancellationToken)
    //{
    //    if (agent.IsDeleted)
    //    {
    //        throw new KernelException($"Agent Failure - {nameof(OpenAIAssistantAgent)} agent is deleted: {agent.Id}.");
    //    }

    //    logger.LogOpenAIAssistantCreatingRun(nameof(InvokeAsync), threadId);

    //    ToolDefinition[]? tools = [.. agent.Tools, .. kernel.Plugins.SelectMany(p => p.Select(f => f.ToToolDefinition(p.Name)))];

    //    string? instructions = await agent.GetInstructionsAsync(kernel, arguments, cancellationToken).ConfigureAwait(false);

    //    RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(agent.Definition, instructions, invocationOptions);

    //    options.ToolsOverride.AddRange(tools);

    //    // Evaluate status and process steps and messages, as encountered.
    //    HashSet<string> processedStepIds = [];
    //    Dictionary<string, FunctionResultContent[]> stepFunctionResults = [];
    //    List<RunStep> stepsToProcess = [];
    //    ThreadRun? run = null;

    //    FunctionCallsProcessor functionProcessor = new(logger);
    //    // This matches current behavior.  Will be configurable upon integrating with `FunctionChoice` (#6795/#5200)
    //    FunctionChoiceBehaviorOptions functionOptions = new() { AllowConcurrentInvocation = true, AllowParallelCalls = true };

    //    IAsyncEnumerable<StreamingUpdate> asyncUpdates = client.CreateRunStreamingAsync(threadId, agent.Id, options, cancellationToken);
    //    do
    //    {
    //        // Check for cancellation
    //        cancellationToken.ThrowIfCancellationRequested();

    //        stepsToProcess.Clear();

    //        await foreach (StreamingUpdate update in asyncUpdates.ConfigureAwait(false))
    //        {
    //            if (update is RunUpdate runUpdate)
    //            {
    //                run = runUpdate.Value;

    //                switch (runUpdate.UpdateKind)
    //                {
    //                    case StreamingUpdateReason.RunCreated:
    //                        logger.LogOpenAIAssistantCreatedRun(nameof(InvokeAsync), run.Id, threadId);
    //                        break;
    //                }
    //            }
    //            else if (update is MessageContentUpdate contentUpdate)
    //            {
    //                switch (contentUpdate.UpdateKind)
    //                {
    //                    case StreamingUpdateReason.MessageUpdated:
    //                        yield return GenerateStreamingMessageContent(agent.GetName(), contentUpdate);
    //                        break;
    //                }
    //            }
    //            else if (update is RunStepDetailsUpdate detailsUpdate)
    //            {
    //                StreamingChatMessageContent? toolContent = GenerateStreamingCodeInterpreterContent(agent.GetName(), detailsUpdate);
    //                if (toolContent != null)
    //                {
    //                    yield return toolContent;
    //                }
    //                else if (detailsUpdate.FunctionOutput != null)
    //                {
    //                    yield return
    //                        new StreamingChatMessageContent(AuthorRole.Assistant, null)
    //                        {
    //                            AuthorName = agent.Name,
    //                            Items = [new StreamingFunctionCallUpdateContent(detailsUpdate.ToolCallId, detailsUpdate.FunctionName, detailsUpdate.FunctionArguments)]
    //                        };
    //                }
    //            }
    //            else if (update is RunStepUpdate stepUpdate)
    //            {
    //                switch (stepUpdate.UpdateKind)
    //                {
    //                    case StreamingUpdateReason.RunStepCompleted:
    //                        stepsToProcess.Add(stepUpdate.Value);
    //                        break;
    //                    default:
    //                        break;
    //                }
    //            }
    //        }

    //        if (run == null)
    //        {
    //            throw new KernelException($"Agent Failure - Run not created for thread: ${threadId}");
    //        }

    //        // Is in terminal state?
    //        if (run.Status.IsTerminal && run.Status != RunStatus.Completed)
    //        {
    //            throw new KernelException($"Agent Failure - Run terminated: {run.Status} [{run.Id}]: {run.LastError?.Message ?? "Unknown"}");
    //        }

    //        if (run.Status == RunStatus.RequiresAction)
    //        {
    //            RunStep[] activeSteps =
    //                await client.GetRunStepsAsync(run.ThreadId, run.Id, cancellationToken: cancellationToken)
    //                .Where(step => step.Status == RunStepStatus.InProgress)
    //                .ToArrayAsync(cancellationToken).ConfigureAwait(false);

    //            // Capture map between the tool call and its associated step
    //            Dictionary<string, string> toolMap = [];
    //            foreach (RunStep step in activeSteps)
    //            {
    //                foreach (RunStepToolCall stepDetails in step.Details.ToolCalls)
    //                {
    //                    toolMap[stepDetails.ToolCallId] = step.Id;
    //                }
    //            }

    //            // Execute functions in parallel and post results at once.
    //            FunctionCallContent[] functionCalls = activeSteps.SelectMany(step => ParseFunctionStep(agent, step)).ToArray();
    //            if (functionCalls.Length > 0)
    //            {
    //                // Emit function-call content
    //                ChatMessageContent functionCallMessage = GenerateFunctionCallContent(agent.GetName(), functionCalls);
    //                messages?.Add(functionCallMessage);

    //                FunctionResultContent[] functionResults =
    //                    await functionProcessor.InvokeFunctionCallsAsync(
    //                        functionCallMessage,
    //                        (_) => true,
    //                        functionOptions,
    //                        kernel,
    //                        isStreaming: true,
    //                        cancellationToken).ToArrayAsync(cancellationToken).ConfigureAwait(false);

    //                // Process tool output
    //                ToolOutput[] toolOutputs = GenerateToolOutputs(functionResults);
    //                asyncUpdates = client.SubmitToolOutputsToRunStreamingAsync(run.ThreadId, run.Id, toolOutputs, cancellationToken);

    //                foreach (RunStep step in activeSteps)
    //                {
    //                    stepFunctionResults.Add(step.Id, functionResults.Where(result => step.Id == toolMap[result.CallId!]).ToArray());
    //                }
    //            }
    //        }

    //        if (stepsToProcess.Count > 0)
    //        {
    //            logger.LogOpenAIAssistantProcessingRunMessages(nameof(InvokeAsync), run!.Id, threadId);

    //            foreach (RunStep step in stepsToProcess)
    //            {
    //                if (!string.IsNullOrEmpty(step.Details.CreatedMessageId))
    //                {
    //                    ThreadMessage? message =
    //                        await RetrieveMessageAsync(
    //                            client,
    //                            threadId,
    //                            step.Details.CreatedMessageId,
    //                            agent.PollingOptions.MessageSynchronizationDelay,
    //                            cancellationToken).ConfigureAwait(false);

    //                    if (message != null)
    //                    {
    //                        ChatMessageContent content = GenerateMessageContent(agent.GetName(), message, step);
    //                        messages?.Add(content);
    //                    }
    //                }
    //                else
    //                {
    //                    foreach (RunStepToolCall toolCall in step.Details.ToolCalls)
    //                    {
    //                        if (toolCall.ToolKind == RunStepToolCallKind.Function)
    //                        {
    //                            messages?.Add(GenerateFunctionResultContent(agent.GetName(), stepFunctionResults[step.Id], step));
    //                            stepFunctionResults.Remove(step.Id);
    //                            break;
    //                        }

    //                        if (toolCall.ToolKind == RunStepToolCallKind.CodeInterpreter)
    //                        {
    //                            messages?.Add(GenerateCodeInterpreterContent(agent.GetName(), toolCall.CodeInterpreterInput, step));
    //                        }
    //                    }
    //                }
    //            }

    //            logger.LogOpenAIAssistantProcessedRunMessages(nameof(InvokeAsync), stepsToProcess.Count, run!.Id, threadId);
    //        }
    //    }
    //    while (run?.Status != RunStatus.Completed);

    //    logger.LogOpenAIAssistantCompletedRun(nameof(InvokeAsync), run?.Id ?? "Failed", threadId);
    //}

    private static ChatMessageContent GenerateMessageContent(string? assistantName, AzureAIP.ThreadMessage message, AzureAIP.RunStep? completedStep = null)
=======
            logger.LogAzureAIAgentPolledRunStatus(nameof(PollRunStatusAsync), run.Status, run.Id, threadId);
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
        AgentsClient client,
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
                    else if (detailsUpdate.FunctionOutput != null)
                    {
                        yield return
                            new StreamingChatMessageContent(AuthorRole.Assistant, null)
                            {
                                AuthorName = agent.Name,
                                Items = [new StreamingFunctionCallUpdateContent(detailsUpdate.ToolCallId, detailsUpdate.FunctionName, detailsUpdate.FunctionArguments)]
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
                FunctionCallContent[] functionCalls = activeSteps.SelectMany(step => ParseFunctionStep(agent, step)).ToArray();
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
                    asyncUpdates = client.SubmitToolOutputsToStreamAsync(run, toolOutputs, cancellationToken);

                    foreach (RunStep step in activeSteps)
                    {
                        stepFunctionResults.Add(step.Id, functionResults.Where(result => step.Id == toolMap[result.CallId!]).ToArray());
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
                        ThreadMessage? message =
                            await RetrieveMessageAsync(
                                client,
                                threadId,
                                messageDetails.MessageCreation.MessageId,
                                agent.PollingOptions.MessageSynchronizationDelay,
                                cancellationToken).ConfigureAwait(false);

                        if (message != null)
                        {
                            ChatMessageContent content = GenerateMessageContent(agent.GetName(), message, step, logger);
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
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        AuthorRole role = new(message.Role.ToString());

        Dictionary<string, object?>? metadata =
            new()
            {
<<<<<<< HEAD
                { nameof(AzureAIP.ThreadMessage.CreatedAt), message.CreatedAt },
                { nameof(AzureAIP.ThreadMessage.AssistantId), message.AssistantId },
                { nameof(AzureAIP.ThreadMessage.ThreadId), message.ThreadId },
                { nameof(AzureAIP.ThreadMessage.RunId), message.RunId },
                { nameof(AzureAIP.MessageContentUpdate.MessageId), message.Id },
=======
                { nameof(ThreadMessage.CreatedAt), message.CreatedAt },
                { nameof(ThreadMessage.AssistantId), message.AssistantId },
                { nameof(ThreadMessage.ThreadId), message.ThreadId },
                { nameof(ThreadMessage.RunId), message.RunId },
                { nameof(MessageContentUpdate.MessageId), message.Id },
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            };

        if (completedStep != null)
        {
<<<<<<< HEAD
            metadata[nameof(AzureAIP.RunStepDetailsUpdate.StepId)] = completedStep.Id;
            metadata[nameof(AzureAIP.RunStep.Usage)] = completedStep.Usage;
=======
            metadata[nameof(RunStepDetailsUpdate.StepId)] = completedStep.Id;
            metadata[nameof(RunStep.Usage)] = completedStep.Usage;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        }

        ChatMessageContent content =
            new(role, content: null)
            {
                AuthorName = assistantName,
                Metadata = metadata,
            };

<<<<<<< HEAD
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
=======
        foreach (MessageContent itemContent in message.ContentItems)
        {
            // Process text content
            if (itemContent is MessageTextContent textContent)
            {
                content.Items.Add(new TextContent(textContent.Text));

                foreach (MessageTextAnnotation annotation in textContent.Annotations)
                {
                    AnnotationContent? annotationItem = GenerateAnnotationContent(annotation);
                    if (annotationItem != null)
                    {
                        content.Items.Add(annotationItem);
                    }
                    else
                    {
                        logger?.LogAzureAIAgentUnknownAnnotation(nameof(GenerateMessageContent), message.RunId, message.ThreadId, annotation.GetType());
                    }
                }
            }
            // Process image content
            else if (itemContent is MessageImageFileContent imageContent)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            {
                content.Items.Add(new FileReferenceContent(imageContent.FileId));
            }
        }

        return content;
    }

<<<<<<< HEAD
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
=======
    private static StreamingChatMessageContent GenerateStreamingMessageContent(string? assistantName, ThreadRun run, MessageContentUpdate update, ILogger? logger)
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
            StreamingAnnotationContent? annotationItem = GenerateStreamingAnnotationContent(update.TextAnnotation);
            if (annotationItem != null)
            {
                content.Items.Add(annotationItem);
            }
            else
            {
                logger?.LogAzureAIAgentUnknownAnnotation(nameof(GenerateStreamingMessageContent), run.Id, run.ThreadId, update.TextAnnotation.GetType());
            }
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

    private static AnnotationContent? GenerateAnnotationContent(MessageTextAnnotation annotation)
    {
        if (annotation is MessageTextFileCitationAnnotation fileCitationAnnotation)
        {
            return
                new AnnotationContent(
                    kind: AnnotationKind.FileCitation,
                    label: annotation.Text,
                    referenceId: fileCitationAnnotation.FileId)
                {
                    InnerContent = annotation,
                    StartIndex = fileCitationAnnotation.StartIndex,
                    EndIndex = fileCitationAnnotation.EndIndex,
                };
        }
        if (annotation is MessageTextUrlCitationAnnotation urlCitationAnnotation)
        {
            return
                new AnnotationContent(
                    kind: AnnotationKind.UrlCitation,
                    label: annotation.Text,
                    referenceId: urlCitationAnnotation.UrlCitation.Url)
                {
                    InnerContent = annotation,
                    Title = urlCitationAnnotation.UrlCitation.Title,
                    StartIndex = urlCitationAnnotation.StartIndex,
                    EndIndex = urlCitationAnnotation.EndIndex,
                };
        }
        else if (annotation is MessageTextFilePathAnnotation filePathAnnotation)
        {
            return
                new AnnotationContent(
                    label: annotation.Text,
                    kind: AnnotationKind.TextCitation,
                    referenceId: filePathAnnotation.FileId)
                {
                    InnerContent = annotation,
                    StartIndex = filePathAnnotation.StartIndex,
                    EndIndex = filePathAnnotation.EndIndex,
                };
        }

        return null;
    }

    private static StreamingAnnotationContent? GenerateStreamingAnnotationContent(TextAnnotationUpdate annotation)
    {
        string? referenceId = null;
        AnnotationKind kind;

        if (!string.IsNullOrEmpty(annotation.OutputFileId))
        {
            referenceId = annotation.OutputFileId;
            kind = AnnotationKind.TextCitation;
        }
        else if (!string.IsNullOrEmpty(annotation.InputFileId))
        {
            referenceId = annotation.InputFileId;
            kind = AnnotationKind.FileCitation;
        }
        else if (!string.IsNullOrEmpty(annotation.Url))
        {
            referenceId = annotation.Url;
            kind = AnnotationKind.UrlCitation;
        }
        else
        {
            return null;
        }

        return
            new StreamingAnnotationContent(kind, referenceId)
            {
                Label = annotation.TextToReplace,
                InnerContent = annotation,
                Title = annotation.Title,
                StartIndex = annotation.StartIndex,
                EndIndex = annotation.EndIndex,
            };
    }

    private static ChatMessageContent GenerateCodeInterpreterContent(string agentName, string pythonCode, RunStep completedStep)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
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

<<<<<<< HEAD
    private static IEnumerable<FunctionCallContent> ParseFunctionStep(AzureAIAgent agent, AzureAIP.RunStep step)
    {
        if (step.Status == AzureAIP.RunStepStatus.InProgress && step.Type == AzureAIP.RunStepType.ToolCalls)
        {
            AzureAIP.RunStepToolCallDetails toolCallDetails = (AzureAIP.RunStepToolCallDetails)step.StepDetails;
            foreach (AzureAIP.RunStepToolCall toolCall in toolCallDetails.ToolCalls)
            {
                if (toolCall is AzureAIP.RunStepFunctionToolCall functionCall)
=======
    private static IEnumerable<FunctionCallContent> ParseFunctionStep(AzureAIAgent agent, RunStep step)
    {
        if (step.Status == RunStepStatus.InProgress && step.Type == RunStepType.ToolCalls)
        {
            RunStepToolCallDetails toolCallDetails = (RunStepToolCallDetails)step.StepDetails;
            foreach (RunStepToolCall toolCall in toolCallDetails.ToolCalls)
            {
                if (toolCall is RunStepFunctionToolCall functionCall)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
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
            foreach (var argumentKvp in JsonSerializer.Deserialize<Dictionary<string, object>>(functionArguments!)!)
            {
                arguments[argumentKvp.Key] = argumentKvp.Value.ToString();
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

<<<<<<< HEAD
    private static ChatMessageContent GenerateFunctionResultContent(string agentName, IEnumerable<FunctionResultContent> functionResults, AzureAIP.RunStep completedStep)
=======
    private static ChatMessageContent GenerateFunctionResultContent(string agentName, IEnumerable<FunctionResultContent> functionResults, RunStep completedStep)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
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

<<<<<<< HEAD
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
=======
    private static Dictionary<string, object?> GenerateToolCallMetadata(RunStep completedStep)
    {
        return new()
            {
                { nameof(RunStep.CreatedAt), completedStep.CreatedAt },
                { nameof(RunStep.AssistantId), completedStep.AssistantId },
                { nameof(RunStep.ThreadId), completedStep.ThreadId },
                { nameof(RunStep.RunId), completedStep.RunId },
                { nameof(RunStepDetailsUpdate.StepId), completedStep.Id },
                { nameof(RunStep.Usage), completedStep.Usage },
            };
    }

    private static ToolOutput[] GenerateToolOutputs(FunctionResultContent[] functionResults)
    {
        ToolOutput[] toolOutputs = new ToolOutput[functionResults.Length];
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        for (int index = 0; index < functionResults.Length; ++index)
        {
            FunctionResultContent functionResult = functionResults[index];

            object resultValue = functionResult.Result ?? string.Empty;

            if (resultValue is not string textResult)
            {
                textResult = JsonSerializer.Serialize(resultValue);
            }

<<<<<<< HEAD
            toolOutputs[index] = new AzureAIP.ToolOutput(functionResult.CallId, textResult!);
=======
            toolOutputs[index] = new ToolOutput(functionResult.CallId, textResult!);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        }

        return toolOutputs;
    }

<<<<<<< HEAD
    private static async Task<AzureAIP.ThreadMessage?> RetrieveMessageAsync(AzureAIP.AgentsClient client, string threadId, string messageId, TimeSpan syncDelay, CancellationToken cancellationToken)
    {
        AzureAIP.ThreadMessage? message = null;
=======
    private static async Task<ThreadMessage?> RetrieveMessageAsync(AgentsClient client, string threadId, string messageId, TimeSpan syncDelay, CancellationToken cancellationToken)
    {
        ThreadMessage? message = null;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        bool retry = false;
        int count = 0;
        do
        {
            try
            {
                message = await client.GetMessageAsync(threadId, messageId, cancellationToken).ConfigureAwait(false);
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
