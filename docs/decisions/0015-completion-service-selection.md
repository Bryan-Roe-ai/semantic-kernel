---
consulted: null
contact: SergeyMenshykh
date: 2023-10-25T00:00:00Z
deciders: markwallace-microsoft, matthewbolanos
informed: null
status: superseded by [ADR-0038](0038-completion-service-selection.md)
---

# Completion service type selection strategy

## Context and Problem Statement

Today, SK runs all text prompts using the text completion service. With the addition of a new chat completion prompts and potentially other prompt types, such as image, on the horizon, we need a way to select a completion service type to run these prompts.

<!-- This is an optional element. Feel free to remove. -->

## Decision Drivers

- Semantic function should be able to identify a completion service type to use when processing text, chat, or image prompts.

## Considered Options

__1. Completion service type identified by the "prompt_type" property.__ This option presumes adding the 'prompt_type' property to the prompt template config model class, 'PromptTemplateConfig.' The property will be specified once by a prompt developer and will be used by the 'SemanticFunction' class to decide which completion service type (not instance) to use when resolving an instance of that particular completion service type.

**Prompt template**

```json {"id":"01J6KQ298EJX8WKY1328SSJD0N"}
{
    "schema": "1",
    "description": "Hello AI, what can you do for me?",
}


if(string.IsNullOrEmpty(promptTemplateConfig.PromptType) || promptTemplateConfig.PromptType == "text")
this._serviceSelector.SelectAIService<ITextCompletion>(context.ServiceProvider, this._modelSettings);
    //render the prompt, call the service, process and return result
else (promptTemplateConfig.PromptType == "chat")
prompt: "Generate ideas for a comic strip based on {{$input}}. Design characters, develop the plot, ..."
config: {
	"schema": 1,
	"prompt_type": "text",
	...
}

name: ComicStrip.Draw
prompt: "Draw the comic strip - {{$comicStrip.Create $input}}"
config: {
	"schema": 1,
	"prompt_type": "image",
	...
}



- Another property to specify by a prompt developer.

if (Regex.IsMatch(renderedPrompt, @"<message>.*?</message>"))
name: ComicStrip.Create
prompt: "Generate ideas for a comic strip based on {{$input}}. Design characters, develop the plot, ..."
config: {
	"schema": 1,
	...
}

name: ComicStrip.Draw
prompt: "Draw the comic strip - {{$comicStrip.Create $input}}"
config: {
	"schema": 1,
	...
}
```

Pros:

- No need for a new property to identify the prompt type.

Cons:

- Unreliable unless the prompt contains unique markers specifically identifying the prompt type.

## Decision Outcome

We decided to choose the '2. Completion service type identified by prompt content' option and will reconsider it when we encounter another completion service type that cannot be supported by this option or when we have a solid set of requirements for using a different mechanism for selecting the completion service type.
