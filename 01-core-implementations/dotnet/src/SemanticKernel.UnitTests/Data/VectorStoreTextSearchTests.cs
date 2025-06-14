// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.SemanticKernel.Connectors.InMemory;
using Microsoft.SemanticKernel.Data;
using Microsoft.SemanticKernel.Embeddings;
using Xunit;

namespace SemanticKernel.UnitTests.Data;
public class VectorStoreTextSearchTests : VectorStoreTextSearchTestBase
{
#pragma warning disable CS0618 // VectorStoreTextSearch with ITextEmbeddingGenerationService is obsolete
    [Fact]
    public void CanCreateVectorStoreTextSearchWithEmbeddingGenerationService()
    {
        // Arrange.
        using var vectorStore = new InMemoryVectorStore();
        var vectorSearch = vectorStore.GetCollection<Guid, DataModelWithRawEmbedding>("records");
        var stringMapper = new DataModelTextSearchStringMapper();
        var resultMapper = new DataModelTextSearchResultMapper();
        using var embeddingGenerationService = new MockTextEmbeddingGenerator();

        // Act.
        var sut = new VectorStoreTextSearch<DataModelWithRawEmbedding>(vectorSearch, (ITextEmbeddingGenerationService)embeddingGenerationService, stringMapper, resultMapper);

        // Assert.
        Assert.NotNull(sut);
    }
#pragma warning restore CS0618

    [Fact]
    public void CanCreateVectorStoreTextSearchWithIVectorSearch()
    {
        // Arrange.
        using var vectorStore = new InMemoryVectorStore(new() { EmbeddingGenerator = new MockTextEmbeddingGenerator() });
        var vectorSearch = vectorStore.GetCollection<Guid, DataModel>("records");
        var stringMapper = new DataModelTextSearchStringMapper();
        var resultMapper = new DataModelTextSearchResultMapper();

        // Act.
        var sut = new VectorStoreTextSearch<DataModel>(vectorSearch, stringMapper, resultMapper);

        // Assert.
        Assert.NotNull(sut);
    }

    [Fact]
    public async Task CanSearchAsync()
    {
        // Arrange.
        var sut = await CreateVectorStoreTextSearchAsync();

        // Act.
        IAsyncEnumerable<string> searchResults = sut.SearchAsync("What is the Semantic Kernel?", 2, new() { Skip = 0 });
        var results = await searchResults.ToListAsync();

        Assert.Equal(2, results.Count);
    }

    [Fact]
    public async Task CanGetTextSearchResultsAsync()
    {
        // Arrange.
        var sut = await CreateVectorStoreTextSearchAsync();

        // Act.
        IAsyncEnumerable<TextSearchResult> searchResults = sut.GetTextSearchResultsAsync("What is the Semantic Kernel?", 2, new() { Skip = 0 });
        var results = await searchResults.ToListAsync();

        Assert.Equal(2, results.Count);
    }

    [Fact]
    public async Task CanGetSearchResultAsync()
    {
        // Arrange.
        var sut = await CreateVectorStoreTextSearchAsync();

        // Act.
        IAsyncEnumerable<object> searchResults = sut.GetSearchResultsAsync("What is the Semantic Kernel?", 2, new() { Skip = 0 });
        var results = await searchResults.ToListAsync();

        Assert.Equal(2, results.Count);
    }

    [Fact]
    public async Task CanSearchWithEmbeddingGeneratorAsync()
    {
        // Arrange.
        var sut = await CreateVectorStoreTextSearchWithEmbeddingGeneratorAsync();

        // Act.
        var searchResults = sut.SearchAsync("What is the Semantic Kernel?", top: 2, new() { Skip = 0 });
        var results = await searchResults.ToListAsync();

        Assert.Equal(2, results.Count);
    }

    [Fact]
    public async Task CanGetTextSearchResultsWithEmbeddingGeneratorAsync()
    {
        // Arrange.
        var sut = await CreateVectorStoreTextSearchWithEmbeddingGeneratorAsync();

        // Act.
        var searchResults = sut.GetTextSearchResultsAsync("What is the Semantic Kernel?", top: 2, new() { Skip = 0 });
        var results = await searchResults.ToListAsync();

        Assert.Equal(2, results.Count);
    }

    [Fact]
    public async Task CanGetSearchResultsWithEmbeddingGeneratorAsync()
    {
        // Arrange.
        var sut = await CreateVectorStoreTextSearchWithEmbeddingGeneratorAsync();

        // Act.
        var searchResults = sut.GetSearchResultsAsync("What is the Semantic Kernel?", top: 2, new() { Skip = 0 });
        var results = await searchResults.ToListAsync();

        Assert.Equal(2, results.Count);
    }

#pragma warning disable CS0618 // VectorStoreTextSearch with ITextEmbeddingGenerationService is obsolete
    [Fact]
    public async Task CanSearchWithEmbeddingGenerationServiceAsync()
    {
        // Arrange.
        var sut = await CreateVectorStoreTextSearchWithEmbeddingGenerationServiceAsync();

        // Act.
        IAsyncEnumerable<string> searchResults = sut.SearchAsync("What is the Semantic Kernel?", 2, new() { Skip = 0 });
        var results = await searchResults.ToListAsync();

        Assert.Equal(2, results.Count);
    }

    [Fact]
    public async Task CanGetTextSearchResultsWithEmbeddingGenerationServiceAsync()
    {
        // Arrange.
        var sut = await CreateVectorStoreTextSearchWithEmbeddingGenerationServiceAsync();

        // Act.
        IAsyncEnumerable<TextSearchResult> searchResults = sut.GetTextSearchResultsAsync("What is the Semantic Kernel?", 2, new() { Skip = 0 });
        var results = await searchResults.ToListAsync();

        Assert.Equal(2, results.Count);
    }

    [Fact]
    public async Task CanGetSearchResultsWithEmbeddingGenerationServiceAsync()
    {
        // Arrange.
        var sut = await CreateVectorStoreTextSearchWithEmbeddingGenerationServiceAsync();

        // Act.
        IAsyncEnumerable<object> searchResults = sut.GetSearchResultsAsync("What is the Semantic Kernel?", 2, new() { Skip = 0 });
        var results = await searchResults.ToListAsync();

        Assert.Equal(2, results.Count);
    }
#pragma warning restore CS0618 // VectorStoreTextSearch with ITextEmbeddingGenerationService is obsolete

    [Fact]
    public async Task CanFilterGetSearchResultsWithVectorizedSearchAsync()
    {
        // Arrange.
        var sut = await CreateVectorStoreTextSearchAsync();
        TextSearchFilter evenFilter = new();
        evenFilter.Equality("Tag", "Even");
        TextSearchFilter oddFilter = new();
        oddFilter.Equality("Tag", "Odd");

        // Act.
        IAsyncEnumerable<object> evenSearchResults = sut.GetSearchResultsAsync("What is the Semantic Kernel?", 2, new()
        {
            Skip = 0,
            Filter = evenFilter
        });
        var evenResults = await evenSearchResults.ToListAsync();
        IAsyncEnumerable<object> oddSearchResults = sut.GetSearchResultsAsync("What is the Semantic Kernel?", 2, new()
        {
            Skip = 0,
            Filter = oddFilter
        });
        var oddResults = await oddSearchResults.ToListAsync();

        Assert.Equal(2, evenResults.Count);
        var result1 = evenResults[0] as DataModel;
        Assert.Equal("Even", result1?.Tag);
        var result2 = evenResults[1] as DataModel;
        Assert.Equal("Even", result2?.Tag);

        Assert.Equal(2, oddResults.Count);
        result1 = oddResults[0] as DataModel;
        Assert.Equal("Odd", result1?.Tag);
        result2 = oddResults[1] as DataModel;
        Assert.Equal("Odd", result2?.Tag);
    }
}
