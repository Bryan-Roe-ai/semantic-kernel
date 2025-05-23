// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json.Serialization;
using Microsoft.Extensions.VectorData;
using Microsoft.Extensions.VectorData.ConnectorSupport;
using Microsoft.SemanticKernel.Connectors.Qdrant;
using Qdrant.Client.Grpc;
using Xunit;

namespace SemanticKernel.Connectors.Qdrant.UnitTests;

/// <summary>
/// Contains tests for the <see cref="QdrantVectorStoreRecordMapper{TConsumerDataModel}"/> class.
/// </summary>
public class QdrantVectorStoreRecordMapperTests
{
    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public void MapsSinglePropsFromDataToStorageModelWithUlong(bool hasNamedVectors)
    {
        // Arrange.
        var definition = CreateSinglePropsVectorStoreRecordDefinition(typeof(ulong));
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
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<ulong>>(definition, hasNamedVectors, s_singlePropsModelStorageNamesMap);
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
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<ulong>>(definition, hasNamedVectors, s_singlePropsModelStorageNamesMap);
=======
        var reader = new VectorStoreRecordPropertyReader(typeof(SinglePropsModel<ulong>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<ulong>>(reader, hasNamedVectors);
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
        var reader = new VectorStoreRecordPropertyReader(typeof(SinglePropsModel<ulong>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<ulong>>(reader, hasNamedVectors);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
        var model = new VectorStoreRecordModelBuilder(QdrantVectorStoreRecordFieldMapping.GetModelBuildOptions(hasNamedVectors))
            .Build(typeof(SinglePropsModel<ulong>), definition, defaultEmbeddingGenerator: null);
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<ulong>>(model, hasNamedVectors);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Act.
        var actual = sut.MapFromDataToStorageModel(CreateSinglePropsModel<ulong>(5ul), recordIndex: 0, generatedEmbeddings: null);

        // Assert.
        Assert.NotNull(actual);
        Assert.Equal(5ul, actual.Id.Num);
        Assert.Single(actual.Payload);
        Assert.Equal("data value", actual.Payload["data"].StringValue);

        if (hasNamedVectors)
        {
            Assert.Equal(new float[] { 1, 2, 3, 4 }, actual.Vectors.Vectors_.Vectors["vector"].Data.ToArray());
        }
        else
        {
            Assert.Equal(new float[] { 1, 2, 3, 4 }, actual.Vectors.Vector.Data.ToArray());
        }
    }

    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public void MapsSinglePropsFromDataToStorageModelWithGuid(bool hasNamedVectors)
    {
        // Arrange.
        var definition = CreateSinglePropsVectorStoreRecordDefinition(typeof(Guid));
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
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<Guid>>(definition, hasNamedVectors, s_singlePropsModelStorageNamesMap);
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
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<Guid>>(definition, hasNamedVectors, s_singlePropsModelStorageNamesMap);
=======
        var reader = new VectorStoreRecordPropertyReader(typeof(SinglePropsModel<Guid>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<Guid>>(reader, hasNamedVectors);
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
        var reader = new VectorStoreRecordPropertyReader(typeof(SinglePropsModel<Guid>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<Guid>>(reader, hasNamedVectors);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
        var reader = new VectorStoreRecordPropertyReader(typeof(SinglePropsModel<Guid>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<Guid>>(reader, hasNamedVectors);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
=======
        var model = new VectorStoreRecordModelBuilder(QdrantVectorStoreRecordFieldMapping.GetModelBuildOptions(hasNamedVectors))
            .Build(typeof(SinglePropsModel<Guid>), definition, defaultEmbeddingGenerator: null);
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<Guid>>(model, hasNamedVectors);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Act.
        var actual = sut.MapFromDataToStorageModel(CreateSinglePropsModel<Guid>(Guid.Parse("11111111-1111-1111-1111-111111111111")), recordIndex: 0, generatedEmbeddings: null);

        // Assert.
        Assert.NotNull(actual);
        Assert.Equal(Guid.Parse("11111111-1111-1111-1111-111111111111"), Guid.Parse(actual.Id.Uuid));
        Assert.Single(actual.Payload);
        Assert.Equal("data value", actual.Payload["data"].StringValue);
    }

    [Theory]
    [InlineData(true, true)]
    [InlineData(true, false)]
    [InlineData(false, true)]
    [InlineData(false, false)]
    public void MapsSinglePropsFromStorageToDataModelWithUlong(bool hasNamedVectors, bool includeVectors)
    {
        // Arrange.
        var definition = CreateSinglePropsVectorStoreRecordDefinition(typeof(ulong));
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
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<ulong>>(definition, hasNamedVectors, s_singlePropsModelStorageNamesMap);
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
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<ulong>>(definition, hasNamedVectors, s_singlePropsModelStorageNamesMap);
=======
        var reader = new VectorStoreRecordPropertyReader(typeof(SinglePropsModel<ulong>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<ulong>>(reader, hasNamedVectors);
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
        var reader = new VectorStoreRecordPropertyReader(typeof(SinglePropsModel<ulong>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<ulong>>(reader, hasNamedVectors);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
        var model = new VectorStoreRecordModelBuilder(QdrantVectorStoreRecordFieldMapping.GetModelBuildOptions(hasNamedVectors))
            .Build(typeof(SinglePropsModel<ulong>), definition, defaultEmbeddingGenerator: null);
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<ulong>>(model, hasNamedVectors);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Act.
        var point = CreateSinglePropsPointStruct(5, hasNamedVectors);
        var actual = sut.MapFromStorageToDataModel(point.Id, point.Payload, point.Vectors, new() { IncludeVectors = includeVectors });

        // Assert.
        Assert.NotNull(actual);
        Assert.Equal(5ul, actual.Key);
        Assert.Equal("data value", actual.Data);

        if (includeVectors)
        {
            Assert.Equal(new float[] { 1, 2, 3, 4 }, actual.Vector!.Value.ToArray());
        }
        else
        {
            Assert.Null(actual.Vector);
        }
    }

    [Theory]
    [InlineData(true, true)]
    [InlineData(true, false)]
    [InlineData(false, true)]
    [InlineData(false, false)]
    public void MapsSinglePropsFromStorageToDataModelWithGuid(bool hasNamedVectors, bool includeVectors)
    {
        // Arrange.
        var definition = CreateSinglePropsVectorStoreRecordDefinition(typeof(Guid));
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
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<Guid>>(definition, hasNamedVectors, s_singlePropsModelStorageNamesMap);
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
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<Guid>>(definition, hasNamedVectors, s_singlePropsModelStorageNamesMap);
=======
        var reader = new VectorStoreRecordPropertyReader(typeof(SinglePropsModel<Guid>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<Guid>>(reader, hasNamedVectors);
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
        var reader = new VectorStoreRecordPropertyReader(typeof(SinglePropsModel<Guid>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<Guid>>(reader, hasNamedVectors);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
        var reader = new VectorStoreRecordPropertyReader(typeof(SinglePropsModel<Guid>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<Guid>>(reader, hasNamedVectors);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
=======
        var model = new VectorStoreRecordModelBuilder(QdrantVectorStoreRecordFieldMapping.GetModelBuildOptions(hasNamedVectors))
            .Build(typeof(SinglePropsModel<Guid>), definition, defaultEmbeddingGenerator: null);
        var sut = new QdrantVectorStoreRecordMapper<SinglePropsModel<Guid>>(model, hasNamedVectors);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Act.
        var point = CreateSinglePropsPointStruct(Guid.Parse("11111111-1111-1111-1111-111111111111"), hasNamedVectors);
        var actual = sut.MapFromStorageToDataModel(point.Id, point.Payload, point.Vectors, new() { IncludeVectors = includeVectors });

        // Assert.
        Assert.NotNull(actual);
        Assert.Equal(Guid.Parse("11111111-1111-1111-1111-111111111111"), actual.Key);
        Assert.Equal("data value", actual.Data);

        if (includeVectors)
        {
            Assert.Equal(new float[] { 1, 2, 3, 4 }, actual.Vector!.Value.ToArray());
        }
        else
        {
            Assert.Null(actual.Vector);
        }
    }

    [Fact]
    public void MapsMultiPropsFromDataToStorageModelWithUlong()
    {
        // Arrange.
        var definition = CreateMultiPropsVectorStoreRecordDefinition(typeof(ulong));
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
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<ulong>>(definition, true, s_multiPropsModelStorageNamesMap);
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
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<ulong>>(definition, true, s_multiPropsModelStorageNamesMap);
=======
        var reader = new VectorStoreRecordPropertyReader(typeof(MultiPropsModel<ulong>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<ulong>>(reader, true);
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
        var reader = new VectorStoreRecordPropertyReader(typeof(MultiPropsModel<ulong>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<ulong>>(reader, true);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
        var model = new VectorStoreRecordModelBuilder(QdrantVectorStoreRecordFieldMapping.GetModelBuildOptions(hasNamedVectors: true))
            .Build(typeof(MultiPropsModel<ulong>), definition, defaultEmbeddingGenerator: null);

        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<ulong>>(model, hasNamedVectors: true);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Act.
        var actual = sut.MapFromDataToStorageModel(CreateMultiPropsModel<ulong>(5ul), recordIndex: 0, generatedEmbeddings: null);

        // Assert.
        Assert.NotNull(actual);
        Assert.Equal(5ul, actual.Id.Num);
        Assert.Equal(8, actual.Payload.Count);
        Assert.Equal("data 1", actual.Payload["dataString"].StringValue);
        Assert.Equal(5, actual.Payload["dataInt"].IntegerValue);
        Assert.Equal(5, actual.Payload["dataLong"].IntegerValue);
        Assert.Equal(5.5f, actual.Payload["dataFloat"].DoubleValue);
        Assert.Equal(5.5d, actual.Payload["dataDouble"].DoubleValue);
        Assert.True(actual.Payload["dataBool"].BoolValue);
        Assert.Equal("2025-02-10T05:10:15.0000000+01:00", actual.Payload["dataDateTimeOffset"].StringValue);
        Assert.Equal(new int[] { 1, 2, 3, 4 }, actual.Payload["dataArrayInt"].ListValue.Values.Select(x => (int)x.IntegerValue).ToArray());
        Assert.Equal(new float[] { 1, 2, 3, 4 }, actual.Vectors.Vectors_.Vectors["vector1"].Data.ToArray());
        Assert.Equal(new float[] { 5, 6, 7, 8 }, actual.Vectors.Vectors_.Vectors["vector2"].Data.ToArray());
    }

    [Fact]
    public void MapsMultiPropsFromDataToStorageModelWithGuid()
    {
        // Arrange.
        var definition = CreateMultiPropsVectorStoreRecordDefinition(typeof(Guid));
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
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<Guid>>(definition, true, s_multiPropsModelStorageNamesMap);
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
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<Guid>>(definition, true, s_multiPropsModelStorageNamesMap);
=======
        var reader = new VectorStoreRecordPropertyReader(typeof(MultiPropsModel<Guid>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<Guid>>(reader, true);
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
        var reader = new VectorStoreRecordPropertyReader(typeof(MultiPropsModel<Guid>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<Guid>>(reader, true);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
        var model = new VectorStoreRecordModelBuilder(QdrantVectorStoreRecordFieldMapping.GetModelBuildOptions(hasNamedVectors: true))
            .Build(typeof(MultiPropsModel<Guid>), definition, defaultEmbeddingGenerator: null);
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<Guid>>(model, hasNamedVectors: true);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Act.
        var actual = sut.MapFromDataToStorageModel(CreateMultiPropsModel<Guid>(Guid.Parse("11111111-1111-1111-1111-111111111111")), recordIndex: 0, generatedEmbeddings: null);

        // Assert.
        Assert.NotNull(actual);
        Assert.Equal(Guid.Parse("11111111-1111-1111-1111-111111111111"), Guid.Parse(actual.Id.Uuid));
        Assert.Equal(8, actual.Payload.Count);
        Assert.Equal("data 1", actual.Payload["dataString"].StringValue);
        Assert.Equal(5, actual.Payload["dataInt"].IntegerValue);
        Assert.Equal(5, actual.Payload["dataLong"].IntegerValue);
        Assert.Equal(5.5f, actual.Payload["dataFloat"].DoubleValue);
        Assert.Equal(5.5d, actual.Payload["dataDouble"].DoubleValue);
        Assert.True(actual.Payload["dataBool"].BoolValue);
        Assert.Equal("2025-02-10T05:10:15.0000000+01:00", actual.Payload["dataDateTimeOffset"].StringValue);
        Assert.Equal(new int[] { 1, 2, 3, 4 }, actual.Payload["dataArrayInt"].ListValue.Values.Select(x => (int)x.IntegerValue).ToArray());
        Assert.Equal(new float[] { 1, 2, 3, 4 }, actual.Vectors.Vectors_.Vectors["vector1"].Data.ToArray());
        Assert.Equal(new float[] { 5, 6, 7, 8 }, actual.Vectors.Vectors_.Vectors["vector2"].Data.ToArray());
    }

    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public void MapsMultiPropsFromStorageToDataModelWithUlong(bool includeVectors)
    {
        // Arrange.
        var definition = CreateMultiPropsVectorStoreRecordDefinition(typeof(ulong));
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
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<ulong>>(definition, true, s_multiPropsModelStorageNamesMap);
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
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<ulong>>(definition, true, s_multiPropsModelStorageNamesMap);
=======
        var reader = new VectorStoreRecordPropertyReader(typeof(MultiPropsModel<ulong>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<ulong>>(reader, true);
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
        var reader = new VectorStoreRecordPropertyReader(typeof(MultiPropsModel<ulong>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<ulong>>(reader, true);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
        var reader = new VectorStoreRecordPropertyReader(typeof(MultiPropsModel<ulong>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<ulong>>(reader, true);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
=======
        var model = new VectorStoreRecordModelBuilder(QdrantVectorStoreRecordFieldMapping.GetModelBuildOptions(hasNamedVectors: true))
            .Build(typeof(MultiPropsModel<ulong>), definition, defaultEmbeddingGenerator: null);
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<ulong>>(model, hasNamedVectors: true);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Act.
        var point = CreateMultiPropsPointStruct(5);
        var actual = sut.MapFromStorageToDataModel(point.Id, point.Payload, point.Vectors, new() { IncludeVectors = includeVectors });

        // Assert.
        Assert.NotNull(actual);
        Assert.Equal(5ul, actual.Key);
        Assert.Equal("data 1", actual.DataString);
        Assert.Equal(5, actual.DataInt);
        Assert.Equal(5L, actual.DataLong);
        Assert.Equal(5.5f, actual.DataFloat);
        Assert.Equal(5.5d, actual.DataDouble);
        Assert.True(actual.DataBool);
        Assert.Equal(new DateTimeOffset(2025, 2, 10, 5, 10, 15, TimeSpan.FromHours(1)), actual.DataDateTimeOffset);
        Assert.Equal(new int[] { 1, 2, 3, 4 }, actual.DataArrayInt);

        if (includeVectors)
        {
            Assert.Equal(new float[] { 1, 2, 3, 4 }, actual.Vector1!.Value.ToArray());
            Assert.Equal(new float[] { 5, 6, 7, 8 }, actual.Vector2!.Value.ToArray());
        }
        else
        {
            Assert.Null(actual.Vector1);
            Assert.Null(actual.Vector2);
        }
    }

    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public void MapsMultiPropsFromStorageToDataModelWithGuid(bool includeVectors)
    {
        // Arrange.
        var definition = CreateMultiPropsVectorStoreRecordDefinition(typeof(Guid));
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
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<Guid>>(definition, true, s_multiPropsModelStorageNamesMap);
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
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<Guid>>(definition, true, s_multiPropsModelStorageNamesMap);
=======
        var reader = new VectorStoreRecordPropertyReader(typeof(MultiPropsModel<Guid>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<Guid>>(reader, true);
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
        var reader = new VectorStoreRecordPropertyReader(typeof(MultiPropsModel<Guid>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<Guid>>(reader, true);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
        var reader = new VectorStoreRecordPropertyReader(typeof(MultiPropsModel<Guid>), definition, null);
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<Guid>>(reader, true);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
=======
        var model = new VectorStoreRecordModelBuilder(QdrantVectorStoreRecordFieldMapping.GetModelBuildOptions(hasNamedVectors: true))
            .Build(typeof(MultiPropsModel<Guid>), definition, defaultEmbeddingGenerator: null);
        var sut = new QdrantVectorStoreRecordMapper<MultiPropsModel<Guid>>(model, hasNamedVectors: true);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Act.
        var point = CreateMultiPropsPointStruct(Guid.Parse("11111111-1111-1111-1111-111111111111"));
        var actual = sut.MapFromStorageToDataModel(point.Id, point.Payload, point.Vectors, new() { IncludeVectors = includeVectors });

        // Assert.
        Assert.NotNull(actual);
        Assert.Equal(Guid.Parse("11111111-1111-1111-1111-111111111111"), actual.Key);
        Assert.Equal("data 1", actual.DataString);
        Assert.Equal(5, actual.DataInt);
        Assert.Equal(5L, actual.DataLong);
        Assert.Equal(5.5f, actual.DataFloat);
        Assert.Equal(5.5d, actual.DataDouble);
        Assert.True(actual.DataBool);
        Assert.Equal(new DateTimeOffset(2025, 2, 10, 5, 10, 15, TimeSpan.FromHours(1)), actual.DataDateTimeOffset);
        Assert.Equal(new int[] { 1, 2, 3, 4 }, actual.DataArrayInt);

        if (includeVectors)
        {
            Assert.Equal(new float[] { 1, 2, 3, 4 }, actual.Vector1!.Value.ToArray());
            Assert.Equal(new float[] { 5, 6, 7, 8 }, actual.Vector2!.Value.ToArray());
        }
        else
        {
            Assert.Null(actual.Vector1);
            Assert.Null(actual.Vector2);
        }
    }

    private static SinglePropsModel<TKey> CreateSinglePropsModel<TKey>(TKey key)
    {
        return new SinglePropsModel<TKey>
        {
            Key = key,
            Data = "data value",
            Vector = new float[] { 1, 2, 3, 4 },
            NotAnnotated = "notAnnotated",
        };
    }

    private static MultiPropsModel<TKey> CreateMultiPropsModel<TKey>(TKey key)
    {
        return new MultiPropsModel<TKey>
        {
            Key = key,
            DataString = "data 1",
            DataInt = 5,
            DataLong = 5L,
            DataFloat = 5.5f,
            DataDouble = 5.5d,
            DataBool = true,
            DataDateTimeOffset = new DateTimeOffset(2025, 2, 10, 5, 10, 15, TimeSpan.FromHours(1)),
            DataArrayInt = new List<int> { 1, 2, 3, 4 },
            Vector1 = new float[] { 1, 2, 3, 4 },
            Vector2 = new float[] { 5, 6, 7, 8 },
            NotAnnotated = "notAnnotated",
        };
    }

    private static RetrievedPoint CreateSinglePropsPointStruct(ulong id, bool hasNamedVectors)
    {
        var pointStruct = new RetrievedPoint();
        pointStruct.Id = new PointId() { Num = id };
        AddDataToSinglePropsPointStruct(pointStruct, hasNamedVectors);
        return pointStruct;
    }

    private static RetrievedPoint CreateSinglePropsPointStruct(Guid id, bool hasNamedVectors)
    {
        var pointStruct = new RetrievedPoint();
        pointStruct.Id = new PointId() { Uuid = id.ToString() };
        AddDataToSinglePropsPointStruct(pointStruct, hasNamedVectors);
        return pointStruct;
    }

    private static void AddDataToSinglePropsPointStruct(RetrievedPoint pointStruct, bool hasNamedVectors)
    {
        var responseVector = VectorOutput.Parser.ParseJson("{ \"data\": [1, 2, 3, 4] }");

        pointStruct.Payload.Add("data", "data value");

        if (hasNamedVectors)
        {
            var namedVectors = new NamedVectorsOutput();
            namedVectors.Vectors.Add("vector", responseVector);
            pointStruct.Vectors = new VectorsOutput() { Vectors = namedVectors };
        }
        else
        {
            pointStruct.Vectors = new VectorsOutput() { Vector = responseVector };
        }
    }

    private static RetrievedPoint CreateMultiPropsPointStruct(ulong id)
    {
        var pointStruct = new RetrievedPoint();
        pointStruct.Id = new PointId() { Num = id };
        AddDataToMultiPropsPointStruct(pointStruct);
        return pointStruct;
    }

    private static RetrievedPoint CreateMultiPropsPointStruct(Guid id)
    {
        var pointStruct = new RetrievedPoint();
        pointStruct.Id = new PointId() { Uuid = id.ToString() };
        AddDataToMultiPropsPointStruct(pointStruct);
        return pointStruct;
    }

    private static void AddDataToMultiPropsPointStruct(RetrievedPoint pointStruct)
    {
        pointStruct.Payload.Add("dataString", "data 1");
        pointStruct.Payload.Add("dataInt", 5);
        pointStruct.Payload.Add("dataLong", 5L);
        pointStruct.Payload.Add("dataFloat", 5.5f);
        pointStruct.Payload.Add("dataDouble", 5.5d);
        pointStruct.Payload.Add("dataBool", true);
        pointStruct.Payload.Add("dataDateTimeOffset", "2025-02-10T05:10:15.0000000+01:00");

        var dataIntArray = new ListValue();
        dataIntArray.Values.Add(1);
        dataIntArray.Values.Add(2);
        dataIntArray.Values.Add(3);
        dataIntArray.Values.Add(4);
        pointStruct.Payload.Add("dataArrayInt", new Value { ListValue = dataIntArray });

        var responseVector1 = VectorOutput.Parser.ParseJson("{ \"data\": [1, 2, 3, 4] }");
        var responseVector2 = VectorOutput.Parser.ParseJson("{ \"data\": [5, 6, 7, 8] }");

        var namedVectors = new NamedVectorsOutput();
        namedVectors.Vectors.Add("vector1", responseVector1);
        namedVectors.Vectors.Add("vector2", responseVector2);
        pointStruct.Vectors = new VectorsOutput() { Vectors = namedVectors };
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
    private static readonly Dictionary<string, string> s_singlePropsModelStorageNamesMap = new()
    {
        { "Key", "key" },
        { "Data", "data" },
        { "Vector", "vector" },
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
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
    private static VectorStoreRecordDefinition CreateSinglePropsVectorStoreRecordDefinition(Type keyType) => new()
    {
        Properties = new List<VectorStoreRecordProperty>
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
            new VectorStoreRecordKeyProperty("Key", keyType),
            new VectorStoreRecordDataProperty("Data", typeof(string)),
            new VectorStoreRecordVectorProperty("Vector", typeof(ReadOnlyMemory<float>)),
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
            new VectorStoreRecordKeyProperty("Key", keyType),
            new VectorStoreRecordDataProperty("Data", typeof(string)),
            new VectorStoreRecordVectorProperty("Vector", typeof(ReadOnlyMemory<float>)),
=======
            new VectorStoreRecordKeyProperty("Key", keyType) { StoragePropertyName = "key" },
            new VectorStoreRecordDataProperty("Data", typeof(string)) { StoragePropertyName = "data" },
<<<<<<< HEAD
            new VectorStoreRecordVectorProperty("Vector", typeof(ReadOnlyMemory<float>)) { StoragePropertyName = "vector" },
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
            new VectorStoreRecordKeyProperty("Key", keyType) { StoragePropertyName = "key" },
            new VectorStoreRecordDataProperty("Data", typeof(string)) { StoragePropertyName = "data" },
            new VectorStoreRecordVectorProperty("Vector", typeof(ReadOnlyMemory<float>)) { StoragePropertyName = "vector" },
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
            new VectorStoreRecordVectorProperty("Vector", typeof(ReadOnlyMemory<float>), 10) { StoragePropertyName = "vector" },
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        },
    };

    private sealed class SinglePropsModel<TKey>
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
        [VectorStoreRecordKey]
        public TKey? Key { get; set; } = default;

        [VectorStoreRecordData]
        public string Data { get; set; } = string.Empty;

        [VectorStoreRecordVector]
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
        [VectorStoreRecordKey(StoragePropertyName = "key")]
        public TKey? Key { get; set; } = default;

        [VectorStoreRecordData(StoragePropertyName = "data")]
        public string Data { get; set; } = string.Empty;

<<<<<<< HEAD
        [VectorStoreRecordVector(StoragePropertyName = "vector")]
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
        [VectorStoreRecordVector(10, StoragePropertyName = "vector")]
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        public ReadOnlyMemory<float>? Vector { get; set; }

        public string NotAnnotated { get; set; } = string.Empty;
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
    private static readonly Dictionary<string, string> s_multiPropsModelStorageNamesMap = new()
    {
        { "Key", "key" },
        { "DataString", "dataString" },
        { "DataInt", "dataInt" },
        { "DataLong", "dataLong" },
        { "DataFloat", "dataFloat" },
        { "DataDouble", "dataDouble" },
        { "DataBool", "dataBool" },
        { "DataArrayInt", "dataArrayInt" },
        { "Vector1", "vector1" },
        { "Vector2", "vector2" },
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
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> Stashed changes
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
<<<<<<< div
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
    private static VectorStoreRecordDefinition CreateMultiPropsVectorStoreRecordDefinition(Type keyType) => new()
    {
        Properties = new List<VectorStoreRecordProperty>
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
            new VectorStoreRecordKeyProperty("Key", keyType),
            new VectorStoreRecordDataProperty("DataString", typeof(string)),
            new VectorStoreRecordDataProperty("DataInt", typeof(int)),
            new VectorStoreRecordDataProperty("DataLong", typeof(long)),
            new VectorStoreRecordDataProperty("DataFloat", typeof(float)),
            new VectorStoreRecordDataProperty("DataDouble", typeof(double)),
            new VectorStoreRecordDataProperty("DataBool", typeof(bool)),
            new VectorStoreRecordDataProperty("DataArrayInt", typeof(List<int>)),
            new VectorStoreRecordVectorProperty("Vector1", typeof(ReadOnlyMemory<float>)),
            new VectorStoreRecordVectorProperty("Vector2", typeof(ReadOnlyMemory<float>)),
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
            new VectorStoreRecordKeyProperty("Key", keyType) { StoragePropertyName = "key" },
            new VectorStoreRecordDataProperty("DataString", typeof(string)) { StoragePropertyName = "dataString" },
            new VectorStoreRecordDataProperty("DataInt", typeof(int)) { StoragePropertyName = "dataInt" },
            new VectorStoreRecordDataProperty("DataLong", typeof(long)) { StoragePropertyName = "dataLong" },
            new VectorStoreRecordDataProperty("DataFloat", typeof(float)) { StoragePropertyName = "dataFloat" },
            new VectorStoreRecordDataProperty("DataDouble", typeof(double)) { StoragePropertyName = "dataDouble" },
            new VectorStoreRecordDataProperty("DataBool", typeof(bool)) { StoragePropertyName = "dataBool" },
            new VectorStoreRecordDataProperty("DataDateTimeOffset", typeof(DateTimeOffset)) { StoragePropertyName = "dataDateTimeOffset" },
            new VectorStoreRecordDataProperty("DataArrayInt", typeof(List<int>)) { StoragePropertyName = "dataArrayInt" },
<<<<<<< HEAD
            new VectorStoreRecordVectorProperty("Vector1", typeof(ReadOnlyMemory<float>)) { StoragePropertyName = "vector1" },
            new VectorStoreRecordVectorProperty("Vector2", typeof(ReadOnlyMemory<float>)) { StoragePropertyName = "vector2" },
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
            new VectorStoreRecordVectorProperty("Vector1", typeof(ReadOnlyMemory<float>), 10) { StoragePropertyName = "vector1" },
            new VectorStoreRecordVectorProperty("Vector2", typeof(ReadOnlyMemory<float>), 10) { StoragePropertyName = "vector2" },
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        },
    };

    private sealed class MultiPropsModel<TKey>
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
        [VectorStoreRecordKey]
        public TKey? Key { get; set; } = default;

        [VectorStoreRecordData]
        public string DataString { get; set; } = string.Empty;

        [JsonPropertyName("data_int_json")]
        [VectorStoreRecordData]
        public int DataInt { get; set; } = 0;

        [VectorStoreRecordData]
        public long DataLong { get; set; } = 0;

        [VectorStoreRecordData]
        public float DataFloat { get; set; } = 0;

        [VectorStoreRecordData]
        public double DataDouble { get; set; } = 0;

        [VectorStoreRecordData]
        public bool DataBool { get; set; } = false;

        [VectorStoreRecordData]
        public List<int>? DataArrayInt { get; set; }

        [VectorStoreRecordVector]
        public ReadOnlyMemory<float>? Vector1 { get; set; }

        [VectorStoreRecordVector]
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
        [VectorStoreRecordKey(StoragePropertyName = "key")]
        public TKey? Key { get; set; } = default;

        [VectorStoreRecordData(StoragePropertyName = "dataString")]
        public string DataString { get; set; } = string.Empty;

        [JsonPropertyName("data_int_json")]
        [VectorStoreRecordData(StoragePropertyName = "dataInt")]
        public int DataInt { get; set; } = 0;

        [VectorStoreRecordData(StoragePropertyName = "dataLong")]
        public long DataLong { get; set; } = 0;

        [VectorStoreRecordData(StoragePropertyName = "dataFloat")]
        public float DataFloat { get; set; } = 0;

        [VectorStoreRecordData(StoragePropertyName = "dataDouble")]
        public double DataDouble { get; set; } = 0;

        [VectorStoreRecordData(StoragePropertyName = "dataBool")]
        public bool DataBool { get; set; } = false;

        [VectorStoreRecordData(StoragePropertyName = "dataDateTimeOffset")]
        public DateTimeOffset DataDateTimeOffset { get; set; }

        [VectorStoreRecordData(StoragePropertyName = "dataArrayInt")]
        public List<int>? DataArrayInt { get; set; }

        [VectorStoreRecordVector(10, StoragePropertyName = "vector1")]
        public ReadOnlyMemory<float>? Vector1 { get; set; }

<<<<<<< HEAD
        [VectorStoreRecordVector(StoragePropertyName = "vector2")]
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
        [VectorStoreRecordVector(10, StoragePropertyName = "vector2")]
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        public ReadOnlyMemory<float>? Vector2 { get; set; }

        public string NotAnnotated { get; set; } = string.Empty;
    }
}
