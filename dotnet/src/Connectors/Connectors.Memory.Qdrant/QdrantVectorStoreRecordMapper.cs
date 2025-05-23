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
﻿// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Linq;
<<<<<<< main
using System.Reflection;
using System.Text.Json;
using System.Text.Json.Nodes;
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
// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
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
using Microsoft.SemanticKernel.Data;
=======
using Microsoft.Extensions.VectorData;
>>>>>>> upstream/main
=======
// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Diagnostics;
using System.Linq;
using Google.Protobuf.Collections;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.VectorData;
using Microsoft.Extensions.VectorData.ConnectorSupport;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
using Qdrant.Client.Grpc;

namespace Microsoft.SemanticKernel.Connectors.Qdrant;

/// <summary>
/// Mapper between a Qdrant record and the consumer data model that uses json as an intermediary to allow supporting a wide range of models.
/// </summary>
/// <typeparam name="TRecord">The consumer data model to map to or from.</typeparam>
internal sealed class QdrantVectorStoreRecordMapper<TRecord>(VectorStoreRecordModel model, bool hasNamedVectors)
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
    /// <summary>A set of types that data properties on the provided model may have.</summary>
    private static readonly HashSet<Type> s_supportedDataTypes =
    [
        typeof(string),
        typeof(int),
        typeof(long),
        typeof(double),
        typeof(float),
        typeof(bool),
        typeof(int?),
        typeof(long?),
        typeof(double?),
        typeof(float?),
        typeof(bool?)
    ];

    /// <summary>A set of types that vectors on the provided model may have.</summary>
    /// <remarks>
    /// While qdrant supports float32 and uint64, the api only supports float64, therefore
    /// any float32 vectors will be converted to float64 before being sent to qdrant.
    /// </remarks>
    private static readonly HashSet<Type> s_supportedVectorTypes =
    [
        typeof(ReadOnlyMemory<float>),
        typeof(ReadOnlyMemory<float>?),
        typeof(ReadOnlyMemory<double>),
        typeof(ReadOnlyMemory<double>?)
    ];

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
    /// <summary>A property info object that points at the key property for the current model, allowing easy reading and writing of this property.</summary>
    private readonly PropertyInfo _keyPropertyInfo;

    /// <summary>A list of property info objects that point at the data properties in the current model, and allows easy reading and writing of these properties.</summary>
    private readonly List<PropertyInfo> _dataPropertiesInfo;

    /// <summary>A list of property info objects that point at the vector properties in the current model, and allows easy reading and writing of these properties.</summary>
    private readonly List<PropertyInfo> _vectorPropertiesInfo;

    /// <summary>A dictionary that maps from a property name to the configured name that should be used when storing it.</summary>
    private readonly Dictionary<string, string> _storagePropertyNames;

    /// <summary>A dictionary that maps from a property name to the configured name that should be used when serializing it to json.</summary>
    private readonly Dictionary<string, string> _jsonPropertyNames = new();
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
    /// <summary>A helper to access property information for the current data model and record definition.</summary>
    private readonly VectorStoreRecordPropertyReader _propertyReader;
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
    /// <summary>A helper to access property information for the current data model and record definition.</summary>
    private readonly VectorStoreRecordPropertyReader _propertyReader;
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
    /// <summary>A helper to access property information for the current data model and record definition.</summary>
    private readonly VectorStoreRecordPropertyReader _propertyReader;
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head

    /// <summary>A value indicating whether the vectors in the store are named, or whether there is just a single unnamed vector per qdrant point.</summary>
    private readonly bool _hasNamedVectors;

    /// <summary>
    /// Initializes a new instance of the <see cref="QdrantVectorStoreRecordMapper{TDataModel}"/> class.
    /// </summary>
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
    /// <param name="vectorStoreRecordDefinition">The record definition that defines the schema of the record type.</param>
    /// <param name="hasNamedVectors">A value indicating whether the vectors in the store are named, or whether there is just a single unnamed vector per qdrant point.</param>
    /// <param name="storagePropertyNames">A dictionary that maps from a property name to the configured name that should be used when storing it.</param>
    public QdrantVectorStoreRecordMapper(
        VectorStoreRecordDefinition vectorStoreRecordDefinition,
        bool hasNamedVectors,
        Dictionary<string, string> storagePropertyNames)
    {
        Verify.NotNull(vectorStoreRecordDefinition);
        Verify.NotNull(storagePropertyNames);
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
    /// <param name="propertyReader">A helper to access property information for the current data model and record definition.</param>
    /// <param name="hasNamedVectors">A value indicating whether the vectors in the store are named, or whether there is just a single unnamed vector per qdrant point.</param>
    public QdrantVectorStoreRecordMapper(
        VectorStoreRecordPropertyReader propertyReader,
        bool hasNamedVectors)
    {
        Verify.NotNull(propertyReader);
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

        // Validate property types.
        var propertiesInfo = VectorStoreRecordPropertyReader.FindProperties(typeof(TRecord), vectorStoreRecordDefinition, supportsMultipleVectors: hasNamedVectors);
        VectorStoreRecordPropertyReader.VerifyPropertyTypes(propertiesInfo.DataProperties, QdrantVectorStoreRecordFieldMapping.s_supportedDataTypes, "Data", supportEnumerable: true);
        VectorStoreRecordPropertyReader.VerifyPropertyTypes(propertiesInfo.VectorProperties, QdrantVectorStoreRecordFieldMapping.s_supportedVectorTypes, "Vector");
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

        // Assign.
        this._hasNamedVectors = hasNamedVectors;
        this._keyPropertyInfo = propertiesInfo.KeyProperty;
        this._dataPropertiesInfo = propertiesInfo.DataProperties;
        this._vectorPropertiesInfo = propertiesInfo.VectorProperties;
        this._storagePropertyNames = storagePropertyNames;

        // Get json storage names and store for later use.
        this._jsonPropertyNames = VectorStoreRecordPropertyReader.BuildPropertyNameToJsonPropertyNameMap(propertiesInfo, typeof(TRecord), JsonSerializerOptions.Default);
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
        VectorStoreRecordPropertyReader.VerifyPropertyTypes(propertiesInfo.DataProperties, s_supportedDataTypes, "Data", supportEnumerable: true);
        VectorStoreRecordPropertyReader.VerifyPropertyTypes(propertiesInfo.VectorProperties, s_supportedVectorTypes, "Vector");
        propertyReader.VerifyHasParameterlessConstructor();
        propertyReader.VerifyDataProperties(QdrantVectorStoreRecordFieldMapping.s_supportedDataTypes, supportEnumerable: true);
        propertyReader.VerifyVectorProperties(QdrantVectorStoreRecordFieldMapping.s_supportedVectorTypes);

        // Assign.
        this._propertyReader = propertyReader;
        this._hasNamedVectors = hasNamedVectors;
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

=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// <inheritdoc />
    public PointStruct MapFromDataToStorageModel(TRecord dataModel, int recordIndex, GeneratedEmbeddings<Embedding<float>>?[]? generatedEmbeddings)
    {
<<<<<<< HEAD
        PointId pointId;
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
        if (this._keyPropertyInfo.PropertyType == typeof(ulong))
        {
            var key = this._keyPropertyInfo.GetValue(dataModel) as ulong? ?? throw new VectorStoreRecordMappingException($"Missing key property {this._keyPropertyInfo.Name} on provided record of type {typeof(TRecord).FullName}.");
            pointId = new PointId { Num = key };
        }
        else if (this._keyPropertyInfo.PropertyType == typeof(Guid))
        {
            var key = this._keyPropertyInfo.GetValue(dataModel) as Guid? ?? throw new VectorStoreRecordMappingException($"Missing key property {this._keyPropertyInfo.Name} on provided record of type {typeof(TRecord).FullName}.");
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
        var keyPropertyInfo = this._propertyReader.KeyPropertyInfo;
        if (keyPropertyInfo.PropertyType == typeof(ulong))
        {
            var key = keyPropertyInfo.GetValue(dataModel) as ulong? ?? throw new VectorStoreRecordMappingException($"Missing key property {keyPropertyInfo.Name} on provided record of type {typeof(TRecord).FullName}.");
            pointId = new PointId { Num = key };
        }
        else if (keyPropertyInfo.PropertyType == typeof(Guid))
        {
            var key = keyPropertyInfo.GetValue(dataModel) as Guid? ?? throw new VectorStoreRecordMappingException($"Missing key property {keyPropertyInfo.Name} on provided record of type {typeof(TRecord).FullName}.");
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
            pointId = new PointId { Uuid = key.ToString("D") };
        }
        else
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
            throw new VectorStoreRecordMappingException($"Unsupported key type {this._keyPropertyInfo.PropertyType.FullName} for key property {this._keyPropertyInfo.Name} on provided record of type {typeof(TRecord).FullName}.");
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
            throw new VectorStoreRecordMappingException($"Unsupported key type {this._keyPropertyInfo.PropertyType.FullName} for key property {this._keyPropertyInfo.Name} on provided record of type {typeof(TRecord).FullName}.");
=======
            throw new VectorStoreRecordMappingException($"Unsupported key type {keyPropertyInfo.PropertyType.FullName} for key property {keyPropertyInfo.Name} on provided record of type {typeof(TRecord).FullName}.");
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
            throw new VectorStoreRecordMappingException($"Unsupported key type {keyPropertyInfo.PropertyType.FullName} for key property {keyPropertyInfo.Name} on provided record of type {typeof(TRecord).FullName}.");
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
            throw new VectorStoreRecordMappingException($"Unsupported key type {keyPropertyInfo.PropertyType.FullName} for key property {keyPropertyInfo.Name} on provided record of type {typeof(TRecord).FullName}.");
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
        }
=======
        var keyProperty = model.KeyProperty;

        var pointId = keyProperty.Type switch
        {
            var t when t == typeof(ulong) => new PointId
            {
                Num = (ulong?)keyProperty.GetValueAsObject(dataModel!) ?? throw new VectorStoreRecordMappingException($"Missing key property '{keyProperty.ModelName}' on provided record of type '{typeof(TRecord).Name}'.")
            },

            var t when t == typeof(Guid) => new PointId
            {
                Uuid = ((Guid?)keyProperty.GetValueAsObject(dataModel!))?.ToString("D") ?? throw new VectorStoreRecordMappingException($"Missing key property '{keyProperty.ModelName}' on provided record of type '{typeof(TRecord).Name}'.")
            },
            _ => throw new VectorStoreRecordMappingException($"Unsupported key type '{keyProperty.Type.Name}' for key property '{keyProperty.ModelName}' on provided record of type '{typeof(TRecord).Name}'.")
        };
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Create point.
        var pointStruct = new PointStruct
        {
            Id = pointId,
            Vectors = new Vectors(),
            Payload = { },
        };

        // Add point payload.
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
        foreach (var dataPropertyInfo in this._dataPropertiesInfo)
        {
            var propertyName = this._storagePropertyNames[dataPropertyInfo.Name];
            var propertyValue = dataPropertyInfo.GetValue(dataModel);
            pointStruct.Payload.Add(propertyName, QdrantVectorStoreRecordFieldMapping.ConvertToGrpcFieldValue(propertyValue));
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
        foreach (var dataPropertyInfo in this._propertyReader.DataPropertiesInfo)
        {
            var propertyName = this._propertyReader.GetStoragePropertyName(dataPropertyInfo.Name);
            var propertyValue = dataPropertyInfo.GetValue(dataModel);
            pointStruct.Payload.Add(propertyName, QdrantVectorStoreRecordFieldMapping.ConvertToGrpcFieldValue(propertyValue));
            pointStruct.Payload.Add(propertyName, ConvertToGrpcFieldValue(propertyValue));
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
        foreach (var property in model.DataProperties)
        {
            var propertyValue = property.GetValueAsObject(dataModel!);
            pointStruct.Payload.Add(property.StorageName, QdrantVectorStoreRecordFieldMapping.ConvertToGrpcFieldValue(propertyValue));
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        }

        // Add vectors.
        if (hasNamedVectors)
        {
            var namedVectors = new NamedVectors();
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
            foreach (var vectorPropertyInfo in this._vectorPropertiesInfo)
            {
                var propertyName = this._storagePropertyNames[vectorPropertyInfo.Name];
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
            foreach (var vectorPropertyInfo in this._vectorPropertiesInfo)
            {
                var propertyName = this._storagePropertyNames[vectorPropertyInfo.Name];
=======
            foreach (var vectorPropertyInfo in this._propertyReader.VectorPropertiesInfo)
            {
                var propertyName = this._propertyReader.GetStoragePropertyName(vectorPropertyInfo.Name);
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
            foreach (var vectorPropertyInfo in this._propertyReader.VectorPropertiesInfo)
            {
                var propertyName = this._propertyReader.GetStoragePropertyName(vectorPropertyInfo.Name);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
                var propertyValue = vectorPropertyInfo.GetValue(dataModel);
                if (propertyValue is not null)
                {
                    var castPropertyValue = (ReadOnlyMemory<float>)propertyValue;
                    namedVectors.Vectors.Add(propertyName, castPropertyValue.ToArray());
                }
=======

            for (var i = 0; i < model.VectorProperties.Count; i++)
            {
                var property = model.VectorProperties[i];

                namedVectors.Vectors.Add(
                    property.StorageName,
                    GetVector(
                        property,
                        generatedEmbeddings?[i] is GeneratedEmbeddings<Embedding<float>> e
                            ? e[recordIndex]
                            : property.GetValueAsObject(dataModel!)));
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            }

            pointStruct.Vectors.Vectors_ = namedVectors;
        }
        else
        {
            // We already verified in the constructor via FindProperties that there is exactly one vector property when not using named vectors.
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
            var vectorPropertyInfo = this._vectorPropertiesInfo.First();
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
            var vectorPropertyInfo = this._vectorPropertiesInfo.First();
=======
            var vectorPropertyInfo = this._propertyReader.FirstVectorPropertyInfo!;
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
            var vectorPropertyInfo = this._propertyReader.FirstVectorPropertyInfo!;
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
            if (vectorPropertyInfo.GetValue(dataModel) is ReadOnlyMemory<float> floatROM)
            {
                pointStruct.Vectors.Vector = floatROM.ToArray();
            }
            else
            {
                throw new VectorStoreRecordMappingException($"Vector property {vectorPropertyInfo.Name} on provided record of type {typeof(TRecord).FullName} may not be null when not using named vectors.");
            }
=======
            Debug.Assert(
                generatedEmbeddings is null || generatedEmbeddings.Length == 1 && generatedEmbeddings[0] is not null,
                "There should be exactly one generated embedding when not using named vectors (single vector property).");
            pointStruct.Vectors.Vector = GetVector(
                model.VectorProperty,
                generatedEmbeddings is null
                    ? model.VectorProperty.GetValueAsObject(dataModel!)
                    : generatedEmbeddings[0]![recordIndex].Vector);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        }

        return pointStruct;

        Vector GetVector(VectorStoreRecordPropertyModel property, object? embedding)
            => embedding switch
            {
                ReadOnlyMemory<float> floatVector => floatVector.ToArray(),
                null => throw new VectorStoreRecordMappingException($"Vector property '{property.ModelName}' on provided record of type '{typeof(TRecord).Name}' may not be null when not using named vectors."),
                var unknownEmbedding => throw new VectorStoreRecordMappingException($"Vector property '{property.ModelName}' on provided record of type '{typeof(TRecord).Name}' has unsupported embedding type '{unknownEmbedding.GetType().Name}'.")
            };
    }

    /// <inheritdoc />
    public TRecord MapFromStorageToDataModel(PointId pointId, MapField<string, Value> payload, VectorsOutput vectorsOutput, StorageToDataModelMapperOptions options)
    {
<<<<<<< HEAD
        // Get the key property name and value.
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
        var keyJsonName = this._jsonPropertyNames[this._keyPropertyInfo.Name];
        var keyPropertyValue = storageModel.Id.HasNum ? storageModel.Id.Num as object : storageModel.Id.Uuid as object;

        // Create a json object to represent the point.
        var outputJsonObject = new JsonObject
        {
            { keyJsonName, JsonValue.Create(keyPropertyValue) },
        };

        // Add each vector property if embeddings are included in the point.
        if (options?.IncludeVectors is true)
        {
            foreach (var vectorProperty in this._vectorPropertiesInfo)
            {
                var propertyName = this._storagePropertyNames[vectorProperty.Name];
                var jsonName = this._jsonPropertyNames[vectorProperty.Name];

                if (this._hasNamedVectors)
                {
                    if (storageModel.Vectors.Vectors_.Vectors.TryGetValue(propertyName, out var vector))
                    {
                        outputJsonObject.Add(jsonName, new JsonArray(vector.Data.Select(x => JsonValue.Create(x)).ToArray()));
                    }
                }
                else
                {
                    outputJsonObject.Add(jsonName, new JsonArray(storageModel.Vectors.Vector.Data.Select(x => JsonValue.Create(x)).ToArray()));
                }
            }
        }

        // Add each data property.
        foreach (var dataProperty in this._dataPropertiesInfo)
        {
            var propertyName = this._storagePropertyNames[dataProperty.Name];
            var jsonName = this._jsonPropertyNames[dataProperty.Name];

            if (storageModel.Payload.TryGetValue(propertyName, out var value))
            {
                outputJsonObject.Add(jsonName, QdrantVectorStoreRecordFieldMapping.ConvertFromGrpcFieldValueToJsonNode(value));
            }
        }

        // Convert from json object to the target data model.
        return JsonSerializer.Deserialize<TRecord>(outputJsonObject)!;
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
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        var keyPropertyValue = storageModel.Id.HasNum ? storageModel.Id.Num as object : new Guid(storageModel.Id.Uuid) as object;
=======
        var outputRecord = model.CreateRecord<TRecord>()!;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // TODO: Set the following generically to avoid boxing
        model.KeyProperty.SetValueAsObject(outputRecord, pointId switch
        {
            { HasNum: true } => pointId.Num,
            { HasUuid: true } => Guid.Parse(pointId.Uuid),
            _ => throw new UnreachableException()
        });

        // Set each vector property if embeddings are included in the point.
        if (options?.IncludeVectors is true)
        {
            if (hasNamedVectors)
            {
                var storageVectors = vectorsOutput.Vectors.Vectors;

                foreach (var vectorProperty in model.VectorProperties)
                {
                    vectorProperty.SetValueAsObject(
                        outputRecord,
                        new ReadOnlyMemory<float>(storageVectors[vectorProperty.StorageName].Data.ToArray()));
                }
            }
            else
            {
<<<<<<< HEAD
                outputJsonObject.Add(jsonName, QdrantVectorStoreRecordFieldMapping.ConvertFromGrpcFieldValueToJsonNode(value));
                outputJsonObject.Add(jsonName, ConvertFromGrpcFieldValueToJsonNode(value));
                var propertyInfoWithValue = new KeyValuePair<PropertyInfo, object?>(
                        this._propertyReader.FirstVectorPropertyInfo!,
                        new ReadOnlyMemory<float>(storageModel.Vectors.Vector.Data.ToArray()));
                VectorStoreRecordMapping.SetPropertiesOnRecord(
                this._propertyReader.FirstVectorPropertyInfo!.SetValue(
=======
                model.VectorProperty.SetValueAsObject(
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
                    outputRecord,
                    new ReadOnlyMemory<float>(vectorsOutput.Vector.Data.ToArray()));
            }
        }

        foreach (var dataProperty in model.DataProperties)
        {
            if (payload.TryGetValue(dataProperty.StorageName, out var fieldValue))
            {
                dataProperty.SetValueAsObject(
                    outputRecord,
                    QdrantVectorStoreRecordFieldMapping.ConvertFromGrpcFieldValueToNativeType(fieldValue, dataProperty.Type));
            }
        }

        return outputRecord;
    }

    /// <summary>
    /// Convert the given <paramref name="payloadValue"/> to the correct native type based on its properties.
    /// </summary>
    /// <param name="payloadValue">The value to convert to a native type.</param>
    /// <returns>The converted native value.</returns>
    /// <exception cref="VectorStoreRecordMappingException">Thrown when an unsupported type is encountered.</exception>
    private static JsonNode? ConvertFromGrpcFieldValueToJsonNode(Value payloadValue)
    {
        return payloadValue.KindCase switch
        {
            Value.KindOneofCase.NullValue => null,
            Value.KindOneofCase.IntegerValue => JsonValue.Create(payloadValue.IntegerValue),
            Value.KindOneofCase.StringValue => JsonValue.Create(payloadValue.StringValue),
            Value.KindOneofCase.DoubleValue => JsonValue.Create(payloadValue.DoubleValue),
            Value.KindOneofCase.BoolValue => JsonValue.Create(payloadValue.BoolValue),
            Value.KindOneofCase.ListValue => new JsonArray(payloadValue.ListValue.Values.Select(x => ConvertFromGrpcFieldValueToJsonNode(x)).ToArray()),
            Value.KindOneofCase.StructValue => new JsonObject(payloadValue.StructValue.Fields.ToDictionary(x => x.Key, x => ConvertFromGrpcFieldValueToJsonNode(x.Value))),
            _ => throw new VectorStoreRecordMappingException($"Unsupported grpc value kind {payloadValue.KindCase}."),
        };
    }

    /// <summary>
    /// Convert the given <paramref name="sourceValue"/> to a <see cref="Value"/> object that can be stored in Qdrant.
    /// </summary>
    /// <param name="sourceValue">The object to convert.</param>
    /// <returns>The converted Qdrant value.</returns>
    /// <exception cref="VectorStoreRecordMappingException">Thrown when an unsupported type is encountered.</exception>
    private static Value ConvertToGrpcFieldValue(object? sourceValue)
    {
        var value = new Value();
        if (sourceValue is null)
        {
            value.NullValue = NullValue.NullValue;
        }
        else if (sourceValue is int intValue)
        {
            value.IntegerValue = intValue;
        }
        else if (sourceValue is long longValue)
        {
            value.IntegerValue = longValue;
        }
        else if (sourceValue is string stringValue)
        {
            value.StringValue = stringValue;
        }
        else if (sourceValue is float floatValue)
        {
            value.DoubleValue = floatValue;
        }
        else if (sourceValue is double doubleValue)
        {
            value.DoubleValue = doubleValue;
        }
        else if (sourceValue is bool boolValue)
        {
            value.BoolValue = boolValue;
        }
        else if (sourceValue is IEnumerable<int> ||
            sourceValue is IEnumerable<long> ||
            sourceValue is IEnumerable<string> ||
            sourceValue is IEnumerable<float> ||
            sourceValue is IEnumerable<double> ||
            sourceValue is IEnumerable<bool>)
        {
            var listValue = sourceValue as IEnumerable;
            value.ListValue = new ListValue();
            foreach (var item in listValue!)
            {
                value.ListValue.Values.Add(ConvertToGrpcFieldValue(item));
            }
        }
        else
        {
            throw new VectorStoreRecordMappingException($"Unsupported source value type {sourceValue?.GetType().FullName}.");
        }

        return value;
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
}
