﻿// Copyright (c) Microsoft. All rights reserved.

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
using System.Reflection;
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
using System.Reflection;
=======
<<<<<<< HEAD
using System.Reflection;
=======
>>>>>>> 6d73513a859ab2d05e01db3bc1d405827799e34b
>>>>>>> main
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
using Microsoft.Azure.Cosmos;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.AzureCosmosDBNoSQL;
using Microsoft.SemanticKernel.Data;
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
using Microsoft.SemanticKernel.Http;
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
using Microsoft.SemanticKernel.Http;
=======
<<<<<<< HEAD
using Microsoft.SemanticKernel.Http;
=======
>>>>>>> 6d73513a859ab2d05e01db3bc1d405827799e34b
>>>>>>> main
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
using Moq;
using Xunit;

namespace SemanticKernel.Connectors.AzureCosmosDBNoSQL.UnitTests;

/// <summary>
/// Unit tests for <see cref="AzureCosmosDBNoSQLServiceCollectionExtensions"/> class.
/// </summary>
public sealed class AzureCosmosDBNoSQLServiceCollectionExtensionsTests
{
    private readonly IServiceCollection _serviceCollection = new ServiceCollection();

    [Fact]
    public void AddVectorStoreRegistersClass()
    {
        // Arrange
        this._serviceCollection.AddSingleton<Database>(Mock.Of<Database>());

        // Act
        this._serviceCollection.AddAzureCosmosDBNoSQLVectorStore();

        var serviceProvider = this._serviceCollection.BuildServiceProvider();
        var vectorStore = serviceProvider.GetRequiredService<IVectorStore>();

        // Assert
        Assert.NotNull(vectorStore);
        Assert.IsType<AzureCosmosDBNoSQLVectorStore>(vectorStore);
    }
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> main
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

    [Fact]
    public void AddVectorStoreWithConnectionStringRegistersClass()
    {
        // Act
        this._serviceCollection.AddAzureCosmosDBNoSQLVectorStore("AccountEndpoint=https://test.documents.azure.com:443/;AccountKey=mock;", "mydb");

        var serviceProvider = this._serviceCollection.BuildServiceProvider();
        var vectorStore = serviceProvider.GetRequiredService<IVectorStore>();

        // Assert
        Assert.NotNull(vectorStore);
        Assert.IsType<AzureCosmosDBNoSQLVectorStore>(vectorStore);
        var database = (Database)vectorStore.GetType().GetField("_database", BindingFlags.NonPublic | BindingFlags.Instance)!.GetValue(vectorStore)!;
        Assert.Equal(HttpHeaderConstant.Values.UserAgent, database.Client.ClientOptions.ApplicationName);
    }
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
<<<<<<< HEAD
=======
<<<<<<< main
=======
>>>>>>> 6d73513a859ab2d05e01db3bc1d405827799e34b
=======

    [Fact]
    public void AddVectorStoreRecordCollectionRegistersClass()
    {
        // Arrange
        this._serviceCollection.AddSingleton<Database>(Mock.Of<Database>());

        // Act
        this._serviceCollection.AddAzureCosmosDBNoSQLVectorStoreRecordCollection<TestRecord>("testcollection");

        // Assert
        this.AssertVectorStoreRecordCollectionCreated();
    }

    [Fact]
    public void AddVectorStoreRecordCollectionWithConnectionStringRegistersClass()
    {
        // Act
        this._serviceCollection.AddAzureCosmosDBNoSQLVectorStoreRecordCollection<TestRecord>("testcollection", "AccountEndpoint=https://test.documents.azure.com:443/;AccountKey=mock;", "mydb");

        // Assert
        this.AssertVectorStoreRecordCollectionCreated();
    }

    private void AssertVectorStoreRecordCollectionCreated()
    {
        var serviceProvider = this._serviceCollection.BuildServiceProvider();

        var collection = serviceProvider.GetRequiredService<IVectorStoreRecordCollection<string, TestRecord>>();
        Assert.NotNull(collection);
        Assert.IsType<AzureCosmosDBNoSQLVectorStoreRecordCollection<TestRecord>>(collection);

        var vectorizedSearch = serviceProvider.GetRequiredService<IVectorizedSearch<TestRecord>>();
        Assert.NotNull(vectorizedSearch);
        Assert.IsType<AzureCosmosDBNoSQLVectorStoreRecordCollection<TestRecord>>(vectorizedSearch);
    }

#pragma warning disable CA1812 // Avoid uninstantiated internal classes
    private sealed class TestRecord
#pragma warning restore CA1812 // Avoid uninstantiated internal classes
    {
        [VectorStoreRecordKey]
        public string Id { get; set; } = string.Empty;
    }
>>>>>>> upstream/feature-vector-search
>>>>>>> main
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
}
