// Copyright (c) Microsoft. All rights reserved.

using System;
using Microsoft.Extensions.AI;

namespace Microsoft.SemanticKernel.Connectors.Redis;

/// <summary>
/// Options when creating a <see cref="RedisVectorStore"/>.
/// </summary>
public sealed class RedisVectorStoreOptions
{
    /// <summary>
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
    /// An optional factory to use for constructing <see cref="RedisJsonVectorStoreRecordCollection{TRecord}"/> instances, if a custom record collection is required.
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
    /// An optional factory to use for constructing <see cref="RedisJsonVectorStoreRecordCollection{TRecord}"/> instances, if a custom record collection is required.
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
    /// An optional factory to use for constructing <see cref="RedisJsonVectorStoreRecordCollection{TRecord}"/> instances, if a custom record collection is required.
=======
>>>>>>> Stashed changes
=======
    /// An optional factory to use for constructing <see cref="RedisJsonVectorStoreRecordCollection{TRecord}"/> instances, if a custom record collection is required.
=======
>>>>>>> Stashed changes
>>>>>>> head
<<<<<<< main
<<<<<<< HEAD
    /// An optional factory to use for constructing <see cref="RedisJsonVectorStoreRecordCollection{TRecord}"/> instances, if a custom record collection is required.
=======
    /// An optional factory to use for constructing <see cref="RedisJsonVectorStoreRecordCollection{TRecord}"/> instances, if custom options are required.
>>>>>>> 46c3c89f5c5dbc355794ac231b509e142f4fb770
=======
    /// An optional factory to use for constructing <see cref="RedisJsonVectorStoreRecordCollection{TRecord}"/> instances, if a custom record collection is required.
>>>>>>> ms/features/bugbash-prep
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
    /// An optional factory to use for constructing <see cref="RedisJsonVectorStoreRecordCollection{TKey, TRecord}"/> instances, if a custom record collection is required.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    [Obsolete("To control how collections are instantiated, extend your provider's IVectorStore implementation and override GetCollection()")]
    public IRedisVectorStoreRecordCollectionFactory? VectorStoreCollectionFactory { get; init; }

    /// <summary>
    /// Indicates the way in which data should be stored in redis. Default is <see cref="RedisStorageType.Json"/>.
    /// </summary>
    public RedisStorageType? StorageType { get; init; } = RedisStorageType.Json;

    /// <summary>
    /// Gets or sets the default embedding generator to use when generating vectors embeddings with this vector store.
    /// </summary>
    public IEmbeddingGenerator? EmbeddingGenerator { get; init; }
}
