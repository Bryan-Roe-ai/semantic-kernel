// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Generic;
using System.Text.Json.Nodes;
using System.Web;

namespace Microsoft.SemanticKernel.Plugins.OpenApi;

/// <summary>
/// This class provides methods for serializing values of array parameters.
/// </summary>
internal static class ArrayParameterValueSerializer
{
    /// <summary>
    /// Serializes the items of an array as separate parameters with the same name.
    /// </summary>
    /// <param name="name">The name of the parameter.</param>
    /// <param name="array">The array containing the items to serialize.</param>
    /// <param name="delimiter">The delimiter used to separate parameters.</param>
    /// <returns>A string containing the serialized parameters.</returns>
    public static string SerializeArrayAsSeparateParameters(string name, JsonArray array, string delimiter)
    {
        var segments = new List<string>();

        foreach (var item in array)
        {
            segments.Add($"{name}={HttpUtility.UrlEncode(item?.ToString())}");
        }

        return string.Join(delimiter, segments); //id=1&id=2&id=3
    }

    /// <summary>
    /// Serializes the items of an array as one parameter with delimited values.
    /// </summary>
    /// <param name="array">The array containing the items to serialize.</param>
    /// <param name="delimiter">The delimiter used to separate items.</param>
    /// <param name="encode">Flag specifying whether to encode items or not.</param>
    /// <returns>A string containing the serialized parameter.</returns>
    public static string SerializeArrayAsDelimitedValues(JsonArray array, string delimiter, bool encode = true)
    {
        var values = new List<string?>();

        foreach (var item in array)
        {
            values.Add(encode ? HttpUtility.UrlEncode(item?.ToString()) : item?.ToString());
        }

        return string.Join(delimiter, values);
    }
}
