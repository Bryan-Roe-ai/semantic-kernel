# Semantic Kernel Concepts by Feature

This section contains code snippets that demonstrate the usage of Semantic Kernel features.

| Features | Description |
| -------- | ----------- |
| Agents | Creating and using [agents](../../semantic_kernel/agents/) in Semantic Kernel |
| Audio | Using services that support audio-to-text and text-to-audio conversion |
| AutoFunctionCalling | Using `Auto Function Calling` to allow function call capable models to invoke Kernel Functions automatically |
| ChatCompletion | Using [`ChatCompletion`](https://github.com/microsoft/semantic-kernel/blob/main/python/semantic_kernel/connectors/ai/chat_completion_client_base.py) messaging capable service with models  |
| ChatHistory | Using and serializing the [`ChatHistory`](https://github.com/microsoft/semantic-kernel/blob/main/python/semantic_kernel/contents/chat_history.py) |
| Filtering | Creating and using Filters |
| Functions | Invoking [`Method`](https://github.com/microsoft/semantic-kernel/blob/main/python/semantic_kernel/functions/kernel_function_from_method.py) or [`Prompt`](https://github.com/microsoft/semantic-kernel/blob/main/python/semantic_kernel/functions/kernel_function_from_prompt.py) functions with [`Kernel`](https://github.com/microsoft/semantic-kernel/blob/main/python/semantic_kernel/kernel.py) |
| Grounding | An example of how to perform LLM grounding |
| Local Models | Using the [`OpenAI connector`](https://github.com/microsoft/semantic-kernel/blob/main/python/semantic_kernel/connectors/ai/open_ai/services/open_ai_chat_completion.py) and [`OnnxGenAI connector`](https://github.com/microsoft/semantic-kernel/blob/main/python/semantic_kernel/connectors/ai/onnx/services/onnx_gen_ai_chat_completion.py) to talk to models hosted locally in Ollama, OnnxGenAI and LM Studio |
| Logging | Showing how to set up logging |
| Memory | Using [`Memory`](https://github.com/microsoft/semantic-kernel/tree/main/dotnet/src/SemanticKernel.Abstractions/Memory) AI concepts |
| Model-as-a-Service | Using models deployed as [`serverless APIs on Azure AI Studio`](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/deploy-models-serverless?tabs=azure-ai-studio) to benchmark model performance against open-source datasets |
| On Your Data | Examples of using AzureOpenAI [`On Your Data`](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/use-your-data?tabs=mongo-db) |
| Planners | Showing the uses of [`Planners`](https://github.com/microsoft/semantic-kernel/tree/main/python/semantic_kernel/planners) |
| Plugins | Different ways of creating and using [`Plugins`](https://github.com/microsoft/semantic-kernel/blob/main/python/semantic_kernel/functions/kernel_plugin.py) |
| PromptTemplates | Using [`Templates`](https://github.com/microsoft/semantic-kernel/blob/main/python/semantic_kernel/prompt_template/prompt_template_base.py) with parametrization for `Prompt` rendering  |
| RAG | Different ways of `RAG` (Retrieval-Augmented Generation) |
| Search | Using search services information |
| Service Selector | Shows how to create and use a custom service selector class. |
| Setup | How to setup environment variables for Semantic Kernel |
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
| Structured Output | How to leverage OpenAI's json_schema structured output functionality. |
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
| Structured Output | How to leverage OpenAI's json_schema structured output functionality. |
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
| Structured Output | How to leverage OpenAI's json_schema structured output functionality. |
>>>>>>> main
>>>>>>> Stashed changes
=======
=======
| Structured Output | How to leverage OpenAI's json_schema structured output functionality. |
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
| TextGeneration | Using [`TextGeneration`](https://github.com/microsoft/semantic-kernel/blob/main/python/semantic_kernel/connectors/ai/text_completion_client_base.py) capable service with models  |

# Configuring the Kernel

In Semantic Kernel for Python, we leverage Pydantic Settings to manage configurations for AI and Memory Connectors, among other components. Here’s a clear guide on how to configure your settings effectively:

## Steps for Configuration

1. **Reading Environment Variables:**
   - **Primary Source:** Pydantic first attempts to read the required settings from environment variables.
   
2. **Using a .env File:**
   - **Fallback Source:** If the required environment variables are not set, Pydantic will look for a `.env` file in the current working directory.
   - **Custom Path (Optional):** You can specify an alternative path for the `.env` file via `env_file_path`. This can be either a relative or an absolute path.

3. **Direct Constructor Input:**
   - As an alternative to environment variables and `.env` files, you can pass the required settings directly through the constructor of the AI Connector or Memory Connector.

<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
>>>>>>> head
## Microsoft Entra Token Authentication

To authenticate to your Azure resources using a Microsoft Entra Authentication Token, the `AzureChatCompletion` AI Service connector now supports this as a built-in feature. If you do not provide an API key -- either through an environment variable, a `.env` file, or the constructor -- and you also do not provide a custom `AsyncAzureOpenAI` client, an `ad_token`, or an `ad_token_provider`, the `AzureChatCompletion` connector will attempt to retrieve a token using the [`DefaultAzureCredential`](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python).

To successfully retrieve and use the Entra Auth Token, you need the `Cognitive Services OpenAI Contributor` role assigned to your Azure OpenAI resource. By default, the `https://cognitiveservices.azure.com` token endpoint is used. You can override this endpoint by setting an environment variable `.env` variable as `AZURE_OPENAI_TOKEN_ENDPOINT` or by passing a new value to the `AzureChatCompletion` constructor as part of the `AzureOpenAISettings`.

<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< HEAD
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
## Best Practices

- **.env File Placement:** We highly recommend placing the `.env` file in the `semantic-kernel/python` root directory. This is a common practice when developing in the Semantic Kernel repository.

By following these guidelines, you can ensure that your settings for various components are configured correctly, enabling seamless functionality and integration of Semantic Kernel in your Python projects.