﻿// Copyright (c) Microsoft. All rights reserved.

using System;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;
using Azure.Identity;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Agents.Chat;
using Microsoft.SemanticKernel.Agents.History;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.AzureOpenAI;

namespace AgentsSample;

/*****************
 * SETUP:
 * dotnet user-secrets set "OpenAISettings:ApiKey" "<api-key>"
 * dotnet user-secrets set "OpenAISettings:ChatModel" "gpt-4o"
 * dotnet user-secrets set "AzureOpenAISettings:Endpoint" "<model-endpoint>"
 * dotnet user-secrets set "AzureOpenAISettings:ChatModelDeployment" "gpt-4o"

 * INPUTS:
 * 1. Hi
 * 2. {"message: "hello world"}
 * 3. {"message": "hello world"}
 * 4. Semantic Kernel (SK) is an open-source SDK that enables developers to build and orchestrate complex AI workflows that involve natural language processing (NLP) and machine learning models. It provies a flexible platform for integrating AI capabilities such as semantic search, text summarization, and dialogue systems into applications. With SK, you can easily combine different AI services and models, define thei relationships, and orchestrate interactions between them.
 * 5. make this two paragraphs
 * 6. thank you
 * 7. @.\WomensSuffrage.txt
 * 8. its good, but is it ready for my college professor? 
 ******************/

public static class Program
{
    public static async Task Main()
    {
        // Load configuration from environment variables or user secrets.
        Settings settings = new();

        Console.WriteLine("Creating kernel...");
        IKernelBuilder builder = Kernel.CreateBuilder();

        builder.AddAzureOpenAIChatCompletion(
            settings.AzureOpenAI.ChatModelDeployment,
            settings.AzureOpenAI.Endpoint,
            new AzureCliCredential());

        Kernel kernel = builder.Build();

        Kernel toolKernel = kernel.Clone();
        toolKernel.Plugins.AddFromType<ClipboardAccess>();


        Console.WriteLine("Defining agents...");

        const string ReviewerName = "Reviewer";
        const string WriterName = "Writer";

        ChatCompletionAgent agentReviewer =
            new()
            {
                Name = ReviewerName,
                Instructions =
                        """
                        Your responsiblity is to review and identify how to improve user provided content.
                        If the user has providing input or direction for content already provided, specify how to address this input.
                        Never directly perform the correction or provide example.
                        Once the content has been updated in a subsequent response, you will review the content again until satisfactory.
                        Always copy satisfactory content to the clipboard using available tools and inform user.

                        RULES:
                        - Only identify suggestions that are specific and actionable.
                        - Verify previous suggestions have been addressed.
                        - Never repeat previous suggestions.
                        """,
                Kernel = toolKernel,
                Arguments = new KernelArguments(new AzureOpenAIPromptExecutionSettings() { FunctionChoiceBehavior = FunctionChoiceBehavior.Auto() })
            };

        ChatCompletionAgent agentWriter =
            new()
            {
                Name = WriterName,
                Instructions =
                        """
                        Your sole responsiblity is to rewrite content according to review suggestions.

                        - Always apply all review direction.
                        - Always revise the content in its entirety without explanation.
                        - Never address the user.
                        """,
                Kernel = kernel,
            };

        KernelFunction selectionFunction =
            AgentGroupChat.CreatePromptFunctionForStrategy(
                $$$"""
                Examine the provided RESPONSE and choose the next participant.
                State only the name of the chosen participant without explanation.
                Never choose the participant named in the RESPONSE.
                
                Choose only from these participants:
                - {{{ReviewerName}}}
                - {{{WriterName}}}

                Always follow these rules when choosing the next participant:
                - If RESPONSE is user input, it is {{{ReviewerName}}}'s turn.
                - If RESPONSE is by {{{ReviewerName}}}, it is {{{WriterName}}}'s turn.
                - If RESPONSE is by {{{WriterName}}}, it is {{{ReviewerName}}}'s turn.

                RESPONSE:
                {{$lastmessage}}
                """,
                safeParameterNames: "lastmessage");

        const string TerminationToken = "yes";

        KernelFunction terminationFunction =
            AgentGroupChat.CreatePromptFunctionForStrategy(
                $$$"""
                Examine the RESPONSE and determine whether the content has been deemed satisfactory.
                If content is satisfactory, respond with a single word without explanation: {{{TerminationToken}}}.
                If specific suggestions are being provided, it is not satisfactory.
                If no correction is suggested, it is satisfactory.

                RESPONSE:
                {{$lastmessage}}
                """,
                safeParameterNames: "lastmessage");

        ChatHistoryTruncationReducer historyReducer = new(1);

        AgentGroupChat chat =
            new(agentReviewer, agentWriter)
            {
                ExecutionSettings = new AgentGroupChatSettings
                {
                    SelectionStrategy =
                        new KernelFunctionSelectionStrategy(selectionFunction, kernel)
                        {
                            // Always start with the editor agent.
                            InitialAgent = agentReviewer,
                            // Save tokens by only including the final two responses
                            HistoryReducer = historyReducer,
                            // The prompt variable name for the history argument.
                            HistoryVariableName = "lastmessage",
                            // Returns the entire result value as a string.
                            ResultParser = (result) => result.GetValue<string>() ?? agentReviewer.Name
                        },
                    TerminationStrategy =
                        new KernelFunctionTerminationStrategy(terminationFunction, kernel)
                        {
                            // Only evaluate for editor's response
                            Agents = [agentReviewer],
                            // Save tokens by only including the final response
                            HistoryReducer = historyReducer,
                            // The prompt variable name for the history argument.
                            HistoryVariableName = "lastmessage",
                            // Limit total number of turns
                            MaximumIterations = 12,
                            // Customer result parser to determine if the response is "yes"
                            ResultParser = (result) => result.GetValue<string>()?.Contains(TerminationToken, StringComparison.OrdinalIgnoreCase) ?? false
                        }
                }
            };

        Console.WriteLine("Ready!");

        bool isComplete = false;
        do
        {
            Console.WriteLine();
            Console.Write("> ");
            string input = Console.ReadLine();
            if (string.IsNullOrWhiteSpace(input))
            {
                continue;
            }
            input = input.Trim();
            if (input.Equals("EXIT", StringComparison.OrdinalIgnoreCase))
            {
                isComplete = true;
                break;
            }

            if (input.Equals("RESET", StringComparison.OrdinalIgnoreCase))
            {
                await chat.ResetAsync();
                Console.WriteLine("[Converation has been reset]");
                continue;
            }

            if (input.StartsWith("@", StringComparison.Ordinal) && input.Length > 1)
            {
                string filePath = input.Substring(1);
                try
                {
                    if (!File.Exists(filePath))
                    {
                        Console.WriteLine($"Unable to access file: {filePath}");
                        continue;
                    }
                    input = await File.ReadAllTextAsync(filePath);
                }
                catch (Exception)
                {
                    Console.WriteLine($"Unable to access file: {filePath}");
                    continue;
                }
            }

            chat.AddChatMessage(new ChatMessageContent(AuthorRole.User, input));

            chat.IsComplete = false;

            try
            {
                await foreach (ChatMessageContent response in chat.InvokeAsync())
                {
                    Console.WriteLine();
                    Console.WriteLine($"{response.AuthorName.ToUpperInvariant()}:{Environment.NewLine}{response.Content}");
                }
            }
            catch (HttpOperationException exception)
            {
                Console.WriteLine(exception.Message);
                if (exception.InnerException != null)
                {
                    Console.WriteLine(exception.InnerException.Message);
                    if (exception.InnerException.Data.Count > 0)
                    {
                        Console.WriteLine(JsonSerializer.Serialize(exception.InnerException.Data, new JsonSerializerOptions() { WriteIndented = true }));
                    }
                }
            }
        } while (!isComplete);
    }

    public sealed class ClipboardAccess
    {
        [KernelFunction("Copies the provided content to the clipboard.")]
        [Description("Copies the provided content to the clipboard.")]
        public static void SetClipboard(string content)
        {
            if (string.IsNullOrWhiteSpace(content))
            {
                return;
            }

            using Process clipProcess = Process.Start(
                new ProcessStartInfo
                {
                    FileName = "clip",
                    RedirectStandardInput = true,
                    UseShellExecute = false,
                });

            clipProcess.StandardInput.Write(content);
            clipProcess.StandardInput.Close();
        }
    }

    // Method to run the AI automatically within a web page
    public static async Task RunAIAutomatically()
    {
        using HttpClient client = new HttpClient();
        string aiServiceUrl = "https://your-ai-service-url.com/api/ai";

        while (true)
        {
            try
            {
                HttpResponseMessage response = await client.GetAsync(aiServiceUrl);
                response.EnsureSuccessStatusCode();

                string responseBody = await response.Content.ReadAsStringAsync();
                await UpdateWebPage(responseBody);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }

            await Task.Delay(5000); // Wait for 5 seconds before making the next request
        }
    }

    // Method to handle the AI response and update the web page
    private static async Task UpdateWebPage(string aiResponse)
    {
        string filePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "docs", "index.html");
        string content = await File.ReadAllTextAsync(filePath);
        string updatedContent = content.Replace("<div id=\"ai-response\"></div>", $"<div id=\"ai-response\">{aiResponse}</div>");
        await File.WriteAllTextAsync(filePath, updatedContent);
    }
}
