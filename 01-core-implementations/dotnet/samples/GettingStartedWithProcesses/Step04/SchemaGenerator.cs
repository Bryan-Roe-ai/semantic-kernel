// Copyright (c) Microsoft. All rights reserved.
using System.Text.Json;
using System.Text.Json.Serialization;

using Microsoft.Extensions.AI;
using Microsoft.SemanticKernel;

namespace Step04;

internal static class JsonSchemaGenerator
{
    private static readonly AIJsonSchemaCreateOptions s_config = new()
    {
        TransformOptions = new()
        {
            DisallowAdditionalProperties = true,
            RequireAllProperties = true,
            MoveDefaultKeywordToDescription = true,
        }
    };

    /// <summary>
    /// Wrapper for generating a JSON schema as string from a .NET type.
    /// </summary>
    public static string FromType<TSchemaType>()
    {
        JsonSerializerOptions options = new(JsonSerializerOptions.Default)
        {
            UnmappedMemberHandling = JsonUnmappedMemberHandling.Disallow,
        };
        AIJsonSchemaCreateOptions config = new()
        {
            IncludeSchemaKeyword = false,
            DisallowAdditionalProperties = true,
        };

        return KernelJsonSchemaBuilder.Build(null, typeof(SchemaType), "Intent Result", config).AsJson();
        return KernelJsonSchemaBuilder.Build(typeof(TSchemaType), "Intent Result", config).AsJson();

    }
}
