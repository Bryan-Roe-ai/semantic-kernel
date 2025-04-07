consulted: dmytrostruk
contact: markwallace-microsoft
date: 2023-10-26T00:00:00Z
deciders: matthewbolanos, markwallace-microsoft, SergeyMenshykh, RogerBarreto
informed: null
runme:
  document:
    relativePath: 0018-custom-prompt-template-formats.md
  session:
    id: 01J6KPJ8XM6CDP9YHD1ZQR868H
    updated: 2024-08-31 07:59:27Z
status: approved

# Custom Prompt Template Formats

## Table of Contents
- [Context and Problem Statement](#context-and-problem-statement)
- [Current Design](#current-design)
- [Code Patterns](#code-patterns)
- [Performance](#performance)
- [Implementing a Custom Prompt Template Engine](#implementing-a-custom-prompt-template-engine)
- [Handlebars Considerations](#handlebars-considerations)
- [Decision Drivers](#decision-drivers)
- [Considered Options](#considered-options)
- [Decision Outcome](#decision-outcome)

## Context and Problem Statement

Semantic Kernel currently supports a custom prompt template language that allows for variable interpolation and function execution. Semantic Kernel allows for custom prompt template formats to be integrated, e.g., prompt templates using [Handlebars](https://github.com/Handlebars-Net/Handlebars.Net) syntax

The purpose of this ADR is to describe how custom prompt template formats will be supported in the Semantic Kernel

By default, the `Kernel` uses the `BasicPromptTemplateEngine`, which supports the Semantic Kernel-specific template format

### Code Patterns

Below is an expanded example of how to create a semantic function from a prompt template string using the built-in Semantic Kernel format:

IKernel kernel = Kernel.Builder
    .WithPromptTemplateEngine(new BasicPromptTemplateEngine())
    .WithOpenAIChatCompletionService(
        apiKey: openAIApiKey)

1. You need to have a `Kernel` instance to create a semantic function, which contradicts the goal of creating semantic functions once and reusing them across multiple `Kernel` instances.
4. Our semantic function extension methods rely on our implementation of `IPromptTemplate` (i.e., `PromptTemplate`), which stores the template string and uses the 
| ---------------- | ------- | ------------ |
| Render variables | 168     | 0            |
| Operation        | Ticks | Milliseconds |
| ---------------- | ----- | ------------ |
| Compile template | 66277 | 6            |
| Render variables | 4173  | 0            |

public interface IPromptTemplate
{
    IReadOnlyList<ParameterView> Parameters { get; }
    Task<string> RenderAsync(SKContext executionContext, CancellationToken cancellationToken = default);
}
A prototype implementation of a Handlebars prompt template engine could look like this:

public class HandlebarsTemplateEngine : IPromptTemplateEngine
{
    private readonly ILoggerFactory _loggerFactory;
    public HandlebarsTemplateEngine(ILoggerFactory? loggerFactory = null)
    {
        this._loggerFactory = loggerFactory ?? NullLoggerFactory.Instance;

    public async Task<string> RenderAsync(string templateText, SKContext context, CancellationToken cancellationToken = default)
    {

        var functionViews = context.Functions.GetFunctionViews();
        foreach (FunctionView functionView in functionViews)
        {
            var skfunction = context.Functions.GetFunction(functionView.PluginName, functionView.Name);
            handlebars.RegisterHelper($"{functionView.PluginName}_{functionView.Name}", async (writer, hcontext, parameters) =>
                {
                    var result = await skfunction.InvokeAsync(context).ConfigureAwait(true);
                    writer.WriteSafeString(result.GetValue<string>());
                });
        }

    }
}

**Note: This is just a prototype implementation for illustration purposes only.**

Some issues:
1. The `IPromptTemplate` interface is not used and causes confusion.
2. There is no way to allow developers to support multiple prompt template formats simultaneously.

There is one implementation of `IPromptTemplate` provided in the Semantic Kernel core package. The `RenderAsync` implementation delegates to the `IPromptTemplateEngine`. The `Parameters` list gets populated with the parameters defined in the `PromptTemplateConfig` and any missing variables defined in the template.

## Handlebars Considerations


```csharp
HandlebarsHelper link_to = (writer, context, parameters) =>
{
    writer.WriteSafeString($"<a href='{context["url"]}'>{context["text"]}</a>");
};

string source = @"Click here: {{link_to}}";

var data = new
{
    url = "https://github.com",
    text = "Handlebars.Net"
};

var handlebars = HandlebarsDotNet.Handlebars.Create();
handlebars.RegisterHelper("link_to", link_to);
var template = handlebars.Compile(source);
var result = template(data);
```

Handlebars allows the helpers to be registered with the `Handlebars` instance either before or after a template is compiled. The optimum would be to have a shared `Handlebars` instance for a specific collection of functions and register the helpers just once. For use cases where the Kernel function collection may have been mutated, we will be forced to create a `Handlebars` instance at render time and then register the helpers. This means we cannot take advantage of the performance improvement provided by compiling the template.

## Decision Drivers

In no particular order:

- Support creating a semantic function without a `IKernel` instance.
- Support late binding of functions, i.e., having functions resolved when the prompt is rendered.
- Support allowing the prompt template to be parsed (compiled) just once to optimize performance if needed.
- Support using multiple prompt template formats with a single `Kernel` instance.
- Provide simple abstractions that allow third parties to implement support for custom prompt template formats.

## Considered Options

- Obsolete `IPromptTemplateEngine` and replace it with `IPromptTemplateFactory`.

### Obsolete `IPromptTemplateEngine` and replace with `IPromptTemplateFactory`

![ISKFunction class relationships](./diagrams/prompt-template-factory.png)

Below is an expanded example of how to create a semantic function from a prompt template string using the built-in Semantic Kernel format:

```csharp
// Semantic function can be created once
var promptTemplateFactory = new BasicPromptTemplateFactory();
string templateString = "Today is: {{time.Date}} Is it weekend time (weekend/not weekend)?";
var promptTemplate = promptTemplateFactory.CreatePromptTemplate(templateString, new PromptTemplateConfig());
var kindOfDay = ISKFunction.CreateSemanticFunction("KindOfDay", promptTemplateConfig, promptTemplate);

// Create Kernel after creating the semantic function
// Later we will support passing a function collection to the KernelBuilder
IKernel kernel = Kernel.Builder
    .WithOpenAIChatCompletionService(
        modelId: openAIModelId,
        apiKey: openAIApiKey)
    .Build();

kernel.ImportFunctions(new TimePlugin(), "time");
// Optionally register the semantic function with the Kernel
// kernel.RegisterCustomFunction(kindOfDay);

var result = await kernel.RunAsync(kindOfDay);
Console.WriteLine(result.GetValue<string>());
```

**Notes:**

- `BasicPromptTemplateFactory` will be the default implementation and will be automatically provided in `KernelSemanticFunctionExtensions`. Developers will also be able to provide their own implementations.
- The factory uses the new `PromptTemplateConfig.TemplateFormat` to create the appropriate `IPromptTemplate` instance.
- We should look to remove `promptTemplateConfig` as a parameter to `CreateSemanticFunction`. That change is outside the scope of this ADR.

The `BasicPromptTemplateFactory` and `BasicPromptTemplate` implementations look as follows:

```csharp
public sealed class BasicPromptTemplateFactory : IPromptTemplateFactory
{
    private readonly IPromptTemplateFactory _promptTemplateFactory;
    private readonly ILoggerFactory _loggerFactory;

    public BasicPromptTemplateFactory(IPromptTemplateFactory promptTemplateFactory, ILoggerFactory? loggerFactory = null)
    {
        this._promptTemplateFactory = promptTemplateFactory;
        this._loggerFactory = loggerFactory ?? NullLoggerFactory.Instance;
    }

    public IPromptTemplate? CreatePromptTemplate(string templateString, PromptTemplateConfig promptTemplateConfig)
    {
        if (promptTemplateConfig.TemplateFormat.Equals(PromptTemplateConfig.SEMANTICKERNEL, System.StringComparison.Ordinal))
        {
            return new BasicPromptTemplate(templateString, promptTemplateConfig, this._loggerFactory);
        }
        else if (this._promptTemplateFactory is not null)
        {
            return this._promptTemplateFactory.CreatePromptTemplate(templateString, promptTemplateConfig);
        }

        throw new SKException($"Invalid prompt template format {promptTemplateConfig.TemplateFormat}");
    }
}

public sealed class BasicPromptTemplate : IPromptTemplate
{
    public BasicPromptTemplate(string templateString, PromptTemplateConfig promptTemplateConfig, ILoggerFactory? loggerFactory = null)
    {
        this._loggerFactory = loggerFactory ?? NullLoggerFactory.Instance;
        this._logger = this._loggerFactory.CreateLogger(typeof(BasicPromptTemplate));
        this._templateString = templateString;
        this._promptTemplateConfig = promptTemplateConfig;
        this._parameters = new(() => this.InitParameters());
        this._blocks = new(() => this.ExtractBlocks(this._templateString));
        this._tokenizer = new TemplateTokenizer(this._loggerFactory);
    }

    public IReadOnlyList<ParameterView> Parameters => this._parameters.Value;

    public async Task<string> RenderAsync(SKContext executionContext, CancellationToken cancellationToken = default)
    {
        return await this.RenderAsync(this._blocks.Value, executionContext, cancellationToken).ConfigureAwait(false);
    }

    // Not showing the implementation details
}
```

**Note:**

- The call to `ExtractBlocks` is called lazily once for each prompt template.
- The `RenderAsync` doesn't need to extract the blocks every time.

## Decision Outcome

Chosen option: "Obsolete `IPromptTemplateEngine` and replace with `IPromptTemplateFactory`", because it addresses the requirements and provides good flexibility for the future.
