﻿// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Diagnostics.CodeAnalysis;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;

namespace Microsoft.SemanticKernel;

[ExcludeFromCodeCoverage]
internal static partial class Verify
{
#if NET
    [GeneratedRegex("^[0-9A-Za-z_]*$")]
    private static partial Regex AsciiLettersDigitsUnderscoresRegex();

    [GeneratedRegex("^[^.]+\\.[^.]+$")]
    private static partial Regex FilenameRegex();
#else
    private static Regex AsciiLettersDigitsUnderscoresRegex() => s_asciiLettersDigitsUnderscoresRegex;
    private static readonly Regex s_asciiLettersDigitsUnderscoresRegex = new("^[0-9A-Za-z_]*$", RegexOptions.Compiled);

    private static Regex FilenameRegex() => s_filenameRegex;
    private static readonly Regex s_filenameRegex = new("^[^.]+\\.[^.]+$", RegexOptions.Compiled);
#endif

    /// <summary>
    /// Equivalent of ArgumentNullException.ThrowIfNull
    /// </summary>
    /// <summary>
    /// Ensures that the provided string is not null or composed entirely of whitespace.
    /// Throws an ArgumentException if the string is null or whitespace.
    /// </summary>
    /// <param name="str">The string to validate.</param>
    /// <param name="paramName">The name of the parameter being validated.</param>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    /// Throws an ArgumentNullException if the provided object is null.
    /// </summary>
    /// <param name="obj">The object to check for null.</param>
    /// <param name="paramName">The name of the parameter being checked.</param>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    internal static void NotNull([NotNull] object? obj, [CallerArgumentExpression(nameof(obj))] string? paramName = null)
    {
#if NET
        ArgumentNullException.ThrowIfNull(obj, paramName);
#else
        if (obj is null)
        {
            ThrowArgumentNullException(paramName);
        }
#endif
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    internal static void NotNullOrWhiteSpace([NotNull] string? str, [CallerArgumentExpression(nameof(str))] string? paramName = null)
    {
#if NET
        ArgumentException.ThrowIfNullOrWhiteSpace(str, paramName);
#else
        NotNull(str, paramName);
        if (string.IsNullOrWhiteSpace(str))
        {
            ThrowArgumentWhiteSpaceException(paramName);
        }
#endif
    }

    internal static void NotNullOrEmpty<T>(IList<T> list, [CallerArgumentExpression(nameof(list))] string? paramName = null)
    {
        NotNull(list, paramName);
        if (list.Count == 0)
        {
            throw new ArgumentException("The value cannot be empty.", paramName);
        }
    }

    public static void True(bool condition, string message, [CallerArgumentExpression(nameof(condition))] string? paramName = null)
    {
        if (!condition)
        {
            throw new ArgumentException(message, paramName);
        }
    }

    internal static void ValidPluginName([NotNull] string? pluginName, IReadOnlyKernelPluginCollection? plugins = null, [CallerArgumentExpression(nameof(pluginName))] string? paramName = null)
    {
        NotNullOrWhiteSpace(pluginName);
        if (!AsciiLettersDigitsUnderscoresRegex().IsMatch(pluginName))
        {
            ThrowArgumentInvalidName("plugin name", pluginName, paramName);
        }

        if (plugins is not null && plugins.Contains(pluginName))
        {
            throw new ArgumentException($"A plugin with the name '{pluginName}' already exists.");
        }
    }

    internal static void ValidFunctionName([NotNull] string? functionName, [CallerArgumentExpression(nameof(functionName))] string? paramName = null)
    {
        NotNullOrWhiteSpace(functionName);
        if (!AsciiLettersDigitsUnderscoresRegex().IsMatch(functionName))
        {
            ThrowArgumentInvalidName("function name", functionName, paramName);
        }
    }

    internal static void ValidFilename([NotNull] string? filename, [CallerArgumentExpression(nameof(filename))] string? paramName = null)
    {
        NotNullOrWhiteSpace(filename);
        if (!FilenameRegex().IsMatch(filename))
        {
            throw new ArgumentException($"Invalid filename format: '{filename}'. Filename should consist of an actual name and a file extension.", paramName);
        }
    }

    public static void ValidateUrl(string url, bool allowQuery = false, [CallerArgumentExpression(nameof(url))] string? paramName = null)
    {
        NotNullOrWhiteSpace(url, paramName);

        if (!Uri.TryCreate(url, UriKind.Absolute, out var uri) || string.IsNullOrEmpty(uri.Host))
        {
            throw new ArgumentException($"The `{url}` is not valid.", paramName);
        }

        if (!allowQuery && !string.IsNullOrEmpty(uri.Query))
        {
            throw new ArgumentException($"The `{url}` is not valid: it cannot contain query parameters.", paramName);
        }

        if (!string.IsNullOrEmpty(uri.Fragment))
        {
            throw new ArgumentException($"The `{url}` is not valid: it cannot contain URL fragments.", paramName);
        }
    }

    internal static void StartsWith([NotNull] string? text, string prefix, string message, [CallerArgumentExpression(nameof(text))] string? textParamName = null)
    {
        Debug.Assert(prefix is not null);

        NotNullOrWhiteSpace(text, textParamName);
        if (!text.StartsWith(prefix, StringComparison.OrdinalIgnoreCase))
        {
            throw new ArgumentException(textParamName, message);
        }
    }

    internal static void DirectoryExists(string path)
    {
        if (!Directory.Exists(path))
        {
            throw new DirectoryNotFoundException($"Directory '{path}' could not be found.");
        }
    }

    /// <summary>
    /// Make sure every function parameter name is unique
    /// </summary>
    /// <param name="parameters">List of parameters</param>
    internal static void ParametersUniqueness(IReadOnlyList<KernelParameterMetadata> parameters)
    {
        int count = parameters.Count;
        if (count > 0)
        {
            var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            for (int i = 0; i < count; i++)
            {
                KernelParameterMetadata p = parameters[i];
                if (string.IsNullOrWhiteSpace(p.Name))
                {
                    string paramName = $"{nameof(parameters)}[{i}].{p.Name}";
                    if (p.Name is null)
                    {
                        ThrowArgumentNullException(paramName);
                    }
                    else
                    {
                        ThrowArgumentWhiteSpaceException(paramName);
                    }
                }

                if (!seen.Add(p.Name))
                {
                    throw new ArgumentException($"The function has two or more parameters with the same name '{p.Name}'");
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
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
=======
                    throw new SKException($"The function has two or more parameters with the same name '{p.Name}'");
                    throw new SKException($"The function has two or more parameters with the same name '{p.Name}'");
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
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
>>>>>>> Stashed changes
=======
                    throw new SKException($"The function has two or more parameters with the same name '{p.Name}'");
                    throw new SKException($"The function has two or more parameters with the same name '{p.Name}'");
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
                    throw new SKException($"The function has two or more parameters with the same name '{p.Name}'");
                    throw new SKException($"The function has two or more parameters with the same name '{p.Name}'");
>>>>>>> main
=======
>>>>>>> head
                }
            }
        }
    }

    [DoesNotReturn]
    private static void ThrowArgumentInvalidName(string kind, string name, string? paramName) =>
        throw new ArgumentException($"A {kind} can contain only ASCII letters, digits, and underscores: '{name}' is not a valid name.", paramName);
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
    private static void ThrowInvalidName(string kind, string name) =>
        throw new SKException($"A {kind} can contain only ASCII letters, digits, and underscores: '{name}' is not a valid name.");
>>>>>>> Stashed changes
=======
    private static void ThrowInvalidName(string kind, string name) =>
        throw new SKException($"A {kind} can contain only ASCII letters, digits, and underscores: '{name}' is not a valid name.");
>>>>>>> Stashed changes
=======
    private static void ThrowInvalidName(string kind, string name) =>
        throw new SKException($"A {kind} can contain only ASCII letters, digits, and underscores: '{name}' is not a valid name.");
>>>>>>> Stashed changes
=======
    private static void ThrowInvalidName(string kind, string name) =>
        throw new SKException($"A {kind} can contain only ASCII letters, digits, and underscores: '{name}' is not a valid name.");
>>>>>>> Stashed changes
=======
    private static void ThrowInvalidName(string kind, string name) =>
        throw new SKException($"A {kind} can contain only ASCII letters, digits, and underscores: '{name}' is not a valid name.");
>>>>>>> Stashed changes
=======
    private static void ThrowInvalidName(string kind, string name) =>
        throw new SKException($"A {kind} can contain only ASCII letters, digits, and underscores: '{name}' is not a valid name.");
>>>>>>> Stashed changes
=======
    private static void ThrowInvalidName(string kind, string name) =>
        throw new SKException($"A {kind} can contain only ASCII letters, digits, and underscores: '{name}' is not a valid name.");
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
    private static void ThrowInvalidName(string kind, string name) =>
        throw new SKException($"A {kind} can contain only ASCII letters, digits, and underscores: '{name}' is not a valid name.");
>>>>>>> Stashed changes
=======
    private static void ThrowInvalidName(string kind, string name) =>
        throw new SKException($"A {kind} can contain only ASCII letters, digits, and underscores: '{name}' is not a valid name.");
>>>>>>> Stashed changes
>>>>>>> head

    [DoesNotReturn]
    internal static void ThrowArgumentNullException(string? paramName) =>
        throw new ArgumentNullException(paramName, $"Value cannot be null. (Parameter '{paramName}')");

    [DoesNotReturn]
    internal static void ThrowArgumentWhiteSpaceException(string? paramName) =>
        throw new ArgumentException($"The value of '{paramName}' cannot be an empty string or composed entirely of whitespace.", paramName);

    [DoesNotReturn]
    internal static void ThrowArgumentOutOfRangeException<T>(string? paramName, T actualValue, string message) =>
        throw new ArgumentOutOfRangeException(paramName, actualValue, message);
}
