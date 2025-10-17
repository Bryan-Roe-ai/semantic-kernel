// Copyright (c) Microsoft. All rights reserved.

using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;

// This simple console app demonstrates how to chat with an LLM using Semantic Kernel
// 
// To configure your LLM connection, you can use either:
// 1. .NET Secret Manager (recommended for development)
// 2. Environment variables
// 3. Direct configuration in code (not recommended for production)
//
// For OpenAI:
//   dotnet user-secrets set "OpenAI:ApiKey" "your-api-key"
//   dotnet user-secrets set "OpenAI:ChatModelId" "gpt-4o-mini"
//
// For Azure OpenAI:
//   dotnet user-secrets set "AzureOpenAI:Endpoint" "https://your-endpoint.openai.azure.com"
//   dotnet user-secrets set "AzureOpenAI:ApiKey" "your-api-key"
//   dotnet user-secrets set "AzureOpenAI:ChatDeploymentName" "your-deployment-name"

Console.WriteLine("=== Semantic Kernel Chat Demo ===\n");

// Build the kernel with your chosen AI service
var builder = Kernel.CreateBuilder();

// Option 1: Use OpenAI (requires OpenAI API key)
// Get configuration from user secrets or environment variables
var openAIApiKey = Environment.GetEnvironmentVariable("OpenAI__ApiKey");
var openAIModelId = Environment.GetEnvironmentVariable("OpenAI__ChatModelId") ?? "gpt-4o-mini";

// Option 2: Use Azure OpenAI
var azureEndpoint = Environment.GetEnvironmentVariable("AzureOpenAI__Endpoint");
var azureApiKey = Environment.GetEnvironmentVariable("AzureOpenAI__ApiKey");
var azureDeployment = Environment.GetEnvironmentVariable("AzureOpenAI__ChatDeploymentName");

// Option 3: Use Ollama (local, free - no API key needed)
var ollamaEndpoint = Environment.GetEnvironmentVariable("Ollama__Endpoint") ?? "http://localhost:11434";
var ollamaModelId = Environment.GetEnvironmentVariable("Ollama__ModelId") ?? "llama3.2";

// Choose which service to use based on what's configured
if (!string.IsNullOrEmpty(azureEndpoint) && !string.IsNullOrEmpty(azureApiKey) && !string.IsNullOrEmpty(azureDeployment))
{
    Console.WriteLine($"Using Azure OpenAI: {azureEndpoint} / {azureDeployment}\n");
    builder.AddAzureOpenAIChatCompletion(
        deploymentName: azureDeployment,
        endpoint: azureEndpoint,
        apiKey: azureApiKey);
}
else if (!string.IsNullOrEmpty(openAIApiKey))
{
    Console.WriteLine($"Using OpenAI: {openAIModelId}\n");
    builder.AddOpenAIChatCompletion(
        modelId: openAIModelId,
        apiKey: openAIApiKey);
}
else
{
    Console.WriteLine($"Using Ollama (local): {ollamaEndpoint} / {ollamaModelId}");
    Console.WriteLine("Note: Make sure Ollama is running locally with the model installed.");
    Console.WriteLine($"Install model with: ollama pull {ollamaModelId}\n");
    
    builder.AddOllamaChatCompletion(
        modelId: ollamaModelId,
        endpoint: new Uri(ollamaEndpoint));
}

var kernel = builder.Build();
var chatService = kernel.GetRequiredService<IChatCompletionService>();

// Create chat history to maintain conversation context
var chatHistory = new ChatHistory();
chatHistory.AddSystemMessage("You are a helpful AI assistant. You provide clear, concise, and accurate responses.");

Console.WriteLine("Chat started! Type your messages below. Type 'exit' or 'quit' to end the conversation.\n");

// Main chat loop
while (true)
{
    Console.Write("You: ");
    var userMessage = Console.ReadLine();
    
    if (string.IsNullOrWhiteSpace(userMessage))
    {
        continue;
    }
    
    if (userMessage.Equals("exit", StringComparison.OrdinalIgnoreCase) || 
        userMessage.Equals("quit", StringComparison.OrdinalIgnoreCase))
    {
        Console.WriteLine("\nGoodbye!");
        break;
    }
    
    // Add user message to history
    chatHistory.AddUserMessage(userMessage);
    
    try
    {
        // Get response from AI
        Console.Write("Assistant: ");
        
        // Stream the response for a better user experience
        await foreach (var message in chatService.GetStreamingChatMessageContentsAsync(chatHistory))
        {
            Console.Write(message.Content);
        }
        Console.WriteLine("\n");
        
        // Get the complete response and add to history
        var response = await chatService.GetChatMessageContentAsync(chatHistory);
        chatHistory.Add(response);
    }
    catch (Exception ex)
    {
        Console.WriteLine($"\nError: {ex.Message}\n");
    }
}
