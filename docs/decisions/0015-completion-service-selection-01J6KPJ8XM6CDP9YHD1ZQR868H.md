consulted: null
contact: SergeyMenshykh
date: 2023-10-25T00:00:00Z
deciders: markwallace-microsoft, matthewbolanos
informed: null
runme:
  document:
    relativePath: 0015-completion-service-selection.md
  session:
    id: 01J6KPJ8XM6CDP9YHD1ZQR868H
    updated: 2024-08-31 07:58:19Z
status: superseded by [ADR-0038](0038-completion-service-selection.md)

# Completion service type selection strategy

## Context and Problem Statement

Today, SK runs all text prompts using the text completion service. With the addition of new chat completion prompts and potentially other prompt types, such as image, on the horizon, we need a way to identify and route these prompts to the correct completion service.

## Decision Drivers

- Semantic function should be able to identify a completion service type to use when processing text, chat, or image prompts.

## Considered Options

### 1. Completion service type identified by the "prompt_type" property

This option presumes adding the 'prompt_type' property to the prompt template config model class, `PromptTemplateConfig`.

**Prompt template**

```json
{
    "schema": "1",
    "description": "Hello AI, what can you do for me?",
    "prompt_type": "<text|chat|image>",
    "models": [...]
}
```

**Semantic function pseudocode**

```csharp
if(string.IsNullOrEmpty(promptTemplateConfig.PromptType) || promptTemplateConfig.PromptType == "text")
{
    var service = this._serviceSelector.SelectAIService<ITextCompletion>(context.ServiceProvider, this._modelSettings);
    // render the prompt, call the service, process and return result
}
else if (promptTemplateConfig.PromptType == "chat")
{
    var service = this._serviceSelector.SelectAIService<IChatCompletion>(context.ServiceProvider, this._modelSettings);
    // render the prompt, call the service, process and return result
}
else if (promptTemplateConfig.PromptType == "image")
{
    var service = this._serviceSelector.SelectAIService<IImageGeneration>(context.ServiceProvider, this._modelSettings);
    // render the prompt, call the service, process and return result
}
```

**Example**

```json
{
    "name": "ComicStrip.Create",
    "prompt": "Generate ideas for a comic strip based on {{$input}}. Design characters, develop the plot, ...",
    "config": {
        "schema": 1,
        "prompt_type": "text",
        ...
    }
}

{
    "name": "ComicStrip.Draw",
    "prompt": "Draw the comic strip - {{$comicStrip.Create $input}}",
    "config": {
        "schema": 1,
        "prompt_type": "image",
        ...
    }
}
```

**Pros:**

- Deterministically specifies which completion service type to use, so image prompts won't be rendered by a text completion service, and vice versa.

**Cons:**

- Another property to specify by a prompt developer.

### 2. Completion service type identified by prompt content

The idea behind this option is to analyze the rendered prompt by using regex to check for the presence of specific markers associated with different prompt types.

**Semantic function pseudocode**

```csharp
if (Regex.IsMatch(renderedPrompt, @"<message>.*?</message>"))
{
    var service = this._serviceSelector.SelectAIService<IChatCompletion>(context.ServiceProvider, this._modelSettings);
    // render the prompt, call the service, process and return result
}
else
{
    var service = this._serviceSelector.SelectAIService<ITextCompletion>(context.ServiceProvider, this._modelSettings);
    // render the prompt, call the service, process and return result
}
```

**Example**

```json
{
    "name": "ComicStrip.Create",
    "prompt": "Generate ideas for a comic strip based on {{$input}}. Design characters, develop the plot, ...",
    "config": {
        "schema": 1,
        ...
    }
}

{
    "name": "ComicStrip.Draw",
    "prompt": "Draw the comic strip - {{$comicStrip.Create $input}}",
    "config": {
        "schema": 1,
        ...
    }
}
```

**Pros:**

- No need for a new property to identify the prompt type.

**Cons:**

- Unreliable unless the prompt contains unique markers specifically identifying the prompt type.

## Decision Outcome

We decided to choose the '2. Completion service type identified by prompt content' option. This approach does not require additional properties in the prompt configuration, making it simpler for prompt developers. However, we acknowledge that it may be unreliable unless the prompts are designed with unique markers. We will reconsider this decision if we encounter another completion service type that cannot be supported by this approach.

```
