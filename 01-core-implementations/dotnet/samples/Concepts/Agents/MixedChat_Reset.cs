

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
/// Demonstrate the use of <see cref="AgentChat.ResetAsync"/>.
/// </summary>
public class MixedChat_Reset(ITestOutputHelper output) : BaseAssistantTest(output)
{
    private const string AgentInstructions =
        """
        The user may either provide information or query on information previously provided.
        If the query does not correspond with information provided, inform the user that their query cannot be answered.
        """;

    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public async Task ResetChat(bool useChatClient)
    {
        // Define the assistant
        Assistant assistant =
            await this.AssistantClient.CreateAssistantAsync(
                this.Model,
                instructions: AgentInstructions,
                metadata: SampleMetadata);

        // Define the agents
        OpenAIAssistantAgent assistantAgent =
            await OpenAIAssistantAgent.CreateAsync(

                kernel: new(),
                provider,
                new(this.Model)

                kernel: new(),
                provider,
                new(this.Model)

                provider,
                definition: new OpenAIAssistantDefinition(this.Model)
                {
                    Name = nameof(OpenAIAssistantAgent),
                    Instructions = AgentInstructions,
                },
                kernel: new Kernel());
                kernel: new(),
                provider,
                definition: new OpenAIAssistantDefinition(this.Model)

                {
                    Name = nameof(OpenAIAssistantAgent),
                    Instructions = AgentInstructions,
                });

                },
                kernel: new Kernel());

                },
                kernel: new Kernel());

        // Create the agent
        OpenAIAssistantAgent assistantAgent = new(assistant, this.AssistantClient);

        ChatCompletionAgent chatAgent =
            new()
            {
                Name = nameof(ChatCompletionAgent),
                Instructions = AgentInstructions,
                Kernel = this.CreateKernelWithChatCompletion(useChatClient, out var chatClient),
            };

        // Create a chat for agent interaction.
        AgentGroupChat chat = new();

        // Respond to user input
        try
        {
            await InvokeAgentAsync(assistantAgent, "What is my favorite color?");
            await InvokeAgentAsync(chatAgent);

            await InvokeAgentAsync(assistantAgent, "I like green.");
            await InvokeAgentAsync(chatAgent);

            await InvokeAgentAsync(assistantAgent, "What is my favorite color?");
            await InvokeAgentAsync(chatAgent);

            await chat.ResetAsync();

            await InvokeAgentAsync(assistantAgent, "What is my favorite color?");
            await InvokeAgentAsync(chatAgent);
        }
        finally
        {
            await chat.ResetAsync();
            await this.AssistantClient.DeleteAssistantAsync(assistantAgent.Id);
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
            }
        }
    }
}
