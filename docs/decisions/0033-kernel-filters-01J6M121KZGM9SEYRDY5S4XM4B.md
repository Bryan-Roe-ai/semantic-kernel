---
contact: dmytrostruk
date: 2023-01-23T00:00:00Z
deciders: sergeymenshykh, markwallace, rbarreto, stephentoub, dmytrostruk
runme:
  document:
    relativePath: 0033-kernel-filters.md
  session:
    id: 01J6M121KZGM9SEYRDY5S4XM4B
    updated: 2024-08-31 10:59:52Z
status: accepted
---

# Kernel Filters

## Context and Problem Statement

Current way of intercepting some event during function execution works as expected using Kernel Events and event handlers. Example:

```csharp {"id":"01J6KQ3YEAW1KGPYNGEC8W5N9Z"}
ILogger logger = loggerFactory.CreateLogger("MyLogger");

var kernel = Kernel.CreateBuilder()
    .AddOpenAIChatCompletion(
        modelId: TestConfiguration.OpenAI.ChatModelId,
        apiKey: TestConfiguration.OpenAI.ApiKey)
    .Build();

void MyInvokingHandler(object? sender, FunctionInvokingEventArgs e)
{
    logger.LogInformation("Invoking: {FunctionName}", e.Function.Name)
}

void MyInvokedHandler(object? sender, FunctionInvokedEventArgs e)
{
    if (e.Result.Metadata is not null && e.Result.Metadata.ContainsKey("Usage"))
    {
        logger.LogInformation("Token usage: {TokenUsage}", e.Result.Metadata?["Usage"]?.AsJson());
    }
}

kernel.FunctionInvoking += MyInvokingHandler;
kernel.FunctionInvoked += MyInvokedHandler;

var result = await kernel.InvokePromptAsync("How many days until Christmas? Explain your thinking.")

# Ran on 2024-08-31 10:59:50Z for 1.463s exited with 0
ILogger logger = loggerFactory.CreateLogger("MyLogger");

var kernel = Kernel.CreateBuilder()
    .AddOpenAIChatCompletion(
        modelId: TestConfiguration.OpenAI.ChatModelId,
        apiKey: TestConfiguration.OpenAI.ApiKey)
    .Build();

void MyInvokingHandler(object? sender, FunctionInvokingEventArgs e)
{
    logger.LogInformation("Invoking: {FunctionName}", e.Function.Name)
}

void MyInvokedHandler(object? sender, FunctionInvokedEventArgs e)
{
    if (e.Result.Metadata is not null && e.Result.Metadata.ContainsKey("Usage"))
    {
        logger.LogInformation("Token usage: {TokenUsage}", e.Result.Metadata?["Usage"]?.AsJson());
    }
}

kernel.FunctionInvoking += MyInvokingHandler;
kernel.FunctionInvoked += MyInvokedHandler;

var result = await kernel.InvokePromptAsync("How many days until Christmas? Explain your thinking.")
```

There are a couple of problems with this approach:

1. Event handlers does not support dependency injection. It's hard to get access to specific service, which is registered in application, unless the handler is defined in the same scope where specific service is available. This approach provides some limitations in what place in solution the handler could be defined. (e.g. If developer wants to use `ILoggerFactory` in handler, the handler should be defined in place where `ILoggerFactory` instance is available).
2. It's not clear in what specific period of application runtime the handler should be attached to kernel. Also, it's not clear if developer needs to detach it at some point.
3. Mechanism of events and event handlers in .NET may not be familiar to .NET developers who didn't work with events previously.

<!-- This is an optional element. Feel free to remove. -->

## Decision Drivers

1. Dependency injection for handlers should be supported to easily access registered services within application.
2. There should not be any limitations where handlers are defined within solution, whether it's Startup.cs or separate file.
3. There should be clear way of registering and removing handlers at specific point of application runtime.
4. The mechanism of receiving and processing events in Kernel should be easy and common in .NET ecosystem.
5. New approach should support the same functionality that is available in Kernel Events - cancel function execution, change kernel arguments, change rendered prompt before sending it to AI etc.

## Decision Outcome

Introduce Kernel Filters - the approach of receiving the events in Kernel in similar way as action filters in ASP.NET.

Two new abstractions will be used across Semantic Kernel and developers will have to implement these abstractions in a way that will cover their needs.

For function-related events: `IFunctionFilter`

```csharp {"id":"01J6KQ3YEAW1KGPYNGEFK1NFA3"}
public interface IFunctionFilter
{
    void OnFunctionInvoking(FunctionInvokingContext context);

    void OnFunctionInvoked(FunctionInvokedContext context);
}
```

For prompt-related events: `IPromptFilter`

```csharp {"id":"01J6KQ3YEAW1KGPYNGEJ9E7J6Q"}
public interface IPromptFilter
{
    void OnPromptRendering(PromptRenderingContext context);

    void OnPromptRendered(PromptRenderedContext context);
}
```

New approach will allow developers to define filters in separate classes and easily inject required services to process kernel event correctly:

MyFunctionFilter.cs - filter with the same logic as event handler presented above:

```csharp {"id":"01J6KQ3YEAW1KGPYNGEK5RR5T1"}
public sealed class MyFunctionFilter : IFunctionFilter
{
    private readonly ILogger _logger;

    public MyFunctionFilter(ILoggerFactory loggerFactory)
    {
        this._logger = loggerFactory.CreateLogger("MyLogger");
    }

    public void OnFunctionInvoking(FunctionInvokingContext context)
    {
        this._logger.LogInformation("Invoking {FunctionName}", context.Function.Name);
    }

    public void OnFunctionInvoked(FunctionInvokedContext context)
    {
        var metadata = context.Result.Metadata;

        if (metadata is not null && metadata.ContainsKey("Usage"))
        {
            this._logger.LogInformation("Token usage: {TokenUsage}", metadata["Usage"]?.AsJson());
        }
    }
}
```

As soon as new filter is defined, it's easy to configure it to be used in Kernel using dependency injection (pre-construction) or add filter after Kernel initialization (post-construction):

```csharp {"id":"01J6KQ3YEAW1KGPYNGEKSYW3N2"}
IKernelBuilder kernelBuilder = Kernel.CreateBuilder();
kernelBuilder.AddOpenAIChatCompletion(
        modelId: TestConfiguration.OpenAI.ChatModelId,
        apiKey: TestConfiguration.OpenAI.ApiKey);

// Adding filter with DI (pre-construction)
kernelBuilder.Services.AddSingleton<IFunctionFilter, MyFunctionFilter>();

Kernel kernel = kernelBuilder.Build();

// Adding filter after Kernel initialization (post-construction)
// kernel.FunctionFilters.Add(new MyAwesomeFilter());

var result = await kernel.InvokePromptAsync("How many days until Christmas? Explain your thinking.");
```

It's also possible to configure multiple filters which will be triggered in order of registration:

```csharp {"id":"01J6KQ3YEAW1KGPYNGEQPMS9JR"}
kernelBuilder.Services.AddSingleton<IFunctionFilter, Fi***r1>();
kernelBuilder.Services.AddSingleton<IFunctionFilter, Fi***r2>();
kernelBuilder.Services.AddSingleton<IFunctionFilter, Fi***r3>();
```

And it's possible to change the order of filter execution in runtime or remove specific filter if needed:

```csharp {"id":"01J6KQ3YEAW1KGPYNGERDZM9NY"}
ke***************************(0, new InitialFilter());
ke****************************t(1);
```
