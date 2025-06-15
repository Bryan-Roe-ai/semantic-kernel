# Repository Organization Index

Generated: 2025-06-15 22:45:17

## 🏗️ Repository Structure

### 01-core-implementations/
Language-specific implementations:
- `dotnet/` - .NET Semantic Kernel implementation
- `python/` - Python Semantic Kernel implementation  
- `java/` - Java Semantic Kernel implementation
- `typescript/` - TypeScript Semantic Kernel implementation

### 02-ai-workspace/
AI development workspace and tools:
- Organized AI development environment
- Sample applications and demos
- Model training and inference tools

### 03-development-tools/
Development utilities:
- `notebooks/` - Jupyter notebooks for experimentation
- `samples/` - Code samples and examples
- `tests/` - Test suites
- `plugins/` - Plugin development

### 04-infrastructure/
Build, deployment, and configuration:
- `scripts/` - Build and deployment scripts
- `.github/` - GitHub Actions workflows
- `config/` - Configuration files

### 05-documentation/
Documentation and guides:
- `docs/` - Main documentation (GitHub Pages)
- `docs-backup/` - Documentation backups
- `AgentDocs/` - Agent-specific documentation

### 06-deployment/
Deployment scripts and containers:
- Docker configurations
- Deployment scripts
- Azure Functions

### 07-resources/
Data, models, and static resources:
- `data/` - Training and test data
- `models/` - Model files
- `uploads/` - User uploads

### 08-archived-versions/
Archived versions and legacy code:
- Previous versions of the repository
- Legacy implementations
- Deprecated tools

## 🔗 Backward Compatibility

Symlinks have been created for all moved directories to maintain compatibility with existing scripts and workflows.

## 🧹 Cleanup

Temporary and duplicate files have been moved to `.cleanup/` for review:
- `.cleanup/duplicates/` - Duplicate files
- `.cleanup/temp/` - Temporary files  
- `.cleanup/system_files/` - System-generated files
- `.cleanup/temp_ids/` - Files with temporary IDs

## 🚀 Quick Start

1. **Core Development**: Start in `01-core-implementations/[language]/`
2. **AI Workspace**: Explore `02-ai-workspace/` for AI tools
3. **Documentation**: Visit `docs/` or the GitHub Pages site
4. **Scripts**: Use `04-infrastructure/scripts/` for automation

## 📞 Support

For questions about the organization or to restore files from `.cleanup/`, please refer to the cleanup logs or contact the maintainers.
