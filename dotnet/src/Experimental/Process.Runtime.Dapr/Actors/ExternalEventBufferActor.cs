// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Generic;
using System.Threading.Tasks;
using Dapr.Actors.Runtime;

namespace Microsoft.SemanticKernel;

/// <summary>
/// An actor that represents an external event queue.
/// </summary>
internal class ExternalEventBufferActor : Actor, IExternalEventBuffer
{
<<<<<<< HEAD
    private const string EventQueueState = "DaprExternalEventBufferState";
    private Queue<KernelProcessEvent>? _queue = new();
=======
    private List<string> _queue = [];
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377

    /// <summary>
    /// Required constructor for Dapr Actor.
    /// </summary>
    /// <param name="host">The actor host.</param>
    public ExternalEventBufferActor(ActorHost host) : base(host)
    {
    }

    /// <summary>
    /// Dequeues an event.
    /// </summary>
<<<<<<< HEAD
    /// <returns>A <see cref="List{T}"/> where T is <see cref="DaprEvent"/></returns>
    public async Task<List<KernelProcessEvent>> DequeueAllAsync()
=======
    /// <returns>A <see cref="List{T}"/> where T is <see cref="ProcessEvent"/></returns>
    public async Task<IList<string>> DequeueAllAsync()
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
    {
        // Dequeue and clear the queue.
        string[] items = [.. this._queue];
        this._queue!.Clear();

        // Save the state.
        await this.StateManager.SetStateAsync(EventQueueState, this._queue).ConfigureAwait(false);
        await this.StateManager.SaveStateAsync().ConfigureAwait(false);

        return items;
    }

    public async Task EnqueueAsync(string externalEvent)
    {
        this._queue.Add(externalEvent);

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
        var eventQueueState = await this.StateManager.TryGetStateAsync<Queue<KernelProcessEvent>>(EventQueueState).ConfigureAwait(false);
=======
        var eventQueueState = await this.StateManager.TryGetStateAsync<List<string>>(ActorStateKeys.ExternalEventQueueState).ConfigureAwait(false);
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
        if (eventQueueState.HasValue)
        {
            this._queue = [.. eventQueueState.Value];
        }
        else
        {
            this._queue = [];
        }
    }
}
