// Copyright (c) Microsoft. All rights reserved.
using System.Collections.Generic;
using System.Runtime.Serialization;

namespace Microsoft.SemanticKernel.Process.Runtime;

/// <summary>
/// Represents a message used in a process runtime.
/// </summary>
/// <remarks>
/// Initializes a new instance of the <see cref="ProcessMessage"/> class.
/// </remarks>
/// <param name="SourceId">The source identifier of the message.</param>
/// <param name="DestinationId">The destination identifier of the message.</param>
/// <param name="FunctionName">The name of the function associated with the message.</param>
/// <param name="Values">The dictionary of values associated with the message.</param>
/// <param name="writtenToThread"></param>
[KnownType(typeof(KernelProcessError))]
[KnownType(typeof(KernelProcessProxyMessage))]
public record ProcessMessage(
    string SourceId,
    string DestinationId,
    string FunctionName,
    Dictionary<string, object?> Values, string? writtenToThread = null)
{
    /// <summary>
    /// Id of the the event that triggered the process message
    /// </summary>
    public string? SourceEventId { get; init; }

    /// <summary>
    /// The Id of the target event. This may be null if the message is not targeting a sub-process.
    /// </summary>
    public string? TargetEventId { get; init; }

    /// <summary>
    /// The data associated with the target event. This may be null if the message is not targeting a sub-process.
    /// </summary>
    public object? TargetEventData { get; init; }

    /// <summary>
    /// The Id of the group that the message belongs to. This may be null if the message is not part of a group.
    /// </summary>
    public string? GroupId { get; init; }

    /// <summary>
    /// An evaluation string that will be evaluated to determine the thread to run on.
    /// </summary>
    public string? ThreadEval { get; init; }

    /// <summary>
    /// An evaluation string that will be evaluated to determine the messages to send to the target.
    /// </summary>
    public List<string>? MessagesInEval { get; init; }

    /// <summary>
    /// An evaluation string that will be evaluated to determine the inputs to send to the target.
    /// </summary>
    public Dictionary<string, string>? InputEvals { get; init; }
}
