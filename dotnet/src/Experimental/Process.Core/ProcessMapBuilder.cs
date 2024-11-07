﻿// Copyright (c) Microsoft. All rights reserved.
using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.SemanticKernel.Process.Models;

namespace Microsoft.SemanticKernel;

/// <summary>
/// Provides functionality to define a step that maps an enumerable input for parallel processing
/// targeting the provided operation and provides the resulting value as an enumerable parameter
/// with equivalent dimension as the input.
/// </summary>
public sealed class ProcessMapBuilder : ProcessStepBuilder
{
    internal readonly ProcessFunctionTargetBuilder _mapTarget;

    /// <summary>
    /// Initializes a new instance of the <see cref="ProcessMapBuilder"/> class.
    /// </summary>
    /// <param name="mapTarget">The target of the map operation.  May target a step or process</param>
    internal ProcessMapBuilder(ProcessFunctionTargetBuilder mapTarget)
        : base($"Map{mapTarget.Step.Name}")
    {
        this._mapTarget = mapTarget;
        this.MapOperation = this.CreateMapProcess(mapTarget);
    }

    /// <summary>
    /// Version of the map-step, used when saving the state of the step.
    /// </summary>
    public string Version { get; init; } = "v1";

    /// <summary>
    /// The map operation that will be executed for each element in the input.
    /// </summary>
    internal ProcessBuilder MapOperation { get; }

    /// <inheritdoc/>
    /// <remarks>
    /// Never called as the map is a proxy for the map operation and does not have a function target.
    /// </remarks>
    internal override Dictionary<string, KernelFunctionMetadata> GetFunctionMetadataMap()
    {
        throw new NotImplementedException($"{nameof(ProcessMapBuilder)}.{nameof(GetFunctionMetadataMap)} should never be invoked");
    }

    /// <inheritdoc/>
    internal override KernelProcessFunctionTarget ResolveFunctionTarget(string? functionName, string? parameterName)
    {
        return new KernelProcessFunctionTarget(this.Id, this._mapTarget.FunctionName, this._mapTarget.ParameterName);
    }

    /// <inheritdoc/>
    internal override KernelProcessStepInfo BuildStep(KernelProcessStepStateMetadata? stateMetadata = null)
    {
        // Build the edges first
        var builtEdges = this.Edges.ToDictionary(kvp => kvp.Key, kvp => kvp.Value.Select(e => e.Build()).ToList());

        KernelProcessMapState state = new(this.Name, this.Version, this.Id);
        return new KernelProcessMap(state, this.MapOperation.Build(), builtEdges);
    }

    private ProcessBuilder CreateMapProcess(ProcessFunctionTargetBuilder mapTarget)
    {
        if (mapTarget.Step is ProcessBuilder mapProcess)
        {
            if (string.IsNullOrWhiteSpace(mapTarget.TargetEventId))
            {
                throw new InvalidOperationException($"Invalid target for map: {this.Name}");
            }

            return CreateMapOperationFromProcess(mapProcess, mapTarget.TargetEventId!);
        }

        return CreateMapOperationFromStep(mapTarget);
    }

    private static ProcessBuilder CreateMapOperationFromProcess(ProcessBuilder mapProcess, string eventId)
    {
        ProcessBuilder transformBuilder = new($"One{mapProcess.Name}");

        var transformProcess = transformBuilder.AddStepFromProcess(mapProcess);
        transformBuilder
            .OnInputEvent(KernelProcessMap.MapEventId)
            .SendEventTo(transformProcess.WhereInputEventIs(eventId));

        return transformBuilder;
    }

    private static ProcessBuilder CreateMapOperationFromStep(ProcessFunctionTargetBuilder mapTarget)
    {
        ProcessBuilder transformBuilder = new($"One{mapTarget.Step.Name}");

        transformBuilder.AddStepFromBuilder(mapTarget.Step);
        transformBuilder
            .OnInputEvent(KernelProcessMap.MapEventId)
            .SendEventTo(mapTarget);

        return transformBuilder;
    }
}
