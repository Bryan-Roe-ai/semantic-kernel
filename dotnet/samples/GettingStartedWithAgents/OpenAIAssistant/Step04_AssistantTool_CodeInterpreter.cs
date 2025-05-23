<<<<<<< HEAD:dotnet/samples/GettingStartedWithAgents/Step10_AssistantTool_CodeInterpreter.cs
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
﻿// Copyright (c) Microsoft. All rights reserved.
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
﻿// Copyright (c) Microsoft. All rights reserved.
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e:dotnet/samples/GettingStartedWithAgents/OpenAIAssistant/Step04_AssistantTool_CodeInterpreter.cs
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
<<<<<<< HEAD:dotnet/samples/GettingStartedWithAgents/Step10_AssistantTool_CodeInterpreter.cs
        // Define the agent
        OpenAIAssistantAgent agent =
            await OpenAIAssistantAgent.CreateAsync(
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
                kernel: new(),
                clientProvider: this.GetClientProvider(),
                new(this.Model)
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
                kernel: new(),
                clientProvider: this.GetClientProvider(),
                new(this.Model)
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
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
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< HEAD
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
                {
                    EnableCodeInterpreter = true,
                    Metadata = AssistantSampleMetadata,
                });
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
 6d73513a859ab2d05e01db3bc1d405827799e34b
                },
                kernel: new Kernel());
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
 6d73513a859ab2d05e01db3bc1d405827799e34b
                },
                kernel: new Kernel());
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
        // Define the assistant
        Assistant assistant =
            await this.AssistantClient.CreateAssistantAsync(
                this.Model,
                enableCodeInterpreter: true,
                metadata: SampleMetadata);

        // Create the agent
        OpenAIAssistantAgent agent = new(assistant, this.AssistantClient);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e:dotnet/samples/GettingStartedWithAgents/OpenAIAssistant/Step04_AssistantTool_CodeInterpreter.cs

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
