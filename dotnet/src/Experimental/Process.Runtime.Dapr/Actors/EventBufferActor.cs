// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Generic;
using System.Threading.Tasks;
using Dapr.Actors.Runtime;

namespace Microsoft.SemanticKernel;

/// <summary>
/// An actor that represents an event queue.
/// </summary>
internal class EventBufferActor : Actor, IEventBuffer
{
<<<<<<< HEAD
    private const string EventQueueState = "DaprEventBufferState";
    private Queue<DaprEvent>? _queue = new();
=======
    private List<string> _queue = [];
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377

    /// <summary>
    /// Required constructor for Dapr Actor.
    /// </summary>
    /// <param name="host">The actor host.</param>
    public EventBufferActor(ActorHost host) : base(host)
    {
    }

    /// <summary>
    /// Dequeues an event.
    /// </summary>
    /// <returns>A <see cref="List{T}"/> where T is <see cref="DaprEvent"/></returns>
    public async Task<List<DaprEvent>> DequeueAllAsync()
    /// <returns>A <see cref="List{T}"/> where T is <see cref="ProcessEvent"/></returns>
    public async Task<IList<string>> DequeueAllAsync()
    {
        // Dequeue and clear the queue.
        string[] items = [.. this._queue];
        this._queue.Clear();

        // Save the state.
        await this.StateManager.SetStateAsync(EventQueueState, this._queue).ConfigureAwait(false);
        await this.StateManager.SaveStateAsync().ConfigureAwait(false);

        return items;
    }

<<<<<<< HEAD
    public async Task EnqueueAsync(DaprEvent stepEvent)
=======
    public async Task EnqueueAsync(string stepEvent)
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
    {
        this._queue.Add(stepEvent);

        // Save the state.
        await this.StateManager.SetStateAsync(EventQueueState, this._queue).ConfigureAwait(false);
        await this.StateManager.SaveStateAsync().ConfigureAwait(false);
    }

    /// <summary>
    /// Called when the actor is activated. Used to initialize the state of the actor.
    /// </summary>
    /// <returns>A <see cref="Task"/></returns>
    protected override async Task OnActivateAsync()
    {
<<<<<<< HEAD
        var eventQueueState = await this.StateManager.TryGetStateAsync<Queue<DaprEvent>>(EventQueueState).ConfigureAwait(false);
=======
        var eventQueueState = await this.StateManager.TryGetStateAsync<List<string>>(ActorStateKeys.EventQueueState).ConfigureAwait(false);
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
        if (eventQueueState.HasValue)
        {
            this._queue = eventQueueState.Value;
        }
        else
        {
<<<<<<< HEAD
            this._queue = new Queue<DaprEvent>();
=======
            this._queue = [];
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
        }
    }
}
