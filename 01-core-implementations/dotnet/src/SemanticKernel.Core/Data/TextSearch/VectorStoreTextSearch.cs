// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Diagnostics.CodeAnalysis;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.VectorData;
using Microsoft.SemanticKernel.Embeddings;

namespace Microsoft.SemanticKernel.Data;

/// <summary>
/// A Vector Store Text Search implementation that can be used to perform searches using a <see cref="VectorStoreCollection{TKey, TRecord}"/>.
/// </summary>
[Experimental("SKEXP0001")]
public sealed class VectorStoreTextSearch<[DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicProperties)] TRecord> : ITextSearch
#pragma warning restore CA1711 // Identifiers should not have incorrect suffix
{
    /// <summary>
    /// Create an instance of the <see cref="VectorStoreTextSearch{TRecord}"/> with the
    /// provided <see cref="IVectorSearchable{TRecord}"/> for performing searches and
    /// <see cref="IEmbeddingGenerator"/> for generating vectors from the text search query.
    /// </summary>
    /// <param name="vectorSearchable"><see cref="IVectorSearchable{TRecord}"/> instance used to perform the search.</param>
    /// <param name="embeddingGenerator"><see cref="IEmbeddingGenerator"/> instance used to create a vector from the text query. Only FLOAT32 vector generation is currently supported by <see cref="VectorStoreTextSearch{TRecord}"/>. If you required a different type of vector use the built in vector generation in the vector store.</param>
    /// <param name="stringMapper"><see cref="MapFromResultToString" /> instance that can map a TRecord to a <see cref="string"/></param>
    /// <param name="resultMapper"><see cref="MapFromResultToTextSearchResult" /> instance that can map a TRecord to a <see cref="TextSearchResult"/></param>
    /// <param name="options">Options used to construct an instance of <see cref="VectorStoreTextSearch{TRecord}"/></param>
    public VectorStoreTextSearch(
        IVectorSearchable<TRecord> vectorSearchable,
        IEmbeddingGenerator<string, Embedding<float>> embeddingGenerator,
        MapFromResultToString stringMapper,
        MapFromResultToTextSearchResult resultMapper,
        VectorStoreTextSearchOptions? options = null) :
        this(
            vectorSearchable,
            embeddingGenerator,
            stringMapper is null ? null : new TextSearchStringMapper(stringMapper),
            resultMapper is null ? null : new TextSearchResultMapper(resultMapper),
            options)
    {
    }

    /// <summary>
    /// Create an instance of the <see cref="VectorStoreTextSearch{TRecord}"/> with the
    /// provided <see cref="IVectorSearchable{TRecord}"/> for performing searches and
    /// <see cref="IEmbeddingGenerator"/> for generating vectors from the text search query.
    /// </summary>
    /// <param name="vectorSearchable"><see cref="IVectorSearchable{TRecord}"/> instance used to perform the search.</param>
    /// <param name="embeddingGenerator"><see cref="IEmbeddingGenerator"/> instance used to create a vector from the text query. Only FLOAT32 vector generation is currently supported by <see cref="VectorStoreTextSearch{TRecord}"/>. If you required a different type of vector use the built in vector generation in the vector store.</param>
    /// <param name="stringMapper"><see cref="ITextSearchStringMapper" /> instance that can map a TRecord to a <see cref="string"/></param>
    /// <param name="resultMapper"><see cref="ITextSearchResultMapper" /> instance that can map a TRecord to a <see cref="TextSearchResult"/></param>
    /// <param name="options">Options used to construct an instance of <see cref="VectorStoreTextSearch{TRecord}"/></param>
    public VectorStoreTextSearch(
        IVectorSearchable<TRecord> vectorSearchable,
        IEmbeddingGenerator<string, Embedding<float>> embeddingGenerator,
        ITextSearchStringMapper? stringMapper = null,
        ITextSearchResultMapper? resultMapper = null,
#pragma warning disable CS0618 // Type or member is obsolete
        VectorStoreTextSearchOptions? options = null) :
        this(
            vectorSearchable,
            embeddingGenerator.AsTextEmbeddingGenerationService(),
            stringMapper,
            resultMapper,
            options)
#pragma warning restore CS0618 // Type or member is obsolete
    {
    }

    /// <summary>
    /// Create an instance of the <see cref="VectorStoreTextSearch{TRecord}"/> with the
    /// provided <see cref="IVectorSearchable{TRecord}"/> for performing searches and
    /// <see cref="ITextEmbeddingGenerationService"/> for generating vectors from the text search query.
    /// </summary>
    /// <param name="vectorSearchable"><see cref="IVectorSearchable{TRecord}"/> instance used to perform the search.</param>
    /// <param name="textEmbeddingGeneration"><see cref="ITextEmbeddingGenerationService"/> instance used to create a vector from the text query.</param>
    /// <param name="stringMapper"><see cref="MapFromResultToString" /> instance that can map a TRecord to a <see cref="string"/></param>
    /// <param name="resultMapper"><see cref="MapFromResultToTextSearchResult" /> instance that can map a TRecord to a <see cref="TextSearchResult"/></param>
    /// <param name="options">Options used to construct an instance of <see cref="VectorStoreTextSearch{TRecord}"/></param>
    [Obsolete("Use the constructor with IEmbeddingGenerator or use the constructor without an ITextEmbeddingGenerationService and pass a vectorSearch configured to perform embedding generation with IEmbeddingGenerator")]
    public VectorStoreTextSearch(
        IVectorSearchable<TRecord> vectorSearchable,
        ITextEmbeddingGenerationService textEmbeddingGeneration,
        MapFromResultToString stringMapper,
        MapFromResultToTextSearchResult resultMapper,
        VectorStoreTextSearchOptions? options = null) :
        this(
            vectorSearchable,
            textEmbeddingGeneration,
            stringMapper is null ? null : new TextSearchStringMapper(stringMapper),
            resultMapper is null ? null : new TextSearchResultMapper(resultMapper),
            options)
    {
    }

    /// <summary>
    /// Create an instance of the <see cref="VectorStoreTextSearch{TRecord}"/> with the
    /// provided <see cref="IVectorSearchable{TRecord}"/> for performing searches and
    /// <see cref="ITextEmbeddingGenerationService"/> for generating vectors from the text search query.
    /// </summary>
    /// <param name="vectorSearchable"><see cref="IVectorSearchable{TRecord}"/> instance used to perform the search.</param>
    /// <param name="textEmbeddingGeneration"><see cref="ITextEmbeddingGenerationService"/> instance used to create a vector from the text query.</param>
    /// <param name="stringMapper"><see cref="ITextSearchStringMapper" /> instance that can map a TRecord to a <see cref="string"/></param>
    /// <param name="resultMapper"><see cref="ITextSearchResultMapper" /> instance that can map a TRecord to a <see cref="TextSearchResult"/></param>
    /// <param name="options">Options used to construct an instance of <see cref="VectorStoreTextSearch{TRecord}"/></param>
    [Obsolete("Use the constructor with IEmbeddingGenerator or use the constructor without an ITextEmbeddingGenerationService and pass a vectorSearch configured to perform embedding generation with IEmbeddingGenerator")]
    public VectorStoreTextSearch(
        IVectorSearchable<TRecord> vectorSearchable,
        ITextEmbeddingGenerationService textEmbeddingGeneration,
        ITextSearchStringMapper? stringMapper = null,
        ITextSearchResultMapper? resultMapper = null,
        VectorStoreTextSearchOptions? options = null)
    {
        Verify.NotNull(vectorSearchable);
        Verify.NotNull(textEmbeddingGeneration);

        this._vectorSearchable = vectorSearchable;
        this._textEmbeddingGeneration = textEmbeddingGeneration;
        this._propertyReader = new Lazy<TextSearchResultPropertyReader>(() => new TextSearchResultPropertyReader(typeof(TRecord)));
        this._stringMapper = stringMapper ?? this.CreateTextSearchStringMapper();
        this._resultMapper = resultMapper ?? this.CreateTextSearchResultMapper();
    }

    /// <summary>
    /// Create an instance of the <see cref="VectorStoreTextSearch{TRecord}"/> with the
    /// provided <see cref="IVectorSearchable{TRecord}"/> for performing searches and
    /// <see cref="ITextEmbeddingGenerationService"/> for generating vectors from the text search query.
    /// </summary>
    /// <param name="vectorSearchable"><see cref="IVectorSearchable{TRecord}"/> instance used to perform the text search.</param>
    /// <param name="stringMapper"><see cref="MapFromResultToString" /> instance that can map a TRecord to a <see cref="string"/></param>
    /// <param name="resultMapper"><see cref="MapFromResultToTextSearchResult" /> instance that can map a TRecord to a <see cref="TextSearchResult"/></param>
    /// <param name="options">Options used to construct an instance of <see cref="VectorStoreTextSearch{TRecord}"/></param>
    public VectorStoreTextSearch(
        IVectorSearchable<TRecord> vectorSearchable,
        MapFromResultToString stringMapper,
        MapFromResultToTextSearchResult resultMapper,
        VectorStoreTextSearchOptions? options = null) :
        this(
            vectorSearchable,
            new TextSearchStringMapper(stringMapper),
            new TextSearchResultMapper(resultMapper),
            options)
    {
    }

    /// <summary>
    /// Create an instance of the <see cref="VectorStoreTextSearch{TRecord}"/> with the
    /// provided <see cref="IVectorSearchable{TRecord}"/> for performing searches and
    /// <see cref="ITextEmbeddingGenerationService"/> for generating vectors from the text search query.
    /// </summary>
    /// <param name="vectorSearchable"><see cref="IVectorSearchable{TRecord}"/> instance used to perform the text search.</param>
    /// <param name="stringMapper"><see cref="ITextSearchStringMapper" /> instance that can map a TRecord to a <see cref="string"/></param>
    /// <param name="resultMapper"><see cref="ITextSearchResultMapper" /> instance that can map a TRecord to a <see cref="TextSearchResult"/></param>
    /// <param name="options">Options used to construct an instance of <see cref="VectorStoreTextSearch{TRecord}"/></param>
    public VectorStoreTextSearch(
        IVectorSearchable<TRecord> vectorSearchable,
        ITextSearchStringMapper? stringMapper = null,
        ITextSearchResultMapper? resultMapper = null,
        VectorStoreTextSearchOptions? options = null)
    {
        Verify.NotNull(vectorSearchable);

        this._vectorSearchable = vectorSearchable;
        this._propertyReader = new Lazy<TextSearchResultPropertyReader>(() => new TextSearchResultPropertyReader(typeof(TRecord)));
        this._stringMapper = stringMapper ?? this.CreateTextSearchStringMapper();
        this._resultMapper = resultMapper ?? this.CreateTextSearchResultMapper();
    }

    /// <inheritdoc/>
    public async IAsyncEnumerable<string> SearchAsync(string query, int top, TextSearchOptions? searchOptions = null, [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        var searchResponse = this.ExecuteVectorSearchAsync(query, top, searchOptions, cancellationToken);

        await foreach (var result in this.GetResultsAsStringAsync(searchResponse, cancellationToken).ConfigureAwait(false))
        {
            yield return result;
        }
    }

    /// <inheritdoc/>
    public async IAsyncEnumerable<TextSearchResult> GetTextSearchResultsAsync(string query, int top, TextSearchOptions? searchOptions = null, [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        var searchResponse = this.ExecuteVectorSearchAsync(query, top, searchOptions, cancellationToken);

        await foreach (var result in this.GetResultsAsTextSearchResultAsync(searchResponse, cancellationToken).ConfigureAwait(false))
        {
            yield return result;
        }
    }

    /// <inheritdoc/>
    public async IAsyncEnumerable<object> GetSearchResultsAsync(string query, int top, TextSearchOptions? searchOptions = null, [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        var searchResponse = this.ExecuteVectorSearchAsync(query, top, searchOptions, cancellationToken);

        await foreach (var result in this.GetResultsAsRecordAsync(searchResponse, cancellationToken).ConfigureAwait(false))
        {
            yield return result;
        }
    }

    #region obsolete
    /// <inheritdoc/>
    [Obsolete("This method is deprecated and will be removed in future versions. Use SearchAsync that returns IAsyncEnumerable<T> instead.", false)]
    public Task<KernelSearchResults<string>> SearchAsync(string query, TextSearchOptions? searchOptions = null, CancellationToken cancellationToken = default)
    {
        var searchResponse = this.ExecuteVectorSearchAsync(query, searchOptions?.Top ?? TextSearchOptions.DefaultTop, searchOptions, cancellationToken);

        return Task.FromResult(new KernelSearchResults<string>(this.GetResultsAsStringAsync(searchResponse, cancellationToken)));
    }

    /// <inheritdoc/>
    [Obsolete("This method is deprecated and will be removed in future versions. Use SearchAsync that returns IAsyncEnumerable<T> instead.", false)]
    public Task<KernelSearchResults<TextSearchResult>> GetTextSearchResultsAsync(string query, TextSearchOptions? searchOptions = null, CancellationToken cancellationToken = default)
    {
        var searchResponse = this.ExecuteVectorSearchAsync(query, searchOptions?.Top ?? TextSearchOptions.DefaultTop, searchOptions, cancellationToken);

        return Task.FromResult(new KernelSearchResults<TextSearchResult>(this.GetResultsAsTextSearchResultAsync(searchResponse, cancellationToken)));
    }

    /// <inheritdoc/>
    [Obsolete("This method is deprecated and will be removed in future versions. Use SearchAsync that returns IAsyncEnumerable<T> instead.", false)]
    public Task<KernelSearchResults<object>> GetSearchResultsAsync(string query, TextSearchOptions? searchOptions = null, CancellationToken cancellationToken = default)
    {
        var searchResponse = this.ExecuteVectorSearchAsync(query, searchOptions?.Top ?? TextSearchOptions.DefaultTop, searchOptions, cancellationToken);

        return Task.FromResult(new KernelSearchResults<object>(this.GetResultsAsRecordAsync(searchResponse, cancellationToken)));
    }
    #endregion

    #region private
    [Obsolete("This property is obsolete.")]
    private readonly ITextEmbeddingGenerationService? _textEmbeddingGeneration;
    private readonly IVectorSearchable<TRecord>? _vectorSearchable;
    private readonly ITextSearchStringMapper _stringMapper;
    private readonly ITextSearchResultMapper _resultMapper;
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
    /// Result mapper which converts a TRecord to a <see cref="string"/>.
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

    /// <summary>
    /// Execute a vector search and return the results.
    /// </summary>
    /// <param name="query">What to search for.</param>
    /// <param name="top">Maximum number of search results to return.</param>
    /// <param name="searchOptions">Search options.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    private async IAsyncEnumerable<VectorSearchResult<TRecord>> ExecuteVectorSearchAsync(string query, int top, TextSearchOptions? searchOptions, [EnumeratorCancellation] CancellationToken cancellationToken)
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

            await foreach (var result in this._vectorSearchable!.SearchAsync(vectorizedQuery, top, vectorSearchOptions, cancellationToken).ConfigureAwait(false))
            {
                yield return result;
            }

            yield break;
        }
#pragma warning restore CS0618 // Type or member is obsolete

        await foreach (var result in this._vectorSearchable!.SearchAsync(query, top, vectorSearchOptions, cancellationToken).ConfigureAwait(false))
        {
            yield return result;
        }
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

    #endregion
}
