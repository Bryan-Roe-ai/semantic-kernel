

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

namespace Agents;

/// <summary>
/// Demonstrate <see cref="ChatCompletionAgent"/> agent interacts with
/// <see cref="OpenAIAssistantAgent"/> when it produces image output.
/// </summary>
public class MixedChat_Images(ITestOutputHelper output) : BaseAssistantTest(output)
{
    private const string AnalystName = "Analyst";
    private const string AnalystInstructions = "Create charts as requested without explanation.";

    private const string SummarizerName = "Summarizer";
    private const string SummarizerInstructions = "Summarize the entire conversation for the user in natural language.";

    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public async Task AnalyzeDataAndGenerateChartAsync(bool useChatClient)
    {
        // Define the assistant
        Assistant assistant =
            await this.AssistantClient.CreateAssistantAsync(
                this.Model,
                name: AnalystName,
                instructions: AnalystInstructions,
                enableCodeInterpreter: true,
                metadata: SampleMetadata);

        FileClient fileClient = provider.Client.GetFileClient();

        FileClient fileClient = provider.Client.GetFileClient();

        OpenAIFileClient fileClient = provider.Client.GetOpenAIFileClient();

        OpenAIFileClient fileClient = provider.Client.GetOpenAIFileClient();

        OpenAIFileClient fileClient = provider.Client.GetOpenAIFileClient();

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
                    Instructions = AnalystInstructions,
                    Name = AnalystName,
                    EnableCodeInterpreter = true,
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

        // Create the agent
        OpenAIAssistantAgent analystAgent = new(assistant, this.AssistantClient);

        ChatCompletionAgent summaryAgent =
            new()
            {
                Instructions = SummarizerInstructions,
                Name = SummarizerName,
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
                Graph the percentage of storm events by state using a pie chart:

                State, StormCount
                TEXAS, 4701
                KANSAS, 3166
                IOWA, 2337
                ILLINOIS, 2022
                MISSOURI, 2016
                GEORGIA, 1983
                MINNESOTA, 1881
                WISCONSIN, 1850
                NEBRASKA, 1766
                NEW YORK, 1750
                """);

            await InvokeAgentAsync(summaryAgent);
        }
        finally
        {
            await this.AssistantClient.DeleteAssistantAsync(analystAgent.Id);
        }

        chatClient?.Dispose();

        // Local function to invoke agent and display the conversation messages.
        async Task InvokeAgentAsync(Agent agent, string? input = null)
        {
            if (!string.IsNullOrWhiteSpace(input))
            {
                ChatMessageContent message = new(AuthorRole.User, input);
                chat.AddChatMessage(message);
                this.WriteAgentChatMessage(message);
            }

            await foreach (ChatMessageContent response in chat.InvokeAsync(agent))
            {
                this.WriteAgentChatMessage(response);
                await this.DownloadResponseImageAsync(response);
            }
        }
    }
}
