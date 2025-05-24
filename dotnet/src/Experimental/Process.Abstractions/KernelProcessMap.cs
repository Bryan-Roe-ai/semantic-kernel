// Copyright (c) Microsoft. All rights reserved.
using System.Collections.Generic;

namespace Microsoft.SemanticKernel;

/// <summary>
/// A serializable representation of a ProcessMap.
/// </summary>
public sealed record KernelProcessMap : KernelProcessStepInfo
{
    /// <summary>
<<<<<<< HEAD
    /// Event Id used internally to initiate the map operation.
    /// </summary>
    public const string MapEventId = "StartMap";

    /// <summary>
    /// The map operation.
    /// </summary>
    public KernelProcessStepInfo Operation { get; }
    public KernelProcess Operation { get; }
=======
    /// The map operation.
    /// </summary>
    public KernelProcessStepInfo Operation { get; }
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377

    /// <summary>
    /// Creates a new instance of the <see cref="KernelProcess"/> class.
    /// </summary>
    /// <param name="state">The process state.</param>
    /// <param name="operation">The map operation.</param>
    /// <param name="edges">The edges for the map.</param>
    public KernelProcessMap(KernelProcessMapState state, KernelProcessStepInfo operation, Dictionary<string, List<KernelProcessEdge>> edges)
<<<<<<< HEAD
    public KernelProcessMap(KernelProcessMapState state, KernelProcess operation, Dictionary<string, List<KernelProcessEdge>> edges)
=======
    public KernelProcessMap(KernelProcessMapState state, KernelProcessStepInfo operation, Dictionary<string, List<KernelProcessEdge>> edges)
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
        : base(typeof(KernelProcessMap), state, edges)
    {
        Verify.NotNull(operation, nameof(operation));
        Verify.NotNullOrWhiteSpace(state.Name, $"{nameof(state)}.{nameof(KernelProcessMapState.Name)}");
        Verify.NotNullOrWhiteSpace(state.Id, $"{nameof(state)}.{nameof(KernelProcessMapState.Id)}");

        this.Operation = operation;
    }
}
