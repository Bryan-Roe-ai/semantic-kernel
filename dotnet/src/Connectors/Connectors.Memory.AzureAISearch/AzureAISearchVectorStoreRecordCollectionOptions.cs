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
﻿// Copyright (c) Microsoft. All rights reserved.
=======
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
﻿// Copyright (c) Microsoft. All rights reserved.
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> main
<<<<<<< Updated upstream
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
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head

using System.Text.Json;
using System.Text.Json.Nodes;
using Azure.Search.Documents.Indexes;
using Microsoft.SemanticKernel.Data;

namespace Microsoft.SemanticKernel.Connectors.AzureAISearch;

/// <summary>
/// Options when creating a <see cref="AzureAISearchVectorStoreRecordCollection{TRecord}"/>.
/// </summary>
public sealed class AzureAISearchVectorStoreRecordCollectionOptions<TRecord>
    where TRecord : class
{
    /// <summary>
    /// Gets or sets an optional custom mapper to use when converting between the data model and the Azure AI Search record.
    /// </summary>
    /// <remarks>
    /// If not set, the default mapper that is provided by the Azure AI Search client SDK will be used.
    /// </remarks>
    public IVectorStoreRecordMapper<TRecord, JsonObject>? JsonObjectCustomMapper { get; init; } = null;

    /// <summary>
    /// Gets or sets an optional record definition that defines the schema of the record type.
    /// </summary>
    /// <remarks>
    /// If not provided, the schema will be inferred from the record model class using reflection.
    /// In this case, the record model properties must be annotated with the appropriate attributes to indicate their usage.
    /// See <see cref="VectorStoreRecordKeyAttribute"/>, <see cref="VectorStoreRecordDataAttribute"/> and <see cref="VectorStoreRecordVectorAttribute"/>.
    /// </remarks>
    public VectorStoreRecordDefinition? VectorStoreRecordDefinition { get; init; } = null;

    /// <summary>
    /// Gets or sets the JSON serializer options to use when converting between the data model and the Azure AI Search record.
    /// Note that when using the default mapper and you are constructing your own <see cref="SearchIndexClient"/>, you will need
    /// to provide the same set of <see cref="System.Text.Json.JsonSerializerOptions"/> both here and when constructing the <see cref="SearchIndexClient"/>.
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
=======
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
<<<<<<< main
    /// Note that when using the default mapper, you will need to provide the same set of <see cref="System.Text.Json.JsonSerializerOptions"/> both here and when constructing the <see cref="SearchIndexClient"/>.
=======
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
    /// </summary>
    public JsonSerializerOptions? JsonSerializerOptions { get; init; } = null;
}
