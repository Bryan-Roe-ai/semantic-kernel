# 🤖 Semantic Kernel AI Workspace

**Organized for Maximum AI Development Productivity**

Welcome to your fully organized AI development workspace! This structure has been designed to streamline AI development workflows using Microsoft Semantic Kernel and related technologies.

## 🚀 Quick Start

```bash
# Navigate to the AI workspace
cd /workspaces/semantic-kernel/ai-workspace

# Launch the interactive workspace manager
./launch.sh

# Or setup the environment directly
python ai_workspace_manager.py --setup
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

## 🛠️ Development Environment

### Prerequisites

- Python 3.10+
- Node.js (for JavaScript components)
- Docker (for containerized services)
- VS Code (recommended IDE)

### Environment Setup

1. **Copy environment template:**

   ```bash
   cp .env.template .env
   ```

2. **Add your API keys to `.env`:**

   ```env
   OPENAI_API_KEY=your_key_here
   AZURE_OPENAI_API_KEY=your_azure_key_here
   AZURE_OPENAI_ENDPOINT=your_endpoint_here
   ```

3. **Install dependencies:**
   ```bash
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

```bash
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

```bash
./scripts/docker_manager.sh [command]
# Commands: build, compose, stop, logs, exec, health, cleanup, dev, deploy
```

For detailed Docker deployment instructions, see [DOCKER_GUIDE.md](DOCKER_GUIDE.md).
