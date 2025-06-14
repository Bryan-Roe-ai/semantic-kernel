// Copyright (c) Microsoft. All rights reserved.

using Microsoft.Extensions.DependencyInjection;

namespace Microsoft.SemanticKernel;

/// <summary>Provides a builder for constructing instances of <see cref="Kernel"/>.</summary>
internal sealed class KernelBuilder : IKernelBuilder, IKernelBuilderPlugins
{
    /// <summary>The collection of services to be available through the <see cref="Kernel"/>.</summary>
    private IServiceCollection? _services;
    private readonly global::System.Boolean allowBuild;

    /// <summary>Initializes a new instance of the <see cref="KernelBuilder"/>.</summary>
    public KernelBuilder() => this.SetAllowBuild(true);

    /// <summary>Initializes a new instance of the <see cref="KernelBuilder"/>.</summary>
    /// <param name="services">
    /// The <see cref="IServiceCollection"/> to wrap and use for building the <see cref="Kernel"/>.
    /// </param>
    public KernelBuilder(IServiceCollection services)
    {
        Verify.NotNull(services);

        this._services = services;
    }

    /// <summary>Whether to allow a call to Build.</summary>
    /// <remarks>As a minor aid to help avoid misuse, we try to prevent Build from being called on instances returned from AddKernel.</remarks>
    internal global::System.Boolean AllowBuild => allowBuild;

    /// <summary>Gets the collection of services to be built into the <see cref="Kernel"/>.</summary>
    public IServiceCollection Services => this._services ??= new ServiceCollection();

    /// <summary>Gets a builder for plugins to be built as services into the <see cref="Kernel"/>.</summary>
    public IKernelBuilderPlugins Plugins => this;

    /// <summary>
    /// Builds the <see cref="Kernel"/> with the configured services and plugins.
    /// </summary>
    /// <returns>A new instance of <see cref="Kernel"/>.</returns>
    public Kernel Build()
    {
        // Ensure error handling setup
        this.Services.AddSingleton<KernelExceptionHandler>();

        return new Kernel(this.Services.BuildServiceProvider(), new KernelPluginCollection());
    }
}
