﻿// Copyright (c) Microsoft. All rights reserved.

using System.Linq;
using System.Threading.Tasks;
using Microsoft.SemanticKernel.Connectors.Redis;
using Xunit;
using Xunit.Abstractions;

namespace SemanticKernel.IntegrationTests.Connectors.Memory.Redis;

/// <summary>
/// Contains tests for the <see cref="RedisVectorStore"/> class.
/// </summary>
/// <param name="output">Used to write to the test output stream.</param>
/// <param name="fixture">The test fixture.</param>
[Collection("RedisVectorStoreCollection")]
public class RedisVectorStoreTests(ITestOutputHelper output, RedisVectorStoreFixture fixture)
{
<<<<<<< HEAD
    // If null, all tests will be enabled
    private const string SkipReason = "Requires Redis docker container up and running";

    [Fact(Skip = SkipReason)]
=======
    [Fact]
>>>>>>> 46c3c89f5c5dbc355794ac231b509e142f4fb770
    public async Task ItCanGetAListOfExistingCollectionNamesAsync()
    {
        // Arrange
        var sut = new RedisVectorStore(fixture.Database);

        // Act
        var collectionNames = await sut.ListCollectionNamesAsync().ToListAsync();

        // Assert
        Assert.Equal(2, collectionNames.Count);
        Assert.Contains("jsonhotels", collectionNames);
        Assert.Contains("hashhotels", collectionNames);

        // Output
        output.WriteLine(string.Join(",", collectionNames));
    }
}
