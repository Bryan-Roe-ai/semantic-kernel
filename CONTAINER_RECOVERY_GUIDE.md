# Container Recovery Guide

## Issues Fixed

### 1. Missing Dockerfile
- **Problem**: The devcontainer configuration referenced a Dockerfile that didn't exist in the root directory
- **Solution**: Created `/workspaces/semantic-kernel/Dockerfile` with proper development environment setup

### 2. Devcontainer Configuration
- **Problem**: The devcontainer.json was using a pre-built image instead of building from our Dockerfile
- **Solution**: Updated `.devcontainer/devcontainer.json` to build from the new Dockerfile

### 3. Missing Dependencies
- **Problem**: Essential tools (.NET SDK, npm) were not available in the recovery container
- **Solution**: Created installation scripts and updated Dockerfile to include all necessary tools

### 4. Docker Build Context
- **Problem**: Docker compose referenced missing files and had unclear build context
- **Solution**: Added `.dockerignore` and `requirements.txt` to ensure clean builds

## Files Created/Modified

1. **`/workspaces/semantic-kernel/Dockerfile`** - Main development container definition
2. **`/workspaces/semantic-kernel/.dockerignore`** - Optimized build context
3. **`/workspaces/semantic-kernel/requirements.txt`** - Python dependencies
4. **`/workspaces/semantic-kernel/.devcontainer/devcontainer.json`** - Updated to use Dockerfile
5. **`/workspaces/semantic-kernel/health-check.sh`** - Container validation script
6. **`/workspaces/semantic-kernel/container-fix.sh`** - Quick fix script for recovery
7. **`/workspaces/semantic-kernel/entrypoint.sh`** - Container initialization script

## Next Steps

1. **Test the container**: Run `./health-check.sh` to verify all tools are working
2. **Reopen in Container**: Use VS Code's "Reopen in Container" command
3. **If issues persist**: Run `./container-fix.sh` in the recovery container

## Container Features

The new development container includes:
- ✅ .NET 8.0 SDK
- ✅ Python 3.12 with pip and poetry
- ✅ Node.js LTS with npm
- ✅ Azure Functions Core Tools
- ✅ MongoDB (for development)
- ✅ Git, curl, and essential development tools
- ✅ VS Code extensions for Semantic Kernel development

## Troubleshooting

If you encounter issues:

1. **Check health**: `./health-check.sh`
2. **Fix missing tools**: `./container-fix.sh`
3. **Rebuild container**: Delete container and rebuild
4. **Check logs**: Look at VS Code Developer Console for build errors

## Environment Variables

The container sets:
- `DOTNET_CLI_TELEMETRY_OPTOUT=1`
- `PYTHONUNBUFFERED=1`
- `PATH` includes .NET and Python tools

