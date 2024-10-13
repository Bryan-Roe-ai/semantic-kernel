<<<<<<< HEAD
<<<<<<< Updated upstream
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

using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.VectorData;
using MongoDB.Driver;
using Xunit;

namespace SemanticKernel.IntegrationTests.Connectors.AzureCosmosDBMongoDB;

public class AzureCosmosDBMongoDBVectorStoreFixture : IAsyncLifetime
{
    private readonly List<string> _testCollections = ["sk-test-hotels", "sk-test-contacts", "sk-test-addresses"];

    /// <summary>Main test collection for tests.</summary>
    public string TestCollection => this._testCollections[0];

    /// <summary><see cref="IMongoDatabase"/> that can be used to manage the collections in Azure CosmosDB MongoDB.</summary>
    public IMongoDatabase MongoDatabase { get; }

    /// <summary>Gets the manually created vector store record definition for Azure CosmosDB MongoDB test model.</summary>
    public VectorStoreRecordDefinition HotelVectorStoreRecordDefinition { get; private set; }

    /// <summary>
    /// Initializes a new instance of the <see cref="AzureCosmosDBMongoDBVectorStoreFixture"/> class.
    /// </summary>
    public AzureCosmosDBMongoDBVectorStoreFixture()
    {
        var configuration = new ConfigurationBuilder()
            .AddJsonFile(path: "testsettings.json", optional: false, reloadOnChange: true)
            .AddJsonFile(
                path: "testsettings.development.json",
                optional: false,
                reloadOnChange: true
            )
            .AddEnvironmentVariables()
            .Build();

        var connectionString = GetConnectionString(configuration);
        var client = new MongoClient(connectionString);

        this.MongoDatabase = client.GetDatabase("test");

        this.HotelVectorStoreRecordDefinition = new()
        {
            Properties =
            [
                new VectorStoreRecordKeyProperty("HotelId", typeof(string)),
                new VectorStoreRecordDataProperty("HotelName", typeof(string)),
                new VectorStoreRecordDataProperty("HotelCode", typeof(int)),
                new VectorStoreRecordDataProperty("ParkingIncluded", typeof(bool)) { StoragePropertyName = "parking_is_included" },
                new VectorStoreRecordDataProperty("HotelRating", typeof(float)),
                new VectorStoreRecordDataProperty("Tags", typeof(List<string>)),
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
                new VectorStoreRecordDataProperty("Timestamp", typeof(DateTime)),
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
                new VectorStoreRecordDataProperty("Timestamp", typeof(DateTime)),
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
=======
                new VectorStoreRecordDataProperty("Timestamp", typeof(DateTime)),
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
                new VectorStoreRecordDataProperty("Timestamp", typeof(DateTime)),
>>>>>>> main
>>>>>>> Stashed changes
                new VectorStoreRecordDataProperty("Description", typeof(string)),
                new VectorStoreRecordVectorProperty("DescriptionEmbedding", typeof(ReadOnlyMemory<float>?)) { Dimensions = 4, IndexKind = IndexKind.IvfFlat, DistanceFunction = DistanceFunction.CosineDistance }
            ]
        };
    }

    public async Task InitializeAsync()
    {
        foreach (var collection in this._testCollections)
        {
            await this.MongoDatabase.CreateCollectionAsync(collection);
        }
    }

    public async Task DisposeAsync()
    {
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
        var cursor = await this.MongoDatabase.ListCollectionNamesAsync();

        while (await cursor.MoveNextAsync().ConfigureAwait(false))
        {
            foreach (var collection in cursor.Current)
            {
                await this.MongoDatabase.DropCollectionAsync(collection);
            }
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
        foreach (var collection in this._testCollections)
=======
        var cursor = await this.MongoDatabase.ListCollectionNamesAsync();

        while (await cursor.MoveNextAsync().ConfigureAwait(false))
>>>>>>> upstream/main
        {
            foreach (var collection in cursor.Current)
            {
                await this.MongoDatabase.DropCollectionAsync(collection);
            }
        }
    }

#pragma warning disable CS8618
    public record AzureCosmosDBMongoDBHotel()
    {
        /// <summary>The key of the record.</summary>
        [VectorStoreRecordKey]
        public string HotelId { get; init; }

        /// <summary>A string metadata field.</summary>
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
        [VectorStoreRecordData(IsFilterable = true)]
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
        [VectorStoreRecordData(IsFilterable = true)]
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
=======
        [VectorStoreRecordData(IsFilterable = true)]
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
        [VectorStoreRecordData(IsFilterable = true)]
>>>>>>> main
>>>>>>> Stashed changes
        [VectorStoreRecordData]
=======
        [VectorStoreRecordData(IsFilterable = true)]
>>>>>>> upstream/main
        public string? HotelName { get; set; }

        /// <summary>An int metadata field.</summary>
        [VectorStoreRecordData]
        public int HotelCode { get; set; }

        /// <summary>A float metadata field.</summary>
        [VectorStoreRecordData]
        public float? HotelRating { get; set; }

        /// <summary>A bool metadata field.</summary>
        [VectorStoreRecordData(StoragePropertyName = "parking_is_included")]
        public bool ParkingIncluded { get; set; }

        /// <summary>An array metadata field.</summary>
        [VectorStoreRecordData]
        public List<string> Tags { get; set; } = [];

        /// <summary>A data field.</summary>
        [VectorStoreRecordData]
        public string Description { get; set; }

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
        /// <summary>A datetime metadata field.</summary>
        [VectorStoreRecordData]
        public DateTime Timestamp { get; set; }

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
        /// <summary>A vector field.</summary>
        [VectorStoreRecordVector(Dimensions: 4, IndexKind: IndexKind.IvfFlat, DistanceFunction: DistanceFunction.CosineDistance)]
        public ReadOnlyMemory<float>? DescriptionEmbedding { get; set; }
    }
#pragma warning restore CS8618

    #region private

    private static string GetConnectionString(IConfigurationRoot configuration)
    {
        var settingValue = configuration["AzureCosmosDBMongoDB:ConnectionString"];
        if (string.IsNullOrWhiteSpace(settingValue))
        {
            throw new ArgumentNullException($"{settingValue} string is not configured");
        }

        return settingValue;
    }

    #endregion
}
