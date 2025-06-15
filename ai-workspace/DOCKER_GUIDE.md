# 🐳 Docker Deployment Guide for AI Workspace

This guide covers the complete Docker deployment and automation setup for your Semantic Kernel AI Workspace.

## 🚀 Quick Start with Docker

### Option 1: Docker Compose (Recommended)

```bash
# Start all services with one command
./scripts/docker_manager.sh compose

# Or manually:
docker-compose up -d
```

### Option 2: Single Container

```bash
# Build and run single container
./scripts/docker_manager.sh build
./scripts/docker_manager.sh run
```

## 📁 Docker Structure

ai-workspace/
├── Dockerfile # Multi-stage production build
├── docker-compose.yml # Full orchestration
├── docker-compose.dev.yml # Development overrides
├── .dockerignore # Build optimization
├── docker/
│ ├── entrypoint.sh # Container initialization
│ ├── supervisord.conf # Service management
│ └── nginx.conf # Reverse proxy config
└── scripts/
├── cleanup_and_automate.sh # Workspace automation
└── docker_manager.sh # Docker operations

```
ai-workspace/
├── Dockerfile                 # Multi-stage production build
├── docker-compose.yml         # Full orchestration
├── docker-compose.dev.yml     # Development overrides
├── .dockerignore              # Build optimization
├── docker/
│   ├── entrypoint.sh          # Container initialization
│   ├── supervisord.conf       # Service management
│   └── nginx.conf             # Reverse proxy config
└── scripts/
    ├── cleanup_and_automate.sh # Workspace automation
    └── docker_manager.sh       # Docker operations
```

## 🛠️ Available Services

### Core AI Workspace

- **Main Portal**: <http://localhost> (Nginx reverse proxy)
- **Jupyter Lab**: <http://localhost:8888> (or <http://localhost/jupyter>)
- **Backend API**: <http://localhost:8000> (or <http://localhost/api>)
- **Web Interface**: <http://localhost:3000>

### Supporting Services

- **Redis Cache**: localhost:6379
- **ChromaDB**: <http://localhost:8001>
- **Prometheus**: <http://localhost:9090>
- **Grafana**: <http://localhost:3001>

## 🔧 Management Commands

### Using Docker Manager Script

```bash
# Build image
./scripts/docker_manager.sh build

# Start services
./scripts/docker_manager.sh compose

# Show status
./scripts/docker_manager.sh status

# View logs
./scripts/docker_manager.sh logs [service-name]

# Execute into container
./scripts/docker_manager.sh exec [service-name]

# Development mode
./scripts/docker_manager.sh dev

# Production deployment
./scripts/docker_manager.sh deploy

# Stop services
./scripts/docker_manager.sh stop

# Cleanup resources
./scripts/docker_manager.sh cleanup
```

### Using Cleanup Script

```bash
# Run all automation tasks
./scripts/cleanup_and_automate.sh --all

# Individual tasks
./scripts/cleanup_and_automate.sh --cleanup
./scripts/cleanup_and_automate.sh --optimize
./scripts/cleanup_and_automate.sh --docker
./scripts/cleanup_and_automate.sh --health
```

## 📋 Pre-Deployment Checklist

1. **Environment Configuration**

   ```bash
   # Copy template and configure
   cp .env.template .env
   # Edit .env with your API keys
   ```

2. **Cleanup Workspace**

   ```bash
   ./scripts/cleanup_and_automate.sh --all
   ```

3. **Build and Test**

   ```bash
   ./scripts/docker_manager.sh build
   ./scripts/docker_manager.sh health
   ```

## 🏗️ Docker Build Stages

### Stage 1: Base Dependencies

- Python 3.11 slim
- System packages (Node.js, Git, Supervisor, Nginx)

### Stage 2: Python Dependencies

- Virtual environment creation
- Requirements installation

### Stage 3: Application Build

- Workspace copying
- Permission setup

### Stage 4: Production Runtime

- Non-root user setup
- Health checks
- Service orchestration

## 🔐 Security Features

- Non-root container execution
- Environment variable isolation
- Nginx reverse proxy with security headers
- Network isolation with custom bridge
- Health check endpoints
- CORS configuration

## 📊 Monitoring & Logging

### Service Logs

```bash
# View all services
docker-compose logs -f

# Specific service
./scripts/docker_manager.sh logs jupyter
./scripts/docker_manager.sh logs backend
```

### Health Monitoring

- Container health checks
- Service endpoint monitoring
- Resource usage tracking
- Automatic service restart

### Metrics Collection

- Prometheus metrics
- Grafana dashboards
- System diagnostics
- Performance monitoring

## 🛠️ Development Mode

### Enable Development Features

```bash
# Start in development mode
./scripts/docker_manager.sh dev

# Or manually
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### Development Features

- Hot reloading
- Debug logging
- Volume mounts for live editing
- Development database
- Extended debugging tools

## 🚀 Production Deployment

### Production-Ready Features

- Multi-stage optimized builds
- Service orchestration
- Automatic restarts
- Load balancing
- Caching layer
- Security hardening

### Deployment Process

```bash
# One-command production deploy
./scripts/docker_manager.sh deploy
```

This will:

1. Build optimized image
2. Start all services
3. Run health checks
4. Verify deployment

## 🔧 Troubleshooting

### Common Issues

1. **Port Conflicts**

   ```bash
   # Check what's using ports
   netstat -tulpn | grep :8000
   # Stop conflicting services
   ```

2. **Permission Issues**

   ```bash
   # Fix permissions
   sudo chown -R $USER:$USER .
   chmod +x scripts/*.sh
   ```

3. **Docker Space Issues**

   ```bash
   # Clean up Docker
   ./scripts/docker_manager.sh cleanup
   docker system prune -a
   ```

4. **Service Not Starting**

   ```bash
   # Check logs
   ./scripts/docker_manager.sh logs [service]
   # Check health
   ./scripts/docker_manager.sh health
   ```

### Debug Commands

```bash
# Enter container shell
./scripts/docker_manager.sh exec

# Check service status
docker-compose ps

# View resource usage
docker stats

# Inspect container
docker inspect semantic-kernel-ai-workspace
```

## 📈 Performance Optimization

### Resource Allocation

- Adjust memory limits in docker-compose.yml
- Configure worker processes
- Optimize caching strategies

### Build Optimization

- Multi-stage builds reduce image size
- .dockerignore excludes unnecessary files
- Layer caching for faster rebuilds

### Runtime Optimization

- Supervisor for process management
- Nginx for efficient serving
- Redis for caching
- Volume mounts for data persistence

## 🔄 Backup & Recovery

### Data Persistence

All important data is stored in Docker volumes:

- `ai_data`: Application data
- `ai_models`: ML models
- `ai_logs`: Service logs
- `ai_uploads`: User uploads

### Backup Strategy

```bash
# Backup volumes
docker run --rm -v ai_data:/data -v $(pwd):/backup alpine tar czf /backup/ai_data_backup.tar.gz -C /data .

# Backup configuration
./scripts/cleanup_and_automate.sh --backup
```

## 🎯 Next Steps

1. **Configure Environment**: Set up your API keys in `.env`
2. **Deploy Services**: Run `./scripts/docker_manager.sh deploy`
3. **Access Services**: Open <http://localhost> in your browser
4. **Monitor Health**: Use `./scripts/docker_manager.sh health`
5. **Scale as Needed**: Adjust docker-compose.yml for your requirements

## 🤝 Support

- Use `./launch.sh` for interactive management
- Check logs with `./scripts/docker_manager.sh logs`
- Run health checks with `./scripts/docker_manager.sh health`
- Clean up with `./scripts/cleanup_and_automate.sh --all`

Your AI workspace is now fully containerized and production-ready! 🎉
