// Copyright (c) Microsoft. All rights reserved.
using Azure.AI.Agents.Persistent;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Agents.AzureAI;
using Microsoft.SemanticKernel.ChatCompletion;
using Plugins;

namespace GettingStarted.AzureAgents;

/// <summary>
/// Demonstrates how to define function tools for an <see cref="AzureAIAgent"/> when the agent is created.
/// Improved summary: Shows how to add function tools to an Azure AI agent, retrieve the agent, and dynamically check required tools for conversational tasks.
/// </summary>
public class Step07_AzureAIAgent_Functions(ITestOutputHelper output) : BaseAzureAgentTest(output)
{
    private const string HostName = "Host";
    private const string HostInstructions = "Answer questions about the menu.";

    [Fact]
    public async Task UseSingleAgentWithFunctionTools()
    {
        // Define the agent
        // In this sample the function tools are added to the agent this is
        // important if you want to retrieve the agent later and then dynamically check
        // what function tools it requires.
        KernelPlugin plugin = KernelPluginFactory.CreateFromType<MenuPlugin>();
        var tools = plugin.Select(f => f.ToToolDefinition(plugin.Name));

        PersistentAgent definition = await this.Client.Administration.CreateAgentAsync(
            model: TestConfiguration.AzureAI.ChatModelId,
            name: HostName,
            description: null,
            instructions: HostInstructions,
            tools: tools);
        AzureAIAgent agent = new(definition, this.Client);

        // Add plugin to the agent's Kernel (same as direct Kernel usage).
        agent.Kernel.Plugins.Add(plugin);

        // Create a thread for the agent conversation.
        AgentThread thread = new AzureAIAgentThread(this.Client, metadata: SampleMetadata);

        // Respond to user input
        try
        {
            await InvokeAgentAsync("Hello");
            await InvokeAgentAsync("What is the special soup and its price?");
            await InvokeAgentAsync("What is the special drink and its price?");
            await InvokeAgentAsync("Thank you");
        }
        finally
        {
            await thread.DeleteAsync();
            await this.Client.Administration.DeleteAgentAsync(agent.Id);
        }

        // Local function to invoke agent and display the conversation messages.
        async Task InvokeAgentAsync(string input)
        {
            ChatMessageContent message = new(AuthorRole.User, input);
            this.WriteAgentChatMessage(message);

            await foreach (ChatMessageContent response in agent.InvokeAsync(message, thread))
            {
                this.WriteAgentChatMessage(response);
            }
        }
    }
}
