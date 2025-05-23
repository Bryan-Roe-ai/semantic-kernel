// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Linq;

namespace Microsoft.SemanticKernel;

/// <summary>
/// Contains information about a Step in a Process including it's state and edges.
/// </summary>
public class KernelProcessStepInfo
{
public record KernelProcessStepInfo
{
    private KernelProcessStepState _state;

    /// <summary>
    /// A mapping of output edges from the Step using the .
    /// </summary>
    private readonly Dictionary<string, List<KernelProcessEdge>> _outputEdges;

    /// <summary>
    /// The type of the inner step.
    /// </summary>
    internal Type InnerStepType { get; }

    /// <summary>
    /// A read-only collection of event Ids that this Step can emit.
    /// </summary>
    public IReadOnlyCollection<string> EventIds => this._outputEdges.Keys.ToArray();
    public Type InnerStepType { get; }

    /// <summary>
    /// The state of the Step.
    /// </summary>
    public KernelProcessStepState State { get; }

    /// <summary>
    /// Retrieves the output edges for a given event Id. Returns an empty list if the event Id is not found.
    /// </summary>
    /// <param name="eventId">The Id of an event.</param>
    /// <returns>An <see cref="IReadOnlyCollection{T}"/> where T is <see cref="KernelProcessEdge"/></returns>
    protected IReadOnlyCollection<KernelProcessEdge> GetOutputEdges(string eventId)
    {
        if (this._outputEdges.TryGetValue(eventId, out List<KernelProcessEdge>? edges))
        {
            return edges.AsReadOnly();
        }

        return [];
    }

    /// <summary>
    public KernelProcessStepState State
    {
        get => this._state;
        init
        {
            Verify.NotNull(value);
            this._state = value;
        }
    }

    /// <summary>
    /// The semantic description of the Step. This is intended to be human and AI readable and is not required to be unique.
    /// </summary>
    public string? Description { get; init; } = null;

    /// <summary>
    /// A read-only dictionary of output edges from the Step.
    /// </summary>
    public IReadOnlyDictionary<string, IReadOnlyCollection<KernelProcessEdge>> Edges =>
        this._outputEdges.ToDictionary(kvp => kvp.Key, kvp => (IReadOnlyCollection<KernelProcessEdge>)kvp.Value.AsReadOnly());

    /// <summary>
    /// A dictionary of input mappings for the grouped edges.
    /// </summary>
    public IReadOnlyDictionary<string, KernelProcessEdgeGroup>? IncomingEdgeGroups { get; }

    /// <summary>
    /// Initializes a new instance of the <see cref="KernelProcessStepInfo"/> class.
    /// </summary>
    public KernelProcessStepInfo(Type innerStepType, KernelProcessStepState state, Dictionary<string, List<KernelProcessEdge>> edges, Dictionary<string, KernelProcessEdgeGroup>? incomingEdgeGroups = null)
    {
        Verify.NotNull(innerStepType);
        Verify.NotNull(edges);
        Verify.NotNull(state);

        this.InnerStepType = innerStepType;
<<<<<<< main
        this._outputEdges = edges;
        this.State = state;
        this.Edges = edges.ToDictionary(kvp => kvp.Key, kvp => (IReadOnlyCollection<KernelProcessEdge>)kvp.Value.AsReadOnly());
=======
        this._outputEdges = edges;
        this.State = state;
>>>>>>> origin/main
        this._state = state;
        this.IncomingEdgeGroups = incomingEdgeGroups;

        // Register the state as a know type for the DataContractSerialization used by Dapr.
        KernelProcessState.RegisterDerivedType(state.GetType());
    }
}
