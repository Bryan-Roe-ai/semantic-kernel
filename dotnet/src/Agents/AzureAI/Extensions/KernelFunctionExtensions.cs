<<<<<<< HEAD
﻿// Copyright (c) Microsoft. All rights reserved.
using System;
using System.Collections.Generic;
using System.Linq;
using AzureAIP = Azure.AI.Projects;

namespace Microsoft.SemanticKernel.Agents.AzureAI;

internal static class KernelFunctionExtensions
=======
// Copyright (c) Microsoft. All rights reserved.
using System;
using Azure.AI.Projects;

namespace Microsoft.SemanticKernel.Agents.AzureAI;

/// <summary>
/// Extensions for <see cref="KernelFunction"/> to support Azure AI specific operations.
/// </summary>
public static class KernelFunctionExtensions
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
{
    /// <summary>
    /// Convert <see cref="KernelFunction"/> to an OpenAI tool model.
    /// </summary>
    /// <param name="function">The source function</param>
    /// <param name="pluginName">The plugin name</param>
    /// <returns>An OpenAI tool definition</returns>
<<<<<<< HEAD
    public static AzureAIP.FunctionToolDefinition ToToolDefinition(this KernelFunction function, string pluginName)
    {
        var metadata = function.Metadata;
        if (metadata.Parameters.Count > 0)
        {
            var required = new List<string>(metadata.Parameters.Count);
            var parameters =
                metadata.Parameters.ToDictionary(
                    p => p.Name,
                    p =>
                    {
                        if (p.IsRequired)
                        {
                            required.Add(p.Name);
                        }

                        return
                            new
                            {
                                type = ConvertType(p.ParameterType),
                                description = p.Description,
                            };
                    });

            var spec =
                new
                {
                    type = "object",
                    properties = parameters,
                    required,
                };

            return new AzureAIP.FunctionToolDefinition(FunctionName.ToFullyQualifiedName(function.Name, pluginName), function.Description, BinaryData.FromObjectAsJson(spec));
        }

        return new AzureAIP.FunctionToolDefinition(FunctionName.ToFullyQualifiedName(function.Name, pluginName), function.Description);
    }

    private static string ConvertType(Type? type)
    {
        if (type is null || type == typeof(string))
        {
            return "string";
        }

        if (type == typeof(bool))
        {
            return "boolean";
        }

        if (type.IsEnum)
        {
            return "enum";
        }

        if (type.IsArray)
        {
            return "array";
        }

        if (type == typeof(DateTime) || type == typeof(DateTimeOffset))
        {
            return "date-time";
        }

        return Type.GetTypeCode(type) switch
        {
            TypeCode.SByte or TypeCode.Byte or
            TypeCode.Int16 or TypeCode.UInt16 or
            TypeCode.Int32 or TypeCode.UInt32 or
            TypeCode.Int64 or TypeCode.UInt64 or
            TypeCode.Single or TypeCode.Double or TypeCode.Decimal => "number",

            _ => "object",
        };
=======
    public static FunctionToolDefinition ToToolDefinition(this KernelFunction function, string pluginName)
    {
        if (function.Metadata.Parameters.Count > 0)
        {
            BinaryData parameterData = function.Metadata.CreateParameterSpec();

            return new FunctionToolDefinition(FunctionName.ToFullyQualifiedName(function.Name, pluginName), function.Description, parameterData);
        }

        return new FunctionToolDefinition(FunctionName.ToFullyQualifiedName(function.Name, pluginName), function.Description);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    }
}
