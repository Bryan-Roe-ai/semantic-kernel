// Copyright (c) Microsoft. All rights reserved.

using System;
using System.IO;
using System.Net;
using System.Threading.Tasks;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Orchestration;
using Microsoft.SemanticKernel.SkillDefinition;
using Microsoft.SemanticKernel.Orchestration;

namespace SemanticKernel.Functions
{
    /// <summary>
    /// KernelAIPluginRunner provides functionality for running AI plugins using Semantic Kernel.
    /// </summary>
    public class KernelAIPluginRunner
    {
        private readonly IKernel _kernel;

        /// <summary>
        /// Initializes a new instance of the KernelAIPluginRunner class.
        /// </summary>
        /// <param name="kernel">The Semantic Kernel instance</param>
        public KernelAIPluginRunner(IKernel kernel)
        {
            _kernel = kernel ?? throw new ArgumentNullException(nameof(kernel));
        }

        /// <summary>
        /// Runs an AI plugin function with the specified input.
        /// </summary>
        /// <param name="pluginName">Name of the plugin to run</param>
        /// <param name="functionName">Name of the function to execute</param>
        /// <param name="input">Optional input for the function. Defaults to an empty string.</param>
        /// <returns>Result of the plugin execution</returns>
        public async Task<string> RunPluginAsync(string pluginName, string functionName, string input = "")
        {
            ValidatePluginParameters(pluginName, functionName);

            var function = _kernel.Functions.GetFunction(pluginName, functionName);
            var context = _kernel.CreateNewContext();
            context.Variables.Update(input);
            var result = await function.InvokeAsync(context).ConfigureAwait(false);
            return result.GetValue<string>() ??= string.Empty;
        }

        /// <summary>
        /// Runs an AI plugin function with a pre-configured context.
        /// </summary>
        /// <param name="pluginName">Name of the plugin to run</param>
        /// <param name="functionName">Name of the function to execute</param>
        /// <param name="context">Pre-configured kernel context</param>
        /// <returns>Result of the plugin execution</returns>
        public async Task<string> RunPluginWithContextAsync(string pluginName, string functionName, SKContext context)
        {
            ValidatePluginParameters(pluginName, functionName);

            var function = _kernel.Functions.GetFunction(pluginName, functionName);
            var result = await function.InvokeAsync(context);
            return result.GetValue<string>() ?? string.Empty;
        }

        private static void ValidatePluginParameters(string pluginName, string functionName)
        {
            if (string.IsNullOrEmpty(pluginName))
            {
                throw new ArgumentException("Plugin name cannot be null or empty", nameof(pluginName));
            }

            if (string.IsNullOrEmpty(functionName))
            {
                throw new ArgumentException("Function name cannot be null or empty", nameof(functionName));
            }
        }
    }
}
