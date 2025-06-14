// Copyright (c) Microsoft. All rights reserved.
using Azure.AI.Agents.Persistent;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Agents.AzureAI;
using Microsoft.SemanticKernel.Agents.Chat;
using Microsoft.SemanticKernel.ChatCompletion;

namespace GettingStarted.AzureAgents;

/// <summary>
/// Demonstrates creation of <see cref="AgentChat"/> with <see cref="AgentGroupChatSettings"/>.
/// Improved summary: Shows how to set up a group chat with multiple Azure AI agents, configure chat settings, and manage agent interactions for collaborative tasks.
/// </summary>
public class Step03_AzureAIAgent_Chat(ITestOutputHelper output) : BaseAzureAgentTest(output)
{
    private const string ReviewerName = "ArtDirector";
    private const string ReviewerInstructions =
        """
        You are an art director who has opinions about copywriting born of a love for David Ogilvy.
        The goal is to determine if the given copy is acceptable to print.
        If so, state that it is approved.  Do not use the word "approve" unless you are giving approval.
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

    [Fact]
    public async Task UseGroupChatWithTwoAgents()
    {
        // Define the agents
        PersistentAgent reviewerModel = await this.Client.Administration.CreateAgentAsync(
            TestConfiguration.AzureAI.ChatModelId,
            ReviewerName,
            null,
            ReviewerInstructions);
        AzureAIAgent agentReviewer = new(reviewerModel, this.Client);
        PersistentAgent writerModel = await this.Client.Administration.CreateAgentAsync(
            TestConfiguration.AzureAI.ChatModelId,
            CopyWriterName,
            null,
            CopyWriterInstructions);
        AzureAIAgent agentWriter = new(writerModel, this.Client);

        // Create a chat for agent interaction.
        AgentGroupChat chat =
            new(agentWriter, agentReviewer)
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

        try
        {
            // Invoke chat and display messages.
            ChatMessageContent input = new(AuthorRole.User, "concept: maps made out of egg cartons.");
            chat.AddChatMessage(input);
            this.WriteAgentChatMessage(input);

            await foreach (ChatMessageContent response in chat.InvokeAsync())
            {
                this.WriteAgentChatMessage(response);
            }

            Console.WriteLine($"\n[IS COMPLETED: {chat.IsComplete}]");
        }
        finally
        {
            await chat.ResetAsync();
            await agentReviewer.Client.Administration.DeleteAgentAsync(agentReviewer.Id);
            await agentWriter.Client.Administration.DeleteAgentAsync(agentWriter.Id);
        }
    }

    private sealed class ApprovalTerminationStrategy : TerminationStrategy
    {
        // Terminate when the final message contains the term "approve"
        protected override Task<bool> ShouldAgentTerminateAsync(Microsoft.SemanticKernel.Agents.Agent agent, IReadOnlyList<ChatMessageContent> history, CancellationToken cancellationToken)
            => Task.FromResult(history[history.Count - 1].Content?.Contains("approve", StringComparison.OrdinalIgnoreCase) ?? false);
    }
}
