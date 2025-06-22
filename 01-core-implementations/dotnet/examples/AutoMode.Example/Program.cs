// Copyright (c) Microsoft. All rights reserved.

using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using SemanticKernel.AutoMode;
using System.ComponentModel;

namespace SemanticKernel.AutoMode.Examples;

/// <summary>
/// Example console application demonstrating Extended Auto Mode usage.
/// </summary>
internal class Program
{
    /// <summary>
    /// Entry point for the example application.
    /// </summary>
    /// <param name="args">Command line arguments.</param>
    /// <returns>Exit code.</returns>
    public static async Task<int> Main(string[] args)
    {
        try
        {
            // Create and configure the host
            var host = CreateHostBuilder(args).Build();

            // Run the application
            Console.WriteLine("Starting Semantic Kernel Extended Auto Mode Example...");
            Console.WriteLine("Press Ctrl+C to stop gracefully.");

            await host.RunAsync();

            return 0;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Application failed: {ex.Message}");
            return 1;
        }
    }

    /// <summary>
    /// Creates and configures the host builder.
    /// </summary>
    /// <param name="args">Command line arguments.</param>
    /// <returns>The configured host builder.</returns>
    private static IHostBuilder CreateHostBuilder(string[] args) =>
        Host.CreateDefaultBuilder(args)
            .ConfigureAppConfiguration((context, config) =>
            {
                // Add configuration sources
                config.AddJsonFile("appsettings.json", optional: true, reloadOnChange: true)
                      .AddJsonFile($"appsettings.{context.HostingEnvironment.EnvironmentName}.json", optional: true)
                      .AddEnvironmentVariables()
                      .AddCommandLine(args);
            })
            .ConfigureLogging((context, logging) =>
            {
                logging.ClearProviders()
                       .AddConsole()
                       .AddConfiguration(context.Configuration.GetSection("Logging"));
            })
            .ConfigureServices((context, services) =>
            {
                // Configure Semantic Kernel
                services.AddSingleton<Kernel>(serviceProvider =>
                {
                    var configuration = serviceProvider.GetRequiredService<IConfiguration>();
                    var loggerFactory = serviceProvider.GetRequiredService<ILoggerFactory>();

                    var kernelBuilder = Kernel.CreateBuilder()
                        .AddOpenAIChatCompletion(
                            configuration["OpenAI:ModelId"] ?? "gpt-3.5-turbo",
                            configuration["OpenAI:ApiKey"] ?? throw new InvalidOperationException("OpenAI API key not configured"))
                        .Build();

                    // Add example plugins
                    kernelBuilder.Plugins.AddFromType<ExamplePlugin>();

                    return kernelBuilder;
                });

                // Configure Extended Auto Mode
                services.AddExtendedAutoMode(context.Configuration.GetSection("ExtendedAutoMode"));

                // Add status monitoring service
                services.AddHostedService<StatusMonitoringService>();
            });
}

/// <summary>
/// Example plugin for demonstration purposes.
/// </summary>
public class ExamplePlugin
{
    /// <summary>
    /// Example function that simulates processing.
    /// </summary>
    /// <param name="input">Input text to process.</param>
    /// <returns>Processed output.</returns>
    [KernelFunction]
    [Description("Processes input text and returns a modified version")]
    public string ProcessText(
        [Description("Input text to process")] string input)
    {
        // Simulate some processing
        Thread.Sleep(Random.Shared.Next(50, 200));

        return $"Processed: {input} (at {DateTime.UtcNow:yyyy-MM-dd HH:mm:ss} UTC)";
    }

    /// <summary>
    /// Example function that performs a calculation.
    /// </summary>
    /// <param name="x">First number.</param>
    /// <param name="y">Second number.</param>
    /// <returns>Sum of the numbers.</returns>
    [KernelFunction]
    [Description("Adds two numbers together")]
    public double Add(
        [Description("First number")] double x,
        [Description("Second number")] double y)
    {
        return x + y;
    }

    /// <summary>
    /// Example function that retrieves current time.
    /// </summary>
    /// <returns>Current UTC time.</returns>
    [KernelFunction]
    [Description("Gets the current UTC time")]
    public string GetCurrentTime()
    {
        return DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss UTC");
    }
}

/// <summary>
/// Background service that monitors the Extended Auto Mode status.
/// </summary>
public class StatusMonitoringService : BackgroundService
{
    private readonly ExtendedAutoModeAgent _agent;
    private readonly ILogger<StatusMonitoringService> _logger;

    /// <summary>
    /// Initializes a new instance of the <see cref="StatusMonitoringService"/> class.
    /// </summary>
    /// <param name="agent">The Extended Auto Mode agent.</param>
    /// <param name="logger">Logger for diagnostics.</param>
    public StatusMonitoringService(ExtendedAutoModeAgent agent, ILogger<StatusMonitoringService> logger)
    {
        _agent = agent ?? throw new ArgumentNullException(nameof(agent));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }

    /// <summary>
    /// Executes the background monitoring service.
    /// </summary>
    /// <param name="stoppingToken">Cancellation token for stopping the service.</param>
    /// <returns>A task representing the asynchronous operation.</returns>
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Status monitoring service started");

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                var status = _agent.GetStatus();

                // Log detailed status every 30 seconds
                _logger.LogInformation(
                    "Extended Auto Mode Status - Running: {IsRunning}, Uptime: {Uptime}, " +
                    "Operations: {OperationCount}, Errors: {ErrorCount}, Error Rate: {ErrorRate:P2}, " +
                    "Memory: {MemoryUsageMB}MB, State Entries: {StateCount}",
                    status.IsRunning,
                    status.Uptime,
                    status.OperationCount,
                    status.ErrorCount,
                    status.ErrorRate,
                    status.MemoryUsageMB,
                    status.StateCount);

                // Display simplified status to console
                Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Status: {(status.IsRunning ? "Running" : "Stopped")} | " +
                                $"Uptime: {status.Uptime:dd\\.hh\\:mm\\:ss} | " +
                                $"Ops: {status.OperationCount} | " +
                                $"Errors: {status.ErrorCount} | " +
                                $"Memory: {status.MemoryUsageMB}MB");

                await Task.Delay(TimeSpan.FromSeconds(30), stoppingToken);
            }
            catch (OperationCanceledException)
            {
                break;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in status monitoring service");
                await Task.Delay(TimeSpan.FromSeconds(5), stoppingToken);
            }
        }

        _logger.LogInformation("Status monitoring service stopped");
    }
}
