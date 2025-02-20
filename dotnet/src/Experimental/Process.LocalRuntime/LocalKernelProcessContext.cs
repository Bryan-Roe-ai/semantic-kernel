<<<<<<< HEAD
// Copyright (c) Microsoft. All rights reserved.
=======
﻿// Copyright (c) Microsoft. All rights reserved.
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
using System;
using System.Threading.Tasks;
using Microsoft.SemanticKernel.Process;

namespace Microsoft.SemanticKernel;

/// <summary>
/// Provides context and actions on a process that is running locally.
/// </summary>
public sealed class LocalKernelProcessContext : KernelProcessContext, IDisposable
{
    private readonly LocalProcess _localProcess;
    private readonly Kernel _kernel;

    internal LocalKernelProcessContext(KernelProcess process, Kernel kernel, ProcessEventProxy? filter = null)
<<<<<<< HEAD
    internal LocalKernelProcessContext(KernelProcess process, Kernel kernel, ProcessEventFilter? filter = null)
=======
    internal LocalKernelProcessContext(KernelProcess process, Kernel kernel, ProcessEventProxy? eventProxy = null)
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
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
        this._localProcess = new LocalProcess(
            process,
            kernel)
        {
            EventProxy = eventProxy
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
    public void Dispose() => this._localProcess.Dispose();
}
