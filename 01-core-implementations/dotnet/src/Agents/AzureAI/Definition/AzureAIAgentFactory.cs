// Copyright (c) Microsoft. All rights reserved.

using System.Diagnostics.CodeAnalysis;
using System.Threading;
using System.Threading.Tasks;
using Azure.AI.Agents.Persistent;

namespace Microsoft.SemanticKernel.Agents.AzureAI;

/// <summary>
/// Provides a <see cref="AgentFactory"/> which creates instances of <see cref="AzureAIAgent"/>.
/// </summary>
[Experimental("SKEXP0110")]
public sealed class AzureAIAgentFactory : AgentFactory
{
    /// <summary>
    /// The type of the Azure AI agent.
    /// </summary>
    public const string AzureAIAgentType = "foundry_agent";

    /// <summary>
    /// Initializes a new instance of the <see cref="AzureAIAgentFactory"/> class.
    /// </summary>
    public AzureAIAgentFactory()
        : base([AzureAIAgentType])
    {
    }

    /// <inheritdoc/>
    public override async Task<Agent?> TryCreateAsync(Kernel kernel, AgentDefinition agentDefinition, AgentCreationOptions? agentCreationOptions = null, CancellationToken cancellationToken = default)
    {
        Verify.NotNull(agentDefinition);

        if (agentDefinition.Type?.Equals(AzureAIAgentType, System.StringComparison.Ordinal) ?? false)
        {
            var client = agentDefinition.GetAgentsClient(kernel);

            PersistentAgent agent;
            if (!string.IsNullOrEmpty(agentDefinition.Id))
            {
                // Get an existing agent
                agent = await client.Administration.GetAgentAsync(
                    agentDefinition.Id,
                    cancellationToken: cancellationToken).ConfigureAwait(false);

                return new AzureAIAgent(agent, client)
                {
                    Kernel = kernel,
                    Arguments = agentDefinition.GetDefaultKernelArguments(kernel) ?? [],
                    Template = agentDefinition.GetPromptTemplate(kernel, agentCreationOptions?.PromptTemplateFactory),
                    Instructions = agentDefinition.Instructions ?? agent.Instructions,
                };
            }

            // Create a new agent
            Verify.NotNull(agentDefinition.Model);
            Verify.NotNull(agentDefinition.Model.Id);

            agent = await client.Administration.CreateAgentAsync(
                model: agentDefinition.Model.Id,
                name: agentDefinition.Name,
                description: agentDefinition.Description,
                instructions: agentDefinition.Instructions,
                tools: agentDefinition.GetAzureToolDefinitions(kernel),
                toolResources: agentDefinition.GetAzureToolResources(),
                metadata: agentDefinition.GetMetadata(),
                cancellationToken: cancellationToken).ConfigureAwait(false);

            return new AzureAIAgent(agent, client)
            {
                Kernel = kernel,
                Arguments = agentDefinition.GetDefaultKernelArguments(kernel) ?? [],
                Template = agentDefinition.GetPromptTemplate(kernel, agentCreationOptions?.PromptTemplateFactory),
            };
        }

        return null;
    }
}
