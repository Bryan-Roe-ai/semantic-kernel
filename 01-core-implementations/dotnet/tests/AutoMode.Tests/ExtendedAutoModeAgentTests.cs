// Copyright (c) Microsoft. All rights reserved.

using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using SemanticKernel.AutoMode;
using Xunit;
using Xunit.Abstractions;

namespace SemanticKernel.AutoMode.Tests;

/// <summary>
/// Unit tests for ExtendedAutoModeAgent.
/// </summary>
public class ExtendedAutoModeAgentTests : IDisposable
{
    private readonly ITestOutputHelper _output;
    private readonly IServiceProvider _serviceProvider;
    private readonly Kernel _kernel;
    private readonly string _tempDirectory;

    public ExtendedAutoModeAgentTests(ITestOutputHelper output)
    {
        _output = output;
        _tempDirectory = Path.Combine(Path.GetTempPath(), Guid.NewGuid().ToString());
        Directory.CreateDirectory(_tempDirectory);

        var services = new ServiceCollection();
        services.AddLogging(builder => builder.AddConsole().SetMinimumLevel(LogLevel.Debug));
        
        var configuration = new ConfigurationBuilder()
            .AddInMemoryCollection(new Dictionary<string, string?>
            {
                ["ExtendedAutoMode:StateDirectory"] = _tempDirectory,
                ["ExtendedAutoMode:MaxConcurrentOperations"] = "2",
                ["ExtendedAutoMode:BaseOperationDelayMs"] = "100"
            })
            .Build();
        
        services.AddSingleton<IConfiguration>(configuration);
        services.AddSingleton<Kernel>(sp =>
        {
            var kernelBuilder = Kernel.CreateBuilder();
            return kernelBuilder.Build();
        });

        _serviceProvider = services.BuildServiceProvider();
        _kernel = _serviceProvider.GetRequiredService<Kernel>();
    }

    [Fact]
    public void Constructor_WithValidParameters_CreatesInstance()
    {
        // Arrange
        var logger = _serviceProvider.GetRequiredService<ILogger<ExtendedAutoModeAgent>>();
        var configuration = _serviceProvider.GetRequiredService<IConfiguration>();
        var options = new ExtendedAutoModeOptions { StateDirectory = _tempDirectory };

        // Act
        using var agent = new ExtendedAutoModeAgent(_kernel, logger, configuration, options);

        // Assert
        Assert.NotNull(agent);
        var status = agent.GetStatus();
        Assert.False(status.IsRunning);
        Assert.Equal(0, status.OperationCount);
        Assert.Equal(0, status.ErrorCount);
    }

    [Fact]
    public void Constructor_WithNullKernel_ThrowsArgumentNullException()
    {
        // Arrange
        var logger = _serviceProvider.GetRequiredService<ILogger<ExtendedAutoModeAgent>>();
        var configuration = _serviceProvider.GetRequiredService<IConfiguration>();

        // Act & Assert
        Assert.Throws<ArgumentNullException>(() =>
            new ExtendedAutoModeAgent(null!, logger, configuration));
    }

    [Fact]
    public void Constructor_WithNullLogger_ThrowsArgumentNullException()
    {
        // Arrange
        var configuration = _serviceProvider.GetRequiredService<IConfiguration>();

        // Act & Assert
        Assert.Throws<ArgumentNullException>(() =>
            new ExtendedAutoModeAgent(_kernel, null!, configuration));
    }

    [Fact]
    public void Constructor_WithNullConfiguration_ThrowsArgumentNullException()
    {
        // Arrange
        var logger = _serviceProvider.GetRequiredService<ILogger<ExtendedAutoModeAgent>>();

        // Act & Assert
        Assert.Throws<ArgumentNullException>(() =>
            new ExtendedAutoModeAgent(_kernel, logger, null!));
    }

    [Fact]
    public async Task StartAsync_WhenNotRunning_StartsSuccessfully()
    {
        // Arrange
        var logger = _serviceProvider.GetRequiredService<ILogger<ExtendedAutoModeAgent>>();
        var configuration = _serviceProvider.GetRequiredService<IConfiguration>();
        var options = new ExtendedAutoModeOptions 
        { 
            StateDirectory = _tempDirectory,
            BaseOperationDelayMs = 50
        };

        using var agent = new ExtendedAutoModeAgent(_kernel, logger, configuration, options);
        using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(2));

        // Act
        var startTask = agent.StartAsync(cts.Token);
        
        // Wait briefly to ensure it starts
        await Task.Delay(100);
        
        var status = agent.GetStatus();
        
        // Stop the agent
        await agent.StopAsync();
        
        // Wait for start task to complete
        try
        {
            await startTask;
        }
        catch (OperationCanceledException)
        {
            // Expected when cancelled
        }

        // Assert
        Assert.True(status.IsRunning || !startTask.IsCompleted); // Was running or still starting
    }

    [Fact]
    public async Task GetStatus_AfterInitialization_ReturnsCorrectStatus()
    {
        // Arrange
        var logger = _serviceProvider.GetRequiredService<ILogger<ExtendedAutoModeAgent>>();
        var configuration = _serviceProvider.GetRequiredService<IConfiguration>();
        var options = new ExtendedAutoModeOptions { StateDirectory = _tempDirectory };

        using var agent = new ExtendedAutoModeAgent(_kernel, logger, configuration, options);

        // Act
        var status = agent.GetStatus();

        // Assert
        Assert.False(status.IsRunning);
        Assert.Equal(0, status.OperationCount);
        Assert.Equal(0, status.ErrorCount);
        Assert.True(status.MemoryUsageMB >= 0);
        Assert.Equal(0.0, status.ErrorRate);
    }

    [Fact]
    public async Task StopAsync_WhenNotRunning_CompletesSuccessfully()
    {
        // Arrange
        var logger = _serviceProvider.GetRequiredService<ILogger<ExtendedAutoModeAgent>>();
        var configuration = _serviceProvider.GetRequiredService<IConfiguration>();
        var options = new ExtendedAutoModeOptions { StateDirectory = _tempDirectory };

        using var agent = new ExtendedAutoModeAgent(_kernel, logger, configuration, options);

        // Act & Assert (should not throw)
        await agent.StopAsync();
    }

    [Fact]
    public void Dispose_MultipleCallsAreSafe()
    {
        // Arrange
        var logger = _serviceProvider.GetRequiredService<ILogger<ExtendedAutoModeAgent>>();
        var configuration = _serviceProvider.GetRequiredService<IConfiguration>();
        var options = new ExtendedAutoModeOptions { StateDirectory = _tempDirectory };

        var agent = new ExtendedAutoModeAgent(_kernel, logger, configuration, options);

        // Act & Assert (should not throw)
        agent.Dispose();
        agent.Dispose(); // Second dispose should be safe
    }

    [Fact]
    public void ExtendedAutoModeOptions_DefaultValues_AreValid()
    {
        // Arrange & Act
        var options = new ExtendedAutoModeOptions();

        // Assert
        Assert.True(options.MaxConcurrentOperations > 0);
        Assert.True(options.BaseOperationDelayMs >= 0);
        Assert.True(options.HealthCheckIntervalMinutes > 0);
        Assert.True(options.MaintenanceIntervalHours > 0);
        Assert.True(options.MaxMemoryUsageMB > 0);
        Assert.True(options.MaxErrorRate >= 0.0 && options.MaxErrorRate <= 1.0);
        Assert.True(options.StateRetentionHours > 0);
        Assert.NotNull(options.StateDirectory);
    }

    [Fact]
    public async Task StateDirectory_CreatedWhenDoesNotExist()
    {
        // Arrange
        var nonExistentDirectory = Path.Combine(_tempDirectory, "non-existent");
        var logger = _serviceProvider.GetRequiredService<ILogger<ExtendedAutoModeAgent>>();
        var configuration = _serviceProvider.GetRequiredService<IConfiguration>();
        var options = new ExtendedAutoModeOptions { StateDirectory = nonExistentDirectory };

        using var agent = new ExtendedAutoModeAgent(_kernel, logger, configuration, options);
        using var cts = new CancellationTokenSource(TimeSpan.FromMilliseconds(500));

        // Act
        try
        {
            await agent.StartAsync(cts.Token);
        }
        catch (OperationCanceledException)
        {
            // Expected
        }

        await agent.StopAsync();

        // Assert
        Assert.True(Directory.Exists(nonExistentDirectory));
    }

    public void Dispose()
    {
        _serviceProvider?.Dispose();
        
        if (Directory.Exists(_tempDirectory))
        {
            try
            {
                Directory.Delete(_tempDirectory, true);
            }
            catch
            {
                // Ignore cleanup errors in tests
            }
        }
    }
}
