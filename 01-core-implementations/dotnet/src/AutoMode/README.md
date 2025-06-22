# Extended Auto Mode for Semantic Kernel

## Overview

The Extended Auto Mode provides robust, long-term autonomous operation capabilities for Semantic Kernel applications. It's designed for scenarios requiring months-long continuous operation with advanced self-maintenance, predictive analytics, and autonomous problem resolution.

## Features

- **Ultra-Long-Term Stability**: Designed for months-long continuous operation
- **Self-Maintenance**: Automatic garbage collection, state cleanup, and resource management
- **Health Monitoring**: Real-time health checks and performance metrics
- **Adaptive Performance**: Dynamic adjustment based on system load and memory usage
- **Graceful Error Handling**: Exponential backoff, comprehensive logging, and recovery mechanisms
- **State Persistence**: Automatic state saving and restoration across restarts
- **Dependency Injection**: Full integration with .NET hosting and DI container
- **Comprehensive Logging**: Structured logging with configurable levels

## Quick Start

### Basic Usage

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using SemanticKernel.AutoMode;

// Create host with Extended Auto Mode
var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices((context, services) =>
    {
        // Add Semantic Kernel
        services.AddSingleton<Kernel>(sp =>
        {
            var builder = Kernel.CreateBuilder();
            // Configure your kernel here
            return builder.Build();
        });

        // Add Extended Auto Mode
        services.AddExtendedAutoMode(options =>
        {
            options.MaxConcurrentOperations = 10;
            options.BaseOperationDelayMs = 500;
            options.HealthCheckIntervalMinutes = 5;
            options.MaintenanceIntervalHours = 24;
            options.StateDirectory = "./state";
        });
    })
    .Build();

// Run the host
await host.RunAsync();
```

### Using the Builder Pattern

```csharp
var services = new ServiceCollection();

services.AddLogging()
        .AddSingleton<Kernel>(/* kernel setup */)
        .AddExtendedAutoMode();

// Or with fluent configuration
var builder = new ExtendedAutoModeBuilder(services);
builder.WithMaxConcurrentOperations(5)
       .WithBaseOperationDelay(1000)
       .WithHealthCheckInterval(10)
       .WithMaintenanceInterval(12)
       .WithMaxMemoryUsage(2048)
       .WithMaxErrorRate(0.02)
       .WithStateRetention(168)
       .WithStateDirectory("/var/lib/automode")
       .Build();
```

### Manual Control

```csharp
var serviceProvider = services.BuildServiceProvider();
var kernel = serviceProvider.GetRequiredService<Kernel>();
var logger = serviceProvider.GetRequiredService<ILogger<ExtendedAutoModeAgent>>();
var configuration = serviceProvider.GetRequiredService<IConfiguration>();

using var agent = new ExtendedAutoModeAgent(kernel, logger, configuration);

// Start the agent
await agent.StartAsync();

// Monitor status
var status = agent.GetStatus();
Console.WriteLine($"Running: {status.IsRunning}");
Console.WriteLine($"Uptime: {status.Uptime}");
Console.WriteLine($"Operations: {status.OperationCount}");
Console.WriteLine($"Error Rate: {status.ErrorRate:P2}");

// Stop gracefully
await agent.StopAsync();
```

## Configuration

### Options

| Property | Default | Description |
|----------|---------|-------------|
| `MaxConcurrentOperations` | 5 | Maximum number of concurrent operations |
| `BaseOperationDelayMs` | 1000 | Base delay between operations (milliseconds) |
| `HealthCheckIntervalMinutes` | 5 | Health check interval (minutes) |
| `MaintenanceIntervalHours` | 24 | Maintenance interval (hours) |
| `MaxMemoryUsageMB` | 2048 | Memory usage threshold for warnings (MB) |
| `MaxErrorRate` | 0.05 | Maximum acceptable error rate (0.0-1.0) |
| `StateRetentionHours` | 168 | State retention time (hours, default 7 days) |
| `StateDirectory` | "./state" | Directory for storing state files |

### Configuration File

```json
{
  "ExtendedAutoMode": {
    "MaxConcurrentOperations": 10,
    "BaseOperationDelayMs": 500,
    "HealthCheckIntervalMinutes": 5,
    "MaintenanceIntervalHours": 24,
    "MaxMemoryUsageMB": 4096,
    "MaxErrorRate": 0.02,
    "StateRetentionHours": 336,
    "StateDirectory": "/var/lib/semantic-kernel/state"
  }
}
```

### Environment Variables

```bash
ExtendedAutoMode__MaxConcurrentOperations=10
ExtendedAutoMode__BaseOperationDelayMs=500
ExtendedAutoMode__StateDirectory=/var/lib/semantic-kernel/state
```

## Status Monitoring

The `GetStatus()` method provides comprehensive status information:

```csharp
var status = agent.GetStatus();

// Basic information
bool isRunning = status.IsRunning;
DateTime startTime = status.StartTime;
TimeSpan uptime = status.Uptime;

// Performance metrics
int operationCount = status.OperationCount;
int errorCount = status.ErrorCount;
double errorRate = status.ErrorRate;
long memoryUsageMB = status.MemoryUsageMB;

// State information
int stateCount = status.StateCount;
DateTime lastHealthCheck = status.LastHealthCheck;
```

## Integration with Azure

### Azure Container Instances

```dockerfile
FROM mcr.microsoft.com/dotnet/runtime:8.0
WORKDIR /app
COPY . .
ENTRYPOINT ["dotnet", "YourApp.dll"]
```

### Azure App Service

Configure in `appsettings.json`:

```json
{
  "ExtendedAutoMode": {
    "StateDirectory": "/home/data/state",
    "MaxMemoryUsageMB": 1024,
    "HealthCheckIntervalMinutes": 2
  }
}
```

### Azure Functions (Consumption Plan)

For Azure Functions, use shorter intervals:

```csharp
services.AddExtendedAutoMode(options =>
{
    options.HealthCheckIntervalMinutes = 1;
    options.MaintenanceIntervalHours = 1;
    options.MaxMemoryUsageMB = 512;
});
```

## Logging

The Extended Auto Mode provides structured logging:

```csharp
services.AddLogging(builder =>
{
    builder.AddConsole()
           .AddApplicationInsights() // For Azure
           .SetMinimumLevel(LogLevel.Information);
});
```

### Log Categories

- `SemanticKernel.AutoMode.ExtendedAutoModeAgent` - Main agent operations
- `SemanticKernel.AutoMode.ExtendedAutoModeHostedService` - Hosted service lifecycle

### Sample Log Output

```
[2024-01-15 10:30:00] INFO ExtendedAutoModeAgent initialized successfully
[2024-01-15 10:30:01] INFO Starting ExtendedAutoModeAgent for long-term operation
[2024-01-15 10:35:00] INFO Health check completed - Uptime: 00:05:00, Operations: 150, Errors: 0, Memory: 256MB
[2024-01-15 10:40:00] WARN High memory usage detected: 1800MB
[2024-01-15 22:30:00] INFO System maintenance completed
```

## Best Practices

### Resource Management

1. **Memory**: Monitor memory usage and set appropriate limits
2. **State**: Regularly clean up old state to prevent disk bloat
3. **Logging**: Use appropriate log levels to balance observability and performance

### Error Handling

1. **Exponential Backoff**: Built-in exponential backoff for transient errors
2. **Circuit Breaker**: Consider implementing circuit breaker patterns for external dependencies
3. **Health Checks**: Use the built-in health checks for monitoring

### Security

1. **State Directory**: Ensure proper permissions on the state directory
2. **Secrets**: Use Azure Key Vault or similar for sensitive configuration
3. **Network**: Implement proper network security for long-running services

### Performance

1. **Concurrent Operations**: Tune based on your specific workload
2. **Operation Delay**: Adjust based on external service rate limits
3. **Adaptive Delays**: The system automatically adjusts delays based on memory pressure

## Troubleshooting

### Common Issues

#### High Memory Usage

```text
WARN High memory usage detected: 2048MB
```

**Solution**: Reduce `MaxConcurrentOperations` or increase `MaxMemoryUsageMB` threshold.

#### High Error Rate

```text
WARN High error rate detected: 15.00%
```

**Solution**: Check external dependencies, review error logs, consider increasing `BaseOperationDelayMs`.

#### State Directory Issues

```text
ERROR Error saving state
```

**Solution**: Verify directory permissions and disk space.

### Debugging

Enable debug logging:

```csharp
services.AddLogging(builder =>
{
    builder.SetMinimumLevel(LogLevel.Debug);
});
```

### Health Endpoint

For monitoring systems, expose health status:

```csharp
app.MapGet("/health", (ExtendedAutoModeAgent agent) =>
{
    var status = agent.GetStatus();
    return status.IsRunning && status.ErrorRate < 0.1 
        ? Results.Ok(status) 
        : Results.Problem("Unhealthy");
});
```

## Advanced Scenarios

### Custom Operations

Extend the agent for custom operations:

```csharp
public class CustomExtendedAutoModeAgent : ExtendedAutoModeAgent
{
    protected override async Task ProcessOperationAsync(CancellationToken cancellationToken)
    {
        // Your custom logic here
        await base.ProcessOperationAsync(cancellationToken);
    }
}
```

### Multi-Tenant Support

Configure per-tenant state directories:

```csharp
services.AddExtendedAutoMode(options =>
{
    options.StateDirectory = $"/var/lib/semantic-kernel/tenant-{tenantId}";
});
```

### Distributed Deployment

For distributed scenarios, consider:

1. **Shared State**: Use Redis or similar for shared state
2. **Load Balancing**: Distribute load across multiple instances
3. **Coordination**: Use distributed locks for coordinated operations

## Support

For issues and questions:

1. Check the [Semantic Kernel documentation](https://learn.microsoft.com/semantic-kernel/)
2. Review logs for detailed error information
3. Monitor system resources and adjust configuration accordingly
4. Consider Azure Application Insights for production monitoring
