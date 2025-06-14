// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Text.RegularExpressions;
using Microsoft.Extensions.Logging;

namespace Microsoft.SemanticKernel.TemplateEngine;

/// <summary>
/// A <see cref="Block"/> that represents a named argument for a function call.
/// For example, in the template {{ MyPlugin.MyFunction var1="foo" }}, var1="foo" is a named arg block.
/// </summary>
internal sealed class NamedArgBlock : Block, ITextRendering
{
    /// <summary>
    /// Returns the <see cref="BlockTypes"/>.
    /// </summary>
    internal override BlockTypes Type => BlockTypes.NamedArg;

    /// <summary>
    /// Gets the name of the function argument.
    /// </summary>
    internal string Name { get; } = string.Empty;

    /// <summary>
    /// VarBlock associated with this named argument.
    /// </summary>
    internal VarBlock? VarBlock { get; }

    /// <summary>
    /// Initializes a new instance of the <see cref="NamedArgBlock"/> class.
    /// </summary>
    /// <param name="text">Raw text parsed from the prompt template.</param>
    /// <param name="logger">The <see cref="ILoggerFactory"/> to use for logging. If null, no logging will be performed.</param>
    /// <exception cref="KernelException"></exception>
    public NamedArgBlock(string? text, ILoggerFactory? logger = null)
        : base(NamedArgBlock.TrimWhitespace(text), logger)
    {
        if (!TryGetNameAndValue(this.Content, out string argName, out string argValue))
        {
            this.Logger.LogError("Invalid named argument `{Text}`", text);
            throw new KernelException($"A function named argument must contain a name and value separated by a '{Symbols.NamedArgBlockSeparator}' character.");
        }

        this.Name = argName;
        this._argNameAsVarBlock = new VarBlock($"{Symbols.VarPrefix}{argName}");

        if (argValue[0] == Symbols.VarPrefix)
        {
            this.VarBlock = new VarBlock(argValue);
        }
        else
        {
            this._valBlock = new ValBlock(argValue);
        }
    }

    /// <summary>
    /// Attempts to extract the name and value of a named argument block from a string
    /// </summary>
    /// <param name="text">String from which to extract a name and value</param>
    /// <param name="name">Name extracted from argument block, when successful. Empty string otherwise.</param>
    /// <param name="value">Value extracted from argument block, when successful. Empty string otherwise.</param>
    /// <returns>true when a name and value are successfully extracted from the given text, false otherwise</returns>
    internal static bool TryGetNameAndValue(string? text, out string name, out string value)
    {
        name = string.Empty;
        value = string.Empty;

        if (!string.IsNullOrEmpty(text))
        {
            string[] argBlockParts = text!.Split(new char[] { Symbols.NamedArgBlockSeparator }, StringSplitOptions.RemoveEmptyEntries);

            if (argBlockParts.Length == 2)
            {
                name = argBlockParts[0];
                value = argBlockParts[1];

                return true;
            }
        }

        return false;
    }

    /// <summary>
    /// Gets the rendered value of the function argument. If the value is a <see cref="ValBlock"/>, the value stays the same.
    /// If the value is a <see cref="VarBlock"/>, the value of the variable is determined by the arguments passed in.
    /// </summary>
    /// <param name="arguments">Arguments to use for rendering the named argument value when the value is a <see cref="VarBlock"/>.</param>
    /// <returns></returns>
    internal object? GetValue(KernelArguments? arguments)
    {
        var valueIsValidValBlock = this._valBlock is not null && this._valBlock.IsValid(out var errorMessage);
        if (valueIsValidValBlock)
        {
            return this._valBlock!.Render(arguments);
        }

        var valueIsValidVarBlock = this.VarBlock is not null && this.VarBlock.IsValid(out var errorMessage2);
        if (valueIsValidVarBlock)
        {
            return this.VarBlock!.Render(arguments);
        }

        return string.Empty;
    }

    /// <inheritdoc/>
    public object? Render(KernelArguments? arguments)
    {
        return this.Content;
    }

    /// <summary>
    /// Returns whether the named arg block has valid syntax.
    /// </summary>
    /// <param name="errorMsg">An error message that gets set when the named arg block is not valid.</param>
    /// <returns></returns>
#pragma warning disable CA2254 // error strings are used also internally, not just for logging
    public override bool IsValid(out string errorMsg)
    {
        errorMsg = string.Empty;
        if (string.IsNullOrEmpty(this.Name))
        {
            errorMsg = "A named argument must have a name";
            this.Logger.LogError(errorMsg);
            return false;
        }

        if (this._valBlock is not null && !this._valBlock.IsValid(out var valErrorMsg))
        {
            errorMsg = $"There was an issue with the named argument value for '{this.Name}': {valErrorMsg}";
            this.Logger.LogError(errorMsg);
            return false;
        }
        else if (this.VarBlock is not null && !this.VarBlock.IsValid(out var variableErrorMsg))
        {
            errorMsg = $"There was an issue with the named argument value for '{this.Name}': {variableErrorMsg}";
            this.Logger.LogError(errorMsg);
            return false;
        }
        else if (this._valBlock is null && this.VarBlock is null)
        {
            errorMsg = "A named argument must have a value";
            this.Logger.LogError(errorMsg);
            return false;
        }

        // Argument names share the same validation as variables
        if (!this._argNameAsVarBlock.IsValid(out var argNameErrorMsg))
        {
            errorMsg = Regex.Replace(argNameErrorMsg, "a variable", "An argument", RegexOptions.IgnoreCase);
            errorMsg = Regex.Replace(errorMsg, "the variable", "The argument", RegexOptions.IgnoreCase);
            return false;
        }

        return true;
    }
#pragma warning restore CA2254

    #region private ================================================================================

    private readonly VarBlock _argNameAsVarBlock;
    private readonly ValBlock? _valBlock;

    private static string? TrimWhitespace(string? text)
    {
        if (text is null)
        {
            return text;
        }

        string[] trimmedParts = NamedArgBlock.GetTrimmedParts(text);
        return (trimmedParts?.Length) switch
        {
            1 => trimmedParts[0],
            2 => $"{trimmedParts[0]}{Symbols.NamedArgBlockSeparator}{trimmedParts[1]}",
            _ => null,
        };
    }

    private static string[] GetTrimmedParts(string? text)
    {
        if (text is null)
        {
            return [];
        }

        string[] parts = text.Split([Symbols.NamedArgBlockSeparator], 2);
        string[] result = new string[parts.Length];
        if (parts.Length > 0)
        {
            result[0] = parts[0].Trim();
        }

        if (parts.Length > 1)
        {
            result[1] = parts[1].Trim();
        }

        return result;
    }

    #endregion
}
