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

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Linq.Expressions;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Runtime.CompilerServices;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.VectorData;
using Microsoft.Extensions.VectorData.ConnectorSupport;
using Microsoft.Extensions.VectorData.Properties;

namespace Microsoft.SemanticKernel.Connectors.Weaviate;

/// <summary>
/// Service for storing and retrieving vector records, that uses Weaviate as the underlying storage.
/// </summary>
/// <typeparam name="TKey">The data type of the record key. Can be either <see cref="Guid"/>, or <see cref="object"/> for dynamic mapping.</typeparam>
/// <typeparam name="TRecord">The data model to use for adding, updating and retrieving data from storage.</typeparam>
#pragma warning disable CA1711 // Identifiers should not have incorrect suffix
public sealed class WeaviateVectorStoreRecordCollection<TKey, TRecord> : IVectorStoreRecordCollection<TKey, TRecord>, IKeywordHybridSearch<TRecord>
    where TKey : notnull
    where TRecord : notnull
#pragma warning restore CA1711 // Identifiers should not have incorrect suffix
{
<<<<<<< HEAD
    /// <summary>The name of this database for telemetry purposes.</summary>
    private const string DatabaseName = "Weaviate";

    /// <summary>A set of types that a key on the provided model may have.</summary>
    private static readonly HashSet<Type> s_supportedKeyTypes =
    [
        typeof(Guid)
    ];

    /// <summary>A set of types that vectors on the provided model may have.</summary>
    private static readonly HashSet<Type> s_supportedVectorTypes =
    [
        typeof(ReadOnlyMemory<float>),
        typeof(ReadOnlyMemory<float>?),
        typeof(ReadOnlyMemory<double>),
        typeof(ReadOnlyMemory<double>?)
    ];

    /// <summary>A set of types that data properties on the provided model may have.</summary>
    private static readonly HashSet<Type> s_supportedDataTypes =
    [
        typeof(string),
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
        typeof(bool),
        typeof(bool?),
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
        typeof(bool),
        typeof(bool?),
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
        typeof(int),
        typeof(int?),
        typeof(long),
        typeof(long?),
        typeof(short),
        typeof(short?),
        typeof(byte),
        typeof(byte?),
        typeof(float),
        typeof(float?),
        typeof(double),
        typeof(double?),
        typeof(decimal),
        typeof(decimal?),
        typeof(DateTime),
        typeof(DateTime?),
        typeof(DateTimeOffset),
        typeof(DateTimeOffset?),
        typeof(Guid),
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
        typeof(Guid?),
        typeof(bool),
        typeof(bool?)
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
        typeof(Guid?),
        typeof(bool),
        typeof(bool?)
=======
        typeof(Guid?)
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
        typeof(Guid?)
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
        typeof(Guid?)
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
    ];
=======
    /// <summary>Metadata about vector store record collection.</summary>
    private readonly VectorStoreRecordCollectionMetadata _collectionMetadata;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

    /// <summary>Default JSON serializer options.</summary>
    private static readonly JsonSerializerOptions s_jsonSerializerOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        Converters =
        {
            new WeaviateDateTimeOffsetConverter(),
            new WeaviateNullableDateTimeOffsetConverter()
        }
    };

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
    /// <summary>The default options for vector search.</summary>
    private static readonly VectorSearchOptions<TRecord> s_defaultVectorSearchOptions = new();

    /// <summary>The default options for hybrid vector search.</summary>
    private static readonly HybridSearchOptions<TRecord> s_defaultKeywordVectorizedHybridSearchOptions = new();

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
    /// <summary>The default options for vector search.</summary>
    private static readonly VectorSearchOptions s_defaultVectorSearchOptions = new();

>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
=======
<<<<<<< div
>>>>>>> div
=======
    /// <summary>The default options for vector search.</summary>
    private static readonly VectorSearchOptions s_defaultVectorSearchOptions = new();

<<<<<<< main
>>>>>>> upstream/main
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
>>>>>>> div
    /// <summary><see cref="HttpClient"/> that is used to interact with Weaviate API.</summary>
    private readonly HttpClient _httpClient;

    /// <summary>Optional configuration options for this class.</summary>
    private readonly WeaviateVectorStoreRecordCollectionOptions<TRecord> _options;

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
    /// <summary>A definition of the current storage model.</summary>
    private readonly VectorStoreRecordDefinition _vectorStoreRecordDefinition;

    /// <summary>A dictionary that maps from a property name to the storage name that should be used when serializing it to JSON for data and vector properties.</summary>
    private readonly Dictionary<string, string> _storagePropertyNames;

    /// <summary>The key property of the current storage model.</summary>
    private readonly VectorStoreRecordKeyProperty _keyProperty;

    /// <summary>The data properties of the current storage model.</summary>
    private readonly List<VectorStoreRecordDataProperty> _dataProperties;

    /// <summary>The vector properties of the current storage model.</summary>
    private readonly List<VectorStoreRecordVectorProperty> _vectorProperties;

    /// <summary>The mapper to use when mapping between the consumer data model and the Weaviate record.</summary>
    private readonly IVectorStoreRecordMapper<TRecord, JsonNode> _mapper;
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
    /// <summary>A helper to access property information for the current data model and record definition.</summary>
    private readonly VectorStoreRecordPropertyReader _propertyReader;
=======
    /// <summary>The model for this collection.</summary>
    private readonly VectorStoreRecordModel _model;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

    /// <summary>First vector property for the collections that this class is used with.</summary>
    private readonly VectorStoreRecordVectorProperty? _firstVectorProperty;

    /// <summary>Collection of storage names for data properties of the current storage model.</summary>
    private readonly List<string> _dataPropertyStorageNames;

    /// <summary>Collection of storage names for vector properties of the current storage model.</summary>
    private readonly List<string> _vectorPropertyStorageNames;

    /// <summary>The mapper to use when mapping between the consumer data model and the Weaviate record.</summary>
<<<<<<< HEAD
    private readonly IVectorStoreRecordMapper<TRecord, JsonObject> _mapper;
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
    private readonly IWeaviateMapper<TRecord> _mapper;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

    /// <summary>Weaviate endpoint.</summary>
    private readonly Uri _endpoint;

    /// <summary>Weaviate API key.</summary>
    private readonly string? _apiKey;

    /// <inheritdoc />
    public string Name { get; }

    /// <summary>
    /// Initializes a new instance of the <see cref="WeaviateVectorStoreRecordCollection{TKey, TRecord}"/> class.
    /// </summary>
    /// <param name="httpClient">
    /// <see cref="HttpClient"/> that is used to interact with Weaviate API.
    /// <see cref="HttpClient.BaseAddress"/> should point to remote or local cluster and API key can be configured via <see cref="HttpClient.DefaultRequestHeaders"/>.
    /// It's also possible to provide these parameters via <see cref="WeaviateVectorStoreRecordCollectionOptions{TRecord}"/>.
    /// </param>
    /// <param name="name">The name of the collection that this <see cref="WeaviateVectorStoreRecordCollection{TKey, TRecord}"/> will access.</param>
    /// <param name="options">Optional configuration options for this class.</param>
    /// <remarks>The collection name must start with a capital letter and contain only ASCII letters and digits.</remarks>
    public WeaviateVectorStoreRecordCollection(
        HttpClient httpClient,
        string name,
        WeaviateVectorStoreRecordCollectionOptions<TRecord>? options = default)
    {
        // Verify.
        Verify.NotNull(httpClient);
        VerifyCollectionName(name);

        if (typeof(TKey) != typeof(Guid) && typeof(TKey) != typeof(object))
        {
            throw new NotSupportedException($"Only {nameof(Guid)} key is supported (and object for dynamic mapping).");
        }

        var endpoint = (options?.Endpoint ?? httpClient.BaseAddress) ?? throw new ArgumentException($"Weaviate endpoint should be provided via HttpClient.BaseAddress property or {nameof(WeaviateVectorStoreRecordCollectionOptions<TRecord>)} options parameter.");

        // Assign.
        this._httpClient = httpClient;
        this._endpoint = endpoint;
        this.Name = name;
        this._options = options ?? new();
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
        this._vectorStoreRecordDefinition = this._options.VectorStoreRecordDefinition ?? VectorStoreRecordPropertyReader.CreateVectorStoreRecordDefinitionFromType(typeof(TRecord), supportsMultipleVectors: true);
        this._apiKey = this._options.ApiKey;

        // Validate property types.
        var properties = VectorStoreRecordPropertyReader.SplitDefinitionAndVerify(typeof(TRecord).Name, this._vectorStoreRecordDefinition, supportsMultipleVectors: true, requiresAtLeastOneVector: false);
        VectorStoreRecordPropertyReader.VerifyPropertyTypes([properties.KeyProperty], s_supportedKeyTypes, "Key");
        VectorStoreRecordPropertyReader.VerifyPropertyTypes(properties.DataProperties, s_supportedDataTypes, "Data", supportEnumerable: true);
        VectorStoreRecordPropertyReader.VerifyPropertyTypes(properties.VectorProperties, s_supportedVectorTypes, "Vector");

        // Assign properties and names for later usage.
        this._storagePropertyNames = VectorStoreRecordPropertyReader.BuildPropertyNameToJsonPropertyNameMap(properties, typeof(TRecord), s_jsonSerializerOptions);
        this._keyProperty = properties.KeyProperty;
        this._dataProperties = properties.DataProperties;
        this._vectorProperties = properties.VectorProperties;

        // Assign mapper.
        this._mapper = this._options.JsonNodeCustomMapper ??
            new WeaviateVectorStoreRecordMapper<TRecord>(
                this.CollectionName,
                this._keyProperty,
                this._dataProperties,
                this._vectorProperties,
                this._storagePropertyNames,
                s_jsonSerializerOptions);
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
        this._apiKey = this._options.ApiKey;
        this._model = new WeaviateModelBuilder(this._options.HasNamedVectors)
            .Build(typeof(TRecord), this._options.VectorStoreRecordDefinition, this._options.EmbeddingGenerator, s_jsonSerializerOptions);

        if (this._vectorProperties.Count > 0)
        {
            this._firstVectorProperty = this._vectorProperties[0];
        }

        this._dataPropertyStorageNames = this._dataProperties.Select(l => this._storagePropertyNames[l.DataModelPropertyName]).ToList();
        this._vectorPropertyStorageNames = this._vectorProperties.Select(l => this._storagePropertyNames[l.DataModelPropertyName]).ToList();

        // Assign mapper.
<<<<<<< HEAD
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
        this._mapper = typeof(TRecord) == typeof(Dictionary<string, object?>)
            ? (new WeaviateDynamicDataModelMapper(this.Name, this._options.HasNamedVectors, this._model, s_jsonSerializerOptions) as IWeaviateMapper<TRecord>)!
            : new WeaviateVectorStoreRecordMapper<TRecord>(this.Name, this._options.HasNamedVectors, this._model, s_jsonSerializerOptions);

        this._collectionMetadata = new()
        {
            VectorStoreSystemName = WeaviateConstants.VectorStoreSystemName,
            CollectionName = name
        };
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <inheritdoc />
    public Task<bool> CollectionExistsAsync(CancellationToken cancellationToken = default)
    {
        const string OperationName = "GetCollectionSchema";

        return this.RunOperationAsync(OperationName, async () =>
        {
            var request = new WeaviateGetCollectionSchemaRequest(this.Name).Build();

            var response = await this
                .ExecuteRequestWithNotFoundHandlingAsync<WeaviateGetCollectionSchemaResponse>(request, cancellationToken)
                .ConfigureAwait(false);

            return response != null;
        });
    }

    /// <inheritdoc />
    public Task CreateCollectionAsync(CancellationToken cancellationToken = default)
    {
        const string OperationName = "CreateCollectionSchema";

        var schema = WeaviateVectorStoreCollectionCreateMapping.MapToSchema(
            this.Name,
            this._options.HasNamedVectors,
            this._model);

        return this.RunOperationAsync(OperationName, () =>
        {
<<<<<<< HEAD
            var schema = WeaviateVectorStoreCollectionCreateMapping.MapToSchema(
                this.CollectionName,
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
                this._dataProperties,
                this._vectorProperties,
                this._storagePropertyNames);
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
                this._dataProperties,
                this._vectorProperties,
                this._storagePropertyNames);
=======
                this._propertyReader.DataProperties,
                this._propertyReader.VectorProperties,
                this._propertyReader.JsonPropertyNamesMap);
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
                this._propertyReader.DataProperties,
                this._propertyReader.VectorProperties,
                this._propertyReader.JsonPropertyNamesMap);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
                this._propertyReader.DataProperties,
                this._propertyReader.VectorProperties,
                this._propertyReader.JsonPropertyNamesMap);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head

=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            var request = new WeaviateCreateCollectionSchemaRequest(schema).Build();

            return this.ExecuteRequestAsync(request, cancellationToken: cancellationToken);
        });
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
    {
        const string OperationName = "DeleteCollectionSchema";

        return this.RunOperationAsync(OperationName, () =>
        {
            var request = new WeaviateDeleteCollectionSchemaRequest(this.Name).Build();

            return this.ExecuteRequestAsync(request, cancellationToken: cancellationToken);
        });
    }

    /// <inheritdoc />
    public Task DeleteAsync(TKey key, CancellationToken cancellationToken = default)
    {
        const string OperationName = "DeleteObject";

        return this.RunOperationAsync(OperationName, () =>
        {
            var guid = key switch
            {
                Guid g => g,
                object o => (Guid)o,
                _ => throw new UnreachableException("Guid key should have been validated during model building")
            };

            var request = new WeaviateDeleteObjectRequest(this.Name, guid).Build();

            return this.ExecuteRequestAsync(request, cancellationToken: cancellationToken);
        });
    }

    /// <inheritdoc />
    public Task DeleteAsync(IEnumerable<TKey> keys, CancellationToken cancellationToken = default)
    {
        const string OperationName = "DeleteObjectBatch";
        const string ContainsAnyOperator = "ContainsAny";

        Verify.NotNull(keys);

        var stringKeys = keys.Select(key => key.ToString()).ToList();

        if (stringKeys.Count == 0)
        {
            return Task.CompletedTask;
        }

        return this.RunOperationAsync(OperationName, () =>
        {
            var match = new WeaviateQueryMatch
            {
                CollectionName = this.Name,
                WhereClause = new WeaviateQueryMatchWhereClause
                {
                    Operator = ContainsAnyOperator,
                    Path = [WeaviateConstants.ReservedKeyPropertyName],
                    Values = stringKeys!
                }
            };

            var request = new WeaviateDeleteObjectBatchRequest(match).Build();

            return this.ExecuteRequestAsync(request, cancellationToken: cancellationToken);
        });
    }

    /// <inheritdoc />
    public Task<TRecord?> GetAsync(TKey key, GetRecordOptions? options = null, CancellationToken cancellationToken = default)
    {
        const string OperationName = "GetCollectionObject";

        var guid = key as Guid? ?? throw new InvalidCastException("Only Guid keys are supported");
        var includeVectors = options?.IncludeVectors is true;
        if (includeVectors && this._model.VectorProperties.Any(p => p.EmbeddingGenerator is not null))
        {
            throw new NotSupportedException(VectorDataStrings.IncludeVectorsNotSupportedWithEmbeddingGeneration);
        }

        return this.RunOperationAsync(OperationName, async () =>
        {
            using var request = new WeaviateGetCollectionObjectRequest(this.Name, guid, includeVectors).Build();

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
            var jsonNode = await this.ExecuteRequestWithNotFoundHandlingAsync<JsonNode>(request, cancellationToken).ConfigureAwait(false);

            if (jsonNode is null)
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
            var jsonNode = await this.ExecuteRequestWithNotFoundHandlingAsync<JsonNode>(request, cancellationToken).ConfigureAwait(false);

            if (jsonNode is null)
=======
            var jsonObject = await this.ExecuteRequestWithNotFoundHandlingAsync<JsonObject>(request, cancellationToken).ConfigureAwait(false);

            if (jsonObject is null)
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
            var jsonObject = await this.ExecuteRequestWithNotFoundHandlingAsync<JsonObject>(request, cancellationToken).ConfigureAwait(false);

            if (jsonObject is null)
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
            var jsonObject = await this.ExecuteRequestWithNotFoundHandlingAsync<JsonObject>(request, cancellationToken).ConfigureAwait(false);

            if (jsonObject is null)
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
            {
                return default;
            }

            return VectorStoreErrorHandler.RunModelConversion(
                WeaviateConstants.VectorStoreSystemName,
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
                () => this._mapper.MapFromStorageToDataModel(jsonNode!, new() { IncludeVectors = includeVectors }));
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
                () => this._mapper.MapFromStorageToDataModel(jsonNode!, new() { IncludeVectors = includeVectors }));
=======
                () => this._mapper.MapFromStorageToDataModel(jsonObject!, new() { IncludeVectors = includeVectors }));
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
                () => this._mapper.MapFromStorageToDataModel(jsonObject!, new() { IncludeVectors = includeVectors }));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
                () => this._mapper.MapFromStorageToDataModel(jsonObject!, new() { IncludeVectors = includeVectors }));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
        });
    }

    /// <inheritdoc />
    public async IAsyncEnumerable<TRecord> GetAsync(
        IEnumerable<TKey> keys,
        GetRecordOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        Verify.NotNull(keys);

        var tasks = keys.Select(key => this.GetAsync(key, options, cancellationToken));

        var records = await Task.WhenAll(tasks).ConfigureAwait(false);

        foreach (var record in records)
        {
            if (record is not null)
            {
                yield return record;
            }
        }
    }

    /// <inheritdoc />
    public async Task<TKey> UpsertAsync(TRecord record, CancellationToken cancellationToken = default)
    {
        var keys = await this.UpsertAsync([record], cancellationToken).ConfigureAwait(false);

        return keys.Single();
    }

    /// <inheritdoc />
    public async Task<IReadOnlyList<TKey>> UpsertAsync(IEnumerable<TRecord> records, CancellationToken cancellationToken = default)
    {
        const string OperationName = "UpsertCollectionObject";

        Verify.NotNull(records);

        IReadOnlyList<TRecord>? recordsList = null;

        // If an embedding generator is defined, invoke it once per property for all records.
        IReadOnlyList<Embedding>?[]? generatedEmbeddings = null;

        var vectorPropertyCount = this._model.VectorProperties.Count;
        for (var i = 0; i < vectorPropertyCount; i++)
        {
            var vectorProperty = this._model.VectorProperties[i];

            if (vectorProperty.EmbeddingGenerator is null)
            {
                continue;
            }

            // We have a property with embedding generation; materialize the records' enumerable if needed, to
            // prevent multiple enumeration.
            if (recordsList is null)
            {
                recordsList = records is IReadOnlyList<TRecord> r ? r : records.ToList();

                if (recordsList.Count == 0)
                {
                    return [];
                }

                records = recordsList;
            }

            // TODO: Ideally we'd group together vector properties using the same generator (and with the same input and output properties),
            // and generate embeddings for them in a single batch. That's some more complexity though.
            if (vectorProperty.TryGenerateEmbeddings<TRecord, Embedding<float>, ReadOnlyMemory<float>>(records, cancellationToken, out var floatTask))
            {
                generatedEmbeddings ??= new IReadOnlyList<Embedding>?[vectorPropertyCount];
                generatedEmbeddings[i] = (IReadOnlyList<Embedding<float>>)await floatTask.ConfigureAwait(false);
            }
            else if (vectorProperty.TryGenerateEmbeddings<TRecord, Embedding<double>, ReadOnlyMemory<float>>(records, cancellationToken, out var doubleTask))
            {
                generatedEmbeddings ??= new IReadOnlyList<Embedding>?[vectorPropertyCount];
                generatedEmbeddings[i] = await doubleTask.ConfigureAwait(false);
            }
            else
            {
                throw new InvalidOperationException(
                    $"The embedding generator configured on property '{vectorProperty.ModelName}' cannot produce an embedding of type '{typeof(Embedding<float>).Name}' for the given input type.");
            }
        }

        var jsonObjects = records.Select((record, i) => VectorStoreErrorHandler.RunModelConversion(
            WeaviateConstants.VectorStoreSystemName,
            this._collectionMetadata.VectorStoreName,
            this.Name,
            OperationName,
            () => this._mapper.MapFromDataToStorageModel(record, i, generatedEmbeddings))).ToList();

        if (jsonObjects.Count == 0)
        {
            return [];
        }

        var responses = await this.RunOperationAsync(OperationName, async () =>
        {
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
            var jsonNodes = records.Select(record => VectorStoreErrorHandler.RunModelConversion(
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
            var jsonNodes = records.Select(record => VectorStoreErrorHandler.RunModelConversion(
=======
            var jsonObjects = records.Select(record => VectorStoreErrorHandler.RunModelConversion(
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
            var jsonObjects = records.Select(record => VectorStoreErrorHandler.RunModelConversion(
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
            var jsonObjects = records.Select(record => VectorStoreErrorHandler.RunModelConversion(
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
                DatabaseName,
                this.CollectionName,
                OperationName,
                () => this._mapper.MapFromDataToStorageModel(record))).ToList();

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
            var request = new WeaviateUpsertCollectionObjectBatchRequest(jsonNodes).Build();
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
            var request = new WeaviateUpsertCollectionObjectBatchRequest(jsonNodes).Build();
=======
=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            var request = new WeaviateUpsertCollectionObjectBatchRequest(jsonObjects).Build();
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
            var request = new WeaviateUpsertCollectionObjectBatchRequest(jsonObjects).Build();
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
            var request = new WeaviateUpsertCollectionObjectBatchRequest(jsonObjects).Build();
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head

            return await this.ExecuteRequestAsync<List<WeaviateUpsertCollectionObjectBatchResponse>>(request, cancellationToken).ConfigureAwait(false);
        }).ConfigureAwait(false);

        var keys = new List<TKey>(jsonObjects.Count);

        if (responses is not null)
        {
            foreach (var response in responses)
            {
                if (response?.Result?.IsSuccess is true)
                {
                    keys.Add((TKey)(object)response.Id);
                }
            }
        }

        return keys;
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
                    WeaviateModelBuilder.s_supportedVectorTypes.Contains(typeof(TInput))
                        ? string.Format(VectorDataStrings.EmbeddingTypePassedToSearchAsync)
                        : string.Format(VectorDataStrings.IncompatibleEmbeddingGeneratorWasConfiguredForInputType, typeof(TInput).Name, vectorProperty.EmbeddingGenerator.GetType().Name));
        }
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
    /// <inheritdoc />
    public async IAsyncEnumerable<VectorSearchResult<TRecord>> VectorizedSearchAsync<TVector>(
        TVector vector,
        VectorSearchOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
=======
    /// <inheritdoc />
    public IAsyncEnumerable<VectorSearchResult<TRecord>> SearchEmbeddingAsync<TVector>(
        TVector vector,
        int top,
        VectorSearchOptions<TRecord>? options = null,
        CancellationToken cancellationToken = default)
<<<<<<< HEAD
>>>>>>> upstream/main
=======
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
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        const string OperationName = "VectorSearch";

        VerifyVectorParam(vector);
        Verify.NotLessThan(top, 1);

        if (options.IncludeVectors && this._model.VectorProperties.Any(p => p.EmbeddingGenerator is not null))
        {
            throw new NotSupportedException(VectorDataStrings.IncludeVectorsNotSupportedWithEmbeddingGeneration);
        }

        var query = WeaviateVectorStoreRecordCollectionQueryBuilder.BuildSearchQuery(
            vector,
            this.Name,
            vectorProperty.StorageName,
            s_jsonSerializerOptions,
            top,
            options,
            this._model,
            this._options.HasNamedVectors);

        return this.ExecuteQueryAsync(query, options.IncludeVectors, WeaviateConstants.ScorePropertyName, OperationName, cancellationToken);
    }

    /// <inheritdoc />
    [Obsolete("Use either SearchEmbeddingAsync to search directly on embeddings, or SearchAsync to handle embedding generation internally as part of the call.")]
    public IAsyncEnumerable<VectorSearchResult<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, int top, VectorSearchOptions<TRecord>? options = null, CancellationToken cancellationToken = default)
        where TVector : notnull
        => this.SearchEmbeddingAsync(vector, top, options, cancellationToken);

    #endregion Search

    /// <inheritdoc />
    public IAsyncEnumerable<TRecord> GetAsync(Expression<Func<TRecord, bool>> filter, int top,
        GetFilteredRecordOptions<TRecord>? options = null, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(filter);
        Verify.NotLessThan(top, 1);

        options ??= new();

        var query = WeaviateVectorStoreRecordCollectionQueryBuilder.BuildQuery(
            filter,
            top,
            options,
            this.Name,
            this._model,
            this._options.HasNamedVectors);

        return this.ExecuteQueryAsync(query, options.IncludeVectors, WeaviateConstants.ScorePropertyName, "GetAsync", cancellationToken)
            .SelectAsync(result => result.Record, cancellationToken: cancellationToken);
    }

    /// <inheritdoc />
    public IAsyncEnumerable<VectorSearchResult<TRecord>> HybridSearchAsync<TVector>(TVector vector, ICollection<string> keywords, int top, HybridSearchOptions<TRecord>? options = null, CancellationToken cancellationToken = default)
    {
        const string OperationName = "HybridSearch";

        VerifyVectorParam(vector);
        Verify.NotLessThan(top, 1);

        options ??= s_defaultKeywordVectorizedHybridSearchOptions;
        var vectorProperty = this._model.GetVectorPropertyOrSingle<TRecord>(new() { VectorProperty = options.VectorProperty });
        var textDataProperty = this._model.GetFullTextDataPropertyOrSingle(options.AdditionalProperty);

        var query = WeaviateVectorStoreRecordCollectionQueryBuilder.BuildHybridSearchQuery(
            vector,
            top,
            string.Join(" ", keywords),
            this.Name,
            this._model,
            vectorProperty,
            textDataProperty,
            s_jsonSerializerOptions,
            options,
            this._options.HasNamedVectors);

        return this.ExecuteQueryAsync(query, options.IncludeVectors, WeaviateConstants.HybridScorePropertyName, OperationName, cancellationToken);
    }

    /// <inheritdoc />
    public object? GetService(Type serviceType, object? serviceKey = null)
    {
        Verify.NotNull(serviceType);

        return
            serviceKey is not null ? null :
            serviceType == typeof(VectorStoreRecordCollectionMetadata) ? this._collectionMetadata :
            serviceType == typeof(HttpClient) ? this._httpClient :
            serviceType.IsInstanceOfType(this) ? this :
            null;
    }

    #region private

    private async IAsyncEnumerable<VectorSearchResult<TRecord>> ExecuteQueryAsync(string query, bool includeVectors, string scorePropertyName, string operationName, [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        using var request = new WeaviateVectorSearchRequest(query).Build();

        var (responseModel, content) = await this.ExecuteRequestWithResponseContentAsync<WeaviateVectorSearchResponse>(request, cancellationToken).ConfigureAwait(false);

        var collectionResults = responseModel?.Data?.GetOperation?[this.Name];

        if (collectionResults is null)
        {
            throw new VectorStoreOperationException($"Error occurred during vector search. Response: {content}")
            {
                VectorStoreSystemName = WeaviateConstants.VectorStoreSystemName,
                VectorStoreName = this._collectionMetadata.VectorStoreName,
                CollectionName = this.Name,
                OperationName = operationName
            };
        }

<<<<<<< HEAD
<<<<<<< main
        foreach (var result in collectionResults)
        {
            if (result is not null)
            {
                var (storageModel, score) = WeaviateVectorStoreCollectionSearchMapping.MapSearchResult(result);

                var record = VectorStoreErrorHandler.RunModelConversion(
                    DatabaseName,
                    this.CollectionName,
                    OperationName,
                    () => this._mapper.MapFromStorageToDataModel(storageModel, new() { IncludeVectors = searchOptions.IncludeVectors }));

                yield return new VectorSearchResult<TRecord>(record, score);
            }
        }
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
<<<<<<< main
=======
        var mappedResults = collectionResults.Where(x => x is not null).Select(result =>
=======
        foreach (var result in collectionResults)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        {
            if (result is not null)
            {
                var (storageModel, score) = WeaviateVectorStoreCollectionSearchMapping.MapSearchResult(result, scorePropertyName, this._options.HasNamedVectors);

                var record = VectorStoreErrorHandler.RunModelConversion(
                    WeaviateConstants.VectorStoreSystemName,
                    this._collectionMetadata.VectorStoreName,
                    this.Name,
                    operationName,
                    () => this._mapper.MapFromStorageToDataModel(storageModel, new() { IncludeVectors = includeVectors }));

                yield return new VectorSearchResult<TRecord>(record, score);
            }
        }
    }

<<<<<<< HEAD
>>>>>>> upstream/main
=======
>>>>>>> head
>>>>>>> div
    #region private

    private Task<HttpResponseMessage> ExecuteRequestAsync(HttpRequestMessage request, CancellationToken cancellationToken)
=======
    private async Task<HttpResponseMessage> ExecuteRequestAsync(
        HttpRequestMessage request,
        bool ensureSuccessStatusCode = true,
        CancellationToken cancellationToken = default)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        request.RequestUri = new Uri(this._endpoint, request.RequestUri!);

        if (!string.IsNullOrWhiteSpace(this._apiKey))
        {
            request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", this._apiKey);
        }

        var response = await this._httpClient
            .SendAsync(request, HttpCompletionOption.ResponseContentRead, cancellationToken)
            .ConfigureAwait(false);

        if (ensureSuccessStatusCode)
        {
            response.EnsureSuccessStatusCode();
        }

        return response;
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
    private async Task<TResponse?> ExecuteRequestAsync<TResponse>(HttpRequestMessage request, CancellationToken cancellationToken)
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
    private async Task<TResponse?> ExecuteRequestAsync<TResponse>(HttpRequestMessage request, CancellationToken cancellationToken)
=======
    private async Task<(TResponse?, string)> ExecuteRequestWithResponseContentAsync<TResponse>(HttpRequestMessage request, CancellationToken cancellationToken)
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
    private async Task<(TResponse?, string)> ExecuteRequestWithResponseContentAsync<TResponse>(HttpRequestMessage request, CancellationToken cancellationToken)
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
=======
    private async Task<(TResponse?, string)> ExecuteRequestWithResponseContentAsync<TResponse>(HttpRequestMessage request, CancellationToken cancellationToken)
>>>>>>> upstream/main
=======
<<<<<<< div
=======
    private async Task<(TResponse?, string)> ExecuteRequestWithResponseContentAsync<TResponse>(HttpRequestMessage request, CancellationToken cancellationToken)
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
>>>>>>> div
    {
        var response = await this.ExecuteRequestAsync(request, cancellationToken: cancellationToken).ConfigureAwait(false);
        response.EnsureSuccessStatusCode();

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
        return JsonSerializer.Deserialize<TResponse>(responseContent, s_jsonSerializerOptions);
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
        return JsonSerializer.Deserialize<TResponse>(responseContent, s_jsonSerializerOptions);
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
        return JsonSerializer.Deserialize<TResponse>(responseContent, s_jsonSerializerOptions);
=======
>>>>>>> Stashed changes
=======
        return JsonSerializer.Deserialize<TResponse>(responseContent, s_jsonSerializerOptions);
=======
>>>>>>> Stashed changes
<<<<<<< main
=======
>>>>>>> upstream/main
=======
>>>>>>> head
>>>>>>> div
=======
        var responseContent = await response.Content.ReadAsStringAsync(cancellationToken).ConfigureAwait(false);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        var responseModel = JsonSerializer.Deserialize<TResponse>(responseContent, s_jsonSerializerOptions);

        return (responseModel, responseContent);
    }

    private async Task<TResponse?> ExecuteRequestAsync<TResponse>(HttpRequestMessage request, CancellationToken cancellationToken)
    {
        var (model, _) = await this.ExecuteRequestWithResponseContentAsync<TResponse>(request, cancellationToken).ConfigureAwait(false);

        return model;
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
    }

    private async Task<TResponse?> ExecuteRequestWithNotFoundHandlingAsync<TResponse>(HttpRequestMessage request, CancellationToken cancellationToken)
    {
        var response = await this.ExecuteRequestAsync(request, ensureSuccessStatusCode: false, cancellationToken: cancellationToken).ConfigureAwait(false);

        if (response.StatusCode == HttpStatusCode.NotFound)
        {
            return default;
        }

        response.EnsureSuccessStatusCode();

        var responseContent = await response.Content.ReadAsStringAsync(cancellationToken).ConfigureAwait(false);
        var responseModel = JsonSerializer.Deserialize<TResponse>(responseContent, s_jsonSerializerOptions);

        return responseModel;
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
                VectorStoreSystemName = WeaviateConstants.VectorStoreSystemName,
                VectorStoreName = this._collectionMetadata.VectorStoreName,
                CollectionName = this.Name,
                OperationName = operationName
            };
        }
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
    private static void VerifyVectorParam<TVector>(TVector vector)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        Verify.NotNull(vector);

        var vectorType = vector.GetType();

        if (!WeaviateModelBuilder.s_supportedVectorTypes.Contains(vectorType))
        {
            throw new NotSupportedException(
                $"The provided vector type {vectorType.FullName} is not supported by the Weaviate connector. " +
                $"Supported types are: {string.Join(", ", WeaviateModelBuilder.s_supportedVectorTypes.Select(l => l.FullName))}");
        }
    }

    private static void VerifyCollectionName(string collectionName)
    {
        Verify.NotNullOrWhiteSpace(collectionName);

        // Based on https://weaviate.io/developers/weaviate/starter-guides/managing-collections#collection--property-names
        char first = collectionName[0];
        if (!(first is >= 'A' and <= 'Z'))
        {
            throw new ArgumentException("Collection name must start with an uppercase ASCII letter.", nameof(collectionName));
        }

        foreach (char character in collectionName)
        {
            if (!((character is >= 'a' and <= 'z') || (character is >= 'A' and <= 'Z') || (character is >= '0' and <= '9')))
            {
                throw new ArgumentException("Collection name must contain only ASCII letters and digits.", nameof(collectionName));
            }
        }
    }
<<<<<<< HEAD

    /// <summary>
    /// Returns custom mapper, generic data model mapper or default record mapper.
    /// </summary>
    private IVectorStoreRecordMapper<TRecord, JsonObject> InitializeMapper()
    {
        if (this._options.JsonObjectCustomMapper is not null)
        {
            return this._options.JsonObjectCustomMapper;
        }

        if (typeof(TRecord) == typeof(VectorStoreGenericDataModel<Guid>))
        {
            var mapper = new WeaviateGenericDataModelMapper(
                this.CollectionName,
                this._propertyReader.KeyProperty,
                this._propertyReader.DataProperties,
                this._propertyReader.VectorProperties,
                this._propertyReader.JsonPropertyNamesMap,
                s_jsonSerializerOptions);

            return (mapper as IVectorStoreRecordMapper<TRecord, JsonObject>)!;
        }

        return new WeaviateVectorStoreRecordMapper<TRecord>(
            this.CollectionName,
            this._propertyReader.KeyProperty,
            this._propertyReader.DataProperties,
            this._propertyReader.VectorProperties,
            this._propertyReader.JsonPropertyNamesMap,
            s_jsonSerializerOptions);
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
=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    #endregion
}
