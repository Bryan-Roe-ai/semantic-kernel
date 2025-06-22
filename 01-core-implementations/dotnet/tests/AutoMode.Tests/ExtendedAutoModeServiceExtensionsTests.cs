// Copyright (c) Microsoft. All rights reserved.

using System;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using SemanticKernel.AutoMode;
using Xunit;

namespace SemanticKernel.AutoMode.Tests;

/// <summary>
/// Unit tests for ExtendedAutoModeServiceExtensions.
/// </summary>
public class ExtendedAutoModeServiceExtensionsTests
{
    [Fact]
    public void AddExtendedAutoMode_WithAction_RegistersServices()
    {
        // Arrange
        var services = new ServiceCollection();
        services.AddLogging();
        services.AddSingleton<IConfiguration>(new ConfigurationBuilder().Build());
        services.AddSingleton<Kernel>(Kernel.CreateBuilder().Build());

        // Act
        services.AddExtendedAutoMode(options =>
        {
            options.MaxConcurrentOperations = 10;
            options.BaseOperationDelayMs = 500;
        });

        var serviceProvider = services.BuildServiceProvider();

        // Assert
        var options = serviceProvider.GetRequiredService<ExtendedAutoModeOptions>();
        Assert.Equal(10, options.MaxConcurrentOperations);
        Assert.Equal(500, options.BaseOperationDelayMs);

        var agent = serviceProvider.GetRequiredService<ExtendedAutoModeAgent>();
        Assert.NotNull(agent);
    }

    [Fact]
    public void AddExtendedAutoMode_WithConfiguration_RegistersServices()
    {
        // Arrange
        var configuration = new ConfigurationBuilder()
            .AddInMemoryCollection(new Dictionary<string, string?>
            {
                ["MaxConcurrentOperations"] = "15",
                ["BaseOperationDelayMs"] = "200"
            })
            .Build();

        var services = new ServiceCollection();
        services.AddLogging();
        services.AddSingleton<IConfiguration>(new ConfigurationBuilder().Build());
        services.AddSingleton<Kernel>(Kernel.CreateBuilder().Build());

        // Act
        services.AddExtendedAutoMode(configuration);

        var serviceProvider = services.BuildServiceProvider();

        // Assert
        var agent = serviceProvider.GetRequiredService<ExtendedAutoModeAgent>();
        Assert.NotNull(agent);
    }
}

/// <summary>
/// Unit tests for ExtendedAutoModeBuilder.
/// </summary>
public class ExtendedAutoModeBuilderTests
{
    [Fact]
    public void WithMaxConcurrentOperations_ValidValue_SetsOption()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act
        var result = builder.WithMaxConcurrentOperations(20);

        // Assert
        Assert.Same(builder, result); // Fluent interface
    }

    [Fact]
    public void WithMaxConcurrentOperations_ZeroValue_ThrowsArgumentOutOfRangeException()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act & Assert
        Assert.Throws<ArgumentOutOfRangeException>(() => builder.WithMaxConcurrentOperations(0));
    }

    [Fact]
    public void WithMaxConcurrentOperations_NegativeValue_ThrowsArgumentOutOfRangeException()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act & Assert
        Assert.Throws<ArgumentOutOfRangeException>(() => builder.WithMaxConcurrentOperations(-1));
    }

    [Fact]
    public void WithBaseOperationDelay_ValidValue_SetsOption()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act
        var result = builder.WithBaseOperationDelay(1000);

        // Assert
        Assert.Same(builder, result); // Fluent interface
    }

    [Fact]
    public void WithBaseOperationDelay_NegativeValue_ThrowsArgumentOutOfRangeException()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act & Assert
        Assert.Throws<ArgumentOutOfRangeException>(() => builder.WithBaseOperationDelay(-1));
    }

    [Fact]
    public void WithHealthCheckInterval_ValidValue_SetsOption()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act
        var result = builder.WithHealthCheckInterval(10);

        // Assert
        Assert.Same(builder, result); // Fluent interface
    }

    [Fact]
    public void WithHealthCheckInterval_ZeroValue_ThrowsArgumentOutOfRangeException()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act & Assert
        Assert.Throws<ArgumentOutOfRangeException>(() => builder.WithHealthCheckInterval(0));
    }

    [Fact]
    public void WithMaintenanceInterval_ValidValue_SetsOption()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act
        var result = builder.WithMaintenanceInterval(24);

        // Assert
        Assert.Same(builder, result); // Fluent interface
    }

    [Fact]
    public void WithMaintenanceInterval_ZeroValue_ThrowsArgumentOutOfRangeException()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act & Assert
        Assert.Throws<ArgumentOutOfRangeException>(() => builder.WithMaintenanceInterval(0));
    }

    [Fact]
    public void WithMaxMemoryUsage_ValidValue_SetsOption()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act
        var result = builder.WithMaxMemoryUsage(2048);

        // Assert
        Assert.Same(builder, result); // Fluent interface
    }

    [Fact]
    public void WithMaxMemoryUsage_ZeroValue_ThrowsArgumentOutOfRangeException()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act & Assert
        Assert.Throws<ArgumentOutOfRangeException>(() => builder.WithMaxMemoryUsage(0));
    }

    [Fact]
    public void WithMaxErrorRate_ValidValue_SetsOption()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act
        var result = builder.WithMaxErrorRate(0.05);

        // Assert
        Assert.Same(builder, result); // Fluent interface
    }

    [Fact]
    public void WithMaxErrorRate_NegativeValue_ThrowsArgumentOutOfRangeException()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act & Assert
        Assert.Throws<ArgumentOutOfRangeException>(() => builder.WithMaxErrorRate(-0.1));
    }

    [Fact]
    public void WithMaxErrorRate_ValueGreaterThanOne_ThrowsArgumentOutOfRangeException()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act & Assert
        Assert.Throws<ArgumentOutOfRangeException>(() => builder.WithMaxErrorRate(1.1));
    }

    [Fact]
    public void WithStateRetention_ValidValue_SetsOption()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act
        var result = builder.WithStateRetention(168);

        // Assert
        Assert.Same(builder, result); // Fluent interface
    }

    [Fact]
    public void WithStateRetention_ZeroValue_ThrowsArgumentOutOfRangeException()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act & Assert
        Assert.Throws<ArgumentOutOfRangeException>(() => builder.WithStateRetention(0));
    }

    [Fact]
    public void WithStateDirectory_ValidValue_SetsOption()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act
        var result = builder.WithStateDirectory("/tmp/state");

        // Assert
        Assert.Same(builder, result); // Fluent interface
    }

    [Fact]
    public void WithStateDirectory_NullValue_ThrowsArgumentException()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act & Assert
        Assert.Throws<ArgumentException>(() => builder.WithStateDirectory(null!));
    }

    [Fact]
    public void WithStateDirectory_EmptyValue_ThrowsArgumentException()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act & Assert
        Assert.Throws<ArgumentException>(() => builder.WithStateDirectory(string.Empty));
    }

    [Fact]
    public void WithStateDirectory_WhitespaceValue_ThrowsArgumentException()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act & Assert
        Assert.Throws<ArgumentException>(() => builder.WithStateDirectory("   "));
    }

    [Fact]
    public void Build_ReturnsServiceCollection()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act
        var result = builder.Build();

        // Assert
        Assert.Same(services, result);
    }

    [Fact]
    public void FluentInterface_ChainingWorks()
    {
        // Arrange
        var services = new ServiceCollection();
        var builder = new ExtendedAutoModeBuilder(services);

        // Act & Assert
        var result = builder
            .WithMaxConcurrentOperations(5)
            .WithBaseOperationDelay(100)
            .WithHealthCheckInterval(5)
            .WithMaintenanceInterval(12)
            .WithMaxMemoryUsage(1024)
            .WithMaxErrorRate(0.02)
            .WithStateRetention(72)
            .WithStateDirectory("/tmp/test")
            .Build();

        Assert.Same(services, result);
    }
}

/// <summary>
/// Unit tests for ExtendedAutoModeAgentFactory.
/// </summary>
public class ExtendedAutoModeAgentFactoryTests
{
    [Fact]
    public void Constructor_WithNullServiceProvider_ThrowsArgumentNullException()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => new ExtendedAutoModeAgentFactory(null!));
    }

    [Fact]
    public void CreateAgent_WithKernel_ReturnsAgent()
    {
        // Arrange
        var services = new ServiceCollection();
        services.AddLogging();
        services.AddSingleton<IConfiguration>(new ConfigurationBuilder().Build());

        var serviceProvider = services.BuildServiceProvider();
        var factory = new ExtendedAutoModeAgentFactory(serviceProvider);
        var kernel = Kernel.CreateBuilder().Build();

        // Act
        using var agent = factory.CreateAgent(kernel);

        // Assert
        Assert.NotNull(agent);
    }

    [Fact]
    public void CreateAgent_WithKernelAndOptions_ReturnsAgent()
    {
        // Arrange
        var services = new ServiceCollection();
        services.AddLogging();
        services.AddSingleton<IConfiguration>(new ConfigurationBuilder().Build());

        var serviceProvider = services.BuildServiceProvider();
        var factory = new ExtendedAutoModeAgentFactory(serviceProvider);
        var kernel = Kernel.CreateBuilder().Build();
        var options = new ExtendedAutoModeOptions { MaxConcurrentOperations = 3 };

        // Act
        using var agent = factory.CreateAgent(kernel, options);

        // Assert
        Assert.NotNull(agent);
    }
}
