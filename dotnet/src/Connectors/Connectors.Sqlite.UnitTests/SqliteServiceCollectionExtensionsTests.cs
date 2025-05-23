// Copyright (c) Microsoft. All rights reserved.

<<<<<<< HEAD
using Microsoft.Data.Sqlite;
=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.VectorData;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.Sqlite;
using Xunit;

namespace SemanticKernel.Connectors.Sqlite.UnitTests;

/// <summary>
/// Unit tests for <see cref="SqliteServiceCollectionExtensions"/> class.
/// </summary>
public sealed class SqliteServiceCollectionExtensionsTests
{
    private readonly IServiceCollection _serviceCollection = new ServiceCollection();

    [Fact]
    public void AddVectorStoreRegistersClass()
    {
<<<<<<< HEAD
        // Arrange
        this._serviceCollection.AddSingleton<SqliteConnection>(Mock.Of<SqliteConnection>());

=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        // Act
        this._serviceCollection.AddSqliteVectorStore("Data Source=:memory:");

        var serviceProvider = this._serviceCollection.BuildServiceProvider();
        var vectorStore = serviceProvider.GetRequiredService<IVectorStore>();

        // Assert
        Assert.NotNull(vectorStore);
        Assert.IsType<SqliteVectorStore>(vectorStore);
    }

    [Fact]
<<<<<<< HEAD
    public void AddVectorStoreWithSqliteConnectionRegistersClass()
    {
        // Act
        this._serviceCollection.AddSqliteVectorStore("Data Source=:test:");

        var serviceProvider = this._serviceCollection.BuildServiceProvider();
        var vectorStore = serviceProvider.GetRequiredService<IVectorStore>();

        // Assert
        Assert.NotNull(vectorStore);
        Assert.IsType<SqliteVectorStore>(vectorStore);
    }

    [Fact]
    public void AddVectorStoreRecordCollectionWithStringKeyRegistersClass()
    {
        // Arrange
        this._serviceCollection.AddSingleton<SqliteConnection>(Mock.Of<SqliteConnection>());

=======
    public void AddVectorStoreRecordCollectionWithStringKeyRegistersClass()
    {
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        // Act
        this._serviceCollection.AddSqliteVectorStoreRecordCollection<string, TestRecord>("testcollection", "Data Source=:memory:");

        var serviceProvider = this._serviceCollection.BuildServiceProvider();

        // Assert
        var collection = serviceProvider.GetRequiredService<IVectorStoreRecordCollection<string, TestRecord>>();
        Assert.NotNull(collection);
        Assert.IsType<SqliteVectorStoreRecordCollection<string, TestRecord>>(collection);

        var vectorizedSearch = serviceProvider.GetRequiredService<IVectorSearch<TestRecord>>();
        Assert.NotNull(vectorizedSearch);
<<<<<<< HEAD
        Assert.IsType<SqliteVectorStoreRecordCollection<TestRecord>>(vectorizedSearch);
=======
        Assert.IsType<SqliteVectorStoreRecordCollection<string, TestRecord>>(vectorizedSearch);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    [Fact]
    public void AddVectorStoreRecordCollectionWithNumericKeyRegistersClass()
    {
<<<<<<< HEAD
        // Arrange
        this._serviceCollection.AddSingleton<SqliteConnection>(Mock.Of<SqliteConnection>());

=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        // Act
        this._serviceCollection.AddSqliteVectorStoreRecordCollection<ulong, TestRecord>("testcollection", "Data Source=:memory:");

        var serviceProvider = this._serviceCollection.BuildServiceProvider();

        // Assert
        var collection = serviceProvider.GetRequiredService<IVectorStoreRecordCollection<ulong, TestRecord>>();
        Assert.NotNull(collection);
        Assert.IsType<SqliteVectorStoreRecordCollection<ulong, TestRecord>>(collection);

        var vectorizedSearch = serviceProvider.GetRequiredService<IVectorSearch<TestRecord>>();
        Assert.NotNull(vectorizedSearch);
<<<<<<< HEAD
        Assert.IsType<SqliteVectorStoreRecordCollection<TestRecord>>(vectorizedSearch);
    }

    [Fact]
    public void AddVectorStoreRecordCollectionWithStringKeyAndSqliteConnectionRegistersClass()
    {
        // Act
        this._serviceCollection.AddSqliteVectorStoreRecordCollection<string, TestRecord>("testcollection", "Data Source=:test:");

        var serviceProvider = this._serviceCollection.BuildServiceProvider();

        // Assert
        var collection = serviceProvider.GetRequiredService<IVectorStoreRecordCollection<string, TestRecord>>();
        Assert.NotNull(collection);
        Assert.IsType<SqliteVectorStoreRecordCollection<TestRecord>>(collection);

        var vectorizedSearch = serviceProvider.GetRequiredService<IVectorizedSearch<TestRecord>>();
        Assert.NotNull(vectorizedSearch);
        Assert.IsType<SqliteVectorStoreRecordCollection<TestRecord>>(vectorizedSearch);
    }

    [Fact]
    public void AddVectorStoreRecordCollectionWithNumericKeyAndSqliteConnectionRegistersClass()
    {
        // Act
        this._serviceCollection.AddSqliteVectorStoreRecordCollection<ulong, TestRecord>("testcollection", "Data Source=:test:");

        var serviceProvider = this._serviceCollection.BuildServiceProvider();

        // Assert
        var collection = serviceProvider.GetRequiredService<IVectorStoreRecordCollection<ulong, TestRecord>>();
        Assert.NotNull(collection);
        Assert.IsType<SqliteVectorStoreRecordCollection<TestRecord>>(collection);

        var vectorizedSearch = serviceProvider.GetRequiredService<IVectorizedSearch<TestRecord>>();
        Assert.NotNull(vectorizedSearch);
        Assert.IsType<SqliteVectorStoreRecordCollection<TestRecord>>(vectorizedSearch);
=======
        Assert.IsType<SqliteVectorStoreRecordCollection<ulong, TestRecord>>(vectorizedSearch);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    #region private

#pragma warning disable CA1812 // Avoid uninstantiated internal classes
    private sealed class TestRecord
#pragma warning restore CA1812 // Avoid uninstantiated internal classes
    {
        [VectorStoreRecordKey]
        public string Id { get; set; } = string.Empty;
    }

    #endregion
}
