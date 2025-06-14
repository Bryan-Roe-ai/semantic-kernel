// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.VectorData;
using Microsoft.SemanticKernel.Connectors.MongoDB;
using MongoDB.Bson;
using MongoDB.Bson.Serialization;
using MongoDB.Bson.Serialization.Attributes;
using MongoDB.Driver;
using Moq;
using Xunit;
using MEVD = Microsoft.Extensions.VectorData;

namespace SemanticKernel.Connectors.MongoDB.UnitTests;

/// <summary>
/// Unit tests for <see cref="MongoCollection{TKey, TRecord}"/> class.
/// </summary>
public sealed class MongoCollectionTests
{
    private readonly Mock<IMongoDatabase> _mockMongoDatabase = new();
    private readonly Mock<IMongoCollection<BsonDocument>> _mockMongoCollection = new();

    public MongoCollectionTests()
    {
        this._mockMongoDatabase
            .Setup(l => l.GetCollection<BsonDocument>(It.IsAny<string>(), It.IsAny<MongoCollectionSettings>()))
            .Returns(this._mockMongoCollection.Object);
    }

    [Fact]
    public void ConstructorForModelWithoutKeyThrowsException()
    {
        // Act & Assert
        var exception = Assert.Throws<NotSupportedException>(() => new MongoCollection<string, object>(this._mockMongoDatabase.Object, "collection"));
        Assert.Contains("No key property found", exception.Message);
    }

    [Fact]
    public void ConstructorWithDeclarativeModelInitializesCollection()
    {
        // Act & Assert
        using var collection = new MongoCollection<string, MongoHotelModel>(
            this._mockMongoDatabase.Object,
            "collection");

        Assert.NotNull(collection);
    }

    [Fact]
    public void ConstructorWithImperativeModelInitializesCollection()
    {
        // Arrange
        var definition = new VectorStoreCollectionDefinition
        {
            Properties = [new VectorStoreKeyProperty("Id", typeof(string))]
        };

        // Act
        using var collection = new MongoCollection<string, TestModel>(
            this._mockMongoDatabase.Object,
            "collection",
            new() { Definition = definition });

        // Assert
        Assert.NotNull(collection);
    }

    [Theory]
    [MemberData(nameof(CollectionExistsData))]
    public async Task CollectionExistsReturnsValidResultAsync(List<string> collections, string collectionName, bool expectedResult)
    {
        // Arrange
        var mockCursor = new Mock<IAsyncCursor<string>>();

        mockCursor
            .Setup(l => l.MoveNextAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(true);

        mockCursor
            .Setup(l => l.Current)
            .Returns(collections);

        this._mockMongoDatabase
            .Setup(l => l.ListCollectionNamesAsync(It.IsAny<ListCollectionNamesOptions>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(mockCursor.Object);

        using var sut = new MongoCollection<string, MongoHotelModel>(
            this._mockMongoDatabase.Object,
            collectionName);

        // Act
        var actualResult = await sut.CollectionExistsAsync();

        // Assert
        Assert.Equal(expectedResult, actualResult);
    }

    [Fact]
    public async Task EnsureCollectionExistsInvokesValidMethodsAsync()
    {
        // Arrange
        const string CollectionName = "collection";

        var mockCursor = new Mock<IAsyncCursor<string>>();
        mockCursor
            .Setup(l => l.MoveNextAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(true);

        mockCursor
            .Setup(l => l.Current)
            .Returns([]);

        this._mockMongoDatabase
            .Setup(l => l.ListCollectionNamesAsync(It.IsAny<ListCollectionNamesOptions>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(mockCursor.Object);

        var mockIndexCursor = new Mock<IAsyncCursor<BsonDocument>>();
        mockIndexCursor
            .SetupSequence(l => l.MoveNext(It.IsAny<CancellationToken>()))
            .Returns(true)
            .Returns(false);

        mockIndexCursor
            .Setup(l => l.Current)
            .Returns([]);

        var mockMongoIndexManager = new Mock<IMongoIndexManager<BsonDocument>>();

        mockMongoIndexManager
            .Setup(l => l.ListAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(mockIndexCursor.Object);

        this._mockMongoCollection
            .Setup(l => l.Indexes)
            .Returns(mockMongoIndexManager.Object);

        using var sut = new MongoCollection<string, MongoHotelModel>(
            this._mockMongoDatabase.Object,
            CollectionName);

        // Act
        await sut.EnsureCollectionExistsAsync();

        // Assert
        this._mockMongoDatabase.Verify(l => l.CreateCollectionAsync(
            CollectionName,
            It.IsAny<CreateCollectionOptions>(),
            It.IsAny<CancellationToken>()), Times.Exactly(1));

        this._mockMongoDatabase.Verify(l => l.ListCollectionNamesAsync(
            It.IsAny<ListCollectionNamesOptions>(),
            It.IsAny<CancellationToken>()), Times.Never);
    }

    [Fact]
    public async Task DeleteInvokesValidMethodsAsync()
    {
        // Arrange
        const string RecordKey = "key";

        using var sut = new MongoCollection<string, MongoHotelModel>(
            this._mockMongoDatabase.Object,
            "collection");

        var serializerRegistry = BsonSerializer.SerializerRegistry;
        var documentSerializer = serializerRegistry.GetSerializer<BsonDocument>();
        var expectedDefinition = Builders<BsonDocument>.Filter.Eq(document => document["_id"], RecordKey);

        // Act
        await sut.DeleteAsync(RecordKey);

        // Assert
        this._mockMongoCollection.Verify(l => l.DeleteOneAsync(
            It.Is<FilterDefinition<BsonDocument>>(definition =>
                CompareFilterDefinitions(definition, expectedDefinition, documentSerializer, serializerRegistry)),
            It.IsAny<CancellationToken>()), Times.Once());
    }

    [Fact]
    public async Task DeleteBatchInvokesValidMethodsAsync()
    {
        // Arrange
        List<string> recordKeys = ["key1", "key2"];

        using var sut = new MongoCollection<string, MongoHotelModel>(
            this._mockMongoDatabase.Object,
            "collection");

        var serializerRegistry = BsonSerializer.SerializerRegistry;
        var documentSerializer = serializerRegistry.GetSerializer<BsonDocument>();
        var expectedDefinition = Builders<BsonDocument>.Filter.In(document => document["_id"].AsString, recordKeys);

        // Act
        await sut.DeleteAsync(recordKeys);

        // Assert
        this._mockMongoCollection.Verify(l => l.DeleteManyAsync(
            It.Is<FilterDefinition<BsonDocument>>(definition =>
                CompareFilterDefinitions(definition, expectedDefinition, documentSerializer, serializerRegistry)),
            It.IsAny<CancellationToken>()), Times.Once());
    }

    [Fact]
    public async Task DeleteCollectionInvokesValidMethodsAsync()
    {
        // Arrange
        const string CollectionName = "collection";

        using var sut = new MongoCollection<string, MongoHotelModel>(
            this._mockMongoDatabase.Object,
            CollectionName);

        // Act
        await sut.EnsureCollectionDeletedAsync();

        // Assert
        this._mockMongoDatabase.Verify(l => l.DropCollectionAsync(
            It.Is<string>(name => name == CollectionName),
            It.IsAny<CancellationToken>()), Times.Once());
    }

    [Fact]
    public async Task GetReturnsValidRecordAsync()
    {
        // Arrange
        const string RecordKey = "key";

        var document = new BsonDocument { ["_id"] = RecordKey, ["HotelName"] = "Test Name" };

        var mockCursor = new Mock<IAsyncCursor<BsonDocument>>();
        mockCursor
            .Setup(l => l.MoveNextAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(true);

        mockCursor
            .Setup(l => l.Current)
            .Returns([document]);

        this._mockMongoCollection
            .Setup(l => l.FindAsync(
                It.IsAny<FilterDefinition<BsonDocument>>(),
                It.IsAny<FindOptions<BsonDocument>>(),
                It.IsAny<CancellationToken>()))
            .ReturnsAsync(mockCursor.Object);

        using var sut = new MongoCollection<string, MongoHotelModel>(
            this._mockMongoDatabase.Object,
            "collection");

        // Act
        var result = await sut.GetAsync(RecordKey);

        // Assert
        Assert.NotNull(result);
        Assert.Equal(RecordKey, result.HotelId);
        Assert.Equal("Test Name", result.HotelName);
    }

    [Fact]
    public async Task GetBatchReturnsValidRecordAsync()
    {
        // Arrange
        var document1 = new BsonDocument { ["_id"] = "key1", ["HotelName"] = "Test Name 1" };
        var document2 = new BsonDocument { ["_id"] = "key2", ["HotelName"] = "Test Name 2" };
        var document3 = new BsonDocument { ["_id"] = "key3", ["HotelName"] = "Test Name 3" };

        var mockCursor = new Mock<IAsyncCursor<BsonDocument>>();
        mockCursor
            .SetupSequence(l => l.MoveNextAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(true)
            .ReturnsAsync(false);

        mockCursor
            .Setup(l => l.Current)
            .Returns([document1, document2, document3]);

        this._mockMongoCollection
            .Setup(l => l.FindAsync(
                It.IsAny<FilterDefinition<BsonDocument>>(),
                It.IsAny<FindOptions<BsonDocument>>(),
                It.IsAny<CancellationToken>()))
            .ReturnsAsync(mockCursor.Object);

        using var sut = new MongoCollection<string, MongoHotelModel>(
            this._mockMongoDatabase.Object,
            "collection");

        // Act
        var results = await sut.GetAsync(["key1", "key2", "key3"]).ToListAsync();

        // Assert
        Assert.NotNull(results[0]);
        Assert.Equal("key1", results[0].HotelId);
        Assert.Equal("Test Name 1", results[0].HotelName);

        Assert.NotNull(results[1]);
        Assert.Equal("key2", results[1].HotelId);
        Assert.Equal("Test Name 2", results[1].HotelName);

        Assert.NotNull(results[2]);
        Assert.Equal("key3", results[2].HotelId);
        Assert.Equal("Test Name 3", results[2].HotelName);
    }

    [Fact]
    public async Task CanUpsertRecordAsync()
    {
        // Arrange
        var hotel = new MongoHotelModel("key") { HotelName = "Test Name" };

        var serializerRegistry = BsonSerializer.SerializerRegistry;
        var documentSerializer = serializerRegistry.GetSerializer<BsonDocument>();
        var expectedDefinition = Builders<BsonDocument>.Filter.Eq(document => document["_id"], "key");

        using var sut = new MongoCollection<string, MongoHotelModel>(
            this._mockMongoDatabase.Object,
            "collection");

        // Act
        await sut.UpsertAsync(hotel);

        // Assert
        this._mockMongoCollection.Verify(l => l.ReplaceOneAsync(
            It.Is<FilterDefinition<BsonDocument>>(definition =>
                CompareFilterDefinitions(definition, expectedDefinition, documentSerializer, serializerRegistry)),
            It.Is<BsonDocument>(document =>
                document["_id"] == "key" &&
                document["HotelName"] == "Test Name"),
            It.IsAny<ReplaceOptions>(),
            It.IsAny<CancellationToken>()), Times.Once());
    }

    [Fact]
    public async Task CanUpsertManyRecordsAsync()
    {
        // Arrange
        var hotel1 = new MongoHotelModel("key1") { HotelName = "Test Name 1" };
        var hotel2 = new MongoHotelModel("key2") { HotelName = "Test Name 2" };
        var hotel3 = new MongoHotelModel("key3") { HotelName = "Test Name 3" };

        using var sut = new MongoCollection<string, MongoHotelModel>(
            this._mockMongoDatabase.Object,
            "collection");

        // Act
        await sut.UpsertAsync([hotel1, hotel2, hotel3]);
    }

    [Fact]
    public async Task UpsertWithModelWorksCorrectlyAsync()
    {
        var definition = new VectorStoreCollectionDefinition
        {
            Properties = new List<VectorStoreProperty>
            {
                new VectorStoreKeyProperty("Id", typeof(string)),
                new VectorStoreDataProperty("HotelName", typeof(string))
            }
        };

        await this.TestUpsertWithModelAsync<TestModel>(
            dataModel: new TestModel { Id = "key", HotelName = "Test Name" },
            expectedPropertyName: "HotelName",
            definition: definition);
    }

    [Fact]
    public async Task UpsertWithVectorStoreModelWorksCorrectlyAsync()
    {
        await this.TestUpsertWithModelAsync<VectorStoreTestModel>(
            dataModel: new VectorStoreTestModel { Id = "key", HotelName = "Test Name" },
            expectedPropertyName: "HotelName");
    }

    [Fact]
    public async Task UpsertWithBsonModelWorksCorrectlyAsync()
    {
        var definition = new VectorStoreCollectionDefinition
        {
            Properties = new List<VectorStoreProperty>
            {
                new VectorStoreKeyProperty("Id", typeof(string)),
                new VectorStoreDataProperty("HotelName", typeof(string))
            }
        };

        await this.TestUpsertWithModelAsync<BsonTestModel>(
            dataModel: new BsonTestModel { Id = "key", HotelName = "Test Name" },
            expectedPropertyName: "hotel_name",
            definition: definition);
    }

    [Fact]
    public async Task UpsertWithBsonVectorStoreModelWorksCorrectlyAsync()
    {
        await this.TestUpsertWithModelAsync<BsonVectorStoreTestModel>(
            dataModel: new BsonVectorStoreTestModel { Id = "key", HotelName = "Test Name" },
            expectedPropertyName: "hotel_name");
    }

    [Fact]
    public async Task UpsertWithBsonVectorStoreWithNameModelWorksCorrectlyAsync()
    {
        await this.TestUpsertWithModelAsync<BsonVectorStoreWithNameTestModel>(
            dataModel: new BsonVectorStoreWithNameTestModel { Id = "key", HotelName = "Test Name" },
            expectedPropertyName: "bson_hotel_name");
    }

    [Theory]
    [MemberData(nameof(SearchVectorTypeData))]
    public async Task SearchThrowsExceptionWithInvalidVectorTypeAsync(object vector, bool exceptionExpected)
    {
        // Arrange
        this.MockCollectionForSearch();

        using var sut = new MongoCollection<string, MongoHotelModel>(
            this._mockMongoDatabase.Object,
            "collection");

        // Act & Assert
        if (exceptionExpected)
        {
            await Assert.ThrowsAsync<NotSupportedException>(async () => await sut.SearchAsync(vector, top: 3).ToListAsync());
        }
        else
        {
            Assert.NotNull(await sut.SearchAsync(vector, top: 3).FirstOrDefaultAsync());
        }
    }

    [Theory]
    [InlineData("TestEmbedding1", "TestEmbedding1", 3, 3)]
    [InlineData("TestEmbedding2", "test_embedding_2", 4, 4)]
    public async Task SearchUsesValidQueryAsync(
        string? vectorPropertyName,
        string expectedVectorPropertyName,
        int actualTop,
        int expectedTop)
    {
        // Arrange
        var vector = new ReadOnlyMemory<float>([1f, 2f, 3f]);

        var expectedSearch = new BsonDocument
        {
            { "$vectorSearch",
                new BsonDocument
                {
                    { "index", "vector_index" },
                    { "queryVector", BsonArray.Create(vector.ToArray()) },
                    { "path", expectedVectorPropertyName },
                    { "limit", expectedTop },
                    { "numCandidates", expectedTop * 10 },
                }
            }
        };

        var expectedProjection = new BsonDocument
        {
            { "$project",
                new BsonDocument
                {
                    { "similarityScore", new BsonDocument { { "$meta", "vectorSearchScore" } } },
                    { "document", "$$ROOT" }
                }
            }
        };

        this.MockCollectionForSearch();

        using var sut = new MongoCollection<string, VectorSearchModel>(
            this._mockMongoDatabase.Object,
            "collection");

        Expression<Func<VectorSearchModel, object?>>? vectorSelector = vectorPropertyName switch
        {
            "TestEmbedding1" => record => record.TestEmbedding1,
            "TestEmbedding2" => record => record.TestEmbedding2,
            _ => null
        };

        // Act
        var actual = await sut.SearchAsync(vector, top: actualTop, new()
        {
            VectorProperty = vectorSelector,
        }).FirstOrDefaultAsync();

        // Assert
        Assert.NotNull(actual);

        this._mockMongoCollection.Verify(l => l.AggregateAsync(
            It.Is<PipelineDefinition<BsonDocument, BsonDocument>>(pipeline =>
                this.ComparePipeline(pipeline, expectedSearch, expectedProjection)),
            It.IsAny<AggregateOptions>(),
            It.IsAny<CancellationToken>()), Times.Once());
    }

    [Fact]
    public async Task SearchThrowsExceptionWithNonExistentVectorPropertyNameAsync()
    {
        // Arrange
        this.MockCollectionForSearch();

        using var sut = new MongoCollection<string, MongoHotelModel>(
            this._mockMongoDatabase.Object,
            "collection");

        var options = new MEVD.VectorSearchOptions<MongoHotelModel> { VectorProperty = r => "non-existent-property" };

        // Act & Assert
        await Assert.ThrowsAsync<InvalidOperationException>(async () => await sut.SearchAsync(new ReadOnlyMemory<float>([1f, 2f, 3f]), top: 3, options).FirstOrDefaultAsync());
    }

    [Fact]
    public async Task SearchReturnsRecordWithScoreAsync()
    {
        // Arrange
        this.MockCollectionForSearch();

        using var sut = new MongoCollection<string, MongoHotelModel>(
            this._mockMongoDatabase.Object,
            "collection");

        // Act
        var result = await sut.SearchAsync(new ReadOnlyMemory<float>([1f, 2f, 3f]), top: 3).FirstOrDefaultAsync();

        // Assert
        Assert.NotNull(result);
        Assert.Equal("key", result.Record.HotelId);
        Assert.Equal("Test Name", result.Record.HotelName);
        Assert.Equal(0.99f, result.Score);
    }

    public static TheoryData<List<string>, string, bool> CollectionExistsData => new()
    {
        { ["collection-2"], "collection-2", true },
        { [], "non-existent-collection", false }
    };

    public static TheoryData<List<string>, int> EnsureCollectionExistsData => new()
    {
        { ["collection"], 0 },
        { [], 1 }
    };

    public static TheoryData<object, bool> SearchVectorTypeData => new()
    {
        { new ReadOnlyMemory<float>([1f, 2f, 3f]), false },
        { new ReadOnlyMemory<float>?(new([1f, 2f, 3f])), false },
        { new List<float>([1f, 2f, 3f]), true },
    };

    #region private

    private bool ComparePipeline(
        PipelineDefinition<BsonDocument, BsonDocument> actualPipeline,
        BsonDocument expectedSearch,
        BsonDocument expectedProjection)
    {
        var serializerRegistry = BsonSerializer.SerializerRegistry;
        var documentSerializer = serializerRegistry.GetSerializer<BsonDocument>();

        var documents = actualPipeline.Render(new RenderArgs<BsonDocument>(documentSerializer, serializerRegistry)).Documents;

        return
            documents[0].ToJson() == expectedSearch.ToJson() &&
            documents[1].ToJson() == expectedProjection.ToJson();
    }

    private void MockCollectionForSearch()
    {
        var document = new BsonDocument { ["_id"] = "key", ["HotelName"] = "Test Name" };
        var searchResult = new BsonDocument { ["document"] = document, ["similarityScore"] = 0.99f };

        var mockCursor = new Mock<IAsyncCursor<BsonDocument>>();
        mockCursor
            .Setup(l => l.MoveNextAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(true);

        mockCursor
            .Setup(l => l.Current)
            .Returns([searchResult]);

        this._mockMongoCollection
            .Setup(l => l.AggregateAsync(
                It.IsAny<PipelineDefinition<BsonDocument, BsonDocument>>(),
                It.IsAny<AggregateOptions>(),
                It.IsAny<CancellationToken>()))
            .ReturnsAsync(mockCursor.Object);
    }

    private async Task TestUpsertWithModelAsync<TDataModel>(
        TDataModel dataModel,
        string expectedPropertyName,
        VectorStoreCollectionDefinition? definition = null)
        where TDataModel : class
    {
        // Arrange
        var serializerRegistry = BsonSerializer.SerializerRegistry;
        var documentSerializer = serializerRegistry.GetSerializer<BsonDocument>();
        var expectedDefinition = Builders<BsonDocument>.Filter.Eq(document => document["_id"], "key");

        MongoCollectionOptions? options = definition != null ?
            new() { Definition = definition } :
            null;

        using var sut = new MongoCollection<string, TDataModel>(
            this._mockMongoDatabase.Object,
            "collection",
            options);

        // Act
        await sut.UpsertAsync(dataModel);

        // Assert
        this._mockMongoCollection.Verify(l => l.ReplaceOneAsync(
            It.Is<FilterDefinition<BsonDocument>>(definition =>
                CompareFilterDefinitions(definition, expectedDefinition, documentSerializer, serializerRegistry)),
            It.Is<BsonDocument>(document =>
                document["_id"] == "key" &&
                document.Contains(expectedPropertyName) &&
                document[expectedPropertyName] == "Test Name"),
            It.IsAny<ReplaceOptions>(),
            It.IsAny<CancellationToken>()), Times.Once());
    }

    private static bool CompareFilterDefinitions(
        FilterDefinition<BsonDocument> actual,
        FilterDefinition<BsonDocument> expected,
        IBsonSerializer<BsonDocument> documentSerializer,
        IBsonSerializerRegistry serializerRegistry)
    {
        return actual.Render(new RenderArgs<BsonDocument>(documentSerializer, serializerRegistry)) ==
            expected.Render(new RenderArgs<BsonDocument>(documentSerializer, serializerRegistry));
    }

#pragma warning disable CA1812
    private sealed class TestModel
    {
        public string? Id { get; set; }

        public string? HotelName { get; set; }
    }

    private sealed class VectorStoreTestModel
    {
        [VectorStoreKey]
        public string? Id { get; set; }

        [VectorStoreData(StorageName = "hotel_name")]
        public string? HotelName { get; set; }
    }

    private sealed class BsonTestModel
    {
        [BsonId]
        public string? Id { get; set; }

        [BsonElement("hotel_name")]
        public string? HotelName { get; set; }
    }

    private sealed class BsonVectorStoreTestModel
    {
        [BsonId]
        [VectorStoreKey]
        public string? Id { get; set; }

        [BsonElement("hotel_name")]
        [VectorStoreData]
        public string? HotelName { get; set; }
    }

    private sealed class BsonVectorStoreWithNameTestModel
    {
        [BsonId]
        [VectorStoreKey]
        public string? Id { get; set; }

        [BsonElement("bson_hotel_name")]
        [VectorStoreData(StorageName = "storage_hotel_name")]
        public string? HotelName { get; set; }
    }

    private sealed class VectorSearchModel
    {
        [BsonId]
        [VectorStoreKey]
        public string? Id { get; set; }

        [VectorStoreData]
        public string? HotelName { get; set; }

        [VectorStoreVector(Dimensions: 4, DistanceFunction = DistanceFunction.CosineDistance, IndexKind = IndexKind.IvfFlat, StorageName = "test_embedding_1")]
        public ReadOnlyMemory<float> TestEmbedding1 { get; set; }

        [BsonElement("test_embedding_2")]
        [VectorStoreVector(Dimensions: 4, DistanceFunction = DistanceFunction.CosineDistance, IndexKind = IndexKind.IvfFlat)]
        public ReadOnlyMemory<float> TestEmbedding2 { get; set; }
    }
#pragma warning restore CA1812

    #endregion
}
