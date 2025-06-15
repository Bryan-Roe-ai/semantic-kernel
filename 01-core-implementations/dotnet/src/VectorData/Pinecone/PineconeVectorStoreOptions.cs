

﻿// Copyright (c) Microsoft. All rights reserved.

﻿// Copyright (c) Microsoft. All rights reserved.

// Copyright (c) Microsoft. All rights reserved.

// Copyright (c) Microsoft. All rights reserved.

// Copyright (c) Microsoft. All rights reserved.

// Copyright (c) Microsoft. All rights reserved.

using Microsoft.Extensions.AI;

namespace Microsoft.SemanticKernel.Connectors.Pinecone;

/// <summary>
/// Options when creating a <see cref="PineconeVectorStore"/>.
/// </summary>
public sealed class PineconeVectorStoreOptions
{
    /// <summary>
    /// An optional factory to use for constructing <see cref="PineconeVectorStoreRecordCollection{TRecord}"/> instances, if a custom record collection is required.

    /// An optional factory to use for constructing <see cref="PineconeVectorStoreRecordCollection{TRecord}"/> instances, if custom options are required.

    /// Gets or sets the default embedding generator for vector properties in this collection.

    /// </summary>
    public IEmbeddingGenerator? EmbeddingGenerator { get; set; }

    /// <summary>
    /// Initializes a new instance of the <see cref="PineconeVectorStoreOptions"/> class.
    /// </summary>
    public PineconeVectorStoreOptions()
    {
    }

    internal PineconeVectorStoreOptions(PineconeVectorStoreOptions? source)
    {
        this.EmbeddingGenerator = source?.EmbeddingGenerator;
    }
}
