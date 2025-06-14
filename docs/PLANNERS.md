# Semantic Kernel Planner

The Semantic Kernel Planner module is a powerful tool that allows you to automatically orchestrate AI tasks and workflows. This document provides an overview of the planner module, its features, and examples of how to use it effectively.

## Overview

The planner module enables you to define and execute plans that consist of multiple steps, each representing a specific task or action. These plans can be used to automate complex workflows, coordinate multiple AI services, and achieve specific goals.

## Features

- **Automatic Orchestration**: The planner module can automatically orchestrate AI tasks and workflows based on predefined plans.
- **Flexible Plans**: Plans can be customized to include various tasks, conditions, and dependencies.
- **Integration with AI Services**: The planner module can integrate with various AI services, such as OpenAI, Azure OpenAI, and Hugging Face, to perform tasks like text generation, image recognition, and more.
- **Error Handling**: The planner module includes built-in error handling to ensure that tasks are executed smoothly and any issues are addressed.

## Examples

### Example 1: Simple Plan

```python
from semantic_kernel import Planner

# Define a simple plan with two steps
plan = Planner()
plan.add_step("Generate text", service="OpenAI", model="text-davinci-003", prompt="Write a short story about a robot.")
plan.add_step("Summarize text", service="OpenAI", model="text-davinci-003", prompt="Summarize the following text: {generated_text}")

# Execute the plan
result = plan.execute()
print(result)
```

### Example 2: Conditional Plan

```python
from semantic_kernel import Planner

# Define a plan with a conditional step
plan = Planner()
plan.add_step("Generate text", service="OpenAI", model="text-davinci-003", prompt="Write a short story about a robot.")
plan.add_step("Check text length", condition="len(generated_text) > 100", true_step="Summarize text", false_step="Generate more text")
plan.add_step("Summarize text", service="OpenAI", model="text-davinci-003", prompt="Summarize the following text: {generated_text}")
plan.add_step("Generate more text", service="OpenAI", model="text-davinci-003", prompt="Continue the story: {generated_text}")

# Execute the plan
result = plan.execute()
print(result)
```

### Example 3: Plan with Dependencies

```python
from semantic_kernel import Planner

# Define a plan with dependencies between steps
plan = Planner()
plan.add_step("Generate text", service="OpenAI", model="text-davinci-003", prompt="Write a short story about a robot.")
plan.add_step("Translate text", service="Azure OpenAI", model="translation", prompt="Translate the following text to French: {generated_text}", depends_on="Generate text")
plan.add_step("Summarize text", service="Hugging Face", model="summarization", prompt="Summarize the following text: {translated_text}", depends_on="Translate text")

# Execute the plan
result = plan.execute()
print(result)
```

### Example 4: Plan with Error Handling

```python
from semantic_kernel import Planner

# Define a plan with error handling
plan = Planner()
plan.add_step("Generate text", service="OpenAI", model="text-davinci-003", prompt="Write a short story about a robot.")
plan.add_step("Summarize text", service="OpenAI", model="text-davinci-003", prompt="Summarize the following text: {generated_text}")
plan.add_error_handler("Summarize text", handler="Handle error", service="OpenAI", model="text-davinci-003", prompt="An error occurred while summarizing the text. Please try again.")

# Execute the plan
result = plan.execute()
print(result)
```

### Example 5: Plan with Multiple AI Services

```python
from semantic_kernel import Planner

# Define a plan that uses multiple AI services
plan = Planner()
plan.add_step("Generate text", service="OpenAI", model="text-davinci-003", prompt="Write a short story about a robot.")
plan.add_step("Translate text", service="Azure OpenAI", model="translation", prompt="Translate the following text to French: {generated_text}")
plan.add_step("Summarize text", service="Hugging Face", model="summarization", prompt="Summarize the following text: {translated_text}")

# Execute the plan
result = plan.execute()
print(result)
```

## Use Cases

The planner module can be used in various scenarios, including:

- **Content Generation**: Automate the generation of articles, blog posts, and other content by defining plans that include text generation, summarization, and translation tasks.
- **Data Processing**: Coordinate multiple AI services to process and analyze data, such as extracting information from documents, performing sentiment analysis, and generating reports.
- **Workflow Automation**: Automate complex workflows that involve multiple steps and dependencies, such as customer support processes, data pipelines, and more.

By leveraging the planner module, you can streamline your AI workflows, improve efficiency, and achieve better results with minimal manual intervention.
To make an update on the page, file a PR on the [docs repo.](https://github.com/MicrosoftDocs/semantic-kernel-docs/blob/main/semantic-kernel/concepts/planning.md)
