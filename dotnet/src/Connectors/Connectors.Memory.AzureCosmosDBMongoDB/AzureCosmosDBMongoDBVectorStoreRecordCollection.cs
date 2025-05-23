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
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Linq.Expressions;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.VectorData;
<<<<<<< HEAD
=======
using Microsoft.Extensions.VectorData.ConnectorSupport;
using Microsoft.Extensions.VectorData.Properties;
using Microsoft.SemanticKernel.Connectors.MongoDB;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using MongoDB.Driver;
using MEVD = Microsoft.Extensions.VectorData;

namespace Microsoft.SemanticKernel.Connectors.AzureCosmosDBMongoDB;

/// <summary>
/// Service for storing and retrieving vector records, that uses Azure CosmosDB MongoDB as the underlying storage.
/// </summary>
/// <typeparam name="TKey">The data type of the record key. Can be either <see cref="string"/>, or <see cref="object"/> for dynamic mapping.</typeparam>
/// <typeparam name="TRecord">The data model to use for adding, updating and retrieving data from storage.</typeparam>
#pragma warning disable CA1711 // Identifiers should not have incorrect suffix
public sealed class AzureCosmosDBMongoDBVectorStoreRecordCollection<TKey, TRecord> : IVectorStoreRecordCollection<TKey, TRecord>
    where TKey : notnull
    where TRecord : notnull
#pragma warning restore CA1711 // Identifiers should not have incorrect suffix
{
    /// <summary>Metadata about vector store record collection.</summary>
    private readonly VectorStoreRecordCollectionMetadata _collectionMetadata;

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
<<<<<<< main
=======
>>>>>>> upstream/main
=======
>>>>>>> head
>>>>>>> div
    /// <summary>Property name to be used for search similarity score value.</summary>
    private const string ScorePropertyName = "similarityScore";

    /// <summary>Property name to be used for search document value.</summary>
    private const string DocumentPropertyName = "document";

    /// <summary>The default options for vector search.</summary>
    private static readonly MEVD.VectorSearchOptions<TRecord> s_defaultVectorSearchOptions = new();

<<<<<<< main
<<<<<<< main
=======
<<<<<<< div
=======
>>>>>>> div
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
    /// <summary><see cref="IMongoDatabase"/> that can be used to manage the collections in Azure CosmosDB MongoDB.</summary>
    private readonly IMongoDatabase _mongoDatabase;

    /// <summary>Azure CosmosDB MongoDB collection to perform record operations.</summary>
    private readonly IMongoCollection<BsonDocument> _mongoCollection;

    /// <summary>Optional configuration options for this class.</summary>
    private readonly AzureCosmosDBMongoDBVectorStoreRecordCollectionOptions<TRecord> _options;

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
    /// <summary>A definition of the current storage model.</summary>
    private readonly VectorStoreRecordDefinition _vectorStoreRecordDefinition;

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
    /// <summary>A definition of the current storage model.</summary>
    private readonly VectorStoreRecordDefinition _vectorStoreRecordDefinition;

=======
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
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
    /// <summary>Interface for mapping between a storage model, and the consumer record data model.</summary>
    private readonly IMongoDBMapper<TRecord> _mapper;

<<<<<<< HEAD
    /// <summary>A dictionary that maps from a property name to the storage name that should be used when serializing it for data and vector properties.</summary>
    private readonly Dictionary<string, string> _storagePropertyNames;

    /// <summary>Collection of vector storage property names.</summary>
    private readonly List<string> _vectorStoragePropertyNames;

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
    /// <summary>Collection of record vector properties.</summary>
    private readonly List<VectorStoreRecordVectorProperty> _vectorProperties;
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
    /// <summary>Collection of record vector properties.</summary>
    private readonly List<VectorStoreRecordVectorProperty> _vectorProperties;
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
    /// <summary>Collection of record vector properties.</summary>
    private readonly List<VectorStoreRecordVectorProperty> _vectorProperties;
=======
>>>>>>> Stashed changes
=======
    /// <summary>Collection of record vector properties.</summary>
    private readonly List<VectorStoreRecordVectorProperty> _vectorProperties;
=======
>>>>>>> Stashed changes
>>>>>>> head
    /// <summary>A helper to access property information for the current data model and record definition.</summary>
    private readonly VectorStoreRecordPropertyReader _propertyReader;
=======
    /// <summary>The model for this collection.</summary>
    private readonly VectorStoreRecordModel _model;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

    /// <summary>Collection of record data properties.</summary>
    private readonly List<VectorStoreRecordDataProperty> _dataProperties;

    /// <summary>First vector property for the collections that this class is used with.</summary>
    private readonly VectorStoreRecordVectorProperty? _firstVectorProperty = null;
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
>>>>>>> head

    /// <inheritdoc />
    public string Name { get; }

    /// <summary>
    /// Initializes a new instance of the <see cref="AzureCosmosDBMongoDBVectorStoreRecordCollection{TKey, TRecord}"/> class.
    /// </summary>
    /// <param name="mongoDatabase"><see cref="IMongoDatabase"/> that can be used to manage the collections in Azure CosmosDB MongoDB.</param>
    /// <param name="name">The name of the collection that this <see cref="AzureCosmosDBMongoDBVectorStoreRecordCollection{TKey, TRecord}"/> will access.</param>
    /// <param name="options">Optional configuration options for this class.</param>
    public AzureCosmosDBMongoDBVectorStoreRecordCollection(
        IMongoDatabase mongoDatabase,
        string name,
        AzureCosmosDBMongoDBVectorStoreRecordCollectionOptions<TRecord>? options = default)
    {
        // Verify.
        Verify.NotNull(mongoDatabase);
<<<<<<< HEAD
        Verify.NotNullOrWhiteSpace(collectionName);
<<<<<<< main
<<<<<<< main
=======
>>>>>>> origin/main
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
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
        VectorStoreRecordPropertyVerification.VerifyGenericDataModelKeyType(typeof(TRecord), options?.BsonDocumentCustomMapper is not null, AzureCosmosDBMongoDBConstants.SupportedKeyTypes);
        VectorStoreRecordPropertyVerification.VerifyGenericDataModelDefinitionSupplied(typeof(TRecord), options?.VectorStoreRecordDefinition is not null);
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
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
        VectorStoreRecordPropertyVerification.VerifyGenericDataModelKeyType(typeof(TRecord), options?.BsonDocumentCustomMapper is not null, AzureCosmosDBMongoDBConstants.SupportedKeyTypes);
<<<<<<< main
=======
        VectorStoreRecordPropertyVerification.VerifyGenericDataModelKeyType(typeof(TRecord), options?.BsonDocumentCustomMapper is not null, MongoDBConstants.SupportedKeyTypes);
>>>>>>> upstream/main
=======
>>>>>>> origin/main
        VectorStoreRecordPropertyVerification.VerifyGenericDataModelDefinitionSupplied(typeof(TRecord), options?.VectorStoreRecordDefinition is not null);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
        Verify.NotNullOrWhiteSpace(name);

        if (typeof(TKey) != typeof(string) && typeof(TKey) != typeof(object))
        {
            throw new NotSupportedException("Only string keys are supported (and object for dynamic mapping)");
        }
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Assign.
        this._mongoDatabase = mongoDatabase;
        this._mongoCollection = mongoDatabase.GetCollection<BsonDocument>(name);
        this.Name = name;
        this._options = options ?? new AzureCosmosDBMongoDBVectorStoreRecordCollectionOptions<TRecord>();
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
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        this._vectorStoreRecordDefinition = this._options.VectorStoreRecordDefinition ?? VectorStoreRecordPropertyReader.CreateVectorStoreRecordDefinitionFromType(typeof(TRecord), true);

        var properties = VectorStoreRecordPropertyReader.SplitDefinitionAndVerify(
            typeof(TRecord).Name,
            this._vectorStoreRecordDefinition,
            supportsMultipleVectors: true,
            requiresAtLeastOneVector: false);

        this._storagePropertyNames = GetStoragePropertyNames(properties, typeof(TRecord));

        // Use Mongo reserved key property name as storage key property name
        this._storagePropertyNames[properties.KeyProperty.DataModelPropertyName] = AzureCosmosDBMongoDBConstants.MongoReservedKeyPropertyName;

<<<<<<< Updated upstream
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
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
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
        this._propertyReader = new VectorStoreRecordPropertyReader(typeof(TRecord), this._options.VectorStoreRecordDefinition, new() { RequiresAtLeastOneVector = false, SupportsMultipleKeys = false, SupportsMultipleVectors = true });

        this._storagePropertyNames = GetStoragePropertyNames(this._propertyReader.Properties, typeof(TRecord));

        // Use Mongo reserved key property name as storage key property name
        this._storagePropertyNames[this._propertyReader.KeyPropertyName] = AzureCosmosDBMongoDBConstants.MongoReservedKeyPropertyName;

        this._dataProperties = properties.DataProperties;
        this._vectorProperties = properties.VectorProperties;
        this._vectorStoragePropertyNames = this._vectorProperties.Select(property => this._storagePropertyNames[property.DataModelPropertyName]).ToList();

        if (this._vectorProperties.Count > 0)
        {
            this._firstVectorProperty = this._vectorProperties[0];
        }

        this._mapper = this._options.BsonDocumentCustomMapper ??
            new AzureCosmosDBMongoDBVectorStoreRecordMapper<TRecord>(
                this._vectorStoreRecordDefinition,
                properties.KeyProperty.DataModelPropertyName);
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
>>>>>>> head
        this._vectorProperties = properties.VectorProperties;
        this._vectorStoragePropertyNames = this._vectorProperties.Select(property => this._storagePropertyNames[property.DataModelPropertyName]).ToList();

        this._mapper = this._options.BsonDocumentCustomMapper ??
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
            new AzureCosmosDBMongoDBVectorStoreRecordMapper<TRecord>(this._vectorStoreRecordDefinition, properties.KeyProperty.DataModelPropertyName);
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
            new AzureCosmosDBMongoDBVectorStoreRecordMapper<TRecord>(this._vectorStoreRecordDefinition, properties.KeyProperty.DataModelPropertyName);
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
            new AzureCosmosDBMongoDBVectorStoreRecordMapper<TRecord>(this._vectorStoreRecordDefinition, properties.KeyProperty.DataModelPropertyName);
=======
>>>>>>> Stashed changes
=======
            new AzureCosmosDBMongoDBVectorStoreRecordMapper<TRecord>(this._vectorStoreRecordDefinition, properties.KeyProperty.DataModelPropertyName);
=======
>>>>>>> Stashed changes
>>>>>>> head
            new AzureCosmosDBMongoDBVectorStoreRecordMapper<TRecord>(this._vectorStoreRecordDefinition, this._storagePropertyNames);
        this._mapper = this.InitializeMapper(properties.KeyProperty);
        this._vectorStoragePropertyNames = this._propertyReader.VectorProperties.Select(property => this._storagePropertyNames[property.DataModelPropertyName]).ToList();


        this._vectorStoragePropertyNames = this._propertyReader.VectorProperties.Select(property => this._storagePropertyNames[property.DataModelPropertyName]).ToList();

        this._mapper = this.InitializeMapper();
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
>>>>>>> head
=======
        this._model = new MongoDBModelBuilder().Build(typeof(TRecord), this._options.VectorStoreRecordDefinition, this._options.EmbeddingGenerator);
        this._mapper = typeof(TRecord) == typeof(Dictionary<string, object?>)
            ? (new MongoDBDynamicDataModelMapper(this._model) as IMongoDBMapper<TRecord>)!
            : new MongoDBVectorStoreRecordMapper<TRecord>(this._model);

        this._collectionMetadata = new()
        {
            VectorStoreSystemName = AzureCosmosDBMongoDBConstants.VectorStoreSystemName,
            VectorStoreName = mongoDatabase.DatabaseNamespace?.DatabaseName,
            CollectionName = name
        };
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <inheritdoc />
    public Task<bool> CollectionExistsAsync(CancellationToken cancellationToken = default)
        => this.RunOperationAsync("ListCollectionNames", () => this.InternalCollectionExistsAsync(cancellationToken));

    /// <inheritdoc />
    public async Task CreateCollectionAsync(CancellationToken cancellationToken = default)
    {
        // The IMongoDatabase.CreateCollectionAsync "Creates a new collection if not already available".
        // To make sure that all the connectors are consistent, we throw when the collection exists.
        if (await this.CollectionExistsAsync(cancellationToken).ConfigureAwait(false))
        {
            throw new VectorStoreOperationException("Collection already exists.")
            {
                VectorStoreSystemName = AzureCosmosDBMongoDBConstants.VectorStoreSystemName,
                VectorStoreName = this._collectionMetadata.VectorStoreName,
                CollectionName = this.Name,
                OperationName = "CreateCollection"
            };
        }

<<<<<<< HEAD
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
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
        await this.RunOperationAsync("CreateIndexes",
            () => this.CreateIndexesAsync(this.CollectionName, cancellationToken: cancellationToken)).ConfigureAwait(false);
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
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
        await this.RunOperationAsync("CreateIndexes",
            () => this.CreateIndexesAsync(this.CollectionName, cancellationToken: cancellationToken)).ConfigureAwait(false);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
        await this.RunOperationAsync("CreateIndexes",
            () => this.CreateIndexesAsync(this.CollectionName, cancellationToken: cancellationToken)).ConfigureAwait(false);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
        await this.RunOperationAsync("CreateIndex",
            () => this.CreateIndexAsync(this.CollectionName, cancellationToken: cancellationToken)).ConfigureAwait(false);
=======
        await this.RunOperationAsync("CreateIndexes",
            () => this.CreateIndexesAsync(this.CollectionName, cancellationToken: cancellationToken)).ConfigureAwait(false);
>>>>>>> upstream/main
=======
        await this.CreateCollectionIfNotExistsAsync(cancellationToken).ConfigureAwait(false);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <inheritdoc />
    public async Task CreateCollectionIfNotExistsAsync(CancellationToken cancellationToken = default)
    {
        await this.RunOperationAsync("CreateCollection",
            () => this._mongoDatabase.CreateCollectionAsync(this.Name, cancellationToken: cancellationToken)).ConfigureAwait(false);

        await this.RunOperationAsync("CreateIndexes",
            () => this.CreateIndexesAsync(this.Name, cancellationToken: cancellationToken)).ConfigureAwait(false);
    }

    /// <inheritdoc />
    public async Task DeleteAsync(TKey key, CancellationToken cancellationToken = default)
    {
        var stringKey = this.GetStringKey(key);

        await this.RunOperationAsync("DeleteOne", () => this._mongoCollection.DeleteOneAsync(this.GetFilterById(stringKey), cancellationToken))
            .ConfigureAwait(false);
    }

    /// <inheritdoc />
    public async Task DeleteAsync(IEnumerable<TKey> keys, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(keys);

        var stringKeys = keys is IEnumerable<string> k ? k : keys.Cast<string>();

        await this.RunOperationAsync("DeleteMany", () => this._mongoCollection.DeleteManyAsync(this.GetFilterByIds(stringKeys), cancellationToken))
            .ConfigureAwait(false);
    }

    /// <inheritdoc />
    public Task DeleteCollectionAsync(CancellationToken cancellationToken = default)
        => this.RunOperationAsync("DropCollection", () => this._mongoDatabase.DropCollectionAsync(this.Name, cancellationToken));

    /// <inheritdoc />
    public async Task<TRecord?> GetAsync(TKey key, GetRecordOptions? options = null, CancellationToken cancellationToken = default)
    {
        const string OperationName = "Find";

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
=======
=======
        var stringKey = this.GetStringKey(key);

>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        var includeVectors = options?.IncludeVectors ?? false;
        if (includeVectors && this._model.VectorProperties.Any(p => p.EmbeddingGenerator is not null))
        {
            throw new NotSupportedException(VectorDataStrings.IncludeVectorsNotSupportedWithEmbeddingGeneration);
        }

>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
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
        var includeVectors = options?.IncludeVectors ?? false;

>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
        var record = await this.RunOperationAsync(OperationName, async () =>
        {
            using var cursor = await this
                .FindAsync(this.GetFilterById(stringKey), options, cancellationToken)
                .ConfigureAwait(false);

            return await cursor.SingleOrDefaultAsync(cancellationToken).ConfigureAwait(false);
        }).ConfigureAwait(false);

        if (record is null)
        {
            return default;
        }

        return VectorStoreErrorHandler.RunModelConversion(
            AzureCosmosDBMongoDBConstants.VectorStoreSystemName,
            this._collectionMetadata.VectorStoreName,
            this.Name,
            OperationName,
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
            () => this._mapper.MapFromStorageToDataModel(record, new()));
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
            () => this._mapper.MapFromStorageToDataModel(record, new()));
=======
            () => this._mapper.MapFromStorageToDataModel(record, new() { IncludeVectors = includeVectors }));
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
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
            () => this._mapper.MapFromStorageToDataModel(record, new() { IncludeVectors = includeVectors }));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
    }

    /// <inheritdoc />
    public async IAsyncEnumerable<TRecord> GetAsync(
        IEnumerable<TKey> keys,
        GetRecordOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        Verify.NotNull(keys);

        const string OperationName = "Find";

        if (options?.IncludeVectors == true && this._model.VectorProperties.Any(p => p.EmbeddingGenerator is not null))
        {
            throw new NotSupportedException(VectorDataStrings.IncludeVectorsNotSupportedWithEmbeddingGeneration);
        }

        var stringKeys = keys is IEnumerable<string> k ? k : keys.Cast<string>();

        using var cursor = await this
            .FindAsync(this.GetFilterByIds(stringKeys), options, cancellationToken)
            .ConfigureAwait(false);

        while (await cursor.MoveNextAsync(cancellationToken).ConfigureAwait(false))
        {
            foreach (var record in cursor.Current)
            {
                if (record is not null)
                {
                    yield return VectorStoreErrorHandler.RunModelConversion(
                        AzureCosmosDBMongoDBConstants.VectorStoreSystemName,
                        this._collectionMetadata.VectorStoreName,
                        this.Name,
                        OperationName,
                        () => this._mapper.MapFromStorageToDataModel(record, new()));
                }
            }
        }
    }

    /// <inheritdoc />
    public async Task<TKey> UpsertAsync(TRecord record, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(record);

        const string OperationName = "ReplaceOne";

        Embedding?[]? generatedEmbeddings = null;

        var vectorPropertyCount = this._model.VectorProperties.Count;
        for (var i = 0; i < vectorPropertyCount; i++)
        {
            var vectorProperty = this._model.VectorProperties[i];

            if (vectorProperty.EmbeddingGenerator is null)
            {
                continue;
            }

            // TODO: Ideally we'd group together vector properties using the same generator (and with the same input and output properties),
            // and generate embeddings for them in a single batch. That's some more complexity though.
            if (vectorProperty.TryGenerateEmbedding<TRecord, Embedding<float>, ReadOnlyMemory<float>>(record, cancellationToken, out var floatTask))
            {
                generatedEmbeddings ??= new Embedding?[vectorPropertyCount];
                generatedEmbeddings[i] = await floatTask.ConfigureAwait(false);
            }
            else if (vectorProperty.TryGenerateEmbedding<TRecord, Embedding<double>, ReadOnlyMemory<double>>(record, cancellationToken, out var doubleTask))
            {
                generatedEmbeddings ??= new Embedding?[vectorPropertyCount];
                generatedEmbeddings[i] = await doubleTask.ConfigureAwait(false);
            }
            else
            {
                throw new InvalidOperationException(
                    $"The embedding generator configured on property '{vectorProperty.ModelName}' cannot produce an embedding of type '{typeof(Embedding<float>).Name}' for the given input type.");
            }
        }

        var replaceOptions = new ReplaceOptions { IsUpsert = true };
        var storageModel = VectorStoreErrorHandler.RunModelConversion(
            AzureCosmosDBMongoDBConstants.VectorStoreSystemName,
            this._collectionMetadata.VectorStoreName,
            this.Name,
            OperationName,
            () => this._mapper.MapFromDataToStorageModel(record, generatedEmbeddings));

        var key = storageModel[AzureCosmosDBMongoDBConstants.MongoReservedKeyPropertyName].AsString;

        return await this.RunOperationAsync(OperationName, async () =>
        {
            await this._mongoCollection
                .ReplaceOneAsync(this.GetFilterById(key), storageModel, replaceOptions, cancellationToken)
                .ConfigureAwait(false);

            return (TKey)(object)key;
        }).ConfigureAwait(false);
    }

    /// <inheritdoc />
    public async Task<IReadOnlyList<TKey>> UpsertAsync(IEnumerable<TRecord> records, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(records);

        var tasks = records.Select(record => this.UpsertAsync(record, cancellationToken));
        var results = await Task.WhenAll(tasks).ConfigureAwait(false);
        return results.Where(r => r is not null).ToList();
    }

    #region Search

    /// <inheritdoc />
    public async IAsyncEnumerable<VectorSearchResult<TRecord>> SearchAsync<TInput>(
        TInput value,
        int top,
        MEVD.VectorSearchOptions<TRecord>? options = default,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
        where TInput : notnull
    {
        options ??= s_defaultVectorSearchOptions;
        var vectorProperty = this._model.GetVectorPropertyOrSingle(options);

        switch (vectorProperty.EmbeddingGenerator)
        {
            case IEmbeddingGenerator<TInput, Embedding<float>> generator:
            {
                var embedding = await generator.GenerateAsync(value, new() { Dimensions = vectorProperty.Dimensions }, cancellationToken).ConfigureAwait(false);

                await foreach (var record in this.SearchCoreAsync(embedding.Vector, top, vectorProperty, operationName: "Search", options, cancellationToken).ConfigureAwait(false))
                {
                    yield return record;
                }

                yield break;
            }

            case IEmbeddingGenerator<TInput, Embedding<double>> generator:
            {
                var embedding = await generator.GenerateAsync(value, new() { Dimensions = vectorProperty.Dimensions }, cancellationToken).ConfigureAwait(false);

                await foreach (var record in this.SearchCoreAsync(embedding.Vector, top, vectorProperty, operationName: "Search", options, cancellationToken).ConfigureAwait(false))
                {
                    yield return record;
                }

                yield break;
            }

            case null:
                throw new InvalidOperationException(VectorDataStrings.NoEmbeddingGeneratorWasConfiguredForSearch);

            default:
                throw new InvalidOperationException(
                    MongoDBConstants.SupportedVectorTypes.Contains(typeof(TInput))
                        ? string.Format(VectorDataStrings.EmbeddingTypePassedToSearchAsync)
                        : string.Format(VectorDataStrings.IncompatibleEmbeddingGeneratorWasConfiguredForInputType, typeof(TInput).Name, vectorProperty.EmbeddingGenerator.GetType().Name));
        }
    }
<<<<<<< HEAD
<<<<<<< Updated upstream
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

    #region private

=======
<<<<<<< Updated upstream
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

    /// <inheritdoc />
    public IAsyncEnumerable<VectorSearchResult<TRecord>> SearchEmbeddingAsync<TVector>(
        TVector vector,
        int top,
        MEVD.VectorSearchOptions<TRecord>? options = null,
        CancellationToken cancellationToken = default)
        where TVector : notnull
    {
        options ??= s_defaultVectorSearchOptions;
        var vectorProperty = this._model.GetVectorPropertyOrSingle(options);

        return this.SearchCoreAsync(vector, top, vectorProperty, operationName: "SearchEmbedding", options, cancellationToken);
    }

    private async IAsyncEnumerable<VectorSearchResult<TRecord>> SearchCoreAsync<TVector>(
        TVector vector,
        int top,
        VectorStoreRecordVectorPropertyModel vectorProperty,
        string operationName,
        MEVD.VectorSearchOptions<TRecord> options,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
        where TVector : notnull
    {
        Verify.NotNull(vector);
        Verify.NotLessThan(top, 1);

        Array vectorArray = vector switch
        {
            ReadOnlyMemory<float> memoryFloat => memoryFloat.ToArray(),
            ReadOnlyMemory<double> memoryDouble => memoryDouble.ToArray(),
            _ => throw new NotSupportedException(
                $"The provided vector type {vector.GetType().FullName} is not supported by the Azure CosmosDB for MongoDB connector. " +
                $"Supported types are: {string.Join(", ", [
                    typeof(ReadOnlyMemory<float>).FullName,
                    typeof(ReadOnlyMemory<double>).FullName])}")
        };

        if (options.IncludeVectors && this._model.VectorProperties.Any(p => p.EmbeddingGenerator is not null))
        {
            throw new NotSupportedException(VectorDataStrings.IncludeVectorsNotSupportedWithEmbeddingGeneration);
        }

#pragma warning disable CS0618 // VectorSearchFilter is obsolete
        var filter = options switch
        {
            { OldFilter: not null, Filter: not null } => throw new ArgumentException("Either Filter or OldFilter can be specified, but not both"),
            { OldFilter: VectorSearchFilter legacyFilter } => AzureCosmosDBMongoDBVectorStoreCollectionSearchMapping.BuildFilter(legacyFilter, this._model),
            { Filter: Expression<Func<TRecord, bool>> newFilter } => new AzureCosmosDBMongoDBFilterTranslator().Translate(newFilter, this._model),
            _ => null
        };
#pragma warning restore CS0618

        // Constructing a query to fetch "skip + top" total items
        // to perform skip logic locally, since skip option is not part of API.
        var itemsAmount = options.Skip + top;

        var vectorPropertyIndexKind = AzureCosmosDBMongoDBVectorStoreCollectionSearchMapping.GetVectorPropertyIndexKind(vectorProperty.IndexKind);

        var searchQuery = vectorPropertyIndexKind switch
        {
            IndexKind.Hnsw => AzureCosmosDBMongoDBVectorStoreCollectionSearchMapping.GetSearchQueryForHnswIndex(
                vectorArray,
                vectorProperty.StorageName,
                itemsAmount,
                this._options.EfSearch,
                filter),
            IndexKind.IvfFlat => AzureCosmosDBMongoDBVectorStoreCollectionSearchMapping.GetSearchQueryForIvfIndex(
                vectorArray,
                vectorProperty.StorageName,
                itemsAmount,
                filter),
            _ => throw new InvalidOperationException(
                $"Index kind '{vectorProperty.IndexKind}' on {nameof(VectorStoreRecordVectorProperty)} '{vectorProperty.StorageName}' is not supported by the Azure CosmosDB for MongoDB VectorStore. " +
                $"Supported index kinds are: {string.Join(", ", [IndexKind.Hnsw, IndexKind.IvfFlat])}")
        };

        var projectionQuery = AzureCosmosDBMongoDBVectorStoreCollectionSearchMapping.GetProjectionQuery(
            ScorePropertyName,
            DocumentPropertyName);

        BsonDocument[] pipeline = [searchQuery, projectionQuery];

        var cursor = await this._mongoCollection
            .AggregateAsync<BsonDocument>(pipeline, cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        await foreach (var result in this.EnumerateAndMapSearchResultsAsync(cursor, options, cancellationToken).ConfigureAwait(false))
        {
            yield return result;
        }
    }

    /// <inheritdoc />
    [Obsolete("Use either SearchEmbeddingAsync to search directly on embeddings, or SearchAsync to handle embedding generation internally as part of the call.")]
    public IAsyncEnumerable<VectorSearchResult<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, int top, MEVD.VectorSearchOptions<TRecord>? options = null, CancellationToken cancellationToken = default)
        where TVector : notnull
        => this.SearchEmbeddingAsync(vector, top, options, cancellationToken);

    #endregion Search

    /// <inheritdoc />
    public object? GetService(Type serviceType, object? serviceKey = null)
    {
        Verify.NotNull(serviceType);

        return
            serviceKey is not null ? null :
            serviceType == typeof(VectorStoreRecordCollectionMetadata) ? this._collectionMetadata :
            serviceType == typeof(IMongoDatabase) ? this._mongoDatabase :
            serviceType == typeof(IMongoCollection<BsonDocument>) ? this._mongoCollection :
            serviceType.IsInstanceOfType(this) ? this :
            null;
    }

    /// <inheritdoc />
    public async IAsyncEnumerable<TRecord> GetAsync(Expression<Func<TRecord, bool>> filter, int top,
        GetFilteredRecordOptions<TRecord>? options = null, [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        Verify.NotNull(filter);
        Verify.NotLessThan(top, 1);

        options ??= new();

        // Translate the filter now, so if it fails, we throw immediately.
        var translatedFilter = new AzureCosmosDBMongoDBFilterTranslator().Translate(filter, this._model);

        SortDefinition<BsonDocument>? sortDefinition = null;
        if (options.OrderBy.Values.Count > 0)
        {
            sortDefinition = Builders<BsonDocument>.Sort.Combine(
                options.OrderBy.Values.Select(pair =>
                {
                    var storageName = this._model.GetDataOrKeyProperty(pair.PropertySelector).StorageName;

                    return pair.Ascending
                        ? Builders<BsonDocument>.Sort.Ascending(storageName)
                        : Builders<BsonDocument>.Sort.Descending(storageName);
                }));
        }

        using IAsyncCursor<BsonDocument> cursor = await this.RunOperationAsync(
            "GetAsync",
            async () =>
            {
                return await this._mongoCollection.FindAsync(translatedFilter,
                    new()
                    {
                        Limit = top,
                        Skip = options.Skip,
                        Sort = sortDefinition
                    },
                    cancellationToken: cancellationToken).ConfigureAwait(false);
            }).ConfigureAwait(false);

        while (await cursor.MoveNextAsync(cancellationToken).ConfigureAwait(false))
        {
            foreach (var response in cursor.Current)
            {
                var record = VectorStoreErrorHandler.RunModelConversion(
                    AzureCosmosDBMongoDBConstants.VectorStoreSystemName,
                    this._collectionMetadata.VectorStoreName,
                    this.Name,
                    "GetAsync",
                    () => this._mapper.MapFromStorageToDataModel(response, new() { IncludeVectors = options.IncludeVectors }));

                yield return record;
            }
        }
    }

    #region private

<<<<<<< main
=======
<<<<<<< div
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
<<<<<<< Updated upstream
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
    /// <inheritdoc />
    public async IAsyncEnumerable<VectorSearchResult<TRecord>> VectorizedSearchAsync<TVector>(
        TVector vector,
        VectorSearchOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        const string OperationName = "Aggregate";

        Verify.NotNull(vector);

        Array vectorArray = vector switch
        {
            ReadOnlyMemory<float> memoryFloat => memoryFloat.ToArray(),
            ReadOnlyMemory<double> memoryDouble => memoryDouble.ToArray(),
            _ => throw new NotSupportedException(
                $"The provided vector type {vector.GetType().FullName} is not supported by the Azure CosmosDB for MongoDB connector. " +
                $"Supported types are: {string.Join(", ", [
                    typeof(ReadOnlyMemory<float>).FullName,
                    typeof(ReadOnlyMemory<double>).FullName])}")
        };

        var searchOptions = options ?? s_defaultVectorSearchOptions;
        var vectorProperty = this.GetVectorPropertyForSearch(searchOptions.VectorPropertyName);

        if (vectorProperty is null)
        {
            throw new InvalidOperationException("The collection does not have any vector properties, so vector search is not possible.");
        }

        var vectorPropertyName = this._storagePropertyNames[vectorProperty.DataModelPropertyName];

        var filter = AzureCosmosDBMongoDBVectorStoreCollectionSearchMapping.BuildFilter(
            searchOptions.Filter,
            this._storagePropertyNames);

        // Constructing a query to fetch "skip + top" total items
        // to perform skip logic locally, since skip option is not part of API. 
        var itemsAmount = searchOptions.Skip + searchOptions.Top;

        var searchQuery = vectorProperty.IndexKind switch
        {
            IndexKind.Hnsw => AzureCosmosDBMongoDBVectorStoreCollectionSearchMapping.GetSearchQueryForHnswIndex(
                vectorArray,
                vectorPropertyName,
                itemsAmount,
                this._options.EfSearch,
                filter),
            IndexKind.IvfFlat => AzureCosmosDBMongoDBVectorStoreCollectionSearchMapping.GetSearchQueryForIvfIndex(
                vectorArray,
                vectorPropertyName,
                itemsAmount,
                filter),
            _ => throw new InvalidOperationException(
                $"Index kind '{vectorProperty.IndexKind}' on {nameof(VectorStoreRecordVectorProperty)} '{vectorPropertyName}' is not supported by the Azure CosmosDB for MongoDB VectorStore. " +
                $"Supported index kinds are: {string.Join(", ", [IndexKind.Hnsw, IndexKind.IvfFlat])}")
        };

        var projectionQuery = AzureCosmosDBMongoDBVectorStoreCollectionSearchMapping.GetProjectionQuery(
            ScorePropertyName,
            DocumentPropertyName);

        BsonDocument[] pipeline = [searchQuery, projectionQuery];

        var cursor = await this._mongoCollection
            .AggregateAsync<BsonDocument>(pipeline, cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        var skipCounter = 0;

        while (await cursor.MoveNextAsync(cancellationToken).ConfigureAwait(false))
        {
            foreach (var response in cursor.Current)
            {
                if (skipCounter >= searchOptions.Skip)
                {
                    var score = response[ScorePropertyName].AsDouble;
                    var record = VectorStoreErrorHandler.RunModelConversion(
                        DatabaseName,
                        this.CollectionName,
                        OperationName,
                        () => this._mapper.MapFromStorageToDataModel(response[DocumentPropertyName].AsBsonDocument, new()));

                    yield return new VectorSearchResult<TRecord>(record, score);
                }

                skipCounter++;
            }
        }
    }

    #region private

    private async Task CreateIndexesAsync(string collectionName, CancellationToken cancellationToken)
    {
        var indexCursor = await this._mongoCollection.Indexes.ListAsync(cancellationToken).ConfigureAwait(false);
        var indexes = indexCursor.ToList(cancellationToken).Select(index => index["name"].ToString()) ?? [];
        var uniqueIndexes = new HashSet<string?>(indexes);

        var indexArray = new BsonArray();

        indexArray.AddRange(AzureCosmosDBMongoDBVectorStoreCollectionCreateMapping.GetVectorIndexes(
            this._model.VectorProperties,
            uniqueIndexes,
            this._options.NumLists,
            this._options.EfConstruction));

        indexArray.AddRange(AzureCosmosDBMongoDBVectorStoreCollectionCreateMapping.GetFilterableDataIndexes(
            this._model.DataProperties,
            uniqueIndexes));
    #region private

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
>>>>>>> head
    private async Task CreateIndexAsync(string collectionName, CancellationToken cancellationToken)
=======
    private async Task CreateIndexesAsync(string collectionName, CancellationToken cancellationToken)
>>>>>>> upstream/main
    {
        var indexCursor = await this._mongoCollection.Indexes.ListAsync(cancellationToken).ConfigureAwait(false);
        var indexes = indexCursor.ToList(cancellationToken).Select(index => index["name"].ToString()) ?? [];
        var uniqueIndexes = new HashSet<string?>(indexes);

        var indexArray = new BsonArray();

<<<<<<< main
        // Create separate index for each vector property
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
        foreach (var property in this._vectorStoreRecordDefinition.Properties.OfType<VectorStoreRecordVectorProperty>())
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
        foreach (var property in this._vectorStoreRecordDefinition.Properties.OfType<VectorStoreRecordVectorProperty>())
=======
        foreach (var property in this._propertyReader.VectorProperties)
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
        foreach (var property in this._propertyReader.VectorProperties)
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
        foreach (var property in this._propertyReader.VectorProperties)
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
        {
            // Use index name same as vector property name with underscore
            var vectorPropertyName = this._storagePropertyNames[property.DataModelPropertyName];
            var indexName = $"{vectorPropertyName}_";
=======
        indexArray.AddRange(AzureCosmosDBMongoDBVectorStoreCollectionCreateMapping.GetVectorIndexes(
            this._propertyReader.VectorProperties,
            this._storagePropertyNames,
            uniqueIndexes,
            this._options.NumLists,
            this._options.EfConstruction));
>>>>>>> upstream/main

        indexArray.AddRange(AzureCosmosDBMongoDBVectorStoreCollectionCreateMapping.GetFilterableDataIndexes(
            this._propertyReader.DataProperties,
            this._storagePropertyNames,
            uniqueIndexes));

        if (indexArray.Count > 0)
        {
            var createIndexCommand = new BsonDocument
            {
                { "createIndexes", collectionName },
                { "indexes", indexArray }
            };

            await this._mongoDatabase.RunCommandAsync<BsonDocument>(createIndexCommand, cancellationToken: cancellationToken).ConfigureAwait(false);
        }
    }

    private async Task<IAsyncCursor<BsonDocument>> FindAsync(FilterDefinition<BsonDocument> filter, GetRecordOptions? options, CancellationToken cancellationToken)
    {
        ProjectionDefinitionBuilder<BsonDocument> projectionBuilder = Builders<BsonDocument>.Projection;
        ProjectionDefinition<BsonDocument>? projectionDefinition = null;

        var includeVectors = options?.IncludeVectors ?? false;

        if (!includeVectors && this._model.VectorProperties.Count > 0)
        {
            foreach (var vectorProperty in this._model.VectorProperties)
            {
                projectionDefinition = projectionDefinition is not null ?
                    projectionDefinition.Exclude(vectorProperty.StorageName) :
                    projectionBuilder.Exclude(vectorProperty.StorageName);
            }
        }

        var findOptions = projectionDefinition is not null ?
            new FindOptions<BsonDocument> { Projection = projectionDefinition } :
            null;

        return await this._mongoCollection.FindAsync(filter, findOptions, cancellationToken).ConfigureAwait(false);
    }

    private async IAsyncEnumerable<VectorSearchResult<TRecord>> EnumerateAndMapSearchResultsAsync(
        IAsyncCursor<BsonDocument> cursor,
        MEVD.VectorSearchOptions<TRecord> searchOptions,
        [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        const string OperationName = "Aggregate";

        var skipCounter = 0;

        while (await cursor.MoveNextAsync(cancellationToken).ConfigureAwait(false))
        {
            foreach (var response in cursor.Current)
            {
                if (skipCounter >= searchOptions.Skip)
                {
                    var score = response[ScorePropertyName].AsDouble;
                    var record = VectorStoreErrorHandler.RunModelConversion(
                        AzureCosmosDBMongoDBConstants.VectorStoreSystemName,
                        this._collectionMetadata.VectorStoreName,
                        this.Name,
                        OperationName,
                        () => this._mapper.MapFromStorageToDataModel(response[DocumentPropertyName].AsBsonDocument, new()));

                    yield return new VectorSearchResult<TRecord>(record, score);
                }

                skipCounter++;
            }
        }
    }

    private FilterDefinition<BsonDocument> GetFilterById(string id)
        => Builders<BsonDocument>.Filter.Eq(document => document[AzureCosmosDBMongoDBConstants.MongoReservedKeyPropertyName], id);

    private FilterDefinition<BsonDocument> GetFilterByIds(IEnumerable<string> ids)
        => Builders<BsonDocument>.Filter.In(document => document[AzureCosmosDBMongoDBConstants.MongoReservedKeyPropertyName].AsString, ids);

    private async Task<bool> InternalCollectionExistsAsync(CancellationToken cancellationToken)
    {
        var filter = new BsonDocument("name", this.Name);
        var options = new ListCollectionNamesOptions { Filter = filter };

        using var cursor = await this._mongoDatabase.ListCollectionNamesAsync(options, cancellationToken: cancellationToken).ConfigureAwait(false);

        return await cursor.AnyAsync(cancellationToken).ConfigureAwait(false);
    }

    private async Task RunOperationAsync(string operationName, Func<Task> operation)
    {
        try
        {
            await operation.Invoke().ConfigureAwait(false);
        }
        catch (Exception ex)
        {
            throw new VectorStoreOperationException("Call to vector store failed.", ex)
            {
                VectorStoreSystemName = AzureCosmosDBMongoDBConstants.VectorStoreSystemName,
                VectorStoreName = this._collectionMetadata.VectorStoreName,
                CollectionName = this.Name,
                OperationName = operationName
            };
        }
    }

    private async Task<T> RunOperationAsync<T>(string operationName, Func<Task<T>> operation)
    {
        try
        {
            return await operation.Invoke().ConfigureAwait(false);
        }
        catch (Exception ex)
        {
            throw new VectorStoreOperationException("Call to vector store failed.", ex)
            {
                VectorStoreSystemName = AzureCosmosDBMongoDBConstants.VectorStoreSystemName,
                VectorStoreName = this._collectionMetadata.VectorStoreName,
                CollectionName = this.Name,
                OperationName = operationName
            };
        }
    }

    /// <summary>
    /// Gets storage property names taking into account BSON serialization attributes.
    /// </summary>
    private static Dictionary<string, string> GetStoragePropertyNames(
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
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        (VectorStoreRecordKeyProperty KeyProperty, List<VectorStoreRecordDataProperty> DataProperties, List<VectorStoreRecordVectorProperty> VectorProperties) properties,
        Type dataModel)
    {
        var storagePropertyNames = new Dictionary<string, string>();

        var allProperties = new List<VectorStoreRecordProperty>([properties.KeyProperty])
            .Concat(properties.DataProperties)
            .Concat(properties.VectorProperties);

        foreach (var property in allProperties)
        {
            var propertyInfo = dataModel.GetProperty(property.DataModelPropertyName);
<<<<<<< Updated upstream
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
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
=======
>>>>>>> Stashed changes
=======
=======
<<<<<<< div
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
>>>>>>> head
        IReadOnlyList<VectorStoreRecordProperty> properties,
        Type dataModel)
    {
        var storagePropertyNames = new Dictionary<string, string>();
        var storagePropertyNames = VectorStoreRecordPropertyReader.BuildPropertyNameToStorageNameMap(properties);

        foreach (var property in properties)
        {
            var propertyInfo = dataModel.GetProperty(property.DataModelPropertyName);
            string propertyName;
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
>>>>>>> head

            if (propertyInfo != null)
            {
                var bsonElementAttribute = propertyInfo.GetCustomAttribute<BsonElementAttribute>();

                storagePropertyNames[property.DataModelPropertyName] = bsonElementAttribute?.ElementName ?? property.DataModelPropertyName;
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
            }
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
            }
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
            }
=======
>>>>>>> Stashed changes
=======
            }
=======
>>>>>>> Stashed changes
>>>>>>> head
                if (bsonElementAttribute is not null)
                {
                    storagePropertyNames[property.DataModelPropertyName] = bsonElementAttribute.ElementName;
                }
                propertyName = bsonElementAttribute?.ElementName ?? property.DataModelPropertyName;
            }
            else
            {
                propertyName = property.DataModelPropertyName;
            }

            storagePropertyNames[property.DataModelPropertyName] = propertyName;
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
>>>>>>> head
        }

        return storagePropertyNames;
    }

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
    /// <summary>
    /// Get vector property to use for a search by using the storage name for the field name from options
    /// if available, and falling back to the first vector property in <typeparamref name="TRecord"/> if not.
    /// </summary>
    /// <param name="vectorFieldName">The vector field name.</param>
    /// <exception cref="InvalidOperationException">Thrown if the provided field name is not a valid field name.</exception>
    private VectorStoreRecordVectorProperty? GetVectorPropertyForSearch(string? vectorFieldName)
    {
        // If vector property name is provided in options, try to find it in schema or throw an exception.
        if (!string.IsNullOrWhiteSpace(vectorFieldName))
        {
            // Check vector properties by data model property name.
            var vectorProperty = this._propertyReader.VectorProperties
                .FirstOrDefault(l => l.DataModelPropertyName.Equals(vectorFieldName, StringComparison.Ordinal));

            if (vectorProperty is not null)
            {
                return vectorProperty;
            }

            throw new InvalidOperationException($"The {typeof(TRecord).FullName} type does not have a vector property named '{vectorFieldName}'.");
        }

        // If vector property is not provided in options, return first vector property from schema.
        return this._firstVectorProperty;
        return this._propertyReader.VectorProperty;
    }

    /// <summary>
    /// Get vector property to use for a search by using the storage name for the field name from options
    /// if available, and falling back to the first vector property in <typeparamref name="TRecord"/> if not.
    /// </summary>
    /// <param name="vectorFieldName">The vector field name.</param>
    /// <exception cref="InvalidOperationException">Thrown if the provided field name is not a valid field name.</exception>
    private VectorStoreRecordVectorProperty? GetVectorPropertyForSearch(string? vectorFieldName)
=======
    private string GetStringKey(TKey key)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        Verify.NotNull(key);

        var stringKey = key as string ?? throw new UnreachableException("string key should have been validated during model building");

        Verify.NotNullOrWhiteSpace(stringKey, nameof(key));

<<<<<<< HEAD
        // If vector property is not provided in options, return first vector property from schema.
        return this._propertyReader.VectorProperty;
    }

    /// <summary>
    /// Returns custom mapper, generic data model mapper or default record mapper.
    /// </summary>
    private IVectorStoreRecordMapper<TRecord, BsonDocument> InitializeMapper()
    {
        if (this._options.BsonDocumentCustomMapper is not null)
        {
            return this._options.BsonDocumentCustomMapper;
        }

        if (typeof(TRecord) == typeof(VectorStoreGenericDataModel<string>))
        {
            return (new AzureCosmosDBMongoDBGenericDataModelMapper(this._propertyReader.RecordDefinition) as IVectorStoreRecordMapper<TRecord, BsonDocument>)!;
        }

        return new AzureCosmosDBMongoDBVectorStoreRecordMapper<TRecord>(this._propertyReader);
=======
        return stringKey;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

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
>>>>>>> head
    #endregion
}
