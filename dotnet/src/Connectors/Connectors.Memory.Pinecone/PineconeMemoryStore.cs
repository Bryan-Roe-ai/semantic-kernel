﻿// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Diagnostics.CodeAnalysis;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Abstractions;
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
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
<<<<<<< main
=======
=======
>>>>>>> origin/main
=======
<<<<<<< main
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
=======
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> Stashed changes
>>>>>>> head
<<<<<<< main
=======
using Microsoft.SemanticKernel.AI.Embeddings;
using Microsoft.SemanticKernel.Connectors.Memory.Pinecone.Model;
using Microsoft.SemanticKernel.Diagnostics;
<<<<<<< main
>>>>>>> ms/feature-error-handling
=======
>>>>>>> ms/feature-error-handling-part3
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
>>>>>>> origin/main
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
<<<<<<< div
>>>>>>> main
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> origin/main
>>>>>>> head
using Microsoft.SemanticKernel.Memory;

namespace Microsoft.SemanticKernel.Connectors.Pinecone;

/// <summary>
/// An implementation of <see cref="IMemoryStore"/> for Pinecone Vector database.
/// </summary>
/// <remarks>
/// The Embedding data is saved to a Pinecone Vector database instance that the client is connected to.
/// The embedding data persists between subsequent instances and has similarity search capability.
/// It should be noted that "Collection" in Pinecone's terminology is much different than what Collection means in IMemoryStore.
/// For that reason, we use the term "Index" in Pinecone to refer to what is a "Collection" in IMemoryStore. So, in the case of Pinecone,
///  "Collection" is synonymous with "Index" when referring to IMemoryStore.
/// </remarks>
[Experimental("SKEXP0020")]
public class PineconeMemoryStore : IPineconeMemoryStore
{
    /// <summary>
    /// Initializes a new instance of the <see cref="PineconeMemoryStore"/> class.
    /// </summary>
    /// <param name="pineconeClient">Instance of Pinecone client which implements <see cref="IPineconeClient"/> interface.</param>
    /// <param name="loggerFactory">The <see cref="ILoggerFactory"/> to use for logging. If null, no logging will be performed.</param>
    public PineconeMemoryStore(
        IPineconeClient pineconeClient,
        ILoggerFactory? loggerFactory = null)
    {
        this._pineconeClient = pineconeClient;
        this._logger = loggerFactory?.CreateLogger(typeof(PineconeMemoryStore)) ?? NullLogger.Instance;
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="PineconeMemoryStore"/> class.
    /// </summary>
    /// <param name="pineconeEnvironment">Pinecone project environment, see https://docs.pinecone.io/docs/projects#project-environment.</param>
    /// <param name="apiKey">Pinecone API key.</param>
    /// <param name="loggerFactory">The <see cref="ILoggerFactory"/> to use for logging. If null, no logging will be performed.</param>
    public PineconeMemoryStore(
        string pineconeEnvironment,
        string apiKey,
        ILoggerFactory? loggerFactory = null)
    {
        this._pineconeClient = new PineconeClient(pineconeEnvironment, apiKey, loggerFactory);
        this._logger = loggerFactory?.CreateLogger(typeof(PineconeMemoryStore)) ?? NullLogger.Instance;
    }

    /// <inheritdoc/>
    /// <param name="collectionName"> in the case of Pinecone, collectionName is synonymous with indexName </param>
    /// <param name="cancellationToken"></param>
    /// <remarks>
    /// Pinecone index creation is asynchronous action which should be performed before any interaction with it.
    /// To make operations within index, its state should be <see cref="IndexState.Ready"/>.
    /// </remarks>
    public async Task CreateCollectionAsync(string collectionName, CancellationToken cancellationToken = default)
    {
        if (!await this.DoesCollectionExistAsync(collectionName, cancellationToken).ConfigureAwait(false))
        {
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            throw new KernelException("Index creation is not supported within memory store. " +
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
<<<<<<< main
<<<<<<< main
            throw new KernelException("Index creation is not supported within memory store. " +
=======
=======
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
<<<<<<< main
<<<<<<< main
            throw new KernelException("Index creation is not supported within memory store. " +
=======
<<<<<<< div
>>>>>>> main
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
            throw new SKException("Index creation is not supported within memory store. " +
>>>>>>> ms/feature-error-handling
=======
            throw new SKException("Index creation is not supported within memory store. " +
>>>>>>> ms/feature-error-handling-part3
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
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
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head
                $"It should be created manually or using {nameof(IPineconeClient.CreateIndexAsync)}. " +
                $"Ensure index state is {IndexState.Ready}.");
        }
    }

    /// <inheritdoc />
    /// <returns> a list of index names </returns>
    public async IAsyncEnumerable<string> GetCollectionsAsync([EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        await foreach (var index in this._pineconeClient.ListIndexesAsync(cancellationToken).ConfigureAwait(false))
        {
            yield return index ?? "";
        }
    }

    /// <inheritdoc/>
    /// <param name="collectionName"> in the case of Pinecone, collectionName is synonymous with indexName </param>
    /// <param name="cancellationToken"></param>
    public async Task<bool> DoesCollectionExistAsync(string collectionName, CancellationToken cancellationToken = default)
    {
        return await this._pineconeClient.DoesIndexExistAsync(collectionName, cancellationToken).ConfigureAwait(false);
    }

    /// <inheritdoc/>
    /// <param name="collectionName"> in the case of Pinecone, collectionName is synonymous with indexName </param>
    /// <param name="cancellationToken"></param>
    public async Task DeleteCollectionAsync(string collectionName, CancellationToken cancellationToken = default)
    {
        if (await this.DoesCollectionExistAsync(collectionName, cancellationToken).ConfigureAwait(false))
        {
            await this._pineconeClient.DeleteIndexAsync(collectionName, cancellationToken).ConfigureAwait(false);
        }
    }

    /// <inheritdoc/>
    /// <param name="collectionName"> in the case of Pinecone, collectionName is synonymous with indexName </param>
    /// <param name="record"></param>
    /// <param name="cancellationToken"></param>
    public async Task<string> UpsertAsync(string collectionName, MemoryRecord record, CancellationToken cancellationToken = default)
    {
        return await this.UpsertToNamespaceAsync(collectionName, string.Empty, record, cancellationToken).ConfigureAwait(false);
    }

    /// <inheritdoc />
    public async Task<string> UpsertToNamespaceAsync(string indexName, string indexNamespace, MemoryRecord record, CancellationToken cancellationToken = default)
    {
        (PineconeDocument vectorData, OperationType operationType) = await this.EvaluateAndUpdateMemoryRecordAsync(indexName, record, indexNamespace, cancellationToken).ConfigureAwait(false);

        Task request = operationType switch
        {
            OperationType.Upsert => this._pineconeClient.UpsertAsync(indexName, [vectorData], indexNamespace, cancellationToken),
            OperationType.Update => this._pineconeClient.UpdateAsync(indexName, vectorData, indexNamespace, cancellationToken),
            OperationType.Skip => Task.CompletedTask,
            _ => Task.CompletedTask
        };

<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> origin/main
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
<<<<<<< div
=======
<<<<<<< main
>>>>>>> main
=======
>>>>>>> head
        try
        {
            await request.ConfigureAwait(false);
        }
        catch (HttpOperationException ex)
        {
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            this._logger.LogError(ex, "Failed to upsert: {Message}", ex.Message);
            throw;
        }
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
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
<<<<<<< main
            this._logger.LogError(ex, "Failed to upsert: {Message}", ex.Message);
            throw;
=======
            throw new SKException($"Failed to upsert due to HttpRequestException: {ex.Message}", ex);
>>>>>>> ms/feature-error-handling-part3
        }
=======
        await request.ConfigureAwait(false);
>>>>>>> ms/feature-error-handling
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
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
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head

        return vectorData.Id;
    }

    /// <inheritdoc/>
    /// <param name="collectionName"> in the case of Pinecone, collectionName is synonymous with indexName </param>
    /// <param name="records"></param>
    /// <param name="cancellationToken"></param>
    public async IAsyncEnumerable<string> UpsertBatchAsync(
        string collectionName,
        IEnumerable<MemoryRecord> records,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        await foreach (string id in this.UpsertBatchToNamespaceAsync(collectionName, string.Empty, records, cancellationToken).ConfigureAwait(false))
        {
            yield return id;
        }
    }

    /// <inheritdoc />
    public async IAsyncEnumerable<string> UpsertBatchToNamespaceAsync(
        string indexName,
        string indexNamespace,
        IEnumerable<MemoryRecord> records,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        List<PineconeDocument> upsertDocuments = [];
        List<PineconeDocument> updateDocuments = [];

        foreach (MemoryRecord? record in records)
        {
            (PineconeDocument document, OperationType operationType) = await this.EvaluateAndUpdateMemoryRecordAsync(
                indexName,
                record,
                indexNamespace,
                cancellationToken).ConfigureAwait(false);

            // ReSharper disable once SwitchStatementHandlesSomeKnownEnumValuesWithDefault
            switch (operationType)
            {
                case OperationType.Upsert:
                    upsertDocuments.Add(document);
                    break;

                case OperationType.Update:

                    updateDocuments.Add(document);
                    break;

                case OperationType.Skip:
                    yield return document.Id;
                    break;
            }
        }

        List<Task> tasks = [];

        if (upsertDocuments.Count > 0)
        {
            tasks.Add(this._pineconeClient.UpsertAsync(indexName, upsertDocuments, indexNamespace, cancellationToken));
        }

        if (updateDocuments.Count > 0)
        {
            IEnumerable<Task> updates = updateDocuments.Select(async d
                => await this._pineconeClient.UpdateAsync(indexName, d, indexNamespace, cancellationToken).ConfigureAwait(false));

            tasks.AddRange(updates);
        }

        PineconeDocument[] vectorData = [.. upsertDocuments, .. updateDocuments];

<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
>>>>>>> head
        try
        {
            await Task.WhenAll(tasks).ConfigureAwait(false);
        }
        catch (HttpOperationException ex)
        {
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            this._logger.LogError(ex, "Failed to upsert batch: {Message}", ex.Message);
            throw;
        }
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
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
<<<<<<< main
            this._logger.LogError(ex, "Failed to upsert batch: {Message}", ex.Message);
            throw;
=======
            throw new SKException($"Failed to upsert due to HttpRequestException: {ex.Message}", ex);
>>>>>>> ms/feature-error-handling-part3
        }
=======
        await Task.WhenAll(tasks).ConfigureAwait(false);
>>>>>>> ms/feature-error-handling
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
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
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head

        foreach (PineconeDocument? v in vectorData)
        {
            yield return v.Id;
        }
    }

    /// <inheritdoc/>
    /// <param name="collectionName"> in the case of Pinecone, collectionName is synonymous with indexName </param>
    /// <param name="key"></param>
    /// <param name="withEmbedding"></param>
    /// <param name="cancellationToken"></param>
    public async Task<MemoryRecord?> GetAsync(
        string collectionName,
        string key,
        bool withEmbedding = false,
        CancellationToken cancellationToken = default)
    {
        return await this.GetFromNamespaceAsync(collectionName, string.Empty, key, withEmbedding, cancellationToken).ConfigureAwait(false);
    }

    /// <inheritdoc />
    public async Task<MemoryRecord?> GetFromNamespaceAsync(
        string indexName,
        string indexNamespace,
        string key,
        bool withEmbedding = false,
        CancellationToken cancellationToken = default)
    {
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        try
        {
            await foreach (PineconeDocument? record in this._pineconeClient.FetchVectorsAsync(
=======
        await foreach (PineconeDocument? record in this._pineconeClient.FetchVectorsAsync(
>>>>>>> Stashed changes
=======
        await foreach (PineconeDocument? record in this._pineconeClient.FetchVectorsAsync(
>>>>>>> Stashed changes
=======
        await foreach (PineconeDocument? record in this._pineconeClient.FetchVectorsAsync(
>>>>>>> Stashed changes
=======
        await foreach (PineconeDocument? record in this._pineconeClient.FetchVectorsAsync(
>>>>>>> Stashed changes
=======
        await foreach (PineconeDocument? record in this._pineconeClient.FetchVectorsAsync(
>>>>>>> Stashed changes
=======
        await foreach (PineconeDocument? record in this._pineconeClient.FetchVectorsAsync(
<<<<<<< Updated upstream
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
        await foreach (PineconeDocument? record in this._pineconeClient.FetchVectorsAsync(
>>>>>>> Stashed changes
=======
        await foreach (PineconeDocument? record in this._pineconeClient.FetchVectorsAsync(
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
                               indexName,
                               [key],
                               indexNamespace,
                               withEmbedding,
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
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
<<<<<<< main
=======
<<<<<<< main
>>>>>>> origin/main
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
<<<<<<< main
<<<<<<< div
>>>>>>> main
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> origin/main
>>>>>>> head
                               cancellationToken).ConfigureAwait(false))
            {
                return record?.ToMemoryRecord();
            }
        }
        catch (HttpOperationException ex)
        {
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            this._logger.LogError(ex, "Failed to get vector data from Pinecone: {Message}", ex.Message);
            throw;
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
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
<<<<<<< main
            this._logger.LogError(ex, "Failed to get vector data from Pinecone: {Message}", ex.Message);
            throw;
=======
                               cancellationToken))
        {
            return record?.ToMemoryRecord(transferVectorOwnership: true);
>>>>>>> ms/feature-error-handling
=======
            throw new SKException($"Failed to get vector data from Pinecone: {ex.Message}", ex);
>>>>>>> ms/feature-error-handling-part3
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
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
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
        }

        return null;
    }

    /// <inheritdoc/>
    /// <param name="collectionName"> in the case of Pinecone, collectionName is synonymous with indexName </param>
    /// <param name="keys"></param>
    /// <param name="withEmbeddings"></param>
    /// <param name="cancellationToken"></param>
    public async IAsyncEnumerable<MemoryRecord> GetBatchAsync(
        string collectionName,
        IEnumerable<string> keys,
        bool withEmbeddings = false,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        await foreach (MemoryRecord? record in this.GetBatchFromNamespaceAsync(collectionName, string.Empty, keys, withEmbeddings, cancellationToken).ConfigureAwait(false))
        {
            yield return record;
        }
    }

    /// <inheritdoc />
    public async IAsyncEnumerable<MemoryRecord> GetBatchFromNamespaceAsync(
        string indexName,
        string indexNamespace,
        IEnumerable<string> keys,
        bool withEmbeddings = false,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        foreach (string? key in keys)
        {
            MemoryRecord? record = await this.GetFromNamespaceAsync(indexName, indexNamespace, key, withEmbeddings, cancellationToken).ConfigureAwait(false);

            if (record is not null)
            {
                yield return record;
            }
        }
    }

    /// <summary>
    /// Get a MemoryRecord from the Pinecone Vector database by pointId.
    /// </summary>
    /// <param name="indexName">The name associated with the index to get the Pinecone vector record from.</param>
    /// <param name="documentId">The unique indexed ID associated with the Pinecone vector record to get.</param>
    /// <param name="limit"></param>
    /// <param name="indexNamespace"> The namespace associated with the Pinecone vector record to get.</param>
    /// <param name="withEmbedding">If true, the embedding will be returned in the memory record.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns></returns>
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    /// <exception cref="KernelException"></exception>
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
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
<<<<<<< main
<<<<<<< main
    /// <exception cref="KernelException"></exception>
=======
    /// <exception cref="SKException"></exception>
>>>>>>> ms/feature-error-handling
=======
    /// <exception cref="SKException"></exception>
>>>>>>> ms/feature-error-handling-part3
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
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
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head
    public async IAsyncEnumerable<MemoryRecord?> GetWithDocumentIdAsync(string indexName,
        string documentId,
        int limit = 3,
        string indexNamespace = "",
        bool withEmbedding = false,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        await foreach (MemoryRecord? record in this.GetWithDocumentIdBatchAsync(indexName, [documentId], limit, indexNamespace, withEmbedding, cancellationToken).ConfigureAwait(false))
        {
            yield return record;
        }
    }

    /// <summary>
    /// Get a MemoryRecord from the Pinecone Vector database by a group of documentIds.
    /// </summary>
    /// <param name="indexName">The name associated with the index to get the Pinecone vector records from.</param>
    /// <param name="documentIds">The unique indexed IDs associated with Pinecone vector records to get.</param>
    /// <param name="limit"></param>
    /// <param name="indexNamespace"> The namespace associated with the Pinecone vector records to get.</param>
    /// <param name="withEmbeddings">If true, the embeddings will be returned in the memory records.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns></returns>
    public async IAsyncEnumerable<MemoryRecord?> GetWithDocumentIdBatchAsync(string indexName,
        IEnumerable<string> documentIds,
        int limit = 3,
        string indexNamespace = "",
        bool withEmbeddings = false,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        foreach (IAsyncEnumerable<MemoryRecord?>? records
                 in documentIds.Select(
                     documentId => this.GetWithDocumentIdAsync(indexName, documentId, limit, indexNamespace, withEmbeddings, cancellationToken)))
        {
            await foreach (MemoryRecord? record in records.WithCancellation(cancellationToken).ConfigureAwait(false))
            {
                yield return record;
            }
        }
    }

    /// <inheritdoc />
    public async IAsyncEnumerable<MemoryRecord?> GetBatchWithFilterAsync(string indexName,
        Dictionary<string, object> filter,
        int limit = 10,
        string indexNamespace = "",
        bool withEmbeddings = false,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        IEnumerable<PineconeDocument?> vectorDataList;

<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        try
        {
            Query query = Query.Create(limit)
                .InNamespace(indexNamespace)
                .WithFilter(filter);

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
        Query query = Query.Create(limit)
                .InNamespace(indexNamespace)
                .WithFilter(filter);

<<<<<<< main
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
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
>>>>>>> head
        Query query = Query.Create(limit)
                .InNamespace(indexNamespace)
                .WithFilter(filter);

<<<<<<< main
<<<<<<< div
>>>>>>> main
=======
<<<<<<< Updated upstream
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
            vectorDataList = await this._pineconeClient
                .QueryAsync(indexName,
                    query,
                    cancellationToken: cancellationToken)
                .ToListAsync(cancellationToken: cancellationToken)
                .ConfigureAwait(false);
        }
        catch (HttpOperationException ex)
        {
            this._logger.LogError(ex, "Error getting batch with filter from Pinecone: {Message}", ex.Message);
            throw;
        }
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
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
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
        vectorDataList = await this._pineconeClient
            .QueryAsync(indexName,
                query,
                cancellationToken: cancellationToken)
            .ToListAsync(cancellationToken: cancellationToken)
            .ConfigureAwait(false);
>>>>>>> ms/feature-error-handling
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
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
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head

        foreach (PineconeDocument? record in vectorDataList)
        {
            yield return record?.ToMemoryRecord();
        }
    }

    /// <inheritdoc />
    /// <param name="collectionName"> in the case of Pinecone, collectionName is synonymous with indexName </param>
    /// <param name="key"></param>
    /// <param name="cancellationToken"></param>
    public async Task RemoveAsync(string collectionName, string key, CancellationToken cancellationToken = default)
    {
        await this.RemoveFromNamespaceAsync(collectionName, string.Empty, key, cancellationToken).ConfigureAwait(false);
    }

    /// <inheritdoc />
    public async Task RemoveFromNamespaceAsync(string indexName, string indexNamespace, string key, CancellationToken cancellationToken = default)
    {
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> origin/main
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
<<<<<<< div
=======
<<<<<<< main
>>>>>>> main
=======
>>>>>>> head
        try
        {
            await this._pineconeClient.DeleteAsync(indexName,
                [
                    key
                ],
                indexNamespace,
                cancellationToken: cancellationToken).ConfigureAwait(false);
        }
        catch (HttpOperationException ex)
        {
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< div
=======
<<<<<<< main
>>>>>>> main
=======
<<<<<<< Updated upstream
=======
<<<<<<< main
>>>>>>> origin/main
>>>>>>> head
=======
<<<<<<< Updated upstream
>>>>>>> Stashed changes
            this._logger.LogError(ex, "Failed to remove vector data from Pinecone: {Message}", ex.Message);
            throw;
=======
            throw new SKException($"Failed to remove vector data from Pinecone {ex.Message}", ex);
>>>>>>> ms/feature-error-handling-part3
        }
=======
<<<<<<< div
<<<<<<< div
=======
<<<<<<< head
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
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
<<<<<<< main
            this._logger.LogError(ex, "Failed to remove vector data from Pinecone: {Message}", ex.Message);
            throw;
=======
            throw new SKException($"Failed to remove vector data from Pinecone {ex.Message}", ex);
>>>>>>> ms/feature-error-handling-part3
        }
=======
<<<<<<< div
=======
>>>>>>> main
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
        await this._pineconeClient.DeleteAsync(
            indexName,
            new[] { key },
            indexNamespace,
            cancellationToken: cancellationToken).ConfigureAwait(false);
>>>>>>> ms/feature-error-handling
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
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
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
    }

    /// <inheritdoc />
    /// <param name="collectionName"> in the case of Pinecone, collectionName is synonymous with indexName </param>
    /// <param name="keys"></param>
    /// <param name="cancellationToken"></param>
    public async Task RemoveBatchAsync(string collectionName, IEnumerable<string> keys, CancellationToken cancellationToken = default)
    {
        await this.RemoveBatchFromNamespaceAsync(collectionName, string.Empty, keys, cancellationToken).ConfigureAwait(false);
    }

    /// <inheritdoc />
    public async Task RemoveBatchFromNamespaceAsync(string indexName, string indexNamespace, IEnumerable<string> keys, CancellationToken cancellationToken = default)
    {
        try
        {
            await this._pineconeClient.DeleteAsync(indexName,
                keys,
                indexNamespace,
                cancellationToken: cancellationToken).ConfigureAwait(false);
        }
        catch (HttpOperationException ex)
        {
            this._logger.LogError(ex, "Failed to remove vector data from Pinecone: {Message}", ex.Message);
            throw;
        }
    }

    /// <inheritdoc />
    public async Task RemoveWithFilterAsync(
        string indexName,
        Dictionary<string, object> filter,
        string indexNamespace = "",
        CancellationToken cancellationToken = default)
    {
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        try
        {
            await this._pineconeClient.DeleteAsync(
=======
        await this._pineconeClient.DeleteAsync(
>>>>>>> Stashed changes
=======
        await this._pineconeClient.DeleteAsync(
>>>>>>> Stashed changes
=======
        await this._pineconeClient.DeleteAsync(
>>>>>>> Stashed changes
=======
        await this._pineconeClient.DeleteAsync(
>>>>>>> Stashed changes
=======
        await this._pineconeClient.DeleteAsync(
>>>>>>> Stashed changes
=======
        await this._pineconeClient.DeleteAsync(
<<<<<<< Updated upstream
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
        await this._pineconeClient.DeleteAsync(
>>>>>>> Stashed changes
=======
        await this._pineconeClient.DeleteAsync(
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
                indexName,
                default,
                indexNamespace,
                filter,
                cancellationToken: cancellationToken).ConfigureAwait(false);
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        }
        catch (HttpOperationException ex)
        {
            this._logger.LogError(ex, "Failed to remove vector data from Pinecone: {Message}", ex.Message);
            throw;
        }
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
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
<<<<<<< main
        }
        catch (HttpOperationException ex)
        {
<<<<<<< main
            this._logger.LogError(ex, "Failed to remove vector data from Pinecone: {Message}", ex.Message);
            throw;
=======
            throw new SKException($"Failed to remove vector data from Pinecone {ex.Message}", ex);
>>>>>>> ms/feature-error-handling-part3
        }
=======
>>>>>>> ms/feature-error-handling
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
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
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head
    }

    /// <summary>
    /// Remove a MemoryRecord from the Pinecone Vector database by pointId.
    /// </summary>
    /// <param name="indexName"> The name associated with the index to remove the Pinecone vector record from.</param>
    /// <param name="documentId">The unique indexed ID associated with the Pinecone vector record to remove.</param>
    /// <param name="indexNamespace">The name associated with a collection of embeddings.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns></returns>
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< main
<<<<<<< main
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
<<<<<<< main
<<<<<<< main
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
    /// <exception cref="KernelException"></exception>
=======
    /// <exception cref="SKException"></exception>
>>>>>>> ms/feature-error-handling
=======
    /// <exception cref="SKException"></exception>
>>>>>>> ms/feature-error-handling-part3
    public async Task RemoveWithDocumentIdAsync(string indexName, string documentId, string indexNamespace, CancellationToken cancellationToken = default)
    {
        await this._pineconeClient.DeleteAsync(
            indexName,
            null,
            indexNamespace,
            new Dictionary<string, object>()
            {
                { "document_Id", documentId }
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< head
=======
>>>>>>> head
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
<<<<<<< main
<<<<<<< main
    /// <exception cref="KernelException"></exception>
=======
    /// <exception cref="SKException"></exception>
>>>>>>> ms/feature-error-handling
=======
    /// <exception cref="SKException"></exception>
>>>>>>> ms/feature-error-handling-part3
    public async Task RemoveWithDocumentIdAsync(string indexName, string documentId, string indexNamespace, CancellationToken cancellationToken = default)
    {
        await this._pineconeClient.DeleteAsync(
            indexName,
            null,
            indexNamespace,
            new Dictionary<string, object>()
            {
                { "document_Id", documentId }
<<<<<<< main
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
<<<<<<< main
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
<<<<<<< div
=======
<<<<<<< main
>>>>>>> main
=======
>>>>>>> head
            }, cancellationToken: cancellationToken).ConfigureAwait(false);
        }
        catch (HttpOperationException ex)
        {
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< div
=======
<<<<<<< main
>>>>>>> main
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< main
>>>>>>> origin/main
=======
<<<<<<< main
>>>>>>> Stashed changes
>>>>>>> head
=======
<<<<<<< Updated upstream
>>>>>>> Stashed changes
            this._logger.LogError(ex, "Failed to remove vector data from Pinecone: {Message}", ex.Message);
            throw;
=======
            throw new SKException($"Failed to remove vector data from Pinecone {ex.Message}", ex);
>>>>>>> ms/feature-error-handling-part3
        }
=======
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< head
=======
>>>>>>> Stashed changes
>>>>>>> head
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
<<<<<<< main
            this._logger.LogError(ex, "Failed to remove vector data from Pinecone: {Message}", ex.Message);
            throw;
=======
            throw new SKException($"Failed to remove vector data from Pinecone {ex.Message}", ex);
>>>>>>> ms/feature-error-handling-part3
        }
=======
            },
            cancellationToken: cancellationToken).ConfigureAwait(false);
>>>>>>> ms/feature-error-handling
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
            },
            cancellationToken: cancellationToken).ConfigureAwait(false);
>>>>>>> ms/feature-error-handling
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
            },
            cancellationToken: cancellationToken).ConfigureAwait(false);
>>>>>>> ms/feature-error-handling
>>>>>>> Stashed changes
<<<<<<< div
=======
            },
            cancellationToken: cancellationToken).ConfigureAwait(false);
>>>>>>> ms/feature-error-handling
>>>>>>> main
=======
>>>>>>> head
    }

    /// <summary>
    /// Remove a MemoryRecord from the Pinecone Vector database by a group of pointIds.
    /// </summary>
    /// <param name="indexName"> The name associated with the index to remove the Pinecone vector record from.</param>
    /// <param name="documentIds">The unique indexed IDs associated with the Pinecone vector records to remove.</param>
    /// <param name="indexNamespace">The name associated with a collection of embeddings.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns></returns>
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    /// <exception cref="KernelException"></exception>
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
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
<<<<<<< main
<<<<<<< main
    /// <exception cref="KernelException"></exception>
=======
    /// <exception cref="SKException"></exception>
>>>>>>> ms/feature-error-handling
=======
    /// <exception cref="SKException"></exception>
>>>>>>> ms/feature-error-handling-part3
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
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
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head
    public async Task RemoveWithDocumentIdBatchAsync(
        string indexName,
        IEnumerable<string> documentIds,
        string indexNamespace,
        CancellationToken cancellationToken = default)
    {
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        try
        {
            IEnumerable<Task> tasks = documentIds.Select(async id
                => await this.RemoveWithDocumentIdAsync(indexName, id, indexNamespace, cancellationToken)
                    .ConfigureAwait(false));

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
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        IEnumerable<Task> tasks = documentIds.Select(async id
                => await this.RemoveWithDocumentIdAsync(indexName, id, indexNamespace, cancellationToken)
                    .ConfigureAwait(false));

<<<<<<< main
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
        IEnumerable<Task> tasks = documentIds.Select(async id
                => await this.RemoveWithDocumentIdAsync(indexName, id, indexNamespace, cancellationToken)
                    .ConfigureAwait(false));

<<<<<<< main
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
            await Task.WhenAll(tasks).ConfigureAwait(false);
        }
        catch (HttpOperationException ex)
        {
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            this._logger.LogError(ex, "Error in batch removing data from Pinecone: {Message}", ex.Message);
            throw;
        }
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
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
<<<<<<< main
            this._logger.LogError(ex, "Error in batch removing data from Pinecone: {Message}", ex.Message);
            throw;
=======
            throw new SKException($"Error in batch removing data from Pinecone {ex.Message}", ex);
>>>>>>> ms/feature-error-handling-part3
        }
=======
        await Task.WhenAll(tasks).ConfigureAwait(false);
>>>>>>> ms/feature-error-handling
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
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
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
    }

    /// <inheritdoc/>
    /// <param name="collectionName"> in the case of Pinecone, collectionName is synonymous with indexName </param>
    /// <param name="embedding"> The embedding to search for </param>
    /// <param name="limit"> The maximum number of results to return </param>
    /// <param name="minRelevanceScore"> The minimum relevance score to return </param>
    /// <param name="withEmbeddings"> Whether to return the embeddings with the results </param>
    /// <param name="cancellationToken"></param>
    public IAsyncEnumerable<(MemoryRecord, double)> GetNearestMatchesAsync(
        string collectionName,
        ReadOnlyMemory<float> embedding,
        int limit,
        double minRelevanceScore = 0,
        bool withEmbeddings = false,
        CancellationToken cancellationToken = default)
    {
        return this.GetNearestMatchesFromNamespaceAsync(
            collectionName,
            string.Empty,
            embedding,
            limit,
            minRelevanceScore,
            withEmbeddings,
            cancellationToken);
    }

    /// <inheritdoc />
    public async IAsyncEnumerable<(MemoryRecord, double)> GetNearestMatchesFromNamespaceAsync(
        string indexName,
        string indexNamespace,
        ReadOnlyMemory<float> embedding,
        int limit,
        double minRelevanceScore = 0,
        bool withEmbeddings = false,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        IAsyncEnumerable<(PineconeDocument, double)> results = this._pineconeClient.GetMostRelevantAsync(
            indexName,
            embedding,
            minRelevanceScore,
            limit,
            withEmbeddings,
            true,
            indexNamespace,
            default,
            cancellationToken);

        await foreach ((PineconeDocument, double) result in results.WithCancellation(cancellationToken).ConfigureAwait(false))
        {
            yield return (result.Item1.ToMemoryRecord(), result.Item2);
        }
    }

    /// <inheritdoc/>
    /// <param name="collectionName"> in the case of Pinecone, collectionName is synonymous with indexName </param>
    /// <param name="embedding"> The embedding to search for </param>
    /// <param name="minRelevanceScore"> The minimum relevance score to return </param>
    /// <param name="withEmbedding"> Whether to return the embeddings with the results </param>
    /// <param name="cancellationToken"></param>
    public async Task<(MemoryRecord, double)?> GetNearestMatchAsync(
        string collectionName,
        ReadOnlyMemory<float> embedding,
        double minRelevanceScore = 0,
        bool withEmbedding = false,
        CancellationToken cancellationToken = default)
    {
        return await this.GetNearestMatchFromNamespaceAsync(
            collectionName,
            string.Empty,
            embedding,
            minRelevanceScore,
            withEmbedding,
            cancellationToken).ConfigureAwait(false);
    }

    /// <inheritdoc />
    public async Task<(MemoryRecord, double)?> GetNearestMatchFromNamespaceAsync(
        string indexName,
        string indexNamespace,
        ReadOnlyMemory<float> embedding,
        double minRelevanceScore = 0,
        bool withEmbedding = false,
        CancellationToken cancellationToken = default)
    {
        IAsyncEnumerable<(MemoryRecord, double)> results = this.GetNearestMatchesFromNamespaceAsync(
            indexName,
            indexNamespace,
            embedding,
            minRelevanceScore: minRelevanceScore,
            limit: 1,
            withEmbeddings: withEmbedding,
            cancellationToken: cancellationToken);

        (MemoryRecord, double) record = await results.FirstOrDefaultAsync(cancellationToken).ConfigureAwait(false);

        return (record.Item1, record.Item2);
    }

    /// <inheritdoc />
    public async IAsyncEnumerable<(MemoryRecord, double)> GetNearestMatchesWithFilterAsync(
        string indexName,
        ReadOnlyMemory<float> embedding,
        int limit,
        Dictionary<string, object> filter,
        double minRelevanceScore = 0D,
        string indexNamespace = "",
        bool withEmbeddings = false,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        IAsyncEnumerable<(PineconeDocument, double)> results = this._pineconeClient.GetMostRelevantAsync(
            indexName,
            embedding,
            minRelevanceScore,
            limit,
            withEmbeddings,
            true,
            indexNamespace,
            filter,
            cancellationToken);

        await foreach ((PineconeDocument, double) result in results.WithCancellation(cancellationToken).ConfigureAwait(false))
        {
            yield return (result.Item1.ToMemoryRecord(), result.Item2);
        }
    }

    /// <inheritdoc />
    public async Task ClearNamespaceAsync(string indexName, string indexNamespace, CancellationToken cancellationToken = default)
    {
        await this._pineconeClient.DeleteAsync(indexName, default, indexNamespace, null, true, cancellationToken).ConfigureAwait(false);
    }

    /// <inheritdoc />
    public async IAsyncEnumerable<string?> ListNamespacesAsync(string indexName, [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        IndexStats? indexStats = await this._pineconeClient.DescribeIndexStatsAsync(indexName, default, cancellationToken).ConfigureAwait(false);

        if (indexStats is null)
        {
            yield break;
        }

        foreach (string? indexNamespace in indexStats.Namespaces.Keys)
        {
            yield return indexNamespace;
        }
    }

    #region private ================================================================================

    private readonly IPineconeClient _pineconeClient;
    private readonly ILogger _logger;

    private async Task<(PineconeDocument, OperationType)> EvaluateAndUpdateMemoryRecordAsync(
        string indexName,
        MemoryRecord record,
        string indexNamespace = "",
        CancellationToken cancellationToken = default)
    {
        string key = !string.IsNullOrEmpty(record.Key)
            ? record.Key
            : record.Metadata.Id;

        PineconeDocument vectorData = record.ToPineconeDocument();

        PineconeDocument? existingRecord = await this._pineconeClient.FetchVectorsAsync(indexName, [key], indexNamespace, false, cancellationToken)
            .FirstOrDefaultAsync(cancellationToken).ConfigureAwait(false);

        if (existingRecord is null)
        {
            return (vectorData, OperationType.Upsert);
        }

        // compare metadata dictionaries
        if (existingRecord.Metadata is not null && vectorData.Metadata is not null)
        {
            if (existingRecord.Metadata.SequenceEqual(vectorData.Metadata))
            {
                return (vectorData, OperationType.Skip);
            }
        }

        return (vectorData, OperationType.Update);
    }

    #endregion
}
