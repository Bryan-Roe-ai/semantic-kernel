// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Azure;
using Azure.Search.Documents.Indexes;
using Microsoft.Extensions.VectorData;
using Microsoft.SemanticKernel.Connectors.AzureAISearch;
<<<<<<< HEAD
using Microsoft.SemanticKernel.Data;
using Microsoft.SemanticKernel.Embeddings;
=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
using Xunit;
using Xunit.Abstractions;

namespace SemanticKernel.IntegrationTests.Connectors.Memory.AzureAISearch;

#pragma warning disable CS0618 // VectorSearchFilter is obsolete

/// <summary>
/// Integration tests for <see cref="AzureAISearchVectorStoreRecordCollection{TKey, TRecord}"/> class.
/// Tests work with an Azure AI Search Instance.
/// </summary>
[Collection("AzureAISearchVectorStoreCollection")]
public sealed class AzureAISearchVectorStoreRecordCollectionTests(ITestOutputHelper output, AzureAISearchVectorStoreFixture fixture)
{
    // If null, all tests will be enabled
    private const string SkipReason = "Requires Azure AI Search Service instance up and running";

    [Theory(Skip = SkipReason)]
    [InlineData(true)]
    [InlineData(false)]
    public async Task CollectionExistsReturnsCollectionStateAsync(bool expectedExists)
    {
        // Arrange.
        var collectionName = expectedExists ? fixture.TestIndexName : "nonexistentcollection";
        var sut = new AzureAISearchVectorStoreRecordCollection<string, AzureAISearchHotel>(fixture.SearchIndexClient, collectionName);

        // Act.
        var actual = await sut.CollectionExistsAsync();

        // Assert.
        Assert.Equal(expectedExists, actual);
    }

    [Theory(Skip = SkipReason)]
    [InlineData(true)]
    [InlineData(false)]
    public async Task ItCanCreateACollectionUpsertAndGetAsync(bool useRecordDefinition)
    {
        // Arrange
        var hotel = CreateTestHotel("Upsert-1");
    public async Task ItCanCreateACollectionUpsertGetAndSearchAsync(bool useRecordDefinition)
    public async Task ItCanCreateACollectionUpsertAndGetAsync(bool useRecordDefinition)
    {
        // Arrange
        var hotel = await CreateTestHotelAsync("Upsert-1");
    public async Task ItCanCreateACollectionUpsertGetAndSearchAsync(bool useRecordDefinition)
    {
        // Arrange
        var hotel = this.CreateTestHotel("Upsert-1");
        var testCollectionName = $"{fixture.TestIndexName}-createtest";
        var options = new AzureAISearchVectorStoreRecordCollectionOptions<AzureAISearchHotel>
        {
            VectorStoreRecordDefinition = useRecordDefinition ? fixture.VectorStoreRecordDefinition : null
        };
        var sut = new AzureAISearchVectorStoreRecordCollection<string, AzureAISearchHotel>(fixture.SearchIndexClient, testCollectionName, options);

        await sut.DeleteCollectionAsync();

        // Act
        await sut.CreateCollectionAsync();
        var upsertResult = await sut.UpsertAsync(hotel);
<<<<<<< HEAD
        var getResult = await sut.GetAsync("Upsert-1");
        var embedding = new ReadOnlyMemory<float>(AzureAISearchVectorStoreFixture.CreateTestEmbedding());
        var embedding = await fixture.EmbeddingGenerator.GenerateEmbeddingAsync("A great hotel");
        var searchResult = await sut.VectorizedSearchAsync(
=======
        var getResult = await sut.GetAsync("Upsert-1", new() { IncludeVectors = true });
        var embedding = fixture.Embedding;
        var searchResults = await sut.VectorizedSearchAsync(
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            embedding,
            top: 3,
            new()
            {
                IncludeVectors = true,
<<<<<<< HEAD
                Filter = new VectorSearchFilter().EqualTo("HotelName", "MyHotel Upsert-1")
=======
                OldFilter = new VectorSearchFilter().EqualTo("HotelName", "MyHotel Upsert-1")
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            }).ToListAsync();

        // Assert
        var collectionExistResult = await sut.CollectionExistsAsync();
        Assert.True(collectionExistResult);
        await sut.DeleteCollectionAsync();

        Assert.NotNull(upsertResult);
        Assert.Equal("Upsert-1", upsertResult);

        Assert.NotNull(getResult);
        Assert.Equal(hotel.HotelName, getResult.HotelName);
        Assert.Equal(hotel.Description, getResult.Description);
        Assert.NotNull(getResult.DescriptionEmbedding);
        Assert.Equal(hotel.DescriptionEmbedding?.ToArray(), getResult.DescriptionEmbedding?.ToArray());
        Assert.Equal(hotel.Tags, getResult.Tags);
        Assert.Equal(hotel.ParkingIncluded, getResult.ParkingIncluded);
        Assert.Equal(hotel.LastRenovationDate, getResult.LastRenovationDate);
        Assert.Equal(hotel.Rating, getResult.Rating);

        Assert.Single(searchResults);
        var searchResultRecord = searchResults.First().Record;
        Assert.Equal(hotel.HotelName, searchResultRecord.HotelName);
        Assert.Equal(hotel.Description, searchResultRecord.Description);
        Assert.NotNull(searchResultRecord.DescriptionEmbedding);
        Assert.Equal(hotel.DescriptionEmbedding?.ToArray(), searchResultRecord.DescriptionEmbedding?.ToArray());
        Assert.Equal(hotel.Tags, searchResultRecord.Tags);
        Assert.Equal(hotel.ParkingIncluded, searchResultRecord.ParkingIncluded);
        Assert.Equal(hotel.LastRenovationDate, searchResultRecord.LastRenovationDate);
        Assert.Equal(hotel.Rating, searchResultRecord.Rating);
        // Output
        output.WriteLine(collectionExistResult.ToString());
        output.WriteLine(upsertResult);
        output.WriteLine(getResult.ToString());
    }

    [Fact(Skip = SkipReason)]
    public async Task ItCanDeleteCollectionAsync()
    {
        // Arrange
        var tempCollectionName = fixture.TestIndexName + "-delete";
        await AzureAISearchVectorStoreFixture.CreateIndexAsync(tempCollectionName, fixture.SearchIndexClient);
        var sut = new AzureAISearchVectorStoreRecordCollection<string, AzureAISearchHotel>(fixture.SearchIndexClient, tempCollectionName);

        // Act
        await sut.DeleteCollectionAsync();

        // Assert
        Assert.False(await sut.CollectionExistsAsync());
    }

    [Theory(Skip = SkipReason)]
    [InlineData(true)]
    [InlineData(false)]
    public async Task ItCanUpsertDocumentToVectorStoreAsync(bool useRecordDefinition)
    {
        // Arrange
        var options = new AzureAISearchVectorStoreRecordCollectionOptions<AzureAISearchHotel>
        {
            VectorStoreRecordDefinition = useRecordDefinition ? fixture.VectorStoreRecordDefinition : null
        };
        var sut = new AzureAISearchVectorStoreRecordCollection<string, AzureAISearchHotel>(fixture.SearchIndexClient, fixture.TestIndexName, options);

        // Act
<<<<<<< HEAD
        var hotel = CreateTestHotel("Upsert-1");
        var hotel = await this.CreateTestHotelAsync("Upsert-1");
        var hotel = await CreateTestHotelAsync("Upsert-1");
=======
        var hotel = this.CreateTestHotel("Upsert-1");
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        var upsertResult = await sut.UpsertAsync(hotel);
        var getResult = await sut.GetAsync("Upsert-1", new() { IncludeVectors = true });

        // Assert
        Assert.NotNull(upsertResult);
        Assert.Equal("Upsert-1", upsertResult);

        Assert.NotNull(getResult);
        Assert.Equal(hotel.HotelName, getResult.HotelName);
        Assert.Equal(hotel.Description, getResult.Description);
        Assert.NotNull(getResult.DescriptionEmbedding);
        Assert.Equal(hotel.DescriptionEmbedding?.ToArray(), getResult.DescriptionEmbedding?.ToArray());
        Assert.Equal(hotel.Tags, getResult.Tags);
        Assert.Equal(hotel.ParkingIncluded, getResult.ParkingIncluded);
        Assert.Equal(hotel.LastRenovationDate, getResult.LastRenovationDate);
        Assert.Equal(hotel.Rating, getResult.Rating);

        // Output
        output.WriteLine(upsertResult);
        output.WriteLine(getResult.ToString());
    }

    [Fact(Skip = SkipReason)]
    public async Task ItCanUpsertManyDocumentsToVectorStoreAsync()
    {
        // Arrange
        var sut = new AzureAISearchVectorStoreRecordCollection<string, AzureAISearchHotel>(fixture.SearchIndexClient, fixture.TestIndexName);

        // Act
        var results = await sut.UpsertAsync(
            [
<<<<<<< HEAD
                CreateTestHotel("UpsertMany-1"),
                CreateTestHotel("UpsertMany-2"),
                CreateTestHotel("UpsertMany-3"),
                await CreateTestHotelAsync("UpsertMany-1"),
                await CreateTestHotelAsync("UpsertMany-2"),
                await CreateTestHotelAsync("UpsertMany-3"),
                await this.CreateTestHotelAsync("UpsertMany-1"),
                await this.CreateTestHotelAsync("UpsertMany-2"),
                await this.CreateTestHotelAsync("UpsertMany-3"),
=======
                this.CreateTestHotel("UpsertMany-1"),
                this.CreateTestHotel("UpsertMany-2"),
                this.CreateTestHotel("UpsertMany-3"),
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            ]);

        // Assert
        Assert.NotNull(results);

        Assert.Equal(3, results.Count);
        Assert.Contains("UpsertMany-1", results);
        Assert.Contains("UpsertMany-2", results);
        Assert.Contains("UpsertMany-3", results);

        // Output
        foreach (var result in results)
        {
            output.WriteLine(result);
        }
    }

    [Theory(Skip = SkipReason)]
    [InlineData(true, true)]
    [InlineData(true, false)]
    [InlineData(false, true)]
    [InlineData(false, false)]
    public async Task ItCanGetDocumentFromVectorStoreAsync(bool includeVectors, bool useRecordDefinition)
    {
        // Arrange
        var options = new AzureAISearchVectorStoreRecordCollectionOptions<AzureAISearchHotel>
        {
            VectorStoreRecordDefinition = useRecordDefinition ? fixture.VectorStoreRecordDefinition : null
        };
        var sut = new AzureAISearchVectorStoreRecordCollection<string, AzureAISearchHotel>(fixture.SearchIndexClient, fixture.TestIndexName, options);

        // Act
        var getResult = await sut.GetAsync("BaseSet-1", new GetRecordOptions { IncludeVectors = includeVectors });

        // Assert
        Assert.NotNull(getResult);

        Assert.Equal("Hotel 1", getResult.HotelName);
        Assert.Equal("This is a great hotel", getResult.Description);
        Assert.Equal(includeVectors, getResult.DescriptionEmbedding != null);
        if (includeVectors)
        {
<<<<<<< HEAD
            Assert.Equal(AzureAISearchVectorStoreFixture.CreateTestEmbedding(), getResult.DescriptionEmbedding!.Value.ToArray());
            Assert.Equal(new[] { 30f, 31f, 32f, 33f }, getResult.DescriptionEmbedding!.Value.ToArray());
            var embedding = await fixture.EmbeddingGenerator.GenerateEmbeddingAsync("This is a great hotel");
=======
            var embedding = fixture.Embedding;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            Assert.Equal(embedding, getResult.DescriptionEmbedding!.Value.ToArray());
        }
        else
        {
            Assert.Null(getResult.DescriptionEmbedding);
        }
        Assert.Equal(new[] { "pool", "air conditioning", "concierge" }, getResult.Tags);
        Assert.False(getResult.ParkingIncluded);
        Assert.Equal(new DateTimeOffset(1970, 1, 18, 0, 0, 0, TimeSpan.Zero), getResult.LastRenovationDate);
        Assert.Equal(3.6, getResult.Rating);

        // Output
        output.WriteLine(getResult.ToString());
    }

    [Fact(Skip = SkipReason)]
    public async Task ItCanGetManyDocumentsFromVectorStoreAsync()
    {
        // Arrange
        var sut = new AzureAISearchVectorStoreRecordCollection<string, AzureAISearchHotel>(fixture.SearchIndexClient, fixture.TestIndexName);

        // Act
        // Also include one non-existing key to test that the operation does not fail for these and returns only the found ones.
        var hotels = sut.GetAsync(["BaseSet-1", "BaseSet-2", "BaseSet-3", "BaseSet-5", "BaseSet-4"], new GetRecordOptions { IncludeVectors = true });

        // Assert
        Assert.NotNull(hotels);
        var hotelsList = await hotels.ToListAsync();
        Assert.Equal(4, hotelsList.Count);

        // Output
        foreach (var hotel in hotelsList)
        {
            output.WriteLine(hotel.ToString());
        }
    }

    [Theory(Skip = SkipReason)]
    [InlineData(true)]
    [InlineData(false)]
    public async Task ItCanRemoveDocumentFromVectorStoreAsync(bool useRecordDefinition)
    {
        // Arrange
        var options = new AzureAISearchVectorStoreRecordCollectionOptions<AzureAISearchHotel>
        {
            VectorStoreRecordDefinition = useRecordDefinition ? fixture.VectorStoreRecordDefinition : null
        };
<<<<<<< HEAD
        var sut = new AzureAISearchVectorStoreRecordCollection<Hotel>(fixture.SearchIndexClient, fixture.TestIndexName);
        await sut.UpsertAsync(CreateTestHotel("Remove-1"));
        await sut.UpsertAsync(await CreateTestHotelAsync("Remove-1"));
        var sut = new AzureAISearchVectorStoreRecordCollection<AzureAISearchHotel>(fixture.SearchIndexClient, fixture.TestIndexName);
        await sut.UpsertAsync(await this.CreateTestHotelAsync("Remove-1"));
        await sut.UpsertAsync(await CreateTestHotelAsync("Remove-1"));
=======
        var sut = new AzureAISearchVectorStoreRecordCollection<string, AzureAISearchHotel>(fixture.SearchIndexClient, fixture.TestIndexName);
        await sut.UpsertAsync(this.CreateTestHotel("Remove-1"));
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Act
        await sut.DeleteAsync("Remove-1");
        // Also delete a non-existing key to test that the operation does not fail for these.
        await sut.DeleteAsync("Remove-2");

        // Assert
        Assert.Null(await sut.GetAsync("Remove-1", new GetRecordOptions { IncludeVectors = true }));
    }

    [Fact(Skip = SkipReason)]
    public async Task ItCanRemoveManyDocumentsFromVectorStoreAsync()
    {
        // Arrange
<<<<<<< HEAD
        var sut = new AzureAISearchVectorStoreRecordCollection<Hotel>(fixture.SearchIndexClient, fixture.TestIndexName);
        await sut.UpsertAsync(CreateTestHotel("RemoveMany-1"));
        await sut.UpsertAsync(CreateTestHotel("RemoveMany-2"));
        await sut.UpsertAsync(CreateTestHotel("RemoveMany-3"));
        await sut.UpsertAsync(CreateTestHotel("RemoveMany-1"));
        await sut.UpsertAsync(CreateTestHotel("RemoveMany-2"));
        await sut.UpsertAsync(CreateTestHotel("RemoveMany-3"));
        await sut.UpsertAsync(await CreateTestHotelAsync("RemoveMany-1"));
        await sut.UpsertAsync(await CreateTestHotelAsync("RemoveMany-2"));
        await sut.UpsertAsync(await CreateTestHotelAsync("RemoveMany-3"));
        await sut.UpsertAsync(await CreateTestHotelAsync("RemoveMany-1"));
        await sut.UpsertAsync(await CreateTestHotelAsync("RemoveMany-2"));
        await sut.UpsertAsync(await CreateTestHotelAsync("RemoveMany-3"));
        var sut = new AzureAISearchVectorStoreRecordCollection<AzureAISearchHotel>(fixture.SearchIndexClient, fixture.TestIndexName);
        await sut.UpsertAsync(await this.CreateTestHotelAsync("RemoveMany-1"));
        await sut.UpsertAsync(await this.CreateTestHotelAsync("RemoveMany-2"));
        await sut.UpsertAsync(await this.CreateTestHotelAsync("RemoveMany-3"));
=======
        var sut = new AzureAISearchVectorStoreRecordCollection<string, AzureAISearchHotel>(fixture.SearchIndexClient, fixture.TestIndexName);
        await sut.UpsertAsync(this.CreateTestHotel("RemoveMany-1"));
        await sut.UpsertAsync(this.CreateTestHotel("RemoveMany-2"));
        await sut.UpsertAsync(this.CreateTestHotel("RemoveMany-3"));
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Act
        // Also include a non-existing key to test that the operation does not fail for these.
        await sut.DeleteAsync(["RemoveMany-1", "RemoveMany-2", "RemoveMany-3", "RemoveMany-4"]);

        // Assert
        Assert.Null(await sut.GetAsync("RemoveMany-1", new GetRecordOptions { IncludeVectors = true }));
        Assert.Null(await sut.GetAsync("RemoveMany-2", new GetRecordOptions { IncludeVectors = true }));
        Assert.Null(await sut.GetAsync("RemoveMany-3", new GetRecordOptions { IncludeVectors = true }));
    }

    [Fact(Skip = SkipReason)]
    public async Task ItReturnsNullWhenGettingNonExistentRecordAsync()
    {
        // Arrange
        var sut = new AzureAISearchVectorStoreRecordCollection<string, AzureAISearchHotel>(fixture.SearchIndexClient, fixture.TestIndexName);

        // Act & Assert
        Assert.Null(await sut.GetAsync("BaseSet-5", new GetRecordOptions { IncludeVectors = true }));
    }

    [Fact(Skip = SkipReason)]
    public async Task ItThrowsOperationExceptionForFailedConnectionAsync()
    {
        // Arrange
        var searchIndexClient = new SearchIndexClient(new Uri("https://localhost:12345"), new AzureKeyCredential("12345"));
        var sut = new AzureAISearchVectorStoreRecordCollection<string, AzureAISearchHotel>(searchIndexClient, fixture.TestIndexName);

        // Act & Assert
        await Assert.ThrowsAsync<VectorStoreOperationException>(async () => await sut.GetAsync("BaseSet-1", new GetRecordOptions { IncludeVectors = true }));
    }

    [Fact(Skip = SkipReason)]
    public async Task ItThrowsOperationExceptionForFailedAuthenticationAsync()
    {
        // Arrange
        var searchIndexClient = new SearchIndexClient(new Uri(fixture.Config.ServiceUrl), new AzureKeyCredential("12345"));
        var sut = new AzureAISearchVectorStoreRecordCollection<string, AzureAISearchHotel>(searchIndexClient, fixture.TestIndexName);

        // Act & Assert
        await Assert.ThrowsAsync<VectorStoreOperationException>(async () => await sut.GetAsync("BaseSet-1", new GetRecordOptions { IncludeVectors = true }));
    }

    [Theory(Skip = SkipReason)]
    [InlineData("equality", true)]
    [InlineData("tagContains", false)]
    public async Task ItCanSearchWithVectorAndFiltersAsync(string option, bool includeVectors)
    {
        // Arrange.
        var sut = new AzureAISearchVectorStoreRecordCollection<string, AzureAISearchHotel>(fixture.SearchIndexClient, fixture.TestIndexName);

        // Act.
        var filter = option == "equality" ? new VectorSearchFilter().EqualTo("HotelName", "Hotel 3") : new VectorSearchFilter().AnyTagEqualTo("Tags", "bar");
<<<<<<< HEAD
        var searchResults = sut.VectorizedSearchAsync(
        var actual = await sut.VectorizedSearchAsync(
            await fixture.EmbeddingGenerator.GenerateEmbeddingAsync("A great hotel"),
=======
        var searchResults = await sut.VectorizedSearchAsync(
            fixture.Embedding,
            top: 3,
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            new()
            {
                IncludeVectors = includeVectors,
                VectorProperty = r => r.DescriptionEmbedding,
                OldFilter = filter,
            }).ToListAsync();

        // Assert.
<<<<<<< HEAD
        Assert.NotNull(searchResults);
        var searchResultsList = await searchResults.ToListAsync();
        Assert.Single(searchResultsList);
        var searchResult = searchResultsList.First();
        var searchResults = await actual.Results.ToListAsync();
=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        Assert.Single(searchResults);
        var searchResult = searchResults.First();
        Assert.Equal("BaseSet-3", searchResult.Record.HotelId);
        Assert.Equal("Hotel 3", searchResult.Record.HotelName);
        Assert.Equal("This is a great hotel", searchResult.Record.Description);
        Assert.Equal(new[] { "air conditioning", "bar", "continental breakfast" }, searchResult.Record.Tags);
        Assert.True(searchResult.Record.ParkingIncluded);
        Assert.Equal(new DateTimeOffset(2015, 9, 20, 0, 0, 0, TimeSpan.Zero), searchResult.Record.LastRenovationDate);
        Assert.Equal(4.8, searchResult.Record.Rating);
        if (includeVectors)
        {
            Assert.NotNull(searchResult.Record.DescriptionEmbedding);
            var embedding = fixture.Embedding;
            Assert.Equal(embedding, searchResult.Record.DescriptionEmbedding!.Value.ToArray());
        }
        else
        {
            Assert.Null(searchResult.Record.DescriptionEmbedding);
        }
    }

    [Fact(Skip = SkipReason)]
    public async Task ItCanSearchWithVectorizableTextAndFiltersAsync()
    {
        // Arrange.
        var sut = new AzureAISearchVectorStoreRecordCollection<string, AzureAISearchHotel>(fixture.SearchIndexClient, fixture.TestIndexName);

        // Act.
        var filter = new VectorSearchFilter().EqualTo("HotelName", "Hotel 3");
<<<<<<< HEAD
        var searchResults = sut.VectorizableTextSearchAsync(
        var actual = await sut.VectorizableTextSearchAsync(
=======
        var searchResults = await sut.VectorizableTextSearchAsync(
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            "A hotel with great views.",
            top: 3,
            new()
            {
                VectorProperty = r => r.DescriptionEmbedding,
                OldFilter = filter,
            }).ToListAsync();

        // Assert.
<<<<<<< HEAD
        Assert.NotNull(searchResults);
        var searchResultsList = await searchResults.ToListAsync();
        Assert.Single(searchResultsList);
    }

        var searchResults = await actual.Results.ToListAsync();
=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        Assert.Single(searchResults);
    }

    [Fact(Skip = SkipReason)]
    public async Task ItCanUpsertAndRetrieveUsingTheDynamicMapperAsync()
    {
        // Arrange
        var options = new AzureAISearchVectorStoreRecordCollectionOptions<Dictionary<string, object?>>
        {
            VectorStoreRecordDefinition = fixture.VectorStoreRecordDefinition
        };
        var sut = new AzureAISearchVectorStoreRecordCollection<object, Dictionary<string, object?>>(fixture.SearchIndexClient, fixture.TestIndexName, options);

        // Act
        var baseSetGetResult = await sut.GetAsync("BaseSet-1", new GetRecordOptions { IncludeVectors = true });
<<<<<<< HEAD

        var baseSetEmbedding = await fixture.EmbeddingGenerator.GenerateEmbeddingAsync("This is a great hotel");
        var genericMapperEmbedding = await fixture.EmbeddingGenerator.GenerateEmbeddingAsync("This is a generic mapper hotel");
        var upsertResult = await sut.UpsertAsync(new VectorStoreGenericDataModel<string>("GenericMapper-1")
        {
            Data =
            {
                { "HotelName", "Generic Mapper Hotel" },
                { "Description", "This is a generic mapper hotel" },
                { "Tags", new string[] { "generic" } },
                { "ParkingIncluded", false },
                { "LastRenovationDate", new DateTimeOffset(1970, 1, 18, 0, 0, 0, TimeSpan.Zero) },
                { "Rating", 3.6d }
            },
            Vectors =
            {
                { "DescriptionEmbedding", new ReadOnlyMemory<float>(new[] { 30f, 31f, 32f, 33f }) }
                { "DescriptionEmbedding", genericMapperEmbedding }
            }
=======
        var baseSetEmbedding = fixture.Embedding;
        var dynamicMapperEmbedding = fixture.Embedding;
        var upsertResult = await sut.UpsertAsync(new Dictionary<string, object?>
        {
            ["HotelId"] = "DynamicMapper-1",

            ["HotelName"] = "Dynamic Mapper Hotel",
            ["Description"] = "This is a dynamic mapper hotel",
            ["Tags"] = new string[] { "dynamic" },
            ["ParkingIncluded"] = false,
            ["LastRenovationDate"] = new DateTimeOffset(1970, 1, 18, 0, 0, 0, TimeSpan.Zero),
            ["Rating"] = 3.6d,

            ["DescriptionEmbedding"] = dynamicMapperEmbedding
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        });
        var localGetResult = await sut.GetAsync("DynamicMapper-1", new GetRecordOptions { IncludeVectors = true });

        // Assert
        Assert.NotNull(baseSetGetResult);
<<<<<<< HEAD
        Assert.Equal("Hotel 1", baseSetGetResult.Data["HotelName"]);
        Assert.Equal("This is a great hotel", baseSetGetResult.Data["Description"]);
        Assert.Equal(new[] { "pool", "air conditioning", "concierge" }, baseSetGetResult.Data["Tags"]);
        Assert.False((bool?)baseSetGetResult.Data["ParkingIncluded"]);
        Assert.Equal(new DateTimeOffset(1970, 1, 18, 0, 0, 0, TimeSpan.Zero), baseSetGetResult.Data["LastRenovationDate"]);
        Assert.Equal(3.6d, baseSetGetResult.Data["Rating"]);
        Assert.Equal(new[] { 30f, 31f, 32f, 33f }, ((ReadOnlyMemory<float>)baseSetGetResult.Vectors["DescriptionEmbedding"]!).ToArray());
        Assert.Equal(baseSetEmbedding, (ReadOnlyMemory<float>)baseSetGetResult.Vectors["DescriptionEmbedding"]!);
        Assert.Equal(baseSetEmbedding, (ReadOnlyMemory<float>)baseSetGetResult.Vectors["DescriptionEmbedding"]!);
=======
        Assert.Equal("Hotel 1", baseSetGetResult["HotelName"]);
        Assert.Equal("This is a great hotel", baseSetGetResult["Description"]);
        Assert.Equal(new[] { "pool", "air conditioning", "concierge" }, baseSetGetResult["Tags"]);
        Assert.False((bool?)baseSetGetResult["ParkingIncluded"]);
        Assert.Equal(new DateTimeOffset(1970, 1, 18, 0, 0, 0, TimeSpan.Zero), baseSetGetResult["LastRenovationDate"]);
        Assert.Equal(3.6d, baseSetGetResult["Rating"]);
        Assert.Equal(baseSetEmbedding, (ReadOnlyMemory<float>)baseSetGetResult["DescriptionEmbedding"]!);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        Assert.NotNull(upsertResult);
        Assert.Equal("DynamicMapper-1", upsertResult);

        Assert.NotNull(localGetResult);
<<<<<<< HEAD
        Assert.Equal("Generic Mapper Hotel", localGetResult.Data["HotelName"]);
        Assert.Equal("This is a generic mapper hotel", localGetResult.Data["Description"]);
        Assert.Equal(new[] { "generic" }, localGetResult.Data["Tags"]);
        Assert.False((bool?)localGetResult.Data["ParkingIncluded"]);
        Assert.Equal(new DateTimeOffset(1970, 1, 18, 0, 0, 0, TimeSpan.Zero), localGetResult.Data["LastRenovationDate"]);
        Assert.Equal(3.6d, localGetResult.Data["Rating"]);
        Assert.Equal(new[] { 30f, 31f, 32f, 33f }, ((ReadOnlyMemory<float>)localGetResult.Vectors["DescriptionEmbedding"]!).ToArray());
    }

    private static Hotel CreateTestHotel(string hotelId) => new()
        Assert.Equal(genericMapperEmbedding, (ReadOnlyMemory<float>)localGetResult.Vectors["DescriptionEmbedding"]!);
    }

    private static Hotel CreateTestHotel(string hotelId) => new()
    private async Task<Hotel> CreateTestHotelAsync(string hotelId) => new()
        Assert.Equal(genericMapperEmbedding, (ReadOnlyMemory<float>)localGetResult.Vectors["DescriptionEmbedding"]!);
    }

    private async Task<Hotel> CreateTestHotelAsync(string hotelId) => new()
    private async Task<AzureAISearchHotel> CreateTestHotelAsync(string hotelId) => new()
=======
        Assert.Equal("Dynamic Mapper Hotel", localGetResult["HotelName"]);
        Assert.Equal("This is a dynamic mapper hotel", localGetResult["Description"]);
        Assert.Equal(new[] { "dynamic" }, localGetResult["Tags"]);
        Assert.False((bool?)localGetResult["ParkingIncluded"]);
        Assert.Equal(new DateTimeOffset(1970, 1, 18, 0, 0, 0, TimeSpan.Zero), localGetResult["LastRenovationDate"]);
        Assert.Equal(3.6d, localGetResult["Rating"]);
        Assert.Equal(dynamicMapperEmbedding, (ReadOnlyMemory<float>)localGetResult["DescriptionEmbedding"]!);
    }

    private AzureAISearchHotel CreateTestHotel(string hotelId) => new()
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        HotelId = hotelId,
        HotelName = $"MyHotel {hotelId}",
        Description = "My Hotel is great.",
<<<<<<< HEAD
        DescriptionEmbedding = new[] { 30f, 31f, 32f, 33f },
        DescriptionEmbedding = AzureAISearchVectorStoreFixture.CreateTestEmbedding(),
        DescriptionEmbedding = await fixture.EmbeddingGenerator.GenerateEmbeddingAsync("My hotel is great"),
=======
        DescriptionEmbedding = fixture.Embedding,
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        Tags = ["pool", "air conditioning", "concierge"],
        ParkingIncluded = true,
        LastRenovationDate = new DateTimeOffset(1970, 1, 18, 0, 0, 0, TimeSpan.Zero),
        Rating = 3.6
    };
}
