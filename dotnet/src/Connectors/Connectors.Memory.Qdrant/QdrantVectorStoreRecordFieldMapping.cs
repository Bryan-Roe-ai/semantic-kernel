﻿// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections;
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
using System.Text.Json.Nodes;
=======
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
using System.Text.Json.Nodes;
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
using System.Text.Json.Nodes;
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
using Microsoft.SemanticKernel.Data;
=======
using Microsoft.Extensions.VectorData;
>>>>>>> upstream/main
using Qdrant.Client.Grpc;

namespace Microsoft.SemanticKernel.Connectors.Qdrant;

/// <summary>
/// Contains helper methods for mapping fields to and from the format required by the Qdrant client sdk.
/// </summary>
internal static class QdrantVectorStoreRecordFieldMapping
{
    /// <summary>A set of types that data properties on the provided model may have.</summary>
    public static readonly HashSet<Type> s_supportedDataTypes =
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
    public static readonly HashSet<Type> s_supportedVectorTypes =
    [
        typeof(ReadOnlyMemory<float>),
        typeof(ReadOnlyMemory<float>?)
    ];

    /// <summary>
    /// Convert the given <paramref name="payloadValue"/> to the correct native type based on its properties.
    /// </summary>
    /// <param name="payloadValue">The value to convert to a native type.</param>
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
=======
>>>>>>> Stashed changes
    /// <returns>The converted native value.</returns>
    /// <exception cref="VectorStoreRecordMappingException">Thrown when an unsupported type is encountered.</exception>
    public static JsonNode? ConvertFromGrpcFieldValueToJsonNode(Value payloadValue)
=======
<<<<<<< Updated upstream
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
    /// <returns>The converted native value.</returns>
    /// <exception cref="VectorStoreRecordMappingException">Thrown when an unsupported type is encountered.</exception>
    public static JsonNode? ConvertFromGrpcFieldValueToJsonNode(Value payloadValue)
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
    /// <param name="targetType">The target type to convert the value to.</param>
    /// <returns>The converted native value.</returns>
    /// <exception cref="VectorStoreRecordMappingException">Thrown when an unsupported type is encountered.</exception>
    public static object? ConvertFromGrpcFieldValueToNativeType(Value payloadValue, Type targetType)
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
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
    {
        return payloadValue.KindCase switch
        {
            Value.KindOneofCase.NullValue => null,
<<<<<<< Updated upstream
<<<<<<< Updated upstream
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
<<<<<<< HEAD
>>>>>>> Stashed changes
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
    /// Convert the given <paramref name="payloadValue"/> to the correct native type based on its properties.
    /// </summary>
    /// <param name="payloadValue">The value to convert to a native type.</param>
    /// <returns>The converted native value.</returns>
    /// <exception cref="VectorStoreRecordMappingException">Thrown when an unsupported type is encountered.</exception>
    public static object? ConvertFromGrpcFieldValue(Value payloadValue)
<<<<<<< div
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
    {
        return payloadValue.KindCase switch
        {
            Value.KindOneofCase.NullValue => null,
<<<<<<< div
<<<<<<< HEAD
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< HEAD
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
            Value.KindOneofCase.IntegerValue => payloadValue.IntegerValue,
            Value.KindOneofCase.StringValue => payloadValue.StringValue,
            Value.KindOneofCase.DoubleValue => payloadValue.DoubleValue,
            Value.KindOneofCase.BoolValue => payloadValue.BoolValue,
            Value.KindOneofCase.ListValue => payloadValue.ListValue.Values.Select(x => ConvertFromGrpcFieldValue(x)).ToArray(),
            Value.KindOneofCase.StructValue => payloadValue.StructValue.Fields.ToDictionary(x => x.Key, x => ConvertFromGrpcFieldValue(x.Value)),
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
            Value.KindOneofCase.IntegerValue =>
                targetType == typeof(int) || targetType == typeof(int?) ?
                (object)(int)payloadValue.IntegerValue :
                (object)payloadValue.IntegerValue,
            Value.KindOneofCase.StringValue => payloadValue.StringValue,
            Value.KindOneofCase.DoubleValue =>
                targetType == typeof(float) || targetType == typeof(float?) ?
                (object)(float)payloadValue.DoubleValue :
                (object)payloadValue.DoubleValue,
            Value.KindOneofCase.BoolValue => payloadValue.BoolValue,
            Value.KindOneofCase.ListValue => VectorStoreRecordMapping.CreateEnumerable(
                payloadValue.ListValue.Values.Select(
                    x => ConvertFromGrpcFieldValueToNativeType(x, VectorStoreRecordPropertyVerification.GetCollectionElementType(targetType))),
                targetType),
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
            _ => throw new VectorStoreRecordMappingException($"Unsupported grpc value kind {payloadValue.KindCase}."),
        };
    }

    /// <summary>
    /// Convert the given <paramref name="sourceValue"/> to a <see cref="Value"/> object that can be stored in Qdrant.
    /// </summary>
    /// <param name="sourceValue">The object to convert.</param>
    /// <returns>The converted Qdrant value.</returns>
    /// <exception cref="VectorStoreRecordMappingException">Thrown when an unsupported type is encountered.</exception>
    public static Value ConvertToGrpcFieldValue(object? sourceValue)
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
    }
}
