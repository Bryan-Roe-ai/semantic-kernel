// Copyright (c) Microsoft. All rights reserved.
using Azure.AI.Projects;
using Azure.AI.Agents.Persistent;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents.AzureAI;
using Microsoft.SemanticKernel.ChatCompletion;
using Resources;

namespace Agents;

/// <summary>
/// Demonstrates using code-interpreter to manipulate and generate CSV files with <see cref="AzureAIAgent"/>.
/// Improved summary: This sample shows how to upload a CSV, create an agent, and interact with it to analyze and generate reports from the data using Azure AI's code interpreter capabilities.
/// </summary>
public class AzureAIAgent_FileManipulation(ITestOutputHelper output) : BaseAzureAgentTest(output)
{
    [Fact]
    public async Task AnalyzeCSVFileUsingAzureAIAgentAsync()
    {
        await using Stream stream = EmbeddedResource.ReadStream("sales.csv")!;
        PersistentAgentFileInfo fileInfo = await this.Client.Files.UploadFileAsync(stream, PersistentAgentFilePurpose.Agents, "sales.csv");

        // Define the agent
        PersistentAgent definition = await this.Client.Administration.CreateAgentAsync(
            TestConfiguration.AzureAI.ChatModelId,
            tools: [new CodeInterpreterToolDefinition()],
            toolResources:
                new()
                {
                    CodeInterpreter = new()
                    {
                        FileIds = { fileInfo.Id },
                    }
                });
        AzureAIAgent agent = new(definition, this.Client);
        AzureAIAgentThread thread = new(this.Client);

        // Respond to user input
        try
        {
            await InvokeAgentAsync("Which segment had the most sales?");
            await InvokeAgentAsync("List the top 5 countries that generated the most profit.");
            await InvokeAgentAsync("Create a tab delimited file report of profit by each country per month.");
        }
        finally
        {
            await thread.DeleteAsync();
            await this.Client.Administration.DeleteAgentAsync(agent.Id);
            await this.Client.Files.DeleteFileAsync(fileInfo.Id);
        }

        // Local function to invoke agent and display the conversation messages.
        async Task InvokeAgentAsync(string input)
        {
            ChatMessageContent message = new(AuthorRole.User, input);
            this.WriteAgentChatMessage(message);

            await foreach (ChatMessageContent response in agent.InvokeAsync(message, thread))
            {
                this.WriteAgentChatMessage(response);
                await this.DownloadContentAsync(response);
            }
        }
    }
}
