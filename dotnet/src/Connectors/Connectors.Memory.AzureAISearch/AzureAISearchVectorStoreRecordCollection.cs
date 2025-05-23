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
using System.Runtime.CompilerServices;
using System.Text.Json.Nodes;
using System.Threading;
using System.Threading.Tasks;
using Azure;
using Azure.Search.Documents;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.Models;
using Microsoft.Extensions.VectorData;
using Microsoft.Extensions.VectorData.ConnectorSupport;

namespace Microsoft.SemanticKernel.Connectors.AzureAISearch;

/// <summary>
/// Service for storing and retrieving vector records, that uses Azure AI Search as the underlying storage.
/// </summary>
/// <typeparam name="TKey">The data type of the record key. Can be either <see cref="string"/>, or <see cref="object"/> for dynamic mapping.</typeparam>
/// <typeparam name="TRecord">The data model to use for adding, updating and retrieving data from storage.</typeparam>
#pragma warning disable CA1711 // Identifiers should not have incorrect suffix
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
public sealed class AzureAISearchVectorStoreRecordCollection<TRecord> : IVectorStoreRecordCollection<string, TRecord>, IVectorizableTextSearch<TRecord>
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
public sealed class AzureAISearchVectorStoreRecordCollection<TRecord> : IVectorStoreRecordCollection<string, TRecord>, IVectorizableTextSearch<TRecord>
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
public sealed class AzureAISearchVectorStoreRecordCollection<TRecord> : IVectorStoreRecordCollection<string, TRecord>, IVectorizableTextSearch<TRecord>
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
public sealed class AzureAISearchVectorStoreRecordCollection<TRecord> : IVectorStoreRecordCollection<string, TRecord>, IVectorizableTextSearch<TRecord>
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
public sealed class AzureAISearchVectorStoreRecordCollection<TRecord> : IVectorStoreRecordCollection<string, TRecord>
=======
public sealed class AzureAISearchVectorStoreRecordCollection<TRecord> : IVectorStoreRecordCollection<string, TRecord>, IVectorizableTextSearch<TRecord>
>>>>>>> upstream/main
=======
#pragma warning disable CS0618 // IVectorizableTextSearch is obsolete
public sealed class AzureAISearchVectorStoreRecordCollection<TKey, TRecord> :
    IVectorStoreRecordCollection<TKey, TRecord>,
    IVectorizableTextSearch<TRecord>,
    IKeywordHybridSearch<TRecord>
    where TKey : notnull
    where TRecord : notnull
#pragma warning restore CS0618 // IVectorizableTextSearch is obsolete
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
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
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
    /// <summary>The default options for vector search.</summary>
    private static readonly Data.VectorSearchOptions s_defaultVectorSearchOptions = new();

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
    /// <summary>The default options for vector search.</summary>
    private static readonly Data.VectorSearchOptions s_defaultVectorSearchOptions = new();

>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
=======
    /// <summary>The default options for vector search.</summary>
    private static readonly VectorSearchOptions<TRecord> s_defaultVectorSearchOptions = new();

    /// <summary>The default options for hybrid vector search.</summary>
    private static readonly HybridSearchOptions<TRecord> s_defaultKeywordVectorizedHybridSearchOptions = new();

>>>>>>> upstream/main
=======
>>>>>>> head
>>>>>>> div
    /// <summary>Azure AI Search client that can be used to manage the list of indices in an Azure AI Search Service.</summary>
    private readonly SearchIndexClient _searchIndexClient;

    /// <summary>Azure AI Search client that can be used to manage data in an Azure AI Search Service index.</summary>
    private readonly SearchClient _searchClient;

    /// <summary>The name of the collection that this <see cref="AzureAISearchVectorStoreRecordCollection{TKey, TRecord}"/> will access.</summary>
    private readonly string _collectionName;

    /// <summary>Optional configuration options for this class.</summary>
    private readonly AzureAISearchVectorStoreRecordCollectionOptions<TRecord> _options;

    /// <summary>A mapper to use for converting between the data model and the Azure AI Search record.</summary>
    private readonly AzureAISearchDynamicDataModelMapper? _dynamicMapper;

<<<<<<< HEAD
    /// <summary>A definition of the current storage model.</summary>
    private readonly VectorStoreRecordDefinition _vectorStoreRecordDefinition;

    /// <summary>The storage name of the key field for the collections that this class is used with.</summary>
    private readonly string _keyStoragePropertyName;

    /// <summary>The storage names of all non vector fields on the current model.</summary>
    private readonly List<string> _nonVectorStoragePropertyNames = new();

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
    /// <summary>A dictionary that maps from a property name to the storage name that should be used when serializing it to json for data and vector properties.</summary>
    private readonly Dictionary<string, string> _storagePropertyNames = new();
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
    /// <summary>A dictionary that maps from a property name to the storage name that should be used when serializing it to json for data and vector properties.</summary>
    private readonly Dictionary<string, string> _storagePropertyNames = new();
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
    /// <summary>A dictionary that maps from a property name to the storage name that should be used when serializing it to json for data and vector properties.</summary>
    private readonly Dictionary<string, string> _storagePropertyNames = new();
=======
>>>>>>> Stashed changes
=======
    /// <summary>A dictionary that maps from a property name to the storage name that should be used when serializing it to json for data and vector properties.</summary>
    private readonly Dictionary<string, string> _storagePropertyNames = new();
=======
>>>>>>> Stashed changes
>>>>>>> head
    /// <summary>The name of the first vector field for the collections that this class is used with.</summary>
    private readonly string? _firstVectorPropertyName = null;

    /// <summary>The name of the first string data field for the collections that this class is used with.</summary>
    private readonly string? _firstStringDataPropertyName = null;

    /// <summary>A dictionary that maps from a property name to the storage name that should be used when serializing it to json for data and vector properties.</summary>
    private readonly Dictionary<string, string> _storagePropertyNames = new();
    /// <summary>A helper to access property information for the current data model and record definition.</summary>
    private readonly VectorStoreRecordPropertyReader _propertyReader;
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
    /// <summary>The model for this collection.</summary>
    private readonly VectorStoreRecordModel _model;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

    /// <summary>
    /// Initializes a new instance of the <see cref="AzureAISearchVectorStoreRecordCollection{TKey, TRecord}"/> class.
    /// </summary>
    /// <param name="searchIndexClient">Azure AI Search client that can be used to manage the list of indices in an Azure AI Search Service.</param>
    /// <param name="name">The name of the collection that this <see cref="AzureAISearchVectorStoreRecordCollection{TKey, TRecord}"/> will access.</param>
    /// <param name="options">Optional configuration options for this class.</param>
    /// <exception cref="ArgumentNullException">Thrown when <paramref name="searchIndexClient"/> is null.</exception>
    /// <exception cref="ArgumentException">Thrown when options are misconfigured.</exception>
    public AzureAISearchVectorStoreRecordCollection(SearchIndexClient searchIndexClient, string name, AzureAISearchVectorStoreRecordCollectionOptions<TRecord>? options = default)
    {
        // Verify.
        Verify.NotNull(searchIndexClient);
<<<<<<< HEAD
        Verify.NotNullOrWhiteSpace(collectionName);
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
        Verify.True(
            !(typeof(TRecord).IsGenericType &&
                typeof(TRecord).GetGenericTypeDefinition() == typeof(VectorStoreGenericDataModel<>) &&
                typeof(TRecord).GetGenericArguments()[0] != typeof(string) &&
                options?.JsonObjectCustomMapper is null),
            "A data model of VectorStoreGenericDataModel with a different key type than string, is not supported by the default mappers. Please provide your own mapper to map to your chosen key type.");
        Verify.True(
            !(typeof(TRecord) == typeof(VectorStoreGenericDataModel<string>) && options?.VectorStoreRecordDefinition is null),
            $"A {nameof(VectorStoreRecordDefinition)} must be provided when using {nameof(VectorStoreGenericDataModel<string>)}.");
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
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
        VectorStoreRecordPropertyVerification.VerifyGenericDataModelKeyType(typeof(TRecord), options?.JsonObjectCustomMapper is not null, s_supportedKeyTypes);
        VectorStoreRecordPropertyVerification.VerifyGenericDataModelDefinitionSupplied(typeof(TRecord), options?.VectorStoreRecordDefinition is not null);
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
        VectorStoreRecordPropertyVerification.VerifyGenericDataModelKeyType(typeof(TRecord), options?.JsonObjectCustomMapper is not null, s_supportedKeyTypes);
        VectorStoreRecordPropertyVerification.VerifyGenericDataModelDefinitionSupplied(typeof(TRecord), options?.VectorStoreRecordDefinition is not null);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
        VectorStoreRecordPropertyVerification.VerifyGenericDataModelKeyType(typeof(TRecord), options?.JsonObjectCustomMapper is not null, s_supportedKeyTypes);
        VectorStoreRecordPropertyVerification.VerifyGenericDataModelDefinitionSupplied(typeof(TRecord), options?.VectorStoreRecordDefinition is not null);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
=======
        Verify.NotNullOrWhiteSpace(name);

        if (typeof(TKey) != typeof(string) && typeof(TKey) != typeof(object))
        {
            throw new NotSupportedException("Only string keys are supported (and object for dynamic mapping)");
        }
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Assign.
        this._searchIndexClient = searchIndexClient;
        this._collectionName = name;
        this._options = options ?? new AzureAISearchVectorStoreRecordCollectionOptions<TRecord>();
<<<<<<< HEAD
        this._searchClient = this._searchIndexClient.GetSearchClient(collectionName);
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
        var jsonSerializerOptions = this._options.JsonSerializerOptions ?? JsonSerializerOptions.Default;

        // Validate property types.
        var properties = VectorStoreRecordPropertyReader.SplitDefinitionAndVerify(typeof(TRecord).Name, this._vectorStoreRecordDefinition, supportsMultipleVectors: true, requiresAtLeastOneVector: false);
        VectorStoreRecordPropertyReader.VerifyPropertyTypes([properties.KeyProperty], s_supportedKeyTypes, "Key");
        VectorStoreRecordPropertyReader.VerifyPropertyTypes(properties.DataProperties, s_supportedDataTypes, "Data", supportEnumerable: true);
        VectorStoreRecordPropertyReader.VerifyPropertyTypes(properties.VectorProperties, s_supportedVectorTypes, "Vector");

        // Get storage names and store for later use.
        this._storagePropertyNames = VectorStoreRecordPropertyReader.BuildPropertyNameToJsonPropertyNameMap(properties, typeof(TRecord), jsonSerializerOptions);
        this._keyStoragePropertyName = this._storagePropertyNames[properties.KeyProperty.DataModelPropertyName];
        this._nonVectorStoragePropertyNames = properties.DataProperties
            .Cast<VectorStoreRecordProperty>()
            .Concat([properties.KeyProperty])
            .Select(x => this._storagePropertyNames[x.DataModelPropertyName])
            .ToList();
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
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< Updated upstream
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
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        this._propertyReader = new VectorStoreRecordPropertyReader(
            typeof(TRecord),
            this._options.VectorStoreRecordDefinition,
            new()
            {
                RequiresAtLeastOneVector = false,
                SupportsMultipleKeys = false,
                SupportsMultipleVectors = true,
                JsonSerializerOptions = this._options.JsonSerializerOptions ?? JsonSerializerOptions.Default
            });
=======
        this._searchClient = this._searchIndexClient.GetSearchClient(name);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        this._model = typeof(TRecord) == typeof(Dictionary<string, object?>) ?
            new AzureAISearchDynamicModelBuilder().Build(typeof(TRecord), this._options.VectorStoreRecordDefinition, this._options.EmbeddingGenerator) :
            new AzureAISearchModelBuilder().Build(typeof(TRecord), this._options.VectorStoreRecordDefinition, this._options.EmbeddingGenerator, this._options.JsonSerializerOptions);

        if (properties.VectorProperties.Count > 0)
        {
            this._firstVectorPropertyName = VectorStoreRecordPropertyReader.GetJsonPropertyName(properties.VectorProperties.First(), typeof(TRecord), jsonSerializerOptions);
        }

        var firstStringDataProperty = properties.DataProperties.FirstOrDefault(x => x.PropertyType == typeof(string));
        if (firstStringDataProperty is not null)
        {
            this._firstStringDataPropertyName = VectorStoreRecordPropertyReader.GetJsonPropertyName(firstStringDataProperty, typeof(TRecord), jsonSerializerOptions);
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

        // Resolve mapper.
        // If they didn't provide a custom mapper, and the record type is the generic data model, use the built in mapper for that.
        // Otherwise, don't set the mapper, and we'll default to just using Azure AI Search's built in json serialization and deserialization.
        if (typeof(TRecord) == typeof(Dictionary<string, object?>))
        {
            this._dynamicMapper = new AzureAISearchDynamicDataModelMapper(this._model);
        }

        this._collectionMetadata = new()
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
            this._mapper = new AzureAISearchGenericDataModelMapper(this._vectorStoreRecordDefinition) as IVectorStoreRecordMapper<TRecord, JsonObject>;
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
            this._mapper = new AzureAISearchGenericDataModelMapper(this._vectorStoreRecordDefinition) as IVectorStoreRecordMapper<TRecord, JsonObject>;
=======
            this._mapper = new AzureAISearchGenericDataModelMapper(this._propertyReader.RecordDefinition) as IVectorStoreRecordMapper<TRecord, JsonObject>;
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
            this._mapper = new AzureAISearchGenericDataModelMapper(this._propertyReader.RecordDefinition) as IVectorStoreRecordMapper<TRecord, JsonObject>;
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
            this._mapper = new AzureAISearchGenericDataModelMapper(this._propertyReader.RecordDefinition) as IVectorStoreRecordMapper<TRecord, JsonObject>;
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
        }
=======
            VectorStoreSystemName = AzureAISearchConstants.VectorStoreSystemName,
            VectorStoreName = searchIndexClient.ServiceName,
            CollectionName = name
        };
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <inheritdoc />
    public string Name => this._collectionName;

    /// <inheritdoc />
    public async Task<bool> CollectionExistsAsync(CancellationToken cancellationToken = default)
    {
        try
        {
            await this._searchIndexClient.GetIndexAsync(this._collectionName, cancellationToken).ConfigureAwait(false);
            return true;
        }
        catch (RequestFailedException ex) when (ex.Status == 404)
        {
            return false;
        }
        catch (RequestFailedException ex)
        {
            throw new VectorStoreOperationException("Call to vector store failed.", ex)
            {
                VectorStoreSystemName = AzureAISearchConstants.VectorStoreSystemName,
                VectorStoreName = this._collectionMetadata.VectorStoreName,
                CollectionName = this._collectionName,
                OperationName = "GetIndex"
            };
        }
    }

    /// <inheritdoc />
    public Task CreateCollectionAsync(CancellationToken cancellationToken = default)
    {
        var vectorSearchConfig = new VectorSearch();
        var searchFields = new List<SearchField>();

        // Loop through all properties and create the search fields.
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
        foreach (var property in this._vectorStoreRecordDefinition.Properties)
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
        foreach (var property in this._vectorStoreRecordDefinition.Properties)
=======
        foreach (var property in this._propertyReader.Properties)
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
        foreach (var property in this._propertyReader.Properties)
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
        foreach (var property in this._model.Properties)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        {
            switch (property)
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
                searchFields.Add(AzureAISearchVectorStoreCollectionCreateMapping.MapKeyField(keyProperty, this._keyStoragePropertyName));
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
                searchFields.Add(AzureAISearchVectorStoreCollectionCreateMapping.MapKeyField(keyProperty, this._keyStoragePropertyName));
=======
                searchFields.Add(AzureAISearchVectorStoreCollectionCreateMapping.MapKeyField(
                    keyProperty,
                    this._propertyReader.KeyPropertyJsonName));
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
                searchFields.Add(AzureAISearchVectorStoreCollectionCreateMapping.MapKeyField(
                    keyProperty,
                    this._propertyReader.KeyPropertyJsonName));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
            }

            // Data property.
            if (property is VectorStoreRecordDataProperty dataProperty)
            {
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
                searchFields.Add(AzureAISearchVectorStoreCollectionCreateMapping.MapDataField(dataProperty, this._storagePropertyNames[dataProperty.DataModelPropertyName]));
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
                searchFields.Add(AzureAISearchVectorStoreCollectionCreateMapping.MapDataField(dataProperty, this._storagePropertyNames[dataProperty.DataModelPropertyName]));
=======
                searchFields.Add(AzureAISearchVectorStoreCollectionCreateMapping.MapDataField(
                    dataProperty,
                    this._propertyReader.GetJsonPropertyName(dataProperty.DataModelPropertyName)));
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
                searchFields.Add(AzureAISearchVectorStoreCollectionCreateMapping.MapDataField(
                    dataProperty,
                    this._propertyReader.GetJsonPropertyName(dataProperty.DataModelPropertyName)));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
                searchFields.Add(AzureAISearchVectorStoreCollectionCreateMapping.MapDataField(
                    dataProperty,
                    this._propertyReader.GetJsonPropertyName(dataProperty.DataModelPropertyName)));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
            }

            // Vector property.
            if (property is VectorStoreRecordVectorProperty vectorProperty)
            {
                (VectorSearchField vectorSearchField, VectorSearchAlgorithmConfiguration algorithmConfiguration, VectorSearchProfile vectorSearchProfile) = AzureAISearchVectorStoreCollectionCreateMapping.MapVectorField(
                    vectorProperty,
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
                    this._storagePropertyNames[vectorProperty.DataModelPropertyName]);
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
                    this._storagePropertyNames[vectorProperty.DataModelPropertyName]);
=======
                    this._propertyReader.GetJsonPropertyName(vectorProperty.DataModelPropertyName));
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
                    this._propertyReader.GetJsonPropertyName(vectorProperty.DataModelPropertyName));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
                    this._propertyReader.GetJsonPropertyName(vectorProperty.DataModelPropertyName));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
=======
                case VectorStoreRecordKeyPropertyModel p:
                    searchFields.Add(AzureAISearchVectorStoreCollectionCreateMapping.MapKeyField(p));
                    break;

                case VectorStoreRecordDataPropertyModel p:
                    searchFields.Add(AzureAISearchVectorStoreCollectionCreateMapping.MapDataField(p));
                    break;

                case VectorStoreRecordVectorPropertyModel p:
                    (VectorSearchField vectorSearchField, VectorSearchAlgorithmConfiguration algorithmConfiguration, VectorSearchProfile vectorSearchProfile) = AzureAISearchVectorStoreCollectionCreateMapping.MapVectorField(p);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

                    // Add the search field, plus its profile and algorithm configuration to the search config.
                    searchFields.Add(vectorSearchField);
                    vectorSearchConfig.Algorithms.Add(algorithmConfiguration);
                    vectorSearchConfig.Profiles.Add(vectorSearchProfile);
                    break;

                default:
                    throw new UnreachableException();
            }
        }

        // Create the index.
        var searchIndex = new SearchIndex(this._collectionName, searchFields);
        searchIndex.VectorSearch = vectorSearchConfig;

        return this.RunOperationAsync(
            "CreateIndex",
            () => this._searchIndexClient.CreateIndexAsync(searchIndex, cancellationToken));
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
        return this.RunOperationAsync<Response>(
            "DeleteIndex",
            async () =>
            {
                try
                {
                    return await this._searchIndexClient.DeleteIndexAsync(this._collectionName, cancellationToken).ConfigureAwait(false);
                }
                catch (RequestFailedException ex) when (ex.Status == 404)
                {
                    return null!;
                }
            });
    }

    /// <inheritdoc />
    public Task<TRecord?> GetAsync(TKey key, GetRecordOptions? options = default, CancellationToken cancellationToken = default)
    {
        // Create Options.
        var innerOptions = this.ConvertGetDocumentOptions(options);
        var includeVectors = options?.IncludeVectors ?? false;

        // Get record.
        return this.GetDocumentAndMapToDataModelAsync(key, includeVectors, innerOptions, cancellationToken);
    }

    /// <inheritdoc />
    public async IAsyncEnumerable<TRecord> GetAsync(IEnumerable<TKey> keys, GetRecordOptions? options = default, [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        Verify.NotNull(keys);

        // Create Options
        var innerOptions = this.ConvertGetDocumentOptions(options);
        var includeVectors = options?.IncludeVectors ?? false;

        // Get records in parallel.
        var tasks = keys.Select(key => this.GetDocumentAndMapToDataModelAsync(key, includeVectors, innerOptions, cancellationToken));
        var results = await Task.WhenAll(tasks).ConfigureAwait(false);
        foreach (var result in results)
        {
            if (result is not null)
            {
                yield return result;
            }
        }
    }

    /// <inheritdoc />
    public Task DeleteAsync(TKey key, CancellationToken cancellationToken = default)
    {
        var stringKey = this.GetStringKey(key);

        // Remove record.
        return this.RunOperationAsync(
            "DeleteDocuments",
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
            () => this._searchClient.DeleteDocumentsAsync(this._keyStoragePropertyName, [key], new IndexDocumentsOptions(), cancellationToken));
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
            () => this._searchClient.DeleteDocumentsAsync(this._keyStoragePropertyName, [key], new IndexDocumentsOptions(), cancellationToken));
=======
            () => this._searchClient.DeleteDocumentsAsync(this._propertyReader.KeyPropertyJsonName, [key], new IndexDocumentsOptions(), cancellationToken));
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
            () => this._searchClient.DeleteDocumentsAsync(this._propertyReader.KeyPropertyJsonName, [key], new IndexDocumentsOptions(), cancellationToken));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
            () => this._searchClient.DeleteDocumentsAsync(this._propertyReader.KeyPropertyJsonName, [key], new IndexDocumentsOptions(), cancellationToken));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
=======
            () => this._searchClient.DeleteDocumentsAsync(this._model.KeyProperty.StorageName, [stringKey], new IndexDocumentsOptions(), cancellationToken));
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <inheritdoc />
    public Task DeleteAsync(IEnumerable<TKey> keys, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(keys);
        if (!keys.Any())
        {
            return Task.CompletedTask;
        }

        var stringKeys = keys is IEnumerable<string> k ? k : keys.Cast<string>();

        // Remove records.
        return this.RunOperationAsync(
            "DeleteDocuments",
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
            () => this._searchClient.DeleteDocumentsAsync(this._keyStoragePropertyName, keys, new IndexDocumentsOptions(), cancellationToken));
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
            () => this._searchClient.DeleteDocumentsAsync(this._keyStoragePropertyName, keys, new IndexDocumentsOptions(), cancellationToken));
=======
            () => this._searchClient.DeleteDocumentsAsync(this._propertyReader.KeyPropertyJsonName, keys, new IndexDocumentsOptions(), cancellationToken));
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
            () => this._searchClient.DeleteDocumentsAsync(this._propertyReader.KeyPropertyJsonName, keys, new IndexDocumentsOptions(), cancellationToken));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
            () => this._searchClient.DeleteDocumentsAsync(this._model.KeyProperty.StorageName, stringKeys, new IndexDocumentsOptions(), cancellationToken));
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <inheritdoc />
    public async Task<TKey> UpsertAsync(TRecord record, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(record);

        // Create options.
        var innerOptions = new IndexDocumentsOptions { ThrowOnAnyError = true };

        // Upsert record.
        var results = await this.MapToStorageModelAndUploadDocumentAsync([record], innerOptions, cancellationToken).ConfigureAwait(false);

        return (TKey)(object)results.Value.Results[0].Key;
    }

    /// <inheritdoc />
    public async Task<IReadOnlyList<TKey>> UpsertAsync(IEnumerable<TRecord> records, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(records);
        if (!records.Any())
        {
            return [];
        }

        // Create Options
        var innerOptions = new IndexDocumentsOptions { ThrowOnAnyError = true };

        // Upsert records
        var results = await this.MapToStorageModelAndUploadDocumentAsync(records, innerOptions, cancellationToken).ConfigureAwait(false);

        return results.Value.Results.Select(x => (TKey)(object)x.Key).ToList();
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
    public IAsyncEnumerable<VectorSearchResult<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, Data.VectorSearchOptions? options = null, CancellationToken cancellationToken = default)
=======
    /// <inheritdoc />
<<<<<<< HEAD
    public Task<VectorSearchResults<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, VectorData.VectorSearchOptions? options = null, CancellationToken cancellationToken = default)
>>>>>>> upstream/main
=======
    public IAsyncEnumerable<VectorSearchResult<TRecord>> SearchEmbeddingAsync<TVector>(
        TVector vector,
        int top,
        VectorSearchOptions<TRecord>? options = null,
        CancellationToken cancellationToken = default)
        where TVector : notnull
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        options ??= s_defaultVectorSearchOptions;
        var vectorProperty = this._model.GetVectorPropertyOrSingle(options);

        var floatVector = VerifyVectorParam(vector);
        Verify.NotLessThan(top, 1);

        // Configure search settings.
        var vectorQueries = new List<VectorQuery>
        {
            new VectorizedQuery(floatVector) { KNearestNeighborsCount = top, Fields = { vectorProperty.StorageName } }
        };

#pragma warning disable CS0618 // VectorSearchFilter is obsolete
        // Build filter object.
        var filter = options switch
        {
            { OldFilter: not null, Filter: not null } => throw new ArgumentException("Either Filter or OldFilter can be specified, but not both"),
            { OldFilter: VectorSearchFilter legacyFilter } => AzureAISearchVectorStoreCollectionSearchMapping.BuildLegacyFilterString(legacyFilter, this._model),
            { Filter: Expression<Func<TRecord, bool>> newFilter } => new AzureAISearchFilterTranslator().Translate(newFilter, this._model),
            _ => null
        };
#pragma warning restore CS0618

        // Build search options.
        var searchOptions = new SearchOptions
        {
            VectorSearch = new(),
<<<<<<< HEAD
            Size = internalOptions.Top,
            Skip = internalOptions.Skip,
            Filter = filterString,
<<<<<<< main
=======
            IncludeTotalCount = internalOptions.IncludeTotalCount,
>>>>>>> upstream/main
=======
            Size = top,
            Skip = options.Skip,
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        };

        if (filter is not null)
        {
            searchOptions.Filter = filter;
        }

        searchOptions.VectorSearch.Queries.AddRange(vectorQueries);

        // Filter out vector fields if requested.
        if (!options.IncludeVectors)
        {
            searchOptions.Select.Add(this._model.KeyProperty.StorageName);

            foreach (var dataProperty in this._model.DataProperties)
            {
                searchOptions.Select.Add(dataProperty.StorageName);
            }
        }

        return this.SearchAndMapToDataModelAsync(null, searchOptions, options.IncludeVectors, cancellationToken);
    }

    /// <inheritdoc />
<<<<<<< HEAD
<<<<<<< main
    public IAsyncEnumerable<VectorSearchResult<TRecord>> VectorizableTextSearchAsync(string searchText, Data.VectorSearchOptions? options = null, CancellationToken cancellationToken = default)
=======
    public Task<VectorSearchResults<TRecord>> VectorizableTextSearchAsync(string searchText, VectorData.VectorSearchOptions? options = null, CancellationToken cancellationToken = default)
>>>>>>> upstream/main
=======
    [Obsolete("Use either SearchEmbeddingAsync to search directly on embeddings, or SearchAsync to handle embedding generation internally as part of the call.")]
    public IAsyncEnumerable<VectorSearchResult<TRecord>> VectorizedSearchAsync<TVector>(TVector vector, int top, VectorSearchOptions<TRecord>? options = null, CancellationToken cancellationToken = default)
        where TVector : notnull
        => this.SearchEmbeddingAsync(vector, top, options, cancellationToken);

    /// <inheritdoc />
    public IAsyncEnumerable<TRecord> GetAsync(Expression<Func<TRecord, bool>> filter, int top,
        GetFilteredRecordOptions<TRecord>? options = null, CancellationToken cancellationToken = default)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        Verify.NotNull(filter);
        Verify.NotLessThan(top, 1);

        options ??= new();

        SearchOptions searchOptions = new()
        {
            VectorSearch = new(),
            Size = top,
            Skip = options.Skip,
            Filter = new AzureAISearchFilterTranslator().Translate(filter, this._model),
        };

        // Filter out vector fields if requested.
        if (!options.IncludeVectors)
        {
            searchOptions.Select.Add(this._model.KeyProperty.StorageName);

            foreach (var dataProperty in this._model.DataProperties)
            {
                searchOptions.Select.Add(dataProperty.StorageName);
            }
        }

        foreach (var pair in options.OrderBy.Values)
        {
            VectorStoreRecordPropertyModel property = this._model.GetDataOrKeyProperty(pair.PropertySelector);
            string name = property.StorageName;
            // From https://learn.microsoft.com/dotnet/api/azure.search.documents.searchoptions.orderby:
            // "Each expression can be followed by asc to indicate ascending, or desc to indicate descending".
            // "The default is ascending order."
            if (!pair.Ascending)
            {
                name += " desc";
            }

            searchOptions.OrderBy.Add(name);
        }

        return this.SearchAndMapToDataModelAsync(null, searchOptions, options.IncludeVectors, cancellationToken)
            .SelectAsync(result => result.Record, cancellationToken);
    }

    /// <inheritdoc />
    public IAsyncEnumerable<VectorSearchResult<TRecord>> SearchAsync<TInput>(
        TInput value,
        int top,
        VectorSearchOptions<TRecord>? options = default,
        CancellationToken cancellationToken = default)
        where TInput : notnull
    {
        var searchText = value switch
        {
            string s => s,
            null => throw new ArgumentNullException(nameof(value)),
            _ => throw new ArgumentException($"The provided search type '{value?.GetType().Name}' is not supported by the Azure AI Search connector, pass a string.")
        };

        Verify.NotNull(searchText);
        Verify.NotLessThan(top, 1);

        if (this._model.VectorProperties.Count == 0)
        {
            throw new InvalidOperationException("The collection does not have any vector fields, so vector search is not possible.");
        }

        // Resolve options.
        options ??= s_defaultVectorSearchOptions;
        var vectorProperty = this._model.GetVectorPropertyOrSingle(options);

        // Configure search settings.
        var vectorQueries = new List<VectorQuery>
        {
            new VectorizableTextQuery(searchText) { KNearestNeighborsCount = top, Fields = { vectorProperty.StorageName } }
        };

#pragma warning disable CS0618 // VectorSearchFilter is obsolete
        // Build filter object.
        var filter = options switch
        {
            { OldFilter: not null, Filter: not null } => throw new ArgumentException("Either Filter or OldFilter can be specified, but not both"),
            { OldFilter: VectorSearchFilter legacyFilter } => AzureAISearchVectorStoreCollectionSearchMapping.BuildLegacyFilterString(legacyFilter, this._model),
            { Filter: Expression<Func<TRecord, bool>> newFilter } => new AzureAISearchFilterTranslator().Translate(newFilter, this._model),
            _ => null
        };
#pragma warning restore CS0618

        // Build search options.
        var searchOptions = new SearchOptions
        {
            VectorSearch = new(),
<<<<<<< HEAD
            Size = internalOptions.Top,
            Skip = internalOptions.Skip,
            Filter = filterString,
<<<<<<< main
=======
            IncludeTotalCount = internalOptions.IncludeTotalCount,
>>>>>>> upstream/main
=======
            Size = top,
            Skip = options.Skip,
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        };

        if (filter is not null)
        {
            searchOptions.Filter = filter;
        }

        searchOptions.VectorSearch.Queries.AddRange(vectorQueries);

        // Filter out vector fields if requested.
        if (!options.IncludeVectors)
        {
            searchOptions.Select.Add(this._model.KeyProperty.StorageName);

            foreach (var dataProperty in this._model.DataProperties)
            {
                searchOptions.Select.Add(dataProperty.StorageName);
            }
        }

        return this.SearchAndMapToDataModelAsync(null, searchOptions, options.IncludeVectors, cancellationToken);
    }

    /// <inheritdoc />
    [Obsolete("Use SearchAsync")]
    public IAsyncEnumerable<VectorSearchResult<TRecord>> VectorizableTextSearchAsync(string searchText, int top, VectorSearchOptions<TRecord>? options = null, CancellationToken cancellationToken = default)
        => this.SearchAsync(searchText, top, options, cancellationToken);

    /// <inheritdoc />
    public IAsyncEnumerable<VectorSearchResult<TRecord>> HybridSearchAsync<TVector>(TVector vector, ICollection<string> keywords, int top, HybridSearchOptions<TRecord>? options = null, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(keywords);
        var floatVector = VerifyVectorParam(vector);
        Verify.NotLessThan(top, 1);

        // Resolve options.
        options ??= s_defaultKeywordVectorizedHybridSearchOptions;
        var vectorProperty = this._model.GetVectorPropertyOrSingle<TRecord>(new() { VectorProperty = options.VectorProperty });
        var textDataProperty = this._model.GetFullTextDataPropertyOrSingle(options.AdditionalProperty);

        // Configure search settings.
        var vectorQueries = new List<VectorQuery>
        {
            new VectorizedQuery(floatVector) { KNearestNeighborsCount = top, Fields = { vectorProperty.StorageName } }
        };

#pragma warning disable CS0618 // VectorSearchFilter is obsolete
        // Build filter object.
        var filter = options switch
        {
            { OldFilter: not null, Filter: not null } => throw new ArgumentException("Either Filter or OldFilter can be specified, but not both"),
            { OldFilter: VectorSearchFilter legacyFilter } => AzureAISearchVectorStoreCollectionSearchMapping.BuildLegacyFilterString(legacyFilter, this._model),
            { Filter: Expression<Func<TRecord, bool>> newFilter } => new AzureAISearchFilterTranslator().Translate(newFilter, this._model),
            _ => null
        };
#pragma warning restore CS0618

        // Build search options.
        var searchOptions = new SearchOptions
        {
            VectorSearch = new(),
            Size = top,
            Skip = options.Skip,
            Filter = filter,
            IncludeTotalCount = options.IncludeTotalCount,
        };
        searchOptions.VectorSearch.Queries.AddRange(vectorQueries);
        searchOptions.SearchFields.Add(textDataProperty.StorageName);

        // Filter out vector fields if requested.
        if (!options.IncludeVectors)
        {
            searchOptions.Select.Add(this._model.KeyProperty.StorageName);

            foreach (var dataProperty in this._model.DataProperties)
            {
                searchOptions.Select.Add(dataProperty.StorageName);
            }
        }

        var keywordsCombined = string.Join(" ", keywords);

        return this.SearchAndMapToDataModelAsync(keywordsCombined, searchOptions, options.IncludeVectors, cancellationToken);
    }

    /// <inheritdoc />
    public object? GetService(Type serviceType, object? serviceKey = null)
    {
        Verify.NotNull(serviceType);

        return
            serviceKey is not null ? null :
            serviceType == typeof(VectorStoreRecordCollectionMetadata) ? this._collectionMetadata :
            serviceType == typeof(SearchIndexClient) ? this._searchIndexClient :
            serviceType == typeof(SearchClient) ? this._searchClient :
            serviceType.IsInstanceOfType(this) ? this :
            null;
    }

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
    /// <summary>
    /// Get the document with the given key and map it to the data model using the configured mapper type.
    /// </summary>
    /// <param name="key">The key of the record to get.</param>
    /// <param name="includeVectors">A value indicating whether to include vectors in the result or not.</param>
    /// <param name="innerOptions">The Azure AI Search sdk options for getting a document.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>The retrieved document, mapped to the consumer data model.</returns>
    private async Task<TRecord?> GetDocumentAndMapToDataModelAsync(
        TKey key,
        bool includeVectors,
        GetDocumentOptions innerOptions,
        CancellationToken cancellationToken)
    {
        const string OperationName = "GetDocument";

        var stringKey = this.GetStringKey(key);

        // Use the user provided mapper.
<<<<<<< HEAD
        if (this._mapper is not null)
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
        if (this._options.JsonObjectCustomMapper is not null)
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
        if (this._options.JsonObjectCustomMapper is not null)
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
        if (this._options.JsonObjectCustomMapper is not null)
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
        if (this._options.JsonObjectCustomMapper is not null)
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
=======
        if (this._dynamicMapper is not null)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        {
            Debug.Assert(typeof(TRecord) == typeof(Dictionary<string, object?>));

            var jsonObject = await this.RunOperationAsync(
                OperationName,
                () => GetDocumentWithNotFoundHandlingAsync<JsonObject>(this._searchClient, stringKey, innerOptions, cancellationToken)).ConfigureAwait(false);

            if (jsonObject is null)
            {
                return default;
            }

            return VectorStoreErrorHandler.RunModelConversion(
                AzureAISearchConstants.VectorStoreSystemName,
                this._collectionMetadata.VectorStoreName,
                this._collectionName,
                OperationName,
<<<<<<< HEAD
                () => this._mapper!.MapFromStorageToDataModel(jsonObject, new() { IncludeVectors = includeVectors }));
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
                () => this._options.JsonObjectCustomMapper!.MapFromStorageToDataModel(jsonObject, new() { IncludeVectors = includeVectors }));
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
                () => this._options.JsonObjectCustomMapper!.MapFromStorageToDataModel(jsonObject, new() { IncludeVectors = includeVectors }));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
                () => this._options.JsonObjectCustomMapper!.MapFromStorageToDataModel(jsonObject, new() { IncludeVectors = includeVectors }));
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
                () => this._options.JsonObjectCustomMapper!.MapFromStorageToDataModel(jsonObject, new() { IncludeVectors = includeVectors }));
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
=======
                () => (TRecord)(object)this._dynamicMapper!.MapFromStorageToDataModel(jsonObject, new() { IncludeVectors = includeVectors }));
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        }

        // Use the built in Azure AI Search mapper.
        return await this.RunOperationAsync(
            OperationName,
            () => GetDocumentWithNotFoundHandlingAsync<TRecord>(this._searchClient, stringKey, innerOptions, cancellationToken)).ConfigureAwait(false);
    }

    /// <summary>
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
    /// Search for the documents matching the given options and map them to the data model using the configured mapper type.
    /// </summary>
    /// <param name="searchText">Text to use if doing a hybrid search. Null for non-hybrid search.</param>
    /// <param name="searchOptions">The options controlling the behavior of the search operation.</param>
    /// <param name="includeVectors">A value indicating whether to include vectors in the result or not.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
<<<<<<< main
    /// <returns></returns>
    private async IAsyncEnumerable<VectorSearchResult<TRecord>> SearchAndMapToDataModelAsync(
        string? searchText,
        SearchOptions searchOptions,
        bool includeVectors,
        [EnumeratorCancellation] CancellationToken cancellationToken)
=======
    /// <returns>The mapped search results.</returns>
    private async IAsyncEnumerable<VectorSearchResult<TRecord>> SearchAndMapToDataModelAsync(
        string? searchText,
        SearchOptions searchOptions,
        bool includeVectors,
<<<<<<< HEAD
        CancellationToken cancellationToken)
>>>>>>> upstream/main
=======
        [EnumeratorCancellation] CancellationToken cancellationToken)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        const string OperationName = "Search";

        // Execute search and map using the user provided mapper.
        if (this._dynamicMapper is not null)
        {
            Debug.Assert(typeof(TRecord) == typeof(Dictionary<string, object?>));

            var jsonObjectResults = await this.RunOperationAsync(
                OperationName,
                () => this._searchClient.SearchAsync<JsonObject>(searchText, searchOptions, cancellationToken)).ConfigureAwait(false);

<<<<<<< HEAD
<<<<<<< main
            foreach (var result in jsonObjectResults.Value.GetResults())
            {
                var document = VectorStoreErrorHandler.RunModelConversion(
                    DatabaseName,
                    this._collectionName,
                    OperationName,
                    () => this._options.JsonObjectCustomMapper!.MapFromStorageToDataModel(result.Document, new() { IncludeVectors = includeVectors }));
                yield return new(document, result.Score);
            }
=======
            var mappedJsonObjectResults = this.MapSearchResultsAsync(jsonObjectResults.Value.GetResultsAsync(), OperationName, includeVectors);
            return new VectorSearchResults<TRecord>(mappedJsonObjectResults) { TotalCount = jsonObjectResults.Value.TotalCount };
>>>>>>> upstream/main
=======
            await foreach (var result in this.MapSearchResultsAsync(jsonObjectResults.Value.GetResultsAsync(), OperationName, includeVectors).ConfigureAwait(false))
            {
                yield return result;
            }

            yield break;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        }

        // Execute search and map using the built in Azure AI Search mapper.
        Response<SearchResults<TRecord>> results = await this.RunOperationAsync(OperationName, () => this._searchClient.SearchAsync<TRecord>(searchText, searchOptions, cancellationToken)).ConfigureAwait(false);
<<<<<<< HEAD
<<<<<<< main
        foreach (var result in results.Value.GetResults())
        {
            yield return new(result.Document, result.Score);
        }
    }

    /// <summary>
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
        var mappedResults = this.MapSearchResultsAsync(results.Value.GetResultsAsync());
        return new VectorSearchResults<TRecord>(mappedResults) { TotalCount = results.Value.TotalCount };
=======
        await foreach (var result in this.MapSearchResultsAsync(results.Value.GetResultsAsync()).ConfigureAwait(false))
        {
            yield return result;
        }
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <summary>
>>>>>>> upstream/main
=======
>>>>>>> head
>>>>>>> div
    /// Map the data model to the storage model and upload the document.
    /// </summary>
    /// <param name="records">The records to upload.</param>
    /// <param name="innerOptions">The Azure AI Search sdk options for uploading a document.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>The document upload result.</returns>
    private Task<Response<IndexDocumentsResult>> MapToStorageModelAndUploadDocumentAsync(
        IEnumerable<TRecord> records,
        IndexDocumentsOptions innerOptions,
        CancellationToken cancellationToken)
    {
        const string OperationName = "UploadDocuments";

        // Use the user provided mapper.
<<<<<<< HEAD
        if (this._mapper is not null)
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
        if (this._options.JsonObjectCustomMapper is not null)
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
        if (this._options.JsonObjectCustomMapper is not null)
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
        if (this._options.JsonObjectCustomMapper is not null)
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
        if (this._options.JsonObjectCustomMapper is not null)
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
=======
        if (this._dynamicMapper is not null)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        {
            Debug.Assert(typeof(TRecord) == typeof(Dictionary<string, object?>));

            var jsonObjects = VectorStoreErrorHandler.RunModelConversion(
                AzureAISearchConstants.VectorStoreSystemName,
                this._collectionMetadata.VectorStoreName,
                this._collectionName,
                OperationName,
<<<<<<< HEAD
                () => records.Select(this._mapper!.MapFromDataToStorageModel));
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
                () => records.Select(this._options.JsonObjectCustomMapper!.MapFromDataToStorageModel));
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
                () => records.Select(this._options.JsonObjectCustomMapper!.MapFromDataToStorageModel));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
                () => records.Select(this._options.JsonObjectCustomMapper!.MapFromDataToStorageModel));
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
                () => records.Select(this._options.JsonObjectCustomMapper!.MapFromDataToStorageModel));
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
=======
                () => records.Select(r => this._dynamicMapper!.MapFromDataToStorageModel((Dictionary<string, object?>)(object)r)));
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

            return this.RunOperationAsync(
                OperationName,
                () => this._searchClient.UploadDocumentsAsync<JsonObject>(jsonObjects, innerOptions, cancellationToken));
        }

        // Use the built in Azure AI Search mapper.
        return this.RunOperationAsync(
            OperationName,
            () => this._searchClient.UploadDocumentsAsync<TRecord>(records, innerOptions, cancellationToken));
    }

    /// <summary>
    /// Map the search results from <see cref="SearchResult{JsonObject}"/> to <see cref="VectorSearchResult{TRecord}"/> objects using the configured mapper type.
    /// </summary>
    /// <param name="results">The search results to map.</param>
    /// <param name="operationName">The name of the current operation for telemetry purposes.</param>
    /// <param name="includeVectors">A value indicating whether to include vectors in the resultset or not.</param>
    /// <returns>The mapped results.</returns>
    private async IAsyncEnumerable<VectorSearchResult<TRecord>> MapSearchResultsAsync(IAsyncEnumerable<SearchResult<JsonObject>> results, string operationName, bool includeVectors)
    {
        await foreach (var result in results.ConfigureAwait(false))
        {
            var document = VectorStoreErrorHandler.RunModelConversion(
                AzureAISearchConstants.VectorStoreSystemName,
                this._collectionMetadata.VectorStoreName,
                this._collectionName,
                operationName,
                () => (TRecord)(object)this._dynamicMapper!.MapFromStorageToDataModel(result.Document, new() { IncludeVectors = includeVectors }));
            yield return new VectorSearchResult<TRecord>(document, result.Score);
        }
    }

    /// <summary>
    /// Map the search results from <see cref="SearchResult{TRecord}"/> to <see cref="VectorSearchResult{TRecord}"/> objects.
    /// </summary>
    /// <param name="results">The search results to map.</param>
    /// <returns>The mapped results.</returns>
    private async IAsyncEnumerable<VectorSearchResult<TRecord>> MapSearchResultsAsync(IAsyncEnumerable<SearchResult<TRecord>> results)
    {
        await foreach (var result in results.ConfigureAwait(false))
        {
            yield return new VectorSearchResult<TRecord>(result.Document, result.Score);
        }
    }

    /// <summary>
    /// Convert the public <see cref="GetRecordOptions"/> options model to the Azure AI Search <see cref="GetDocumentOptions"/> options model.
    /// </summary>
    /// <param name="options">The public options model.</param>
    /// <returns>The Azure AI Search options model.</returns>
    private GetDocumentOptions ConvertGetDocumentOptions(GetRecordOptions? options)
    {
        var innerOptions = new GetDocumentOptions();
        if (options?.IncludeVectors is not true)
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
            innerOptions.SelectedFields.AddRange(this._nonVectorStoragePropertyNames);
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
            innerOptions.SelectedFields.AddRange(this._nonVectorStoragePropertyNames);
=======
            innerOptions.SelectedFields.AddRange(this._propertyReader.KeyPropertyJsonNames);
            innerOptions.SelectedFields.AddRange(this._propertyReader.DataPropertyJsonNames);
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
            innerOptions.SelectedFields.AddRange(this._propertyReader.KeyPropertyJsonNames);
            innerOptions.SelectedFields.AddRange(this._propertyReader.DataPropertyJsonNames);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
            innerOptions.SelectedFields.AddRange(this._propertyReader.KeyPropertyJsonNames);
            innerOptions.SelectedFields.AddRange(this._propertyReader.DataPropertyJsonNames);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
=======
            innerOptions.SelectedFields.Add(this._model.KeyProperty.StorageName);

            foreach (var dataProperty in this._model.DataProperties)
            {
                innerOptions.SelectedFields.Add(dataProperty.StorageName);
            }
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        }

        return innerOptions;
    }

    /// <summary>
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
    /// Resolve the vector field name to use for a search by using the storage name for the field name from options
    /// if available, and falling back to the first vector field name if not.
    /// </summary>
    /// <param name="optionsVectorFieldName">The vector field name provided via options.</param>
    /// <returns>The resolved vector field name.</returns>
    /// <exception cref="InvalidOperationException">Thrown if the provided field name is not a valid field name.</exception>
    private string ResolveVectorFieldName(string? optionsVectorFieldName)
    {
        string? vectorFieldName;
        if (!string.IsNullOrWhiteSpace(optionsVectorFieldName))
        {
            if (!this._propertyReader.JsonPropertyNamesMap.TryGetValue(optionsVectorFieldName!, out vectorFieldName))
            {
                throw new InvalidOperationException($"The collection does not have a vector field named '{optionsVectorFieldName}'.");
            }
        }
        else
        {
            vectorFieldName = this._propertyReader.FirstVectorPropertyJsonName;
        }

        return vectorFieldName!;
    }

    /// <summary>
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
=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// Get a document with the given key, and return null if it is not found.
    /// </summary>
    /// <typeparam name="T">The type to deserialize the document to.</typeparam>
    /// <param name="searchClient">The search client to use when fetching the document.</param>
    /// <param name="key">The key of the record to get.</param>
    /// <param name="innerOptions">The Azure AI Search sdk options for getting a document.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>The retrieved document, mapped to the consumer data model, or null if not found.</returns>
    private static async Task<T?> GetDocumentWithNotFoundHandlingAsync<T>(
        SearchClient searchClient,
        string key,
        GetDocumentOptions innerOptions,
        CancellationToken cancellationToken)
    {
        try
        {
            return await searchClient.GetDocumentAsync<T>(key, innerOptions, cancellationToken).ConfigureAwait(false);
        }
        catch (RequestFailedException ex) when (ex.Status == 404)
        {
            return default;
        }
    }

    /// <summary>
    /// Run the given operation and wrap any <see cref="RequestFailedException"/> with <see cref="VectorStoreOperationException"/>."/>
    /// </summary>
    /// <typeparam name="T">The response type of the operation.</typeparam>
    /// <param name="operationName">The type of database operation being run.</param>
    /// <param name="operation">The operation to run.</param>
    /// <returns>The result of the operation.</returns>
    private async Task<T> RunOperationAsync<T>(string operationName, Func<Task<T>> operation)
    {
        try
        {
            return await operation.Invoke().ConfigureAwait(false);
        }
        catch (AggregateException ex) when (ex.InnerException is RequestFailedException innerEx)
        {
            throw new VectorStoreOperationException("Call to vector store failed.", ex)
            {
                VectorStoreSystemName = AzureAISearchConstants.VectorStoreSystemName,
                VectorStoreName = this._collectionMetadata.VectorStoreName,
                CollectionName = this._collectionName,
                OperationName = operationName
            };
        }
        catch (RequestFailedException ex)
        {
            throw new VectorStoreOperationException("Call to vector store failed.", ex)
            {
                VectorStoreSystemName = AzureAISearchConstants.VectorStoreSystemName,
                VectorStoreName = this._collectionMetadata.VectorStoreName,
                CollectionName = this._collectionName,
                OperationName = operationName
            };
        }
    }

    private static ReadOnlyMemory<float> VerifyVectorParam<TVector>(TVector vector)
    {
        Verify.NotNull(vector);

        if (vector is not ReadOnlyMemory<float> floatVector)
        {
            throw new NotSupportedException($"The provided vector type {vector.GetType().FullName} is not supported by the Azure AI Search connector.");
        }

        return floatVector;
    }

    private string GetStringKey(TKey key)
    {
        Verify.NotNull(key);

        var stringKey = key as string ?? throw new UnreachableException("string key should have been validated during model building");

        Verify.NotNullOrWhiteSpace(stringKey, nameof(key));

        return stringKey;
    }
}
