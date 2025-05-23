// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Globalization;
using System.Text.Json;
using System.Text.Json.Nodes;
using Json.Schema;

namespace Microsoft.SemanticKernel.Plugins.OpenApi;

/// <summary>
/// Provides functionality for converting OpenApi types - https://swagger.io/docs/specification/data-models/data-types/
/// </summary>
internal static class OpenApiTypeConverter
{
    /// <summary>
    /// Converts the given parameter argument to a JsonNode based on the specified type or schema.
    /// </summary>
    /// <param name="name">The parameter name.</param>
    /// <param name="type">The parameter type.</param>
    /// <param name="argument">The argument to be converted.</param>
    /// <param name="schema">The parameter schema.</param>
    /// <returns>A JsonNode representing the converted value.</returns>
<<<<<<< HEAD
    public static JsonNode Convert(string name, RestApiParameterType? type, object argument)
=======
    public static JsonNode Convert(string name, string type, object argument, KernelJsonSchema? schema = null)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    {
        Verify.NotNull(argument);

        try
        {
<<<<<<< HEAD
#pragma warning disable IDE0072 // Add missing cases
=======
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            JsonNode? node = type switch
            {
                RestApiParameterType.String => JsonValue.Create(argument),
                RestApiParameterType.Array => argument switch
                {
                    string s => JsonArray.Parse(s) as JsonArray,
                    _ => JsonSerializer.SerializeToNode(argument) as JsonArray
                },
                RestApiParameterType.Integer => argument switch
                {
                    string stringArgument => JsonValue.Create(long.Parse(stringArgument, CultureInfo.InvariantCulture)),
                    byte or sbyte or short or ushort or int or uint or long or ulong => JsonValue.Create(argument),
                    _ => null
                },
                RestApiParameterType.Boolean => argument switch
                {
                    bool b => JsonValue.Create(b),
                    string s => JsonValue.Create(bool.Parse(s)),
                    _ => null
                },
                RestApiParameterType.Number => argument switch
                {
                    string stringArgument when long.TryParse(stringArgument, out var intValue) => JsonValue.Create(intValue),
                    string stringArgument when double.TryParse(stringArgument, out var doubleValue) => JsonValue.Create(doubleValue),
                    byte or sbyte or short or ushort or int or uint or long or ulong or float or double or decimal => JsonValue.Create(argument),
                    _ => null
                },
<<<<<<< HEAD
                // Type may not be specified in the schema which means it can be any type.
                null => JsonSerializer.SerializeToNode(argument),
                _ => throw new NotSupportedException($"Unexpected type '{type}' of parameter '{name}' with argument '{argument}'."),
=======
                _ => schema is null
                    ? JsonSerializer.SerializeToNode(argument)
                    : ValidateSchemaAndConvert(name, schema, argument)
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
            };
#pragma warning restore IDE0072 // Add missing cases

            return node ?? throw new ArgumentOutOfRangeException(name, argument, $"Argument type '{argument.GetType()}' is not convertible to parameter type '{type}'.");
        }
        catch (ArgumentException ex)
        {
            throw new ArgumentOutOfRangeException(name, argument, ex.Message);
        }
        catch (FormatException ex)
        {
            throw new ArgumentOutOfRangeException(name, argument, ex.Message);
        }
    }

    /// <summary>
    /// Validates the argument against the parameter schema and converts it to a JsonNode if valid.
    /// </summary>
    /// <param name="parameterName">The parameter name.</param>
    /// <param name="parameterSchema">The parameter schema.</param>
    /// <param name="argument">The argument to be validated and converted.</param>
    /// <returns>A JsonNode representing the converted value.</returns>
    private static JsonNode? ValidateSchemaAndConvert(string parameterName, KernelJsonSchema parameterSchema, object argument)
    {
        var jsonSchema = JsonSchema.FromText(JsonSerializer.Serialize(parameterSchema));

        var node = JsonSerializer.SerializeToNode(argument);

        if (jsonSchema.Evaluate(node).IsValid)
        {
            return node;
        }

        throw new ArgumentOutOfRangeException(parameterName, argument, $"Argument type '{argument.GetType()}' does not match the schema.");
    }
}
