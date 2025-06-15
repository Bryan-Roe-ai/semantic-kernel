// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Azure.Identity;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents.OpenAI;
using Microsoft.SemanticKernel.ChatCompletion;
using OpenAI.Files;
using OpenAI.VectorStores;
using Microsoft.SemanticKernel.Agents;
using Microsoft.Azure.Cosmos;
using Azure.Security.KeyVault.Secrets;
using Microsoft.TeamFoundation.Client;
using Microsoft.TeamFoundation.Build.Client;
using AI.TaskGenerator;
using Microsoft.Extensions.Logging;

namespace AgentsSample;

/*****************
 * SETUP:
 * dotnet user-secrets set "OpenAISettings:ApiKey" "<api-key>"
 * dotnet user-secrets set "OpenAISettings:ChatModel" "gpt-4o"
 * dotnet user-secrets set "AzureOpenAISettings:Endpoint" "https://lightspeed-team-shared-openai-eastus.openai.azure.com/"
 * dotnet user-secrets set "AzureOpenAISettings:ChatModelDeployment" "gpt-4o"

 * INPUTS:
 * 1. What is the paragraph count for each of the stories?
 * 2. Create a table that identifies the protagonist and antagonist for each story.
 * 3. What is the moral in The White Snake?
 *****************/
public static class Program
{
    private static readonly string[] _fileNames =
        [
            "Grimms-The-King-of-the-Golden-Mountain.txt",
            "Grimms-The-Water-of-Life.txt",
            "Grimms-The-White-Snake.txt",
        ];

    /// <summary>
    /// The main entry point for the application.
    /// </summary>
    /// <returns>A <see cref="Task"/> representing the asynchronous operation.</returns>
    public static async Task Main()
    {
        // Load configuration from environment variables or user secrets.
        Settings settings = new();

        OpenAIClientProvider clientProvider =
            //OpenAIClientProvider.ForOpenAI(settings.OpenAI.ApiKey);
            OpenAIClientProvider.ForAzureOpenAI(
                new AzureCliCredential(),
                new Uri(settings.AzureOpenAI.Endpoint));

        Console.WriteLine("Creating store...");
        VectorStoreClient storeClient = clientProvider.Client.GetVectorStoreClient();
        VectorStore store = await storeClient.CreateVectorStoreAsync();

        // Retain file references.
        Dictionary<string, OpenAIFileInfo> fileReferences = [];

        Console.WriteLine("Uploading files...");
        FileClient fileClient = clientProvider.Client.GetFileClient();
        foreach (string fileName in _fileNames)
        {
            OpenAIFileInfo fileInfo = await fileClient.UploadFileAsync(fileName, FileUploadPurpose.Assistants);
            await storeClient.AddFileToVectorStoreAsync(store.Id, fileInfo.Id);
            fileReferences.Add(fileInfo.Id, fileInfo);
        }

        // Azure Cosmos DB integration
        CosmosClient cosmosClient = new CosmosClient(settings.CosmosDB.Endpoint, new AzureCliCredential());
        Database database = await cosmosClient.CreateDatabaseIfNotExistsAsync("your-database-name");
        Container container = await database.CreateContainerIfNotExistsAsync("your-container-name", "/partitionKey");

        // Azure Key Vault integration
        SecretClient secretClient = new SecretClient(new Uri(settings.KeyVault.Endpoint), new AzureCliCredential());
        KeyVaultSecret secret = await secretClient.GetSecretAsync("your-secret-name");

        // Azure DevOps integration
        TfsTeamProjectCollection tpc = new TfsTeamProjectCollection(new Uri(settings.AzureDevOps.OrganizationUrl), new AzureCliCredential());
        IBuildServer buildServer = tpc.GetService<IBuildServer>();

        Console.WriteLine("Defining agent...");
        OpenAIAssistantAgent agent =
            await OpenAIAssistantAgent.CreateAsync(
                clientProvider,
                new OpenAIAssistantDefinition(settings.AzureOpenAI.ChatModelDeployment)
                {
                    Name = "SampleAssistantAgent",
                    Instructions =
                        """
                        The document store contains the text of fictional stories.
                        Always analyze the document store to provide an answer to the user's question.
                        Never rely on your knowledge of stories not included in the document store.
                        Always format response using markdown.
                        """,
                    EnableFileSearch = true,
                    VectorStoreId = store.Id,
                },
                new Kernel());

        Console.WriteLine("Creating thread...");
        string threadId = await agent.CreateThreadAsync();

        Console.WriteLine("Ready!");

        // Generate tasks using the AI Task Generator
        TaskGenerator taskGenerator = new TaskGenerator();
        var tasks = taskGenerator.GenerateTasks("educational", "students", "math", "medium", "problem-solving");
        foreach (var task in tasks)
        {
            Console.WriteLine(task);
        }

        try
        {
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
                if (input.Trim().Equals("EXIT", StringComparison.OrdinalIgnoreCase))
                {
                    isComplete = true;
                    break;
                }

                await agent.AddChatMessageAsync(threadId, new ChatMessageContent(AuthorRole.User, input));
                Console.WriteLine();

                List<StreamingAnnotationContent> footnotes = [];
                try
                {
                    await foreach (StreamingChatMessageContent chunk in agent.InvokeStreamingAsync(threadId))
                    {
                        // Capture annotations for footnotes
                        footnotes.AddRange(chunk.Items.OfType<StreamingAnnotationContent>());

                        // Render chunk with replacements for unicode brackets.
                        Console.Write(chunk.Content.ReplaceUnicodeBrackets());
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"An error occurred: {ex.Message}");
                }

                Console.WriteLine();

                // Render footnotes for captured annotations.
                if (footnotes.Count > 0)
                {
                    Console.WriteLine();
                    foreach (StreamingAnnotationContent footnote in footnotes)
                    {
                        Console.WriteLine($"#{footnote.Quote.ReplaceUnicodeBrackets()} - {fileReferences[footnote.FileId!].Filename} (Index: {footnote.StartIndex} - {footnote.EndIndex})");
                    }
                }
            } while (!isComplete);
        }
        finally
        {
            Console.WriteLine();
            Console.WriteLine("Cleaning-up...");
            await Task.WhenAll(
                [
                    agent.DeleteThreadAsync(threadId),
                    agent.DeleteAsync(),
                    storeClient.DeleteVectorStoreAsync(store.Id),
                    ..fileReferences.Select(fileReference => fileClient.DeleteFileAsync(fileReference.Key))
                ]);
        }
    }

    private static string ReplaceUnicodeBrackets(this string content) =>
        content?.Replace('【', '[').Replace('】', ']') ?? string.Empty;

    // Method to handle AI interactions via a web interface
    public static async Task<string> HandleAIInteraction(string userInput)
    {
        // Load configuration from environment variables or user secrets.
        Settings settings = new();

        OpenAIClientProvider clientProvider =
            OpenAIClientProvider.ForAzureOpenAI(
                new AzureCliCredential(),
                new Uri(settings.AzureOpenAI.Endpoint));

        Console.WriteLine("Creating store...");
        VectorStoreClient storeClient = clientProvider.Client.GetVectorStoreClient();
        VectorStore store = await storeClient.CreateVectorStoreAsync();

        // Retain file references.
        Dictionary<string, OpenAIFileInfo> fileReferences = [];

        Console.WriteLine("Uploading files...");
        FileClient fileClient = clientProvider.Client.GetFileClient();
        foreach (string fileName in _fileNames)
        {
            OpenAIFileInfo fileInfo = await fileClient.UploadFileAsync(fileName, FileUploadPurpose.Assistants);
            await storeClient.AddFileToVectorStoreAsync(store.Id, fileInfo.Id);
            fileReferences.Add(fileInfo.Id, fileInfo);
        }

        Console.WriteLine("Defining agent...");
        OpenAIAssistantAgent agent =
            await OpenAIAssistantAgent.CreateAsync(
                clientProvider,
                new OpenAIAssistantDefinition(settings.AzureOpenAI.ChatModelDeployment)
                {
                    Name = "SampleAssistantAgent",
                    Instructions =
                        """
                        The document store contains the text of fictional stories.
                        Always analyze the document store to provide an answer to the user's question.
                        Never rely on your knowledge of stories not included in the document store.
                        Always format response using markdown.
                        """,
                    EnableFileSearch = true,
                    VectorStoreId = store.Id,
                },
                new Kernel());

        Console.WriteLine("Creating thread...");
        string threadId = await agent.CreateThreadAsync();

        Console.WriteLine("Ready!");

        try
        {
            await agent.AddChatMessageAsync(threadId, new ChatMessageContent(AuthorRole.User, userInput));
            Console.WriteLine();

            List<StreamingAnnotationContent> footnotes = [];
            string response = string.Empty;
            await foreach (StreamingChatMessageContent chunk in agent.InvokeStreamingAsync(threadId))
            {
                // Capture annotations for footnotes
                footnotes.AddRange(chunk.Items.OfType<StreamingAnnotationContent>());

                // Append chunk content to response
                response += chunk.Content.ReplaceUnicodeBrackets();
            }

            Console.WriteLine();

            // Render footnotes for captured annotations.
            if (footnotes.Count > 0)
            {
                response += "\n\n";
                foreach (StreamingAnnotationContent footnote in footnotes)
                {
                    response += $"#{footnote.Quote.ReplaceUnicodeBrackets()} - {fileReferences[footnote.FileId!].Filename} (Index: {footnote.StartIndex} - {footnote.EndIndex})\n";
                }
            }

            return response;
        }
        finally
        {
            Console.WriteLine();
            Console.WriteLine("Cleaning-up...");
            await Task.WhenAll(
                [
                    agent.DeleteThreadAsync(threadId),
                    agent.DeleteAsync(),
                    storeClient.DeleteVectorStoreAsync(store.Id),
                    ..fileReferences.Select(fileReference => fileClient.DeleteFileAsync(fileReference.Key))
                ]);
        }
    }
}
