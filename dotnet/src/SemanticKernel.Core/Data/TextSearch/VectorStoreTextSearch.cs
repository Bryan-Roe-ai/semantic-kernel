// Copyright (c) Microsoft. All rights reserved.

<<<<<<< HEAD
=======
using System;
>>>>>>> main
using System.Collections.Generic;
using System.Diagnostics.CodeAnalysis;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
using Microsoft.Extensions.AI;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
using Microsoft.Extensions.VectorData;
>>>>>>> main
using Microsoft.SemanticKernel.Embeddings;

namespace Microsoft.SemanticKernel.Data;

/// <summary>
/// A Vector Store Text Search implementation that can be used to perform searches using a <see cref="IVectorStoreRecordCollection{TKey, TRecord}"/>.
/// </summary>
[Experimental("SKEXP0001")]
public sealed class VectorStoreTextSearch<TRecord> : ITextSearch
#pragma warning restore CA1711 // Identifiers should not have incorrect suffix
{
    /// <summary>
    /// Create an instance of the <see cref="VectorStoreTextSearch{TRecord}"/> with the
    /// provided <see cref="IVectorSearch{TRecord}"/> for performing searches and
    /// <see cref="IEmbeddingGenerator"/> for generating vectors from the text search query.
    /// </summary>
    /// <param name="vectorSearch"><see cref="IVectorSearch{TRecord}"/> instance used to perform the search.</param>
    /// <param name="embeddingGenerator"><see cref="IEmbeddingGenerator"/> instance used to create a vector from the text query. Only FLOAT32 vector generation is currently supported by <see cref="VectorStoreTextSearch{TRecord}"/>. If you required a different type of vector use the built in vector generation in the vector store.</param>
    /// <param name="stringMapper"><see cref="MapFromResultToString" /> instance that can map a TRecord to a <see cref="string"/></param>
    /// <param name="resultMapper"><see cref="MapFromResultToTextSearchResult" /> instance that can map a TRecord to a <see cref="TextSearchResult"/></param>
    /// <param name="options">Options used to construct an instance of <see cref="VectorStoreTextSearch{TRecord}"/></param>
    public VectorStoreTextSearch(
        IVectorSearch<TRecord> vectorSearch,
        IEmbeddingGenerator<string, Embedding<float>> embeddingGenerator,
        MapFromResultToString stringMapper,
        MapFromResultToTextSearchResult resultMapper,
        VectorStoreTextSearchOptions? options = null) :
        this(
            vectorSearch,
            embeddingGenerator,
            stringMapper is null ? null : new TextSearchStringMapper(stringMapper),
            resultMapper is null ? null : new TextSearchResultMapper(resultMapper),
            options)
    {
    }

    /// <summary>
    /// Create an instance of the <see cref="VectorStoreTextSearch{TRecord}"/> with the
    /// provided <see cref="IVectorSearch{TRecord}"/> for performing searches and
    /// <see cref="IEmbeddingGenerator"/> for generating vectors from the text search query.
    /// </summary>
    /// <param name="vectorSearch"><see cref="IVectorSearch{TRecord}"/> instance used to perform the search.</param>
    /// <param name="embeddingGenerator"><see cref="IEmbeddingGenerator"/> instance used to create a vector from the text query. Only FLOAT32 vector generation is currently supported by <see cref="VectorStoreTextSearch{TRecord}"/>. If you required a different type of vector use the built in vector generation in the vector store.</param>
    /// <param name="stringMapper"><see cref="ITextSearchStringMapper" /> instance that can map a TRecord to a <see cref="string"/></param>
    /// <param name="resultMapper"><see cref="ITextSearchResultMapper" /> instance that can map a TRecord to a <see cref="TextSearchResult"/></param>
    /// <param name="options">Options used to construct an instance of <see cref="VectorStoreTextSearch{TRecord}"/></param>
    public VectorStoreTextSearch(
        IVectorSearch<TRecord> vectorSearch,
        IEmbeddingGenerator<string, Embedding<float>> embeddingGenerator,
        ITextSearchStringMapper? stringMapper = null,
        ITextSearchResultMapper? resultMapper = null,
#pragma warning disable CS0618 // Type or member is obsolete
        VectorStoreTextSearchOptions? options = null) :
        this(
            vectorSearch,
            embeddingGenerator.AsTextEmbeddingGenerationService(),
            stringMapper,
            resultMapper,
            options)
#pragma warning restore CS0618 // Type or member is obsolete
    {
    }

    /// <summary>
    /// Create an instance of the <see cref="VectorStoreTextSearch{TRecord}"/> with the
    /// provided <see cref="IVectorSearch{TRecord}"/> for performing searches and
    /// <see cref="ITextEmbeddingGenerationService"/> for generating vectors from the text search query.
    /// </summary>
    /// <param name="vectorSearch"><see cref="IVectorSearch{TRecord}"/> instance used to perform the search.</param>
    /// <param name="textEmbeddingGeneration"><see cref="ITextEmbeddingGenerationService"/> instance used to create a vector from the text query.</param>
    /// <param name="stringMapper"><see cref="MapFromResultToString" /> instance that can map a TRecord to a <see cref="string"/></param>
    /// <param name="resultMapper"><see cref="MapFromResultToTextSearchResult" /> instance that can map a TRecord to a <see cref="TextSearchResult"/></param>
    /// <param name="options">Options used to construct an instance of <see cref="VectorStoreTextSearch{TRecord}"/></param>
    [Obsolete("Use the constructor with IEmbeddingGenerator or use the constructor without an ITextEmbeddingGenerationService and pass a vectorSearch configured to perform embedding generation with IEmbeddingGenerator")]
    public VectorStoreTextSearch(
        IVectorSearch<TRecord> vectorSearch,
        ITextEmbeddingGenerationService textEmbeddingGeneration,
        MapFromResultToString stringMapper,
        MapFromResultToTextSearchResult resultMapper,
        VectorStoreTextSearchOptions? options = null) :
        this(
            vectorSearch,
            textEmbeddingGeneration,
<<<<<<< HEAD
            new TextSearchStringMapper(stringMapper),
            new TextSearchResultMapper(resultMapper),
=======
            stringMapper is null ? null : new TextSearchStringMapper(stringMapper),
            resultMapper is null ? null : new TextSearchResultMapper(resultMapper),
>>>>>>> main
            options)
    {
    }

    /// <summary>
    /// Create an instance of the <see cref="VectorStoreTextSearch{TRecord}"/> with the
    /// provided <see cref="IVectorSearch{TRecord}"/> for performing searches and
    /// <see cref="ITextEmbeddingGenerationService"/> for generating vectors from the text search query.
    /// </summary>
    /// <param name="vectorSearch"><see cref="IVectorSearch{TRecord}"/> instance used to perform the search.</param>
    /// <param name="textEmbeddingGeneration"><see cref="ITextEmbeddingGenerationService"/> instance used to create a vector from the text query.</param>
    /// <param name="stringMapper"><see cref="ITextSearchStringMapper" /> instance that can map a TRecord to a <see cref="string"/></param>
    /// <param name="resultMapper"><see cref="ITextSearchResultMapper" /> instance that can map a TRecord to a <see cref="TextSearchResult"/></param>
    /// <param name="options">Options used to construct an instance of <see cref="VectorStoreTextSearch{TRecord}"/></param>
    [Obsolete("Use the constructor with IEmbeddingGenerator or use the constructor without an ITextEmbeddingGenerationService and pass a vectorSearch configured to perform embedding generation with IEmbeddingGenerator")]
    public VectorStoreTextSearch(
        IVectorSearch<TRecord> vectorSearch,
        ITextEmbeddingGenerationService textEmbeddingGeneration,
<<<<<<< HEAD
        ITextSearchStringMapper stringMapper,
        ITextSearchResultMapper resultMapper,
=======
        ITextSearchStringMapper? stringMapper = null,
        ITextSearchResultMapper? resultMapper = null,
>>>>>>> main
        VectorStoreTextSearchOptions? options = null)
    {
        Verify.NotNull(vectorSearch);
        Verify.NotNull(textEmbeddingGeneration);
<<<<<<< HEAD
        Verify.NotNull(stringMapper);
        Verify.NotNull(resultMapper);

        this._vectorizedSearch = vectorizedSearch;
        this._textEmbeddingGeneration = textEmbeddingGeneration;
        this._stringMapper = stringMapper;
        this._resultMapper = resultMapper;
=======

        this._vectorSearch = vectorSearch;
        this._textEmbeddingGeneration = textEmbeddingGeneration;
        this._propertyReader = new Lazy<TextSearchResultPropertyReader>(() => new TextSearchResultPropertyReader(typeof(TRecord)));
        this._stringMapper = stringMapper ?? this.CreateTextSearchStringMapper();
        this._resultMapper = resultMapper ?? this.CreateTextSearchResultMapper();
>>>>>>> main
    }

    /// <summary>
    /// Create an instance of the <see cref="VectorStoreTextSearch{TRecord}"/> with the
    /// provided <see cref="IVectorizableTextSearch{TRecord}"/> for performing searches and
    /// <see cref="ITextEmbeddingGenerationService"/> for generating vectors from the text search query.
    /// </summary>
    /// <param name="vectorSearch"><see cref="IVectorSearch{TRecord}"/> instance used to perform the text search.</param>
    /// <param name="stringMapper"><see cref="MapFromResultToString" /> instance that can map a TRecord to a <see cref="string"/></param>
    /// <param name="resultMapper"><see cref="MapFromResultToTextSearchResult" /> instance that can map a TRecord to a <see cref="TextSearchResult"/></param>
    /// <param name="options">Options used to construct an instance of <see cref="VectorStoreTextSearch{TRecord}"/></param>
    public VectorStoreTextSearch(
        IVectorSearch<TRecord> vectorSearch,
        MapFromResultToString stringMapper,
        MapFromResultToTextSearchResult resultMapper,
        VectorStoreTextSearchOptions? options = null) :
        this(
            vectorSearch,
            new TextSearchStringMapper(stringMapper),
            new TextSearchResultMapper(resultMapper),
            options)
    {
    }

    /// <summary>
    /// Create an instance of the <see cref="VectorStoreTextSearch{TRecord}"/> with the
    /// provided <see cref="IVectorizableTextSearch{TRecord}"/> for performing searches and
    /// <see cref="ITextEmbeddingGenerationService"/> for generating vectors from the text search query.
    /// </summary>
    /// <param name="vectorSearch"><see cref="IVectorSearch{TRecord}"/> instance used to perform the text search.</param>
    /// <param name="stringMapper"><see cref="ITextSearchStringMapper" /> instance that can map a TRecord to a <see cref="string"/></param>
    /// <param name="resultMapper"><see cref="ITextSearchResultMapper" /> instance that can map a TRecord to a <see cref="TextSearchResult"/></param>
    /// <param name="options">Options used to construct an instance of <see cref="VectorStoreTextSearch{TRecord}"/></param>
    public VectorStoreTextSearch(
<<<<<<< HEAD
        IVectorizableTextSearch<TRecord> vectorizableTextSearch,
<<<<<<< HEAD
        ITextSearchStringMapper stringMapper,
        ITextSearchResultMapper resultMapper,
=======
=======
        IVectorSearch<TRecord> vectorSearch,
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        ITextSearchStringMapper? stringMapper = null,
        ITextSearchResultMapper? resultMapper = null,
>>>>>>> main
        VectorStoreTextSearchOptions? options = null)
    {
        Verify.NotNull(vectorSearch);

<<<<<<< HEAD
        this._vectorizableTextSearch = vectorizableTextSearch;
<<<<<<< HEAD
        this._stringMapper = stringMapper;
        this._resultMapper = resultMapper;
=======
=======
        this._vectorSearch = vectorSearch;
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
        this._propertyReader = new Lazy<TextSearchResultPropertyReader>(() => new TextSearchResultPropertyReader(typeof(TRecord)));
        this._stringMapper = stringMapper ?? this.CreateTextSearchStringMapper();
        this._resultMapper = resultMapper ?? this.CreateTextSearchResultMapper();
>>>>>>> main
    }

    /// <inheritdoc/>
    public Task<KernelSearchResults<string>> SearchAsync(string query, TextSearchOptions? searchOptions = null, CancellationToken cancellationToken = default)
    {
<<<<<<< HEAD
<<<<<<< HEAD
        IAsyncEnumerable<VectorSearchResult<TRecord>> searchResponse = await this.ExecuteVectorSearchAsync(query, searchOptions, cancellationToken).ConfigureAwait(false);

        long? totalCount = null;

        return new KernelSearchResults<string>(this.GetResultsAsStringAsync(searchResponse, cancellationToken), totalCount, GetResultsMetadata(searchResponse));
=======
        VectorSearchResults<TRecord> searchResponse = await this.ExecuteVectorSearchAsync(query, searchOptions, cancellationToken).ConfigureAwait(false);

        return new KernelSearchResults<string>(this.GetResultsAsStringAsync(searchResponse.Results, cancellationToken), searchResponse.TotalCount, searchResponse.Metadata);
>>>>>>> main
=======
        var searchResponse = this.ExecuteVectorSearchAsync(query, searchOptions, cancellationToken);

        return Task.FromResult(new KernelSearchResults<string>(this.GetResultsAsStringAsync(searchResponse, cancellationToken)));
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <inheritdoc/>
    public Task<KernelSearchResults<TextSearchResult>> GetTextSearchResultsAsync(string query, TextSearchOptions? searchOptions = null, CancellationToken cancellationToken = default)
    {
<<<<<<< HEAD
<<<<<<< HEAD
        IAsyncEnumerable<VectorSearchResult<TRecord>> searchResponse = await this.ExecuteVectorSearchAsync(query, searchOptions, cancellationToken).ConfigureAwait(false);

        long? totalCount = null;

        return new KernelSearchResults<TextSearchResult>(this.GetResultsAsTextSearchResultAsync(searchResponse, cancellationToken), totalCount, GetResultsMetadata(searchResponse));
=======
        VectorSearchResults<TRecord> searchResponse = await this.ExecuteVectorSearchAsync(query, searchOptions, cancellationToken).ConfigureAwait(false);

        return new KernelSearchResults<TextSearchResult>(this.GetResultsAsTextSearchResultAsync(searchResponse.Results, cancellationToken), searchResponse.TotalCount, searchResponse.Metadata);
>>>>>>> main
=======
        var searchResponse = this.ExecuteVectorSearchAsync(query, searchOptions, cancellationToken);

        return Task.FromResult(new KernelSearchResults<TextSearchResult>(this.GetResultsAsTextSearchResultAsync(searchResponse, cancellationToken)));
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <inheritdoc/>
    public Task<KernelSearchResults<object>> GetSearchResultsAsync(string query, TextSearchOptions? searchOptions = null, CancellationToken cancellationToken = default)
    {
<<<<<<< HEAD
<<<<<<< HEAD
        IAsyncEnumerable<VectorSearchResult<TRecord>> searchResponse = await this.ExecuteVectorSearchAsync(query, searchOptions, cancellationToken).ConfigureAwait(false);

        long? totalCount = null;

        return new KernelSearchResults<object>(this.GetResultsAsRecordAsync(searchResponse, cancellationToken), totalCount, GetResultsMetadata(searchResponse));
=======
        VectorSearchResults<TRecord> searchResponse = await this.ExecuteVectorSearchAsync(query, searchOptions, cancellationToken).ConfigureAwait(false);

        return new KernelSearchResults<object>(this.GetResultsAsRecordAsync(searchResponse.Results, cancellationToken), searchResponse.TotalCount, searchResponse.Metadata);
>>>>>>> main
=======
        var searchResponse = this.ExecuteVectorSearchAsync(query, searchOptions, cancellationToken);

        return Task.FromResult(new KernelSearchResults<object>(this.GetResultsAsRecordAsync(searchResponse, cancellationToken)));
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    #region private
    [Obsolete("This property is obsolete.")]
    private readonly ITextEmbeddingGenerationService? _textEmbeddingGeneration;
    private readonly IVectorSearch<TRecord>? _vectorSearch;
    private readonly ITextSearchStringMapper _stringMapper;
    private readonly ITextSearchResultMapper _resultMapper;
<<<<<<< HEAD
=======
    private readonly Lazy<TextSearchResultPropertyReader> _propertyReader;

    /// <summary>
    /// Result mapper which converts a TRecord to a <see cref="TextSearchResult"/>.
    /// </summary>
    private TextSearchResultMapper CreateTextSearchResultMapper()
    {
        return new TextSearchResultMapper(result =>
        {
            if (typeof(TRecord) != result.GetType())
            {
                throw new ArgumentException($"Expected result of type {typeof(TRecord).FullName} but got {result.GetType().FullName}.");
            }

            var value = this._propertyReader.Value.GetValue(result) ?? throw new InvalidOperationException($"Value property of {typeof(TRecord).FullName} cannot be null.");
            var name = this._propertyReader.Value.GetName(result);
            var link = this._propertyReader.Value.GetLink(result);

            return new TextSearchResult(value)
            {
                Name = name,
                Link = link,
            };
        });
    }

    /// <summary>
    /// /// Result mapper which converts a TRecord to a <see cref="string"/>.
    /// </summary>
    private TextSearchStringMapper CreateTextSearchStringMapper()
    {
        return new TextSearchStringMapper(result =>
        {
            if (typeof(TRecord) != result.GetType())
            {
                throw new ArgumentException($"Expected result of type {typeof(TRecord).FullName} but got {result.GetType().FullName}.");
            }

            var value = this._propertyReader.Value.GetValue(result);
            return (string?)value ?? throw new InvalidOperationException("Value property cannot be null.");
        });
    }
>>>>>>> main

    /// <summary>
    /// Execute a vector search and return the results.
    /// </summary>
    /// <param name="query">What to search for.</param>
    /// <param name="searchOptions">Search options.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
<<<<<<< HEAD
<<<<<<< HEAD
    private async Task<IAsyncEnumerable<VectorSearchResult<TRecord>>> ExecuteVectorSearchAsync(string query, TextSearchOptions? searchOptions, CancellationToken cancellationToken)
=======
    private async Task<VectorSearchResults<TRecord>> ExecuteVectorSearchAsync(string query, TextSearchOptions? searchOptions, CancellationToken cancellationToken)
>>>>>>> main
=======
    private async IAsyncEnumerable<VectorSearchResult<TRecord>> ExecuteVectorSearchAsync(string query, TextSearchOptions? searchOptions, [EnumeratorCancellation] CancellationToken cancellationToken)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        searchOptions ??= new TextSearchOptions();
        var vectorSearchOptions = new VectorSearchOptions<TRecord>
        {
#pragma warning disable CS0618 // VectorSearchFilter is obsolete
            OldFilter = searchOptions.Filter?.FilterClauses is not null ? new VectorSearchFilter(searchOptions.Filter.FilterClauses) : null,
#pragma warning restore CS0618 // VectorSearchFilter is obsolete
            Skip = searchOptions.Skip,
        };

#pragma warning disable CS0618 // Type or member is obsolete
        if (this._textEmbeddingGeneration is not null)
        {
            var vectorizedQuery = await this._textEmbeddingGeneration!.GenerateEmbeddingAsync(query, cancellationToken: cancellationToken).ConfigureAwait(false);

<<<<<<< HEAD
<<<<<<< HEAD
            return this._vectorizedSearch.VectorizedSearchAsync(vectorizedQuery, vectorSearchOptions, cancellationToken);
        }

        return this._vectorizableTextSearch!.VectorizableTextSearchAsync(query, vectorSearchOptions, cancellationToken);
=======
            return await this._vectorizedSearch.VectorizedSearchAsync(vectorizedQuery, vectorSearchOptions, cancellationToken).ConfigureAwait(false);
        }

        return await this._vectorizableTextSearch!.VectorizableTextSearchAsync(query, vectorSearchOptions, cancellationToken).ConfigureAwait(false);
>>>>>>> main
=======
            await foreach (var result in this._vectorSearch!.SearchEmbeddingAsync(vectorizedQuery, searchOptions.Top, vectorSearchOptions, cancellationToken).ConfigureAwait(false))
            {
                yield return result;
            }

            yield break;
        }
#pragma warning restore CS0618 // Type or member is obsolete

        await foreach (var result in this._vectorSearch!.SearchAsync(query, searchOptions.Top, vectorSearchOptions, cancellationToken).ConfigureAwait(false))
        {
            yield return result;
        }
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }

    /// <summary>
    /// Return the search results as instances of TRecord.
    /// </summary>
    /// <param name="searchResponse">Response containing the web pages matching the query.</param>
    /// <param name="cancellationToken">Cancellation token</param>
    private async IAsyncEnumerable<object> GetResultsAsRecordAsync(IAsyncEnumerable<VectorSearchResult<TRecord>>? searchResponse, [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        if (searchResponse is null)
        {
            yield break;
        }

        await foreach (var result in searchResponse.WithCancellation(cancellationToken).ConfigureAwait(false))
        {
            if (result.Record is not null)
            {
                yield return result.Record;
                await Task.Yield();
            }
        }
    }

    /// <summary>
    /// Return the search results as instances of <see cref="TextSearchResult"/>.
    /// </summary>
    /// <param name="searchResponse">Response containing the web pages matching the query.</param>
    /// <param name="cancellationToken">Cancellation token</param>
    private async IAsyncEnumerable<TextSearchResult> GetResultsAsTextSearchResultAsync(IAsyncEnumerable<VectorSearchResult<TRecord>>? searchResponse, [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        if (searchResponse is null)
        {
            yield break;
        }

        await foreach (var result in searchResponse.WithCancellation(cancellationToken).ConfigureAwait(false))
        {
            if (result.Record is not null)
            {
                yield return this._resultMapper.MapFromResultToTextSearchResult(result.Record);
                await Task.Yield();
            }
        }
    }

    /// <summary>
    /// Return the search results as instances of <see cref="TextSearchResult"/>.
    /// </summary>
    /// <param name="searchResponse">Response containing the web pages matching the query.</param>
    /// <param name="cancellationToken">Cancellation token</param>
    private async IAsyncEnumerable<string> GetResultsAsStringAsync(IAsyncEnumerable<VectorSearchResult<TRecord>>? searchResponse, [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        if (searchResponse is null)
        {
            yield break;
        }

        await foreach (var result in searchResponse.WithCancellation(cancellationToken).ConfigureAwait(false))
        {
            if (result.Record is not null)
            {
                yield return this._stringMapper.MapFromResultToString(result.Record);
                await Task.Yield();
            }
        }
    }

<<<<<<< HEAD
    /// <summary>
    /// Return the results metadata.
    /// </summary>
    /// <param name="searchResponse">Response containing the documents matching the query.</param>
    private static Dictionary<string, object?>? GetResultsMetadata(IAsyncEnumerable<VectorSearchResult<TRecord>>? searchResponse)
    {
        return [];
    }

=======
>>>>>>> main
    #endregion
}
