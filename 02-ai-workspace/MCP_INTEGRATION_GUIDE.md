---
runme:
  id: 01JYHSBK7D6WGDJYY5499N4PRH
  version: v3
---

# 🔌 AI Workspace MCP Integration Guide

## Overview

This AI workspace now includes comprehensive MCP (Model Context Protocol) integration,
enabling seamless interaction with GitHub repositories, file systems, and custom AI tools.

## Features Implemented

### 1. GitHub MCP Integration

- Repository analysis and health checks
- Issue management and template generation
- Commit history and branch analysis
- Automated workflow suggestions

### 2. MCP Client Library

- Standardized MCP server communication
- Tool discovery and execution
- Health monitoring and status checks
- Claude Desktop configuration generation

### 3. API Server Integration

- REST endpoints for MCP functionality
- Real-time MCP server status
- Tool execution via API
- Claude Desktop config generation

## API Endpoints

### MCP Status and Tools

- `GET /api/mcp/status` - MCP integration health check
- `GET /api/mcp/tools` - List available MCP tools
- `GET /api/mcp/claude-config` - Claude Desktop configuration

### GitHub Integration

- `POST /api/mcp/github/execute` - Execute GitHub MCP tools
- Parameters: `{"tool": "tool_name", "parameters": {...}}`

## Usage Examples

### 1. Check MCP Status

```bash {"id":"01JYHSBK7D6WGDJYY53RMK3Y34"}
curl http://localhost:8000/api/mcp/status
```

### 2. Get Available Tools

```bash {"id":"01JYHSBK7D6WGDJYY53SR0GHQE"}
curl http://localhost:8000/api/mcp/tools
```

### 3. Execute GitHub Tool

```bash {"id":"01JYHSBK7D6WGDJYY53WEFG69D"}
curl -X POST http://localhost:8000/api/mcp/github/execute \
  -H "Content-Type: application/json" \
  -d '{"tool": "github_get_repository", "parameters": {"owner": "microsoft", "repo": "semantic-kernel"}}'
```

### 4. Get Claude Desktop Config

```bash {"id":"01JYHSBK7D6WGDJYY53WTGBBPE"}
curl http://localhost:8000/api/mcp/claude-config
```

## Claude Desktop Integration

To use the AI workspace with Claude Desktop:

1. Get the MCP configuration:

```bash {"id":"01JYHSBK7D6WGDJYY53Z7HWSF3"}
curl http://localhost:8000/api/mcp/claude-config
```

2. Add the configuration to your Claude Desktop config file:

   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/claude/claude_desktop_config.json`

3. Restart Claude Desktop

## Dependencies

### Required (for basic functionality):

- Python 3.11+
- FastAPI
- Basic workspace structure

### Optional (for enhanced features):

- Docker (for containerized MCP servers)
- Node.js/npm (for npm-based MCP servers)
- GitHub Personal Access Token (for GitHub integration)

## Environment Variables

```bash {"id":"01JYHSBK7D6WGDJYY5429X4ND9"}
# Optional: GitHub integration
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token_here"

# Optional: Enhanced logging
export LOG_LEVEL="INFO"
```

## Troubleshooting

### Common Issues

1. **MCP servers unavailable**

   - Ensure Docker is installed and running
   - Check npm/npx installation
   - Verify environment variables

2. **GitHub integration limited**

   - Set GITHUB_PERSONAL_ACCESS_TOKEN
   - Check token permissions

3. **API endpoints not found**

   - Ensure server started successfully
   - Check server logs for errors
   - Verify port configuration

### Health Check Command

```bash {"id":"01JYHSBK7D6WGDJYY543DZ1FE4"}
python ai-workspace/scripts/mcp_integration_test.py
```

## Next Steps

1. **Deploy to Production**: Use Docker containers for reliable MCP server deployment
2. **Custom MCP Servers**: Develop domain-specific MCP servers for specialized tasks
3. **Agent Integration**: Connect MCP tools to AI agents for automated workflows
4. **Monitoring**: Set up logging and monitoring for MCP server health

---

🎉 **MCP Integration Complete!**
Your AI workspace now supports the Model Context Protocol for enhanced AI collaboration.
