// Copyright (c) Microsoft. All rights reserved.

using System;
<<<<<<< HEAD
<<<<<<< main
<<<<<<< main
=======
>>>>>>> origin/main
using System.Collections.Generic;
using System.Linq;
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
using System.Reflection;
using System.Text.Json;
using System.Text.Json.Nodes;
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
using System.Reflection;
using System.Text.Json;
using System.Text.Json.Nodes;
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
using Microsoft.SemanticKernel.Data;
=======
<<<<<<< main
=======
>>>>>>> upstream/main
=======
>>>>>>> origin/main
using Microsoft.Extensions.VectorData;
>>>>>>> upstream/main
=======
using Microsoft.Extensions.AI;
using Microsoft.Extensions.VectorData;
using Microsoft.Extensions.VectorData.ConnectorSupport;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
using Pinecone;

namespace Microsoft.SemanticKernel.Connectors.Pinecone;

/// <summary>
/// Mapper between a Pinecone record and the consumer data model that uses json as an intermediary to allow supporting a wide range of models.
/// </summary>
/// <typeparam name="TRecord">The consumer data model to map to or from.</typeparam>
internal sealed class PineconeVectorStoreRecordMapper<TRecord>(VectorStoreRecordModel model)
{
<<<<<<< HEAD
<<<<<<< main
<<<<<<< main
=======
>>>>>>> origin/main
    /// <summary>A set of types that a key on the provided model may have.</summary>
    private static readonly HashSet<Type> s_supportedKeyTypes = [typeof(string)];

    /// <summary>A set of types that data properties on the provided model may have.</summary>
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
        typeof(decimal),
        typeof(decimal?),
    ];

    /// <summary>A set of types that enumerable data properties on the provided model may use as their element types.</summary>
    private static readonly HashSet<Type> s_supportedEnumerableDataElementTypes =
    [
        typeof(string)
    ];

    /// <summary>A set of types that vectors on the provided model may have.</summary>
    private static readonly HashSet<Type> s_supportedVectorTypes =
    [
        typeof(ReadOnlyMemory<float>),
        typeof(ReadOnlyMemory<float>?),
    ];

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
    private readonly PropertyInfo _keyPropertyInfo;

    private readonly List<PropertyInfo> _dataPropertiesInfo;

    private readonly PropertyInfo _vectorPropertyInfo;

    private readonly Dictionary<string, string> _storagePropertyNames = [];

    private readonly Dictionary<string, string> _jsonPropertyNames = [];
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
    private readonly VectorStoreRecordPropertyReader _propertyReader;
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
=======
    private readonly VectorStoreRecordPropertyReader _propertyReader;
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
<<<<<<< main
=======
>>>>>>> upstream/main
=======
>>>>>>> origin/main
    private readonly VectorStoreRecordPropertyReader _propertyReader;
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
    private readonly VectorStoreRecordPropertyReader _propertyReader;
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
    private readonly VectorStoreRecordPropertyReader _propertyReader;
>>>>>>> main
>>>>>>> Stashed changes
=======
    private readonly VectorStoreRecordPropertyReader _propertyReader;
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
    private readonly VectorStoreRecordPropertyReader _propertyReader;
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
    private readonly VectorStoreRecordPropertyReader _propertyReader;
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head

    /// <summary>
    /// Initializes a new instance of the <see cref="PineconeVectorStoreRecordMapper{TDataModel}"/> class.
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
    public PineconeVectorStoreRecordMapper(
        VectorStoreRecordDefinition vectorStoreRecordDefinition)
    {
        // Validate property types.
        var propertiesInfo = VectorStoreRecordPropertyReader.FindProperties(typeof(TRecord), vectorStoreRecordDefinition, supportsMultipleVectors: false);
        VectorStoreRecordPropertyReader.VerifyPropertyTypes([propertiesInfo.KeyProperty], s_supportedKeyTypes, "Key");
        VectorStoreRecordPropertyReader.VerifyPropertyTypes(propertiesInfo.DataProperties, s_supportedDataTypes, s_supportedEnumerableDataElementTypes, "Data");
        VectorStoreRecordPropertyReader.VerifyPropertyTypes(propertiesInfo.VectorProperties, s_supportedVectorTypes, "Vector");

        // Assign.
        this._keyPropertyInfo = propertiesInfo.KeyProperty;
        this._dataPropertiesInfo = propertiesInfo.DataProperties;
        this._vectorPropertyInfo = propertiesInfo.VectorProperties[0];

        // Get storage names and store for later use.
        var properties = VectorStoreRecordPropertyReader.SplitDefinitionAndVerify(typeof(TRecord).Name, vectorStoreRecordDefinition, supportsMultipleVectors: false, requiresAtLeastOneVector: true);
        this._jsonPropertyNames = VectorStoreRecordPropertyReader.BuildPropertyNameToJsonPropertyNameMap(properties, typeof(TRecord), JsonSerializerOptions.Default);
        this._storagePropertyNames = VectorStoreRecordPropertyReader.BuildPropertyNameToStorageNameMap(properties);
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
    /// <param name="propertyReader">A helper to access property information for the current data model and record definition.</param>
    public PineconeVectorStoreRecordMapper(
        VectorStoreRecordPropertyReader propertyReader)
    {
        // Validate property types.
        propertyReader.VerifyHasParameterlessConstructor();
        propertyReader.VerifyKeyProperties(s_supportedKeyTypes);
        propertyReader.VerifyDataProperties(s_supportedDataTypes, s_supportedEnumerableDataElementTypes);
        propertyReader.VerifyVectorProperties(s_supportedVectorTypes);

        // Assign.
        this._propertyReader = propertyReader;
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
    public Vector MapFromDataToStorageModel(TRecord dataModel, Embedding<float>? generatedEmbedding)
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
        var keyObject = this._keyPropertyInfo.GetValue(dataModel);
        if (keyObject is null)
        {
            throw new VectorStoreRecordMappingException($"Key property {this._keyPropertyInfo.Name} on provided record of type {typeof(TRecord).FullName} may not be null.");
        }

        var metadata = new MetadataMap();
        foreach (var dataPropertyInfo in this._dataPropertiesInfo)
        {
            var propertyName = this._storagePropertyNames[dataPropertyInfo.Name];
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
        var keyObject = this._propertyReader.KeyPropertyInfo.GetValue(dataModel);
=======
        var keyObject = model.KeyProperty.GetValueAsObject(dataModel!);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        if (keyObject is null)
        {
            throw new VectorStoreRecordMappingException($"Key property '{model.KeyProperty.ModelName}' on provided record of type '{typeof(TRecord).Name}' may not be null.");
        }

        var metadata = new Metadata();
        foreach (var property in model.DataProperties)
        {
<<<<<<< HEAD
            var propertyName = this._propertyReader.GetStoragePropertyName(dataPropertyInfo.Name);
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
            var propertyValue = dataPropertyInfo.GetValue(dataModel);
            if (propertyValue != null)
            {
                metadata[propertyName] = ConvertToMetadataValue(propertyValue);
            }
        }

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
        var valuesObject = this._vectorPropertyInfo.GetValue(dataModel);
        if (valuesObject is not ReadOnlyMemory<float> values)
        {
            throw new VectorStoreRecordMappingException($"Vector property {this._vectorPropertyInfo.Name} on provided record of type {typeof(TRecord).FullName} may not be null.");
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
        var valuesObject = this._propertyReader.FirstVectorPropertyInfo!.GetValue(dataModel);
        if (valuesObject is not ReadOnlyMemory<float> values)
        {
            throw new VectorStoreRecordMappingException($"Vector property {this._propertyReader.FirstVectorPropertyName} on provided record of type {typeof(TRecord).FullName} may not be null.");
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
            if (property.GetValueAsObject(dataModel!) is { } value)
            {
                metadata[property.StorageName] = PineconeVectorStoreRecordFieldMapping.ConvertToMetadataValue(value);
            }
        }

        var values = (generatedEmbedding?.Vector ?? model.VectorProperty!.GetValueAsObject(dataModel!)) switch
        {
            ReadOnlyMemory<float> floats => floats,
            null => throw new VectorStoreRecordMappingException($"Vector property '{model.VectorProperty.ModelName}' on provided record of type '{typeof(TRecord).Name}' may not be null."),
            _ => throw new VectorStoreRecordMappingException($"Unsupported vector type '{model.VectorProperty.Type.Name}' for vector property '{model.VectorProperty.ModelName}' on provided record of type '{typeof(TRecord).Name}'.")
        };
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // TODO: what about sparse values?
        var result = new Vector
        {
            Id = (string)keyObject,
            Values = values,
            Metadata = metadata,
            SparseValues = null
        };

        return result;
    }

    /// <inheritdoc />
    public TRecord MapFromStorageToDataModel(Vector storageModel, StorageToDataModelMapperOptions options)
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
        var outputJsonObject = new JsonObject
        {
            { keyJsonName, JsonValue.Create(storageModel.Id) },
        };

        if (options?.IncludeVectors is true)
        {
            var propertyName = this._storagePropertyNames[this._vectorPropertyInfo.Name];
            var jsonName = this._jsonPropertyNames[this._vectorPropertyInfo.Name];
            outputJsonObject.Add(jsonName, new JsonArray(storageModel.Values.Select(x => JsonValue.Create(x)).ToArray()));
        }

        if (storageModel.Metadata != null)
        {
            foreach (var dataProperty in this._dataPropertiesInfo)
            {
                var propertyName = this._storagePropertyNames[dataProperty.Name];
                var jsonName = this._jsonPropertyNames[dataProperty.Name];

                if (storageModel.Metadata.TryGetValue(propertyName, out var value))
                {
                    outputJsonObject.Add(jsonName, ConvertFromMetadataValueToJsonNode(value));
                }
            }
        }

        return outputJsonObject.Deserialize<TRecord>()!;
    }

    private static JsonNode? ConvertFromMetadataValueToJsonNode(MetadataValue metadataValue)
        => metadataValue.Inner switch
        {
            null => null,
            bool boolValue => JsonValue.Create(boolValue),
            string stringValue => JsonValue.Create(stringValue),
            int intValue => JsonValue.Create(intValue),
            long longValue => JsonValue.Create(longValue),
            float floatValue => JsonValue.Create(floatValue),
            double doubleValue => JsonValue.Create(doubleValue),
            decimal decimalValue => JsonValue.Create(decimalValue),
            MetadataValue[] array => new JsonArray(array.Select(ConvertFromMetadataValueToJsonNode).ToArray()),
            List<MetadataValue> list => new JsonArray(list.Select(ConvertFromMetadataValueToJsonNode).ToArray()),
            _ => throw new VectorStoreRecordMappingException($"Unsupported metadata type: '{metadataValue.Inner?.GetType().FullName}'."),
        };

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
        // Construct the output record.
        var outputRecord = (TRecord)this._propertyReader.ParameterLessConstructorInfo.Invoke(null);
=======
        var outputRecord = model.CreateRecord<TRecord>()!;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        model.KeyProperty.SetValueAsObject(outputRecord, storageModel.Id);

        if (options?.IncludeVectors is true)
        {
            model.VectorProperty.SetValueAsObject(
                outputRecord,
                storageModel.Values);
        }

        if (storageModel.Metadata != null)
        {
<<<<<<< HEAD
            VectorStoreRecordMapping.SetValuesOnProperties(
                outputRecord,
                this._propertyReader.DataPropertiesInfo,
                this._propertyReader.StoragePropertyNamesMap,
                storageModel.Metadata,
                ConvertFromMetadataValueToNativeType);
=======
            foreach (var property in model.DataProperties)
            {
                property.SetValueAsObject(
                    outputRecord,
                    storageModel.Metadata.TryGetValue(property.StorageName, out var metadataValue) && metadataValue is not null
                        ? PineconeVectorStoreRecordFieldMapping.ConvertFromMetadataValueToNativeType(metadataValue, property.Type)
                        : null);
            }
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        }

        return outputRecord;
    }
<<<<<<< main
<<<<<<< main
=======
>>>>>>> origin/main

    private static object? ConvertFromMetadataValueToNativeType(MetadataValue metadataValue, Type targetType)
        => metadataValue.Inner switch
        {
            null => null,
            bool boolValue => boolValue,
            string stringValue => stringValue,
            // Numeric values are not always coming from the SDK in the desired type
            // that the data model requires, so we need to convert them.
            int intValue => ConvertToNumericValue(intValue, targetType),
            long longValue => ConvertToNumericValue(longValue, targetType),
            float floatValue => ConvertToNumericValue(floatValue, targetType),
            double doubleValue => ConvertToNumericValue(doubleValue, targetType),
            decimal decimalValue => ConvertToNumericValue(decimalValue, targetType),
            MetadataValue[] array => VectorStoreRecordMapping.CreateEnumerable(array.Select(x => ConvertFromMetadataValueToNativeType(x, VectorStoreRecordPropertyVerification.GetCollectionElementType(targetType))), targetType),
            List<MetadataValue> list => VectorStoreRecordMapping.CreateEnumerable(list.Select(x => ConvertFromMetadataValueToNativeType(x, VectorStoreRecordPropertyVerification.GetCollectionElementType(targetType))), targetType),
            _ => throw new VectorStoreRecordMappingException($"Unsupported metadata type: '{metadataValue.Inner?.GetType().FullName}'."),
        };

    private static object? ConvertToNumericValue(object? number, Type targetType)
    {
        if (number is null)
        {
            return null;
        }

        return targetType switch
        {
            Type intType when intType == typeof(int) || intType == typeof(int?) => Convert.ToInt32(number),
            Type longType when longType == typeof(long) || longType == typeof(long?) => Convert.ToInt64(number),
            Type floatType when floatType == typeof(float) || floatType == typeof(float?) => Convert.ToSingle(number),
            Type doubleType when doubleType == typeof(double) || doubleType == typeof(double?) => Convert.ToDouble(number),
            Type decimalType when decimalType == typeof(decimal) || decimalType == typeof(decimal?) => Convert.ToDecimal(number),
            _ => throw new VectorStoreRecordMappingException($"Unsupported target numeric type '{targetType.FullName}'."),
        };
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
    // TODO: take advantage of MetadataValue.TryCreate once we upgrade the version of Pinecone.NET
    private static MetadataValue ConvertToMetadataValue(object? sourceValue)
        => sourceValue switch
        {
            bool boolValue => boolValue,
            string stringValue => stringValue,
            int intValue => intValue,
            long longValue => longValue,
            float floatValue => floatValue,
            double doubleValue => doubleValue,
            decimal decimalValue => decimalValue,
            string[] stringArray => stringArray,
            List<string> stringList => stringList,
            IEnumerable<string> stringEnumerable => stringEnumerable.ToArray(),
            _ => throw new VectorStoreRecordMappingException($"Unsupported source value type '{sourceValue?.GetType().FullName}'.")
        };
<<<<<<< main
=======
>>>>>>> upstream/main
=======
>>>>>>> origin/main
}
