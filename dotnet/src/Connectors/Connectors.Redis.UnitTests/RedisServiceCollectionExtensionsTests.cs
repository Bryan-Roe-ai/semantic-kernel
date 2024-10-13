﻿// Copyright (c) Microsoft. All rights reserved.

using Microsoft.Extensions.DependencyInjection;
<<<<<<< main
<<<<<<< HEAD
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
using Microsoft.Extensions.VectorData;
>>>>>>> upstream/main
using Microsoft.SemanticKernel;
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
using Microsoft.SemanticKernel;
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
using Microsoft.SemanticKernel;
=======
>>>>>>> Stashed changes
=======
using Microsoft.SemanticKernel;
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
using Microsoft.SemanticKernel;
=======
>>>>>>> 46c3c89f5c5dbc355794ac231b509e142f4fb770
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< HEAD
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
using Microsoft.SemanticKernel.Connectors.Redis;
using Moq;
using StackExchange.Redis;
using Xunit;

namespace SemanticKernel.Connectors.Redis.UnitTests;

/// <summary>
/// Tests for the <see cref="RedisServiceCollectionExtensions"/> class.
/// </summary>
public class RedisServiceCollectionExtensionsTests
{
    private readonly IServiceCollection _serviceCollection;

    public RedisServiceCollectionExtensionsTests()
    {
        this._serviceCollection = new ServiceCollection();
    }

    [Fact]
    public void AddVectorStoreRegistersClass()
    {
        // Arrange.
        this._serviceCollection.AddSingleton<IDatabase>(Mock.Of<IDatabase>());

        // Act.
        this._serviceCollection.AddRedisVectorStore();

        // Assert.
        this.AssertVectorStoreCreated();
    }

<<<<<<< main
<<<<<<< HEAD
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> upstream/main
    [Fact]
    public void AddRedisHashSetVectorStoreRecordCollectionRegistersClass()
    {
        // Arrange.
        this._serviceCollection.AddSingleton<IDatabase>(Mock.Of<IDatabase>());

        // Act.
        this._serviceCollection.AddRedisHashSetVectorStoreRecordCollection<TestRecord>("testCollection");

        // Assert.
        this.AssertHashSetVectorStoreRecordCollectionCreated<TestRecord>();
    }

    [Fact]
    public void AddRedisJsonVectorStoreRecordCollectionRegistersClass()
    {
        // Arrange.
        this._serviceCollection.AddSingleton<IDatabase>(Mock.Of<IDatabase>());

        // Act.
        this._serviceCollection.AddRedisJsonVectorStoreRecordCollection<TestRecord>("testCollection");

        // Assert.
        this.AssertJsonVectorStoreRecordCollectionCreated<TestRecord>();
    }

<<<<<<< main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< HEAD
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> upstream/main
    private void AssertVectorStoreCreated()
    {
        var serviceProvider = this._serviceCollection.BuildServiceProvider();
        var vectorStore = serviceProvider.GetRequiredService<IVectorStore>();
        Assert.NotNull(vectorStore);
        Assert.IsType<RedisVectorStore>(vectorStore);
    }
<<<<<<< main
<<<<<<< HEAD
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> upstream/main

    private void AssertHashSetVectorStoreRecordCollectionCreated<TRecord>() where TRecord : class
    {
        var serviceProvider = this._serviceCollection.BuildServiceProvider();
        var collection = serviceProvider.GetRequiredService<IVectorStoreRecordCollection<string, TRecord>>();
        Assert.NotNull(collection);
        Assert.IsType<RedisHashSetVectorStoreRecordCollection<TRecord>>(collection);
    }

    private void AssertJsonVectorStoreRecordCollectionCreated<TRecord>() where TRecord : class
    {
        var serviceProvider = this._serviceCollection.BuildServiceProvider();
        var collection = serviceProvider.GetRequiredService<IVectorStoreRecordCollection<string, TRecord>>();
        Assert.NotNull(collection);
        Assert.IsType<RedisJsonVectorStoreRecordCollection<TRecord>>(collection);
    }

#pragma warning disable CA1812 // Avoid uninstantiated internal classes
    private sealed class TestRecord
#pragma warning restore CA1812 // Avoid uninstantiated internal classes
    {
        [VectorStoreRecordKey]
        public string Id { get; set; } = string.Empty;
    }
<<<<<<< main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< HEAD
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> upstream/main
}
