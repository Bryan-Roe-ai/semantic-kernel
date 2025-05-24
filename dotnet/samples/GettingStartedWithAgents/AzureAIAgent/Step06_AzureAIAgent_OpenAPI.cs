// Copyright (c) Microsoft. All rights reserved.
using Azure.AI.Projects;
using Azure.AI.Agents.Persistent;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents.AzureAI;
using Microsoft.SemanticKernel.ChatCompletion;
using Resources;

namespace GettingStarted.AzureAgents;

/// <summary>
/// Demonstrates invoking Open API functions using <see cref="AzureAIAgent" />.
/// Improved summary: Shows how to add OpenAPI tools to an Azure AI agent and interact with external APIs in a conversational workflow.
/// </summary>
/// <remarks>
/// Note: Open API invocation does not involve kernel function calling or kernel filters.
/// Azure Function invocation is managed entirely by the Azure AI Agent service.
/// </remarks>
public class Step06_AzureAIAgent_OpenAPI(ITestOutputHelper output) : BaseAzureAgentTest(output)
{
    [Fact]
    public async Task UseOpenAPIToolWithAgent()
    {
        // Retrieve Open API specifications
        string apiCountries = EmbeddedResource.Read("countries.json");
        string apiWeather = EmbeddedResource.Read("weather.json");

        // Define the agent
        PersistentAgent definition = await this.Client.Administration.CreateAgentAsync(
            TestConfiguration.AzureAI.ChatModelId,
            tools:
            [
                new OpenApiToolDefinition("RestCountries", "Retrieve country information", BinaryData.FromString(apiCountries), new OpenApiAnonymousAuthDetails()),
                new OpenApiToolDefinition("Weather", "Retrieve weather by location", BinaryData.FromString(apiWeather), new OpenApiAnonymousAuthDetails())
            ]);
        AzureAIAgent agent = new(definition, this.Client);

        // Create a thread for the agent conversation.
        Microsoft.SemanticKernel.Agents.AgentThread thread = new AzureAIAgentThread(this.Client, metadata: SampleMetadata);

        // Respond to user input
        try
        {
            await InvokeAgentAsync("What is the name and population of the country that uses currency with abbreviation THB");
            await InvokeAgentAsync("What is the weather in the capitol city of that country?");
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

// SKILL: Add OpenAPI invocation as a skill/feature to Semantic Kernel
namespace Microsoft.SemanticKernel.Skills.OpenAPI
{
    /// <summary>
    /// Provides a skill for invoking OpenAPI endpoints via AzureAIAgent.
    /// </summary>
    public static class OpenApiInvocationSkill
    {
        /// <summary>
        /// Invokes an OpenAPI endpoint using the provided agent and thread.
        /// </summary>
        /// <param name="agent">The AzureAIAgent instance.</param>
        /// <param name="thread">The conversation thread.</param>
        /// <param name="input">The user input or API query.</param>
        /// <returns>Task representing the asynchronous operation.</returns>
        public static async Task InvokeOpenApiAsync(AzureAIAgent agent, AgentThread thread, string input)
        {
            ChatMessageContent message = new(AuthorRole.User, input);
            await foreach (ChatMessageContent response in agent.InvokeAsync(message, thread))
            {
                // Optionally, handle or log the response here
            }
        }
    }
}
