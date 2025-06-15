# 🤖 AI Workspace Advanced Features Guide

## 🚀 Master Control System

The AI Workspace now includes a comprehensive master control system for managing all operations from a single interface.

### Quick Start

```bash
# Interactive mode - recommended for beginners
python ai_workspace_control.py --interactive

# Run specific commands
python ai_workspace_control.py --tool optimizer --command optimize
python ai_workspace_control.py --tool model-manager --command list-models

# Run batch operations
python ai_workspace_control.py --batch batches/quick-setup.batch
```

## 🛠️ Advanced Tools

### 1. AI Workspace Optimizer (`scripts/ai_workspace_optimizer.py`)

**Purpose**: Optimize workspace performance and clean up files

**Features**:
- Clean temporary files and caches
- Analyze disk usage by directory
- Optimize cache directories
- Organize model files with indexing
- Generate structure and metrics reports
- Update configuration files
- Comprehensive health checks

**Usage**:
```bash
# Full optimization
python scripts/ai_workspace_optimizer.py

# Quick optimization
python scripts/ai_workspace_optimizer.py --quick

# Via master control
python ai_workspace_control.py --tool optimizer --command optimize
```

### 2. Real-time Monitor (`scripts/ai_workspace_monitor.py`)

**Purpose**: Real-time monitoring and alerting for the AI workspace

**Features**:
- System resource monitoring (CPU, memory, disk, GPU)
- Service health monitoring
- API endpoint monitoring
- Alert system with configurable thresholds
- Metrics history and reporting
- Docker container monitoring

**Usage**:
```bash
# Start monitoring (interactive)
python scripts/ai_workspace_monitor.py

# Generate 24-hour report
python scripts/ai_workspace_monitor.py --report 24

# Custom monitoring interval
python scripts/ai_workspace_monitor.py --interval 60
```

**Monitoring Thresholds**:
- CPU: 80%
- Memory: 85%
- Disk: 90%
- GPU Memory: 95%
- API Response Time: 5 seconds

### 3. Deployment Automator (`scripts/deployment_automator.py`)

**Purpose**: Automated deployment to various environments

**Features**:
- Multi-environment support (development, staging, production)
- Multiple deployment modes (Docker, Kubernetes, Azure, AWS)
- Pre/post-deployment validation
- Automatic backup creation
- Rollback on failure
- Deployment history tracking

**Usage**:
```bash
# Deploy to production with Docker
python scripts/deployment_automator.py deploy --environment production --mode docker

# Deploy to staging with Kubernetes
python scripts/deployment_automator.py deploy --environment staging --mode kubernetes

# Validate deployment prerequisites
python scripts/deployment_automator.py validate

# List deployment history
python scripts/deployment_automator.py list
```

**Supported Environments**:
- `development`: Development environment with debug settings
- `staging`: Staging environment for testing
- `production`: Production environment with optimized settings

**Supported Deployment Modes**:
- `docker`: Docker Compose deployment
- `kubernetes`: Kubernetes cluster deployment
- `azure`: Azure Container Instances or App Service
- `aws`: AWS ECS or Lambda deployment

### 4. AI Model Manager (`scripts/ai_model_manager.py`)

**Purpose**: Advanced model lifecycle management

**Features**:
- Download models from multiple sources
- Model registry with metadata
- Model optimization (quantization, pruning, distillation)
- Performance benchmarking
- Model export/import
- Automated cleanup of old models
- Checksum verification

**Usage**:
```bash
# List all models
python scripts/ai_model_manager.py list

# Download from Hugging Face
python scripts/ai_model_manager.py download --source "microsoft/DialoGPT-medium"

# Download from URL
python scripts/ai_model_manager.py download --source "https://example.com/model.bin"

# Optimize model
python scripts/ai_model_manager.py optimize --model-id my_model --optimization quantization

# Benchmark model
python scripts/ai_model_manager.py benchmark --model-id my_model

# Export model
python scripts/ai_model_manager.py export --model-id my_model --path model_export.zip

# Cleanup old models
python scripts/ai_model_manager.py cleanup --days 30 --confirm
```

**Model Sources Supported**:
- Hugging Face Hub (`microsoft/DialoGPT-medium` or `hf:model-name`)
- Direct URLs (`https://example.com/model.bin`)
- Local files (`file:/path/to/model`)

## 🎛️ Master Control Interface

### Interactive Dashboard

Run `python ai_workspace_control.py --interactive` to access the interactive dashboard:

```
🤖 AI Workspace Master Control Center
============================================================
📁 Workspace: /workspaces/semantic-kernel/ai-workspace
🕐 Current Time: 2024-06-15 18:00:00

📊 System Status:
   🟢 Workspace
   🟢 Python
   🟢 Docker
   🟢 API Server
   🟢 Required Dirs

🛠️  Available Tools:
   1. optimizer: Optimize workspace performance and clean up files
   2. monitor: Real-time monitoring and alerting
   3. deployment: Automated deployment to various environments
   4. model-manager: AI model lifecycle management
   5. mcp-test: Test MCP integration and GitHub connectivity
   6. api-test: Test API endpoints and services
   7. docker: Docker container management

📈 Recent Activity:
   • 17:45 - optimization_report
   • 17:30 - api_test
   • 17:15 - deployment_validation

💡 Type 'help' for commands or select a tool number (1-7)
   Or use: run <tool> <command> [args...]
```

### Command Format

```bash
# General format
python ai_workspace_control.py --tool <tool_name> --command <command_name> [--args arg1 arg2]

# Examples
python ai_workspace_control.py --tool optimizer --command optimize
python ai_workspace_control.py --tool model-manager --command list-models
python ai_workspace_control.py --tool deployment --command deploy --args --environment staging
```

### Batch Operations

Create batch files in the `batches/` directory:

```bash
# Run predefined batch
python ai_workspace_control.py --batch batches/quick-setup.batch

# Create custom batch
echo "run optimizer optimize" > my_batch.batch
echo "run api-test test-api" >> my_batch.batch
python ai_workspace_control.py --batch my_batch.batch
```

## 📋 Predefined Batch Files

### 1. Quick Setup (`batches/quick-setup.batch`)
- Workspace optimization
- Deployment validation
- API endpoint testing
- MCP integration testing
- Model listing
- Monitoring report generation

### 2. Full Deployment (`batches/full-deployment.batch`)
- Pre-deployment optimization
- Docker container building
- Deployment validation
- Staging environment deployment
- Service testing

### 3. Maintenance (`batches/maintenance.batch`)
- Cleanup temporary files
- Remove old models (30+ days)
- Generate system reports
- Validate all systems
- Test core functionality

## 🔧 Configuration

### Environment Variables

Create `.env` file in the workspace root:

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# Model Configuration
DEFAULT_MODEL_TYPE=transformers
MODEL_CACHE_DIR=models/cache

# Monitoring Configuration
MONITORING_INTERVAL=30
ALERT_EMAIL=admin@example.com

# Deployment Configuration
DEFAULT_ENVIRONMENT=production
DOCKER_REGISTRY=your-registry.com

# Performance Optimization
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
TOKENIZERS_PARALLELISM=false
```

### Monitoring Thresholds

Customize monitoring thresholds in the monitor script:

```python
self.thresholds = {
    "cpu_percent": 80.0,
    "memory_percent": 85.0,
    "disk_percent": 90.0,
    "gpu_memory_percent": 95.0,
    "api_response_time": 5.0,
    "error_rate": 0.1
}
```

## 🚨 Alerting System

The monitoring system includes configurable alerts:

- **CPU Usage**: Alert when CPU usage exceeds threshold
- **Memory Usage**: Alert when memory usage exceeds threshold
- **Disk Space**: Alert when disk usage exceeds threshold
- **API Availability**: Alert when API endpoints are unavailable
- **Service Health**: Alert when services stop responding
- **Error Rate**: Alert when error rate exceeds threshold

## 📊 Reporting

### System Reports

Generated automatically in `08-documentation/reports/`:

- `workspace_structure.md`: Detailed workspace structure
- `metrics.json`: System metrics and statistics
- `optimization_report.json`: Optimization results
- `deployment_history.json`: Deployment records

### Model Reports

Generated in `models/`:

- `model_registry.json`: Complete model registry
- `model_index.json`: Model file index
- `benchmark_<model>_<timestamp>.json`: Performance benchmarks

## 🔄 Automation Workflows

### CI/CD Integration

Add to your `.github/workflows/` for automated operations:

```yaml
name: AI Workspace Maintenance
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  maintenance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Maintenance
        run: |
          cd ai-workspace
          python ai_workspace_control.py --batch batches/maintenance.batch
```

### Scheduled Tasks

Set up cron jobs for regular maintenance:

```bash
# Daily optimization at 2 AM
0 2 * * * cd /path/to/ai-workspace && python ai_workspace_control.py --tool optimizer --command optimize

# Weekly model cleanup
0 3 * * 0 cd /path/to/ai-workspace && python ai_workspace_control.py --tool model-manager --command cleanup --args --days 7 --confirm

# Hourly health check
0 * * * * cd /path/to/ai-workspace && python ai_workspace_control.py --tool deployment --command validate
```

## 🔍 Troubleshooting

### Common Issues

1. **Script Permissions**:
   ```bash
   chmod +x scripts/*.py scripts/*.sh
   ```

2. **Missing Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Docker Issues**:
   ```bash
   # Check Docker status
   python ai_workspace_control.py --tool docker --command docker-build
   ```

4. **API Server Not Responding**:
   ```bash
   # Test API endpoints
   python ai_workspace_control.py --tool api-test --command test-api
   ```

### Log Files

Check logs in `logs/` directory:
- `optimization_report.json`: Optimization results
- `alerts.log`: System alerts
- `metrics_YYYYMMDD.json`: Daily metrics
- `cleanup.log`: Cleanup operations

### Debug Mode

Enable debug mode in interactive mode:

```bash
python ai_workspace_control.py --interactive
# Then type: status
```

## 🎯 Best Practices

1. **Regular Maintenance**: Run maintenance batch weekly
2. **Monitor Resources**: Keep monitoring running during heavy workloads
3. **Model Management**: Clean up unused models regularly
4. **Backup Strategy**: Deployment automator creates backups automatically
5. **Environment Separation**: Use different environments for dev/staging/prod
6. **Performance Monitoring**: Benchmark models before deployment
7. **Security**: Keep secrets in environment variables, not in code

## 🚀 Next Steps

1. **Custom Tools**: Add your own tools to the master control system
2. **Cloud Integration**: Extend deployment automator for your cloud provider
3. **Advanced Monitoring**: Add custom metrics and alerts
4. **Model Pipeline**: Integrate with your ML pipeline
5. **Team Collaboration**: Set up shared monitoring and alerts

---

For more information, see the main [README.md](README.md) and other documentation files.
