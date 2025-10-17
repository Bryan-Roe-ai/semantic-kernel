# Simple Chat App with Semantic Kernel

This is a simple console application that demonstrates how to chat with an LLM using Semantic Kernel.

## Features

- Interactive chat interface
- Support for multiple LLM providers:
  - OpenAI (GPT-4o-mini, GPT-4, etc.)
  - Azure OpenAI
  - Ollama (local, free)
- Maintains conversation history
- Streaming responses for better UX

## Quick Start

### Option 1: Use OpenAI (Easiest if you have an OpenAI API key)

1. **Get an OpenAI API key** from https://platform.openai.com/api-keys

2. **Set up your API key** using .NET Secret Manager:
   ```bash
   cd dotnet/samples/GettingStarted/SimpleChatApp
   dotnet user-secrets init
   dotnet user-secrets set "OpenAI:ApiKey" "your-api-key-here"
   dotnet user-secrets set "OpenAI:ChatModelId" "gpt-4o-mini"
   ```

3. **Run the app**:
   ```bash
   dotnet run
   ```

### Option 2: Use Azure OpenAI

1. **Get Azure OpenAI credentials** from your Azure Portal

2. **Set up your credentials**:
   ```bash
   cd dotnet/samples/GettingStarted/SimpleChatApp
   dotnet user-secrets init
   dotnet user-secrets set "AzureOpenAI:Endpoint" "https://your-endpoint.openai.azure.com"
   dotnet user-secrets set "AzureOpenAI:ApiKey" "your-api-key"
   dotnet user-secrets set "AzureOpenAI:ChatDeploymentName" "your-deployment-name"
   ```

3. **Run the app**:
   ```bash
   dotnet run
   ```

### Option 3: Use Ollama (Free, runs locally - no API key needed!)

1. **Install Ollama** from https://ollama.ai

2. **Pull a model** (this downloads the model to your computer):
   ```bash
   ollama pull llama3.2
   ```

3. **Make sure Ollama is running**:
   ```bash
   ollama serve
   ```

4. **Run the app** (no configuration needed, it will use Ollama by default if no API keys are set):
   ```bash
   cd dotnet/samples/GettingStarted/SimpleChatApp
   dotnet run
   ```

## Using Environment Variables Instead

If you prefer environment variables instead of Secret Manager:

**PowerShell:**
```powershell
# For OpenAI
$env:OpenAI__ApiKey = "your-api-key"
$env:OpenAI__ChatModelId = "gpt-4o-mini"

# For Azure OpenAI
$env:AzureOpenAI__Endpoint = "https://your-endpoint.openai.azure.com"
$env:AzureOpenAI__ApiKey = "your-api-key"
$env:AzureOpenAI__ChatDeploymentName = "your-deployment-name"

# For Ollama (optional, defaults shown)
$env:Ollama__Endpoint = "http://localhost:11434"
$env:Ollama__ModelId = "llama3.2"
```

**Bash:**
```bash
# For OpenAI
export OpenAI__ApiKey="your-api-key"
export OpenAI__ChatModelId="gpt-4o-mini"

# For Azure OpenAI
export AzureOpenAI__Endpoint="https://your-endpoint.openai.azure.com"
export AzureOpenAI__ApiKey="your-api-key"
export AzureOpenAI__ChatDeploymentName="your-deployment-name"

# For Ollama (optional, defaults shown)
export Ollama__Endpoint="http://localhost:11434"
export Ollama__ModelId="llama3.2"
```

## Usage

Once the app is running:

1. Type your message and press Enter
2. The AI will respond
3. Type 'exit' or 'quit' to end the conversation

Example conversation:
```
You: What is semantic kernel?
Assistant: Semantic Kernel is an open-source SDK developed by Microsoft that allows you to integrate 
large language models (LLMs) like GPT-4 with your applications...

You: exit
Goodbye!
```

## Troubleshooting

### "No configuration found" error
- Make sure you've set up at least one of the configuration options above
- Verify your secret keys or environment variables are set correctly
- Try restarting your terminal after setting environment variables

### Ollama connection error
- Make sure Ollama is running: `ollama serve`
- Verify the model is installed: `ollama list`
- If needed, pull the model: `ollama pull llama3.2`

### Azure OpenAI authentication error
- Verify your endpoint URL is correct (should end in `.openai.azure.com`)
- Check that your API key is valid
- Ensure your deployment name matches exactly

## Next Steps

Once you have this working, explore more Semantic Kernel features:
- Add plugins to give your AI access to functions
- Use prompt templates for consistent responses
- Implement RAG (Retrieval Augmented Generation) with vector stores
- Create agents that can plan and execute tasks

Check out the other samples in the `dotnet/samples` directory!
