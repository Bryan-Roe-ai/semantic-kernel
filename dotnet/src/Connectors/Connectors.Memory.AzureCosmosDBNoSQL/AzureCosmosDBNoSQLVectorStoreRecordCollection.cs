// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.Linq;
using System.Linq.Expressions;
using System.Runtime.CompilerServices;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Azure.Cosmos;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.VectorData;
using Microsoft.Extensions.VectorData.ConnectorSupport;
using Microsoft.Extensions.VectorData.Properties;
using DistanceFunction = Microsoft.Azure.Cosmos.DistanceFunction;
using IndexKind = Microsoft.Extensions.VectorData.IndexKind;
using MEAI = Microsoft.Extensions.AI;
using SKDistanceFunction = Microsoft.Extensions.VectorData.DistanceFunction;

namespace Microsoft.SemanticKernel.Connectors.AzureCosmosDBNoSQL;

/// <summary>
/// Service for storing and retrieving vector records, that uses Azure CosmosDB NoSQL as the underlying storage.
/// </summary>
/// <typeparam name="TKey">The data type of the record key. Can be either <see cref="string"/>, or <see cref="object"/> for dynamic mapping.</typeparam>
/// <typeparam name="TRecord">The data model to use for adding, updating and retrieving data from storage.</typeparam>
#pragma warning disable CA1711 // Identifiers should not have incorrect suffix
public sealed class AzureCosmosDBNoSQLVectorStoreRecordCollection<TKey, TRecord> : IVectorStoreRecordCollection<TKey, TRecord>, IKeywordHybridSearch<TRecord>
    where TKey : notnull
    where TRecord : notnull
#pragma warning restore CA1711 // Identifiers should not have incorrect
{
<<<<<<< HEAD
    /// <summary>The name of this database for telemetry purposes.</summary>
    private const string DatabaseName = "AzureCosmosDBNoSQL";

    /// <summary>A set of types that a key on the provided model may have.</summary>

    /// <summary>A <see cref="HashSet{T}"/> of types that a key on the provided model may have.</summary>

    private static readonly HashSet<Type> s_supportedKeyTypes =
    [
        typeof(string)
    ];

    /// <summary>A set of types that data properties on the provided model may have.</summary>
    private static readonly HashSet<Type> s_supportedDataTypes =
    [
        typeof(string),
        typeof(int),
        typeof(long),
        typeof(double),
        typeof(float),
        typeof(bool),
        typeof(DateTimeOffset),
        typeof(int?),
        typeof(long?),
        typeof(double?),
        typeof(float?),
        typeof(bool?),
        typeof(DateTimeOffset?),
    ];

    /// <summary>A set of types that vector properties on the provided model may have, based on <see cref="VectorDataType"/> enumeration.</summary>

    /// <summary>A <see cref="HashSet{T}"/> of types that data properties on the provided model may have.</summary>
    private static readonly HashSet<Type> s_supportedDataTypes =
    [
        typeof(bool),
        typeof(bool?),
        typeof(string),
        typeof(int),
        typeof(int?),
        typeof(long),
        typeof(long?),
        typeof(float),
        typeof(float?),
        typeof(double),
        typeof(double?),
        typeof(DateTimeOffset),
        typeof(DateTimeOffset?),
    ];

    /// <summary>A <see cref="HashSet{T}"/> of types that vector properties on the provided model may have, based on <see cref="VectorDataType"/> enumeration.</summary>

    private static readonly HashSet<Type> s_supportedVectorTypes =
    [
        // Float32
        typeof(ReadOnlyMemory<float>),
        typeof(ReadOnlyMemory<float>?),
        // Uint8
        typeof(ReadOnlyMemory<byte>),
        typeof(ReadOnlyMemory<byte>?),
        // Int8
        typeof(ReadOnlyMemory<sbyte>),
        typeof(ReadOnlyMemory<sbyte>?),
    ];
=======
    /// <summary>Metadata about vector store record collection.</summary>
    private readonly VectorStoreRecordCollectionMetadata _collectionMetadata;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

    /// <summary>The default options for vector search.</summary>
    private static readonly VectorSearchOptions<TRecord> s_defaultVectorSearchOptions = new();

    /// <summary>The default options for hybrid vector search.</summary>
    private static readonly HybridSearchOptions<TRecord> s_defaultKeywordVectorizedHybridSearchOptions = new();

    /// <summary><see cref="Database"/> that can be used to manage the collections in Azure CosmosDB NoSQL.</summary>
    private readonly Database _database;

    /// <summary>Optional configuration options for this class.</summary>
    private readonly AzureCosmosDBNoSQLVectorStoreRecordCollectionOptions<TRecord> _options;

<<<<<<< HEAD
    /// <summary>A definition of the current storage model.</summary>
    private readonly VectorStoreRecordDefinition _vectorStoreRecordDefinition;

    /// <summary>A helper to access property information for the current data model and record definition.</summary>
    private readonly VectorStoreRecordPropertyReader _propertyReader;

    /// <summary>The storage names of all non vector fields on the current model.</summary>
    private readonly List<string> _nonVectorStoragePropertyNames = [];

    /// <summary>A dictionary that maps from a property name to the storage name that should be used when serializing it to json for data and vector properties.</summary>
    private readonly Dictionary<string, string> _storagePropertyNames = [];

    /// <summary>The storage name of the key field for the collections that this class is used with.</summary>
    private readonly string _keyStoragePropertyName;

    /// <summary>The key property of the current storage model.</summary>
    private readonly VectorStoreRecordKeyProperty _keyProperty;

    /// <summary>The property name to use as partition key.</summary>
    private readonly string _partitionKeyPropertyName;

    /// <summary>The storage property name to use as partition key.</summary>
    private readonly string _partitionKeyStoragePropertyName;
=======
    /// <summary>The model for this collection.</summary>
    private readonly VectorStoreRecordModel _model;

    // TODO: Refactor this into the model (Co)
    /// <summary>The property to use as partition key.</summary>
    private readonly VectorStoreRecordPropertyModel _partitionKeyProperty;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

    /// <summary>The mapper to use when mapping between the consumer data model and the Azure CosmosDB NoSQL record.</summary>
    private readonly ICosmosNoSQLMapper<TRecord> _mapper;

    /// <inheritdoc />
    public string Name { get; }

    /// <summary>
    /// Initializes a new instance of the <see cref="AzureCosmosDBNoSQLVectorStoreRecordCollection{TKey, TRecord}"/> class.
    /// </summary>
    /// <param name="database"><see cref="Database"/> that can be used to manage the collections in Azure CosmosDB NoSQL.</param>
    /// <param name="name">The name of the collection that this <see cref="AzureCosmosDBNoSQLVectorStoreRecordCollection{TKey, TRecord}"/> will access.</param>
    /// <param name="options">Optional configuration options for this class.</param>
    public AzureCosmosDBNoSQLVectorStoreRecordCollection(
        Database database,
        string name,
        AzureCosmosDBNoSQLVectorStoreRecordCollectionOptions<TRecord>? options = default)
    {
        // Verify.
        Verify.NotNull(database);
        Verify.NotNullOrWhiteSpace(name);

        if (typeof(TKey) != typeof(string) && typeof(TKey) != typeof(AzureCosmosDBNoSQLCompositeKey) && typeof(TKey) != typeof(object))
        {
            throw new NotSupportedException($"Only {nameof(String)} and {nameof(AzureCosmosDBNoSQLCompositeKey)} keys are supported (and object for dynamic mapping).");
        }

        if (database.Client?.ClientOptions?.UseSystemTextJsonSerializerWithOptions is null)
        {
            throw new ArgumentException(
                $"Property {nameof(CosmosClientOptions.UseSystemTextJsonSerializerWithOptions)} in CosmosClient.ClientOptions " +
                $"is required to be configured for {nameof(AzureCosmosDBNoSQLVectorStoreRecordCollection<TKey, TRecord>)}.");
        }

        // Assign.
        this._database = database;
        this.Name = name;
        this._options = options ?? new();
        this._vectorStoreRecordDefinition = this._options.VectorStoreRecordDefinition ?? VectorStoreRecordPropertyReader.CreateVectorStoreRecordDefinitionFromType(typeof(TRecord), true);
        var jsonSerializerOptions = this._options.JsonSerializerOptions ?? JsonSerializerOptions.Default;

        // Validate property types.
        var properties = VectorStoreRecordPropertyReader.SplitDefinitionAndVerify(typeof(TRecord).Name, this._vectorStoreRecordDefinition, supportsMultipleVectors: true, requiresAtLeastOneVector: false);
        VectorStoreRecordPropertyReader.VerifyPropertyTypes([properties.KeyProperty], s_supportedKeyTypes, "Key");
        VectorStoreRecordPropertyReader.VerifyPropertyTypes(properties.DataProperties, s_supportedDataTypes, "Data", supportEnumerable: true);
        VectorStoreRecordPropertyReader.VerifyPropertyTypes(properties.VectorProperties, s_supportedVectorTypes, "Vector");

        // Get storage names and store for later use.
        this._keyProperty = properties.KeyProperty;
        this._storagePropertyNames = VectorStoreRecordPropertyReader.BuildPropertyNameToJsonPropertyNameMap(properties, typeof(TRecord), jsonSerializerOptions);

        // Assign mapper.
        this._mapper = this._options.JsonObjectCustomMapper ??
            new AzureCosmosDBNoSQLVectorStoreRecordMapper<TRecord>(
                this._storagePropertyNames[this._keyProperty.DataModelPropertyName],
                this._storagePropertyNames,
                jsonSerializerOptions);

        // Use Azure CosmosDB NoSQL reserved key property name as storage key property name.
        this._storagePropertyNames[this._keyProperty.DataModelPropertyName] = AzureCosmosDBNoSQLConstants.ReservedKeyPropertyName;
        var jsonSerializerOptions = this._options.JsonSerializerOptions ?? JsonSerializerOptions.Default;
        this._model = new AzureCosmosDBNoSQLVectorStoreModelBuilder()
            .Build(typeof(TRecord), this._options.VectorStoreRecordDefinition, this._options.EmbeddingGenerator, jsonSerializerOptions);

        // Assign mapper.
        this._mapper = typeof(TRecord) == typeof(Dictionary<string, object?>)
            ? (new AzureCosmosDBNoSQLDynamicDataModelMapper(this._model, jsonSerializerOptions) as ICosmosNoSQLMapper<TRecord>)!
            : new AzureCosmosDBNoSQLVectorStoreRecordMapper<TRecord>(this._model, this._options.JsonSerializerOptions);

<<<<<<< HEAD
        // Use Azure CosmosDB NoSQL reserved key property name as storage key property name.
        this._storagePropertyNames[this._propertyReader.KeyPropertyName] = AzureCosmosDBNoSQLConstants.ReservedKeyPropertyName;
        
        this._keyStoragePropertyName = AzureCosmosDBNoSQLConstants.ReservedKeyPropertyName;

        // If partition key is not provided, use key property as a partition key.
        this._partitionKeyPropertyName = !string.IsNullOrWhiteSpace(this._options.PartitionKeyPropertyName) ?
            this._options.PartitionKeyPropertyName! :
            this._keyProperty.DataModelPropertyName;

        VerifyPartitionKeyProperty(this._partitionKeyPropertyName, this._vectorStoreRecordDefinition);

        this._partitionKeyStoragePropertyName = this._storagePropertyNames[this._partitionKeyPropertyName];

        this._nonVectorStoragePropertyNames = properties.DataProperties
            .Cast<VectorStoreRecordProperty>()
            .Concat([properties.KeyProperty])

            this._propertyReader.KeyPropertyName;
=======
        // Setup partition key property
        if (this._options.PartitionKeyPropertyName is not null)
        {
            if (!this._model.PropertyMap.TryGetValue(this._options.PartitionKeyPropertyName, out var property))
            {
                throw new ArgumentException($"Partition key property '{this._options.PartitionKeyPropertyName}' is not part of the record definition.");
            }

            if (property.Type != typeof(string))
            {
                throw new ArgumentException("Partition key property must be string.");
            }
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

            this._partitionKeyProperty = property;
        }
        else
        {
            // If partition key is not provided, use key property as a partition key.
            this._partitionKeyProperty = this._model.KeyProperty;
        }

        this._collectionMetadata = new()
        {
            VectorStoreSystemName = AzureCosmosDBNoSQLConstants.VectorStoreSystemName,
            VectorStoreName = database.Id,
            CollectionName = name
        };
    }

    /// <inheritdoc />
    public Task<bool> CollectionExistsAsync(CancellationToken cancellationToken = default)
    {
        return this.RunOperationAsync("GetContainerQueryIterator", async () =>
        {
            const string Query = "SELECT VALUE(c.id) FROM c WHERE c.id = @collectionName";

            var queryDefinition = new QueryDefinition(Query).WithParameter("@collectionName", this.Name);

            using var feedIterator = this._database.GetContainerQueryIterator<string>(queryDefinition);

            while (feedIterator.HasMoreResults)
            {
                var next = await feedIterator.ReadNextAsync(cancellationToken).ConfigureAwait(false);

                foreach (var containerName in next.Resource)
                {
                    return true;
                }
            }

            return false;
        });
    }

    /// <inheritdoc />
    public Task CreateCollectionAsync(CancellationToken cancellationToken = default)
    {
        return this.RunOperationAsync("CreateContainer", () =>
            this._database.CreateContainerAsync(this.GetContainerProperties(), cancellationToken: cancellationToken));
    }

    /// <inheritdoc />
    public async Task CreateCollectionIfNotExistsAsync(CancellationToken cancellationToken = default)
    {
        if (!await this.CollectionExistsAsync(cancellationToken).ConfigureAwait(false))
        {
            await this.CreateCollectionAsync(cancellationToken).ConfigureAwait(false);
        }
    }

    /// <inheritdoc />
    public async Task DeleteCollectionAsync(CancellationToken cancellationToken = default)
    {
        try
        {
            await this._database
                .GetContainer(this.Name)
                .DeleteContainerAsync(cancellationToken: cancellationToken).ConfigureAwait(false);
        }
        catch (CosmosException ex) when (ex.StatusCode == System.Net.HttpStatusCode.NotFound)
        {
            // Do nothing, since the container is already deleted.
        }
        catch (CosmosException ex)
        {
            throw new VectorStoreOperationException("Call to vector store failed.", ex)
            {
                VectorStoreSystemName = AzureCosmosDBNoSQLConstants.VectorStoreSystemName,
                VectorStoreName = this._collectionMetadata.VectorStoreName,
                CollectionName = this.Name,
                OperationName = "DeleteContainer"
            };
        }
    }

    /// <inheritdoc />
    public Task DeleteAsync(TKey key, CancellationToken cancellationToken = default)
        => this.DeleteAsync([key], cancellationToken);

    /// <inheritdoc />
    public async Task DeleteAsync(IEnumerable<TKey> keys, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(keys);

        var tasks = GetCompositeKeys(keys).Select(key =>
        {
            Verify.NotNullOrWhiteSpace(key.RecordKey);
            Verify.NotNullOrWhiteSpace(key.PartitionKey);

            return this.RunOperationAsync("DeleteItem", () =>
                this._database
                    .GetContainer(this.Name)
                    .DeleteItemAsync<JsonObject>(key.RecordKey, new PartitionKey(key.PartitionKey), cancellationToken: cancellationToken));
        });

        await Task.WhenAll(tasks).ConfigureAwait(false);
    }

    /// <inheritdoc />
    public async Task<TRecord?> GetAsync(TKey key, GetRecordOptions? options = null, CancellationToken cancellationToken = default)
    {
        return await this.GetAsync([key], options, cancellationToken)
            .FirstOrDefaultAsync(cancellationToken)
            .ConfigureAwait(false);
    }

    /// <inheritdoc />
    public async IAsyncEnumerable<TRecord> GetAsync(
        IEnumerable<TKey> keys,
        GetRecordOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        Verify.NotNull(keys);

        const string OperationName = "GetItemQueryIterator";

        var includeVectors = options?.IncludeVectors ?? false;
        if (includeVectors && this._model.VectorProperties.Any(p => p.EmbeddingGenerator is not null))
        {
            throw new NotSupportedException(VectorDataStrings.IncludeVectorsNotSupportedWithEmbeddingGeneration);
        }

        var queryDefinition = AzureCosmosDBNoSQLVectorStoreCollectionQueryBuilder.BuildSelectQuery(
            this._model,
            this._model.KeyProperty.StorageName,
            this._partitionKeyProperty.StorageName,
            GetCompositeKeys(keys).ToList(),
            includeVectors);

        await foreach (var jsonObject in this.GetItemsAsync<JsonObject>(queryDefinition, cancellationToken).ConfigureAwait(false))
        {
            var record = VectorStoreErrorHandler.RunModelConversion(
                AzureCosmosDBNoSQLConstants.VectorStoreSystemName,
                this._collectionMetadata.VectorStoreName,
                this.Name,
                OperationName,
                () => this._mapper.MapFromStorageToDataModel(jsonObject, new() { IncludeVectors = includeVectors }));

            if (record is not null)
            {
                yield return record;
            }
        }
    }

    /// <inheritdoc />
    public async Task<TKey> UpsertAsync(TRecord record, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(record);

        const string OperationName = "UpsertItem";

        MEAI.Embedding?[]? generatedEmbeddings = null;

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
                generatedEmbeddings ??= new MEAI.Embedding?[vectorPropertyCount];
                generatedEmbeddings[i] = await floatTask.ConfigureAwait(false);
            }
            else if (vectorProperty.TryGenerateEmbedding<TRecord, Embedding<byte>, ReadOnlyMemory<byte>>(record, cancellationToken, out var byteTask))
            {
                generatedEmbeddings ??= new MEAI.Embedding?[vectorPropertyCount];
                generatedEmbeddings[i] = await byteTask.ConfigureAwait(false);
            }
            else if (vectorProperty.TryGenerateEmbedding<TRecord, Embedding<sbyte>, ReadOnlyMemory<sbyte>>(record, cancellationToken, out var sbyteTask))
            {
                generatedEmbeddings ??= new MEAI.Embedding?[vectorPropertyCount];
                generatedEmbeddings[i] = await sbyteTask.ConfigureAwait(false);
            }
            else
            {
                throw new InvalidOperationException(
                    $"The embedding generator configured on property '{vectorProperty.ModelName}' cannot produce an embedding of types '{typeof(Embedding<float>).Name}', '{typeof(Embedding<byte>).Name}' or '{typeof(Embedding<sbyte>).Name}' for the given input type.");
            }
        }

        var jsonObject = VectorStoreErrorHandler.RunModelConversion(
                AzureCosmosDBNoSQLConstants.VectorStoreSystemName,
                this._collectionMetadata.VectorStoreName,
                this.Name,
                OperationName,
                () => this._mapper.MapFromDataToStorageModel(record, generatedEmbeddings));

        var keyValue = jsonObject.TryGetPropertyValue(this._model.KeyProperty.StorageName!, out var jsonKey) ? jsonKey?.ToString() : null;
        var partitionKeyValue = jsonObject.TryGetPropertyValue(this._partitionKeyProperty.StorageName, out var jsonPartitionKey) ? jsonPartitionKey?.ToString() : null;

        if (string.IsNullOrWhiteSpace(keyValue))
        {
            throw new VectorStoreOperationException($"Key property {this._model.KeyProperty.ModelName} is not initialized.");
        }

        if (string.IsNullOrWhiteSpace(partitionKeyValue))
        {
            throw new VectorStoreOperationException($"Partition key property {this._partitionKeyProperty.ModelName} is not initialized.");
        }

        await this.RunOperationAsync(OperationName, () =>
            this._database
                .GetContainer(this.Name)
                .UpsertItemAsync(jsonObject, new PartitionKey(partitionKeyValue), cancellationToken: cancellationToken))
            .ConfigureAwait(false);

        return typeof(TKey) switch
        {
            var t when t == typeof(AzureCosmosDBNoSQLCompositeKey) || t == typeof(object) => (TKey)(object)new AzureCosmosDBNoSQLCompositeKey(keyValue!, partitionKeyValue!),
            var t when t == typeof(string) => (TKey)(object)keyValue!,
            _ => throw new UnreachableException()
        };
    }

    /// <inheritdoc />
    public async Task<IReadOnlyList<TKey>> UpsertAsync(IEnumerable<TRecord> records, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(records);

        // TODO: Do proper bulk upsert rather than parallel single inserts, #11350
        var tasks = records.Select(record => this.UpsertAsync(record, cancellationToken));
        var keys = await Task.WhenAll(tasks).ConfigureAwait(false);
        return keys.Where(k => k is not null).ToList();
    }

    #region Search

    /// <inheritdoc />
    public async IAsyncEnumerable<VectorSearchResult<TRecord>> SearchAsync<TInput>(
        TInput value,
        int top,
        VectorSearchOptions<TRecord>? options = default,
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

            case IEmbeddingGenerator<TInput, Embedding<byte>> generator:
            {
                var embedding = await generator.GenerateAsync(value, new() { Dimensions = vectorProperty.Dimensions }, cancellationToken).ConfigureAwait(false);

                await foreach (var record in this.SearchCoreAsync(embedding.Vector, top, vectorProperty, operationName: "Search", options, cancellationToken).ConfigureAwait(false))
                {
                    yield return record;
                }

                yield break;
            }

            case IEmbeddingGenerator<TInput, Embedding<sbyte>> generator:
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
                    AzureCosmosDBNoSQLVectorStoreModelBuilder.s_supportedVectorTypes.Contains(typeof(TInput))
                        ? string.Format(VectorDataStrings.EmbeddingTypePassedToSearchAsync)
                        : string.Format(VectorDataStrings.IncompatibleEmbeddingGeneratorWasConfiguredForInputType, typeof(TInput).Name, vectorProperty.EmbeddingGenerator.GetType().Name));
        }
    }

    /// <inheritdoc />
<<<<<<< HEAD
    public Task DeleteAsync(AzureCosmosDBNoSQLCompositeKey key, DeleteRecordOptions? options = null, CancellationToken cancellationToken = default)
    {
        return this.InternalDeleteAsync([key], cancellationToken);
    }

    /// <inheritdoc />
    public Task DeleteBatchAsync(IEnumerable<AzureCosmosDBNoSQLCompositeKey> keys, DeleteRecordOptions? options = null, CancellationToken cancellationToken = default)
    {
        return this.InternalDeleteAsync(keys, cancellationToken);
    }

    /// <inheritdoc />
    Task<AzureCosmosDBNoSQLCompositeKey> IVectorStoreRecordCollection<AzureCosmosDBNoSQLCompositeKey, TRecord>.UpsertAsync(TRecord record, UpsertRecordOptions? options, CancellationToken cancellationToken)
    {
        return this.InternalUpsertAsync(record, cancellationToken);
    }

    /// <inheritdoc />
    async IAsyncEnumerable<AzureCosmosDBNoSQLCompositeKey> IVectorStoreRecordCollection<AzureCosmosDBNoSQLCompositeKey, TRecord>.UpsertBatchAsync(
        IEnumerable<TRecord> records,
        UpsertRecordOptions? options,
        [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        Verify.NotNull(records);

        var tasks = records.Select(record => this.InternalUpsertAsync(record, cancellationToken));

        var keys = await Task.WhenAll(tasks).ConfigureAwait(false);

        foreach (var key in keys)
        {
            if (key is not null)
            {
                yield return key;
            }
        }
    }

    /// <inheritdoc />
    public async IAsyncEnumerable<VectorSearchResult<TRecord>> VectorizedSearchAsync<TVector>(
        TVector vector,
        VectorSearchOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)

    /// <inheritdoc />
    public Task<VectorSearchResults<TRecord>> VectorizedSearchAsync<TVector>(
=======
    public IAsyncEnumerable<VectorSearchResult<TRecord>> SearchEmbeddingAsync<TVector>(
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        TVector vector,
        int top,
        VectorSearchOptions<TRecord>? options = null,
        CancellationToken cancellationToken = default)
        where TVector : notnull
    {
        options ??= s_defaultVectorSearchOptions;
        var vectorProperty = this._model.GetVectorPropertyOrSingle(options);

        return this.SearchCoreAsync(vector, top, vectorProperty, operationName: "SearchEmbedding", options, cancellationToken);
    }

    private IAsyncEnumerable<VectorSearchResult<TRecord>> SearchCoreAsync<TVector>(
        TVector vector,
        int top,
        VectorStoreRecordVectorPropertyModel vectorProperty,
        string operationName,
        VectorSearchOptions<TRecord> options,
        CancellationToken cancellationToken = default)
        where TVector : notnull
    {
        const string OperationName = "VectorizedSearch";
        const string ScorePropertyName = "SimilarityScore";

        this.VerifyVectorType(vector);
        Verify.NotLessThan(top, 1);

        if (options.IncludeVectors && this._model.VectorProperties.Any(p => p.EmbeddingGenerator is not null))
        {
            throw new NotSupportedException(VectorDataStrings.IncludeVectorsNotSupportedWithEmbeddingGeneration);
        }

#pragma warning disable CS0618 // Type or member is obsolete
        var queryDefinition = AzureCosmosDBNoSQLVectorStoreCollectionQueryBuilder.BuildSearchQuery(
            vector,
            null,
            this._model,
            vectorProperty.StorageName,
            null,
            ScorePropertyName,
            options.OldFilter,
            options.Filter,
            top,
            options.Skip,
            options.IncludeVectors);
#pragma warning restore CS0618 // Type or member is obsolete

        var searchResults = this.GetItemsAsync<JsonObject>(queryDefinition, cancellationToken);
        return this.MapSearchResultsAsync(
            searchResults,
            ScorePropertyName,
            OperationName,
            options.IncludeVectors,
            cancellationToken);
    }

    /// <inheritdoc />
    [Obsolete("Use either SearchEmbeddingAsync to search directly on embeddings, or SearchAsync to handle embedding generation internally as part of the call.")]
    public IAsyncEnumerable<VectorSearchResult<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, int top, VectorSearchOptions<TRecord>? options = null, CancellationToken cancellationToken = default)
        where TVector : notnull
        => this.SearchEmbeddingAsync(vector, top, options, cancellationToken);

    #endregion Search

    /// <inheritdoc />
    public async IAsyncEnumerable<TRecord> GetAsync(Expression<Func<TRecord, bool>> filter, int top,
        GetFilteredRecordOptions<TRecord>? options = null, [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        Verify.NotNull(filter);
        Verify.NotLessThan(top, 1);

        options ??= new();

        var (whereClause, filterParameters) = new AzureCosmosDBNoSqlFilterTranslator().Translate(filter, this._model);

        var queryDefinition = AzureCosmosDBNoSQLVectorStoreCollectionQueryBuilder.BuildSearchQuery(
            this._model,
            whereClause,
            filterParameters,
            options,
            top);

        var searchResults = this.GetItemsAsync<JsonObject>(queryDefinition, cancellationToken);

        await foreach (var jsonObject in searchResults.ConfigureAwait(false))
        {
            var record = VectorStoreErrorHandler.RunModelConversion(
                AzureCosmosDBNoSQLConstants.VectorStoreSystemName,
                this._collectionMetadata.VectorStoreName,
                this.Name,
                "GetAsync",
                () => this._mapper.MapFromStorageToDataModel(jsonObject, new() { IncludeVectors = options.IncludeVectors }));

            yield return record;
        }
    }

    /// <inheritdoc />
    public IAsyncEnumerable<VectorSearchResult<TRecord>> HybridSearchAsync<TVector>(TVector vector, ICollection<string> keywords, int top, HybridSearchOptions<TRecord>? options = null, CancellationToken cancellationToken = default)
    {
        const string OperationName = "VectorizedSearch";
        const string ScorePropertyName = "SimilarityScore";

        this.VerifyVectorType(vector);
        Verify.NotLessThan(top, 1);

        options ??= s_defaultKeywordVectorizedHybridSearchOptions;
        var vectorProperty = this._model.GetVectorPropertyOrSingle<TRecord>(new() { VectorProperty = options.VectorProperty });
        var textProperty = this._model.GetFullTextDataPropertyOrSingle(options.AdditionalProperty);

#pragma warning disable CS0618 // Type or member is obsolete
        var queryDefinition = AzureCosmosDBNoSQLVectorStoreCollectionQueryBuilder.BuildSearchQuery<TVector, TRecord>(
            vector,
            keywords,
            this._model,
            vectorProperty.StorageName,
            textProperty.StorageName,
            ScorePropertyName,
            options.OldFilter,
            options.Filter,
            top,
            options.Skip,
            options.IncludeVectors);
#pragma warning restore CS0618 // Type or member is obsolete

        var searchResults = this.GetItemsAsync<JsonObject>(queryDefinition, cancellationToken);
        return this.MapSearchResultsAsync(
            searchResults,
            ScorePropertyName,
            OperationName,
            options.IncludeVectors,
            cancellationToken);
    }

    /// <inheritdoc />
    public object? GetService(Type serviceType, object? serviceKey = null)
    {
        Verify.NotNull(serviceType);

        return
            serviceKey is not null ? null :
            serviceType == typeof(VectorStoreRecordCollectionMetadata) ? this._collectionMetadata :
            serviceType == typeof(Database) ? this._database :
            serviceType.IsInstanceOfType(this) ? this :
            null;
    }

    #region private

    private void VerifyVectorType<TVector>(TVector? vector)
    {
        Verify.NotNull(vector);

        var vectorType = vector.GetType();

        if (!AzureCosmosDBNoSQLVectorStoreModelBuilder.s_supportedVectorTypes.Contains(vectorType))
        {
            throw new NotSupportedException(
                $"The provided vector type {vectorType.FullName} is not supported by the Azure CosmosDB NoSQL connector. " +
                $"Supported types are: {string.Join(", ", AzureCosmosDBNoSQLVectorStoreModelBuilder.s_supportedVectorTypes.Select(l => l.FullName))}");
        }
<<<<<<< HEAD

        var searchOptions = options ?? s_defaultVectorSearchOptions;
        var vectorProperty = this.GetVectorPropertyForSearch(searchOptions.VectorPropertyName);

        if (vectorProperty is null)
        {
            throw new InvalidOperationException("The collection does not have any vector properties, so vector search is not possible.");
        }

        var fields = new List<string>(searchOptions.IncludeVectors ? this._storagePropertyNames.Values : this._nonVectorStoragePropertyNames);
        var vectorPropertyName = this._storagePropertyNames[vectorProperty.DataModelPropertyName];

        var queryDefinition = AzureCosmosDBNoSQLVectorStoreCollectionQueryBuilder.BuildSearchQuery(
            vector,
            fields,
            this._storagePropertyNames,
            vectorPropertyName,
            ScorePropertyName,
            searchOptions);

        await foreach (var jsonObject in this.GetItemsAsync<JsonObject>(queryDefinition, cancellationToken).ConfigureAwait(false))
        {
            var score = jsonObject[ScorePropertyName]?.AsValue().GetValue<double>();

            // Remove score from result object for mapping.
            jsonObject.Remove(ScorePropertyName);

            var record = VectorStoreErrorHandler.RunModelConversion(
                DatabaseName,
                this.CollectionName,
                OperationName,
                () => this._mapper.MapFromStorageToDataModel(jsonObject, new() { IncludeVectors = searchOptions.IncludeVectors }));

            yield return new VectorSearchResult<TRecord>(record, score);
        }
    }

        var searchResults = this.GetItemsAsync<JsonObject>(queryDefinition, cancellationToken);
        var mappedResults = this.MapSearchResultsAsync(
            searchResults,
            ScorePropertyName,
            OperationName,
            searchOptions,
            cancellationToken);
        return Task.FromResult(new VectorSearchResults<TRecord>(mappedResults));
=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    private async Task<T> RunOperationAsync<T>(string operationName, Func<Task<T>> operation)
    {
        try
        {
            return await operation.Invoke().ConfigureAwait(false);
        }
        catch (CosmosException ex)
        {
            throw new VectorStoreOperationException("Call to vector store failed.", ex)
            {
                VectorStoreSystemName = AzureCosmosDBNoSQLConstants.VectorStoreSystemName,
                VectorStoreName = this._collectionMetadata.VectorStoreName,
                CollectionName = this.Name,
                OperationName = operationName
            };
        }
    }

<<<<<<< HEAD
    private static void VerifyPartitionKeyProperty(string partitionKeyPropertyName, VectorStoreRecordDefinition definition)
    {
        var partitionKeyProperty = definition.Properties

    private static void VerifyPartitionKeyProperty(string partitionKeyPropertyName, VectorStoreRecordDefinition definition)
    {
        var partitionKeyProperty = definition.Properties

    private static void VerifyPartitionKeyProperty(string partitionKeyPropertyName, IReadOnlyList<VectorStoreRecordProperty> properties)
    {
        var partitionKeyProperty = properties

    private static void VerifyPartitionKeyProperty(string partitionKeyPropertyName, IReadOnlyList<VectorStoreRecordProperty> properties)
    {
        var partitionKeyProperty = properties

            .FirstOrDefault(l => l.DataModelPropertyName.Equals(partitionKeyPropertyName, StringComparison.Ordinal));

        if (partitionKeyProperty is null)
        {
            throw new ArgumentException("Partition key property must be part of record definition.");
        }

        if (partitionKeyProperty.PropertyType != typeof(string))
        {
            throw new ArgumentException("Partition key property must be string.");
        }
    }

=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// <summary>
    /// Returns instance of <see cref="ContainerProperties"/> with applied indexing policy.
    /// More information here: <see href="https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/how-to-manage-indexing-policy"/>.
    /// </summary>
    private ContainerProperties GetContainerProperties()
    {
        // Process Vector properties.
        var embeddings = new Collection<Azure.Cosmos.Embedding>();
        var vectorIndexPaths = new Collection<VectorIndexPath>();

        foreach (var property in this._vectorStoreRecordDefinition.Properties.OfType<VectorStoreRecordVectorProperty>())

        foreach (var property in this._propertyReader.VectorProperties)

        var indexingPolicy = new IndexingPolicy
        {
            IndexingMode = this._options.IndexingMode,
            Automatic = this._options.Automatic
        };

        if (this._options.IndexingMode == IndexingMode.None)
        {
            return new ContainerProperties(this.Name, partitionKeyPath: $"/{this._partitionKeyProperty.StorageName}")
            {
                IndexingPolicy = indexingPolicy
            };
        }

        foreach (var property in this._model.VectorProperties)
        {
            var path = $"/{property.StorageName}";

            var embedding = new Azure.Cosmos.Embedding
            {
                DataType = GetDataType(property.EmbeddingType, property.StorageName),
                Dimensions = (int)property.Dimensions,
                DistanceFunction = GetDistanceFunction(property.DistanceFunction, property.StorageName),
                Path = path
            };

            var vectorIndexPath = new VectorIndexPath
            {
                Type = GetIndexKind(property.IndexKind, property.StorageName),
                Path = path
            };

            embeddings.Add(embedding);
            vectorIndexPaths.Add(vectorIndexPath);
        }

        indexingPolicy.VectorIndexes = vectorIndexPaths;

        var fullTextPolicy = new FullTextPolicy() { FullTextPaths = new Collection<FullTextPath>() };
        var vectorEmbeddingPolicy = new VectorEmbeddingPolicy(embeddings);

        // Process Data properties.
        foreach (var property in this._model.DataProperties)
        {
<<<<<<< HEAD
            // Process Data properties.
            foreach (var property in this._vectorStoreRecordDefinition.Properties.OfType<VectorStoreRecordDataProperty>())
            foreach (var property in this._vectorStoreRecordDefinition.Properties.OfType<VectorStoreRecordDataProperty>())
            foreach (var property in this._propertyReader.DataProperties)
            foreach (var property in this._propertyReader.DataProperties)
            if (property.IsFilterable || property.IsFullTextSearchable)
=======
            if (property.IsIndexed || property.IsFullTextIndexed)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            {
                indexingPolicy.IncludedPaths.Add(new IncludedPath { Path = $"/{property.StorageName}/?" });
            }
            if (property.IsFullTextIndexed)
            {
                indexingPolicy.FullTextIndexes.Add(new FullTextIndexPath { Path = $"/{property.StorageName}" });
                // TODO: Switch to using language from a setting.
                fullTextPolicy.FullTextPaths.Add(new FullTextPath { Path = $"/{property.StorageName}", Language = "en-US" });
            }
        }

        // Adding special mandatory indexing path.
        indexingPolicy.IncludedPaths.Add(new IncludedPath { Path = "/" });

        // Exclude vector paths to ensure optimized performance.
        foreach (var vectorIndexPath in vectorIndexPaths)
        {
            indexingPolicy.ExcludedPaths.Add(new ExcludedPath { Path = $"{vectorIndexPath.Path}/*" });
        }

        return new ContainerProperties(this.Name, partitionKeyPath: $"/{this._partitionKeyProperty.StorageName}")
        {
            VectorEmbeddingPolicy = vectorEmbeddingPolicy,
            IndexingPolicy = indexingPolicy,
            FullTextPolicy = fullTextPolicy
        };
    }

    /// <summary>
    /// More information about Azure CosmosDB NoSQL index kinds here: <see href="https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/vector-search#vector-indexing-policies" />.
    /// </summary>
    private static VectorIndexType GetIndexKind(string? indexKind, string vectorPropertyName)
        => indexKind switch
        {
            IndexKind.DiskAnn or null => VectorIndexType.DiskANN,
            IndexKind.Flat => VectorIndexType.Flat,
            IndexKind.QuantizedFlat => VectorIndexType.QuantizedFlat,
            _ => throw new InvalidOperationException($"Index kind '{indexKind}' on {nameof(VectorStoreRecordVectorProperty)} '{vectorPropertyName}' is not supported by the Azure CosmosDB NoSQL VectorStore.")
        };

    /// <summary>
    /// More information about Azure CosmosDB NoSQL distance functions here: <see href="https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/vector-search#container-vector-policies" />.
    /// </summary>
    private static DistanceFunction GetDistanceFunction(string? distanceFunction, string vectorPropertyName)
    {
        if (string.IsNullOrWhiteSpace(distanceFunction))
        {
            // Use default distance function.
            return DistanceFunction.Cosine;
        }

        return distanceFunction switch
        {
            SKDistanceFunction.CosineSimilarity => DistanceFunction.Cosine,
            SKDistanceFunction.DotProductSimilarity => DistanceFunction.DotProduct,
            SKDistanceFunction.EuclideanDistance => DistanceFunction.Euclidean,
            _ => throw new InvalidOperationException($"Distance function '{distanceFunction}' for {nameof(VectorStoreRecordVectorProperty)} '{vectorPropertyName}' is not supported by the Azure CosmosDB NoSQL VectorStore.")
        };
    }

    /// <summary>
    /// Returns <see cref="VectorDataType"/> based on vector property type.
    /// </summary>
    private static VectorDataType GetDataType(Type vectorDataType, string vectorPropertyName)
        => vectorDataType switch
        {
            Type type when type == typeof(ReadOnlyMemory<float>) || type == typeof(ReadOnlyMemory<float>?) => VectorDataType.Float32,
            Type type when type == typeof(ReadOnlyMemory<byte>) || type == typeof(ReadOnlyMemory<byte>?) => VectorDataType.Uint8,
            Type type when type == typeof(ReadOnlyMemory<sbyte>) || type == typeof(ReadOnlyMemory<sbyte>?) => VectorDataType.Int8,
            _ => throw new InvalidOperationException($"Data type '{vectorDataType}' for {nameof(VectorStoreRecordVectorProperty)} '{vectorPropertyName}' is not supported by the Azure CosmosDB NoSQL VectorStore.")
        };
<<<<<<< HEAD
    }

    private async IAsyncEnumerable<TRecord> InternalGetAsync(
        IEnumerable<AzureCosmosDBNoSQLCompositeKey> keys,
        GetRecordOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        Verify.NotNull(keys);

        const string OperationName = "GetItemQueryIterator";

        var includeVectors = options?.IncludeVectors ?? false;
        var fields = new List<string>(includeVectors ? this._storagePropertyNames.Values : this._nonVectorStoragePropertyNames);
        var queryDefinition = AzureCosmosDBNoSQLVectorStoreCollectionQueryBuilder.BuildSelectQuery(
            this._keyStoragePropertyName,
            this._partitionKeyStoragePropertyName,
            keys.ToList(),
            fields);

        await foreach (var jsonObject in this.GetItemsAsync<JsonObject>(queryDefinition, cancellationToken).ConfigureAwait(false))
        var queryDefinition = this.GetSelectQuery(keys.ToList(), fields);

        await foreach (var jsonObject in this.GetItemsAsync<JsonObject>(queryDefinition, cancellationToken).ConfigureAwait(false))
        {
            yield return VectorStoreErrorHandler.RunModelConversion(
                DatabaseName,
                this.CollectionName,
                OperationName,
                () => this._mapper.MapFromStorageToDataModel(jsonObject, new() { IncludeVectors = includeVectors }));
        }
    }

    private async Task<AzureCosmosDBNoSQLCompositeKey> InternalUpsertAsync(
        TRecord record,
        CancellationToken cancellationToken)
    {
        Verify.NotNull(record);

        const string OperationName = "UpsertItem";

        var jsonObject = VectorStoreErrorHandler.RunModelConversion(
                DatabaseName,
                this.CollectionName,
                OperationName,
                () => this._mapper.MapFromDataToStorageModel(record));

        var keyValue = jsonObject.TryGetPropertyValue(this._keyStoragePropertyName, out var jsonKey) ? jsonKey?.ToString() : null;
        var partitionKeyValue = jsonObject.TryGetPropertyValue(this._partitionKeyStoragePropertyName, out var jsonPartitionKey) ? jsonPartitionKey?.ToString() : null;

        if (string.IsNullOrWhiteSpace(keyValue))
        {
            throw new VectorStoreOperationException($"Key property {this._keyProperty.DataModelPropertyName} is not initialized.");
            throw new VectorStoreOperationException($"Key property {this._propertyReader.KeyPropertyName} is not initialized.");

        }

        if (string.IsNullOrWhiteSpace(partitionKeyValue))
        {
            throw new VectorStoreOperationException($"Partition key property {this._partitionKeyPropertyName} is not initialized.");
        }

        await this.RunOperationAsync(OperationName, () =>
            this._database
                .GetContainer(this.CollectionName)
                .UpsertItemAsync(jsonObject, new PartitionKey(partitionKeyValue), cancellationToken: cancellationToken))
            .ConfigureAwait(false);

        return new AzureCosmosDBNoSQLCompositeKey(keyValue!, partitionKeyValue!);
    }

    private async Task InternalDeleteAsync(IEnumerable<AzureCosmosDBNoSQLCompositeKey> keys, CancellationToken cancellationToken)
    {
        Verify.NotNull(keys);

        var tasks = keys.Select(key =>
        {
            Verify.NotNullOrWhiteSpace(key.RecordKey);
            Verify.NotNullOrWhiteSpace(key.PartitionKey);

            return this.RunOperationAsync("DeleteItem", () =>
                this._database
                    .GetContainer(this.CollectionName)
                    .DeleteItemAsync<JsonObject>(key.RecordKey, new PartitionKey(key.PartitionKey), cancellationToken: cancellationToken));
        });

        await Task.WhenAll(tasks).ConfigureAwait(false);
    }
=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

    private async IAsyncEnumerable<T> GetItemsAsync<T>(QueryDefinition queryDefinition, [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        var iterator = this._database
            .GetContainer(this.Name)
            .GetItemQueryIterator<T>(queryDefinition);
    private QueryDefinition GetSelectQuery(List<AzureCosmosDBNoSQLCompositeKey> keys, List<string> fields)
    {
        Verify.True(keys.Count > 0, "At least one key should be provided.", nameof(keys));

        const string WhereClauseDelimiter = " OR ";
        const string SelectClauseDelimiter = ",";

        const string RecordKeyVariableName = "rk";
        const string PartitionKeyVariableName = "pk";

        const string TableVariableName = "x";

        var selectClauseArguments = string.Join(SelectClauseDelimiter,
            fields.Select(field => $"{TableVariableName}.{field}"));

        var whereClauseArguments = string.Join(WhereClauseDelimiter,
            keys.Select((key, index) =>
                $"({TableVariableName}.{this._keyStoragePropertyName} = @{RecordKeyVariableName}{index} AND " +
                $"{TableVariableName}.{this._partitionKeyStoragePropertyName} = @{PartitionKeyVariableName}{index})"));

        var query = $"SELECT {selectClauseArguments} FROM {TableVariableName} WHERE {whereClauseArguments}";

        var queryDefinition = new QueryDefinition(query);

        for (var i = 0; i < keys.Count; i++)
        {
            var recordKey = keys[i].RecordKey;
            var partitionKey = keys[i].PartitionKey;

            Verify.NotNullOrWhiteSpace(recordKey);
            Verify.NotNullOrWhiteSpace(partitionKey);

            queryDefinition.WithParameter($"@{RecordKeyVariableName}{i}", recordKey);
            queryDefinition.WithParameter($"@{PartitionKeyVariableName}{i}", partitionKey);
        }

        return queryDefinition;
    }

    private async IAsyncEnumerable<JsonObject> GetItemsAsync(QueryDefinition queryDefinition, [EnumeratorCancellation] CancellationToken cancellationToken)
    private async IAsyncEnumerable<T> GetItemsAsync<T>(QueryDefinition queryDefinition, [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        var iterator = this._database
            .GetContainer(this.CollectionName)
            .GetItemQueryIterator<T>(queryDefinition);

        while (iterator.HasMoreResults)
        {
            var response = await iterator.ReadNextAsync(cancellationToken).ConfigureAwait(false);

            foreach (var record in response.Resource)
            {
                if (record is not null)
                {
                    yield return record;
                }
            }
        }
    }

    private async IAsyncEnumerable<VectorSearchResult<TRecord>> MapSearchResultsAsync(
        IAsyncEnumerable<JsonObject> jsonObjects,
        string scorePropertyName,
        string operationName,
        bool includeVectors,
        [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        await foreach (var jsonObject in jsonObjects.ConfigureAwait(false))
        {
            var score = jsonObject[scorePropertyName]?.AsValue().GetValue<double>();

            // Remove score from result object for mapping.
            jsonObject.Remove(scorePropertyName);

            var record = VectorStoreErrorHandler.RunModelConversion(
                AzureCosmosDBNoSQLConstants.VectorStoreSystemName,
                this._collectionMetadata.VectorStoreName,
                this.Name,
                operationName,
                () => this._mapper.MapFromStorageToDataModel(jsonObject, new() { IncludeVectors = includeVectors }));

            yield return new VectorSearchResult<TRecord>(record, score);
        }
    }

    private static IEnumerable<AzureCosmosDBNoSQLCompositeKey> GetCompositeKeys(IEnumerable<TKey> keys)
        => keys switch
        {
            IEnumerable<AzureCosmosDBNoSQLCompositeKey> k => k,
            IEnumerable<string> k => k.Select(key => new AzureCosmosDBNoSQLCompositeKey(recordKey: key, partitionKey: key)),
            IEnumerable<object> k => k.Select(key => key switch
            {
<<<<<<< HEAD
                return vectorProperty;
            }

            throw new InvalidOperationException($"The {typeof(TRecord).FullName} type does not have a vector property named '{vectorFieldName}'.");
        }

        // If vector property is not provided in options, return first vector property from schema.
        return this._firstVectorProperty;
        return this._propertyReader.VectorProperty;
    }

    /// <summary>
    /// Returns custom mapper, generic data model mapper or default record mapper.
    /// </summary>
    private IVectorStoreRecordMapper<TRecord, JsonObject> InitializeMapper(JsonSerializerOptions jsonSerializerOptions)
    {
        if (this._options.JsonObjectCustomMapper is not null)
        {
            return this._options.JsonObjectCustomMapper;
        }

        if (typeof(TRecord) == typeof(VectorStoreGenericDataModel<string>))
        {
            var mapper = new AzureCosmosDBNoSQLGenericDataModelMapper(this._propertyReader.Properties, this._storagePropertyNames, jsonSerializerOptions);
            return (mapper as IVectorStoreRecordMapper<TRecord, JsonObject>)!;
        }

        return new AzureCosmosDBNoSQLVectorStoreRecordMapper<TRecord>(
            this._storagePropertyNames[this._propertyReader.KeyPropertyName],
            this._storagePropertyNames,
            jsonSerializerOptions);
    }
=======
                string s => new AzureCosmosDBNoSQLCompositeKey(recordKey: s, partitionKey: s),
                AzureCosmosDBNoSQLCompositeKey ck => ck,
                _ => throw new ArgumentException($"Invalid key type '{key.GetType().Name}'.")
            }),
            _ => throw new UnreachableException()
        };
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

    #endregion
}
