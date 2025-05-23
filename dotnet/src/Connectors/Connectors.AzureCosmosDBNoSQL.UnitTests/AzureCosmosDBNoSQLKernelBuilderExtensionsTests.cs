<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
﻿// Copyright (c) Microsoft. All rights reserved.
=======
=======
>>>>>>> Stashed changes
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
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
﻿// Copyright (c) Microsoft. All rights reserved.
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
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
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

using System.Reflection;
using System.Text.Json;
using Microsoft.Azure.Cosmos;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.VectorData;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.AzureCosmosDBNoSQL;
using Microsoft.SemanticKernel.Http;
using Moq;
using Xunit;

namespace SemanticKernel.Connectors.AzureCosmosDBNoSQL.UnitTests;

/// <summary>
/// Unit tests for <see cref="AzureCosmosDBNoSQLKernelBuilderExtensions"/> class.
/// </summary>
public sealed class AzureCosmosDBNoSQLKernelBuilderExtensionsTests
{
    private readonly IKernelBuilder _kernelBuilder = Kernel.CreateBuilder();
    private readonly Mock<Database> _mockDatabase = new();

    public AzureCosmosDBNoSQLKernelBuilderExtensionsTests()
    {
        var mockClient = new Mock<CosmosClient>();

        mockClient.Setup(l => l.ClientOptions).Returns(new CosmosClientOptions() { UseSystemTextJsonSerializerWithOptions = JsonSerializerOptions.Default });

        this._mockDatabase
            .Setup(l => l.Client)
            .Returns(mockClient.Object);
    }

    [Fact]
    public void AddVectorStoreRegistersClass()
    {
        // Arrange
        this._kernelBuilder.Services.AddSingleton<Database>(this._mockDatabase.Object);

        // Act
        this._kernelBuilder.AddAzureCosmosDBNoSQLVectorStore();

        var kernel = this._kernelBuilder.Build();
        var vectorStore = kernel.Services.GetRequiredService<IVectorStore>();

        // Assert
        Assert.NotNull(vectorStore);
        Assert.IsType<AzureCosmosDBNoSQLVectorStore>(vectorStore);
    }

    [Fact]
    public void AddVectorStoreWithConnectionStringRegistersClass()
    {
        // Act
        this._kernelBuilder.AddAzureCosmosDBNoSQLVectorStore("AccountEndpoint=https://test.documents.azure.com:443/;AccountKey=mock;", "mydb");

        var kernel = this._kernelBuilder.Build();
        var vectorStore = kernel.Services.GetRequiredService<IVectorStore>();

        // Assert
        Assert.NotNull(vectorStore);
        Assert.IsType<AzureCosmosDBNoSQLVectorStore>(vectorStore);
        var database = (Database)vectorStore.GetType().GetField("_database", BindingFlags.NonPublic | BindingFlags.Instance)!.GetValue(vectorStore)!;
        Assert.Equal(HttpHeaderConstant.Values.UserAgent, database.Client.ClientOptions.ApplicationName);
    }
<<<<<<< main
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
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
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
>>>>>>> head
<<<<<<< main
=======
=======
>>>>>>> upstream/main
    [Fact]
    public void AddVectorStoreRecordCollectionRegistersClass()
    {
        // Arrange
        this._kernelBuilder.Services.AddSingleton<Database>(this._mockDatabase.Object);

        // Act
        this._kernelBuilder.AddAzureCosmosDBNoSQLVectorStoreRecordCollection<TestRecord>("testcollection");

        // Assert
        this.AssertVectorStoreRecordCollectionCreated();
    }

    [Fact]
    public void AddVectorStoreRecordCollectionWithConnectionStringRegistersClass()
    {
        // Act
        this._kernelBuilder.AddAzureCosmosDBNoSQLVectorStoreRecordCollection<TestRecord>("testcollection", "AccountEndpoint=https://test.documents.azure.com:443/;AccountKey=mock;", "mydb");

        // Assert
        this.AssertVectorStoreRecordCollectionCreated();
    }

    private void AssertVectorStoreRecordCollectionCreated()
    {
        var kernel = this._kernelBuilder.Build();

        var collection = kernel.Services.GetRequiredService<IVectorStoreRecordCollection<string, TestRecord>>();
        Assert.NotNull(collection);
        Assert.IsType<AzureCosmosDBNoSQLVectorStoreRecordCollection<string, TestRecord>>(collection);

        var vectorizedSearch = kernel.Services.GetRequiredService<IVectorSearch<TestRecord>>();
        Assert.NotNull(vectorizedSearch);
        Assert.IsType<AzureCosmosDBNoSQLVectorStoreRecordCollection<string, TestRecord>>(vectorizedSearch);
    }

#pragma warning disable CA1812 // Avoid uninstantiated internal classes
    private sealed class TestRecord
#pragma warning restore CA1812 // Avoid uninstantiated internal classes
    {
        [VectorStoreRecordKey]
        public string Id { get; set; } = string.Empty;
    }
<<<<<<< main
>>>>>>> upstream/feature-vector-search
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< HEAD
>>>>>>> main
<<<<<<< Updated upstream
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
>>>>>>> Stashed changes
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
<<<<<<< main
=======
>>>>>>> upstream/main
=======
>>>>>>> head
>>>>>>> div
}
