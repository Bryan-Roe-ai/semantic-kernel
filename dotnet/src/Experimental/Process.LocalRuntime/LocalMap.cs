// Copyright (c) Microsoft. All rights reserved.
using System;
using System.Collections;
using System.Collections.Concurrent;
<<<<<<< HEAD
=======
using System.Collections.Concurrent;
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Abstractions;
using Microsoft.SemanticKernel.Process.Internal;
<<<<<<< HEAD
=======
using Microsoft.SemanticKernel.Process.Internal;
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
using Microsoft.SemanticKernel.Process.Runtime;

namespace Microsoft.SemanticKernel;

internal sealed class LocalMap : LocalStep
{
    private readonly HashSet<string> _mapEvents;
    private readonly KernelProcessMap _map;
    private readonly ILogger _logger;
<<<<<<< HEAD
    private ILogger? _logger;
    private ILogger Logger => this._logger ??= this.LoggerFactory?.CreateLogger(this.Name) ?? NullLogger.Instance;
=======
    private readonly ILogger _logger;
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377

    /// <summary>
    /// Initializes a new instance of the <see cref="LocalMap"/> class.
    /// </summary>
    /// <param name="map">The <see cref="KernelProcessMap"/> instance.</param>
    /// <param name="kernel">An instance of <see cref="Kernel"/></param>
    internal LocalMap(KernelProcessMap map, Kernel kernel)
        : base(map, kernel)
    {
        this._map = map;
        this._logger = this._kernel.LoggerFactory?.CreateLogger(this._map.State.Name) ?? new NullLogger<LocalStep>();
        this._mapEvents = [.. map.Edges.Keys.Select(key => key.Split(ProcessConstants.EventIdSeparator).Last())];
<<<<<<< HEAD

        this._mapEvents = [.. map.Edges.Keys.Select(key => key.Split('.').Last())];
=======
        this._logger = this._kernel.LoggerFactory?.CreateLogger(this._map.State.Name) ?? new NullLogger<LocalStep>();
        this._mapEvents = [.. map.Edges.Keys.Select(key => key.Split(ProcessConstants.EventIdSeparator).Last())];
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
    }

    /// <inheritdoc/>
    internal override async Task HandleMessageAsync(ProcessMessage message)
    {
        IEnumerable values = message.GetMapInput(this._logger);
<<<<<<< HEAD
        IEnumerable values = message.GetMapInput(this.Logger);

        int index = 0;
        List<(Task Task, LocalKernelProcessContext ProcessContext, MapOperationContext Context)> mapOperations = [];
        ConcurrentDictionary<string, Type> capturedEvents = [];

        try
        {
            foreach (var value in values)
            {
                ++index;

                KernelProcess process = this._map.Operation.CloneProcess(this._logger);
                MapOperationContext context = new(this._mapEvents, capturedEvents);
                KernelProcess process = this._map.Operation.CloneProcess(this.Logger);
                MapOperationContext context = new(index, this._mapEvents, capturedEvents);
=======
        // Initialize the current operation
        (IEnumerable inputValues, KernelProcess mapOperation, string startEventId) = this._map.Initialize(message, this._logger);

        // Prepare state for map execution
        int index = 0;
        List<(Task Task, LocalKernelProcessContext ProcessContext, MapOperationContext Context)> mapOperations = [];
        ConcurrentDictionary<string, Type> capturedEvents = [];
        try
        {
            // Execute the map operation for each value
            foreach (var value in inputValues)
            {
                ++index;

                KernelProcess process = mapOperation.CloneProcess(this._logger);
                MapOperationContext context = new(this._mapEvents, capturedEvents);
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
#pragma warning disable CA2000 // Dispose objects before losing scope
                LocalKernelProcessContext processContext = new(process, this._kernel, context.Filter);
                Task processTask =
                    processContext.StartWithEventAsync(
                        new KernelProcessEvent
                        {
                            Id = ProcessConstants.MapEventId,
<<<<<<< HEAD
                            Id = KernelProcessMap.MapEventId,
=======
                            Id = startEventId,
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
                            Data = value
                        });
#pragma warning restore CA2000 // Dispose objects before losing scope

                mapOperations.Add((processTask, processContext, context));
            }

            // Wait for all the map operations to complete
<<<<<<< HEAD
            await Task.WhenAll(mapOperations.Select(p => p.Task)).ConfigureAwait(false);

            // Correlate the operation results to emit as the map result
            Dictionary<string, Array> resultMap = [];
            for (index = 0; index < mapOperations.Count; ++index)
            {
                foreach (KeyValuePair<string, Type> capturedEvent in capturedEvents)
                foreach (var capturedEvent in capturedEvents)
=======
            // Wait for all the map operations to complete
            await Task.WhenAll(mapOperations.Select(p => p.Task)).ConfigureAwait(false);

            // Correlate the operation results to emit as the map result
            Dictionary<string, Array> resultMap = [];
            for (index = 0; index < mapOperations.Count; ++index)
            {
                foreach (KeyValuePair<string, Type> capturedEvent in capturedEvents)
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
                {
                    string eventName = capturedEvent.Key;
                    Type resultType = capturedEvent.Value;

                    mapOperations[index].Context.Results.TryGetValue(eventName, out object? result);
                    if (!resultMap.TryGetValue(eventName, out Array? results))
                    {
                        results = Array.CreateInstance(resultType, mapOperations.Count);
                        resultMap[eventName] = results;
                    }

                    results.SetValue(result, index);
                }
            }

            // Emit map results
            foreach (string eventName in capturedEvents.Keys)
<<<<<<< HEAD
            foreach (var capturedEvent in capturedEvents)
            {
                string eventName = capturedEvent.Key;
=======
            // Emit map results
            foreach (string eventName in capturedEvents.Keys)
            {
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
                Array eventResult = resultMap[eventName];
                await this.EmitEventAsync(new() { Id = eventName, Data = eventResult }).ConfigureAwait(false);
            }
        }
        finally
        {
            foreach (var operation in mapOperations)
            {
                operation.ProcessContext.Dispose();
            }
        }
    }

    /// <inheritdoc/>
    protected override ValueTask InitializeStepAsync()
    {
        // The map does not need any further initialization as it's already been initialized.
        // Override the base method to prevent it from being called.
        return default;
    }

    private sealed record MapOperationContext(in HashSet<string> EventTargets, in IDictionary<string, Type> CapturedEvents)
<<<<<<< HEAD
    private sealed record MapOperationContext(int Index, HashSet<string> EventTargets, Dictionary<string, Type> CapturedEvents)
    {
        public ConcurrentDictionary<string, object?> Results { get; } = [];

        public bool Filter(ProcessEvent processEvent)
        {
            string eventName = processEvent.SourceId;
            if (this.EventTargets.Contains(eventName))
            {
                this.CapturedEvents.TryGetValue(eventName, out Type? resultType);
                if (resultType is null || resultType == typeof(object))
                {
                    this.CapturedEvents[eventName] = processEvent.Data?.GetType() ?? typeof(object);
                }

                this.Results[eventName] = processEvent.Data;
                    this.Results[eventName] = processEvent.Data;
                }
=======
    private sealed record MapOperationContext(in HashSet<string> EventTargets, in IDictionary<string, Type> CapturedEvents)
    {
        public ConcurrentDictionary<string, object?> Results { get; } = [];

        public bool Filter(ProcessEvent processEvent)
        {
            string eventName = processEvent.SourceId;
            if (this.EventTargets.Contains(eventName))
            {
                this.CapturedEvents.TryGetValue(eventName, out Type? resultType);
                if (resultType is null || resultType == typeof(object))
                {
                    this.CapturedEvents[eventName] = processEvent.Data?.GetType() ?? typeof(object);
                }

                this.Results[eventName] = processEvent.Data;
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
            }

            return true;
        }
    }
}
