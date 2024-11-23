// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Generic;
using System.Threading.Tasks;
using Dapr.Actors;

namespace Microsoft.SemanticKernel;

/// <summary>
/// An interface for a buffer of <see cref="DaprEvent"/>s.
/// </summary>
public interface IEventBuffer : IActor
{
    /// <summary>
    /// Enqueues an external event.
    /// </summary>
    /// <param name="stepEvent">The event to enqueue as JSON.</param>
    /// <returns>A <see cref="Task"/></returns>
<<<<<<< HEAD
    Task EnqueueAsync(DaprEvent stepEvent);
=======
    Task EnqueueAsync(string stepEvent);
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377

    /// <summary>
    /// Dequeues all external events.
    /// </summary>
<<<<<<< HEAD
    /// <returns>A <see cref="List{T}"/> where T is <see cref="DaprEvent"/></returns>
    Task<List<DaprEvent>> DequeueAllAsync();
    /// <returns>A <see cref="List{T}"/> where T is <see cref="ProcessEvent"/></returns>
    Task<IList<ProcessEvent>> DequeueAllAsync();
=======
    /// <returns>A <see cref="IList{T}"/> where T is the JSON representation of a <see cref="ProcessEvent"/></returns>
    Task<IList<string>> DequeueAllAsync();
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
}
