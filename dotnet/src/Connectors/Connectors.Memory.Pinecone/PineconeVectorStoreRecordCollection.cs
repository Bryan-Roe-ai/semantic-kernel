// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Linq.Expressions;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.VectorData;
using Microsoft.Extensions.VectorData.ConnectorSupport;
using Microsoft.Extensions.VectorData.Properties;
using Pinecone;
using Sdk = Pinecone;

namespace Microsoft.SemanticKernel.Connectors.Pinecone;

/// <summary>
/// Service for storing and retrieving vector records, that uses Pinecone as the underlying storage.
/// </summary>
/// <typeparam name="TKey">The data type of the record key. Can be either <see cref="string"/>, or <see cref="object"/> for dynamic mapping.</typeparam>
/// <typeparam name="TRecord">The data model to use for adding, updating and retrieving data from storage.</typeparam>
#pragma warning disable CA1711 // Identifiers should not have incorrect suffix
public sealed class PineconeVectorStoreRecordCollection<TKey, TRecord> : IVectorStoreRecordCollection<TKey, TRecord>
    where TKey : notnull
    where TRecord : notnull
#pragma warning restore CA1711 // Identifiers should not have incorrect suffix
{
    private static readonly VectorSearchOptions<TRecord> s_defaultVectorSearchOptions = new();

<<<<<<< HEAD
    private const string UpsertOperationName = "Upsert";
    private const string DeleteOperationName = "Delete";
    private const string GetOperationName = "Get";

    private const string QueryOperationName = "Query";

    private static readonly VectorSearchOptions s_defaultVectorSearchOptions = new();

    private const string QueryOperationName = "Query";

    private static readonly VectorSearchOptions s_defaultVectorSearchOptions = new();

    private readonly Sdk.PineconeClient _pineconeClient;
    private readonly PineconeVectorStoreRecordCollectionOptions<TRecord> _options;
    private readonly VectorStoreRecordDefinition _vectorStoreRecordDefinition;
    private readonly VectorStoreRecordDefinition _vectorStoreRecordDefinition;
    private readonly VectorStoreRecordPropertyReader _propertyReader;
    private readonly VectorStoreRecordPropertyReader _propertyReader;
    private readonly VectorStoreRecordPropertyReader _propertyReader;
    private readonly IVectorStoreRecordMapper<TRecord, Sdk.Vector> _mapper;

    private Sdk.Index<GrpcTransport>? _index;
=======
    /// <summary>Metadata about vector store record collection.</summary>
    private readonly VectorStoreRecordCollectionMetadata _collectionMetadata;

    private readonly Sdk.PineconeClient _pineconeClient;
    private readonly PineconeVectorStoreRecordCollectionOptions<TRecord> _options;
    private readonly VectorStoreRecordModel _model;
    private readonly PineconeVectorStoreRecordMapper<TRecord> _mapper;
    private IndexClient? _indexClient;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

    /// <inheritdoc />
    public string Name { get; }

    /// <summary>
    /// Initializes a new instance of the <see cref="PineconeVectorStoreRecordCollection{TKey, TRecord}"/> class.
    /// </summary>
    /// <param name="pineconeClient">Pinecone client that can be used to manage the collections and vectors in a Pinecone store.</param>
    /// <param name="options">Optional configuration options for this class.</param>
    /// <exception cref="ArgumentNullException">Thrown if the <paramref name="pineconeClient"/> is null.</exception>
    /// <param name="name">The name of the collection that this <see cref="PineconeVectorStoreRecordCollection{TKey, TRecord}"/> will access.</param>
    /// <exception cref="ArgumentException">Thrown for any misconfigured options.</exception>
    public PineconeVectorStoreRecordCollection(Sdk.PineconeClient pineconeClient, string name, PineconeVectorStoreRecordCollectionOptions<TRecord>? options = null)
    {
        Verify.NotNull(pineconeClient);
<<<<<<< HEAD
=======
        VerifyCollectionName(name);

        if (typeof(TKey) != typeof(string) && typeof(TKey) != typeof(object))
        {
            throw new NotSupportedException("Only string keys are supported (and object for dynamic mapping)");
        }
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        this._pineconeClient = pineconeClient;
        this.Name = name;
        this._options = options ?? new PineconeVectorStoreRecordCollectionOptions<TRecord>();
<<<<<<< HEAD
        this._vectorStoreRecordDefinition = this._options.VectorStoreRecordDefinition ?? VectorStoreRecordPropertyReader.CreateVectorStoreRecordDefinitionFromType(typeof(TRecord), true);

        if (this._options.VectorCustomMapper is null)
        {
            this._mapper = new PineconeVectorStoreRecordMapper<TRecord>(this._vectorStoreRecordDefinition);

        this._propertyReader = new VectorStoreRecordPropertyReader(
            typeof(TRecord),
            this._options.VectorStoreRecordDefinition,
            new()
            {
                RequiresAtLeastOneVector = true,
                SupportsMultipleKeys = false,
                SupportsMultipleVectors = false,
            });

        if (this._options.VectorCustomMapper is null)
        {
<<<<<<< main
<<<<<<< main
            this._mapper = new PineconeVectorStoreRecordMapper<TRecord>(this._propertyReader);
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
            // Custom Mapper.
            this._mapper = this._options.VectorCustomMapper;
        }
        else if (typeof(TRecord) == typeof(VectorStoreGenericDataModel<string>))
        {
            // Generic data model mapper.
            this._mapper = (new PineconeGenericDataModelMapper(this._propertyReader) as IVectorStoreRecordMapper<TRecord, Sdk.Vector>)!;
>>>>>>> upstream/main
=======
            this._mapper = new PineconeVectorStoreRecordMapper<TRecord>(this._propertyReader);
>>>>>>> origin/main
        }
        else
        {
            this._mapper = this._options.VectorCustomMapper;
        }
=======
        this._model = new VectorStoreRecordModelBuilder(PineconeVectorStoreRecordFieldMapping.ModelBuildingOptions)
            .Build(typeof(TRecord), this._options.VectorStoreRecordDefinition, this._options.EmbeddingGenerator);
        this._mapper = new PineconeVectorStoreRecordMapper<TRecord>(this._model);

        this._collectionMetadata = new()
        {
            VectorStoreSystemName = PineconeConstants.VectorStoreSystemName,
            CollectionName = name
        };
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <inheritdoc />
    public Task<bool> CollectionExistsAsync(CancellationToken cancellationToken = default)
        => this.RunCollectionOperationAsync(
            "CollectionExists",
            async () =>
            {
                var collections = await this._pineconeClient.ListIndexesAsync(cancellationToken: cancellationToken).ConfigureAwait(false);

                return collections.Indexes?.Any(x => x.Name == this.Name) is true;
            });

    /// <inheritdoc />
    public Task CreateCollectionAsync(CancellationToken cancellationToken = default)
    {
        // we already run through record property validation, so a single VectorStoreRecordVectorProperty is guaranteed.
<<<<<<< HEAD

        var vectorProperty = this._vectorStoreRecordDefinition.Properties.OfType<VectorStoreRecordVectorProperty>().First();
        var vectorProperty = this._vectorStoreRecordDefinition.Properties.OfType<VectorStoreRecordVectorProperty>().First();
        var vectorProperty = this._propertyReader.VectorProperty!;
        var vectorProperty = this._propertyReader.VectorProperty!;
        var (dimension, metric) = PineconeVectorStoreCollectionCreateMapping.MapServerlessIndex(vectorProperty);
=======
        var vectorProperty = this._model.VectorProperty!;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        if (!string.IsNullOrEmpty(vectorProperty.IndexKind) && vectorProperty.IndexKind != "PGA")
        {
            throw new InvalidOperationException(
                $"IndexKind of '{vectorProperty.IndexKind}' for property '{vectorProperty.ModelName}' is not supported. Pinecone only supports 'PGA' (Pinecone Graph Algorithm), which is always enabled.");
        }

        CreateIndexRequest request = new()
        {
            Name = this.Name,
            Dimension = vectorProperty.Dimensions,
            Metric = MapDistanceFunction(vectorProperty),
            Spec = new ServerlessIndexSpec
            {
                Serverless = new ServerlessSpec
                {
                    Cloud = MapCloud(this._options.ServerlessIndexCloud),
                    Region = this._options.ServerlessIndexRegion,
                }
            },
        };

        return this.RunCollectionOperationAsync("CreateCollection",
            () => this._pineconeClient.CreateIndexAsync(request, cancellationToken: cancellationToken));
    }

    /// <inheritdoc />
    public async Task CreateCollectionIfNotExistsAsync(CancellationToken cancellationToken = default)
    {
        if (!await this.CollectionExistsAsync(cancellationToken).ConfigureAwait(false))
        {
            try
            {
                await this.CreateCollectionAsync(cancellationToken).ConfigureAwait(false);
            }
            catch (VectorStoreOperationException ex) when (ex.InnerException is PineconeApiException apiEx && apiEx.InnerException is ConflictError)
            {
                // If the collection got created in the meantime, we should ignore the exception.
            }
        }
    }

    /// <inheritdoc />
    public async Task DeleteCollectionAsync(CancellationToken cancellationToken = default)
    {
        try
        {
            await this._pineconeClient.DeleteIndexAsync(this.Name, cancellationToken: cancellationToken).ConfigureAwait(false);
        }
        catch (NotFoundError)
        {
            // If the collection does not exist, we should ignore the exception.
        }
        catch (PineconeApiException other)
        {
            throw new VectorStoreOperationException("Call to vector store failed.", other)
            {
                VectorStoreSystemName = PineconeConstants.VectorStoreSystemName,
                VectorStoreName = this._collectionMetadata.VectorStoreName,
                CollectionName = this.Name,
                OperationName = "DeleteCollection"
            };
        }
    }

    /// <inheritdoc />
    public async Task<TRecord?> GetAsync(TKey key, GetRecordOptions? options = null, CancellationToken cancellationToken = default)
    {
        if (options?.IncludeVectors is true && this._model.VectorProperties.Any(p => p.EmbeddingGenerator is not null))
        {
            throw new NotSupportedException(VectorDataStrings.IncludeVectorsNotSupportedWithEmbeddingGeneration);
        }

        Sdk.FetchRequest request = new()
        {
            Namespace = this._options.IndexNamespace,
            Ids = [this.GetStringKey(key)]
        };

        var response = await this.RunIndexOperationAsync(
            "Get",
            indexClient => indexClient.FetchAsync(request, cancellationToken: cancellationToken)).ConfigureAwait(false);

        var result = response.Vectors?.Values.FirstOrDefault();
        if (result is null)
        {
            return default;
        }

        StorageToDataModelMapperOptions mapperOptions = new() { IncludeVectors = options?.IncludeVectors is true };
        return VectorStoreErrorHandler.RunModelConversion(
            PineconeConstants.VectorStoreSystemName,
            this._collectionMetadata.VectorStoreName,
            this.Name,
            "Get",
            () => this._mapper.MapFromStorageToDataModel(result, mapperOptions));
    }

    /// <inheritdoc />
    public async IAsyncEnumerable<TRecord> GetAsync(
        IEnumerable<TKey> keys,
        GetRecordOptions? options = default,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        Verify.NotNull(keys);

        if (options?.IncludeVectors is true && this._model.VectorProperties.Any(p => p.EmbeddingGenerator is not null))
        {
            throw new NotSupportedException(VectorDataStrings.IncludeVectorsNotSupportedWithEmbeddingGeneration);
        }

#pragma warning disable CA1851 // Bogus: Possible multiple enumerations of 'IEnumerable' collection
        var keysList = keys switch
        {
            IEnumerable<string> k => k.ToList(),
            IEnumerable<object> k => k.Cast<string>().ToList(),
            _ => throw new UnreachableException("string key should have been validated during model building")
        };
#pragma warning restore CA1851

        if (keysList.Count == 0)
        {
            yield break;
        }

        Sdk.FetchRequest request = new()
        {
            Namespace = this._options.IndexNamespace,
            Ids = keysList
        };

        var response = await this.RunIndexOperationAsync(
            "GetBatch",
            indexClient => indexClient.FetchAsync(request, cancellationToken: cancellationToken)).ConfigureAwait(false);
        if (response.Vectors is null || response.Vectors.Count == 0)
        {
            yield break;
        }

        StorageToDataModelMapperOptions mapperOptions = new() { IncludeVectors = options?.IncludeVectors is true };
        var records = VectorStoreErrorHandler.RunModelConversion(
<<<<<<< HEAD
            DatabaseName,
            this.CollectionName,
            GetOperationName,
            () => results.Values.Select(x => this._mapper.MapFromStorageToDataModel(x, mapperOptions)).ToList());
            () => results.Values.Select(x => this._mapper.MapFromStorageToDataModel(x, mapperOptions)));
            () => results.Values.Select(x => this._mapper.MapFromStorageToDataModel(x, mapperOptions)));
=======
            PineconeConstants.VectorStoreSystemName,
            this._collectionMetadata.VectorStoreName,
            this.Name,
            "GetBatch",
            () => response.Vectors.Values.Select(x => this._mapper.MapFromStorageToDataModel(x, mapperOptions)));

>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        foreach (var record in records)
        {
            yield return record;
        }
    }

    /// <inheritdoc />
    public Task DeleteAsync(TKey key, CancellationToken cancellationToken = default)
    {
        Sdk.DeleteRequest request = new()
        {
            Namespace = this._options.IndexNamespace,
            Ids = [this.GetStringKey(key)]
        };

        return this.RunIndexOperationAsync(
            "Delete",
            indexClient => indexClient.DeleteAsync(request, cancellationToken: cancellationToken));
    }

    /// <inheritdoc />
    public Task DeleteAsync(IEnumerable<TKey> keys, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(keys);

        var keysList = keys switch
        {
            IEnumerable<string> k => k.ToList(),
            IEnumerable<object> k => k.Cast<string>().ToList(),
            _ => throw new UnreachableException("string key should have been validated during model building")
        };

        if (keysList.Count == 0)
        {
            return Task.CompletedTask;
        }

        Sdk.DeleteRequest request = new()
        {
            Namespace = this._options.IndexNamespace,
            Ids = keysList
        };

        return this.RunIndexOperationAsync(
            "DeleteBatch",
            indexClient => indexClient.DeleteAsync(request, cancellationToken: cancellationToken));
    }

    /// <inheritdoc />
    public async Task<TKey> UpsertAsync(TRecord record, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(record);

        // If an embedding generator is defined, invoke it once for all records.
        Embedding<float>? generatedEmbedding = null;

        Debug.Assert(this._model.VectorProperties.Count <= 1);
        if (this._model.VectorProperties is [{ EmbeddingGenerator: not null } vectorProperty])
        {
            if (vectorProperty.TryGenerateEmbedding<TRecord, Embedding<float>, ReadOnlyMemory<float>>(record, cancellationToken, out var task))
            {
                generatedEmbedding = await task.ConfigureAwait(false);
            }
            else
            {
                throw new InvalidOperationException(
                    $"The embedding generator configured on property '{vectorProperty.ModelName}' cannot produce an embedding of type '{typeof(Embedding<float>).Name}' for the given input type.");
            }
        }

        var vector = VectorStoreErrorHandler.RunModelConversion(
            PineconeConstants.VectorStoreSystemName,
            this._collectionMetadata.VectorStoreName,
            this.Name,
            "Upsert",
            () => this._mapper.MapFromDataToStorageModel(record, generatedEmbedding));

        Sdk.UpsertRequest request = new()
        {
            Namespace = this._options.IndexNamespace,
            Vectors = [vector],
        };

        await this.RunIndexOperationAsync(
            "Upsert",
            indexClient => indexClient.UpsertAsync(request, cancellationToken: cancellationToken)).ConfigureAwait(false);

        return (TKey)(object)vector.Id;
    }

    /// <inheritdoc />
    public async Task<IReadOnlyList<TKey>> UpsertAsync(IEnumerable<TRecord> records, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(records);

        // If an embedding generator is defined, invoke it once for all records.
        GeneratedEmbeddings<Embedding<float>>? generatedEmbeddings = null;

        if (this._model.VectorProperties is [{ EmbeddingGenerator: not null } vectorProperty])
        {
            var recordsList = records is IReadOnlyList<TRecord> r ? r : records.ToList();

            if (recordsList.Count == 0)
            {
                return [];
            }

            records = recordsList;

            if (vectorProperty.TryGenerateEmbeddings<TRecord, Embedding<float>, ReadOnlyMemory<float>>(records, cancellationToken, out var task))
            {
                generatedEmbeddings = await task.ConfigureAwait(false);

                Debug.Assert(generatedEmbeddings.Count == recordsList.Count);
            }
            else
            {
                throw new InvalidOperationException(
                    $"The embedding generator configured on property '{vectorProperty.ModelName}' cannot produce an embedding of type '{typeof(Embedding<float>).Name}' for the given input type.");
            }
        }

        var vectors = VectorStoreErrorHandler.RunModelConversion(
            PineconeConstants.VectorStoreSystemName,
            this._collectionMetadata.VectorStoreName,
            this.Name,
            "UpsertBatch",
            () => records.Select((r, i) => this._mapper.MapFromDataToStorageModel(r, generatedEmbeddings?[i])).ToList());

        if (vectors.Count == 0)
        {
            return [];
        }

        Sdk.UpsertRequest request = new()
        {
            Namespace = this._options.IndexNamespace,
            Vectors = vectors,
        };

        await this.RunIndexOperationAsync(
            "UpsertBatch",
            indexClient => indexClient.UpsertAsync(request, cancellationToken: cancellationToken)).ConfigureAwait(false);

        return vectors.Select(x => (TKey)(object)x.Id).ToList();
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
                var embedding = await generator.GenerateAsync(value, new() { Dimensions = vectorProperty.Dimensions }, cancellationToken).ConfigureAwait(false);

                await foreach (var record in this.SearchCoreAsync(embedding.Vector, top, vectorProperty, operationName: "Search", options, cancellationToken).ConfigureAwait(false))
                {
                    yield return record;
                }

                yield break;

            case null:
                throw new InvalidOperationException(VectorDataStrings.NoEmbeddingGeneratorWasConfiguredForSearch);

            default:
                throw new InvalidOperationException(
                    PineconeVectorStoreRecordFieldMapping.s_supportedVectorTypes.Contains(typeof(TInput))
                        ? string.Format(VectorDataStrings.EmbeddingTypePassedToSearchAsync)
                        : string.Format(VectorDataStrings.IncompatibleEmbeddingGeneratorWasConfiguredForInputType, typeof(TInput).Name, vectorProperty.EmbeddingGenerator.GetType().Name));
        }
    }

    /// <inheritdoc />
<<<<<<< HEAD
    public IAsyncEnumerable<VectorSearchResult<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, VectorSearchOptions? options = null, CancellationToken cancellationToken = default)
    /// <inheritdoc />
<<<<<<< main
<<<<<<< main
    public Task<VectorSearchResults<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, VectorSearchOptions? options = null, CancellationToken cancellationToken = default)
>>>>>>> upstream/main
=======
    public async Task<VectorSearchResults<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, VectorSearchOptions? options = null, CancellationToken cancellationToken = default)
>>>>>>> upstream/main
=======
    public Task<VectorSearchResults<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, VectorSearchOptions? options = null, CancellationToken cancellationToken = default)
    {
        throw new NotImplementedException();
    public Task<VectorSearchResults<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, VectorSearchOptions? options = null, CancellationToken cancellationToken = default)
    public async Task<VectorSearchResults<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, VectorSearchOptions? options = null, CancellationToken cancellationToken = default)
>>>>>>> origin/main
    {
        Verify.NotNull(vector);

        if (vector is not ReadOnlyMemory<float> floatVector)
        {
            throw new NotSupportedException($"The provided vector type {vector.GetType().FullName} is not supported by the Pinecone connector." +
                $"Supported types are: {typeof(ReadOnlyMemory<float>).FullName}");
        }

        // Resolve options and build filter clause.
        var internalOptions = options ?? s_defaultVectorSearchOptions;
        var mapperOptions = new StorageToDataModelMapperOptions { IncludeVectors = options?.IncludeVectors ?? false };
        var filter = PineconeVectorStoreCollectionSearchMapping.BuildSearchFilter(
            internalOptions.Filter?.FilterClauses,
            this._propertyReader.StoragePropertyNamesMap);

        // Get the current index.
        var indexNamespace = this.GetIndexNamespace();
        var index = await this.GetIndexAsync(this.CollectionName, cancellationToken).ConfigureAwait(false);

        // Search.
        var results = await this.RunOperationAsync(
            QueryOperationName,
            () => index.Query(
                floatVector.ToArray(),
                (uint)(internalOptions.Skip + internalOptions.Top),
                filter,
                sparseValues: null,
                indexNamespace,
                internalOptions.IncludeVectors,
                includeMetadata: true,
                cancellationToken)).ConfigureAwait(false);

        // Skip the required results for paging.
        var skippedResults = results.Skip(internalOptions.Skip);

        // Map the results.
        var records = VectorStoreErrorHandler.RunModelConversion(
            DatabaseName,
            this.CollectionName,
            QueryOperationName,
            () =>
            {
                // First convert to Vector objects, since the
                // mapper requires these as input.
                var vectorResults = skippedResults.Select(x => (
                    Vector: new Vector()
                    {
                        Id = x.Id,
                        Values = x.Values ?? Array.Empty<float>(),
                        Metadata = x.Metadata,
                        SparseValues = x.SparseValues
                    },
                    x.Score));

                return vectorResults.Select(x => new VectorSearchResult<TRecord>(
                    this._mapper.MapFromStorageToDataModel(x.Vector, mapperOptions),
                    x.Score));
            });

        return new VectorSearchResults<TRecord>(records.ToAsyncEnumerable());
    }

    private async Task<T> RunOperationAsync<T>(string operationName, Func<Task<T>> operation)
    {
        try
        {
            return await operation.Invoke().ConfigureAwait(false);
        }
        catch (RpcException ex)
        {
            throw new VectorStoreOperationException("Call to vector store failed.", ex)
            {
                VectorStoreType = DatabaseName,
                CollectionName = this.CollectionName,
                OperationName = operationName
            };
        }
    }

    private async Task RunOperationAsync(string operationName, Func<Task> operation)
    {
        try
        {
            await operation.Invoke().ConfigureAwait(false);
        }
        catch (RpcException ex)
        {
            throw new VectorStoreOperationException("Call to vector store failed.", ex)
            {
                VectorStoreType = DatabaseName,
                CollectionName = this.CollectionName,
                OperationName = operationName
            };
        }
    }

    private async Task<Sdk.Index<GrpcTransport>> GetIndexAsync(string indexName, CancellationToken cancellationToken)
    {
        this._index ??= await this._pineconeClient.GetIndex(indexName, cancellationToken).ConfigureAwait(false);

        return this._index;
    }

    private string? GetIndexNamespace()
        => this._options.IndexNamespace;
}

// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
using Grpc.Core;
using Microsoft.Extensions.VectorData;
using Pinecone;
using Pinecone.Grpc;
using Sdk = Pinecone;

namespace Microsoft.SemanticKernel.Connectors.Pinecone;

/// <summary>
/// Service for storing and retrieving vector records, that uses Pinecone as the underlying storage.
/// </summary>
/// <typeparam name="TRecord">The data model to use for adding, updating and retrieving data from storage.</typeparam>
#pragma warning disable CA1711 // Identifiers should not have incorrect suffix
public sealed class PineconeVectorStoreRecordCollection<TRecord> : IVectorStoreRecordCollection<string, TRecord>
#pragma warning restore CA1711 // Identifiers should not have incorrect suffix
{
    private const string DatabaseName = "Pinecone";
    private const string CreateCollectionName = "CreateCollection";
    private const string CollectionExistsName = "CollectionExists";
    private const string DeleteCollectionName = "DeleteCollection";

    private const string UpsertOperationName = "Upsert";
    private const string DeleteOperationName = "Delete";
    private const string GetOperationName = "Get";
<<<<<<< Updated upstream

    private const string QueryOperationName = "Query";

    private static readonly VectorSearchOptions s_defaultVectorSearchOptions = new();

=======
    private const string QueryOperationName = "Query";

    private static readonly VectorSearchOptions s_defaultVectorSearchOptions = new();
>>>>>>> Stashed changes
    private const string QueryOperationName = "Query";

    private static readonly VectorSearchOptions s_defaultVectorSearchOptions = new();

    private readonly Sdk.PineconeClient _pineconeClient;
    private readonly PineconeVectorStoreRecordCollectionOptions<TRecord> _options;
    private readonly VectorStoreRecordDefinition _vectorStoreRecordDefinition;
    private readonly VectorStoreRecordDefinition _vectorStoreRecordDefinition;
    private readonly VectorStoreRecordPropertyReader _propertyReader;
    private readonly VectorStoreRecordPropertyReader _propertyReader;
    private readonly VectorStoreRecordPropertyReader _propertyReader;
    private readonly IVectorStoreRecordMapper<TRecord, Sdk.Vector> _mapper;

    private Sdk.Index<GrpcTransport>? _index;

    /// <inheritdoc />
    public string CollectionName { get; }

    /// <summary>
    /// Initializes a new instance of the <see cref="PineconeVectorStoreRecordCollection{TRecord}"/> class.
    /// </summary>
    /// <param name="pineconeClient">Pinecone client that can be used to manage the collections and vectors in a Pinecone store.</param>
    /// <param name="options">Optional configuration options for this class.</param>
    /// <exception cref="ArgumentNullException">Thrown if the <paramref name="pineconeClient"/> is null.</exception>
    /// <param name="collectionName">The name of the collection that this <see cref="PineconeVectorStoreRecordCollection{TRecord}"/> will access.</param>
    /// <exception cref="ArgumentException">Thrown for any misconfigured options.</exception>
    public PineconeVectorStoreRecordCollection(Sdk.PineconeClient pineconeClient, string collectionName, PineconeVectorStoreRecordCollectionOptions<TRecord>? options = null)
    {
        Verify.NotNull(pineconeClient);

        this._pineconeClient = pineconeClient;
        this.CollectionName = collectionName;
        this._options = options ?? new PineconeVectorStoreRecordCollectionOptions<TRecord>();
        this._vectorStoreRecordDefinition = this._options.VectorStoreRecordDefinition ?? VectorStoreRecordPropertyReader.CreateVectorStoreRecordDefinitionFromType(typeof(TRecord), true);

        if (this._options.VectorCustomMapper is null)
        {
            this._mapper = new PineconeVectorStoreRecordMapper<TRecord>(this._vectorStoreRecordDefinition);
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
        this._propertyReader = new VectorStoreRecordPropertyReader(
            typeof(TRecord),
            this._options.VectorStoreRecordDefinition,
            new()
            {
                RequiresAtLeastOneVector = true,
                SupportsMultipleKeys = false,
                SupportsMultipleVectors = false,
            });

        if (this._options.VectorCustomMapper is null)
        {
            this._mapper = new PineconeVectorStoreRecordMapper<TRecord>(this._propertyReader);
        }
        else
        {
            this._mapper = this._options.VectorCustomMapper;
        }
    }

    /// <inheritdoc />
    public async Task<bool> CollectionExistsAsync(CancellationToken cancellationToken = default)
    {
        var result = await this.RunOperationAsync(
            CollectionExistsName,
            async () =>
            {
                var collections = await this._pineconeClient.ListIndexes(cancellationToken).ConfigureAwait(false);

                return collections.Any(x => x.Name == this.CollectionName);
            }).ConfigureAwait(false);

        return result;
    }

    /// <inheritdoc />
    public async Task CreateCollectionAsync(CancellationToken cancellationToken = default)
    {
        // we already run through record property validation, so a single VectorStoreRecordVectorProperty is guaranteed.
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
        var vectorProperty = this._vectorStoreRecordDefinition.Properties.OfType<VectorStoreRecordVectorProperty>().First();
        var vectorProperty = this._vectorStoreRecordDefinition.Properties.OfType<VectorStoreRecordVectorProperty>().First();
        var vectorProperty = this._propertyReader.VectorProperty!;
        var vectorProperty = this._propertyReader.VectorProperty!;
        var (dimension, metric) = PineconeVectorStoreCollectionCreateMapping.MapServerlessIndex(vectorProperty);

        await this.RunOperationAsync(
            CreateCollectionName,
            () => this._pineconeClient.CreateServerlessIndex(
                this.CollectionName,
                dimension,
                metric,
                this._options.ServerlessIndexCloud,
                this._options.ServerlessIndexRegion,
                cancellationToken)).ConfigureAwait(false);
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
    public Task DeleteCollectionAsync(CancellationToken cancellationToken = default)
        => this.RunOperationAsync(
            DeleteCollectionName,
            () => this._pineconeClient.DeleteIndex(this.CollectionName, cancellationToken));

    /// <inheritdoc />
    public async Task<TRecord?> GetAsync(string key, GetRecordOptions? options = null, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(key);

        var records = await this.GetBatchAsync([key], options, cancellationToken).ToListAsync(cancellationToken).ConfigureAwait(false);

        return records.FirstOrDefault();
    }

    /// <inheritdoc />
    public async IAsyncEnumerable<TRecord> GetBatchAsync(
        IEnumerable<string> keys,
        GetRecordOptions? options = default,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        Verify.NotNull(keys);

        var indexNamespace = this.GetIndexNamespace();
        var mapperOptions = new StorageToDataModelMapperOptions { IncludeVectors = options?.IncludeVectors ?? false };

        var index = await this.GetIndexAsync(this.CollectionName, cancellationToken).ConfigureAwait(false);

        var results = await this.RunOperationAsync(
            GetOperationName,
            () => index.Fetch(keys, indexNamespace, cancellationToken)).ConfigureAwait(false);

        var records = VectorStoreErrorHandler.RunModelConversion(
            DatabaseName,
            this.CollectionName,
            GetOperationName,
            () => results.Values.Select(x => this._mapper.MapFromStorageToDataModel(x, mapperOptions)).ToList());
            () => results.Values.Select(x => this._mapper.MapFromStorageToDataModel(x, mapperOptions)));
            () => results.Values.Select(x => this._mapper.MapFromStorageToDataModel(x, mapperOptions)));
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
        foreach (var record in records)
        {
            yield return record;
        }
    }

    /// <inheritdoc />
    public Task DeleteAsync(string key, DeleteRecordOptions? options = default, CancellationToken cancellationToken = default)
    {
        Verify.NotNullOrWhiteSpace(key);

        return this.DeleteBatchAsync([key], options, cancellationToken);
    }

    /// <inheritdoc />
    public async Task DeleteBatchAsync(IEnumerable<string> keys, DeleteRecordOptions? options = default, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(keys);

        var indexNamespace = this.GetIndexNamespace();

        var index = await this.GetIndexAsync(this.CollectionName, cancellationToken).ConfigureAwait(false);

        await this.RunOperationAsync(
            DeleteOperationName,
            () => index.Delete(keys, indexNamespace, cancellationToken)).ConfigureAwait(false);
    }

    /// <inheritdoc />
    public async Task<string> UpsertAsync(TRecord record, UpsertRecordOptions? options = default, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(record);

        var indexNamespace = this.GetIndexNamespace();

        var index = await this.GetIndexAsync(this.CollectionName, cancellationToken).ConfigureAwait(false);

        var vector = VectorStoreErrorHandler.RunModelConversion(
            DatabaseName,
            this.CollectionName,
            UpsertOperationName,
            () => this._mapper.MapFromDataToStorageModel(record));

        await this.RunOperationAsync(
            UpsertOperationName,
            () => index.Upsert([vector], indexNamespace, cancellationToken)).ConfigureAwait(false);

        return vector.Id;
    }

    /// <inheritdoc />
    public async IAsyncEnumerable<string> UpsertBatchAsync(
        IEnumerable<TRecord> records,
        UpsertRecordOptions? options = default,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        Verify.NotNull(records);

        var indexNamespace = this.GetIndexNamespace();

        var index = await this.GetIndexAsync(this.CollectionName, cancellationToken).ConfigureAwait(false);

        var vectors = VectorStoreErrorHandler.RunModelConversion(
            DatabaseName,
            this.CollectionName,
            UpsertOperationName,
            () => records.Select(this._mapper.MapFromDataToStorageModel).ToList());

        await this.RunOperationAsync(
            UpsertOperationName,
            () => index.Upsert(vectors, indexNamespace, cancellationToken)).ConfigureAwait(false);

        foreach (var vector in vectors)
        {
            yield return vector.Id;
        }
    }

    /// <inheritdoc />
    public IAsyncEnumerable<VectorSearchResult<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, VectorSearchOptions? options = null, CancellationToken cancellationToken = default)
    /// <inheritdoc />
    public Task<VectorSearchResults<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, VectorSearchOptions? options = null, CancellationToken cancellationToken = default)
    {
        throw new NotImplementedException();
    public Task<VectorSearchResults<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, VectorSearchOptions? options = null, CancellationToken cancellationToken = default)
    public async Task<VectorSearchResults<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, VectorSearchOptions? options = null, CancellationToken cancellationToken = default)
=======
    public IAsyncEnumerable<VectorSearchResult<TRecord>> SearchEmbeddingAsync<TVector>(
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

    private async IAsyncEnumerable<VectorSearchResult<TRecord>> SearchCoreAsync<TVector>(
        TVector vector,
        int top,
        VectorStoreRecordVectorPropertyModel vectorProperty,
        string operationName,
        VectorSearchOptions<TRecord> options,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
        where TVector : notnull
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        Verify.NotNull(vector);
        Verify.NotLessThan(top, 1);

        if (vector is not ReadOnlyMemory<float> floatVector)
        {
            throw new NotSupportedException($"The provided vector type {vector.GetType().FullName} is not supported by the Pinecone connector." +
                $"Supported types are: {typeof(ReadOnlyMemory<float>).FullName}");
        }

        if (options.IncludeVectors && this._model.VectorProperties.Any(p => p.EmbeddingGenerator is not null))
        {
            throw new NotSupportedException(VectorDataStrings.IncludeVectorsNotSupportedWithEmbeddingGeneration);
        }

#pragma warning disable CS0618 // VectorSearchFilter is obsolete
        var filter = options switch
        {
            { OldFilter: not null, Filter: not null } => throw new ArgumentException("Either Filter or OldFilter can be specified, but not both"),
            { OldFilter: VectorSearchFilter legacyFilter } => PineconeVectorStoreCollectionSearchMapping.BuildSearchFilter(options.OldFilter?.FilterClauses, this._model),
            { Filter: Expression<Func<TRecord, bool>> newFilter } => new PineconeFilterTranslator().Translate(newFilter, this._model),
            _ => null
        };
#pragma warning restore CS0618

        Sdk.QueryRequest request = new()
        {
            TopK = (uint)(top + options.Skip),
            Namespace = this._options.IndexNamespace,
            IncludeValues = options.IncludeVectors,
            IncludeMetadata = true,
            Vector = floatVector,
            Filter = filter,
        };

        Sdk.QueryResponse response = await this.RunIndexOperationAsync(
            "VectorizedSearch",
            indexClient => indexClient.QueryAsync(request, cancellationToken: cancellationToken)).ConfigureAwait(false);

        if (response.Matches is null)
        {
            yield break;
        }

        // Pinecone does not provide a way to skip results, so we need to do it manually.
        var skippedResults = response.Matches
            .Skip(options.Skip);

        StorageToDataModelMapperOptions mapperOptions = new() { IncludeVectors = options.IncludeVectors is true };
        var records = VectorStoreErrorHandler.RunModelConversion(
            PineconeConstants.VectorStoreSystemName,
            this._collectionMetadata.VectorStoreName,
            this.Name,
            "VectorizedSearch",
            () => skippedResults.Select(x => new VectorSearchResult<TRecord>(this._mapper.MapFromStorageToDataModel(new Sdk.Vector()
            {
                Id = x.Id,
                Values = x.Values ?? Array.Empty<float>(),
                Metadata = x.Metadata,
                SparseValues = x.SparseValues
            }, mapperOptions), x.Score)));

        foreach (var record in records)
        {
            yield return record;
        }
    }

    /// <inheritdoc />
    [Obsolete("Use either SearchEmbeddingAsync to search directly on embeddings, or SearchAsync to handle embedding generation internally as part of the call.")]
    public IAsyncEnumerable<VectorSearchResult<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, int top, VectorSearchOptions<TRecord>? options = null, CancellationToken cancellationToken = default)
        where TVector : notnull
        => this.SearchEmbeddingAsync(vector, top, options, cancellationToken);

    #endregion Search

    /// <inheritdoc/>
    public async IAsyncEnumerable<TRecord> GetAsync(Expression<Func<TRecord, bool>> filter, int top, GetFilteredRecordOptions<TRecord>? options = null, [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        Verify.NotNull(filter);
        Verify.NotLessThan(top, 1);

        if (options?.OrderBy.Values.Count > 0)
        {
            throw new NotSupportedException("Pinecone does not support ordering.");
        }

        options ??= new();

        if (options.IncludeVectors && this._model.VectorProperties.Any(p => p.EmbeddingGenerator is not null))
        {
            throw new NotSupportedException(VectorDataStrings.IncludeVectorsNotSupportedWithEmbeddingGeneration);
        }

        Sdk.QueryRequest request = new()
        {
            TopK = (uint)(top + options.Skip),
            Namespace = this._options.IndexNamespace,
            IncludeValues = options.IncludeVectors,
            IncludeMetadata = true,
            // "Either 'vector' or 'ID' must be provided"
            // Since we are doing a query, we don't have a vector to provide, so we fake one.
            // When https://github.com/pinecone-io/pinecone-dotnet-client/issues/43 gets implemented, we need to switch.
            Vector = new ReadOnlyMemory<float>(new float[this._model.VectorProperty.Dimensions]),
            Filter = new PineconeFilterTranslator().Translate(filter, this._model),
        };

        Sdk.QueryResponse response = await this.RunIndexOperationAsync(
            "Get",
            indexClient => indexClient.QueryAsync(request, cancellationToken: cancellationToken)).ConfigureAwait(false);

        if (response.Matches is null)
        {
            yield break;
        }

        StorageToDataModelMapperOptions mapperOptions = new() { IncludeVectors = options.IncludeVectors is true };
        var records = VectorStoreErrorHandler.RunModelConversion(
            PineconeConstants.VectorStoreSystemName,
            this._collectionMetadata.VectorStoreName,
            this.Name,
            "Query",
            () => response.Matches.Skip(options.Skip).Select(x => this._mapper.MapFromStorageToDataModel(new Sdk.Vector()
            {
                Id = x.Id,
                Values = x.Values ?? Array.Empty<float>(),
                Metadata = x.Metadata,
                SparseValues = x.SparseValues
            }, mapperOptions)));

        foreach (var record in records)
        {
            yield return record;
        }
    }

    /// <inheritdoc />
    public object? GetService(Type serviceType, object? serviceKey = null)
    {
        Verify.NotNull(serviceType);

        return
            serviceKey is not null ? null :
            serviceType == typeof(VectorStoreRecordCollectionMetadata) ? this._collectionMetadata :
            serviceType == typeof(Sdk.PineconeClient) ? this._pineconeClient :
            serviceType.IsInstanceOfType(this) ? this :
            null;
    }

    private async Task<T> RunIndexOperationAsync<T>(string operationName, Func<IndexClient, Task<T>> operation)
    {
        try
        {
            if (this._indexClient is null)
            {
                // If we don't provide "host" to the Index method, it's going to perform
                // a blocking call to DescribeIndexAsync!!
                string hostName = (await this._pineconeClient.DescribeIndexAsync(this.Name).ConfigureAwait(false)).Host;
                this._indexClient = this._pineconeClient.Index(host: hostName);
            }

            return await operation.Invoke(this._indexClient).ConfigureAwait(false);
        }
        catch (PineconeApiException ex)
        {
            throw new VectorStoreOperationException("Call to vector store failed.", ex)
            {
                VectorStoreSystemName = PineconeConstants.VectorStoreSystemName,
                VectorStoreName = this._collectionMetadata.VectorStoreName,
                CollectionName = this.Name,
                OperationName = operationName
            };
        }
    }

    private async Task<T> RunCollectionOperationAsync<T>(string operationName, Func<Task<T>> operation)
    {
        try
        {
            return await operation.Invoke().ConfigureAwait(false);
        }
        catch (PineconeApiException ex)
        {
            throw new VectorStoreOperationException("Call to vector store failed.", ex)
            {
                VectorStoreSystemName = PineconeConstants.VectorStoreSystemName,
                VectorStoreName = this._collectionMetadata.VectorStoreName,
                CollectionName = this.Name,
                OperationName = operationName
            };
        }
    }

    private static ServerlessSpecCloud MapCloud(string serverlessIndexCloud)
        => serverlessIndexCloud switch
        {
            "aws" => ServerlessSpecCloud.Aws,
            "azure" => ServerlessSpecCloud.Azure,
            "gcp" => ServerlessSpecCloud.Gcp,
            _ => throw new ArgumentException($"Invalid serverless index cloud: {serverlessIndexCloud}.", nameof(serverlessIndexCloud))
        };

    private static CreateIndexRequestMetric MapDistanceFunction(VectorStoreRecordVectorPropertyModel vectorProperty)
        => vectorProperty.DistanceFunction switch
        {
            DistanceFunction.CosineSimilarity or null => CreateIndexRequestMetric.Cosine,
            DistanceFunction.DotProductSimilarity => CreateIndexRequestMetric.Dotproduct,
            DistanceFunction.EuclideanSquaredDistance => CreateIndexRequestMetric.Euclidean,
            _ => throw new NotSupportedException($"Distance function '{vectorProperty.DistanceFunction}' is not supported.")
        };

    private static void VerifyCollectionName(string collectionName)
    {
        Verify.NotNullOrWhiteSpace(collectionName);

        // Based on https://docs.pinecone.io/troubleshooting/restrictions-on-index-names
        foreach (char character in collectionName)
        {
            if (!((character is >= 'a' and <= 'z') || character is '-' || (character is >= '0' and <= '9')))
            {
                throw new ArgumentException("Collection name must contain only ASCII lowercase letters, digits and dashes.", nameof(collectionName));
            }
        }
    }

    private string GetStringKey(TKey key)
    {
        Verify.NotNull(key);

        var stringKey = key as string ?? throw new UnreachableException("string key should have been validated during model building");

        Verify.NotNullOrWhiteSpace(stringKey, nameof(key));

        return stringKey;
    }
}
