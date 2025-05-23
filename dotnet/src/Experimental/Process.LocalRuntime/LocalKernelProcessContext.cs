<<<<<<< HEAD
<<<<<<< HEAD
// Copyright (c) Microsoft. All rights reserved.
=======
﻿// Copyright (c) Microsoft. All rights reserved.
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
using System;
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
using System.Threading.Tasks;
using Microsoft.SemanticKernel.Process;

namespace Microsoft.SemanticKernel;

/// <summary>
/// Provides context and actions on a process that is running locally.
/// </summary>
public sealed class LocalKernelProcessContext : KernelProcessContext, System.IAsyncDisposable
{
    private readonly LocalProcess _localProcess;
    private readonly Kernel _kernel;

<<<<<<< HEAD
    internal LocalKernelProcessContext(KernelProcess process, Kernel kernel, ProcessEventProxy? filter = null)
<<<<<<< HEAD
    internal LocalKernelProcessContext(KernelProcess process, Kernel kernel, ProcessEventFilter? filter = null)
=======
    internal LocalKernelProcessContext(KernelProcess process, Kernel kernel, ProcessEventProxy? eventProxy = null)
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
=======
    internal LocalKernelProcessContext(KernelProcess process, Kernel kernel, ProcessEventProxy? eventProxy = null, IExternalKernelProcessMessageChannel? externalMessageChannel = null)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        Verify.NotNull(kernel, nameof(kernel));
        Verify.NotNull(process, nameof(process));
        Verify.NotNull(kernel, nameof(kernel));
        Verify.NotNullOrWhiteSpace(process.State?.Name);

        this._kernel = kernel;
        this._localProcess = new LocalProcess(
            process,
            kernel)
        {
            EventProxy = filter
        };
            EventFilter = filter,
            LoggerFactory = kernel.LoggerFactory,
        };
    }

    internal Task StartWithEventAsync(KernelProcessEvent? initialEvent, Kernel? kernel = null)
    {
        return this._localProcess.RunOnceAsync(initialEvent);
    }
        Verify.NotNull(process, nameof(process));
        Verify.NotNull(kernel, nameof(kernel));
        Verify.NotNullOrWhiteSpace(process.State?.Name);

        this._kernel = kernel;
        this._localProcess = new LocalProcess(process, kernel)
        {
            EventProxy = eventProxy,
            ExternalMessageChannel = externalMessageChannel,
        };
    }
        Verify.NotNull(process, nameof(process));
        Verify.NotNull(kernel, nameof(kernel));
        Verify.NotNullOrWhiteSpace(process.State?.Name);

        this._kernel = kernel;
        this._localProcess = new LocalProcess(process, kernel);
    }

    internal Task StartWithEventAsync(KernelProcessEvent initialEvent, Kernel? kernel = null) =>
        this._localProcess.RunOnceAsync(initialEvent, kernel);

    internal Task StartWithEventAsync(KernelProcessEvent initialEvent, Kernel? kernel = null) =>
        this._localProcess.RunOnceAsync(initialEvent, kernel);

    //internal RunUntilEndAsync(KernelProcessEvent initialEvent, Kernel? kernel = null, TimeSpan? timeout = null)
    //{

    //}

    /// <summary>
    /// Sends a message to the process.
    /// </summary>
    /// <param name="processEvent">The event to sent to the process.</param>
    /// <returns>A <see cref="Task"/></returns>
    public override Task SendEventAsync(KernelProcessEvent processEvent) =>
        this._localProcess.SendMessageAsync(processEvent);

    /// <summary>
    /// Stops the process.
    /// </summary>
    /// <returns>A <see cref="Task"/></returns>
    public override Task StopAsync() => this._localProcess.StopAsync();

    /// <summary>
    /// Gets a snapshot of the current state of the process.
    /// </summary>
    /// <returns>A <see cref="Task{T}"/> where T is <see cref="KernelProcess"/></returns>
    public override Task<KernelProcess> GetStateAsync() => this._localProcess.GetProcessInfoAsync();

    /// <summary>
    /// Disposes of the resources used by the process.
    /// </summary>
    public async ValueTask DisposeAsync()
    {
        await this._localProcess.DisposeAsync().ConfigureAwait(false);
    }

    /// <inheritdoc/>
    public override Task<IExternalKernelProcessMessageChannel?> GetExternalMessageChannelAsync()
    {
        return Task.FromResult(this._localProcess.ExternalMessageChannel);
    }

    /// <inheritdoc/>
    public override Task<string> GetProcessIdAsync() => Task.FromResult(this._localProcess.Id);
}
