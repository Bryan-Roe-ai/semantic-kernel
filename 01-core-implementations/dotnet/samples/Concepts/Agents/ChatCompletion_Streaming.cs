// Copyright (c) Microsoft. All rights reserved.
using System.ComponentModel;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.ChatCompletion;

namespace Agents;

/// <summary>
/// Demonstrate consuming "streaming" message for <see cref="ChatCompletionAgent"/>.
/// </summary>
public class ChatCompletion_Streaming(ITestOutputHelper output) : BaseAgentsTest(output)
{
    private const string ParrotName = "Parrot";
    private const string ParrotInstructions = "Repeat the user message in the voice of a pirate and then end with a parrot sound.";

    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public async Task UseStreamingChatCompletionAgent(bool useChatClient)
    {
        // Define the agent
        ChatCompletionAgent agent =
            new()
            {
                Name = ParrotName,
                Instructions = ParrotInstructions,
                Kernel = this.CreateKernelWithChatCompletion(useChatClient, out var chatClient),
            };

        ChatHistoryAgentThread agentThread = new();

        // Respond to user input
        await InvokeAgentAsync(agent, agentThread, "Fortune favors the bold.");
        await InvokeAgentAsync(agent, agentThread, "I came, I saw, I conquered.");
        await InvokeAgentAsync(agent, agentThread, "Practice makes perfect.");

        // Output the entire chat history
        await DisplayChatHistory(agentThread);

        chatClient?.Dispose();
    }

    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public async Task UseStreamingChatCompletionAgentWithPlugin(bool useChatClient)
    {
        const string MenuInstructions = "Answer questions about the menu.";

        // Define the agent
        ChatCompletionAgent agent =
            new()
            {
                Name = "Host",
                Instructions = MenuInstructions,
                Kernel = this.CreateKernelWithChatCompletion(useChatClient, out var chatClient),
                Arguments = new KernelArguments(new PromptExecutionSettings() { FunctionChoiceBehavior = FunctionChoiceBehavior.Auto() }),
            };

        // Initialize plugin and add to the agent's Kernel (same as direct Kernel usage).
        KernelPlugin plugin = KernelPluginFactory.CreateFromType<MenuPlugin>();
        agent.Kernel.Plugins.Add(plugin);

        ChatHistoryAgentThread agentThread = new();

        // Respond to user input
        await InvokeAgentAsync(agent, agentThread, "What is the special soup?");
        await InvokeAgentAsync(agent, agentThread, "What is the special drink?");

        // Output the entire chat history
        await DisplayChatHistory(agentThread);

        chatClient?.Dispose();
    }

    // Local function to invoke agent and display the conversation messages.
    private async Task InvokeAgentAsync(ChatCompletionAgent agent, ChatHistoryAgentThread agentThread, string input)
    {
        ChatMessageContent message = new(AuthorRole.User, input);
        this.WriteAgentChatMessage(message);

        StringBuilder builder = new();

        StringBuilder builder = new();

        StringBuilder builder = new();

        await foreach (StreamingChatMessageContent response in agent.InvokeStreamingAsync(chat))

        await foreach (StreamingChatMessageContent response in agent.InvokeStreamingAsync(message, agentThread))

        {
            if (string.IsNullOrEmpty(response.Content))
            {
                StreamingFunctionCallUpdateContent? functionCall = response.Items.OfType<StreamingFunctionCallUpdateContent>().SingleOrDefault();
                if (!string.IsNullOrEmpty(functionCall?.Name))
                {
                    Console.WriteLine($"\n# {response.Role} - {response.AuthorName ?? "*"}: FUNCTION CALL - {functionCall.Name}");
                }

                continue;
            }

            if (!isFirst)
            {

                Console.WriteLine($"# {response.Role} - {response.AuthorName ?? "*"}:");
            }

            Console.WriteLine($"\t > streamed: '{response.Content}'");
            builder.Append(response.Content);

                Console.WriteLine($"# {response.Role} - {response.AuthorName ?? "*"}:");
            }

            Console.WriteLine($"\t > streamed: '{response.Content}'");
            builder.Append(response.Content);

        }

        if (historyCount <= agentThread.ChatHistory.Count)
        {
            for (int index = historyCount; index < agentThread.ChatHistory.Count; index++)
            {
                this.WriteAgentChatMessage(agentThread.ChatHistory[index]);
            }

        }
    }

    private async Task DisplayChatHistory(ChatHistoryAgentThread agentThread)
    {
        // Display the chat history.
        Console.WriteLine("================================");
        Console.WriteLine("CHAT HISTORY");
        Console.WriteLine("================================");

        await foreach (ChatMessageContent message in agentThread.GetMessagesAsync())
        {
            // Display full response and capture in chat history
            ChatMessageContent response = new(AuthorRole.Assistant, builder.ToString()) { AuthorName = agent.Name };
            chat.Add(response);
            this.WriteAgentChatMessage(response);

            this.WriteAgentChatMessage(message);

            this.WriteAgentChatMessage(message);

            this.WriteAgentChatMessage(message);

        }
    }

    public sealed class MenuPlugin
    {
        [KernelFunction, Description("Provides a list of specials from the menu.")]
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Design", "CA1024:Use properties where appropriate", Justification = "Too smart")]
        public string GetSpecials()
        {
            return @"
Special Soup: Clam Chowder
Special Salad: Cobb Salad
Special Drink: Chai Tea
";
        }

        [KernelFunction, Description("Provides the price of the requested menu item.")]
        public string GetItemPrice(
            [Description("The name of the menu item.")]
        string menuItem)
        {
            return "$9.99";
        }
    }
}
