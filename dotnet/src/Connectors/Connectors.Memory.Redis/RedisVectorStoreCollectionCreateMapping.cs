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
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.Linq;
using Microsoft.Extensions.VectorData;
using Microsoft.Extensions.VectorData.ConnectorSupport;
using NRedisStack.Search;

namespace Microsoft.SemanticKernel.Connectors.Redis;

/// <summary>
/// Contains mapping helpers to use when creating a redis vector collection.
/// </summary>
internal static class RedisVectorStoreCollectionCreateMapping
{
    /// <summary>A set of number types that are supported for filtering.</summary>
    public static readonly HashSet<Type> s_supportedFilterableNumericDataTypes =
    [
        typeof(short),
        typeof(sbyte),
        typeof(byte),
        typeof(ushort),
        typeof(int),
        typeof(uint),
        typeof(long),
        typeof(ulong),
        typeof(float),
        typeof(double),
        typeof(decimal),

        typeof(short?),
        typeof(sbyte?),
        typeof(byte?),
        typeof(ushort?),
        typeof(int?),
        typeof(uint?),
        typeof(long?),
        typeof(ulong?),
        typeof(float?),
        typeof(double?),
        typeof(decimal?),
    ];

    /// <summary>
    /// Map from the given list of <see cref="VectorStoreRecordProperty"/> items to the Redis <see cref="Schema"/>.
    /// </summary>
    /// <param name="properties">The property definitions to map from.</param>
    /// <param name="useDollarPrefix">A value indicating whether to include $. prefix for field names as required in JSON mode.</param>
    /// <returns>The mapped Redis <see cref="Schema"/>.</returns>
    /// <exception cref="InvalidOperationException">Thrown if there are missing required or unsupported configuration options set.</exception>
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
    public static Schema MapToSchema(IEnumerable<VectorStoreRecordProperty> properties, IReadOnlyDictionary<string, string> storagePropertyNames, bool useDollarPrefix)
=======
    public static Schema MapToSchema(IEnumerable<VectorStoreRecordPropertyModel> properties, bool useDollarPrefix)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        var schema = new Schema();
        var fieldNamePrefix = useDollarPrefix ? "$." : string.Empty;
    /// <param name="useDollarPrefix">A value indicating whether to include $. prefix for field names as required in JSON mode.</param>
    /// <returns>The mapped Redis <see cref="Schema"/>.</returns>
    /// <exception cref="InvalidOperationException">Thrown if there are missing required or unsupported configuration options set.</exception>
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
    public static Schema MapToSchema(IEnumerable<VectorStoreRecordProperty> properties, Dictionary<string, string> storagePropertyNames, bool useDollarPrefix)
    {
        var schema = new Schema();
        var fieldNamePrefix = useDollarPrefix ? "$." : string.Empty;

        // Loop through all properties and create the index fields.
        foreach (var property in properties)
        {
            var storageName = property.StorageName;

            switch (property)
            {
                case VectorStoreRecordKeyPropertyModel keyProperty:
                    // Do nothing, since key is not stored as part of the payload and therefore doesn't have to be added to the index.
                    continue;

                case VectorStoreRecordDataPropertyModel dataProperty when dataProperty.IsIndexed || dataProperty.IsFullTextIndexed:
                    if (dataProperty.IsIndexed && dataProperty.IsFullTextIndexed)
                    {
<<<<<<< HEAD
                        schema.AddTextField(new FieldName($"{fieldNamePrefix}{storageName}", storageName));
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
                        schema.AddTextField(new FieldName($"$.{storageName}", storageName));
                        schema.AddTextField(new FieldName($"{fieldNamePrefix}{storageName}", storageName));
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
                        schema.AddTextField(new FieldName($"$.{storageName}", storageName));
                        schema.AddTextField(new FieldName($"{fieldNamePrefix}{storageName}", storageName));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
                        schema.AddTextField(new FieldName($"$.{storageName}", storageName));
                        schema.AddTextField(new FieldName($"{fieldNamePrefix}{storageName}", storageName));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
=======
                        throw new InvalidOperationException($"Property '{dataProperty.ModelName}' has both {nameof(VectorStoreRecordDataProperty.IsIndexed)} and {nameof(VectorStoreRecordDataProperty.IsFullTextIndexed)} set to true, and this is not supported by the Redis VectorStore.");
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
                    }

                    // Add full text search field index.
                    if (dataProperty.IsFullTextIndexed)
                    {
                        if (dataProperty.Type == typeof(string) || (typeof(IEnumerable).IsAssignableFrom(dataProperty.Type) && GetEnumerableType(dataProperty.Type) == typeof(string)))
                        {
                            schema.AddTextField(new FieldName($"{fieldNamePrefix}{storageName}", storageName));
                        }
                        else
                        {
                            throw new InvalidOperationException($"Property {nameof(dataProperty.IsFullTextIndexed)} on {nameof(VectorStoreRecordDataProperty)} '{dataProperty.ModelName}' is set to true, but the property type is not a string or IEnumerable<string>. The Redis VectorStore supports {nameof(dataProperty.IsFullTextIndexed)} on string or IEnumerable<string> properties only.");
                        }
                    }
<<<<<<< HEAD
                    else if (typeof(IEnumerable).IsAssignableFrom(dataProperty.PropertyType) && GetEnumerableType(dataProperty.PropertyType) == typeof(string))
                    {
                        schema.AddTagField(new FieldName($"{fieldNamePrefix}{storageName}.*", storageName));
                    }
                    else if (RedisVectorStoreCollectionCreateMapping.s_supportedFilterableNumericDataTypes.Contains(dataProperty.PropertyType))
                    {
                        schema.AddNumericField(new FieldName($"{fieldNamePrefix}{storageName}", storageName));
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
                        schema.AddTagField(new FieldName($"$.{storageName}", storageName));
                        schema.AddTagField(new FieldName($"{fieldNamePrefix}{storageName}", storageName));
                    }
                    else if (typeof(IEnumerable).IsAssignableFrom(dataProperty.PropertyType) && GetEnumerableType(dataProperty.PropertyType) == typeof(string))
                    {
                        schema.AddTagField(new FieldName($"{fieldNamePrefix}{storageName}.*", storageName));
                    }
                    else if (RedisVectorStoreCollectionCreateMapping.s_supportedFilterableNumericDataTypes.Contains(dataProperty.PropertyType))
                    {
                        schema.AddNumericField(new FieldName($"$.{storageName}", storageName));
                        schema.AddNumericField(new FieldName($"{fieldNamePrefix}{storageName}", storageName));
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
                    else
                    {
                        throw new InvalidOperationException($"Property '{dataProperty.DataModelPropertyName}' is marked as {nameof(VectorStoreRecordDataProperty.IsFilterable)}, but the property type '{dataProperty.PropertyType}' is not supported. Only string, IEnumerable<string> and numeric properties are supported for filtering by the Redis VectorStore.");
                    }
                }
=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

                    // Add filter field index.
                    if (dataProperty.IsIndexed)
                    {
                        if (dataProperty.Type == typeof(string))
                        {
                            schema.AddTagField(new FieldName($"{fieldNamePrefix}{storageName}", storageName));
                        }
                        else if (typeof(IEnumerable).IsAssignableFrom(dataProperty.Type) && GetEnumerableType(dataProperty.Type) == typeof(string))
                        {
                            schema.AddTagField(new FieldName($"{fieldNamePrefix}{storageName}.*", storageName));
                        }
                        else if (RedisVectorStoreCollectionCreateMapping.s_supportedFilterableNumericDataTypes.Contains(dataProperty.Type))
                        {
                            schema.AddNumericField(new FieldName($"{fieldNamePrefix}{storageName}", storageName));
                        }
                        else
                        {
                            throw new InvalidOperationException($"Property '{dataProperty.ModelName}' is marked as {nameof(VectorStoreRecordDataProperty.IsIndexed)}, but the property type '{dataProperty.Type}' is not supported. Only string, IEnumerable<string> and numeric properties are supported for filtering by the Redis VectorStore.");
                        }
                    }

                    continue;

<<<<<<< HEAD
                var storageName = storagePropertyNames[vectorProperty.DataModelPropertyName];
                var indexKind = GetSDKIndexKind(vectorProperty);
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
                var vectorType = GetSDKVectorType(vectorProperty);
                var dimensions = vectorProperty.Dimensions.Value.ToString(CultureInfo.InvariantCulture);
                var distanceAlgorithm = GetSDKDistanceAlgorithm(vectorProperty);
                schema.AddVectorField(new FieldName($"{fieldNamePrefix}{storageName}", storageName), indexKind, new Dictionary<string, object>()
                {
                    ["TYPE"] = vectorType,
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
                var distanceAlgorithm = GetSDKDistanceAlgorithm(vectorProperty);
=======
                var vectorType = GetSDKVectorType(vectorProperty);
>>>>>>> upstream/main
                var dimensions = vectorProperty.Dimensions.Value.ToString(CultureInfo.InvariantCulture);
                var distanceAlgorithm = GetSDKDistanceAlgorithm(vectorProperty);
                schema.AddVectorField(new FieldName($"{fieldNamePrefix}{storageName}", storageName), indexKind, new Dictionary<string, object>()
                {
                    ["TYPE"] = vectorType,
                    ["DIM"] = dimensions,
                    ["DISTANCE_METRIC"] = distanceAlgorithm
                });
=======
                case VectorStoreRecordVectorPropertyModel vectorProperty:
                    var indexKind = GetSDKIndexKind(vectorProperty);
                    var vectorType = GetSDKVectorType(vectorProperty);
                    var dimensions = vectorProperty.Dimensions.ToString(CultureInfo.InvariantCulture);
                    var distanceAlgorithm = GetSDKDistanceAlgorithm(vectorProperty);
                    schema.AddVectorField(new FieldName($"{fieldNamePrefix}{storageName}", storageName), indexKind, new Dictionary<string, object>()
                    {
                        ["TYPE"] = vectorType,
                        ["DIM"] = dimensions,
                        ["DISTANCE_METRIC"] = distanceAlgorithm
                    });
                    continue;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            }
        }

        return schema;
    }

    /// <summary>
    /// Get the configured <see cref="Schema.VectorField.VectorAlgo"/> from the given <paramref name="vectorProperty"/>.
    /// If none is configured the default is <see cref="Schema.VectorField.VectorAlgo.HNSW"/>.
    /// </summary>
    /// <param name="vectorProperty">The vector property definition.</param>
    /// <returns>The chosen <see cref="Schema.VectorField.VectorAlgo"/>.</returns>
    /// <exception cref="InvalidOperationException">Thrown if a index type was chosen that isn't supported by Redis.</exception>
    public static Schema.VectorField.VectorAlgo GetSDKIndexKind(VectorStoreRecordVectorPropertyModel vectorProperty)
        => vectorProperty.IndexKind switch
        {
            IndexKind.Hnsw or null => Schema.VectorField.VectorAlgo.HNSW,
            IndexKind.Flat => Schema.VectorField.VectorAlgo.FLAT,
            _ => throw new InvalidOperationException($"Index kind '{vectorProperty.IndexKind}' for {nameof(VectorStoreRecordVectorProperty)} '{vectorProperty.ModelName}' is not supported by the Redis VectorStore.")
        };

    /// <summary>
    /// Get the configured distance metric from the given <paramref name="vectorProperty"/>.
    /// If none is configured, the default is cosine.
    /// </summary>
    /// <param name="vectorProperty">The vector property definition.</param>
    /// <returns>The chosen distance metric.</returns>
    /// <exception cref="InvalidOperationException">Thrown if a distance function is chosen that isn't supported by Redis.</exception>
    public static string GetSDKDistanceAlgorithm(VectorStoreRecordVectorPropertyModel vectorProperty)
        => vectorProperty.DistanceFunction switch
        {
            DistanceFunction.CosineSimilarity or null => "COSINE",
            DistanceFunction.CosineDistance => "COSINE",
            DistanceFunction.DotProductSimilarity => "IP",
            DistanceFunction.EuclideanSquaredDistance => "L2",
            _ => throw new InvalidOperationException($"Distance function '{vectorProperty.DistanceFunction}' for {nameof(VectorStoreRecordVectorProperty)} '{vectorProperty.ModelName}' is not supported by the Redis VectorStore.")
        };

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
    /// Get the vector type to pass to the SDK based on the data type of the vector property.
    /// </summary>
    /// <param name="vectorProperty">The vector property definition.</param>
    /// <returns>The SDK required vector type.</returns>
    /// <exception cref="InvalidOperationException">Thrown if the property data type is not supported by the connector.</exception>
    public static string GetSDKVectorType(VectorStoreRecordVectorPropertyModel vectorProperty)
        => vectorProperty.EmbeddingType switch
        {
            Type t when t == typeof(ReadOnlyMemory<float>) => "FLOAT32",
            Type t when t == typeof(ReadOnlyMemory<float>?) => "FLOAT32",
            Type t when t == typeof(ReadOnlyMemory<double>) => "FLOAT64",
            Type t when t == typeof(ReadOnlyMemory<double>?) => "FLOAT64",
            null => throw new UnreachableException("null embedding type"),
            _ => throw new InvalidOperationException($"Vector data type '{vectorProperty.Type.Name}' for {nameof(VectorStoreRecordVectorProperty)} '{vectorProperty.ModelName}' is not supported by the Redis VectorStore.")
        };

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
    /// Gets the type of object stored in the given enumerable type.
    /// </summary>
    /// <param name="type">The enumerable to get the stored type for.</param>
    /// <returns>The type of object stored in the given enumerable type.</returns>
    /// <exception cref="InvalidOperationException">Thrown when the given type is not enumerable.</exception>
    private static Type GetEnumerableType(Type type)
    {
        if (type is IEnumerable)
        {
            return typeof(object);
        }
        else if (type.IsArray)
        {
            return type.GetElementType()!;
        }

        if (type.IsGenericType && type.GetGenericTypeDefinition() == typeof(IEnumerable<>))
        {
            return type.GetGenericArguments()[0];
        }

        if (type.GetInterfaces().FirstOrDefault(i => i.IsGenericType && i.GetGenericTypeDefinition() == typeof(IEnumerable<>)) is Type enumerableInterface)
        {
            return enumerableInterface.GetGenericArguments()[0];
        }

        throw new InvalidOperationException($"Data type '{type}' for {nameof(VectorStoreRecordDataProperty)} is not supported by the Redis VectorStore.");
    }
}
