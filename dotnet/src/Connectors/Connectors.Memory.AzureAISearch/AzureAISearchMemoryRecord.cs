﻿// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Diagnostics.CodeAnalysis;
using System.Text;
using System.Text.Json.Serialization;
using Microsoft.SemanticKernel.Memory;
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
using Microsoft.SemanticKernel.Text;
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
using Microsoft.SemanticKernel.Text;
=======
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
using Microsoft.SemanticKernel.Text;
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
using Microsoft.SemanticKernel.Text;
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head

namespace Microsoft.SemanticKernel.Connectors.AzureAISearch;

/// <summary>
/// Azure AI Search record and index definition.
/// Note: once defined, index cannot be modified.
/// </summary>
[Experimental("SKEXP0020")]
internal sealed class AzureAISearchMemoryRecord
{
    /// <summary>
    /// ID field name.
    /// </summary>
    public const string IdField = "Id";
    /// <summary>
    /// Text field name.
    /// </summary>
    public const string TextField = "Text";
    /// <summary>
    /// Embedding field name.
    /// </summary>
    public const string EmbeddingField = "Embedding";
    /// <summary>
    /// External source name field name.
    /// </summary>
    public const string ExternalSourceNameField = "ExternalSourceName";
    /// <summary>
    /// Description field name.
    /// </summary>
    public const string DescriptionField = "Description";
    /// <summary>
    /// Additional metadata field name.
    /// </summary>
    public const string AdditionalMetadataField = "AdditionalMetadata";
    /// <summary>
    /// Is reference field name.
    /// </summary>
    public const string IsReferenceField = "IsReference";

    /// <summary>
    /// Record ID.
    /// The record is not filterable to save quota, also SK uses only semantic search.
    /// </summary>
    [JsonPropertyName(IdField)]
    public string Id { get; set; } = string.Empty;

    /// <summary>
    /// Content is stored here.
    /// </summary>
    [JsonPropertyName(TextField)]
    public string? Text { get; set; } = string.Empty;

    /// <summary>
    /// Content embedding
    /// </summary>
    [JsonPropertyName(EmbeddingField)]
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
    [JsonConverter(typeof(ReadOnlyMemoryConverter))]
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
    [JsonConverter(typeof(ReadOnlyMemoryConverter))]
=======
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
    [JsonConverter(typeof(ReadOnlyMemoryConverter))]
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
    [JsonConverter(typeof(ReadOnlyMemoryConverter))]
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
    public ReadOnlyMemory<float> Embedding { get; set; }

    /// <summary>
    /// Optional description of the content, e.g. a title. This can be useful when
    /// indexing external data without pulling in the entire content.
    /// </summary>
    [JsonPropertyName(DescriptionField)]
    public string? Description { get; set; } = string.Empty;

    /// <summary>
    /// Additional metadata. Currently this is a string, where you could store serialized data as JSON.
    /// In future the design might change to allow storing named values and leverage filters.
    /// </summary>
    [JsonPropertyName(AdditionalMetadataField)]
    public string? AdditionalMetadata { get; set; } = string.Empty;

    /// <summary>
    /// Name of the external source, in cases where the content and the ID are
    /// referenced to external information.
    /// </summary>
    [JsonPropertyName(ExternalSourceNameField)]
    public string ExternalSourceName { get; set; } = string.Empty;

    /// <summary>
    /// Whether the record references external information.
    /// </summary>
    [JsonPropertyName(IsReferenceField)]
    public bool IsReference { get; set; } = false;

    /// <summary>
    /// Initializes a new instance of the <see cref="AzureAISearchMemoryRecord"/> class.
    /// Required by JSON deserializer.
    /// </summary>
    public AzureAISearchMemoryRecord()
    {
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="AzureAISearchMemoryRecord"/> class with the specified ID.
    /// </summary>
    /// <param name="id">The record ID.</param>
    public AzureAISearchMemoryRecord(string id)
    {
        this.Id = EncodeId(id);
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="AzureAISearchMemoryRecord"/> class with the specified parameters.
    /// </summary>
    /// <param name="id">The record ID.</param>
    /// <param name="text">The content stored in the record.</param>
    /// <param name="externalSourceName">The name of the external source.</param>
    /// <param name="isReference">Whether the record references external information.</param>
    /// <param name="embedding">The content embedding.</param>
    /// <param name="description">The optional description of the content.</param>
    /// <param name="additionalMetadata">The additional metadata.</param>
    public AzureAISearchMemoryRecord(
        string id,
        string text,
        string externalSourceName,
        bool isReference,
        ReadOnlyMemory<float> embedding,
        string? description = null,
        string? additionalMetadata = null)
    {
        this.Id = EncodeId(id);
        this.IsReference = isReference;
        this.Embedding = embedding;
        this.Text = text;
        this.ExternalSourceName = externalSourceName;
        this.Description = description;
        this.AdditionalMetadata = additionalMetadata;
    }

    /// <summary>
    /// Converts the current instance to a <see cref="MemoryRecordMetadata"/> object.
    /// </summary>
    /// <returns>A <see cref="MemoryRecordMetadata"/> object.</returns>
    public MemoryRecordMetadata ToMemoryRecordMetadata()
    {
        return new MemoryRecordMetadata(
            isReference: this.IsReference,
            id: DecodeId(this.Id),
            text: this.Text ?? string.Empty,
            description: this.Description ?? string.Empty,
            externalSourceName: this.ExternalSourceName,
            additionalMetadata: this.AdditionalMetadata ?? string.Empty);
    }

    /// <summary>
    /// Creates a new <see cref="AzureAISearchMemoryRecord"/> object from the specified <see cref="MemoryRecord"/>.
    /// </summary>
    /// <param name="record">The <see cref="MemoryRecord"/> object.</param>
    /// <returns>A new <see cref="AzureAISearchMemoryRecord"/> object.</returns>
    public static AzureAISearchMemoryRecord FromMemoryRecord(MemoryRecord record)
    {
        return new AzureAISearchMemoryRecord(
            id: record.Metadata.Id,
            text: record.Metadata.Text,
            externalSourceName: string.Empty,
            isReference: record.Metadata.IsReference,
            description: record.Metadata.Description,
            additionalMetadata: record.Metadata.AdditionalMetadata,
            embedding: record.Embedding
        );
    }

    /// <summary>
    /// Converts the current instance to a <see cref="MemoryRecord"/> object.
    /// </summary>
    /// <param name="withEmbeddings">Whether to include embeddings in the resulting <see cref="MemoryRecord"/>.</param>
    /// <returns>A <see cref="MemoryRecord"/> object.</returns>
    public MemoryRecord ToMemoryRecord(bool withEmbeddings = true)
    {
        return new MemoryRecord(
            metadata: this.ToMemoryRecordMetadata(),
            embedding: withEmbeddings ? this.Embedding : default,
            key: this.Id);
    }

    /// <summary>
    /// Encodes the specified ID using a URL-safe algorithm.
    /// Azure AI Search keys can contain only letters, digits, underscore, dash, equal sign, recommending
    /// to encode values with a URL-safe algorithm.
    /// </summary>
    /// <param name="realId">The original ID.</param>
    /// <returns>The encoded ID.</returns>
    internal static string EncodeId(string realId)
    {
        var bytes = Encoding.UTF8.GetBytes(realId);
        return Convert.ToBase64String(bytes);
    }

    /// <summary>
    /// Decodes the specified encoded ID.
    /// </summary>
    /// <param name="encodedId">The encoded ID.</param>
    /// <returns>The decoded ID.</returns>
    private static string DecodeId(string encodedId)
    {
        var bytes = Convert.FromBase64String(encodedId);
        return Encoding.UTF8.GetString(bytes);
    }
}
