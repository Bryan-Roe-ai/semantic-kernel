// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Microsoft.SemanticKernel;

namespace SemanticKernel.AutoMode;

/// <summary>
/// Hosted service for running ExtendedAutoModeAgent as a background service.
/// </summary>
public class ExtendedAutoModeHostedService : BackgroundService
{
    private readonly ExtendedAutoModeAgent _agent;
    private readonly ILogger<ExtendedAutoModeHostedService> _logger;
    private readonly ExtendedAutoModeOptions _options;

    /// <summary>
    /// Initializes a new instance of the <see cref="ExtendedAutoModeHostedService"/> class.
    /// </summary>
    /// <param name="agent">The ExtendedAutoModeAgent instance.</param>
    /// <param name="logger">Logger for diagnostics.</param>
    /// <param name="options">Configuration options.</param>
    public ExtendedAutoModeHostedService(
        ExtendedAutoModeAgent agent,
        ILogger<ExtendedAutoModeHostedService> logger,
        IOptions<ExtendedAutoModeOptions> options)
    {
        _agent = agent ?? throw new ArgumentNullException(nameof(agent));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _options = options?.Value ?? throw new ArgumentNullException(nameof(options));
    }

    /// <summary>
    /// Executes the background service.
    /// </summary>
    /// <param name="stoppingToken">Cancellation token for stopping the service.</param>
    /// <returns>A task representing the asynchronous operation.</returns>
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("ExtendedAutoModeHostedService starting");

        try
        {
            await _agent.StartAsync(stoppingToken);
        }
        catch (OperationCanceledException)
        {
            _logger.LogInformation("ExtendedAutoModeHostedService was cancelled");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "ExtendedAutoModeHostedService encountered an error");
            throw;
        }
    }

    /// <summary>
    /// Stops the background service.
    /// </summary>
    /// <param name="cancellationToken">Cancellation token for the stop operation.</param>
    /// <returns>A task representing the asynchronous operation.</returns>
    public override async Task StopAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("ExtendedAutoModeHostedService stopping");

        try
        {
            await _agent.StopAsync();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error stopping ExtendedAutoModeAgent");
        }

        await base.StopAsync(cancellationToken);
        
        _logger.LogInformation("ExtendedAutoModeHostedService stopped");
    }

    /// <summary>
    /// Disposes the hosted service.
    /// </summary>
    public override void Dispose()
    {
        try
        {
            _agent?.Dispose();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error disposing ExtendedAutoModeAgent");
        }

        base.Dispose();
    }
}
