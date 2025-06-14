// Copyright (c) Microsoft. All rights reserved.

using MCPServer;
using MCPServer.Tools;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Connectors.InMemory;
using ModelContextProtocol.Protocol;
using ModelContextProtocol.Server;

var builder = Host.CreateEmptyApplicationBuilder(settings: null);


// Register the kernel
IKernelBuilder kernelBuilder = builder.Services.AddKernel();

// Register SK plugins
kernelBuilder.Plugins.AddFromType<DateTimeUtils>();
kernelBuilder.Plugins.AddFromType<WeatherUtils>();
kernelBuilder.Plugins.AddFromType<MailboxUtils>();

// Register SK agent as plugin
kernelBuilder.Plugins.AddFromFunctions("Agents", [AgentKernelFunctionFactory.CreateFromAgent(CreateSalesAssistantAgent(chatModelId, apiKey))]);

// Register embedding generation service and in-memory vector store
kernelBuilder.Services.AddSingleton<VectorStore, InMemoryVectorStore>();
kernelBuilder.Services.AddOpenAIEmbeddingGenerator(embeddingModelId, apiKey);

// Register MCP server
using Azure.Monitor.OpenTelemetry.Exporter;
using MCPServer;
using Microsoft.SemanticKernel;
using ModelContextProtocol;
using OpenTelemetry.Resources;
using OpenTelemetry;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;
using MCPServer.Resources;

// Enable Application Insights telemetry
string connectionString = GetAppInsightsConnectionString();

// Enable diagnostics with sensitive data.
AppContext.SetSwitch("Microsoft.SemanticKernel.Experimental.GenAI.EnableOTelDiagnosticsSensitive", true);

var resourceBuilder = ResourceBuilder
    .CreateDefault()
    .AddService("SKTelemetry");

using var traceProvider = Sdk.CreateTracerProviderBuilder()
    .SetResourceBuilder(resourceBuilder)
    .AddSource("Microsoft.SemanticKernel*")
    .AddAzureMonitorTraceExporter(options => options.ConnectionString = connectionString)
    .Build();

using var meterProvider = Sdk.CreateMeterProviderBuilder()
    .SetResourceBuilder(resourceBuilder)
    .AddMeter("Microsoft.SemanticKernel*")
    .AddAzureMonitorMetricExporter(options => options.ConnectionString = connectionString)
    .Build();

using var loggerFactory = LoggerFactory.Create(builder =>
{
    builder.AddOpenTelemetry(options =>
    {
        options.SetResourceBuilder(resourceBuilder);
        options.AddAzureMonitorLogExporter(options => options.ConnectionString = connectionString);
        options.IncludeFormattedMessage = true;
        options.IncludeScopes = true;
    });
    builder.AddFilter("Microsoft.SemanticKernel*", LogLevel.Trace);
});

// Build the kernel
IKernelBuilder kernelBuilder = Kernel.CreateBuilder();
kernelBuilder.Services.AddSingleton<ILoggerFactory>(loggerFactory);

Kernel kernel = kernelBuilder.Build();

// Import a OpenAPI plugin defined weather.json OpenAPI/Swagger spec
using Stream stream = EmbeddedResource.ReadAsStream("weather.json");
await kernel.ImportPluginFromOpenApiAsync("Weather", stream);

// Register a function invocation filter to validate function calls
kernel.AutoFunctionInvocationFilters.Add(new ContentSafetyAutoFunctionInvocationFilter());

var builder = Host.CreateEmptyApplicationBuilder(settings: null);
builder.Services
    .AddMcpServer()
    .WithStdioServerTransport()

    // Add all functions from the kernel plugins to the MCP server as tools
    .WithTools()

    // Register the `getCurrentWeatherForCity` prompt
    .WithPrompt(PromptDefinition.Create(EmbeddedResource.ReadAsString("getCurrentWeatherForCity.json")))

    // Register vector search as MCP resource template
    .WithResourceTemplate(CreateVectorStoreSearchResourceTemplate())

    // Register the cat image as a MCP resource
    .WithResource(ResourceDefinition.CreateBlobResource(
        uri: "image://cat.jpg",
        name: "cat-image",
        content: EmbeddedResource.ReadAsBytes("cat.jpg"),
        mimeType: "image/jpeg"));

await builder.Build().RunAsync();

/// <summary>
/// Creates a sales assistant agent that can place orders and handle refunds.
/// </summary>
/// <remarks>
/// The agent is created with an OpenAI chat completion service and a plugin for order processing.
/// </remarks>
static Agent CreateSalesAssistantAgent()
{
    // Load and validate configuration
    IConfigurationRoot config = new ConfigurationBuilder()
static string GetAppInsightsConnectionString()
{
    var config = new ConfigurationBuilder()
        .AddUserSecrets<Program>()
        .AddEnvironmentVariables()
        .Build();

    if (config["OpenAI:ApiKey"] is not { } apiKey)
    {
        const string Message = "Please provide a valid OpenAI:ApiKey to run this sample. See the associated README.md for more details.";
        Console.Error.WriteLine(Message);
        throw new InvalidOperationException(Message);
    }

    string embeddingModelId = config["OpenAI:EmbeddingModelId"] ?? "text-embedding-3-small";

    string chatModelId = config["OpenAI:ChatModelId"] ?? "gpt-4o-mini";

    return (embeddingModelId, chatModelId, apiKey);
}
static ResourceTemplateDefinition CreateVectorStoreSearchResourceTemplate(Kernel? kernel = null)
{
    return new ResourceTemplateDefinition
    {
        Kernel = kernel,
        ResourceTemplate = new()
        {
            UriTemplate = "vectorStore://{collection}/{prompt}",
            Name = "Vector Store Record Retrieval",
            Description = "Retrieves relevant records from the vector store based on the provided prompt."
        },
        Handler = async (
            RequestContext<ReadResourceRequestParams> context,
            string collection,
            string prompt,
            [FromKernelServices] IEmbeddingGenerator<string, Embedding<float>> embeddingGenerator,
            [FromKernelServices] VectorStore vectorStore,
            CancellationToken cancellationToken) =>
        {
            // Get the vector store collection
            VectorStoreCollection<Guid, TextDataModel> vsCollection = vectorStore.GetCollection<Guid, TextDataModel>(collection);

            // Check if the collection exists, if not create and populate it
            if (!await vsCollection.CollectionExistsAsync(cancellationToken))
            {
                static TextDataModel CreateRecord(string text, ReadOnlyMemory<float> embedding)
                {
                    return new()
                    {
                        Key = Guid.NewGuid(),
                        Text = text,
                        Embedding = embedding
                    };
                }

                string content = EmbeddedResource.ReadAsString("semantic-kernel-info.txt");

                // Create a collection from the lines in the file
                await vectorStore.CreateCollectionFromListAsync<Guid, TextDataModel>(collection, content.Split('\n'), embeddingGenerator, CreateRecord);
            }

            // Generate embedding for the prompt
            ReadOnlyMemory<float> promptEmbedding = (await embeddingGenerator.GenerateAsync(prompt, cancellationToken: cancellationToken)).Vector;

            // Retrieve top three matching records from the vector store
            var result = vsCollection.SearchAsync(promptEmbedding, top: 3, cancellationToken: cancellationToken);

            // Return the records as resource contents
            List<ResourceContents> contents = [];

            await foreach (var record in result)
            {
                contents.Add(new TextResourceContents()
                {
                    Text = record.Record.Text,
                    Uri = context.Params!.Uri!,
                    MimeType = "text/plain",
                });
            }

            return new ReadResourceResult { Contents = contents };
        }
    };
}

static Agent CreateSalesAssistantAgent(string chatModelId, string apiKey)
{
    (string deploymentName, string endPoint, string apiKey) = GetConfiguration();

    IKernelBuilder kernelBuilder = Kernel.CreateBuilder();

    // Register the SK plugin for the agent to use
    kernelBuilder.Plugins.AddFromType<OrderProcessingUtils>();

    // Register chat completion service
    kernelBuilder.Services.AddAzureOpenAIChatCompletion(deploymentName: deploymentName, endpoint: endPoint, apiKey: apiKey);

    // Using a dedicated kernel with the `OrderProcessingUtils` plugin instead of the global kernel has a few advantages:
    // - The agent has access to only relevant plugins, leading to better decision-making regarding which plugin to use.
    //   Fewer plugins mean less ambiguity in selecting the most appropriate one for a given task.
    // - The plugin is isolated from other plugins exposed by the MCP server. As a result the client's Agent/AI model does
    //   not have access to irrelevant plugins.
    Kernel kernel = kernelBuilder.Build();

    // Define the agent
    return new ChatCompletionAgent()
    {
        Name = "SalesAssistant",
        Instructions = "You are a sales assistant. Place orders for items the user requests and handle refunds.",
        Description = "Agent to invoke to place orders for items the user requests and handle refunds.",
        Kernel = kernel,
        Arguments = new KernelArguments(new PromptExecutionSettings() { FunctionChoiceBehavior = FunctionChoiceBehavior.Auto() }),
    };
    return config["ApplicationInsights:ConnectionString"]!;
}

/// <summary>
/// Gets configuration.
/// </summary>
static (string DeploymentName, string Endpoint, string ApiKey) GetConfiguration()
{
    // Load and validate configuration
    IConfigurationRoot config = new ConfigurationBuilder()
        .AddUserSecrets<Program>()
        .AddEnvironmentVariables()
        .Build();

    if (config["AzureOpenAI:Endpoint"] is not { } endpoint)
    {
        const string Message = "Please provide a valid AzureOpenAI:Endpoint to run this sample.";
        Console.Error.WriteLine(Message);
        throw new InvalidOperationException(Message);
    }

    if (config["AzureOpenAI:ApiKey"] is not { } apiKey)
    {
        const string Message = "Please provide a valid AzureOpenAI:ApiKey to run this sample.";
        Console.Error.WriteLine(Message);
        throw new InvalidOperationException(Message);
    }

    string deploymentName = config["AzureOpenAI:ChatDeploymentName"] ?? "gpt-4o-mini";

    return (deploymentName, endpoint, apiKey);
}
