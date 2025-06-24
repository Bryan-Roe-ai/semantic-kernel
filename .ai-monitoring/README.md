# 🔍 Universal AI Monitoring System

**Complete visibility into every AI action, thought, and change in your repository**

## 🚀 Quick Start

### 1. Setup (One-time)

```bash
cd .ai-monitoring
python ai_launcher.py setup
```

### 2. Start Real-Time Dashboard

```bash
python ai_launcher.py dashboard
```

### 3. Test the System

```bash
python ai_launcher.py test
```

## 🎯 Features

### 📊 Universal AI Activity Tracking

- **Every AI action** across all agents and systems
- **Real-time thoughts** and decision processes
- **File changes** with AI context
- **Inter-agent communications**
- **Performance metrics** and success rates
- **Error tracking** and recovery patterns

### 🎛️ Real-Time Dashboard

```
🤖====================================================================🤖
🔍 UNIVERSAL AI ACTIVITY MONITORING DASHBOARD
📅 2025-06-21 14:30:25 | 🔄 Auto-refresh every 3 seconds
======================================================================

📊 SYSTEM OVERVIEW
🟢 Monitoring Status: ACTIVE
⏱️  Uptime: 2.5 hours
🤖 Active Agents: 7
📦 Event Queue: 0

📈 ACTIVITY SUMMARY (24h)
📊 Total Events: 1,247
✅ Success Rate: 96.1%
❌ Failed Events: 49

🕐 RECENT ACTIVITIES
✅ 14:30:22 | ⚡ PerformanceAgent    | Optimizing cache efficiency...
💭 14:30:20 | 🧠 CognitiveAgent     | Analyzing decision patterns...
📊 14:30:18 | 📈 AnalyticsAgent     | Trend analysis completed...
```

### 🗂️ Repository Organization

- **Logical structure** for maintainability
- **Automatic file organization** by type and purpose
- **Reference updates** to maintain functionality
- **Backup creation** before changes

## 📋 Available Commands

```bash
# Start monitoring dashboard
python ai_launcher.py dashboard

# Generate activity reports
python ai_launcher.py report 24        # Last 24 hours
python ai_launcher.py report 168       # Last week

# Repository organization
python ai_launcher.py organize-dry     # Simulate organization
python ai_launcher.py organize         # Actually organize

# System management
python ai_launcher.py status           # Check system status
python ai_launcher.py test             # Test with sample data
python ai_launcher.py setup            # Setup system
```

## 🏗️ Repository Structure (After Organization)

```
semantic-kernel/
├── 📁 01-core/                     # Core SK implementations
│   ├── dotnet/                     # .NET implementation
│   ├── python/                     # Python implementation
│   ├── java/                       # Java implementation
│   └── typescript/                 # TypeScript implementation
│
├── 📁 02-ai-workspace/             # Enhanced AI workspace
│   ├── agents/                     # AI agent implementations
│   ├── monitoring/                 # AI monitoring system
│   ├── scripts/                    # AI workspace scripts
│   └── logs/                       # Activity logs & reports
│
├── 📁 03-samples/                  # All sample implementations
│   ├── quickstart/                 # Getting started samples
│   ├── advanced/                   # Advanced usage examples
│   └── notebooks/                  # Jupyter notebooks
│
├── 📁 04-documentation/            # Consolidated documentation
│   ├── api/                        # API documentation
│   ├── guides/                     # User guides
│   └── architecture/               # Architecture docs
│
├── 📁 05-infrastructure/           # DevOps and infrastructure
│   ├── deployment/                 # Deployment scripts
│   ├── ci-cd/                      # CI/CD configurations
│   └── docker/                     # Container configurations
│
├── 📁 06-resources/                # Static resources and data
│   ├── data/                       # Sample data sets
│   ├── templates/                  # Project templates
│   └── configs/                    # Configuration files
│
└── 📁 .ai-monitoring/              # AI monitoring system
    ├── universal_ai_monitor.py     # Core monitoring system
    ├── universal_dashboard.py      # Real-time dashboard
    ├── repository_organizer.py     # Repository organization
    └── ai_launcher.py               # Main launcher
```

## 🔧 Integration Examples

### Manual Activity Logging

```python
from .ai-monitoring.universal_ai_monitor import log_ai_event, log_ai_thought, log_ai_decision

# Log AI thoughts
log_ai_thought("MyAgent", "I need to optimize this function for better performance")

# Log decisions with reasoning
log_ai_decision("MyAgent", "Use algorithm X", "It has O(n log n) complexity",
                ["algorithm_x", "algorithm_y"], confidence=0.85)

# Track actions with timing
with track_ai_action("MyAgent", "optimize_function") as action_id:
    result = optimize_my_function()
    # Automatically logs duration and success
```

### Agent Communication Tracking

```python
from .ai-monitoring.universal_ai_monitor import get_universal_monitor

monitor = get_universal_monitor()

# Log inter-agent communications
monitor.log_agent_communication("AnalysisAgent", "OptimizationAgent",
                                "Performance bottleneck detected in module X", "alert")
```

## 📊 Monitoring Capabilities

### What Gets Tracked

- 🧠 **AI Thoughts**: Reasoning processes and cognitive steps
- 🎯 **Decisions**: Choices made with confidence levels and reasoning
- ⚡ **Actions**: Every operation with timing and success metrics
- 📁 **File Changes**: All file modifications with AI context
- 📡 **Communications**: Inter-agent message exchanges
- 🚨 **Errors**: Failures with full context and stack traces
- 📈 **Performance**: Response times, success rates, resource usage

### Intelligence Features

- 🔍 **Pattern Recognition**: Identifies recurring behaviors
- 📊 **Performance Analytics**: Optimization recommendations
- 🚨 **Anomaly Detection**: Unusual behavior alerts
- 📈 **Trend Analysis**: Activity patterns over time
- 🎯 **Predictive Insights**: Future behavior predictions

## 🎯 Use Cases

### 1. **Development & Debugging**

- See exactly what your AI agents are thinking and doing
- Debug complex multi-agent interactions
- Optimize performance based on real metrics

### 2. **System Monitoring**

- Real-time visibility into AI system health
- Performance bottleneck identification
- Error pattern analysis

### 3. **Research & Analysis**

- Study AI decision-making patterns
- Analyze effectiveness of different approaches
- Generate datasets for further research

### 4. **Production Operations**

- Monitor AI systems in production
- Alert on unusual patterns or failures
- Performance optimization insights

## 🚨 Getting Started

1. **Setup the system**:

   ```bash
   cd .ai-monitoring
   python ai_launcher.py setup
   ```

2. **Start monitoring**:

   ```bash
   python ai_launcher.py dashboard
   ```

3. **Test it works**:

   ```bash
   python ai_launcher.py test
   ```

4. **Generate a report**:

   ```bash
   python ai_launcher.py report 24
   ```

5. **Organize your repository** (optional):
   ```bash
   python ai_launcher.py organize-dry  # Simulate first
   python ai_launcher.py organize      # Actually do it
   ```

## 📈 Performance Impact

The monitoring system is designed to be **lightweight**:

- **< 5% CPU overhead** for normal operations
- **< 10MB memory footprint**
- **Async processing** prevents blocking AI operations
- **Background database writes** for minimal latency
- **Automatic cleanup** of old data

## 🔒 Privacy & Security

- All data stays **local** to your repository
- **No external network** calls for monitoring
- **Configurable** data retention policies
- **Secure storage** in local SQLite database

---

## 🎉 You Now Have Complete AI Visibility!

**Every AI action, thought, and change is now tracked and visible in real-time.**

Start with: `python ai_launcher.py dashboard`


---

## 👨‍💻 Author & Attribution

**Created by Bryan Roe**  
Copyright (c) 2025 Bryan Roe  
Licensed under the MIT License

This is part of the Semantic Kernel - Advanced AI Development Framework.
For more information, see the main project repository.
