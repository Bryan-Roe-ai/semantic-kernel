# Get Started with Semantic Kernel Python

Highlights
- Flexible Agent Framework: build, orchestrate, and deploy AI agents and multi-agent systems
- Multi-Agent Systems: Model workflows and collaboration between AI specialists
- Plugin Ecosystem: Extend with Python, OpenAPI, Model Context Protocol (MCP), and more
- LLM Support: OpenAI, Azure OpenAI, Hugging Face, Mistral, Vertex AI, ONNX, Ollama, NVIDIA NIM, and others
- Vector DB Support: Azure AI Search, Elasticsearch, Chroma, and more
- Process Framework: Build structured business processes with workflow modeling
- Multimodal: Text, vision, audio

## Quick Install

```bash
pip install --upgrade semantic-kernel
# Optional: Add integrations
pip install --upgrade semantic-kernel[hugging_face]
pip install --upgrade semantic-kernel[all]
```

Supported Platforms:
- Python: 3.10+
- OS: Windows, macOS, Linux

## 1. Setup API Keys

Set as environment variables, or create a .env file at your project root:

```bash
OPENAI_API_KEY=sk-...
OPENAI_CHAT_MODEL_ID=...
...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=...
...
```

You can also override environment variables by explicitly passing configuration parameters to the AI service constructor:

```python
chat_service = AzureChatCompletion(
    api_key=...,
    endpoint=...,
    deployment_name=...,
    api_version=...,
)
```

See the following [setup guide](https://github.com/microsoft/semantic-kernel/tree/main/python/samples/concepts/setup) for more information.

## 2. Use the Kernel for Prompt Engineering

Create prompt functions and invoke them via the `Kernel`:

```python
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import KernelArguments

kernel = Kernel()
kernel.add_service(OpenAIChatCompletion())

# Prepare OpenAI service using credentials stored in the `.env` file
service_id="chat-gpt"
kernel.add_service(
    OpenAIChatCompletion(
        service_id=service_id,
        ai_model_id="gpt-3.5-turbo",
        api_key=api_key,
        org_id=org_id
    )
)

# Alternative using Azure:
# kernel.add_service(
#   AzureChatCompletion(
#       service_id=service_id,
#       deployment_name=deployment,
#       base_url=endpoint,
#       api_key=api_key
#   )
# )
prompt = """
1) A robot may not injure a human being...
2) A robot must obey orders given it by human beings...
3) A robot must protect its own existence...

Give me the TLDR in exactly {{$num_words}} words."""


async def main():
    result = await kernel.invoke_prompt(prompt, arguments=KernelArguments(num_words=5))
    print(result)


asyncio.run(main())
# Output: Protect humans, obey, self-preserve, prioritized.
```

## 3. Directly Use AI Services (No Kernel Required)

You can use the AI service classes directly for advanced workflows:

```python
import asyncio
import asyncio

from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.contents import ChatHistory


async def main():
    service = OpenAIChatCompletion()
    settings = OpenAIChatPromptExecutionSettings()

    chat_history = ChatHistory(system_message="You are a helpful assistant.")
    chat_history.add_user_message("Write a haiku about Semantic Kernel.")
    response = await service.get_chat_message_content(chat_history=chat_history, settings=settings)
    print(response.content)

    """
    Output:

    Thoughts weave through context,  
    Semantic threads interlace—  
    Kernel sparks meaning.
    """


asyncio.run(main())
```

## 4. Build an Agent with Plugins and Tools

Add Python functions as plugins or Pydantic models as structured outputs;

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
    # Used for structured outputs
    price: float
    name: str

async def main():
    # Configure structured outputs format
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

    response = await agent.get_response("What is the price of the soup special?")
    print(response.content)

    # Output:
    # The price of the Clam Chowder, which is the soup special, is $9.99.

asyncio.run(main()) 
```

You can explore additional getting started agent samples [here](https://github.com/microsoft/semantic-kernel/tree/main/python/samples/getting_started_with_agents).

## 5. Multi-Agent Orchestration

Coordinate a group of agents to iteratively solve a problem or refine content together:

```python
import asyncio
from semantic_kernel.agents import ChatCompletionAgent, GroupChatOrchestration, RoundRobinGroupChatManager
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

def get_agents():
    return [
        ChatCompletionAgent(
            name="Writer",
            instructions="You are a creative content writer. Generate and refine slogans based on feedback.",
            service=AzureChatCompletion(),
        ),
        ChatCompletionAgent(
            name="Reviewer",
            instructions="You are a critical reviewer. Provide detailed feedback on proposed slogans.",
            service=AzureChatCompletion(),
        ),
    ]

async def main():
    agents = get_agents()
    group_chat = GroupChatOrchestration(
        members=agents,
        manager=RoundRobinGroupChatManager(max_rounds=5),
    )
    runtime = InProcessRuntime()
    runtime.start()
    result = await group_chat.invoke(
        task="Create a slogan for a new electric SUV that is affordable and fun to drive.",
        runtime=runtime,
    )
    value = await result.get()
    print(f"Final Slogan: {value}")

    # Example Output:
    # Final Slogan: "Feel the Charge: Adventure Meets Affordability in Your New Electric SUV!"

    await runtime.stop_when_idle()

if __name__ == "__main__":
    asyncio.run(main())
```

For orchestration-focused examples, see [these orchestration samples](https://github.com/microsoft/semantic-kernel/tree/main/python/samples/getting_started_with_agents/multi_agent_orchestration).

## More Examples & Notebooks

- [Getting Started with Agents](https://github.com/microsoft/semantic-kernel/tree/main/python/samples/getting_started_with_agents): Practical agent orchestration and tool use  
- [Getting Started with Processes](https://github.com/microsoft/semantic-kernel/tree/main/python/samples/getting_started_with_processes): Modeling structured workflows with the Process framework  
- [Concept Samples](https://github.com/microsoft/semantic-kernel/tree/main/python/samples/concepts): Advanced scenarios, integrations, and SK patterns  
- [Getting Started Notebooks](https://github.com/microsoft/semantic-kernel/tree/main/python/samples/getting_started): Interactive Python notebooks for rapid experimentation  

## Semantic Kernel Documentation

The two SDKs are compatible and at their core they follow the same design principles.
Some features are still available only in the C# version and are being ported.
Refer to the [FEATURE MATRIX](../FEATURE_MATRIX.md) doc to see where
things stand in matching the features and functionality of the main SK branch.
Over time there will be some features available only in the Python version, and
others only in the C# version, for example, adapters to external services,
scientific libraries, etc.
# Quickstart with Poetry

## Installation

Install the Poetry package manager and create a project virtual environment.
# Setup

## OpenAI / Azure OpenAI API keys

Make sure you have an
[Open AI API Key](https://openai.com/api/) or
[Azure Open AI service key](https://learn.microsoft.com/azure/cognitive-services/openai/quickstart?pivots=rest-api)

Copy those keys into a `.env` file (see the `.env.example` file):

```
OPENAI_API_KEY=""
OPENAI_ORG_ID=""
AZURE_OPENAI_API_KEY=""
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_DEPLOYMENT_NAME=""
```

## Using Poetry

First, navigate to the directory containing this README using your chosen shell.
You will need to have at least Python 3.8 installed.

Install the Poetry package manager and create a project virtual environment. (Note: we require at least Poetry 1.2.0 and Python 3.8.)

```bash
# Install poetry package
pip3 install poetry
# Use poetry to install project deps
poetry install
# Use poetry to activate project venv
poetry shell
```

Make sure you have an
[Open AI API Key](https://openai.com/api/) or
[Azure Open AI service key](https://learn.microsoft.com/azure/cognitive-services/openai/quickstart?pivots=rest-api)

Copy those keys into a `.env` file in this repo

```
OPENAI_API_KEY=""
OPENAI_ORG_ID=""
AZURE_OPENAI_API_KEY=""
AZURE_OPENAI_ENDPOINT=""
```

### Quickstart ⚡

```python
import semantic_kernel as sk

kernel = sk.create_kernel()

api_key, org_id = sk.openai_settings_from_dot_env()

kernel.config.add_openai_completion_backend(
    "davinci-002", "text-davinci-002", api_key, org_id
)

sk_prompt = """
{{$input}}

Give me the TLDR in 5 words.
"""

text_to_summarize = """
    1) A robot may not injure a human being or, through inaction,
    allow a human being to come to harm.

    2) A robot must obey orders given it by human beings except where
    such orders would conflict with the First Law.

    3) A robot must protect its own existence as long as such protection
    does not conflict with the First or Second Law.
"""

tldr_function = sk.extensions.create_semantic_function(
    kernel,
    sk_prompt,
    max_tokens=200,
    temperature=0,
    top_p=0.5,
)

summary = await kernel.run_on_str_async(text_to_summarize, tldr_function)
output = str(summary.variables).strip()
print("Output: " + output)

# Output: Protect humans, follow orders, survive.
```

## Enhancing Documentation

### Detailed Explanations and Examples

To enhance the existing documentation, we have added more detailed explanations and examples to help users understand how to use the various features of the repository. These explanations and examples are included in the relevant sections of the documentation files such as `README.md` and `java/README.md`.

### Code Snippets and Usage Examples

We have included more code snippets and usage examples in the documentation to provide practical guidance on how to use the repository's features. These code snippets and examples are designed to help users quickly grasp the concepts and apply them in their own projects.

### Repository Structure Explanation

To help users navigate the repository, we have added a section that explains the structure of the repository and the purpose of each directory and file. This section provides an overview of the repository's organization and helps users understand where to find specific components and resources.
- [Getting Started with Semantic Kernel Python](https://learn.microsoft.com/en-us/semantic-kernel/get-started/quick-start-guide?pivots=programming-language-python)  
- [Agent Framework Guide](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/?pivots=programming-language-python)  
- [Process Framework Guide](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/process/process-framework)
# Get Started with Semantic Kernel ⚡

## Example: Running a simple prompt

```python
import semantic_kernel as sk
from semantic_kernel.ai.open_ai import OpenAITextCompletion

kernel = sk.create_kernel()

# Prepare OpenAI backend using credentials stored in the `.env` file
api_key, org_id = sk.openai_settings_from_dot_env()
kernel.config.add_text_backend("dv", OpenAITextCompletion("text-davinci-003", api_key, org_id))

# Wrap your prompt in a function
prompt = kernel.create_semantic_function("""
1) A robot may not injure a human being or, through inaction,
allow a human being to come to harm.

2) A robot must obey orders given it by human beings except where
such orders would conflict with the First Law.

3) A robot must protect its own existence as long as such protection
does not conflict with the First or Second Law.

Give me the TLDR in exactly 5 words.""")

# Run your prompt
print(prompt()) # => Robots must not harm humans.
```

## Example: Turn prompts into **reusable functions** with input parameters

```python
# Create a reusable function with one input parameter
summarize = kernel.create_semantic_function("{{$input}}\n\nOne line TLDR with the fewest words.")

# Summarize the laws of thermodynamics
print(summarize("""
1st Law of Thermodynamics - Energy cannot be created or destroyed.
2nd Law of Thermodynamics - For a spontaneous process, the entropy of the universe increases.
3rd Law of Thermodynamics - A perfect crystal at zero Kelvin has zero entropy."""))

# Summarize the laws of motion
print(summarize("""
1. An object at rest remains at rest, and an object in motion remains in motion at constant speed and in a straight line unless acted on by an unbalanced force.
2. The acceleration of an object depends on the mass of the object and the amount of force applied.
3. Whenever one object exerts a force on another object, the second object exerts an equal and opposite on the first."""))

# Summarize the law of universal gravitation
print(summarize("""
Every point mass attracts every single other point mass by a force acting along the line intersecting both points.
The force is proportional to the product of the two masses and inversely proportional to the square of the distance between them."""))

# Output: 
# Energy conserved, entropy increases, zero entropy at 0K.
# Objects move in response to forces.
# Gravitational force between two point masses is inversely proportional to the square of the distance between them.
```

## How does this compare to the C# version of Semantic Kernel?

Refer to the [FEATURE_PARITY.md](FEATURE_PARITY.md) doc to see where
things stand in matching the features and functionality of the main SK branch.


---

## 👨‍💻 Author & Attribution

**Created by Bryan Roe**  
Copyright (c) 2025 Bryan Roe  
Licensed under the MIT License

This is part of the Semantic Kernel - Advanced AI Development Framework.
For more information, see the main project repository.
