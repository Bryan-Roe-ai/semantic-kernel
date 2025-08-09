# Multi-Agent Sample Workspace

This sample shows a minimal, parallel Python + .NET layout for building an "AgentCore" library in both ecosystems. It is intentionally tiny so you can expand rapidly.

## Structure

```
multi_agent_sample/
  python/
    pyproject.toml
    src/agent_core/
      __init__.py
      agent.py
      config.py
    tests/test_agent.py
  dotnet/
    AgentCore/
      AgentCore.csproj
      Agent.cs
    AgentCore.Tests/
      AgentCore.Tests.csproj
      AgentTests.cs
  .editorconfig
  .gitignore
  LICENSE
```

## Concept

Both implementations expose a simple Agent abstraction with:

- name (identifier)
- send_message operation (echo for now)
- basic configuration object / options

## Python Quick Start

```
cd multi_agent_sample/python
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest -q
python -c "from agent_core import Agent; print(Agent(name='PyAgent').send_message('hi'))"
```

## .NET Quick Start

```
cd multi_agent_sample/dotnet
dotnet build
dotnet test
dotnet repl # (optional if installed)
```

## CI

The workflow `.github/workflows/ci.yml` runs Python (3.11) tests and .NET (net8.0) tests.

## Extending

Add real model / connector code behind `Agent.send_message` and mirror semantics across languages. For more advanced features (streaming, memory, planning) follow patterns from the main Semantic Kernel repository.

## License

MIT (see LICENSE).
