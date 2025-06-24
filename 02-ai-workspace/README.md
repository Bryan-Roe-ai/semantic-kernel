---
runme:
  id: 01JYHSCWR5BX8W9QTQ628N72DP
  version: v3
---

# 🤖 Semantic Kernel AI Workspace

**Advanced AI Development Platform with Comprehensive Automation**

Welcome to your fully organized AI development workspace! This structure has been designed to streamline AI development workflows using Microsoft Semantic Kernel, advanced automation tools, and comprehensive management systems.

✅ **Repository Status:** Cleaned, optimized, and deployed via GitHub Pages.

## 🌟 New Here? Start Your AI Journey!

**👋 Welcome, fellow AI enthusiast!** Whether you're just starting out or you're an experienced developer, this workspace is designed to make AI development exciting, accessible, and incredibly powerful.

### 🎯 Quick Start Options

**🌱 Complete Beginner?**

```bash {"id":"01JYHSCWR4YT6HTJTTQ1E9PWRG"}
# Start with our friendly getting started guide
cat GETTING_STARTED.md

# Take the interactive learning journey
python scripts/ai_learning_journey.py --beginner
```

**🚀 Want to See Something Cool?**

```bash {"id":"01JYHSCWR4YT6HTJTTQ1SQBEY1"}
# See the AI agents in action (2-minute demo)
python scripts/demo_showcase.py

# Watch the real-time dashboard
python scripts/friendly_dashboard.py
```

**🛠️ Ready to Build?**

```bash {"id":"01JYHSCWR4YT6HTJTTQ2TRFAY2"}
# Create your first AI project with guided help
python scripts/project_wizard.py

# Get friendly help anytime
python scripts/ai_helper.py
```

## 🚀 Quick Start

```bash {"id":"01JYHSCWR4YT6HTJTTQ5ZK7PRB"}
# Navigate to the AI workspace
cd /workspaces/semantic-kernel/ai-workspace

# Interactive Master Control (Recommended)
python ai_workspace_control.py --interactive

# Quick automated setup
python ai_workspace_control.py --batch batches/quick-setup.batch

# Traditional setup
./launch.sh
```

## 🎛️ Master Control System

The workspace includes a comprehensive **Master Control System** for managing all operations:

- **🔧 Workspace Optimizer**: Performance optimization and cleanup
- **📊 Real-time Monitor**: System monitoring with alerts
- **🚀 Deployment Automator**: Multi-environment deployment automation
- **🤖 AI Model Manager**: Complete model lifecycle management
- **🔗 MCP Integration**: Model Context Protocol for advanced tool interoperability
- **⚡ Batch Operations**: Automated workflow execution

### Interactive Dashboard

```bash {"id":"01JYHSCWR4YT6HTJTTQ9ZC6JAD"}
python ai_workspace_control.py --interactive
```

### Command Line Interface

```bash {"id":"01JYHSCWR4YT6HTJTTQB0Q1JAQ"}
# Optimize workspace
python ai_workspace_control.py --tool optimizer --command optimize

# Deploy to staging
python ai_workspace_control.py --tool deployment --command deploy --args --environment staging

# Manage models
python ai_workspace_control.py --tool model-manager --command list-models
```

## 📁 Organized Directory Structure

### 01-notebooks/

**Jupyter Notebooks & Interactive Development**

- Interactive AI experimentation
- Prototyping and testing
- Quick start notebook included
- Data exploration and visualization

### 02-agents/

**AI Agents & Multi-Agent Systems**

- Agent development frameworks
- Multi-agent collaboration examples
- Agent documentation and guides
- Chat launchers and interfaces

### 03-models-training/

**Model Training & Fine-tuning**

- Custom model training scripts
- Fine-tuning utilities for GPT and other models
- LLM training data collection
- Model evaluation tools

### 04-plugins/

**Semantic Kernel Plugins & Extensions**

- Custom SK plugins
- Prompt templates and samples
- Plugin development utilities
- Function calling examples

### 05-samples-demos/

**Sample Applications & Demonstrations**

- Complete example applications
- Demo projects and proof-of-concepts
- Web servers and APIs
- Integration examples

### 06-backend-services/

**Backend Services & APIs**

- Production-ready backend services
- Azure Functions implementations
- REST API endpoints
- Service orchestration
- Error handling and diagnostics

### 07-data-resources/

**Data, Datasets & Resources**

- Training datasets
- Data processing utilities
- Resource files and assets
- Upload and download directories

### 08-documentation/

**Documentation & Guides**

- Technical documentation
- API references
- Setup guides and tutorials
- Best practices and patterns

### 09-deployment/

**Deployment & Infrastructure**

- Docker configurations
- CI/CD pipelines
- Deployment scripts
- Infrastructure as Code

### 10-config/

**Configuration & Environment**

- Environment variables
- Configuration files
- Package dependencies
- Development settings

## � Advanced Features

### 🤖 AI Model Manager

Complete lifecycle management for AI models:

```bash {"id":"01JYHSCWR4YT6HTJTTQB75BRNC"}
# Download models from Hugging Face, URLs, or local files
python scripts/ai_model_manager.py download --source "microsoft/DialoGPT-medium"

# Optimize models (quantization, pruning, distillation)
python scripts/ai_model_manager.py optimize --model-id my_model --optimization quantization

# Benchmark performance
python scripts/ai_model_manager.py benchmark --model-id my_model

# Export/import models
python scripts/ai_model_manager.py export --model-id my_model --path model.zip
```

### 📊 Real-time Monitoring

Comprehensive system monitoring with alerting:

```bash {"id":"01JYHSCWR4YT6HTJTTQBNDMZFP"}
# Start real-time monitoring
python scripts/ai_workspace_monitor.py

# Generate reports
python scripts/ai_workspace_monitor.py --report 24
```

**Monitors**:

- System resources (CPU, Memory, Disk, GPU)
- API endpoint health
- Service availability
- Error rates and performance

### 🚀 Deployment Automation

Multi-environment deployment with rollback support:

```bash {"id":"01JYHSCWR4YT6HTJTTQD49S8GQ"}
# Deploy to production
python scripts/deployment_automator.py deploy --environment production --mode docker

# Deploy to Kubernetes
python scripts/deployment_automator.py deploy --environment staging --mode kubernetes

# Validate deployment
python scripts/deployment_automator.py validate
```

**Supported Platforms**:

- Docker & Docker Compose
- Kubernetes
- Azure (Container Instances, App Service)
- AWS (ECS, Lambda)

### 🔧 Workspace Optimizer

Automated optimization and cleanup:

```bash {"id":"01JYHSCWR4YT6HTJTTQGV0NDR9"}
# Full optimization
python scripts/ai_workspace_optimizer.py

# Quick cleanup
python scripts/ai_workspace_optimizer.py --quick
```

**Features**:

- Cleanup temporary files
- Disk usage analysis
- Cache optimization
- Model organization
- Performance reporting

### 🎯 Batch Operations

Automate complex workflows:

```bash {"id":"01JYHSCWR4YT6HTJTTQK6E50RH"}
# Quick setup and validation
python ai_workspace_control.py --batch batches/quick-setup.batch

# Full deployment workflow
python ai_workspace_control.py --batch batches/full-deployment.batch

# Regular maintenance
python ai_workspace_control.py --batch batches/maintenance.batch
```

### 🔗 MCP Integration

Advanced tool interoperability with Model Context Protocol:

- GitHub repository integration
- Tool discovery and execution
- Multi-agent coordination
- Real-time context sharing

__See__: [MCP_INTEGRATION_GUIDE.md](MCP_INTEGRATION_GUIDE.md) for detailed setup

## �🛠️ Development Environment

### Prerequisites

- Python 3.10+
- Node.js (for JavaScript components)
- Docker (for containerized services)
- VS Code (recommended IDE)

### Environment Setup

1. **Copy environment template:**

```bash {"id":"01JYHSCWR4YT6HTJTTQKW7DBE1"}
cp .env.template .env
```

2. **Add your API keys to `.env`:**

```env {"id":"01JYHSCWR4YT6HTJTTQNTX7VRP"}
OPENAI_API_KEY=your_key_here
AZURE_OPENAI_API_KEY=your_azure_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
```

3. **Install dependencies:**

```bash {"id":"01JYHSCWR4YT6HTJTTQNYMYZ2D"}
pip install -r requirements.txt
```

## 🚀 Getting Started Workflows

### For AI Research & Experimentation:

1. Start with `01-notebooks/quick-start.ipynb`
2. Explore examples in `01-notebooks/`
3. Use `03-models-training/` for custom models
4. Store data in `07-data-resources/`

### For Production AI Applications:

1. Review samples in `05-samples-demos/`
2. Develop services in `06-backend-services/`
3. Create plugins in `04-plugins/`
4. Deploy using `09-deployment/`

### For Agent Development:

1. Study examples in `02-agents/`
2. Build plugins in `04-plugins/`
3. Test in `01-notebooks/`
4. Deploy via `06-backend-services/`

## 🧰 Key Tools & Scripts

### Workspace Management

- `organize_files.py` - File organization script
- `ai_workspace_manager.py` - Workspace management utilities
- `launch.sh` - Interactive launcher and menu system

### Development Scripts

- `start_backend.py` - Launch backend services
- `start_chat_unified.py` - Start chat interface
- `diagnose_system.py` - System diagnostics
- `test_system.py` - System testing

### Training & ML

- `finetune_gpt2_custom.py` - GPT-2 fine-tuning
- `collect_llm_training_data.py` - Training data collection
- `simple_llm_demo.py` - LLM demonstration

## 🐳 Docker Deployment

### Quick Start with Docker

```bash {"id":"01JYHSCWR4YT6HTJTTQS02DRND"}
# One-command deployment
./scripts/docker_manager.sh deploy

# Or step by step
./scripts/cleanup_and_automate.sh --all  # Cleanup and prepare
./scripts/docker_manager.sh build        # Build image
./scripts/docker_manager.sh compose      # Start services
```

### Docker Services

- **Main Portal**: http://localhost (Nginx reverse proxy)
- **Jupyter Lab**: http://localhost:8888
- **Backend API**: http://localhost:8000
- **Web Interface**: http://localhost:3000
- **ChromaDB**: http://localhost:8001
- **Monitoring**: http://localhost:9090 (Prometheus)

### Management Commands

```bash {"id":"01JYHSCWR4YT6HTJTTQV65A33S"}
./scripts/docker_manager.sh [command]
# Commands: build, compose, stop, logs, exec, health, cleanup, dev, deploy
```

For detailed Docker deployment instructions, see [DOCKER_GUIDE.md](DOCKER_GUIDE.md).
