

﻿// Copyright (c) Microsoft. All rights reserved.

﻿// Copyright (c) Microsoft. All rights reserved.

// Copyright (c) Microsoft. All rights reserved.

// Copyright (c) Microsoft. All rights reserved.

// Copyright (c) Microsoft. All rights reserved.

// Copyright (c) Microsoft. All rights reserved.

using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Agents.OpenAI;
using Microsoft.SemanticKernel.ChatCompletion;
using OpenAI.Assistants;

namespace GettingStarted.OpenAIAssistants;

/// <summary>
/// Demonstrate using code-interpreter on <see cref="OpenAIAssistantAgent"/> .
/// </summary>
public class Step04_AssistantTool_CodeInterpreter(ITestOutputHelper output) : BaseAssistantTest(output)
{
    [Fact]
    public async Task UseCodeInterpreterToolWithAssistantAgent()
    {
        // Define the agent
        OpenAIAssistantAgent agent =
            await OpenAIAssistantAgent.CreateAsync(

                kernel: new(),
                clientProvider: this.GetClientProvider(),
                new(this.Model)

                kernel: new(),
                clientProvider: this.GetClientProvider(),
                new(this.Model)

                clientProvider: this.GetClientProvider(),
                definition: new(this.Model)
                {
                    EnableCodeInterpreter = true,
                    Metadata = AssistantSampleMetadata,
                },
                kernel: new Kernel());
                kernel: new(),
                clientProvider: this.GetClientProvider(),
                definition: new(this.Model)

                {
                    EnableCodeInterpreter = true,
                    Metadata = AssistantSampleMetadata,
                });

 6d73513a859ab2d05e01db3bc1d405827799e34b
                },
                kernel: new Kernel());

 6d73513a859ab2d05e01db3bc1d405827799e34b
                },
                kernel: new Kernel());

        // Define the assistant
        Assistant assistant =
            await this.AssistantClient.CreateAssistantAsync(
                this.Model,
                enableCodeInterpreter: true,
                metadata: SampleMetadata);

        // Create the agent
        OpenAIAssistantAgent agent = new(assistant, this.AssistantClient);

        // Create a thread for the agent conversation.
        AgentThread thread = new OpenAIAssistantAgentThread(this.AssistantClient, metadata: SampleMetadata);

        // Respond to user input
        try
        {
            await InvokeAgentAsync("Use code to determine the values in the Fibonacci sequence that that are less then the value of 101?");
        }
        finally
        {
            await thread.DeleteAsync();
            await this.AssistantClient.DeleteAssistantAsync(agent.Id);
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
