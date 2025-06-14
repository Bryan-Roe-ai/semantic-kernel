// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Threading;
using System.Threading.Channels;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Abstractions;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Process;
using Microsoft.SemanticKernel.Process.Internal;
using Microsoft.SemanticKernel.Process.Runtime;
using Microsoft.VisualStudio.Threading;

namespace Microsoft.SemanticKernel;

internal delegate bool ProcessEventProxy(ProcessEvent processEvent);
internal delegate bool ProcessEventFilter(KernelProcessEvent processEvent);

internal sealed class LocalProcess : LocalStep, System.IAsyncDisposable
{
    private const string EndProcessId = "Microsoft.SemanticKernel.Process.EndStep";

    private readonly JoinableTaskFactory _joinableTaskFactory;
    private readonly JoinableTaskContext _joinableTaskContext;
    private readonly Channel<KernelProcessEvent> _externalEventChannel;
    private new readonly Lazy<ValueTask> _initializeTask;
    private readonly Dictionary<string, KernelProcessAgentThread> _threads = [];

    internal readonly List<KernelProcessStepInfo> _stepsInfos;
    internal readonly List<LocalStep> _steps = [];
    internal readonly KernelProcess _process;
    internal readonly Kernel _kernel;

    private readonly ILogger _logger;

    private JoinableTask? _processTask;
    private CancellationTokenSource? _processCancelSource;
    private ProcessStateManager? _processStateManager;

    /// <summary>
    /// Initializes a new instance of the <see cref="LocalProcess"/> class.
    /// </summary>
    /// <param name="process">The <see cref="KernelProcess"/> instance.</param>
    /// <param name="kernel">An instance of <see cref="Kernel"/></param>
    /// <param name="instanceId">id to be used for LocalProcess as unique identifier</param>
    internal LocalProcess(KernelProcess process, Kernel kernel, string? instanceId = null)
        : base(process, kernel, instanceId: instanceId)
    {
        Verify.NotNull(process);
        Verify.NotNull(process.Steps);
        Verify.NotNull(kernel);

        this._stepsInfos = new List<KernelProcessStepInfo>(process.Steps);
        this._kernel = kernel;
        this._process = process;
        this._initializeTask = new Lazy<ValueTask>(this.InitializeProcessAsync);
        this._externalEventChannel = Channel.CreateUnbounded<KernelProcessEvent>();
        this._joinableTaskContext = new JoinableTaskContext();
        this._joinableTaskFactory = new JoinableTaskFactory(this._joinableTaskContext);
        this._logger = this._kernel.LoggerFactory?.CreateLogger(this.Name) ?? new NullLogger<LocalStep>();
        // if parent id is null this is the root process
        this.RootProcessId = this.ParentProcessId == null ? this.Id : null;
    }

    /// <summary>
    /// The Id of the root process.
    /// </summary>
    internal string? RootProcessId { get; init; }

    /// <summary>
    /// Starts the process with an initial event and an optional kernel.
    /// </summary>
    /// <param name="kernel">The <see cref="Kernel"/> instance to use within the running process.</param>
    /// <param name="keepAlive">Indicates if the process should wait for external events after it's finished processing.</param>
    /// <returns> <see cref="Task"/></returns>
    internal async Task StartAsync(Kernel? kernel = null, bool keepAlive = true)
    {
        // Lazy one-time initialization of the process before staring it.
        await this._initializeTask.Value.ConfigureAwait(false);

        this._processCancelSource = new CancellationTokenSource();
        this._processTask = this._joinableTaskFactory.RunAsync(()
            => this.Internal_ExecuteAsync(kernel, keepAlive: keepAlive, cancellationToken: this._processCancelSource.Token));
    }

    /// <summary>
    /// Starts the process with an initial event and then waits for the process to finish. In this case the process will not
    /// keep alive waiting for external events after the internal messages have stopped.
    /// </summary>
    /// <param name="processEvent">Required. The <see cref="KernelProcessEvent"/> to start the process with.</param>
    /// <param name="kernel">Optional. A <see cref="Kernel"/> to use when executing the process.</param>
    /// <returns>A <see cref="Task"/></returns>
    internal async Task RunOnceAsync(KernelProcessEvent processEvent, Kernel? kernel = null)
    {
        Verify.NotNull(processEvent, nameof(processEvent));
        Verify.NotNullOrWhiteSpace(processEvent.Id, $"{nameof(processEvent)}.{nameof(KernelProcessEvent.Id)}");

        await Task.Yield(); // Ensure that the process has an opportunity to run in a different synchronization context.
        await this._externalEventChannel.Writer.WriteAsync(processEvent).ConfigureAwait(false);
        await this.StartAsync(kernel, keepAlive: false).ConfigureAwait(false);
        await this._processTask!.JoinAsync().ConfigureAwait(false);
    }

    /// <summary>
    /// Starts the process with an initial event and then waits for the process to finish. In this case the process will not
    /// keep alive waiting for external events after the internal messages have stopped.
    /// </summary>
    /// <param name="processEvent">Required. The <see cref="KernelProcessEvent"/> to start the process with.</param>
    /// <param name="kernel">Optional. A <see cref="Kernel"/> to use when executing the process.</param>
    /// <param name="timeout">Optional. A <see cref="TimeSpan"/> to wait for the process to finish.</param>
    /// <returns>A <see cref="Task"/></returns>
    internal async Task RunUntilEndAsync(KernelProcessEvent processEvent, Kernel? kernel = null, TimeSpan? timeout = null)
    {
        Verify.NotNull(processEvent, nameof(processEvent));
        Verify.NotNullOrWhiteSpace(processEvent.Id, $"{nameof(processEvent)}.{nameof(KernelProcessEvent.Id)}");

        await Task.Yield(); // Ensure that the process has an opportunity to run in a different synchronization context.
        await this._externalEventChannel.Writer.WriteAsync(processEvent).ConfigureAwait(false);
        await this.StartAsync(kernel, keepAlive: true).ConfigureAwait(false);
        await this._processTask!.JoinAsync().ConfigureAwait(false);
    }

    /// <summary>
    /// Stops a running process. This will cancel the process and wait for it to complete before returning.
    /// </summary>
    /// <returns>A <see cref="Task"/></returns>
    internal async Task StopAsync()
    {
        if (this._processTask is null || this._processCancelSource is null || this._processTask.IsCompleted)
        {
            return;
        }

        // Cancel the process and wait for it to complete.
        this._processCancelSource.Cancel();

        try
        {
            await this._processTask;
        }
        catch (OperationCanceledException)
        {
            // The task was cancelled, so we can ignore this exception.
        }
        finally
        {
            this._processCancelSource.Dispose();
        }
    }

    /// <summary>
    /// Sends a message to the process. This does not start the process if it's not already running, in
    /// this case the message will remain queued until the process is started.
    /// </summary>
    /// <param name="processEvent">Required. The <see cref="KernelProcessEvent"/> to start the process with.</param>
    /// <param name="kernel">Optional. A <see cref="Kernel"/> to use when executing the process.</param>
    /// <returns>A <see cref="Task"/></returns>
    internal async Task SendMessageAsync(KernelProcessEvent processEvent, Kernel? kernel = null)
    {
        Verify.NotNull(processEvent, nameof(processEvent));
        await this._externalEventChannel.Writer.WriteAsync(processEvent).AsTask().ConfigureAwait(false);

        // make sure the process is running in case it was already cancelled
        if (this._processCancelSource == null)
        {
            await this.StartAsync(this._kernel).ConfigureAwait(false);
        }
    }

    /// <summary>
    /// Gets the process information.
    /// </summary>
    /// <returns>An instance of <see cref="KernelProcess"/></returns>
    internal Task<KernelProcess> GetProcessInfoAsync() => this.ToKernelProcessAsync();

    internal override async Task SaveStepDataAsync()
    {
        await this.SaveStepDataAsync().ConfigureAwait(false);
    }

    /// <summary>
    /// Handles a <see cref="LocalMessage"/> that has been sent to the process. This happens only in the case
    /// of a process (this one) running as a step within another process (this one's parent). In this case the
    /// entire sub-process should be executed within a single superstep.
    /// </summary>
    /// <param name="message">The message to process.</param>
    /// <returns>A <see cref="Task"/></returns>
    /// <exception cref="KernelException"></exception>
    internal override async Task HandleMessageAsync(LocalMessage message)
    {
        if (string.IsNullOrWhiteSpace(message.TargetEventId))
        {
            string errorMessage = "Internal Process Error: The target event id must be specified when sending a message to a step.";
            this.Logger.LogError("{ErrorMessage}", errorMessage);
            throw new KernelException(errorMessage);
        }

        string eventId = message.TargetEventId!;
        if (this._outputEdges!.TryGetValue(eventId, out List<KernelProcessEdge>? edges) && edges is not null)
        {
            // Create the external event that will be used to start the nested process. Since this event came
            // from outside this processes, we set the visibility to internal so that it's not emitted back out again.
            KernelProcessEvent nestedEvent = new() { Id = eventId, Data = message.TargetEventData, Visibility = KernelProcessEventVisibility.Internal };

            // Run the nested process completely within a single superstep.
            await this.RunOnceAsync(nestedEvent, this._kernel).ConfigureAwait(false);
        }
    }

    #region Private Methods
    private string GetChildStepId()
    {
        return $"{this.Id}_{Guid.NewGuid()}";
    }

    private async Task SaveStepDataAsync(bool saveChildrenState = true)
    {
        if (this.StorageManager != null && !string.IsNullOrEmpty(this._stepInfo.State.RunId))
        {
            var storageKeyValues = this.GetStepStorageKeyValues();
            var updatedProcess = this._process with { State = this._stepState, Steps = this._steps.Select(step => step._stepInfo).ToList() };
            await this.StorageManager.SaveProcessDataAsync(storageKeyValues.Item1, storageKeyValues.Item2, updatedProcess).ConfigureAwait(false);
            if (saveChildrenState)
            {
                foreach (var step in this._steps)
                {
                    await step.SaveStepDataAsync().ConfigureAwait(false);
                }
            }
        }
    }

    private async Task<Dictionary<string, string>> TryGetCachedProcessStateAsync()
    {
        Dictionary<string, string> processInfoInstanceMap = [];

        // Initialize Storage Manager
        if (this.StorageManager != null)
        {
            await this.StorageManager.InitializeAsync().ConfigureAwait(false);
            var processState = await this.StorageManager.GetProcessDataAsync(this.Name, this.Id).ConfigureAwait(false);
            if (processState != null)
            {
                // Verification process matches same process type
                // TODO: This verification should be more robust to support versioning - process name change, etc
                if (processState.ProcessName != this._stepState.StepId)
                {
                    throw new KernelException($"The process type {this._stepState.StepId} does not match the persisted process type {processState.ProcessName}").Log(this._logger);
                }

                processInfoInstanceMap = processState.Steps;
            }
        }

        return processInfoInstanceMap;
    }

    /// <summary>
    /// Loads the process and initializes the steps. Once this is complete the process can be started.
    /// </summary>
    /// <returns>A <see cref="Task"/></returns>
    private async ValueTask InitializeProcessAsync()
    {
        // Initialize the input and output edges for the process
        this._outputEdges = this._process.Edges.ToDictionary(kvp => kvp.Key, kvp => kvp.Value.ToList());
        Dictionary<string, string> processInfoInstanceMap = await this.TryGetCachedProcessStateAsync().ConfigureAwait(false);

        // TODO: Pull user state from persisted state on resume.
        this._processStateManager = new ProcessStateManager(this._process.UserStateType, null);

        // Initialize threads. TODO: Need to implement state management here.
        foreach (var kvp in this._process.Threads)
        {
            var threadDefinition = kvp.Value;
            KernelProcessAgentThread? processThread = null;
            if (threadDefinition.ThreadPolicy == KernelProcessThreadLifetime.Scoped)
            {
                // Create scoped threads now as they may be shared across steps
                AgentThread thread = await threadDefinition.CreateAgentThreadAsync(this._kernel).ConfigureAwait(false);
                processThread = new KernelProcessAgentThread
                {
                    ThreadId = thread.Id,
                    ThreadName = kvp.Key,
                    ThreadType = threadDefinition.ThreadType,
                    ThreadPolicy = threadDefinition.ThreadPolicy
                };
            }
            else
            {
                var thread = new KernelProcessAgentThread
                {
                    ThreadId = null,
                    ThreadName = kvp.Key,
                    ThreadType = threadDefinition.ThreadType,
                    ThreadPolicy = threadDefinition.ThreadPolicy
                };
            }

            this._threads.Add(kvp.Key, processThread ?? throw new KernelException("Failed to create process thread."));
        }

        // Initialize the steps within this process
        foreach (var step in this._stepsInfos)
        {
            LocalStep? localStep = null;

            // The current step should already have a name.
            Verify.NotNull(step.State?.StepId);

            // Assign id to kernelStepInfo if any before creation of Local components
            if (!processInfoInstanceMap.TryGetValue(step.State.StepId, out string? stepId) && stepId == null)
            {
                stepId = this.GetChildStepId();
            }

            KernelProcessStepInfo stepInfo = step.CloneWithIdAndEdges(stepId, this._logger);

            if (stepInfo is KernelProcess processStep)
            {
                // Subprocess should be created with an assigned id, only root process can be without the id
                Verify.NotNullOrWhiteSpace(processStep.State.RunId);
                localStep =
                    new LocalProcess(processStep, this._kernel, stepId)
                    {
                        ParentProcessId = this.Id,
                        RootProcessId = this.RootProcessId,
                        EventProxy = this.EventProxy,
                        LoggerFactory = this.LoggerFactory,
                        EventFilter = this.EventFilter,
                        ExternalMessageChannel = this.ExternalMessageChannel,
                        StorageManager = this.StorageManager,
                    };
            }
            else if (stepInfo is KernelProcessMap mapStep)
            {
                mapStep = mapStep with { Operation = mapStep.Operation with { State = mapStep.Operation.State with { RunId = mapStep.Operation.State.StepId } } };
                localStep =
                    new LocalMap(mapStep, this._kernel)
                    {
                        ParentProcessId = this.Id,
                        LoggerFactory = this.LoggerFactory,
                    };
            }
            else if (stepInfo is KernelProcessProxy proxyStep)
            {
                localStep =
                    new LocalProxy(proxyStep, this._kernel, this.ExternalMessageChannel)
                    {
                        ParentProcessId = this.RootProcessId,
                        EventProxy = this.EventProxy,
                    };
            }
            else if (stepInfo is KernelProcessAgentStep agentStep)
            {
                if (!this._threads.TryGetValue(agentStep.ThreadName, out KernelProcessAgentThread? thread) || thread is null)
                {
                    throw new KernelException($"The thread name {agentStep.ThreadName} does not have a matching thread variable defined.").Log(this._logger);
                }

                localStep = new LocalAgentStep(agentStep, this._kernel, thread, this._processStateManager, this.ParentProcessId);
            }
            else
            {
                // The current step should already have an Id.
                Verify.NotNull(stepInfo.State?.RunId);

                localStep =
                    new LocalStep(stepInfo, this._kernel)
                    {
                        ParentProcessId = this.Id,
                        EventProxy = this.EventProxy,
                        LoggerFactory = this.LoggerFactory,
                        EventFilter = this.EventFilter,
                        EventProxy = this.EventProxy
                        EventProxy = this.EventProxy,
                        StorageManager = this.StorageManager,
                    };
            }

            this._steps.Add(localStep);
        }

        // Process steps local instances have been created, saving process state
        await this.SaveStepDataAsync(saveChildrenState: false).ConfigureAwait(false);
    }

    /// <summary>
    /// Initializes this process as a step within another process.
    /// </summary>
    /// <returns>A <see cref="ValueTask"/></returns>
    /// <exception cref="KernelException"></exception>
    protected override ValueTask InitializeStepAsync()
    {
        // The process does not need any further initialization as it's already been initialized.
        // Override the base method to prevent it from being called.
        return default;
    }

    private async Task Internal_ExecuteAsync(Kernel? kernel = null, int maxSupersteps = 100, bool keepAlive = true, TimeSpan? timeout = null, CancellationToken cancellationToken = default)
    {
        Kernel localKernel = kernel ?? this._kernel;
        Queue<LocalMessage> messageChannel = new();

        try
        {
            //
            await this.EnqueueOnEnterMessagesAsync(messageChannel).ConfigureAwait(false);

            // Run the Pregel algorithm until there are no more messages being sent.
            LocalStep? finalStep = null;
            for (int superstep = 0; superstep < maxSupersteps; superstep++)
            {
                // Check for external events
                this.EnqueueExternalMessages(messageChannel);

                // Get all of the messages that have been sent to the steps within the process and queue them up for processing.
                foreach (var step in this._steps)
                {
                    await this.EnqueueStepMessagesAsync(step, messageChannel).ConfigureAwait(false);
                }

                // Complete the writing side, indicating no more messages in this superstep.
                var messagesToProcess = messageChannel.ToArray();
                messageChannel.Clear();

                // If there are no messages to process, wait for an external event.
                if (messagesToProcess.Length == 0)
                {
                    if (!keepAlive || !await this._externalEventChannel.Reader.WaitToReadAsync(cancellationToken).ConfigureAwait(false))
                    {
                        this._processCancelSource?.Cancel();
                        break;
                    }
                }

                List<Task> messageTasks = [];
                foreach (var message in messagesToProcess)
                {
                    // Check for end condition
                    if (message.DestinationId.Equals(ProcessConstants.EndStepName, StringComparison.OrdinalIgnoreCase))
                    {
                        this._processCancelSource?.Cancel();
                        break;
                    }

                    var destinationStep = this._steps.First(v => v.Name == message.DestinationId);

                    // Send a message to the step
                    messageTasks.Add(destinationStep.HandleMessageAsync(message));
                    finalStep = destinationStep;
                }

                await Task.WhenAll(messageTasks).ConfigureAwait(false);
            }
        }
        catch (Exception ex)
        {
            this.Logger?.LogError("An error occurred while running the process: {ErrorMessage}.", ex.Message);
            this._logger?.LogError(ex, "An error occurred while running the process.");
            throw;
        }
        finally
        {
            this._processCancelSource?.Dispose();
            this._processCancelSource = null;
        }

        return;
    }

    private async Task EnqueueEdgesAsync(IEnumerable<KernelProcessEdge> edges, Queue<ProcessMessage> messageChannel, ProcessEvent processEvent)
    {
        bool foundEdge = false;
        List<KernelProcessEdge> defaultConditionedEdges = [];
        foreach (var edge in edges)
        {
            // Default conditions are processed at the end if no other conditions are met.
            if (edge.Condition.IsDefault())
            {
                defaultConditionedEdges.Add(edge);
                continue;
            }

            // Check if the condition is met for this edge, if not skip it.
            bool isConditionMet = await edge.Condition.Callback(processEvent.ToKernelProcessEvent(), this._processStateManager?.GetState()).ConfigureAwait(false);
            if (!isConditionMet)
            {
                continue;
            }

            // Handle different target types
            if (edge.OutputTarget is KernelProcessStateTarget stateTarget)
            {
                if (this._processStateManager is null)
                {
                    throw new KernelException("The process state manager is not initialized.").Log(this._logger);
                }

                await (this._processStateManager.ReduceAsync((stateType, state) =>
                {
                    // this should all be contained within a callback
                    var stateJson = JsonDocument.Parse(JsonSerializer.Serialize(state));
                    stateJson = JMESUpdate.UpdateState(stateJson, stateTarget.VariableUpdate.Path, stateTarget.VariableUpdate.Operation, stateTarget.VariableUpdate.Value);
                    return Task.FromResult(stateJson.Deserialize(stateType));
                })).ConfigureAwait(false);
            }
            else if (edge.OutputTarget is KernelProcessEmitTarget emitTarget)
            {
                // Emit target from the step
            }
            else if (edge.OutputTarget is KernelProcessFunctionTarget functionTarget)
            {
                ProcessMessage message = ProcessMessageFactory.CreateFromEdge(edge, processEvent.SourceId, processEvent.Data);
                messageChannel.Enqueue(message);
            }
            else if (edge.OutputTarget is KernelProcessAgentInvokeTarget agentInvokeTarget)
            {
                ProcessMessage message = ProcessMessageFactory.CreateFromEdge(edge, processEvent.SourceId, processEvent.Data);
                messageChannel.Enqueue(message);
            }
            else
            {
                throw new KernelException("Failed to process edge type.");
            }

            foundEdge = true;
        }

        // If no edges were found for the event, check if there are any default conditioned edges to process.
        if (!foundEdge && defaultConditionedEdges.Count > 0)
        {
            foreach (KernelProcessEdge edge in defaultConditionedEdges)
            {
                ProcessMessage message = ProcessMessageFactory.CreateFromEdge(edge, this._process.State.RunId!, null, null);
                messageChannel.Enqueue(message);

                // TODO: Handle state here as well
            }
        }

        // Error event was raised with no edge to handle it, send it to an edge defined as the global error target.
        if (!foundEdge && processEvent.IsError)
        {
            if (this._outputEdges.TryGetValue(ProcessConstants.GlobalErrorEventId, out List<KernelProcessEdge>? errorEdges))
            {
                foreach (KernelProcessEdge edge in errorEdges)
                {
                    ProcessMessage message = ProcessMessageFactory.CreateFromEdge(edge, processEvent.SourceId, processEvent.Data);
                    messageChannel.Enqueue(message);
                }
            }
        }
    }

    private async Task EnqueueOnEnterMessagesAsync(Queue<ProcessMessage> messageChannel)
    {
        // TODO: Process edges for the OnProcessStart event
        foreach (var kvp in this._process.Edges.Where(e => e.Key.EndsWith(ProcessConstants.Declarative.OnEnterEvent, StringComparison.OrdinalIgnoreCase)))
        {
            var processEvent = new ProcessEvent
            {
                Namespace = this.Name,
                SourceId = this._process.State.RunId!,
                Data = null,
                Visibility = KernelProcessEventVisibility.Internal
            };

            await this.EnqueueEdgesAsync(kvp.Value, messageChannel, processEvent).ConfigureAwait(false);
        }
    }

    /// <summary>
    /// Processes external events that have been sent to the process, translates them to <see cref="LocalMessage"/>s, and enqueues
    /// them to the provided message channel so that they can be processed in the next superstep.
    /// </summary>
    /// <param name="messageChannel">The message channel where messages should be enqueued.</param>
    private void EnqueueExternalMessages(Queue<LocalMessage> messageChannel)
    {
        while (this._externalEventChannel.Reader.TryRead(out var externalEvent))
        {
            if (this._outputEdges.TryGetValue(externalEvent.Id, out List<KernelProcessEdge>? edges) && edges is not null)
            {
                foreach (var edge in edges)
                {
                    LocalMessage message = LocalMessageFactory.CreateFromEdge(edge, externalEvent.Data);
                    ProcessMessage message = ProcessMessageFactory.CreateFromEdge(edge, externalEvent.Id, externalEvent.Data);
                    messageChannel.Enqueue(message);
                }
            }
        }
    }

    /// <summary>
    /// Processes events emitted by the given step in the last superstep, translates them to <see cref="LocalMessage"/>s, and enqueues
    /// them to the provided message channel so that they can be processed in the next superstep.
    /// </summary>
    /// <param name="step">The step containing outgoing events to process.</param>
    /// <param name="messageChannel">The message channel where messages should be enqueued.</param>
    private void EnqueueStepMessages(LocalStep step, Queue<LocalMessage> messageChannel)
    private async Task EnqueueStepMessagesAsync(LocalStep step, Queue<ProcessMessage> messageChannel)
    {
        var allStepEvents = step.GetAllEvents();
        foreach (ProcessEvent stepEvent in allStepEvents)
        {
            // Emit the event out of the process (this one) if it's visibility is public.
            if (stepEvent.Visibility == KernelProcessEventVisibility.Public)
            {
                base.EmitEvent(stepEvent);
            }

            await this.EnqueueEdgesAsync(step.GetEdgeForEvent(stepEvent.QualifiedId), messageChannel, stepEvent).ConfigureAwait(false);
            // Get the edges for the event and queue up the messages to be sent to the next steps.
            bool foundEdge = false;
            foreach (KernelProcessEdge edge in step.GetEdgeForEvent(stepEvent.QualifiedId))
            {
                LocalMessage message = LocalMessageFactory.CreateFromEdge(edge, stepEvent.Data);
                messageChannel.Enqueue(message);
                foundEdge = true;
            }
            await this.EnqueueEdgesAsync(step.GetEdgeForEvent(stepEvent.QualifiedId), messageChannel, stepEvent).ConfigureAwait(false);
                bool isConditionMet = await edge.Condition.Callback(stepEvent.ToKernelProcessEvent(), this._processStateManager?.GetState()).ConfigureAwait(false);
                if (!isConditionMet)
                {
                    continue;
                }
            //bool foundEdge = false;
            //foreach (KernelProcessEdge edge in step.GetEdgeForEvent(stepEvent.QualifiedId))
            //{
            //    bool isConditionMet = await edge.Condition.Callback(stepEvent.ToKernelProcessEvent(), this._processStateManager?.GetState()).ConfigureAwait(false);
            //    if (!isConditionMet)
            //    {
            //        continue;
            //    }

            //    ProcessMessage message = ProcessMessageFactory.CreateFromEdge(edge, stepEvent.SourceId, stepEvent.Data, stepEvent.WrittenToThread);
            //    messageChannel.Enqueue(message);
            //    foundEdge = true;
            //}

            //// Get the edges for the event and queue up the messages to be sent to the next steps.
            //bool foundEdge = false;
            //List<KernelProcessEdge> defaultConditionedEdges = [];
            //foreach (KernelProcessEdge edge in step.GetEdgeForEvent(stepEvent.QualifiedId))
            //{
            //    // TODO: Make this not a string comparison
            //    // Save default conditions for the end
            //    if (edge.Condition.DeclarativeDefinition?.Equals(ProcessConstants.Declarative.DefaultCondition, StringComparison.OrdinalIgnoreCase) ?? false)
            //    {
            //        defaultConditionedEdges.Add(edge);
            //        continue;
            //    }

            //    bool isConditionMet = await edge.Condition.Callback(stepEvent.ToKernelProcessEvent(), this._processStateManager?.GetState()).ConfigureAwait(false);
            //    if (!isConditionMet)
            //    {
            //        continue;
            //    }

            //    // Handle different target types
            //    if (edge.OutputTarget is KernelProcessStateTarget stateTarget)
            //    {
            //        // TODO: Update state
            //    }
            //    else if (edge.OutputTarget is KernelProcessEmitTarget emitTarget)
            //    {
            //        // Emit target from process
            //    }
            //    else if (edge.OutputTarget is KernelProcessFunctionTarget functionTarget)
            //    {
            //        ProcessMessage message = ProcessMessageFactory.CreateFromEdge(edge, stepEvent.SourceId, stepEvent.Data, stepEvent.WrittenToThread);
            //        messageChannel.Enqueue(message);
            //    }
            //    else
            //    {
            //        throw new KernelException("Failed to process edge type.");
            //    }

            //    foundEdge = true;
            //}

            //// If no edges were found for the event, check if there are any default conditioned edges to process.
            //if (!foundEdge && defaultConditionedEdges.Count > 0)
            //{
            //    foreach (KernelProcessEdge edge in defaultConditionedEdges)
            //    {
            //        ProcessMessage message = ProcessMessageFactory.CreateFromEdge(edge, stepEvent.SourceId, stepEvent.Data, stepEvent.WrittenToThread);
            //        messageChannel.Enqueue(message);

            //        // TODO: Handle state here as well
            //    }
            //}

            //// Error event was raised with no edge to handle it, send it to an edge defined as the global error target.
            //if (!foundEdge && stepEvent.IsError)
            //{
            //    if (this._outputEdges.TryGetValue(ProcessConstants.GlobalErrorEventId, out List<KernelProcessEdge>? edges))
            //    {
            //        foreach (KernelProcessEdge edge in edges)
            //        {
            //            ProcessMessage message = ProcessMessageFactory.CreateFromEdge(edge, stepEvent.SourceId, stepEvent.Data);
            //            messageChannel.Enqueue(message);
            //        }
            //    }
            //}
        }
    }

    /// <summary>
    /// Builds a <see cref="KernelProcess"/> from the current <see cref="LocalProcess"/>.
    /// </summary>
    /// <returns>An instance of <see cref="KernelProcess"/></returns>
    /// <exception cref="InvalidOperationException"></exception>
    private async Task<KernelProcess> ToKernelProcessAsync()
    {
        var processState = new KernelProcessState(this.Name, this._stepState.Version, this.Id);
        var stepTasks = this._steps.Select(step => step.ToKernelProcessStepInfoAsync()).ToList();
        var steps = await Task.WhenAll(stepTasks).ConfigureAwait(false);
        return new KernelProcess(processState, steps, this._outputEdges, this._process.Threads);
    }

    /// <summary>
    /// When the process is used as a step within another process, this method will be called
    /// rather than ToKernelProcessAsync when extracting the state.
    /// </summary>
    /// <returns>A <see cref="Task{T}"/> where T is <see cref="KernelProcess"/></returns>
    internal override async Task<KernelProcessStepInfo> ToKernelProcessStepInfoAsync()
    {
        return await this.ToKernelProcessAsync().ConfigureAwait(false);
    }

    #endregion

    /// <inheritdoc/>
    public override async Task DeinitializeStepAsync()
    {
        await this.DisposeAsync().ConfigureAwait(false);
    }

    public async ValueTask DisposeAsync()
    {
        if (this.StorageManager != null)
        {
            await this.StorageManager.CloseAsync().ConfigureAwait(false);
        }

        this._externalEventChannel.Writer.Complete();
        this._joinableTaskContext.Dispose();
        foreach (var step in this._steps)
        {
            await step.DeinitializeStepAsync().ConfigureAwait(false);
        }
        this._processCancelSource?.Dispose();
    }
}
