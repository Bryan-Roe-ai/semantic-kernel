// Copyright (c) Microsoft. All rights reserved.

using System.Threading.Tasks;
using MCPClient.Samples;
using System;
using System.IO;
using System.Linq;
using Microsoft.Extensions.Configuration;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using ModelContextProtocol.Client;
using ModelContextProtocol.Configuration;
using ModelContextProtocol.Protocol.Transport;

IConfigurationRoot config = LoadConfiguration();

internal sealed class Program
{
    /// <summary>
    /// Main method to run all the samples.
    /// </summary>
    public static async Task Main(string[] args)
    {
        await MCPToolsSample.RunAsync();

        await MCPPromptSample.RunAsync();

        await MCPResourcesSample.RunAsync();

        await MCPResourceTemplatesSample.RunAsync();

        await MCPSamplingSample.RunAsync();

        await ChatCompletionAgentWithMCPToolsSample.RunAsync();

        await AzureAIAgentWithMCPToolsSample.RunAsync();

        await AgentAvailableAsMCPToolSample.RunAsync();
// Create an MCP client
await using var mcpClient = await McpClientFactory.CreateAsync(
    new McpServerConfig()
    {
        Id = "MCPServer",
        Name = "MCPServer",
        TransportType = TransportTypes.StdIo,
        TransportOptions = new()
        {
            // Point the client to the MCPServer server executable
            ["command"] = GetMCPServerPath()
        }
    },
    new McpClientOptions()
    {
        ClientInfo = new() { Name = "MCPClient", Version = "1.0.0" }
    }
 );

// Retrieve and display the list of tools available on the MCP server
Console.WriteLine("Available MCP tools:");
var tools = await mcpClient.GetAIFunctionsAsync().ConfigureAwait(false);
foreach (var tool in tools)
{
    Console.WriteLine($"\t{tool.Name}: {tool.Description}");
}

// Prepare and build kernel with the MCP tools as Kernel functions
var kernelBuilder = Kernel.CreateBuilder();
kernelBuilder.Plugins.AddFromFunctions("Tools", tools.Select(aiFunction => aiFunction.AsKernelFunction()));
kernelBuilder.Services.AddOpenAIChatCompletion(serviceId: "openai", modelId: config["OpenAI:ChatModelId"] ?? "gpt-4o-mini", apiKey: config["OpenAI:ApiKey"]!);

Kernel kernel = kernelBuilder.Build();

// Enable automatic function calling
OpenAIPromptExecutionSettings executionSettings = new()
{
    Temperature = 0,
    FunctionChoiceBehavior = FunctionChoiceBehavior.Auto(options: new() { RetainArgumentTypes = true })
};

// Execute a prompt using the MCP tools. The AI model will automatically call the appropriate MCP tools to answer the prompt.
var prompt = "What is the likely color of the sky in Seattle today?";
Console.WriteLine($"\nPrompt: {prompt}\n");

var result = await kernel.InvokePromptAsync(prompt, new(executionSettings)).ConfigureAwait(false);
Console.WriteLine($"Result: {result}");

Console.ReadKey();

// Create an MCP client
await using IMcpClient mcpClient = await CreateMcpClientAsync();

// Retrieve and display the list provided by the MCP server
IList<McpClientTool> tools = await mcpClient.ListToolsAsync();
DisplayTools(tools);

// Create a kernel and register the MCP tools
Kernel kernel = CreateKernelWithChatCompletionService();
kernel.Plugins.AddFromFunctions("Tools", tools.Select(aiFunction => aiFunction.AsKernelFunction()));

// Enable automatic function calling
OpenAIPromptExecutionSettings executionSettings = new()
{
    Temperature = 0,
    FunctionChoiceBehavior = FunctionChoiceBehavior.Auto(options: new() { RetainArgumentTypes = true })
};

string prompt = "What is the likely color of the sky in Boston today?";
Console.WriteLine(prompt);

// Execute a prompt using the MCP tools. The AI model will automatically call the appropriate MCP tools to answer the prompt.
FunctionResult result = await kernel.InvokePromptAsync(prompt, new(executionSettings));

Console.WriteLine(result);

// The expected output is: The likely color of the sky in Boston today is gray, as it is currently rainy.

static Kernel CreateKernelWithChatCompletionService()
{
    // Load and validate configuration
    IConfigurationRoot config = new ConfigurationBuilder()
        .AddUserSecrets<Program>()
        .AddEnvironmentVariables()
        .Build();

    if (config["OpenAI:ApiKey"] is not { } apiKey)
    {
        const string Message = "Please provide a valid OpenAI:ApiKey to run this sample. See the associated README.md for more details.";
        Console.Error.WriteLine(Message);
        throw new InvalidOperationException(Message);
    }

    string modelId = config["OpenAI:ChatModelId"] ?? "gpt-4o-mini";

    // Create kernel
    var kernelBuilder = Kernel.CreateBuilder();
    kernelBuilder.Services.AddOpenAIChatCompletion(serviceId: "openai", modelId: modelId, apiKey: apiKey);

    return kernelBuilder.Build();
}

static Task<IMcpClient> CreateMcpClientAsync()
{
    return McpClientFactory.CreateAsync(
        new McpServerConfig()
        {
            Id = "MCPServer",
            Name = "MCPServer",
            TransportType = TransportTypes.StdIo,
            TransportOptions = new()
            {
                // Point the client to the MCPServer server executable
                ["command"] = GetMCPServerPath()
            }
        },
        new McpClientOptions()
        {
            ClientInfo = new() { Name = "MCPClient", Version = "1.0.0" }
        }
    );
}

static string GetMCPServerPath()
{
    // Determine the configuration (Debug or Release)  
    string configuration;

#if DEBUG
    configuration = "Debug";
#else
        configuration = "Release";
#endif

    return Path.Combine("..", "..", "..", "..", "MCPServer", "bin", configuration, "net8.0", "MCPServer.exe");
}

static IConfigurationRoot LoadConfiguration()
{
    // Load and validate configuration
    var config = new ConfigurationBuilder()
        .AddUserSecrets<Program>()
        .AddEnvironmentVariables()
        .Build();

    if (config["OpenAI:ApiKey"] is not { })
    {
        Console.Error.WriteLine("Please provide a valid OpenAI:ApiKey to run this sample. See the associated README.md for more details.");
        throw new InvalidOperationException("OpenAI:ApiKey is required.");
    }

    return config;
static void DisplayTools(IList<McpClientTool> tools)
{
    Console.WriteLine("Available MCP tools:");
    foreach (var tool in tools)
    {
        Console.WriteLine($"- {tool.Name}: {tool.Description}");
    }
    Console.WriteLine();
}
