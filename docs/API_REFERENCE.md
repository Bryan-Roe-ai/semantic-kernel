# 📚 Semantic Kernel API Reference

> Comprehensive API documentation for all Semantic Kernel components

## 📋 Table of Contents

- [Core Kernel API](#core-kernel-api)
- [Plugin Development](#plugin-development)
- [Memory Systems](#memory-systems)
- [Planning & Orchestration](#planning--orchestration)
- [Chat & Conversations](#chat--conversations)
- [Model Context Protocol (MCP)](#model-context-protocol-mcp)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## 🔧 Core Kernel API

### Kernel Builder (.NET)

```csharp
using Microsoft.SemanticKernel;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

// Create a kernel with OpenAI
var builder = Kernel.CreateBuilder()
    .AddOpenAIChatCompletion(
        modelId: "gpt-4",
        apiKey: Environment.GetEnvironmentVariable("OPENAI_API_KEY"))
    .AddLogging(services => services.AddConsole());

var kernel = builder.Build();
```

### Kernel Builder (Python)

```python
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.core_plugins import TimePlugin

# Create kernel
kernel = Kernel()

# Add AI service
kernel.add_service(OpenAIChatCompletion(
    service_id="openai",
    ai_model_id="gpt-4",
    api_key="your-api-key"
))

# Add plugins
kernel.add_plugin(TimePlugin(), plugin_name="time")
```

### Function Invocation

#### .NET

```csharp
// Create a function from a method
var weatherFunction = KernelFunctionFactory.CreateFromMethod(
    (string location) => $"Weather in {location}: Sunny, 72°F",
    "GetWeather",
    "Gets current weather for a location"
);

// Import the function
kernel.ImportPluginFromFunctions("WeatherPlugin", [weatherFunction]);

// Invoke the function
var result = await kernel.InvokeAsync("WeatherPlugin", "GetWeather",
    new KernelArguments { ["location"] = "Seattle" });

Console.WriteLine(result.GetValue<string>());
```

#### Python

```python
from semantic_kernel.functions import kernel_function

class WeatherPlugin:
    @kernel_function(
        description="Gets current weather for a location",
        name="get_weather"
    )
    def get_weather(self, location: str) -> str:
        return f"Weather in {location}: Sunny, 72°F"

# Add plugin to kernel
kernel.add_plugin(WeatherPlugin(), plugin_name="weather")

# Invoke function
result = await kernel.invoke("weather", "get_weather", location="Seattle")
print(result.value)
```

## 🔌 Plugin Development

### Plugin Structure (.NET)

```csharp
using Microsoft.SemanticKernel;
using System.ComponentModel;

public class MathPlugin
{
    [KernelFunction]
    [Description("Add two numbers")]
    public double Add(
        [Description("First number")] double a,
        [Description("Second number")] double b)
    {
        return a + b;
    }

    [KernelFunction]
    [Description("Calculate percentage")]
    public double Percentage(
        [Description("Part value")] double part,
        [Description("Total value")] double total)
    {
        return (part / total) * 100;
    }
}

// Register plugin
kernel.ImportPluginFromType<MathPlugin>("math");
```

### Plugin Structure (Python)

```python
from semantic_kernel.functions import kernel_function
from typing import Annotated

class MathPlugin:
    @kernel_function(
        description="Add two numbers",
        name="add"
    )
    def add(
        self,
        a: Annotated[float, "First number"],
        b: Annotated[float, "Second number"]
    ) -> Annotated[float, "Sum of a and b"]:
        return a + b

    @kernel_function(
        description="Calculate percentage",
        name="percentage"
    )
    def percentage(
        self,
        part: Annotated[float, "Part value"],
        total: Annotated[float, "Total value"]
    ) -> Annotated[float, "Percentage value"]:
        return (part / total) * 100

# Register plugin
kernel.add_plugin(MathPlugin(), plugin_name="math")
```

### Prompt Functions

#### .NET

```csharp
var promptFunction = KernelFunctionFactory.CreateFromPrompt(
    @"Summarize the following text in {{$style}} style:

{{$input}}

Summary:",
    new PromptTemplateConfig
    {
        Name = "Summarize",
        Description = "Summarizes text in a specified style",
        InputVariables = [
            new InputVariable { Name = "input", Description = "Text to summarize" },
            new InputVariable { Name = "style", Description = "Writing style" }
        ]
    }
);

kernel.ImportPluginFromFunctions("TextPlugin", [promptFunction]);

var result = await kernel.InvokeAsync("TextPlugin", "Summarize",
    new KernelArguments
    {
        ["input"] = "Long text to summarize...",
        ["style"] = "academic"
    });
```

#### Python

```python
from semantic_kernel.functions import kernel_function
from semantic_kernel.prompt_template import PromptTemplateConfig

prompt_template = """
Summarize the following text in {{$style}} style:

{{$input}}

Summary:
"""

summarize_function = kernel.create_function_from_prompt(
    prompt=prompt_template,
    function_name="summarize",
    description="Summarizes text in a specified style"
)

kernel.add_function("text", summarize_function)

result = await kernel.invoke(
    "text",
    "summarize",
    input="Long text to summarize...",
    style="academic"
)
```

## 🧠 Memory Systems

### Semantic Memory (.NET)

```csharp
using Microsoft.SemanticKernel.Memory;
using Microsoft.SemanticKernel.Connectors.OpenAI;

// Create memory with embeddings
var memoryBuilder = new MemoryBuilder()
    .WithOpenAITextEmbeddingGeneration("text-embedding-ada-002", apiKey)
    .WithMemoryStore(new VolatileMemoryStore());

var memory = memoryBuilder.Build();

// Store memories
await memory.SaveInformationAsync(
    collection: "facts",
    text: "The capital of France is Paris",
    id: "fact1"
);

await memory.SaveInformationAsync(
    collection: "facts",
    text: "The Eiffel Tower is in Paris",
    id: "fact2"
);

// Search memories
var results = memory.SearchAsync(
    collection: "facts",
    query: "What is the capital of France?",
    limit: 2
);

await foreach (var result in results)
{
    Console.WriteLine($"{result.Metadata.Text} (Score: {result.Relevance})");
}
```

### Semantic Memory (Python)

```python
from semantic_kernel.memory import SemanticTextMemory
from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding
from semantic_kernel.memory.memory_stores import VolatileMemoryStore

# Create memory
embedding_generator = OpenAITextEmbedding(
    ai_model_id="text-embedding-ada-002",
    api_key="your-api-key"
)

memory = SemanticTextMemory(
    storage=VolatileMemoryStore(),
    embeddings_generator=embedding_generator
)

# Store memories
await memory.save_information(
    collection="facts",
    text="The capital of France is Paris",
    id="fact1"
)

await memory.save_information(
    collection="facts",
    text="The Eiffel Tower is in Paris",
    id="fact2"
)

# Search memories
results = await memory.search(
    collection="facts",
    query="What is the capital of France?",
    limit=2
)

for result in results:
    print(f"{result.text} (Score: {result.relevance})")
```

## 📋 Planning & Orchestration

### Function Calling Planner (.NET)

```csharp
using Microsoft.SemanticKernel.Planning;

// Create planner
var planner = new FunctionCallingStepwisePlanner(
    new FunctionCallingStepwisePlannerOptions
    {
        MaxIterations = 10,
        MaxTokens = 4000
    }
);

// Create a plan
var plan = await planner.CreatePlanAsync(kernel,
    "What is the weather in Seattle and what should I wear?");

// Execute the plan
var planResult = await plan.InvokeAsync(kernel);

Console.WriteLine($"Plan result: {planResult}");
```

### Handlebars Planner (.NET)

```csharp
using Microsoft.SemanticKernel.Planning.Handlebars;

var planner = new HandlebarsPlanner(
    new HandlebarsPlannerOptions
    {
        AllowLoops = true,
        MaxIterations = 10
    }
);

var plan = await planner.CreatePlanAsync(kernel,
    "Create a travel itinerary for a 3-day trip to Paris");

var result = await plan.InvokeAsync(kernel,
    new KernelArguments
    {
        ["destination"] = "Paris",
        ["days"] = "3",
        ["interests"] = "museums, food, architecture"
    });
```

### Sequential Planner (Python)

```python
from semantic_kernel.planning import SequentialPlanner

# Create planner
planner = SequentialPlanner(kernel)

# Create plan
plan = await planner.create_plan(
    "What is the weather in Seattle and what should I wear?"
)

# Execute plan
result = await plan.invoke()
print(f"Plan result: {result}")
```

## 💬 Chat & Conversations

### Chat History (.NET)

```csharp
using Microsoft.SemanticKernel.ChatCompletion;

var chatCompletionService = kernel.GetRequiredService<IChatCompletionService>();

var history = new ChatHistory();
history.AddSystemMessage("You are a helpful AI assistant.");
history.AddUserMessage("What is the capital of France?");

var response = await chatCompletionService.GetChatMessageContentAsync(
    history,
    kernel: kernel
);

history.AddMessage(response.Role, response.Content ?? string.Empty);
Console.WriteLine(response.Content);
```

### Streaming Chat (.NET)

```csharp
var history = new ChatHistory();
history.AddSystemMessage("You are a helpful AI assistant.");
history.AddUserMessage("Tell me a story about a robot.");

await foreach (var streamChunk in chatCompletionService.GetStreamingChatMessageContentsAsync(
    history, kernel: kernel))
{
    Console.Write(streamChunk.Content);
}
```

### Chat Completion (Python)

```python
from semantic_kernel.contents import ChatHistory

# Get chat completion service
chat_completion = kernel.get_service(type=ChatCompletion)

# Create chat history
history = ChatHistory()
history.add_system_message("You are a helpful AI assistant.")
history.add_user_message("What is the capital of France?")

# Get response
response = await chat_completion.get_chat_message_content(
    chat_history=history,
    settings=OpenAIChatPromptExecutionSettings()
)

history.add_message(response)
print(response.content)
```

### Streaming Chat (Python)

```python
async for stream_chunk in chat_completion.get_streaming_chat_message_content(
    chat_history=history,
    settings=OpenAIChatPromptExecutionSettings()
):
    print(stream_chunk.content, end="")
```

## 🔌 Model Context Protocol (MCP)

### MCP Client (.NET)

```csharp
using System.Net.Http;
using System.Text.Json;

public class MCPClient
{
    private readonly HttpClient _httpClient;
    private int _requestId = 0;

    public MCPClient(string serverUrl)
    {
        _httpClient = new HttpClient { BaseAddress = new Uri(serverUrl) };
    }

    public async Task<T?> SendRequestAsync<T>(string method, object? parameters = null)
    {
        var request = new
        {
            jsonrpc = "2.0",
            id = (++_requestId).ToString(),
            method = method,
            @params = parameters
        };

        var json = JsonSerializer.Serialize(request);
        var content = new StringContent(json, System.Text.Encoding.UTF8, "application/json");

        var response = await _httpClient.PostAsync("/mcp", content);
        var responseJson = await response.Content.ReadAsStringAsync();

        using var document = JsonDocument.Parse(responseJson);
        var result = document.RootElement.GetProperty("result");

        return JsonSerializer.Deserialize<T>(result.GetRawText());
    }
}

// Usage
var mcpClient = new MCPClient("http://localhost:8080");

var capabilities = await mcpClient.SendRequestAsync<dynamic>("capabilities/list");
Console.WriteLine($"Server capabilities: {capabilities}");
```

### MCP Client (Python)

```python
import aiohttp
import json

class MCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.request_id = 0

    async def send_request(self, method: str, params: dict = None):
        self.request_id += 1

        request = {
            "jsonrpc": "2.0",
            "id": str(self.request_id),
            "method": method,
            "params": params or {}
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.server_url}/mcp",
                json=request
            ) as response:
                result = await response.json()
                return result.get("result")

# Usage
mcp_client = MCPClient("http://localhost:8080")

capabilities = await mcp_client.send_request("capabilities/list")
print(f"Server capabilities: {capabilities}")

# Solve a problem
solution = await mcp_client.send_request("reasoning/solve", {
    "problem": "How to optimize renewable energy distribution?",
    "context": {"domain": "energy"},
    "reasoning_types": ["deductive", "creative"]
})
```

## 🚨 Error Handling

### Exception Handling (.NET)

```csharp
using Microsoft.SemanticKernel;

try
{
    var result = await kernel.InvokeAsync("plugin", "function",
        new KernelArguments { ["input"] = "test" });
}
catch (KernelException ex)
{
    Console.WriteLine($"Kernel error: {ex.Message}");
    // Handle semantic kernel specific errors
}
catch (HttpRequestException ex)
{
    Console.WriteLine($"Network error: {ex.Message}");
    // Handle network/API errors
}
catch (ArgumentException ex)
{
    Console.WriteLine($"Invalid argument: {ex.Message}");
    // Handle invalid parameters
}
catch (Exception ex)
{
    Console.WriteLine($"Unexpected error: {ex.Message}");
    // Handle all other errors
}
```

### Error Handling (Python)

```python
from semantic_kernel.exceptions import (
    KernelException,
    ServiceInvalidAuthError,
    ServiceInvalidRequestError
)

try:
    result = await kernel.invoke("plugin", "function", input="test")
except ServiceInvalidAuthError as e:
    print(f"Authentication error: {e}")
    # Handle authentication issues
except ServiceInvalidRequestError as e:
    print(f"Invalid request: {e}")
    # Handle request format issues
except KernelException as e:
    print(f"Kernel error: {e}")
    # Handle semantic kernel errors
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle all other errors
```

### Retry Logic

```csharp
using Polly;

var retryPolicy = Policy
    .Handle<HttpRequestException>()
    .Or<TaskCanceledException>()
    .WaitAndRetryAsync(
        retryCount: 3,
        sleepDurationProvider: retryAttempt => TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)),
        onRetry: (outcome, timespan, retryCount, context) =>
        {
            Console.WriteLine($"Retry {retryCount} after {timespan} seconds");
        });

var result = await retryPolicy.ExecuteAsync(async () =>
{
    return await kernel.InvokeAsync("plugin", "function", arguments);
});
```

## 📋 Best Practices

### Configuration Management

#### .NET

```csharp
// Use configuration providers
var configuration = new ConfigurationBuilder()
    .AddJsonFile("appsettings.json")
    .AddEnvironmentVariables()
    .AddUserSecrets<Program>()
    .Build();

var builder = Kernel.CreateBuilder()
    .AddOpenAIChatCompletion(
        modelId: configuration["OpenAI:ModelId"]!,
        apiKey: configuration["OpenAI:ApiKey"]!)
    .AddLogging(services => services.AddConsole());
```

#### Python

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

kernel = Kernel()
kernel.add_service(OpenAIChatCompletion(
    ai_model_id=os.getenv("OPENAI_MODEL_ID", "gpt-4"),
    api_key=os.getenv("OPENAI_API_KEY")
))
```

### Resource Management

```csharp
// Use using statements for proper disposal
using var kernel = Kernel.CreateBuilder()
    .AddOpenAIChatCompletion(modelId, apiKey)
    .Build();

// Configure timeouts
var settings = new OpenAIPromptExecutionSettings
{
    MaxTokens = 1000,
    Temperature = 0.7,
    TopP = 1.0
};
```

### Security Considerations

```csharp
// Input validation
public class SecurePlugin
{
    [KernelFunction]
    public string ProcessInput(
        [Description("User input")] string input)
    {
        // Validate and sanitize input
        if (string.IsNullOrWhiteSpace(input))
            throw new ArgumentException("Input cannot be empty");

        if (input.Length > 1000)
            throw new ArgumentException("Input too long");

        // Remove potentially dangerous characters
        var sanitized = System.Text.RegularExpressions.Regex.Replace(
            input, @"[<>""']", "");

        return ProcessSafeInput(sanitized);
    }
}
```

### Performance Optimization

```csharp
// Use streaming for long responses
await foreach (var chunk in chatCompletion.GetStreamingChatMessageContentsAsync(
    chatHistory, settings, kernel))
{
    // Process chunks as they arrive
    yield return chunk.Content;
}

// Batch operations when possible
var tasks = inputs.Select(input =>
    kernel.InvokeAsync("plugin", "function",
        new KernelArguments { ["input"] = input }));

var results = await Task.WhenAll(tasks);
```

### Logging and Monitoring

```csharp
using Microsoft.Extensions.Logging;

public class MonitoredPlugin
{
    private readonly ILogger<MonitoredPlugin> _logger;

    public MonitoredPlugin(ILogger<MonitoredPlugin> logger)
    {
        _logger = logger;
    }

    [KernelFunction]
    public async Task<string> ProcessDataAsync(string input)
    {
        _logger.LogInformation("Processing input: {Input}", input);

        var stopwatch = System.Diagnostics.Stopwatch.StartNew();

        try
        {
            var result = await ProcessInputAsync(input);

            _logger.LogInformation("Processing completed in {ElapsedMs}ms",
                stopwatch.ElapsedMilliseconds);

            return result;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error processing input: {Input}", input);
            throw;
        }
    }
}
```

## 📚 Additional Resources

### Documentation Links

- **[Official Semantic Kernel Docs](https://learn.microsoft.com/semantic-kernel/)**
- **[.NET API Reference](https://learn.microsoft.com/dotnet/api/microsoft.semantickernel)**
- **[Python API Reference](https://python.semantic-kernel.readthedocs.io/)**
- **[GitHub Repository](https://github.com/microsoft/semantic-kernel)**

### Sample Applications

- **[.NET Samples](https://github.com/microsoft/semantic-kernel/tree/main/dotnet/samples)**
- **[Python Samples](https://github.com/microsoft/semantic-kernel/tree/main/python/samples)**
- **[Jupyter Notebooks](https://github.com/microsoft/semantic-kernel/tree/main/python/notebooks)**

### Community Resources

- **[Discord Community](https://aka.ms/SKDiscord)**
- **[GitHub Discussions](https://github.com/microsoft/semantic-kernel/discussions)**
- **[Stack Overflow](https://stackoverflow.com/questions/tagged/semantic-kernel)**

---

**Last Updated**: June 22, 2025
**Version**: 2.0
**Maintainers**: Semantic Kernel Documentation Team
