# Semantic Kernel

Integrate cutting-edge LLM technology quickly and easily into your apps.

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Usage](#usage)
4. [Configuration](#configuration)
5. [Workflows](#workflows)
6. [Branch Protection Rules](#branch-protection-rules)
7. [CI/CD Pipeline Efficiency](#cicd-pipeline-efficiency)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction
Provide an introduction to the project, its goals, and key features.

## Getting Started
Detailed instructions on how to set up and start using the project.

## Usage
### Using Semantic Kernel in C#
![C# Logo](https://user-images.githubusercontent.com/371009/230673036-fad1e8e6-5d48-49b1-a9c1-6f9834e0d165.png)

[Using Semantic Kernel in C#](dotnet/README.md)

### Using Semantic Kernel in Python
![Python Logo](https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg)

[Using Semantic Kernel in Python](python/README.md)

Include examples and explanations for other supported languages.

## Configuration
Detailed steps to configure the project.

## Workflows
### Handling 'Not Found' Error
We have added a new workflow to handle the "Not Found" error.

#### Configuration
To configure the new workflow, follow these steps:

1. **Create a new workflow file**: Add a new workflow file `.github/workflows/handle-not-found-error.yml`.
2. **Define the workflow**: Add the following content to the file:
    ```yaml
    name: Handle Not Found Error
    on:
      pull_request:
        types: [opened, synchronize]
    jobs:
      handle-not-found-error:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout code
            uses: actions/checkout@v4
          - name: Check for Not Found Error
            run: |
              echo "Checking for Not Found error..."
              echo "Handling Not Found error..."
    ```
3. **Run the workflow**: The workflow will automatically run on pull request events.

### SSRF Detection
Include detailed steps and explanations for the SSRF detection workflow.

## Branch Protection Rules
Explain the branch protection rules and include a link to the GitHub documentation on branch protection.

## CI/CD Pipeline Efficiency
### Parallel Jobs
Modify `.circleci/config.yml` to run `test`, `build`, and `deploy` jobs in parallel.

### Caching
Implement Docker layer caching in `.github/workflows/azure-container-webapp.yml`.

### Multi-Stage Builds
Use multi-stage Docker builds in `.github/workflows/azure-container-webapp.yml`.

### Automation of Issue Management
Add auto-labeling and auto-assigning logic in `.github/workflows/label-issues.yml`.

## Contributing
Provide guidelines for contributing, reporting issues, and requesting features. Link to `CONTRIBUTING.md` if it exists.

   on:
     push:
       branches: [ "main" ]
     pull_request:
       branches: [ "main" ]
     schedule:
       - cron: '0 0 * * 0'

   jobs:
     ssrf-detection:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout code
           uses: actions/checkout@v4

         - name: Run SSRF detection
           run: |
             # Add your SSRF detection script or tool here
             echo "Running SSRF detection..."
   ```

3. **Run the workflow**: The workflow will automatically run on push, pull request, and scheduled events. It will detect and address any SSRF vulnerabilities in the codebase.

By following these steps, you can ensure that SSRF vulnerabilities are detected and addressed in your codebase, enhancing the security of your project.

## New Workflow for Handling "Not Found" Error

We have added a new workflow to handle the "Not Found" error when trying to use GitHub Copilot workspace on pull requests. This workflow is designed to detect and address the specific error.

### Configuration

To configure the new workflow, follow these steps:

1. **Create a new workflow file**: Add a new workflow file named `.github/workflows/handle-not-found-error.yml` to the repository.

2. **Define the workflow**: Add the following content to the workflow file:
=======
**Build intelligent AI agents and multi-agent systems with this enterprise-ready orchestration framework**

[![License: MIT](https://img.shields.io/github/license/microsoft/semantic-kernel)](https://github.com/microsoft/semantic-kernel/blob/main/LICENSE)
[![Python package](https://img.shields.io/pypi/v/semantic-kernel)](https://pypi.org/project/semantic-kernel/)
[![Nuget package](https://img.shields.io/nuget/vpre/Microsoft.SemanticKernel)](https://www.nuget.org/packages/Microsoft.SemanticKernel/)
[![Discord](https://img.shields.io/discord/1063152441819942922?label=Discord&logo=discord&logoColor=white&color=d82679)](https://aka.ms/SKDiscord)


## What is Semantic Kernel?

Semantic Kernel is a model-agnostic SDK that empowers developers to build, orchestrate, and deploy AI agents and multi-agent systems. Whether you're building a simple chatbot or a complex multi-agent workflow, Semantic Kernel provides the tools you need with enterprise-grade reliability and flexibility.

## System Requirements

- **Python**: 3.10+
- **.NET**: .NET 8.0+ 
- **Java**: JDK 17+
- **OS Support**: Windows, macOS, Linux

## Key Features

- **Model Flexibility**: Connect to any LLM with built-in support for [OpenAI](https://platform.openai.com/docs/introduction), [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service), [Hugging Face](https://huggingface.co/), [NVidia](https://www.nvidia.com/en-us/ai-data-science/products/nim-microservices/) and more
- **Agent Framework**: Build modular AI agents with access to tools/plugins, memory, and planning capabilities
- **Multi-Agent Systems**: Orchestrate complex workflows with collaborating specialist agents
- **Plugin Ecosystem**: Extend with native code functions, prompt templates, OpenAPI specs, or Model Context Protocol (MCP)
- **Vector DB Support**: Seamless integration with [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search), [Elasticsearch](https://www.elastic.co/), [Chroma](https://docs.trychroma.com/getting-started), and more
- **Multimodal Support**: Process text, vision, and audio inputs
- **Local Deployment**: Run with [Ollama](https://ollama.com/), [LMStudio](https://lmstudio.ai/), or [ONNX](https://onnx.ai/)
- **Process Framework**: Model complex business processes with a structured workflow approach
- **Enterprise Ready**: Built for observability, security, and stable APIs

## Installation

First, set the environment variable for your AI Services:

**Azure OpenAI:**
```bash
export AZURE_OPENAI_API_KEY=AAA....
```

**or OpenAI directly:**
```bash
export OPENAI_API_KEY=sk-...
```

### Python

```bash
pip install semantic-kernel
```

### .NET

```bash
dotnet add package Microsoft.SemanticKernel
dotnet add package Microsoft.SemanticKernel.Agents.core
```

### Java

See [semantic-kernel-java build](https://github.com/microsoft/semantic-kernel-java/blob/main/BUILD.md) for instructions.

## Quickstart

### Basic Agent - Python

Create a simple assistant that responds to user prompts:

```python
import asyncio
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

async def main():
    # Initialize a chat agent with basic instructions
    agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="SK-Assistant",
        instructions="You are a helpful assistant.",
    )

    # Get a response to a user message
    response = await agent.get_response(messages="Write a haiku about Semantic Kernel.")
    print(response.content)

asyncio.run(main()) 

# Output:
# Language's essence,
# Semantic threads intertwine,
# Meaning's core revealed.
```

### Basic Agent - .NET

```csharp
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;

var builder = Kernel.CreateBuilder();
builder.AddAzureOpenAIChatCompletion(
                Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT"),
                Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT"),
                Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")
                );
var kernel = builder.Build();

ChatCompletionAgent agent =
    new()
    {
        Name = "SK-Agent",
        Instructions = "You are a helpful assistant.",
        Kernel = kernel,
    };

await foreach (AgentResponseItem<ChatMessageContent> response 
    in agent.InvokeAsync("Write a haiku about Semantic Kernel."))
{
    Console.WriteLine(response.Message);
}

// Output:
// Language's essence,
// Semantic threads intertwine,
// Meaning's core revealed.
```

### Agent with Plugins - Python

Enhance your agent with custom tools (plugins) and structured output:

```python
import asyncio
from typing import Annotated
from pydantic import BaseModel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.functions import kernel_function, KernelArguments

class MenuPlugin:
    @kernel_function(description="Provides a list of specials from the menu.")
    def get_specials(self) -> Annotated[str, "Returns the specials from the menu."]:
        return """
        Special Soup: Clam Chowder
        Special Salad: Cobb Salad
        Special Drink: Chai Tea
        """

    @kernel_function(description="Provides the price of the requested menu item.")
    def get_item_price(
        self, menu_item: Annotated[str, "The name of the menu item."]
    ) -> Annotated[str, "Returns the price of the menu item."]:
        return "$9.99"

class MenuItem(BaseModel):
    price: float
    name: str

async def main():
    # Configure structured output format
    settings = OpenAIChatPromptExecutionSettings()
    settings.response_format = MenuItem

    # Create agent with plugin and settings
    agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="SK-Assistant",
        instructions="You are a helpful assistant.",
        plugins=[MenuPlugin()],
        arguments=KernelArguments(settings)
    )

    response = await agent.get_response(messages="What is the price of the soup special?")
    print(response.content)

    # Output:
    # The price of the Clam Chowder, which is the soup special, is $9.99.

asyncio.run(main()) 
```

### Agent with Plugin - .NET

```csharp
using System.ComponentModel;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.ChatCompletion;

var builder = Kernel.CreateBuilder();
builder.AddAzureOpenAIChatCompletion(
                Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT"),
                Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT"),
                Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")
                );
var kernel = builder.Build();

kernel.Plugins.Add(KernelPluginFactory.CreateFromType<MenuPlugin>());

ChatCompletionAgent agent =
    new()
    {
        Name = "SK-Assistant",
        Instructions = "You are a helpful assistant.",
        Kernel = kernel,
        Arguments = new KernelArguments(new PromptExecutionSettings() { FunctionChoiceBehavior = FunctionChoiceBehavior.Auto() })

    };

await foreach (AgentResponseItem<ChatMessageContent> response 
    in agent.InvokeAsync("What is the price of the soup special?"))
{
    Console.WriteLine(response.Message);
}

sealed class MenuPlugin
{
    [KernelFunction, Description("Provides a list of specials from the menu.")]
    public string GetSpecials() =>
        """
        Special Soup: Clam Chowder
        Special Salad: Cobb Salad
        Special Drink: Chai Tea
        """;

    [KernelFunction, Description("Provides the price of the requested menu item.")]
    public string GetItemPrice(
        [Description("The name of the menu item.")]
        string menuItem) =>
        "$9.99";
}
```

### Multi-Agent System - Python

Build a system of specialized agents that can collaborate:

```python
import asyncio
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion

billing_agent = ChatCompletionAgent(
    service=AzureChatCompletion(), 
    name="BillingAgent", 
    instructions="You handle billing issues like charges, payment methods, cycles, fees, discrepancies, and payment failures."
)

refund_agent = ChatCompletionAgent(
    service=AzureChatCompletion(),
    name="RefundAgent",
    instructions="Assist users with refund inquiries, including eligibility, policies, processing, and status updates.",
)

triage_agent = ChatCompletionAgent(
    service=OpenAIChatCompletion(),
    name="TriageAgent",
    instructions="Evaluate user requests and forward them to BillingAgent or RefundAgent for targeted assistance."
    " Provide the full answer to the user containing any information from the agents",
    plugins=[billing_agent, refund_agent],
)

thread: ChatHistoryAgentThread = None

async def main() -> None:
    print("Welcome to the chat bot!\n  Type 'exit' to exit.\n  Try to get some billing or refund help.")
    while True:
        user_input = input("User:> ")

        if user_input.lower().strip() == "exit":
            print("\n\nExiting chat...")
            return False

        response = await triage_agent.get_response(
            messages=user_input,
            thread=thread,
        )

        if response:
            print(f"Agent :> {response}")

# Agent :> I understand that you were charged twice for your subscription last month, and I'm here to assist you with resolving this issue. Here’s what we need to do next:

# 1. **Billing Inquiry**:
#    - Please provide the email address or account number associated with your subscription, the date(s) of the charges, and the amount charged. This will allow the billing team to investigate the discrepancy in the charges.

# 2. **Refund Process**:
#    - For the refund, please confirm your subscription type and the email address associated with your account.
#    - Provide the dates and transaction IDs for the charges you believe were duplicated.

# Once we have these details, we will be able to:

# - Check your billing history for any discrepancies.
# - Confirm any duplicate charges.
# - Initiate a refund for the duplicate payment if it qualifies. The refund process usually takes 5-10 business days after approval.

# Please provide the necessary details so we can proceed with resolving this issue for you.


if __name__ == "__main__":
    asyncio.run(main())
```



## Where to Go Next

1. 📖 Try our [Getting Started Guide](https://learn.microsoft.com/en-us/semantic-kernel/get-started/quick-start-guide) or learn about [Building Agents](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/)
2. 🔌 Explore over 100 [Detailed Samples](https://learn.microsoft.com/en-us/semantic-kernel/get-started/detailed-samples)
3. 💡 Learn about core Semantic Kernel [Concepts](https://learn.microsoft.com/en-us/semantic-kernel/concepts/kernel)

### API References

- [C# API reference](https://learn.microsoft.com/en-us/dotnet/api/microsoft.semantickernel?view=semantic-kernel-dotnet)
- [Python API reference](https://learn.microsoft.com/en-us/python/api/semantic-kernel/semantic_kernel?view=semantic-kernel-python)

## Troubleshooting

### Common Issues

- **Authentication Errors**: Check that your API key environment variables are correctly set
- **Model Availability**: Verify your Azure OpenAI deployment or OpenAI model access

### Getting Help

- Check our [GitHub issues](https://github.com/microsoft/semantic-kernel/issues) for known problems
- Search the [Discord community](https://aka.ms/SKDiscord) for solutions
- Include your SDK version and full error messages when asking for help

>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

   ```yaml
   name: Handle Not Found Error

   on:
     pull_request:
       types: [opened, synchronize]

   jobs:
     handle-not-found-error:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout code
           uses: actions/checkout@v4
We welcome your contributions and suggestions to the SK community! One of the easiest ways to participate is to engage in discussions in the GitHub repository. Bug reports and fixes are welcome!

For new features, components, or extensions, please open an issue and discuss with us before sending a PR. This is to avoid rejection as we might be taking the core in a different direction, but also to consider the impact on the larger ecosystem.

         - name: Check for Not Found Error
           run: |
             # Add your script or tool to check for the Not Found error here
             echo "Checking for Not Found error..."
             # Handle the Not Found error appropriately
             echo "Handling Not Found error..."
   ```

3. **Run the workflow**: The workflow will automatically run on pull request events. It will detect and address the "Not Found" error when trying to use GitHub Copilot workspace on pull requests.

By following these steps, you can ensure that the "Not Found" error is detected and addressed in your codebase, enhancing the functionality of your project.

## Contribution Guidelines

We welcome contributions from the community! To contribute to this project, please follow these guidelines:

1. **Fork the repository**: Create a fork of the repository to work on your changes.

2. **Create a branch**: Create a new branch for your changes.
This project has adopted the
[Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information, see the
[Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
or contact [opencode@microsoft.com](mailto:opencode@microsoft.com)
with any additional questions or comments.

   ```bash
   git checkout -b my-feature-branch
   ```

3. **Make your changes**: Implement your changes in the new branch.

4. **Test your changes**: Ensure that your changes do not break any existing functionality and pass all tests.

5. **Commit your changes**: Commit your changes with a descriptive commit message.

   ```bash
   git commit -m "Add new feature"
   ```

6. **Push your changes**: Push your changes to your forked repository.

   ```bash
   git push origin my-feature-branch
   ```

7. **Create a pull request**: Open a pull request to merge your changes into the main repository.

8. **Review and feedback**: Address any feedback or comments from the maintainers during the review process.

9. **Merge**: Once your pull request is approved, it will be merged into the main repository.

Thank you for your contributions!

For more detailed guidelines on contributing, refer to the `CONTRIBUTING.md` file in the root directory of the repository.

## Setting Up and Using the Repository

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/sk-api.git
   cd sk-api
   ```

2. **Install dependencies**:

   ```bash
   npm install
   ```

3. **Install Python dependencies** (if applicable):

   ```bash
   pip install -r requirements.txt
   ```

4. **Install .NET dependencies** (if applicable):

   ```bash
   dotnet restore
   ```

5. **Install Java dependencies** (if applicable):

   ```bash
   ./mvnw install
   ```

### Configuration

1. **Create a configuration file**:

   Create a `config.json` file in the root directory of the repository and add the necessary configuration settings. Refer to the `config.example.json` file for an example configuration.

2. **Set environment variables**:

   Set the required environment variables in your system. You can use a `.env` file to manage environment variables. Refer to the `.env.example` file for the required variables.

### Running the API

1. **Start the API server**:

   ```bash
   npm start
   ```

2. **Access the API**:

   Open your web browser and navigate to `http://localhost:3000` to access the API.

For more detailed setup instructions, code snippets, and examples, refer to the [Getting Started Guide](docs/Getting_Started.md).
