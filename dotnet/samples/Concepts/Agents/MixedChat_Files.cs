

﻿// Copyright (c) Microsoft. All rights reserved.

﻿// Copyright (c) Microsoft. All rights reserved.

// Copyright (c) Microsoft. All rights reserved.

// Copyright (c) Microsoft. All rights reserved.

// Copyright (c) Microsoft. All rights reserved.

using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Agents.OpenAI;
using Microsoft.SemanticKernel.ChatCompletion;
using OpenAI.Assistants;
using Resources;

namespace Agents;

/// <summary>
/// Demonstrate <see cref="ChatCompletionAgent"/> agent interacts with
/// <see cref="OpenAIAssistantAgent"/> when it produces file output.
/// </summary>
public class MixedChat_Files(ITestOutputHelper output) : BaseAssistantTest(output)
{
    private const string SummaryInstructions = "Summarize the entire conversation for the user in natural language.";

    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public async Task AnalyzeFileAndGenerateReport(bool useChatClient)
    {
        OpenAIClientProvider provider = this.GetClientProvider();

        FileClient fileClient = provider.Client.GetFileClient();

        OpenAIFileInfo uploadFile =

        FileClient fileClient = provider.Client.GetFileClient();

        OpenAIFileInfo uploadFile =

        OpenAIFileClient fileClient = provider.Client.GetOpenAIFileClient();

        OpenAIFile uploadFile =

        OpenAIFileClient fileClient = provider.Client.GetOpenAIFileClient();

        OpenAIFile uploadFile =

        OpenAIFileClient fileClient = provider.Client.GetOpenAIFileClient();

        OpenAIFile uploadFile =

            await fileClient.UploadFileAsync(
                new BinaryData(await EmbeddedResource.ReadAllAsync("30-user-context.txt")),
                "30-user-context.txt",
                FileUploadPurpose.Assistants);

        Console.WriteLine(this.ApiKey);

        // Define the agents
        OpenAIAssistantAgent analystAgent =
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
                    CodeInterpreterFileIds = [uploadFile.Id], // Associate uploaded file with assistant code-interpreter
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

        await using Stream stream = EmbeddedResource.ReadStream("30-user-context.txt")!;
        string fileId = await this.Client.UploadAssistantFileAsync(stream, "30-user-context.txt");

        // Define the agents
        // Define the assistant
        Assistant assistant =
            await this.AssistantClient.CreateAssistantAsync(
                this.Model,
                enableCodeInterpreter: true,
                codeInterpreterFileIds: [fileId],
                metadata: SampleMetadata);

        // Create the agent
        OpenAIAssistantAgent analystAgent = new(assistant, this.AssistantClient);

        ChatCompletionAgent summaryAgent =
            new()
            {
                Instructions = SummaryInstructions,
                Kernel = this.CreateKernelWithChatCompletion(useChatClient, out var chatClient),
            };

        // Create a chat for agent interaction.
        AgentGroupChat chat = new();

        // Respond to user input
        try
        {
            await InvokeAgentAsync(
                analystAgent,
                """
                Create a tab delimited file report of the ordered (descending) frequency distribution
                of words in the file '30-user-context.txt' for any words used more than once.
                """);
            await InvokeAgentAsync(summaryAgent);
        }
        finally
        {
            await this.AssistantClient.DeleteAssistantAsync(analystAgent.Id);
            await this.Client.DeleteFileAsync(fileId);
        }

        chatClient?.Dispose();

        // Local function to invoke agent and display the conversation messages.
        async Task InvokeAgentAsync(Agent agent, string? input = null)
        {
            if (!string.IsNullOrWhiteSpace(input))
            {
                ChatMessageContent message = new(AuthorRole.User, input);
                chat.AddChatMessage(new(AuthorRole.User, input));
                this.WriteAgentChatMessage(message);
            }

            await foreach (ChatMessageContent response in chat.InvokeAsync(agent))
            {
                this.WriteAgentChatMessage(response);
                await this.DownloadResponseContentAsync(response);
            }
        }
    }
}
