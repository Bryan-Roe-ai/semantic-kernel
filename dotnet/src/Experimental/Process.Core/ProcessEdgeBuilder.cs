<<<<<<< HEAD
=======
// Copyright (c) Microsoft. All rights reserved.

>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
using System;

namespace Microsoft.SemanticKernel;

/// <summary>
/// Provides functionality for incrementally defining a process edge.
/// </summary>
public sealed class ProcessEdgeBuilder : ProcessStepEdgeBuilder
{
<<<<<<< HEAD
    private readonly ProcessBuilder _source;
    private readonly string _eventId;
    internal ProcessFunctionTargetBuilder? Target { get; set; }

    /// <summary>
    /// The event Id that the edge fires on.
    /// </summary>
    internal string EventId { get; }

=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// <summary>
    /// The source step of the edge.
    /// </summary>
    internal new ProcessBuilder Source { get; }

    /// <summary>
    /// Initializes a new instance of the <see cref="ProcessEdgeBuilder"/> class.
    /// </summary>
    /// <param name="source">The source step.</param>
    /// <param name="eventId">The Id of the event.</param>
    internal ProcessEdgeBuilder(ProcessBuilder source, string eventId) : base(source, eventId, eventId)
    {
<<<<<<< HEAD
        this._source = source;
        this._eventId = eventId;
        Verify.NotNull(source, nameof(source));
        Verify.NotNullOrWhiteSpace(eventId, nameof(eventId));

=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        this.Source = source;
    }

    /// <summary>
    /// Sends the output of the source step to the specified target when the associated event fires.
    /// </summary>
    /// <param name="outputTarget">The output target.</param>
    public void SendEventTo(ProcessStepEdgeBuilder outputTarget)
    {
        this._source.LinkTo(this._eventId, outputTarget);
    }

    public ProcessEdgeBuilder SendEventTo(ProcessFunctionTargetBuilder target)
    {
        return this.SendEventTo_Int(target as ProcessTargetBuilder);
    }

    /// <summary>
    /// Sends the output of the source step to the specified target when the associated event fires.
    /// </summary>
    public new ProcessEdgeBuilder SendEventTo(ProcessTargetBuilder target)
    {
        return this.SendEventTo_Int(target as ProcessTargetBuilder);
    }

    /// <summary>
    /// Sends the output of the source step to the specified target when the associated event fires.
    /// </summary>
    internal ProcessEdgeBuilder SendEventTo_Int(ProcessTargetBuilder target)
    {
        if (this.Target is not null)
        {
            throw new InvalidOperationException("An output target has already been set.");
        }

        this.Target = target;
        ProcessStepEdgeBuilder edgeBuilder = new(this.Source, this.EventData.EventId, this.EventData.EventId) { Target = this.Target };
        this.Source.LinkTo(this.EventData.EventId, edgeBuilder);

        return new ProcessEdgeBuilder(this.Source, this.EventData.EventId);
    }
}
