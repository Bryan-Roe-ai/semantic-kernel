// Copyright (c) Microsoft. All rights reserved.
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Agents.Chat;
using Microsoft.SemanticKernel.Agents.OpenAI;
using Microsoft.SemanticKernel.ChatCompletion;
using OpenAI.Assistants;

namespace Agents;

/// <summary>
/// Demonstrate that two different agent types are able to participate in the same conversation.
/// In this case a <see cref="ChatCompletionAgent"/> and <see cref="OpenAIAssistantAgent"/> participate.
/// </summary>
public class MixedChat_Agents(ITestOutputHelper output) : BaseAssistantTest(output)
{
    private const string ReviewerName = "ArtDirector";
    private const string ReviewerInstructions =
        """
        You are an art director who has opinions about copywriting born of a love for David Ogilvy.
        The goal is to determine is the given copy is acceptable to print.
        If so, state that it is approved.
        If not, provide insight on how to refine suggested copy without example.
        """;

    private const string CopyWriterName = "CopyWriter";
    private const string CopyWriterInstructions =
        """
        You are a copywriter with ten years of experience and are known for brevity and a dry humor.
        The goal is to refine and decide on the single best copy as an expert in the field.
        Only provide a single proposal per response.
        You're laser focused on the goal at hand.
        Don't waste time with chit chat.
        Consider suggestions when refining an idea.
        """;

    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public async Task ChatWithOpenAIAssistantAgentAndChatCompletionAgent(bool useChatClient)
    {
        // Define the agents: one of each type
        ChatCompletionAgent agentReviewer =
            new()
            {
                Instructions = ReviewerInstructions,
                Name = ReviewerName,
                Kernel = this.CreateKernelWithChatCompletion(useChatClient, out var chatClient),
            };

        OpenAIAssistantAgent agentWriter =
            await OpenAIAssistantAgent.CreateAsync(

                kernel: new(),
                clientProvider: this.GetClientProvider(),
                definition: new(this.Model)

                kernel: new(),
                clientProvider: this.GetClientProvider(),
                definition: new(this.Model)

                clientProvider: this.GetClientProvider(),
                definition: new OpenAIAssistantDefinition(this.Model)
                kernel: new(),
                clientProvider: this.GetClientProvider(),
                definition: new(this.Model)
                clientProvider: this.GetClientProvider(),
                definition: new OpenAIAssistantDefinition(this.Model)

                {
                    Instructions = CopyWriterInstructions,
                    Name = CopyWriterName,
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

        // Define the assistant
        Assistant assistant =
            await this.AssistantClient.CreateAssistantAsync(
                this.Model,
                name: CopyWriterName,
                instructions: CopyWriterInstructions,
                metadata: SampleMetadata);

        // Create the agent
        OpenAIAssistantAgent agentWriter = new(assistant, this.AssistantClient);

        // Create a chat for agent interaction.
        AgentGroupChat chat =
            new(agentWriter, agentReviewer)
        var chat =
            new AgentGroupChat(agentWriter, agentReviewer)
            {
                ExecutionSettings =
                    new()
                    {
                        // Here a TerminationStrategy subclass is used that will terminate when
                        // an assistant message contains the term "approve".
                        TerminationStrategy =
                            new ApprovalTerminationStrategy()
                            {
                                // Only the art-director may approve.
                                Agents = [agentReviewer],
                                // Limit total number of turns
                                MaximumIterations = 10,
                            }
                    }
            };

        // Invoke chat and display messages.

        string input = "concept: maps made out of egg cartons.";
        chat.Add(new ChatMessageContent(AuthorRole.User, input));
        Console.WriteLine($"# {AuthorRole.User}: '{input}'");

        string input = "concept: maps made out of egg cartons.";
        chat.Add(new ChatMessageContent(AuthorRole.User, input));
        Console.WriteLine($"# {AuthorRole.User}: '{input}'");

        string input = "concept: maps made out of egg cartons.";
        chat.Add(new ChatMessageContent(AuthorRole.User, input));
        Console.WriteLine($"# {AuthorRole.User}: '{input}'");

        string input = "concept: maps made out of egg cartons.";
        chat.Add(new ChatMessageContent(AuthorRole.User, input));
        Console.WriteLine($"# {AuthorRole.User}: '{input}'");

        ChatMessageContent input = new(AuthorRole.User, "concept: maps made out of egg cartons.");
        chat.AddChatMessage(input);
        this.WriteAgentChatMessage(input);

        await foreach (ChatMessageContent response in chat.InvokeAsync())
        {
            this.WriteAgentChatMessage(response);
        }

        Console.WriteLine($"\n[IS COMPLETED: {chat.IsComplete}]");

        chatClient?.Dispose();
    }

    private sealed class ApprovalTerminationStrategy : TerminationStrategy
    {
        // Terminate when the final message contains the term "approve"
        protected override Task<bool> ShouldAgentTerminateAsync(Agent agent, IReadOnlyList<ChatMessageContent> history, CancellationToken cancellationToken)
            => Task.FromResult(history[history.Count - 1].Content?.Contains("approve", StringComparison.OrdinalIgnoreCase) ?? false);
    }
}
