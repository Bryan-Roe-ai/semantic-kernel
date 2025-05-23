// Copyright (c) Microsoft. All rights reserved.
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.ChatCompletion;
using Plugins;
using Resources;

namespace GettingStarted;

/// <summary>
/// Demonstrate creation of <see cref="ChatCompletionAgent"/> with a <see cref="KernelPlugin"/>,
/// and then eliciting its response to explicit user messages.
/// </summary>
public class Step02_Plugins(ITestOutputHelper output) : BaseAgentsTest(output)
{
    [Fact]
    public async Task UseChatCompletionWithPlugin()
    {
        // Define the agent
<<<<<<< HEAD
        ChatCompletionAgent agent =
            new()
            {
                Instructions = HostInstructions,
                Name = HostName,
                Kernel = this.CreateKernelWithChatCompletion(),
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
                Arguments = new KernelArguments(new OpenAIPromptExecutionSettings() { FunctionChoiceBehavior = FunctionChoiceBehavior.Auto() }),
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
                Arguments = new KernelArguments(new OpenAIPromptExecutionSettings() { FunctionChoiceBehavior = FunctionChoiceBehavior.Auto() }),
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
                Arguments = new KernelArguments(new OpenAIPromptExecutionSettings() { FunctionChoiceBehavior = FunctionChoiceBehavior.Auto() }),
=======
>>>>>>> Stashed changes
=======
                Arguments = new KernelArguments(new OpenAIPromptExecutionSettings() { FunctionChoiceBehavior = FunctionChoiceBehavior.Auto() }),
=======
>>>>>>> Stashed changes
>>>>>>> head
<<<<<<< HEAD
                Arguments = new KernelArguments(new OpenAIPromptExecutionSettings() { FunctionChoiceBehavior = FunctionChoiceBehavior.Auto() }),
=======
                Arguments = new KernelArguments(new OpenAIPromptExecutionSettings() { ToolCallBehavior = ToolCallBehavior.AutoInvokeKernelFunctions }),
>>>>>>> 6d73513a859ab2d05e01db3bc1d405827799e34b
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
            };
=======
        ChatCompletionAgent agent = CreateAgentWithPlugin(
                plugin: KernelPluginFactory.CreateFromType<MenuPlugin>(),
                instructions: "Answer questions about the menu.",
                name: "Host");
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        /// Create the chat history thread to capture the agent interaction.
        AgentThread thread = new ChatHistoryAgentThread();

        // Respond to user input, invoking functions where appropriate.
        await InvokeAgentAsync(agent, thread, "Hello");
        await InvokeAgentAsync(agent, thread, "What is the special soup and its price?");
        await InvokeAgentAsync(agent, thread, "What is the special drink and its price?");
        await InvokeAgentAsync(agent, thread, "Thank you");
    }

    [Fact]
    public async Task UseChatCompletionWithPluginEnumParameter()
    {
        // Define the agent
        ChatCompletionAgent agent = CreateAgentWithPlugin(
                KernelPluginFactory.CreateFromType<WidgetFactory>());

        /// Create the chat history thread to capture the agent interaction.
        AgentThread thread = new ChatHistoryAgentThread();

        // Respond to user input, invoking functions where appropriate.
        await InvokeAgentAsync(agent, thread, "Create a beautiful red colored widget for me.");
    }

    [Fact]
    public async Task UseChatCompletionWithTemplateExecutionSettings()
    {
        // Read the template resource
        string autoInvokeYaml = EmbeddedResource.Read("AutoInvokeTools.yaml");
        PromptTemplateConfig templateConfig = KernelFunctionYaml.ToPromptTemplateConfig(autoInvokeYaml);
        KernelPromptTemplateFactory templateFactory = new();

        // Define the agent:
        // Execution-settings with auto-invocation of plugins defined via the config.
        ChatCompletionAgent agent =
            new(templateConfig, templateFactory)
            {
                Kernel = this.CreateKernelWithChatCompletion()
            };

        agent.Kernel.Plugins.AddFromType<WidgetFactory>();

        /// Create the chat history thread to capture the agent interaction.
        AgentThread thread = new ChatHistoryAgentThread();

        // Respond to user input, invoking functions where appropriate.
        await InvokeAgentAsync(agent, thread, "Create a beautiful red colored widget for me.");
    }

    private ChatCompletionAgent CreateAgentWithPlugin(
        KernelPlugin plugin,
        string? instructions = null,
        string? name = null)
    {
        ChatCompletionAgent agent =
                new()
                {
                    Instructions = instructions,
                    Name = name,
                    Kernel = this.CreateKernelWithChatCompletion(),
                    Arguments = new KernelArguments(new PromptExecutionSettings() { FunctionChoiceBehavior = FunctionChoiceBehavior.Auto() }),
                };

        // Initialize plugin and add to the agent's Kernel (same as direct Kernel usage).
        agent.Kernel.Plugins.Add(plugin);

        return agent;
    }

    // Local function to invoke agent and display the conversation messages.
    private async Task InvokeAgentAsync(ChatCompletionAgent agent, AgentThread thread, string input)
    {
        ChatMessageContent message = new(AuthorRole.User, input);
        this.WriteAgentChatMessage(message);

        await foreach (ChatMessageContent response in agent.InvokeAsync(message, thread))
        {
            this.WriteAgentChatMessage(response);
        }
    }
}
