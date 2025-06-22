// Copyright (c) Microsoft. All rights reserved.

using System;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;

namespace SemanticKernel.AutoMode;

/// <summary>
/// Extension methods for configuring ExtendedAutoModeAgent services.
/// </summary>
public static class ExtendedAutoModeServiceExtensions
{
    /// <summary>
    /// Adds ExtendedAutoModeAgent services to the dependency injection container.
    /// </summary>
    /// <param name="services">The service collection.</param>
    /// <param name="configureOptions">Action to configure the auto mode options.</param>
    /// <returns>The service collection for chaining.</returns>
    public static IServiceCollection AddExtendedAutoMode(
        this IServiceCollection services,
        Action<ExtendedAutoModeOptions>? configureOptions = null)
    {
        var options = new ExtendedAutoModeOptions();
        configureOptions?.Invoke(options);

        services.AddSingleton(options);
        services.AddSingleton<ExtendedAutoModeAgent>();
        services.AddHostedService<ExtendedAutoModeHostedService>();

        return services;
    }

    /// <summary>
    /// Adds ExtendedAutoModeAgent services to the dependency injection container with configuration.
    /// </summary>
    /// <param name="services">The service collection.</param>
    /// <param name="configuration">The configuration section.</param>
    /// <returns>The service collection for chaining.</returns>
    public static IServiceCollection AddExtendedAutoMode(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.Configure<ExtendedAutoModeOptions>(configuration);
        services.AddSingleton<ExtendedAutoModeAgent>();
        services.AddHostedService<ExtendedAutoModeHostedService>();

        return services;
    }
}

/// <summary>
/// Builder for configuring ExtendedAutoModeAgent.
/// </summary>
public class ExtendedAutoModeBuilder
{
    private readonly IServiceCollection _services;
    private readonly ExtendedAutoModeOptions _options;

    /// <summary>
    /// Initializes a new instance of the <see cref="ExtendedAutoModeBuilder"/> class.
    /// </summary>
    /// <param name="services">The service collection.</param>
    public ExtendedAutoModeBuilder(IServiceCollection services)
    {
        _services = services ?? throw new ArgumentNullException(nameof(services));
        _options = new ExtendedAutoModeOptions();
    }

    /// <summary>
    /// Configures the maximum number of concurrent operations.
    /// </summary>
    /// <param name="maxConcurrentOperations">The maximum number of concurrent operations.</param>
    /// <returns>The builder for chaining.</returns>
    public ExtendedAutoModeBuilder WithMaxConcurrentOperations(int maxConcurrentOperations)
    {
        if (maxConcurrentOperations <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(maxConcurrentOperations), "Must be greater than zero");
        }

        _options.MaxConcurrentOperations = maxConcurrentOperations;
        return this;
    }

    /// <summary>
    /// Configures the base operation delay.
    /// </summary>
    /// <param name="delayMs">The base delay between operations in milliseconds.</param>
    /// <returns>The builder for chaining.</returns>
    public ExtendedAutoModeBuilder WithBaseOperationDelay(int delayMs)
    {
        if (delayMs < 0)
        {
            throw new ArgumentOutOfRangeException(nameof(delayMs), "Must be non-negative");
        }

        _options.BaseOperationDelayMs = delayMs;
        return this;
    }

    /// <summary>
    /// Configures the health check interval.
    /// </summary>
    /// <param name="intervalMinutes">The health check interval in minutes.</param>
    /// <returns>The builder for chaining.</returns>
    public ExtendedAutoModeBuilder WithHealthCheckInterval(int intervalMinutes)
    {
        if (intervalMinutes <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(intervalMinutes), "Must be greater than zero");
        }

        _options.HealthCheckIntervalMinutes = intervalMinutes;
        return this;
    }

    /// <summary>
    /// Configures the maintenance interval.
    /// </summary>
    /// <param name="intervalHours">The maintenance interval in hours.</param>
    /// <returns>The builder for chaining.</returns>
    public ExtendedAutoModeBuilder WithMaintenanceInterval(int intervalHours)
    {
        if (intervalHours <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(intervalHours), "Must be greater than zero");
        }

        _options.MaintenanceIntervalHours = intervalHours;
        return this;
    }

    /// <summary>
    /// Configures memory usage limits.
    /// </summary>
    /// <param name="maxMemoryMB">The maximum memory usage in MB before warnings.</param>
    /// <returns>The builder for chaining.</returns>
    public ExtendedAutoModeBuilder WithMaxMemoryUsage(long maxMemoryMB)
    {
        if (maxMemoryMB <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(maxMemoryMB), "Must be greater than zero");
        }

        _options.MaxMemoryUsageMB = maxMemoryMB;
        return this;
    }

    /// <summary>
    /// Configures the maximum acceptable error rate.
    /// </summary>
    /// <param name="maxErrorRate">The maximum error rate (0.0 to 1.0).</param>
    /// <returns>The builder for chaining.</returns>
    public ExtendedAutoModeBuilder WithMaxErrorRate(double maxErrorRate)
    {
        if (maxErrorRate < 0.0 || maxErrorRate > 1.0)
        {
            throw new ArgumentOutOfRangeException(nameof(maxErrorRate), "Must be between 0.0 and 1.0");
        }

        _options.MaxErrorRate = maxErrorRate;
        return this;
    }

    /// <summary>
    /// Configures the state retention time.
    /// </summary>
    /// <param name="retentionHours">The state retention time in hours.</param>
    /// <returns>The builder for chaining.</returns>
    public ExtendedAutoModeBuilder WithStateRetention(int retentionHours)
    {
        if (retentionHours <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(retentionHours), "Must be greater than zero");
        }

        _options.StateRetentionHours = retentionHours;
        return this;
    }

    /// <summary>
    /// Configures the state directory.
    /// </summary>
    /// <param name="stateDirectory">The directory for storing state files.</param>
    /// <returns>The builder for chaining.</returns>
    public ExtendedAutoModeBuilder WithStateDirectory(string stateDirectory)
    {
        if (string.IsNullOrWhiteSpace(stateDirectory))
        {
            throw new ArgumentException("State directory cannot be null or empty", nameof(stateDirectory));
        }

        _options.StateDirectory = stateDirectory;
        return this;
    }

    /// <summary>
    /// Builds the ExtendedAutoModeAgent with the configured options.
    /// </summary>
    /// <returns>The service collection for further configuration.</returns>
    public IServiceCollection Build()
    {
        _services.AddSingleton(_options);
        _services.AddSingleton<ExtendedAutoModeAgent>();
        _services.AddHostedService<ExtendedAutoModeHostedService>();

        return _services;
    }
}

/// <summary>
/// Factory for creating ExtendedAutoModeAgent instances.
/// </summary>
public class ExtendedAutoModeAgentFactory
{
    private readonly IServiceProvider _serviceProvider;

    /// <summary>
    /// Initializes a new instance of the <see cref="ExtendedAutoModeAgentFactory"/> class.
    /// </summary>
    /// <param name="serviceProvider">The service provider.</param>
    public ExtendedAutoModeAgentFactory(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider ?? throw new ArgumentNullException(nameof(serviceProvider));
    }

    /// <summary>
    /// Creates a new ExtendedAutoModeAgent instance.
    /// </summary>
    /// <param name="kernel">The semantic kernel instance.</param>
    /// <param name="options">Optional configuration options.</param>
    /// <returns>A new ExtendedAutoModeAgent instance.</returns>
    public ExtendedAutoModeAgent CreateAgent(Kernel kernel, ExtendedAutoModeOptions? options = null)
    {
        var logger = _serviceProvider.GetRequiredService<ILogger<ExtendedAutoModeAgent>>();
        var configuration = _serviceProvider.GetRequiredService<IConfiguration>();
        
        options ??= _serviceProvider.GetService<ExtendedAutoModeOptions>() ?? new ExtendedAutoModeOptions();

        return new ExtendedAutoModeAgent(kernel, logger, configuration, options);
    }
}
