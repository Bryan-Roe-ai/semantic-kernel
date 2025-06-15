// Copyright (c) Microsoft. All rights reserved.
using Azure.AI.Agents.Persistent;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Agents.AzureAI;
using Microsoft.SemanticKernel.ChatCompletion;

namespace GettingStarted.AzureAgents;

/// <summary>
/// Demonstrates using code-interpreter on <see cref="AzureAIAgent"/>.
/// Improved summary: Shows how to enable and use the code interpreter tool with an Azure AI agent to solve computational tasks in a conversation.
/// </summary>
public class Step04_AzureAIAgent_CodeInterpreter(ITestOutputHelper output) : BaseAzureAgentTest(output)
{
    [Fact]
    public async Task UseCodeInterpreterToolWithAgent()
    {
        // Define the agent
        PersistentAgent definition = await this.Client.Administration.CreateAgentAsync(
            TestConfiguration.AzureAI.ChatModelId,
            tools: [new CodeInterpreterToolDefinition()]);
        AzureAIAgent agent = new(definition, this.Client);

        // Create a thread for the agent conversation.
        AgentThread thread = new AzureAIAgentThread(this.Client, metadata: SampleMetadata);

        // Respond to user input
        try
        {
            await InvokeAgentAsync("Use code to determine the values in the Fibonacci sequence that that are less then the value of 101?");
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
