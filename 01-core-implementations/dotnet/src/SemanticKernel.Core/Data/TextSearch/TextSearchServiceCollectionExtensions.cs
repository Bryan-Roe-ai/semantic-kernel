// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Diagnostics.CodeAnalysis;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.VectorData;

using Microsoft.SemanticKernel.Data;
using Microsoft.SemanticKernel.Embeddings;

namespace Microsoft.SemanticKernel;

/// <summary>
/// Extension methods to register <see cref="ITextSearch"/> for use with <see cref="IServiceCollection"/>.
/// </summary>
public static class TextSearchServiceCollectionExtensions
{
    /// <summary>
    /// Register a <see cref="VectorStoreTextSearch{TRecord}"/> instance with the specified service ID.
    /// </summary>
    /// <param name="services">The <see cref="IServiceCollection"/> to register the <see cref="ITextSearch"/> on.</param>
    /// <param name="stringMapper"><see cref="ITextSearchStringMapper" /> instance that can map a TRecord to a <see cref="string"/></param>
    /// <param name="resultMapper"><see cref="ITextSearchResultMapper" /> instance that can map a TRecord to a <see cref="TextSearchResult"/></param>
    /// <param name="options">Options used to construct an instance of <see cref="VectorStoreTextSearch{TRecord}"/></param>
    /// <param name="serviceId">An optional service id to use as the service key.</param>
    public static IServiceCollection AddVectorStoreTextSearch<TRecord>(
        this IServiceCollection services,
        ITextSearchStringMapper? stringMapper = null,
        ITextSearchResultMapper? resultMapper = null,
        VectorStoreTextSearchOptions? options = null,
        string? serviceId = default)
    {
        // If we are not constructing the dependent services, add the VectorStoreTextSearch as transient, since we
        // cannot make assumptions about how dependent services are being managed.
        services.AddKeyedTransient<VectorStoreTextSearch<TRecord>>(
            serviceId,
            (sp, obj) =>
            {
                stringMapper ??= sp.GetService<ITextSearchStringMapper>();
                resultMapper ??= sp.GetService<ITextSearchResultMapper>();
                options ??= sp.GetService<VectorStoreTextSearchOptions>();

                var vectorSearch = sp.GetService<IVectorSearchable<TRecord>>();

                return vectorSearch is null
                    ? throw new InvalidOperationException("No IVectorSearch<TRecord> registered.")
                    : new VectorStoreTextSearch<TRecord>(vectorSearch, stringMapper, resultMapper, options);
            });

        return services;
    }

    /// <summary>
    /// Register a <see cref="VectorStoreTextSearch{TRecord}"/> instance with the specified service ID.
    /// </summary>
    /// <param name="services">The <see cref="IServiceCollection"/> to register the <see cref="ITextSearch"/> on.</param>
    /// <param name="vectorSearchableServiceId">Service id of the <see cref="IVectorSearchable{TRecord}"/> to use.</param>
    /// <param name="stringMapper"><see cref="ITextSearchStringMapper" /> instance that can map a TRecord to a <see cref="string"/></param>
    /// <param name="resultMapper"><see cref="ITextSearchResultMapper" /> instance that can map a TRecord to a <see cref="TextSearchResult"/></param>
    /// <param name="options">Options used to construct an instance of <see cref="VectorStoreTextSearch{TRecord}"/></param>
    /// <param name="serviceId">An optional service id to use as the service key.</param>
    public static IServiceCollection AddVectorStoreTextSearch<TRecord>(
        this IServiceCollection services,
        string vectorSearchableServiceId,
        ITextSearchStringMapper? stringMapper = null,
        ITextSearchResultMapper? resultMapper = null,
        VectorStoreTextSearchOptions? options = null,
        string? serviceId = default)
        where TRecord : class
    {
        // If we are not constructing the dependent services, add the VectorStoreTextSearch as transient, since we
        // cannot make assumptions about how dependent services are being managed.
        services.AddKeyedTransient<VectorStoreTextSearch<TRecord>>(
            serviceId,
            (sp, obj) =>
            {
                stringMapper ??= sp.GetService<ITextSearchStringMapper>();
                resultMapper ??= sp.GetService<ITextSearchResultMapper>();
                options ??= sp.GetService<VectorStoreTextSearchOptions>();

                var vectorSearch = sp.GetKeyedService<IVectorSearchable<TRecord>>(vectorSearchableServiceId);
                if (vectorSearch is not null)
                {
                    return new VectorStoreTextSearch<TRecord>(
                        vectorSearch,
                        stringMapper,
                        resultMapper,
                        options);
                }

                throw new InvalidOperationException($"No IVectorSearch<TRecord> for service id {vectorSearchableServiceId} registered.");
            });

        return services;
    }

    /// <summary>
    /// Register a <see cref="VectorStoreTextSearch{TRecord}"/> instance with the specified service ID.
    /// </summary>
    /// <param name="services">The <see cref="IServiceCollection"/> to register the <see cref="ITextSearch"/> on.</param>
    /// <param name="vectorSearchServiceId">Service id of the <see cref="IVectorSearchable{TRecord}"/> to use.</param>
    /// <param name="textEmbeddingGenerationServiceId">Service id of the <see cref="ITextEmbeddingGenerationService"/> to use.</param>
    /// <param name="stringMapper"><see cref="ITextSearchStringMapper" /> instance that can map a TRecord to a <see cref="string"/></param>
    /// <param name="resultMapper"><see cref="ITextSearchResultMapper" /> instance that can map a TRecord to a <see cref="TextSearchResult"/></param>
    /// <param name="options">Options used to construct an instance of <see cref="VectorStoreTextSearch{TRecord}"/></param>
    /// <param name="serviceId">An optional service id to use as the service key.</param>
    public static IServiceCollection AddVectorStoreTextSearch<TRecord>(

        this IServiceCollection services,
        string vectorSearchServiceId,
        string textEmbeddingGenerationServiceId,
        ITextSearchStringMapper? stringMapper = null,
        ITextSearchResultMapper? resultMapper = null,
        VectorStoreTextSearchOptions? options = null,
        string? serviceId = default)
        where TRecord : class
    {
        // If we are not constructing the dependent services, add the VectorStoreTextSearch as transient, since we
        // cannot make assumptions about how dependent services are being managed.
        services.AddKeyedTransient<VectorStoreTextSearch<TRecord>>(
            serviceId,
            (sp, obj) =>
            {
                stringMapper ??= sp.GetService<ITextSearchStringMapper>();
                resultMapper ??= sp.GetService<ITextSearchResultMapper>();
                options ??= sp.GetService<VectorStoreTextSearchOptions>();

                var vectorizedSearch = sp.GetKeyedService<IVectorSearchable<TRecord>>(vectorSearchServiceId);
                if (vectorizedSearch is null)
                {
                    throw new InvalidOperationException($"No IVectorizedSearch<TRecord> for service id {vectorSearchServiceId} registered.");
                }

                var generationService = sp.GetKeyedService<ITextEmbeddingGenerationService>(textEmbeddingGenerationServiceId);
                if (vectorizedSearch is not null && generationService is not null)
                {
                    return new VectorStoreTextSearch<TRecord>(
                        vectorizedSearch,
                        generationService,
                        stringMapper,
                        resultMapper,
                        options);
                }

                throw new InvalidOperationException($"No ITextEmbeddingGenerationService for service id {textEmbeddingGenerationServiceId} registered.");
            });

        return services;
    }
}
