# 🧪 Experimental Features Configuration Guide

This document provides comprehensive guidance on using experimental features and configuration options in Bryan Roe's enhanced Semantic Kernel implementation.

## 🧪 Experimental Features System

The experimental features system uses a hierarchical `SKEXP` (Semantic Kernel Experimental) numbering scheme to categorize and control access to cutting-edge functionality. This allows for granular control over which experimental features to enable in different environments.

### Feature Categories

| Code Range | Category | Description | Production Ready |
|------------|----------|-------------|------------------|
| `SKEXP0001` | Core Features | Fundamental semantic kernel capabilities | 🟢 Stable |
| `SKEXP0010` | Azure OpenAI | Azure OpenAI service integrations | 🟡 Beta |
| `SKEXP0020` | Memory Connectors | Vector stores and memory systems | 🟢 Stable |
| `SKEXP0040` | Function Types | Advanced function orchestration | 🟡 Beta |
| `SKEXP0050` | Plugins | Out-of-the-box plugin ecosystem | 🟢 Stable |
| `SKEXP0060` | Planners | AI planning and orchestration | 🟡 Beta |
| `SKEXP0070` | AI Connectors | Third-party AI service integrations | 🔴 Alpha |
| `SKEXP0100` | Advanced Features | Cutting-edge AI capabilities | 🔴 Alpha |
| `SKEXP0110` | Agent Framework | Multi-agent orchestration | 🔴 Alpha |
| `SKEXP0120` | Native AOT | Ahead-of-time compilation support | 🔴 Alpha |

### Stability Levels
1. **Alpha (🔴)**: Highly experimental, breaking changes expected
2. **Beta (🟡)**: Feature stabilizing, minor breaking changes possible
3. **Stable (🟢)**: Production ready, follows semantic versioning

## 🔧 Configuration Methods

### Basic Feature Enablement
```xml
<!-- In your .csproj file -->
<PropertyGroup>
  <!-- Suppress warnings for stable experimental features -->
  <NoWarn>$(NoWarn);SKEXP0001;SKEXP0020;SKEXP0050</NoWarn>
</PropertyGroup>
```

### Advanced Configuration
```xml
<PropertyGroup>
  <!-- Production-ready features -->
  <NoWarn>$(NoWarn);SKEXP0001;SKEXP0020;SKEXP0050</NoWarn>

  <!-- Conditional feature enablement based on build configuration -->
  <NoWarn Condition="'$(Configuration)' == 'Debug'">$(NoWarn);SKEXP0010;SKEXP0040;SKEXP0060</NoWarn>

  <!-- Alpha features only in development environment -->
  <NoWarn Condition="'$(Environment)' == 'Development'">$(NoWarn);SKEXP0070;SKEXP0100;SKEXP0110</NoWarn>
</PropertyGroup>
```

### Environment Variables
```bash
# Feature-specific configuration
export SEMANTIC_KERNEL_EXPERIMENTAL_FEATURES="SKEXP0001,SKEXP0020,SKEXP0110"
export SKEXP0001_ENABLE_ADVANCED_SEARCH=true
export SKEXP0020_VECTOR_DIMENSIONS=1536
export SKEXP0110_AGENT_TIMEOUT=30000
```

### Configuration in Code
```csharp
public class ExperimentalFeatureConfiguration
{
    public bool IsFeatureEnabled(string featureCode)
    {
        var enabledFeatures = Environment.GetEnvironmentVariable("SEMANTIC_KERNEL_EXPERIMENTAL_FEATURES");
        return enabledFeatures?.Split(',').Contains(featureCode) ?? false;
    }

    public T GetFeatureConfiguration<T>(string featureCode, string configKey, T defaultValue)
    {
        var envVar = $"{featureCode}_{configKey}";
        var value = Environment.GetEnvironmentVariable(envVar);
        if (string.IsNullOrEmpty(value))
            return defaultValue;

        return (T)Convert.ChangeType(value, typeof(T));
    }
}

// Usage
var featureConfig = new ExperimentalFeatureConfiguration();
if (featureConfig.IsFeatureEnabled("SKEXP0110"))
{
    var timeout = featureConfig.GetFeatureConfiguration("SKEXP0110", "AGENT_TIMEOUT", 15000);
    #pragma warning disable SKEXP0110
    var agentConfig = new AgentConfiguration { TimeoutMs = timeout };
    #pragma warning restore SKEXP0110
}
```

### Conditional Compilation
```csharp
public class FeatureManager
{
    public static class Features
    {
        #if ENABLE_SKEXP0110
        public const bool AgentFramework = true;
        #else
        public const bool AgentFramework = false;
        #endif

        #if ENABLE_SKEXP0070
        public const bool ThirdPartyConnectors = true;
        #else
        public const bool ThirdPartyConnectors = false;
        #endif
    }

    public static void ConfigureServices(IServiceCollection services)
    {
        if (Features.AgentFramework)
        {
            #pragma warning disable SKEXP0110
            services.AddScoped<IAgentOrchestrator, EnhancedAgentOrchestrator>();
            #pragma warning restore SKEXP0110
        }

        if (Features.ThirdPartyConnectors)
        {
            #pragma warning disable SKEXP0070
            services.AddScoped<IOllamaConnector, OllamaConnector>();
            #pragma warning restore SKEXP0070
        }
    }
}
```

### Granular Control
```csharp
using Microsoft.SemanticKernel.Data;
using Microsoft.SemanticKernel.Connectors.AzureAISearch;
#pragma warning disable SKEXP0001  // Core features
#pragma warning disable SKEXP0020  // Memory connectors

public class EnhancedMemoryService
{
    public async Task<IEnumerable<SearchResult>> SearchAsync(string query)
    {
        #pragma warning disable SKEXP0110  // Agent framework
        var agentCoordinator = new AgentCoordinator();
        #pragma warning restore SKEXP0110

        // Stable feature usage
        var vectorStore = new AzureAISearchVectorStore(client);
        return await vectorStore.SearchAsync(query);
    }
}
#pragma warning restore SKEXP0020
#pragma warning restore SKEXP0001
```

## 🎛️ Feature-Specific Configuration

### Vector Search Configuration
```csharp
#pragma warning disable SKEXP0001
public class VectorSearchConfiguration
{
    public int VectorDimensions { get; set; } = 1536;
    public bool EnableAdvancedSearch { get; set; } = false;
    public bool CacheResults { get; set; } = true;
}
```

### Multi-Agent Configuration
```csharp
#pragma warning disable SKEXP0110
public class AgentFrameworkConfiguration
{
    public class AgentSettings
    {
        public int MaxConcurrentAgents { get; set; } = 5;
        public TimeSpan AgentTimeout { get; set; } = TimeSpan.FromSeconds(30);
        public ConflictResolutionStrategy ConflictResolution { get; set; } = ConflictResolutionStrategy.Priority;
        public bool EnableDistributedCoordination { get; set; } = false;
    }

    public static void ConfigureAgentFramework(
        IServiceCollection services, 
        AgentSettings settings)
    {
        services.AddSingleton(settings);
        services.AddScoped<IConflictResolver, PriorityBasedConflictResolver>();

        if (settings.EnableDistributedCoordination)
        {
            services.AddScoped<IDistributedCoordinator, RedisDistributedCoordinator>();
        }

        services.AddScoped<IAgentCoordinator, EnhancedAgentCoordinator>();
    }
}

public enum ConflictResolutionStrategy
{
    Priority,
    Consensus,
    FirstWins,
    LastWins,
    Custom
}
#pragma warning restore SKEXP0110
```

### Azure AI Search Enhanced Configuration
```csharp
#pragma warning disable SKEXP0020
public class EnhancedAzureAISearchConfig
{
    public static AzureAISearchMemoryRecordService<T> CreateService<T>(
        string endpoint, 
        string apiKey,
        AzureAISearchMemoryRecordServiceOptions? options = null) where T : class
    {
        var searchIndexClient = new SearchIndexClient(
            new Uri(endpoint), 
            new AzureKeyCredential(apiKey)
        );

        options ??= new AzureAISearchMemoryRecordServiceOptions
        {
            VectorStoreRecordDefinition = CreateRecordDefinition<T>()
        };

        return new AzureAISearchMemoryRecordService<T>(searchIndexClient, options);
    }

    // Enhanced record definition with optimized field mappings
    private static VectorStoreRecordDefinition CreateRecordDefinition<T>()
    {
        return new VectorStoreRecordDefinition
        {
            Properties = GetOptimizedProperties<T>()
        };
    }
}
#pragma warning restore SKEXP0020
```

## 🌍 Environment-Specific Configurations

### Development Environment
```json
{
  "SemanticKernel": {
    "ExperimentalFeatures": {
      "Enabled": [
        "SKEXP0001",
        "SKEXP0010",
        "SKEXP0020",
        "SKEXP0040",
        "SKEXP0050",
        "SKEXP0060",
        "SKEXP0110"
      ],
      "SKEXP0110": {
        "AgentTimeout": 60000,
        "MaxConcurrentAgents": 10,
        "EnableDetailedLogging": true
      },
      "SKEXP0020": {
        "VectorDimensions": 1536,
        "EnableAdvancedSearch": true,
        "CacheResults": true
      }
    }
  }
}
```

### Production Environment
```json
{
  "SemanticKernel": {
    "ExperimentalFeatures": {
      "Enabled": [
        "SKEXP0001",
        "SKEXP0020",
        "SKEXP0050"
      ],
      "SKEXP0020": {
        "VectorDimensions": 1536,
        "EnableAdvancedSearch": false,
        "CacheResults": true
      }
    }
  }
}
```

### Testing Environment
```json
{
  "SemanticKernel": {
    "ExperimentalFeatures": {
      "Enabled": [
        "SKEXP0020"
      ],
      "SKEXP0020": {
        "VectorDimensions": 1536,
        "EnableAdvancedSearch": false,
        "CacheResults": true,
        "EnableTelemetry": true
      }
    }
  }
}
```

## 🔒 Feature Gates & Safety

```csharp
public class FeatureGate
{
    private readonly IConfiguration _configuration;
    private readonly ILogger<FeatureGate> _logger;

    public FeatureGate(IConfiguration configuration, ILogger<FeatureGate> logger)
    {
        _configuration = configuration;
        _logger = logger;
    }

    public bool IsEnabled(string featureCode)
    {
        var enabledFeatures = _configuration
            .GetSection("SemanticKernel:ExperimentalFeatures:Enabled")
            .Get<string[]>() ?? Array.Empty<string>();

        var isEnabled = enabledFeatures.Contains(featureCode);

        _logger.LogDebug("Feature {FeatureCode} is {Status}", 
            featureCode, 
            isEnabled ? "enabled" : "disabled");

        return isEnabled;
    }

    public async Task<T> ExecuteIfEnabledAsync<T>(
        string featureCode, 
        Func<Task<T>> enabledAction, 
        Func<Task<T>> fallbackAction)
    {
        if (IsEnabled(featureCode))
        {
            try
            {
                return await enabledAction();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Experimental feature {FeatureCode} failed, falling back", featureCode);
                return await fallbackAction();
            }
        }

        return await fallbackAction();
    }
}
```

## 📊 Feature Monitoring & Telemetry

```csharp
public class ExperimentalFeatureTelemetry
{
    private readonly ILogger<ExperimentalFeatureTelemetry> _logger;
    private readonly IMetrics _metrics;

    public void TrackFeatureUsage(string featureCode, string operation, bool success, TimeSpan duration)
    {
        _logger.LogInformation(
            "Experimental feature usage: {FeatureCode}.{Operation} - Success: {Success}, Duration: {Duration}ms",
            featureCode, operation, success, duration.TotalMilliseconds);

        _metrics.CreateCounter<int>("experimental_feature_usage")
            .Add(1, new KeyValuePair<string, object?>("feature", featureCode),
                     new KeyValuePair<string, object?>("operation", operation),
                     new KeyValuePair<string, object?>("success", success));

        _metrics.CreateHistogram<double>("experimental_feature_duration")
            .Record(duration.TotalMilliseconds,
                new KeyValuePair<string, object?>("feature", featureCode),
                new KeyValuePair<string, object?>("operation", operation));
    }
}

public class MonitoredFeatureExecutor
{
    private readonly ExperimentalFeatureTelemetry _telemetry;

    public async Task<T> ExecuteAsync<T>(
        string featureCode, 
        string operation, 
        Func<Task<T>> action)
    {
        bool success = false;
        var stopwatch = Stopwatch.StartNew();

        try
        {
            var result = await action();
            success = true;
            return result;
        }
        finally
        {
            stopwatch.Stop();
            _telemetry.TrackFeatureUsage(featureCode, operation, success, stopwatch.Elapsed);
        }
    }
}
```

## 🧪 Testing Experimental Features

```csharp
[TestClass]
public class ExperimentalFeatureTests
{
    [TestMethod]
    public async Task TestAgentFramework_WhenEnabled_ShouldExecuteSuccessfully()
    {
        // Arrange
        var configuration = new ConfigurationBuilder()
            .AddInMemoryCollection(new[]
            {
                new KeyValuePair<string, string?>("SemanticKernel:ExperimentalFeatures:Enabled:0", "SKEXP0110")
            })
            .Build();

        var featureGate = new FeatureGate(configuration, Mock.Of<ILogger<FeatureGate>>());

        // Act & Assert
        Assert.IsTrue(featureGate.IsEnabled("SKEXP0110"));
    }

    [TestMethod]
    public async Task TestAgentFramework_WhenDisabled_ShouldUseFallback()
    {
        // Test fallback behavior when feature is disabled
    }
}

[TestClass]
public class ExperimentalFeatureIntegrationTests
{
    [TestMethod]
    [TestCategory("Integration")]
    public async Task TestEnhancedMemoryStore_WithExperimentalFeatures()
    {
        #pragma warning disable SKEXP0020
        var memoryStore = new AzureAISearchMemoryRecordService<TestRecord>(searchIndexClient);

        var records = await memoryStore.GetBatchAsync(testKeys, options, CancellationToken.None);

        Assert.IsTrue(records.Any());
        #pragma warning restore SKEXP0020
    }
}
```

## 🚨 Migration & Deprecation Strategy

```csharp
[Obsolete("This experimental feature has been deprecated. Use NewFeature instead.", false)]
[Experimental("SKEXP9999")]  // Special code for deprecated features
public class DeprecatedFeature
{
    public void OldMethod()
    {
        // Implementation with migration guidance
    }
}

public static class MigrationHelpers
{
    public static void MigrateFromSKEXP0100ToSKEXP0110(IServiceCollection services)
    {
        // Helper to migrate between experimental feature versions
        services.Remove<IOldAgentInterface>();

        #pragma warning disable SKEXP0110
        services.AddScoped<INewAgentInterface, NewAgentImplementation>();
        #pragma warning restore SKEXP0110
    }
}
```

This configuration guide provides comprehensive control over experimental features while maintaining production safety and enabling innovation. Use these patterns to gradually adopt new capabilities while maintaining system stability.
