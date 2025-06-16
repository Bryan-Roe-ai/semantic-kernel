# Enhanced AutoMode for Long-Running Operations

This enhanced AutoMode system provides robust, self-healing capabilities for running AI applications for extended periods without manual intervention.

## Features

### 🔄 **Auto-Recovery & Self-Healing**
- Automatic process restart on failure
- Memory leak detection and mitigation
- Resource usage monitoring with automatic cleanup
- Circuit breaker pattern for external services
- Graceful degradation under stress

### 📊 **Comprehensive Monitoring**
- Real-time system and application metrics
- Health checks with configurable thresholds
- Prometheus metrics export for dashboards
- Detailed logging with automatic rotation
- Performance tracking and alerting

### 💾 **State Persistence**
- Automatic state backup and recovery
- Process restart counting and limits
- Configuration persistence across restarts
- Crash recovery with state restoration

### ⚙️ **Advanced Configuration**
- JSON-based configuration management
- Runtime parameter adjustment
- Environment-specific settings
- Feature toggles for different deployment modes

## Quick Start

### 1. Basic Setup
```bash
# Install with enhanced features
python setup.py --enhanced

# Or install dependencies manually
pip install psutil watchdog prometheus-client
```

### 2. Configuration
Create or modify `auto_mode_config.json`:
```json
{
  "check_interval": 30,
  "max_retries": 5,
  "max_memory_percent": 85.0,
  "enable_auto_restart": true,
  "enable_self_healing": true,
  "enable_monitoring": true
}
```

### 3. Run Enhanced AutoMode
```bash
# Start with enhanced features
python start_enhanced.py

# Or use the startup script directly
python startup_enhanced.py

# Check dependencies and services only
python startup_enhanced.py --check-only
```

## Configuration Options

### Core Settings
- `check_interval`: Seconds between health checks (default: 30)
- `max_retries`: Maximum restart attempts (default: 5)
- `retry_delay`: Seconds between restart attempts (default: 10)

### Resource Limits
- `max_memory_percent`: Memory usage threshold for restart (default: 85%)
- `max_cpu_percent`: CPU usage warning threshold (default: 90%)
- `max_disk_percent`: Disk usage critical threshold (default: 95%)

### Feature Toggles
- `enable_persistence`: Save/restore state across restarts
- `enable_auto_restart`: Automatically restart failed processes
- `enable_monitoring`: Enable comprehensive monitoring
- `enable_self_healing`: Perform automatic recovery actions
- `enable_graceful_degradation`: Reduce resource usage under stress
- `enable_circuit_breaker`: Protect against cascading failures

### Monitoring & Alerting
- `log_level`: Logging verbosity (DEBUG, INFO, WARNING, ERROR)
- `metrics_retention_days`: Days to keep metrics files
- `backup_retention_days`: Days to keep state backups
- `webhook_url`: URL for health status notifications

## Architecture

### Core Components

#### 1. **EnhancedAutoMode**
Main orchestrator that manages all long-running operations:
- Process lifecycle management
- Health monitoring coordination
- State persistence
- Signal handling for graceful shutdown

#### 2. **HealthMonitor**
Comprehensive monitoring system:
- System resource tracking (CPU, memory, disk, network)
- Application-specific metrics
- Error rate monitoring
- Service availability checks

#### 3. **PersistenceManager**
State management and recovery:
- JSON-based state storage
- Automatic backup creation
- Recovery from multiple backup levels
- Old file cleanup

#### 4. **CircuitBreaker**
Fault tolerance for external services:
- Automatic failure detection
- Service isolation during outages
- Gradual recovery testing
- Configurable thresholds

### Process Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Startup       │───▶│   Environment    │───▶│   Dependencies  │
│   Validation    │    │   Setup          │    │   Check         │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Service       │◀───│   Process        │◀───│   Application   │
│   Monitoring    │    │   Management     │    │   Start         │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│   Health        │    │   Auto-Recovery  │
│   Checks        │    │   Actions        │
└─────────────────┘    └──────────────────┘
```

## Monitoring & Metrics

### Built-in Metrics
- **System**: CPU, memory, disk, network usage
- **Process**: Per-process resource consumption
- **Application**: Uptime, restart count, error rate
- **Custom**: Response times, queue sizes, throughput

### Prometheus Integration
Start the metrics exporter:
```bash
python metrics_exporter.py --port 8001
```

Access metrics at: `http://localhost:8001/metrics`

### Example Prometheus Queries
```promql
# High memory usage alert
system_memory_percent > 90

# Application restart rate
rate(app_restarts_total[5m]) > 0

# Backend response time
histogram_quantile(0.95, backend_response_time_seconds)
```

## Advanced Usage

### Custom Process Management
```python
from auto_mode_enhanced import EnhancedAutoMode, AutoModeConfig

config = AutoModeConfig(
    check_interval=15,
    max_memory_percent=80.0,
    enable_self_healing=True
)

automode = EnhancedAutoMode(config)

# Start managed process
await automode.start_managed_process(
    "my_service",
    ["python", "my_service.py"]
)

# Run forever with monitoring
await automode.run()
```

### Health Check Integration
```python
# Custom health check function
async def custom_health_check():
    # Your health check logic
    return {"status": "healthy", "custom_metric": 42}

# Add to monitoring
automode.health_monitor.add_custom_check(custom_health_check)
```

## Troubleshooting

### Common Issues

**1. High Memory Usage**
- Check `max_memory_percent` setting
- Review application for memory leaks
- Enable automatic restart: `"enable_auto_restart": true`

**2. Frequent Restarts**
- Increase `retry_delay` for slower recovery
- Check external service dependencies
- Review logs for root cause

**3. Process Won't Start**
- Verify dependencies with `--check-only`
- Check file permissions and paths
- Review startup logs in `logs/startup.log`

### Log Locations
- Main log: `logs/automode_YYYYMMDD.log`
- Error log: `logs/errors.log`
- Startup log: `logs/startup.log`
- Metrics log: `logs/metrics.log`

### State Files
- Current state: `.automode_state/automode_state.json`
- Backups: `.automode_state/backups/`
- Configuration: `auto_mode_config.json`

## Best Practices

### 1. **Resource Monitoring**
- Set conservative memory limits (80-85%)
- Monitor disk space regularly
- Use external monitoring tools for alerts

### 2. **Configuration Management**
- Keep configuration in version control
- Use environment-specific configs
- Test configuration changes in staging

### 3. **Logging Strategy**
- Use appropriate log levels
- Implement log rotation
- Monitor error rates and patterns

### 4. **Disaster Recovery**
- Regular state backups
- Test recovery procedures
- Document escalation procedures

### 5. **Performance Optimization**
- Adjust check intervals based on load
- Use circuit breakers for external calls
- Enable graceful degradation for peak loads

## Integration Examples

### Docker Deployment
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["python", "start_enhanced.py"]
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-chat-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ai-chat-app
  template:
    metadata:
      labels:
        app: ai-chat-app
    spec:
      containers:
      - name: ai-chat-app
        image: ai-chat-app:latest
        ports:
        - containerPort: 8000
        - containerPort: 8001  # Metrics
        resources:
          limits:
            memory: "2Gi"
            cpu: "1000m"
          requests:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Systemd Service
```ini
[Unit]
Description=AI Chat Application with Enhanced AutoMode
After=network.target

[Service]
Type=simple
User=aichat
WorkingDirectory=/opt/aichat
ExecStart=/usr/bin/python3 start_enhanced.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

## Contributing

1. Follow the existing code style
2. Add tests for new features
3. Update documentation
4. Test in multiple environments

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review log files for errors
3. Verify configuration settings
4. Test with `--check-only` flag
