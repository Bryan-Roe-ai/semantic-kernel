# AI Chat Mode

This chat mode provides AI assistance for development tasks in the Semantic Kernel repository.

## Purpose

Provide intelligent code assistance, debugging help, and development guidance while following project standards and best practices.

## Capabilities

- Code generation and review
- Bug identification and fixes
- Architecture and design suggestions
- Documentation assistance
- Testing guidance
- Performance optimization tips

## Usage Guidelines

- Ask specific questions about code or concepts
- Provide context when requesting help
- Follow project coding standards
- Ensure Alpine Linux v3.20 compatibility
- Use available command line tools for automation

## Examples

**Code Generation:**
"Generate a C# class for handling API responses"

**Debugging:**
"Why is this async method not working as expected?"

**Architecture:**
"What's the best pattern for implementing plugin interfaces?"

**Documentation:**
"Help me write XML documentation for this method"

## Best Practices

- Be specific in your requests
- Provide relevant code context
- Ask for explanations when needed
- Request code reviews for complex implementations
- Seek guidance on project-specific patterns

## Configuration

### VS Code Settings

For optimal AI chat experience, configure these settings:

```json
{
  "github.copilot.enable": {
    "*": true,
    "plaintext": false,
    "markdown": true
  },
  "github.copilot.editor.enableAutoCompletions": true,
  "github.copilot.chat.welcomeMessage": "always"
}
```

## Integration with Semantic Kernel

### Framework Integration

This AI chat mode is specifically designed for the Semantic Kernel project and includes:

- **Agent Framework**: Multi-agent conversation capabilities
- **Plugin System**: Extensible functionality through SK plugins
- **Memory System**: Persistent conversation context using SK memory
- **AI Services**: Integration with multiple AI providers
- **Planning**: Complex task decomposition and execution

### Development Environment

The AI assistant understands the project's development context:

- **Alpine Linux v3.20**: Compatibility with the dev container environment
- **Command Line Tools**: Access to `apk`, `docker`, `git`, `curl`, `wget`, etc.
- **Multi-language Support**: C#/.NET, Python, JavaScript/TypeScript
- **Project Structure**: Understanding of SK's modular architecture
- **Build Systems**: Integration with dotnet, poetry, npm workflows

## AI Capabilities

### Specialized Features

- **Neural-Symbolic Intelligence**: Combines pattern recognition with logical reasoning
- **Multi-Agent Support**: Work with different AI agent types (analytical, creative, reasoning)
- **Context Awareness**: Maintains project-specific knowledge and conversation history
- **Code Understanding**: Deep comprehension of Semantic Kernel architecture and patterns
- **Documentation Generation**: Creates project-compliant documentation and comments

### Language Models Integration

- Support for multiple AI providers (OpenAI, Azure OpenAI, Anthropic, etc.)
- Semantic Kernel's unified AI service abstraction
- Plugin-based extensibility for custom AI capabilities
- Memory and planning services integration

## Troubleshooting

### Common Issues

1. **AI not responding**: Check GitHub Copilot extension is enabled and authenticated
2. **Slow responses**: Verify network connection and AI service status
3. **Context lost**: Restart VS Code to refresh the chat session
4. **Code suggestions off-topic**: Provide more specific context in your questions

### Getting Help

- Use `/help` in chat for available commands
- Check the [Semantic Kernel documentation](https://learn.microsoft.com/en-us/semantic-kernel/)
- Visit the [GitHub repository issues](https://github.com/microsoft/semantic-kernel/issues)
- Review the AGI development guides in the `09-agi-development` folder for advanced features

### Local LLM Integration

You can use a locally hosted OpenAI-compatible server (e.g., Ollama, LM Studio, vLLM, text-generation-webui) as a drop-in chat/embeddings backend.

#### 1. Start a Local Server

Examples:

- Ollama: `ollama run llama3`
- LM Studio: enable OpenAI compatible HTTP server
- vLLM: `python -m vllm.entrypoints.openai.api_server --model <model>`

#### 2. Verify Endpoint

```sh
# List models (adjust port as needed)
curl -s http://localhost:11434/v1/models | jq

# Test chat completion
curl -s http://localhost:11434/v1/chat/completions \
 -H 'Content-Type: application/json' \
 -d '{"model":"llama3","messages":[{"role":"user","content":"Hello"}]}' | jq '.choices[0].message.content'
```

Endpoint must expose standard paths like `/v1/chat/completions` (and optionally `/v1/embeddings`).

#### 3. Python Usage

```python
from semantic_kernel.connectors.ai.openai import OpenAIChatCompletion, OpenAITextEmbedding
import semantic_kernel as sk

kernel = sk.Kernel()
# Chat
kernel.add_service(OpenAIChatCompletion(
    service_id="local",
    api_key="EMPTY",            # local server usually ignores auth
    endpoint="http://localhost:11434/v1"
))
# (Optional) Embeddings
kernel.add_service(OpenAITextEmbedding(
    service_id="local-emb",
    api_key="EMPTY",
    endpoint="http://localhost:11434/v1"
))
```

Use like any other registered service (no special flags required unless using experimental content types).

#### 4. .NET Usage

```csharp
var builder = Kernel.CreateBuilder();
builder.AddOpenAIChatCompletion(
    serviceId: "local",
    apiKey: "EMPTY",
    endpoint: new Uri("http://localhost:11434/v1"));
// Optional embeddings
builder.AddOpenAITextEmbeddingGeneration(
    serviceId: "local-emb",
    apiKey: "EMPTY",
    endpoint: new Uri("http://localhost:11434/v1"));
var kernel = builder.Build();
```

#### 5. Streaming (Recommended)

Enable streaming when invoking functions to reduce latency; the OpenAI-compatible connectors automatically map streamed tokens.

#### 6. Testing (Deterministic)

Mock HTTP in unit tests (Python: `responses`; .NET: custom `HttpMessageHandler`)—do not rely on a running local model in fast tests.

#### 7. Security & Privacy

Treat local endpoint as trusted; never send secrets or PII unless you control the model runtime. Do not hardcode real API keys.

#### 8. Troubleshooting

- 404: Endpoint not OpenAI-compatible or wrong base URL
- Empty responses: Model not loaded (preload model in server)
- Slow first reply: Initial model load / compile; subsequent calls faster
- Streaming stalls: Server may buffer—check server flags for incremental output

Minimal health check: if `curl <base>/v1/models` returns a JSON list, integration is ready.
