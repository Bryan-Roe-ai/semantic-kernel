// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Diagnostics.CodeAnalysis;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Abstractions;
using Microsoft.SemanticKernel.Diagnostics;

namespace Microsoft.SemanticKernel.SkillDefinition;

/// <summary>
/// Semantic Kernel default skill collection class.
/// The class holds a list of all the functions, native and semantic, known to the kernel instance.
/// The list is used by the planner and when executing pipelines of function compositions.
/// </summary>
[SuppressMessage("Naming", "CA1711:Identifiers should not have incorrect suffix")]
[DebuggerTypeProxy(typeof(IReadOnlySkillCollectionTypeProxy))]
[DebuggerDisplay("{DebuggerDisplay,nq}")]
public class SkillCollection : ISkillCollection
{
    internal const string GlobalSkill = "_GLOBAL_FUNCTIONS_";

    public SkillCollection(ILogger? logger = null)
    {
        this._logger = logger ?? NullLogger.Instance;

        // Important: names are case insensitive
        this._skillCollection = new(StringComparer.OrdinalIgnoreCase);
    }

    public ISkillCollection AddFunction(ISKFunction functionInstance)
    {
        Verify.NotNull(functionInstance);

        ConcurrentDictionary<string, ISKFunction> skill = this._skillCollection.GetOrAdd(functionInstance.SkillName, static _ => new(StringComparer.OrdinalIgnoreCase));
        skill[functionInstance.Name] = functionInstance;

        return this;
    }

    /// <inheritdoc/>
    public ISKFunction GetFunction(string functionName) =>
        this.GetFunction(GlobalSkill, functionName);

    /// <inheritdoc/>
    public ISKFunction GetFunction(string skillName, string functionName)
    {
        if (!this.TryGetFunction(skillName, functionName, out ISKFunction? functionInstance))
        {
            this.ThrowFunctionNotAvailable(skillName, functionName);
        }

        return functionInstance;
    }

    /// <inheritdoc/>
    public bool TryGetFunction(string functionName, [NotNullWhen(true)] out ISKFunction? availableFunction) =>
        this.TryGetFunction(GlobalSkill, functionName, out availableFunction);

    /// <inheritdoc/>
    public bool TryGetFunction(string skillName, string functionName, [NotNullWhen(true)] out ISKFunction? availableFunction)
    {
        Verify.NotNull(skillName);
        Verify.NotNull(functionName);

        if (this._skillCollection.TryGetValue(skillName, out ConcurrentDictionary<string, ISKFunction>? skill))
        {
            return skill.TryGetValue(functionName, out availableFunction);
        }

        availableFunction = null;
        return false;
    }

    /// <inheritdoc/>
    public FunctionsView GetFunctionsView(bool includeSemantic = true, bool includeNative = true)
    {
        var result = new FunctionsView();

        if (includeSemantic || includeNative)
        {
            foreach (var skill in this._skillCollection)
            {
                foreach (KeyValuePair<string, ISKFunction> f in skill.Value)
                {
                    if (f.Value.IsSemantic ? includeSemantic : includeNative)
                    {
                        result.AddFunction(f.Value.Describe());
                    }
                }
            }
        }

        return result;
    }

    [DebuggerBrowsable(DebuggerBrowsableState.Never)]
    internal string DebuggerDisplay => $"Count = {this._skillCollection.Count}";

    #region private ================================================================================

    [DoesNotReturn]
    private void ThrowFunctionNotAvailable(string skillName, string functionName)
    {
        this._logger.LogError("Function not available: skill:{0} function:{1}", skillName, functionName);
        throw new SKException($"Function not available {skillName}.{functionName}");
    }

    private readonly ILogger _logger;

    private readonly ConcurrentDictionary<string, ConcurrentDictionary<string, ISKFunction>> _skillCollection;

    #endregion

    /// <summary>
    /// Process extra comments for merge requests during runtime.
    /// </summary>
    public void ProcessExtraCommentsForMergeRequests()
    {
        foreach (var skill in this._skillCollection)
        {
            foreach (var function in skill.Value)
            {
                try
                {
                    // Attempt to run the function
                    function.Value.Invoke();
                }
                catch (Exception ex)
                {
                    // Log the error and mark the file for needing merge
                    this._logger.LogError(ex, "Error running function: {SkillName}.{FunctionName}", skill.Key, function.Key);
                    MarkFileForMerge(skill.Key, function.Key);
                    continue;
                }

                // If the function runs successfully, mark the file for needing optimization
                MarkFileForOptimization(skill.Key, function.Key);
            }
        }
    }

    private void MarkFileForOptimization(string skillName, string functionName)
    {
        // Logic to mark the file for needing optimization
        this._logger.LogInformation("Marking file for optimization: {SkillName}.{FunctionName}", skillName, functionName);
    }

    private void MarkFileForMerge(string skillName, string functionName)
    {
        // Logic to mark the file for needing merge
        this._logger.LogInformation("Marking file for merge: {SkillName}.{FunctionName}", skillName, functionName);
    }
}
