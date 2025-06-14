// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Text.Json.Serialization;
using Microsoft.Extensions.VectorData;
using Microsoft.Extensions.VectorData.ProviderServices;
using Microsoft.SemanticKernel.Connectors.Weaviate;
using Xunit;

namespace SemanticKernel.Connectors.Weaviate.UnitTests;

/// <summary>
/// Unit tests for dynamic mapping.
/// </summary>
public sealed class WeaviateDynamicMapperTests
{
    private const bool HasNamedVectors = true;

    private static readonly JsonSerializerOptions s_jsonSerializerOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
        Converters =
        {
            new WeaviateDateTimeOffsetConverter(),
            new WeaviateNullableDateTimeOffsetConverter()
        }
    };

    private static readonly CollectionModel s_model = new WeaviateModelBuilder(HasNamedVectors)
        .BuildDynamic(
            new VectorStoreCollectionDefinition
            {
                Properties =
                [
                    new VectorStoreKeyProperty("Key", typeof(Guid)),

                    new VectorStoreDataProperty("StringDataProp", typeof(string)),
                    new VectorStoreDataProperty("BoolDataProp", typeof(bool)),
                    new VectorStoreDataProperty("NullableBoolDataProp", typeof(bool?)),
                    new VectorStoreDataProperty("IntDataProp", typeof(int)),
                    new VectorStoreDataProperty("NullableIntDataProp", typeof(int?)),
                    new VectorStoreDataProperty("LongDataProp", typeof(long)),
                    new VectorStoreDataProperty("NullableLongDataProp", typeof(long?)),
                    new VectorStoreDataProperty("ShortDataProp", typeof(short)),
                    new VectorStoreDataProperty("NullableShortDataProp", typeof(short?)),
                    new VectorStoreDataProperty("ByteDataProp", typeof(byte)),
                    new VectorStoreDataProperty("NullableByteDataProp", typeof(byte?)),
                    new VectorStoreDataProperty("FloatDataProp", typeof(float)),
                    new VectorStoreDataProperty("NullableFloatDataProp", typeof(float?)),
                    new VectorStoreDataProperty("DoubleDataProp", typeof(double)),
                    new VectorStoreDataProperty("NullableDoubleDataProp", typeof(double?)),
                    new VectorStoreDataProperty("DecimalDataProp", typeof(decimal)),
                    new VectorStoreDataProperty("NullableDecimalDataProp", typeof(decimal?)),
                    new VectorStoreDataProperty("DateTimeDataProp", typeof(DateTime)),
                    new VectorStoreDataProperty("NullableDateTimeDataProp", typeof(DateTime?)),
                    new VectorStoreDataProperty("DateTimeOffsetDataProp", typeof(DateTimeOffset)),
                    new VectorStoreDataProperty("NullableDateTimeOffsetDataProp", typeof(DateTimeOffset?)),
                    new VectorStoreDataProperty("GuidDataProp", typeof(Guid)),
                    new VectorStoreDataProperty("NullableGuidDataProp", typeof(Guid?)),
                    new VectorStoreDataProperty("TagListDataProp", typeof(List<string>)),

                    new VectorStoreVectorProperty("FloatVector", typeof(ReadOnlyMemory<float>), 10),
                    new VectorStoreVectorProperty("NullableFloatVector", typeof(ReadOnlyMemory<float>?), 10)
                ]
            },
            defaultEmbeddingGenerator: null,
            s_jsonSerializerOptions);

    private static readonly float[] s_floatVector = [1.0f, 2.0f, 3.0f];
    private static readonly List<string> s_taglist = ["tag1", "tag2"];

    [Fact]
    public void MapFromDataToStorageModelMapsAllSupportedTypes()
    {
        // Arrange
        var key = new Guid("55555555-5555-5555-5555-555555555555");
        var sut = new WeaviateMapper<Dictionary<string, object?>>("Collection", HasNamedVectors, s_model, s_jsonSerializerOptions);

        var dataModel = new Dictionary<string, object?>
        {
            ["Key"] = key,

            ["StringDataProp"] = "string",
            ["BoolDataProp"] = true,
            ["NullableBoolDataProp"] = false,
            ["IntDataProp"] = 1,
            ["NullableIntDataProp"] = 2,
            ["LongDataProp"] = 3L,
            ["NullableLongDataProp"] = 4L,
            ["ShortDataProp"] = (short)5,
            ["NullableShortDataProp"] = (short)6,
            ["ByteDataProp"] = (byte)7,
            ["NullableByteDataProp"] = (byte)8,
            ["FloatDataProp"] = 9.0f,
            ["NullableFloatDataProp"] = 10.0f,
            ["DoubleDataProp"] = 11.0,
            ["NullableDoubleDataProp"] = 12.0,
            ["DecimalDataProp"] = 13.99m,
            ["NullableDecimalDataProp"] = 14.00m,
            ["DateTimeDataProp"] = new DateTime(2021, 1, 1),
            ["NullableDateTimeDataProp"] = new DateTime(2021, 1, 1),
            ["DateTimeOffsetDataProp"] = new DateTimeOffset(2022, 1, 1, 0, 0, 0, TimeSpan.Zero),
            ["NullableDateTimeOffsetDataProp"] = new DateTimeOffset(2022, 1, 1, 0, 0, 0, TimeSpan.Zero),
            ["GuidDataProp"] = new Guid("11111111-1111-1111-1111-111111111111"),
            ["NullableGuidDataProp"] = new Guid("22222222-2222-2222-2222-222222222222"),
            ["TagListDataProp"] = s_taglist,

            ["FloatVector"] = new ReadOnlyMemory<float>(s_floatVector),
            ["NullableFloatVector"] = new ReadOnlyMemory<float>(s_floatVector),
        }
        ;

        // Act
        var storageModel = sut.MapFromDataToStorageModel(dataModel, recordIndex: 0, generatedEmbeddings: null);

        // Assert
        Assert.Equal(key, (Guid?)storageModel["id"]);
        Assert.Equal("Collection", (string?)storageModel["class"]);
        Assert.Equal("string", (string?)storageModel["properties"]?["stringDataProp"]);
        Assert.Equal(true, (bool?)storageModel["properties"]?["boolDataProp"]);
        Assert.Equal(false, (bool?)storageModel["properties"]?["nullableBoolDataProp"]);
        Assert.Equal(1, (int?)storageModel["properties"]?["intDataProp"]);
        Assert.Equal(2, (int?)storageModel["properties"]?["nullableIntDataProp"]);
        Assert.Equal(3L, (long?)storageModel["properties"]?["longDataProp"]);
        Assert.Equal(4L, (long?)storageModel["properties"]?["nullableLongDataProp"]);
        Assert.Equal((short)5, (short?)storageModel["properties"]?["shortDataProp"]);
        Assert.Equal((short)6, (short?)storageModel["properties"]?["nullableShortDataProp"]);
        Assert.Equal((byte)7, (byte?)storageModel["properties"]?["byteDataProp"]);
        Assert.Equal((byte)8, (byte?)storageModel["properties"]?["nullableByteDataProp"]);
        Assert.Equal(9.0f, (float?)storageModel["properties"]?["floatDataProp"]);
        Assert.Equal(10.0f, (float?)storageModel["properties"]?["nullableFloatDataProp"]);
        Assert.Equal(11.0, (double?)storageModel["properties"]?["doubleDataProp"]);
        Assert.Equal(12.0, (double?)storageModel["properties"]?["nullableDoubleDataProp"]);
        Assert.Equal(13.99m, (decimal?)storageModel["properties"]?["decimalDataProp"]);
        Assert.Equal(14.00m, (decimal?)storageModel["properties"]?["nullableDecimalDataProp"]);
        Assert.Equal(new DateTime(2021, 1, 1, 0, 0, 0), (DateTime?)storageModel["properties"]?["dateTimeDataProp"]);
        Assert.Equal(new DateTime(2021, 1, 1, 0, 0, 0), (DateTime?)storageModel["properties"]?["nullableDateTimeDataProp"]);
        Assert.Equal(new DateTimeOffset(2022, 1, 1, 0, 0, 0, TimeSpan.Zero), (DateTimeOffset?)storageModel["properties"]?["dateTimeOffsetDataProp"]);
        Assert.Equal(new DateTimeOffset(2022, 1, 1, 0, 0, 0, TimeSpan.Zero), (DateTimeOffset?)storageModel["properties"]?["nullableDateTimeOffsetDataProp"]);
        Assert.Equal(new Guid("11111111-1111-1111-1111-111111111111"), (Guid?)storageModel["properties"]?["guidDataProp"]);
        Assert.Equal(new Guid("22222222-2222-2222-2222-222222222222"), (Guid?)storageModel["properties"]?["nullableGuidDataProp"]);
        Assert.Equal(s_taglist, storageModel["properties"]?["tagListDataProp"]!.AsArray().GetValues<string>().ToArray());
        Assert.Equal(s_floatVector, storageModel["vectors"]?["floatVector"]!.AsArray().GetValues<float>().ToArray());
        Assert.Equal(s_floatVector, storageModel["vectors"]?["nullableFloatVector"]!.AsArray().GetValues<float>().ToArray());
    }

    [Fact]
    public void MapFromDataToStorageModelMapsNullValues()
    {
        // Arrange
        var key = new Guid("55555555-5555-5555-5555-555555555555");
        var keyProperty = new VectorStoreKeyProperty("Key", typeof(Guid));

        var dataProperties = new List<VectorStoreDataProperty>
        {
            new("StringDataProp", typeof(string)),
            new("NullableIntDataProp", typeof(int?)),
        };

        var vectorProperties = new List<VectorStoreVectorProperty>
        {
            new("NullableFloatVector", typeof(ReadOnlyMemory<float>?), 10)
        };

        var dataModel = new Dictionary<string, object?>
        {
            ["Key"] = key,

            ["StringDataProp"] = null,
            ["NullableIntDataProp"] = null,

            ["NullableFloatVector"] = null
        };

        var sut = new WeaviateMapper<Dictionary<string, object?>>("Collection", HasNamedVectors, s_model, s_jsonSerializerOptions);

        // Act
        var storageModel = sut.MapFromDataToStorageModel(dataModel, recordIndex: 0, generatedEmbeddings: null);

        // Assert
        Assert.Null(storageModel["StringDataProp"]);
        Assert.Null(storageModel["NullableIntDataProp"]);
        Assert.Null(storageModel["NullableFloatVector"]);
    }

    [Fact]
    public void MapFromStorageToDataModelMapsAllSupportedTypes()
    {
        // Arrange
        var key = new Guid("55555555-5555-5555-5555-555555555555");
        var sut = new WeaviateMapper<Dictionary<string, object?>>("Collection", HasNamedVectors, s_model, s_jsonSerializerOptions);

        var storageModel = new JsonObject
        {
            ["id"] = key,
            ["properties"] = new JsonObject
            {
                ["stringDataProp"] = "string",
                ["boolDataProp"] = true,
                ["nullableBoolDataProp"] = false,
                ["intDataProp"] = 1,
                ["nullableIntDataProp"] = 2,
                ["longDataProp"] = 3L,
                ["nullableLongDataProp"] = 4L,
                ["shortDataProp"] = (short)5,
                ["nullableShortDataProp"] = (short)6,
                ["byteDataProp"] = (byte)7,
                ["nullableByteDataProp"] = (byte)8,
                ["floatDataProp"] = 9.0f,
                ["nullableFloatDataProp"] = 10.0f,
                ["doubleDataProp"] = 11.0,
                ["nullableDoubleDataProp"] = 12.0,
                ["decimalDataProp"] = 13.99m,
                ["nullableDecimalDataProp"] = 14.00m,
                ["dateTimeDataProp"] = new DateTime(2021, 1, 1),
                ["nullableDateTimeDataProp"] = new DateTime(2021, 1, 1),
                ["dateTimeOffsetDataProp"] = new DateTimeOffset(2022, 1, 1, 0, 0, 0, TimeSpan.Zero),
                ["nullableDateTimeOffsetDataProp"] = new DateTimeOffset(2022, 1, 1, 0, 0, 0, TimeSpan.Zero),
                ["guidDataProp"] = new Guid("11111111-1111-1111-1111-111111111111"),
                ["nullableGuidDataProp"] = new Guid("22222222-2222-2222-2222-222222222222"),
                ["tagListDataProp"] = new JsonArray(s_taglist.Select(l => (JsonValue)l).ToArray())
            },
            ["vectors"] = new JsonObject
            {
                ["floatVector"] = new JsonArray(s_floatVector.Select(l => (JsonValue)l).ToArray()),
                ["nullableFloatVector"] = new JsonArray(s_floatVector.Select(l => (JsonValue)l).ToArray()),
            }
        };

        // Act
        var dataModel = sut.MapFromStorageToDataModel(storageModel, includeVectors: true);

        // Assert
        Assert.Equal(key, dataModel["Key"]);
        Assert.Equal("string", dataModel["StringDataProp"]);
        Assert.Equal(true, dataModel["BoolDataProp"]);
        Assert.Equal(false, dataModel["NullableBoolDataProp"]);
        Assert.Equal(1, dataModel["IntDataProp"]);
        Assert.Equal(2, dataModel["NullableIntDataProp"]);
        Assert.Equal(3L, dataModel["LongDataProp"]);
        Assert.Equal(4L, dataModel["NullableLongDataProp"]);
        Assert.Equal((short)5, dataModel["ShortDataProp"]);
        Assert.Equal((short)6, dataModel["NullableShortDataProp"]);
        Assert.Equal((byte)7, dataModel["ByteDataProp"]);
        Assert.Equal((byte)8, dataModel["NullableByteDataProp"]);
        Assert.Equal(9.0f, dataModel["FloatDataProp"]);
        Assert.Equal(10.0f, dataModel["NullableFloatDataProp"]);
        Assert.Equal(11.0, dataModel["DoubleDataProp"]);
        Assert.Equal(12.0, dataModel["NullableDoubleDataProp"]);
        Assert.Equal(13.99m, dataModel["DecimalDataProp"]);
        Assert.Equal(14.00m, dataModel["NullableDecimalDataProp"]);
        Assert.Equal(new DateTime(2021, 1, 1, 0, 0, 0), dataModel["DateTimeDataProp"]);
        Assert.Equal(new DateTime(2021, 1, 1, 0, 0, 0), dataModel["NullableDateTimeDataProp"]);
        Assert.Equal(new DateTimeOffset(2022, 1, 1, 0, 0, 0, TimeSpan.Zero), dataModel["DateTimeOffsetDataProp"]);
        Assert.Equal(new DateTimeOffset(2022, 1, 1, 0, 0, 0, TimeSpan.Zero), dataModel["NullableDateTimeOffsetDataProp"]);
        Assert.Equal(new Guid("11111111-1111-1111-1111-111111111111"), dataModel["GuidDataProp"]);
        Assert.Equal(new Guid("22222222-2222-2222-2222-222222222222"), dataModel["NullableGuidDataProp"]);
        Assert.Equal(s_taglist, dataModel["TagListDataProp"]);
        Assert.Equal(s_floatVector, ((ReadOnlyMemory<float>)dataModel["FloatVector"]!).ToArray());
        Assert.Equal(s_floatVector, ((ReadOnlyMemory<float>)dataModel["NullableFloatVector"]!)!.ToArray());
    }

    [Fact]
    public void MapFromStorageToDataModelMapsNullValues()
    {
        // Arrange
        var key = new Guid("55555555-5555-5555-5555-555555555555");
        var keyProperty = new VectorStoreKeyProperty("Key", typeof(Guid));

        var storageModel = new JsonObject
        {
            ["id"] = key,
            ["properties"] = new JsonObject
            {
                ["stringDataProp"] = null,
                ["nullableIntDataProp"] = null,
            },
            ["vectors"] = new JsonObject
            {
                ["nullableFloatVector"] = null
            }
        };

        var sut = new WeaviateMapper<Dictionary<string, object?>>("Collection", HasNamedVectors, s_model, s_jsonSerializerOptions);

        // Act
        var dataModel = sut.MapFromStorageToDataModel(storageModel, includeVectors: true);

        // Assert
        Assert.Equal(key, dataModel["Key"]);
        Assert.Null(dataModel["StringDataProp"]);
        Assert.Null(dataModel["NullableIntDataProp"]);
        Assert.Null(dataModel["NullableFloatVector"]);
    }

    [Fact]
    public void MapFromStorageToDataModelThrowsForMissingKey()
    {
        // Arrange
        var sut = new WeaviateMapper<Dictionary<string, object?>>("Collection", HasNamedVectors, s_model, s_jsonSerializerOptions);

        var storageModel = new JsonObject();

        // Act & Assert
        var exception = Assert.Throws<InvalidOperationException>(
            () => sut.MapFromStorageToDataModel(storageModel, includeVectors: true));
    }

    [Fact]
    public void MapFromDataToStorageModelSkipsMissingProperties()
    {
        // Arrange
        var recordDefinition = new VectorStoreCollectionDefinition
        {
            Properties =
            [
                new VectorStoreKeyProperty("Key", typeof(Guid)),
                new VectorStoreDataProperty("StringDataProp", typeof(string)),
                new VectorStoreDataProperty("NullableIntDataProp", typeof(int?)),
                new VectorStoreVectorProperty("FloatVector", typeof(ReadOnlyMemory<float>), 10)
            ]
        };

        var model = new WeaviateModelBuilder(HasNamedVectors).BuildDynamic(recordDefinition, defaultEmbeddingGenerator: null, s_jsonSerializerOptions);

        var key = new Guid("55555555-5555-5555-5555-555555555555");

        var record = new Dictionary<string, object?> { ["Key"] = key };
        var sut = new WeaviateMapper<Dictionary<string, object?>>("Collection", HasNamedVectors, model, s_jsonSerializerOptions);

        // Act
        var storageModel = sut.MapFromDataToStorageModel(record, recordIndex: 0, generatedEmbeddings: null);

        // Assert
        Assert.Equal(key, (Guid?)storageModel["id"]);
        Assert.False(storageModel.ContainsKey("StringDataProp"));
        Assert.False(storageModel.ContainsKey("FloatVector"));
    }

    [Fact]
    public void MapFromStorageToDataModelSkipsMissingProperties()
    {
        // Arrange
        var recordDefinition = new VectorStoreCollectionDefinition
        {
            Properties =
            [
                new VectorStoreKeyProperty("Key", typeof(Guid)),
                new VectorStoreDataProperty("StringDataProp", typeof(string)),
                new VectorStoreDataProperty("NullableIntDataProp", typeof(int?)),
                new VectorStoreVectorProperty("FloatVector", typeof(ReadOnlyMemory<float>), 10)
            ]
        };

        var model = new WeaviateModelBuilder(HasNamedVectors).BuildDynamic(recordDefinition, defaultEmbeddingGenerator: null, s_jsonSerializerOptions);

        var key = new Guid("55555555-5555-5555-5555-555555555555");

        var sut = new WeaviateMapper<Dictionary<string, object?>>("Collection", HasNamedVectors, model, s_jsonSerializerOptions);

        var storageModel = new JsonObject
        {
            ["id"] = key
        };

        // Act
        var dataModel = sut.MapFromStorageToDataModel(storageModel, includeVectors: true);

        // Assert
        Assert.Equal(key, dataModel["Key"]);
        Assert.False(dataModel.ContainsKey("StringDataProp"));
        Assert.False(dataModel.ContainsKey("FloatVector"));
    }

    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public void MapFromDataToStorageModelMapsNamedVectorsCorrectly(bool hasNamedVectors)
    {
        // Arrange
        var recordDefinition = new VectorStoreCollectionDefinition
        {
            Properties =
            [
                new VectorStoreKeyProperty("Key", typeof(Guid)),
                new VectorStoreVectorProperty("FloatVector", typeof(ReadOnlyMemory<float>), 4)
            ]
        };

        var model = new WeaviateModelBuilder(hasNamedVectors).BuildDynamic(recordDefinition, defaultEmbeddingGenerator: null, s_jsonSerializerOptions);

        var key = new Guid("55555555-5555-5555-5555-555555555555");

        var record = new Dictionary<string, object?> { ["Key"] = key, ["FloatVector"] = new ReadOnlyMemory<float>(s_floatVector) };
        var sut = new WeaviateMapper<Dictionary<string, object?>>("Collection", hasNamedVectors, model, s_jsonSerializerOptions);

        // Act
        var storageModel = sut.MapFromDataToStorageModel(record, recordIndex: 0, generatedEmbeddings: null);

        // Assert
        var vectorProperty = hasNamedVectors ? storageModel["vectors"]!["floatVector"] : storageModel["vector"];

        Assert.Equal(key, (Guid?)storageModel["id"]);
        Assert.Equal(s_floatVector, vectorProperty!.AsArray().GetValues<float>().ToArray());
    }

    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public void MapFromStorageToDataModelMapsNamedVectorsCorrectly(bool hasNamedVectors)
    {
        // Arrange
        var recordDefinition = new VectorStoreCollectionDefinition
        {
            Properties =
            [
                new VectorStoreKeyProperty("Key", typeof(Guid)),
                new VectorStoreVectorProperty("FloatVector", typeof(ReadOnlyMemory<float>), 4)
            ]
        };

        var model = new WeaviateModelBuilder(hasNamedVectors).BuildDynamic(recordDefinition, defaultEmbeddingGenerator: null, s_jsonSerializerOptions);

        var key = new Guid("55555555-5555-5555-5555-555555555555");

        var sut = new WeaviateMapper<Dictionary<string, object?>>("Collection", hasNamedVectors, model, s_jsonSerializerOptions);

        var storageModel = new JsonObject { ["id"] = key };

        var vector = new JsonArray(s_floatVector.Select(l => (JsonValue)l).ToArray());

        if (hasNamedVectors)
        {
            storageModel["vectors"] = new JsonObject
            {
                ["floatVector"] = vector
            };
        }
        else
        {
            storageModel["vector"] = vector;
        }

        // Act
        var dataModel = sut.MapFromStorageToDataModel(storageModel, includeVectors: true);

        // Assert
        Assert.Equal(key, dataModel["Key"]);
        Assert.Equal(s_floatVector, ((ReadOnlyMemory<float>)dataModel["FloatVector"]!).ToArray());
    }
}
