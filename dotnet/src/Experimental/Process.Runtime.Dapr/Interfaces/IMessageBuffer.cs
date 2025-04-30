// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Generic;
using System.Threading.Tasks;
using Dapr.Actors;

namespace Microsoft.SemanticKernel;

/// <summary>
/// An interface for a buffer of <see cref="DaprMessage"/>s.
/// </summary>
public interface IMessageBuffer : IActor
{
    /// <summary>
    /// Enqueues an external event.
    /// </summary>
    /// <param name="message">The message to enqueue as JSON.</param>
    /// <returns>A <see cref="Task"/></returns>
<<<<<<< HEAD
    Task EnqueueAsync(DaprMessage message);
=======
    Task EnqueueAsync(string message);
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377

    /// <summary>
    /// Dequeues all external events.
    /// </summary>
<<<<<<< HEAD
    /// <returns>A <see cref="List{T}"/> where T is <see cref="DaprMessage"/></returns>
    Task<List<DaprMessage>> DequeueAllAsync();
    /// <returns>A <see cref="List{T}"/> where T is <see cref="ProcessMessage"/></returns>
    Task<IList<ProcessMessage>> DequeueAllAsync();
=======
    /// <returns>A <see cref="IList{T}"/> where T is the JSON representation of a <see cref="ProcessMessage"/></returns>
    Task<IList<string>> DequeueAllAsync();
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
}
