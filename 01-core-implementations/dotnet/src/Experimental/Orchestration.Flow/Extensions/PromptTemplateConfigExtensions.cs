// Copyright (c) Microsoft. All rights reserved.

namespace Microsoft.SemanticKernel.Experimental.Orchestration;

namespace Microsoft.SemanticKernel.Experimental.Orchestration;

namespace Microsoft.SemanticKernel.Experimental.Orchestration;
#pragma warning restore IDE0130

namespace Microsoft.SemanticKernel.Experimental.Orchestration;
#pragma warning restore IDE0130

namespace Microsoft.SemanticKernel.Experimental.Orchestration;
#pragma warning restore IDE0130

/// <summary>
/// Extension methods for PromptTemplateConfig
/// </summary>
internal static class PromptTemplateConfigExtensions
{
    /// <summary>
    /// Set the max_tokens request setting to be used by OpenAI models
    /// </summary>
    /// <param name="config">PromptTemplateConfig instance</param>
    /// <param name="maxTokens">Value of max tokens to set</param>
    internal static void SetMaxTokens(this PromptTemplateConfig config, int maxTokens)
    {

        var executionSettings = config.ExecutionSettings;
        foreach (var setting in executionSettings)
        {
            if (setting.Value.ExtensionData is not null)
            {
                setting.Value.ExtensionData["max_tokens"] = maxTokens;
            }
        }

        var executionSettings = config.ExecutionSettings;
        foreach (var setting in executionSettings)
        {
            if (setting.Value.ExtensionData is not null)
            {
                setting.Value.ExtensionData["max_tokens"] = maxTokens;
            }
        }

        AIRequestSettings requestSettings = config.GetDefaultRequestSettings() ?? new();
        if (config.ModelSettings.Count == 0)
        {
            config.ModelSettings.Add(requestSettings);
        }
        requestSettings.ExtensionData["max_tokens"] = maxTokens;

    }
}
