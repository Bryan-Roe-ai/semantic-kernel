// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Diagnostics.CodeAnalysis;
using System.Linq;
using System.Reflection;
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
using System.Text.Json.Nodes;
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
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Abstractions;
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
using Microsoft.SemanticKernel.AI;
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
using Microsoft.SemanticKernel.AI;
=======
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
using Microsoft.SemanticKernel.AI.TextCompletion;
using Microsoft.SemanticKernel.Diagnostics;
using Microsoft.SemanticKernel.Orchestration;
using Microsoft.SemanticKernel.SemanticFunctions;

namespace Microsoft.SemanticKernel.SkillDefinition;

/// <summary>
/// Standard Semantic Kernel callable function.
/// SKFunction is used to extend one C# <see cref="Delegate"/>, <see cref="Func{T, TResult}"/>, <see cref="Action"/>,
/// with additional methods required by the kernel.
/// </summary>
public sealed class SKFunction : ISKFunction, IDisposable
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
[DebuggerDisplay("{DebuggerDisplay,nq}")]
public sealed class SKFunction : ISKFunction
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
{
    /// <inheritdoc/>
    public string Name { get; }

    /// <inheritdoc/>
    public string SkillName { get; }

    /// <inheritdoc/>
    public string Description { get; }

    /// <inheritdoc/>
    public bool IsSemantic { get; }

    /// <inheritdoc/>
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    public CompleteRequestSettings RequestSettings
    {
        get { return this._aiRequestSettings; }
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
    public CompleteRequestSettings RequestSettings
    {
        get { return this._aiRequestSettings; }
=======
    public JsonObject ServiceSettings
    {
        get { return this._aiServiceSettings; }
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
    }

    /// <summary>
    /// List of function parameters
    /// </summary>
    public IList<ParameterView> Parameters { get; }

    /// <summary>
    /// Create a native function instance, wrapping a native object method
    /// </summary>
    /// <param name="methodContainerInstance">Object containing the method to invoke</param>
    /// <param name="methodSignature">Signature of the method to invoke</param>
    /// <param name="skillName">SK skill name</param>
    /// <param name="log">Application logger</param>
    /// <returns>SK function instance</returns>
    public static ISKFunction? FromNativeMethod(
        IKernel kernel,
        MethodInfo methodSignature,
        object? methodContainerInstance = null,
        string skillName = "",
        ILogger? log = null)
    {
        if (string.IsNullOrWhiteSpace(skillName)) { skillName = SkillCollection.GlobalSkill; }

        MethodDetails methodDetails = GetMethodDetails(methodSignature, methodContainerInstance, true, log);

        // If the given method is not a valid SK function
        if (!methodDetails.HasSkFunctionAttribute)
        {
            return null;
        }

        return new SKFunction(
            kernel: kernel,
            delegateType: methodDetails.Type,
            delegateFunction: methodDetails.Function,
            parameters: methodDetails.Parameters,
            skillName: skillName,
            functionName: methodDetails.Name,
            description: methodDetails.Description,
            isSemantic: false,
            log: log);
    }

    /// <summary>
    /// Create a native function instance, wrapping a delegate function
    /// </summary>
    /// <param name="nativeFunction">Function to invoke</param>
    /// <param name="skillName">SK skill name</param>
    /// <param name="functionName">SK function name</param>
    /// <param name="description">SK function description</param>
    /// <param name="parameters">SK function parameters</param>
    /// <param name="log">Application logger</param>
    /// <returns>SK function instance</returns>
    public static ISKFunction FromNativeFunction(
        IKernel kernel,
        Delegate nativeFunction,
        string skillName,
        string functionName,
        string description,
        IEnumerable<ParameterView>? parameters = null,
        ILogger? log = null)
    {
        MethodDetails methodDetails = GetMethodDetails(nativeFunction.Method, nativeFunction.Target, false, log);

        return new SKFunction(
            kernel: kernel,
            delegateType: methodDetails.Type,
            delegateFunction: methodDetails.Function,
            parameters: (parameters ?? Enumerable.Empty<ParameterView>()).ToList(),
            description: description,
            skillName: skillName,
            functionName: functionName,
            isSemantic: false,
            log: log);
    }

    /// <summary>
    /// Create a native function instance, given a semantic function configuration.
    /// </summary>
    /// <param name="skillName">Name of the skill to which the function to create belongs.</param>
    /// <param name="functionName">Name of the function to create.</param>
    /// <param name="functionConfig">Semantic function configuration.</param>
    /// <param name="log">Optional logger for the function.</param>
    /// <returns>SK function instance.</returns>
    public static ISKFunction FromSemanticConfig(
        IKernel kernel,
        string skillName,
        string functionName,
        SemanticFunctionConfig functionConfig,
        ILogger? log = null)
    {
        Verify.NotNull(functionConfig);

        static async Task<SKContext> LocalFunc(
            IKernel kernel,
            ITextCompletion client,
            CompleteRequestSettings requestSettings,
            SKContext context,
            IPromptTemplate promptTemplate,
            string skillName,
            string functionName,
            CancellationToken cancellationToken)
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
            JsonObject serviceSettings,
            SKContext context)
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
        {
            Verify.NotNull(client);

            try
            {
                string prompt = await promptTemplate.RenderAsync(context).ConfigureAwait(false);

                string completion = await client.CompleteAsync(prompt, requestSettings, cancellationToken).ConfigureAwait(false);
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
                context.Variables.Update(completion);
            }
            catch (AIException ex)
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
                context.Variables.Update(completion);
            }
            catch (AIException ex)
=======
                string completion = await client.CompleteAsync(prompt, serviceSettings, context.CancellationToken).ConfigureAwait(false);
                context.Variables.Update(completion);
            }
            catch (SKException ex)
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
            {
                const string Message = "Something went wrong while rendering the semantic function" +
                                       " or while executing the text completion. Function: {0}.{1}. Error: {2}. Details: {3}";
                kernel.Log.LogError(ex, Message, skillName, functionName, ex.Message, ex.Detail);
                context.Fail(ex.Message, ex);
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
                logger?.LogError(ex, Message, skillName, functionName, ex.Message, ex.Message);
                throw;
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
            }
            catch (Exception ex) when (!ex.IsCriticalException())
            {
                const string Message = "Something went wrong while rendering the semantic function" +
                                       " or while executing the text completion. Function: {0}.{1}. Error: {2}";
                kernel.Log.LogError(ex, Message, skillName, functionName, ex.Message);
                context.Fail(ex.Message, ex);
            }

            return context;
        }

        return new SKFunction(
            kernel: kernel,
            delegateType: DelegateTypes.ContextSwitchInSKContextOutTaskSKContext,
            delegateFunction: LocalFunc,
            promptTemplate: functionConfig.PromptTemplate,
            parameters: functionConfig.PromptTemplate.GetParameters(),
            description: functionConfig.PromptTemplateConfig.Description,
            skillName: skillName,
            functionName: functionName,
            isSemantic: true,
            log: log);
    }

    /// <inheritdoc/>
    public FunctionView Describe()
    {
        return new FunctionView
        {
            IsSemantic = this.IsSemantic,
            Name = this.Name,
            SkillName = this.SkillName,
            Description = this.Description,
            Parameters = this.Parameters,
        };
    }

    /// <inheritdoc/>
    public Task<SKContext> InvokeAsync(
        string input,
        SKContext? context = null,
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        CompleteRequestSettings? settings = null,
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
        CompleteRequestSettings? settings = null,
=======
        JsonObject? settings = null,
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
        ILogger? log = null,
        CancellationToken cancellationToken = default)
    {
        if (context == null)
        {
            log ??= NullLogger.Instance;
            context = new SKContext(
                new ContextVariables("")
                // NullMemory.Instance,
                // this._skillCollection,
                // log,
                // cancellationToken
            );
        }

        context.Variables.Update(input);
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
    public async Task<SKContext> InvokeAsync(SKContext context, ITextCompletion? textCompletionService = null, CompleteRequestSettings? settings = null)
    {
        async Task<SKContext> InvokeSemanticAsync(SKContext contextParam, ITextCompletion? _aiService, CompleteRequestSettings? settingsParam)
        {
            if (_aiService == null)
            {
                throw new KernelException(KernelException.ErrorCodes.InvalidServiceConfiguration, "No text completion service provided for semantic function execution.");
            }

            var resultContext = await this._function(_aiService, settingsParam ?? this._aiRequestSettings, contextParam).ConfigureAwait(false);
            contextParam.Variables.Update(resultContext.Variables);
            return contextParam;
        }

        Task<SKContext> InvokeNativeAsync(SKContext contextParam, CompleteRequestSettings? settingsParam)
        {
            return this._function(null, settingsParam, contextParam);
        }

        // If the function is invoked manually, the user might have left out the skill collection
        //context.Skills ??= this._skillCollection;

        var validateContextResult = await this.TrustServiceInstance.ValidateContextAsync(this, context).ConfigureAwait(false);

        var result = this.IsSemantic
            ? await InvokeSemanticAsync(context, textCompletionService, settings).ConfigureAwait(false)
            : await InvokeNativeAsync(context, settings).ConfigureAwait(false);
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

        return this.InvokeAsync(context, settings, log, cancellationToken);
    }

    /// <inheritdoc/>
    public Task<SKContext> InvokeAsync(
        SKContext? context = null,
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        CompleteRequestSettings? settings = null,
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
        CompleteRequestSettings? settings = null,
=======
        JsonObject? settings = null,
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
        ILogger? log = null,
        CancellationToken cancellationToken = default)
    {
        if (context == null)
        {
            // log ??= NullLogger.Instance;
            // context = new SKContext(new ContextVariables(""), NullMemory.Instance, null, log, cancellationToken);
            context = new SKContext(new ContextVariables(""));
        }

        return this.IsSemantic
            ? this.InvokeSemanticAsync(context, settings, cancellationToken)
            : this.InvokeNativeAsync(context);
    }

    /// <inheritdoc/>
    public ISKFunction SetDefaultSkillCollection(IReadOnlySkillCollection skills)
    {
        this._skillCollection = skills;
        return this;
    }

    /// <inheritdoc/>
    public ISKFunction SetAIService(Func<ITextCompletion> serviceFactory)
    {
        Verify.NotNull(serviceFactory);
        this.VerifyIsSemantic();
        this._aiService = serviceFactory.Invoke();
        return this;
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
    }

    /// <inheritdoc/>
    public ISKFunction SetAIConfiguration(CompleteRequestSettings settings)
    {
        Verify.NotNull(settings);
        this.VerifyIsSemantic();
        this._aiRequestSettings = settings;
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
        string? input = null,
        ITextCompletion? textCompletionService = null,
        CompleteRequestSettings? settings = null,
        IReadOnlySkillCollection? skills = null,
        ISemanticTextMemory? memory = null,
        ILogger? logger = null,
        CancellationToken cancellationToken = default)
    {
        SKContext context = new(
            new ContextVariables(input),
            memory: memory,
            skills: skills,
            logger: logger,
            cancellationToken: cancellationToken);

        return this.InvokeAsync(context, textCompletionService, settings);
    }

    /// <inheritdoc/>
    public ISKFunction SetAIConfiguration(JsonObject settings)
    {
        Verify.NotNull(settings);
        this.VerifyIsSemantic();
        this._aiServiceSettings = settings;
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
        return this;
    }

    /// <summary>
    /// Dispose of resources.
    /// </summary>
    public void Dispose()
    {
        this.ReleaseUnmanagedResources();
        GC.SuppressFinalize(this);
    }

    /// <summary>
    /// Finalizer.
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
    /// JSON serialized string representation of the function.
    /// </summary>
    public override string ToString()
        => this.ToString(false);

    /// <summary>
    /// JSON serialized string representation of the function.
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
    /// </summary>
    ~SKFunction()
    {
        this.ReleaseUnmanagedResources();
    }

    #region private

    private IKernel _kernel;
    private readonly DelegateTypes _delegateType;
    private readonly Delegate _function;
    private readonly ILogger _log;
    private IReadOnlySkillCollection? _skillCollection;
    private ITextCompletion? _aiService = null;
    private CompleteRequestSettings _aiRequestSettings = new();
    private readonly IPromptTemplate _promptTemplate;
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
    private JsonObject _aiServiceSettings = new();
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

    private struct MethodDetails
    {
        public bool HasSkFunctionAttribute { get; set; }
        public DelegateTypes Type { get; set; }
        public Delegate Function { get; set; }
        public List<ParameterView> Parameters { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
    }

    internal enum DelegateTypes
    {
        Unknown = 0,
        Void = 1,
        OutString = 2,
        OutTaskString = 3,
        InSKContext = 4,
        InSKContextOutString = 5,
        InSKContextOutTaskString = 6,
        ContextSwitchInSKContextOutTaskSKContext = 7,
        InString = 8,
        InStringOutString = 9,
        InStringOutTaskString = 10,
        InStringAndContext = 11,
        InStringAndContextOutString = 12,
        InStringAndContextOutTaskString = 13,
        ContextSwitchInStringAndContextOutTaskContext = 14,
        InStringOutTask = 15,
        InContextOutTask = 16,
        InStringAndContextOutTask = 17,
        OutTask = 18
    }

    internal SKFunction(
        IKernel kernel,
        DelegateTypes delegateType,
        Delegate delegateFunction,
        IPromptTemplate promptTemplate,
        IList<ParameterView> parameters,
        string skillName,
        string functionName,
        string description,
        bool isSemantic = false,
        ILogger? log = null
    )
    {
        Verify.NotNull(kernel);
        Verify.NotNull(delegateFunction);
        Verify.ValidSkillName(skillName);
        Verify.ValidFunctionName(functionName);
        Verify.ParametersUniqueness(parameters);

        this._kernel = kernel;

        this._log = log ?? NullLogger.Instance;

        this._delegateType = delegateType;
        this._function = delegateFunction;
        this._promptTemplate = promptTemplate;
        this.Parameters = parameters;

        this.IsSemantic = isSemantic;
        this.Name = functionName;
        this.SkillName = skillName;
        this.Description = description;
    }

    private void ReleaseUnmanagedResources()
    {
        if (this._aiService is not IDisposable disposable) { return; }

        disposable.Dispose();
    }

    /// <summary>
    /// Throw an exception if the function is not semantic, use this method when some logic makes sense only for semantic functions.
    /// </summary>
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    /// <exception cref="KernelException"></exception>
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
    /// <exception cref="KernelException"></exception>
=======
    /// <exception cref="SKException"></exception>
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
    private void VerifyIsSemantic()
    {
        if (this.IsSemantic) { return; }

        this._log.LogError("The function is not semantic");
        throw new KernelException(
            KernelException.ErrorCodes.InvalidFunctionType,
            "Invalid operation, the method requires a semantic function");
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
        this._logger.LogError("The function is not semantic");
        throw new SKException("Invalid operation, the method requires a semantic function");
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
    }

    // Run the semantic function
    private async Task<SKContext> InvokeSemanticAsync(
        SKContext context,
        CompleteRequestSettings? settings,
        CancellationToken cancellationToken)
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
    private async Task<SKContext> InvokeSemanticAsync(SKContext context, JsonObject? settings)
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
    {
        this.VerifyIsSemantic();

        // this.EnsureContextHasSkills(context);

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        settings ??= this._aiRequestSettings;
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
        settings ??= this._aiRequestSettings;
=======
        settings ??= this._aiServiceSettings;
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

        var callable = (Func<
            IKernel,
            ITextCompletion?,
            CompleteRequestSettings?,
            SKContext,
            IPromptTemplate,
            string,
            string,
            CancellationToken,
            Task<SKContext>
        >)this._function;

        SKContext? result = await callable(
            this._kernel,
            this._aiService,
            settings,
            context,
            this._promptTemplate,
            this.SkillName,
            this.Name,
            cancellationToken
        ).ConfigureAwait(false);

        context.Variables.Update(result.Variables);

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
        var callable = (Func<ITextCompletion?, JsonObject?, SKContext, Task<SKContext>>)this._function;
        context.Variables.Update((await callable(this._aiService, settings, context).ConfigureAwait(false)).Variables);
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
        return context;
    }

    // Run the native function
    private async Task<SKContext> InvokeNativeAsync(SKContext context)
    {
        TraceFunctionTypeCall(this._delegateType, this._log);

        // this.EnsureContextHasSkills(context);

        switch (this._delegateType)
        {
            case DelegateTypes.Void: // 1
            {
                var callable = (Action)this._function;
                callable();
                return context;
            }

            case DelegateTypes.OutString: // 2
            {
                var callable = (Func<string>)this._function;
                context.Variables.Update(callable());
                return context;
            }

            case DelegateTypes.OutTaskString: // 3
            {
                var callable = (Func<Task<string>>)this._function;
                context.Variables.Update(await callable().ConfigureAwait(false));
                return context;
            }

            case DelegateTypes.InSKContext: // 4
            {
                var callable = (Action<SKContext>)this._function;
                callable(context);
                return context;
            }

            case DelegateTypes.InSKContextOutString: // 5
            {
                var callable = (Func<SKContext, string>)this._function;
                context.Variables.Update(callable(context));
                return context;
            }

            case DelegateTypes.InSKContextOutTaskString: // 6
            {
                var callable = (Func<SKContext, Task<string>>)this._function;
                context.Variables.Update(await callable(context).ConfigureAwait(false));
                return context;
            }

            case DelegateTypes.ContextSwitchInSKContextOutTaskSKContext: // 7
            {
                var callable = (Func<SKContext, Task<SKContext>>)this._function;
                // Note: Context Switching: allows the function to replace with a new context, e.g. to branch execution path
                context = await callable(context).ConfigureAwait(false);
                return context;
            }

            case DelegateTypes.InString:
            {
                var callable = (Action<string>)this._function; // 8
                callable(context.Variables.Input);
                return context;
            }

            case DelegateTypes.InStringOutString: // 9
            {
                var callable = (Func<string, string>)this._function;
                context.Variables.Update(callable(context.Variables.Input));
                return context;
            }

            case DelegateTypes.InStringOutTaskString: // 10
            {
                var callable = (Func<string, Task<string>>)this._function;
                context.Variables.Update(await callable(context.Variables.Input).ConfigureAwait(false));
                return context;
            }

            case DelegateTypes.InStringAndContext: // 11
            {
                var callable = (Action<string, SKContext>)this._function;
                callable(context.Variables.Input, context);
                return context;
            }

            case DelegateTypes.InStringAndContextOutString: // 12
            {
                var callable = (Func<string, SKContext, string>)this._function;
                context.Variables.Update(callable(context.Variables.Input, context));
                return context;
            }

            case DelegateTypes.InStringAndContextOutTaskString: // 13
            {
                var callable = (Func<string, SKContext, Task<string>>)this._function;
                context.Variables.Update(await callable(context.Variables.Input, context).ConfigureAwait(false));
                return context;
            }

            case DelegateTypes.ContextSwitchInStringAndContextOutTaskContext: // 14
            {
                var callable = (Func<string, SKContext, Task<SKContext>>)this._function;
                // Note: Context Switching: allows the function to replace with a new context, e.g. to branch execution path
                context = await callable(context.Variables.Input, context).ConfigureAwait(false);
                return context;
            }

            case DelegateTypes.InStringOutTask: // 15
            {
                var callable = (Func<string, Task>)this._function;
                await callable(context.Variables.Input).ConfigureAwait(false);
                return context;
            }

            case DelegateTypes.InContextOutTask: // 16
            {
                var callable = (Func<SKContext, Task>)this._function;
                await callable(context).ConfigureAwait(false);
                return context;
            }

            case DelegateTypes.InStringAndContextOutTask: // 17
            {
                var callable = (Func<string, SKContext, Task>)this._function;
                await callable(context.Variables.Input, context).ConfigureAwait(false);
                return context;
            }

            case DelegateTypes.OutTask: // 18
            {
                var callable = (Func<Task>)this._function;
                await callable().ConfigureAwait(false);
                return context;
            }

            case DelegateTypes.Unknown:
            default:
                throw new KernelException(
                    KernelException.ErrorCodes.FunctionTypeNotSupported,
                    "Invalid function type detected, unable to execute.");
        }
    }

    // private void EnsureContextHasSkills(SKContext context)
    // {
    //     // If the function is invoked manually, the user might have left out the skill collection
    //     context.Skills ??= this._skillCollection;
    // }

    private static MethodDetails GetMethodDetails(
        MethodInfo methodSignature,
        object? methodContainerInstance,
        bool skAttributesRequired = true,
        ILogger? log = null)
    {
        Verify.NotNull(methodSignature);

        var result = new MethodDetails
        {
            Name = methodSignature.Name,
            Parameters = new List<ParameterView>(),
        };

        // SKFunction attribute
        SKFunctionAttribute? skFunctionAttribute = methodSignature
            .GetCustomAttributes(typeof(SKFunctionAttribute), true)
            .Cast<SKFunctionAttribute>()
            .FirstOrDefault();

        result.HasSkFunctionAttribute = skFunctionAttribute != null;

        if (!result.HasSkFunctionAttribute || skFunctionAttribute == null)
        {
            log?.LogTrace("Method '{0}' doesn't have '{1}' attribute", result.Name, typeof(SKFunctionAttribute).Name);
            if (skAttributesRequired) { return result; }
        }
        else
        {
            result.HasSkFunctionAttribute = true;
        }

        (result.Type, result.Function, bool hasStringParam) = GetDelegateInfo(methodContainerInstance, methodSignature);

        // SKFunctionName attribute
        SKFunctionNameAttribute? skFunctionNameAttribute = methodSignature
            .GetCustomAttributes(typeof(SKFunctionNameAttribute), true)
            .Cast<SKFunctionNameAttribute>()
            .FirstOrDefault();

        if (skFunctionNameAttribute != null)
        {
            result.Name = skFunctionNameAttribute.Name;
        }

        // SKFunctionInput attribute
        SKFunctionInputAttribute? skMainParam = methodSignature
            .GetCustomAttributes(typeof(SKFunctionInputAttribute), true)
            .Cast<SKFunctionInputAttribute>()
            .FirstOrDefault();

        // SKFunctionContextParameter attribute
        IList<SKFunctionContextParameterAttribute> skContextParams = methodSignature
            .GetCustomAttributes(typeof(SKFunctionContextParameterAttribute), true)
            .Cast<SKFunctionContextParameterAttribute>().ToList();

        // Handle main string param description, if available/valid
        // Note: Using [SKFunctionInput] is optional
        if (hasStringParam)
        {
            result.Parameters.Add(skMainParam != null
                ? skMainParam.ToParameterView() // Use the developer description
                : new ParameterView { Name = "input", Description = "Input string", DefaultValue = "" }); // Use a default description
        }
        else if (skMainParam != null)
        {
            // The developer used [SKFunctionInput] on a function that doesn't support a string input
            var message = $"The method '{result.Name}' doesn't have a string parameter, do not use '{typeof(SKFunctionInputAttribute).Name}' attribute.";
            throw new KernelException(KernelException.ErrorCodes.InvalidFunctionDescription, message);
        }

        // Handle named arg passed via the SKContext object
        // Note: "input" is added first to the list, before context params
        // Note: Using [SKFunctionContextParameter] is optional
        result.Parameters.AddRange(skContextParams.Select(x => x.ToParameterView()));

        // Check for param names conflict
        // Note: the name "input" is reserved for the main parameter
        Verify.ParametersUniqueness(result.Parameters);

        result.Description = skFunctionAttribute?.Description ?? "";

        log?.LogTrace("Method '{0}' found, type `{1}`", result.Name, result.Type.ToString("G"));
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
            bool fallBackToInput = !sawFirstParameter && !nameIsInput;
            Func<SKContext, CancellationToken, object?> parameterFunc = (SKContext context, CancellationToken _) =>
            {
                // 1. Use the value of the variable if it exists.
                if (context.Variables.TryGetValue(name, out string? value))
                {
                    return Process(value);
                }

                // 2. Otherwise, use the default value if there is one, sourced either from an attribute or the parameter's default.
                if (hasDefaultValue)
                {
                    return defaultValue;
                }

                // 3. Otherwise, use "input" if this is the first (or only) parameter.
                if (fallBackToInput)
                {
                    return Process(context.Variables.Input);
                }

                // 4. Otherwise, fail.
                throw new SKException($"Missing value for parameter '{name}'");

                object? Process(string value)
                {
                    if (type == typeof(string))
                    {
                        return value;
                    }

                    try
                    {
                        return parser(value, context.Culture);
                    }
                    catch (Exception e) when (!e.IsCriticalException())
                    {
                        throw new ArgumentOutOfRangeException(name, value, e.Message);
                    }
                }
            };

            sawFirstParameter = true;

            var parameterView = new ParameterView(
                name,
                parameter.GetCustomAttribute<DescriptionAttribute>(inherit: true)?.Description ?? string.Empty,
                defaultValue?.ToString() ?? string.Empty);

            return (parameterFunc, parameterView);
        }
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

        return result;
    }

    // Inspect a method and returns the corresponding delegate and related info
    private static (DelegateTypes type, Delegate function, bool hasStringParam) GetDelegateInfo(object? instance, MethodInfo method)
    {
        if (EqualMethods(instance, method, typeof(Action), out Delegate? funcDelegate))
        {
            return (DelegateTypes.Void, funcDelegate, false);
        }

        if (EqualMethods(instance, method, typeof(Func<string>), out funcDelegate))
        {
            return (DelegateTypes.OutString, funcDelegate, false);
        }

        if (EqualMethods(instance, method, typeof(Func<Task<string>>), out funcDelegate!))
        {
            return (DelegateTypes.OutTaskString, funcDelegate, false);
        }

        if (EqualMethods(instance, method, typeof(Action<SKContext>), out funcDelegate!))
        {
            return (DelegateTypes.InSKContext, funcDelegate, false);
        }

        if (EqualMethods(instance, method, typeof(Func<SKContext, string>), out funcDelegate!))
        {
            return (DelegateTypes.InSKContextOutString, funcDelegate, false);
        }

        if (EqualMethods(instance, method, typeof(Func<SKContext, Task<string>>), out funcDelegate!))
        {
            return (DelegateTypes.InSKContextOutTaskString, funcDelegate, false);
        }

        if (EqualMethods(instance, method, typeof(Func<SKContext, Task<SKContext>>), out funcDelegate!))
        {
            return (DelegateTypes.ContextSwitchInSKContextOutTaskSKContext, funcDelegate, false);
        }

        // === string input ==

        if (EqualMethods(instance, method, typeof(Action<string>), out funcDelegate!))
        {
            return (DelegateTypes.InString, funcDelegate, true);
        }

        if (EqualMethods(instance, method, typeof(Func<string, string>), out funcDelegate!))
        {
            return (DelegateTypes.InStringOutString, funcDelegate, true);
        }

        if (EqualMethods(instance, method, typeof(Func<string, Task<string>>), out funcDelegate!))
        {
            return (DelegateTypes.InStringOutTaskString, funcDelegate, true);
        }

        if (EqualMethods(instance, method, typeof(Action<string, SKContext>), out funcDelegate!))
        {
            return (DelegateTypes.InStringAndContext, funcDelegate, true);
        }

        if (EqualMethods(instance, method, typeof(Func<string, SKContext, string>), out funcDelegate!))
        {
            return (DelegateTypes.InStringAndContextOutString, funcDelegate, true);
        }

        if (EqualMethods(instance, method, typeof(Func<string, SKContext, Task<string>>), out funcDelegate!))
        {
            return (DelegateTypes.InStringAndContextOutTaskString, funcDelegate, true);
        }

        if (EqualMethods(instance, method, typeof(Func<string, SKContext, Task<SKContext>>), out funcDelegate!))
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
        // Unrecognized return type.
        throw GetExceptionForInvalidSignature(method, $"Unknown return type {returnType}");

        // Throws an exception if a result is found to be null unexpectedly
        static object ThrowIfNullResult(object? result) =>
            result ??
            throw new SKException("Function returned null unexpectedly.");
    }

    /// <summary>Gets an exception that can be thrown indicating an invalid signature.</summary>
    [DoesNotReturn]
    private static Exception GetExceptionForInvalidSignature(MethodInfo method, string reason) =>
        throw new SKException($"Function '{method.Name}' is not supported by the kernel. {reason}");

    /// <summary>Throws an exception indicating an invalid SKFunction signature if the specified condition is not met.</summary>
    private static void ThrowForInvalidSignatureIf([DoesNotReturnIf(true)] bool condition, MethodInfo method, string reason)
    {
        if (condition)
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
        {
            return (DelegateTypes.ContextSwitchInStringAndContextOutTaskContext, funcDelegate, true);
        }

        // == Tasks without output ==

        if (EqualMethods(instance, method, typeof(Func<string, Task>), out funcDelegate!))
        {
            return (DelegateTypes.InStringOutTask, funcDelegate, true);
        }

        if (EqualMethods(instance, method, typeof(Func<SKContext, Task>), out funcDelegate!))
        {
            return (DelegateTypes.InContextOutTask, funcDelegate, false);
        }

        if (EqualMethods(instance, method, typeof(Func<string, SKContext, Task>), out funcDelegate!))
        {
            return (DelegateTypes.InStringAndContextOutTask, funcDelegate, true);
        }

        if (EqualMethods(instance, method, typeof(Func<Task>), out funcDelegate!))
        {
            return (DelegateTypes.OutTask, funcDelegate, false);
        }

        // [SKContext DoSomething(SKContext context)] is not supported, use the async form instead.
        // If you encounter scenarios that require to interact with the context synchronously, please let us know.
        if (EqualMethods(instance, method, typeof(Func<SKContext, SKContext>), out _))
        {
            throw new KernelException(
                KernelException.ErrorCodes.FunctionTypeNotSupported,
                $"Function '{method.Name}' has an invalid signature 'Func<SKContext, SKContext>'. " +
                "Please use 'Func<SKContext, Task<SKContext>>' instead.");
        }

        throw new KernelException(
            KernelException.ErrorCodes.FunctionTypeNotSupported,
            $"Function '{method.Name}' has an invalid signature not supported by the kernel.");
    }

    /// <summary>
    /// Compare a method against the given signature type using Delegate.CreateDelegate.
    /// </summary>
    /// <param name="instance">Optional object containing the given method</param>
    /// <param name="userMethod">Method to inspect</param>
    /// <param name="delegateDefinition">Definition of the delegate, i.e. method signature</param>
    /// <param name="result">The delegate to use, if the function returns TRUE, otherwise NULL</param>
    /// <returns>True if the method to inspect matches the delegate type</returns>
    [SuppressMessage("Maintainability", "CA1508:Avoid dead conditional code", Justification = "Delegate.CreateDelegate can return NULL")]
    private static bool EqualMethods(
        object? instance,
        MethodInfo userMethod,
        Type delegateDefinition,
        [NotNullWhen(true)] out Delegate? result)
    {
        // Instance methods
        if (instance != null)
        {
            result = Delegate.CreateDelegate(delegateDefinition, instance, userMethod, false);
            if (result != null) { return true; }
        }

        // Static methods
        result = Delegate.CreateDelegate(delegateDefinition, userMethod, false);

        return result != null;
    }

    // Internal event to count (and test) that the correct delegates are invoked
    private static void TraceFunctionTypeCall(DelegateTypes type, ILogger log)
    {
        log.Log(
            LogLevel.Trace,
            new EventId((int)type, $"FuncType{type}"),
            "Executing function type {0}: {1}", (int)type, type.ToString("G"));
    }

    #endregion
}
