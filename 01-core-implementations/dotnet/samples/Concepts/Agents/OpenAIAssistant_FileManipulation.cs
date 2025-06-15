

﻿// Copyright (c) Microsoft. All rights reserved.

// Copyright (c) Microsoft. All rights reserved.
using System.Text;

// Copyright (c) Microsoft. All rights reserved.
using System.Text;

// Copyright (c) Microsoft. All rights reserved.
using System.Text;

// Copyright (c) Microsoft. All rights reserved.

using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Agents.OpenAI;
using Microsoft.SemanticKernel.ChatCompletion;
using OpenAI.Assistants;
using Resources;

namespace Agents;

/// <summary>
/// Demonstrate using code-interpreter to manipulate and generate csv files with <see cref="OpenAIAssistantAgent"/> .
/// </summary>
public class OpenAIAssistant_FileManipulation(ITestOutputHelper output) : BaseAssistantTest(output)
{
    [Fact]
    public async Task RunAsync()
    public async Task AnalyzeCSVFileUsingOpenAIAssistantAgentAsync()
    {
        await using Stream stream = EmbeddedResource.ReadStream("sales.csv")!;
        string fileId = await this.Client.UploadAssistantFileAsync(stream, "sales.csv");

        FileClient fileClient = provider.Client.GetFileClient();

        OpenAIFileInfo uploadFile =

        FileClient fileClient = provider.Client.GetFileClient();

        OpenAIFileInfo uploadFile =

        OpenAIFileClient fileClient = provider.Client.GetOpenAIFileClient();

        OpenAIFile uploadFile =

        OpenAIFileClient fileClient = provider.Client.GetOpenAIFileClient();

        OpenAIFile uploadFile =

            await fileClient.UploadFileAsync(
                new BinaryData(await EmbeddedResource.ReadAllAsync("sales.csv")!),
                "sales.csv",
                FileUploadPurpose.Assistants);

        // Define the agent
        OpenAIAssistantAgent agent =
            await OpenAIAssistantAgent.CreateAsync(

                kernel: new(),
                provider,
                new(this.Model)

                kernel: new(),
                provider,
                new(this.Model)

                provider,
                definition: new OpenAIAssistantDefinition(this.Model)
                kernel: new(),
                provider,
                new(this.Model)
                provider,
                definition: new OpenAIAssistantDefinition(this.Model)

                {
                    EnableCodeInterpreter = true,
                    CodeInterpreterFileIds = [uploadFile.Id],
                    Metadata = AssistantSampleMetadata,

                });

                });

                });

                });

                },
                kernel: new Kernel());
                });
                },
                kernel: new Kernel());

        // Create a chat for agent interaction.
        AgentGroupChat chat = new();
        var chat = new AgentGroupChat();

        // Define the assistant
        Assistant assistant =
            await this.AssistantClient.CreateAssistantAsync(
                this.Model,
                enableCodeInterpreter: true,
                codeInterpreterFileIds: [fileId],
                metadata: SampleMetadata);

        // Create the agent
        OpenAIAssistantAgent agent = new(assistant, this.AssistantClient);
        AgentThread? agentThread = null;

        // Respond to user input
        try
        {
            await InvokeAgentAsync("Which segment had the most sales?");
            await InvokeAgentAsync("List the top 5 countries that generated the most profit.");
            await InvokeAgentAsync("Create a tab delimited file report of profit by each country per month.");
        }
        finally
        {
            if (agentThread is not null)
            {
                await agentThread.DeleteAsync();
            }

            await this.AssistantClient.DeleteAssistantAsync(agent.Id);
            await this.Client.DeleteFileAsync(fileId);
        }

        // Local function to invoke agent and display the conversation messages.
        async Task InvokeAgentAsync(string input)
        {
            ChatMessageContent message = new(AuthorRole.User, input);
            this.WriteAgentChatMessage(message);

            await foreach (AgentResponseItem<ChatMessageContent> response in agent.InvokeAsync(message))
            {

                this.WriteAgentChatMessage(response);

                await this.DownloadResponseContentAsync(fileClient, response);

                this.WriteAgentChatMessage(response);
                await this.DownloadResponseContentAsync(fileClient, response);

                this.WriteAgentChatMessage(response);
                await this.DownloadResponseContentAsync(fileClient, response);

                Console.WriteLine($"# {content.Role} - {content.AuthorName ?? "*"}: '{content.Content}'");

                foreach (AnnotationContent annotation in content.Items.OfType<AnnotationContent>())
            await foreach (var content in chat.InvokeAsync(agent))
            {
                Console.WriteLine($"# {content.Role} - {content.AuthorName ?? "*"}: '{content.Content}'");

                foreach (var annotation in content.Items.OfType<AnnotationContent>())
                {
                    Console.WriteLine($"\n* '{annotation.Quote}' => {annotation.FileId}");
                    BinaryContent fileContent = await fileService.GetFileContentAsync(annotation.FileId!);
                    byte[] byteContent = fileContent.Data?.ToArray() ?? [];
                    Console.WriteLine(Encoding.Default.GetString(byteContent));
                }

                this.WriteAgentChatMessage(response);
                await this.DownloadResponseContentAsync(fileClient, response);

                this.WriteAgentChatMessage(response);
                await this.DownloadResponseContentAsync(fileClient, response);

                this.WriteAgentChatMessage(response);
                await this.DownloadResponseContentAsync(fileClient, response);

                await this.DownloadResponseContentAsync(response);

                agentThread = response.Thread;

            }
        }
    }
}
