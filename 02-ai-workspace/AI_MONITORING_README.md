# 🤖 AI Activity Monitoring System

**See every action, thought, and change made by any AI in your repository**

This comprehensive monitoring system captures and displays all AI activities across your entire workspace, providing real-time visibility into what your AI agents are doing.

## 🌟 Features

### 📊 Complete Activity Tracking
- **Actions**: Every AI operation and execution
- **Thoughts**: AI reasoning and decision-making processes  
- **Decisions**: Choices made with reasoning explanations
- **Analysis**: Results from AI analysis operations
- **File Changes**: Real-time file system monitoring
- **Errors**: Failed operations with detailed context

### 🎯 Real-Time Dashboard
- Live updating display of AI activities
- Agent performance metrics
- Success rates and error tracking
- File change monitoring
- Activity type breakdowns

### 💾 Comprehensive Storage
- **SQLite Database**: Structured, queryable storage
- **JSON Logs**: Human-readable daily activity logs
- **Historical Reports**: Generate reports for any time period
- **Search & Filter**: Find specific activities by agent, type, or time

### 🔌 Automatic Integration
- **Zero-code Integration**: Automatically patches existing AI agents
- **Async Support**: Works with both sync and async operations
- **Error Resilience**: Continues monitoring even if agents fail
- **Background Processing**: Non-intrusive monitoring

## 🚀 Quick Start

### 1. Setup the System
```bash
cd 02-ai-workspace/scripts
python setup_monitoring.py
```

### 2. Start Real-Time Dashboard
```bash
python ai_monitor_launcher.py dashboard
```

### 3. View Live Activity Feed  
```bash
python ai_monitor_launcher.py feed
```

### 4. Generate Activity Report
```bash
python ai_monitor_launcher.py report --hours 24
```

### 5. Test the System
```bash
python ai_monitor_launcher.py test
```

## 📊 Dashboard Overview

The real-time dashboard shows:

```
🤖====================================================================🤖
🎯 AI ACTIVITY MONITORING DASHBOARD
📅 2025-06-21 14:30:25 | 🔄 Auto-refresh every 5 seconds
======================================================================

📊 ACTIVITY SUMMARY
------------------------------
📈 Total Activities (24h): 1,247
✅ Successful: 1,198 (96.1%)
❌ Failed: 49
🔀 Activity Types: action(456), thought(321), analysis(298)

🕐 RECENT ACTIVITIES (Last 20)
--------------------------------------------------
✅ 14:30:22 | 🎯 PerformanceAgent | Optimizing cache efficiency...
💭 14:30:20 | 🧠 CognitiveAgent  | Analyzing decision patterns...
📊 14:30:18 | 📈 AnalyticsAgent  | Trend analysis completed...
🤔 14:30:15 | 🎯 OptimizerAgent  | Choose strategy A over B...

🤖 AGENT PERFORMANCE
------------------------------
🟢 PerformanceAgent   | Acts: 89  | Success: 94.3% | Avg: 234.5ms
🟢 CognitiveAgent     | Acts: 67  | Success: 91.0% | Avg: 567.2ms
🟡 SecurityAgent      | Acts: 45  | Success: 88.9% | Avg: 123.8ms

📝 FILE CHANGES (Last 10)
-----------------------------------
✏️ 14:30:15 | modified | scripts/optimizer.py
➕ 14:29:45 | created  | logs/analysis_2025-06-21.json
🗑️ 14:29:30 | deleted  | temp/old_cache.tmp
```

## 🔧 Advanced Usage

### Manual Activity Logging

```python
from ai_monitoring_integration import get_logger

# Get a logger for your agent
logger = get_logger("MyAgent")

# Log different types of activities
logger.thought("I need to optimize this function")
logger.decision("Use algorithm X", "It has better performance", ["X", "Y", "Z"])
logger.action("optimize_function", function_name="process_data", improvement=23.5)
logger.analysis("performance_test", cpu_usage=45.2, memory_usage=67.8)
logger.error("Database connection failed", error_code="CONN_TIMEOUT")
logger.result("Optimization completed", performance_gain=23.5)
```

### Context Manager for Actions

```python
from ai_monitoring_integration import track_ai_action

async def my_ai_function():
    async with track_ai_action("MyAgent", "complex_analysis", input_size=1000):
        # Your AI logic here
        result = await perform_analysis()
        return result
```

### Monitoring Custom Agents

```python
from ai_monitoring_integration import monitor_agent

# Monitor an existing agent instance
monitored_agent = monitor_agent(my_agent_instance, "CustomAgent")

# Or use as a class decorator
@monitor_agent
class MyAIAgent:
    def analyze(self):
        # This method will be automatically monitored
        pass
```

## 📁 File Structure

```
02-ai-workspace/
├── scripts/
│   ├── ai_activity_monitor.py      # Core monitoring system
│   ├── ai_activity_dashboard.py    # Real-time dashboard
│   ├── ai_monitoring_integration.py # Agent integration
│   ├── ai_monitor_launcher.py      # Main launcher
│   └── setup_monitoring.py         # Setup script
├── logs/
│   ├── ai_activities.db           # SQLite database
│   ├── activities_2025-06-21.jsonl # Daily JSON logs
│   └── ai_activity_report_*.json  # Generated reports
└── monitoring_config.json         # Configuration
```

## 🎛️ Commands Reference

### Dashboard Commands
```bash
# Start real-time dashboard (default)
python ai_monitor_launcher.py dashboard

# Start with custom refresh rate
python ai_monitor_launcher.py dashboard --refresh 3
```

### Reporting Commands
```bash
# Generate 24-hour report
python ai_monitor_launcher.py report

# Generate custom time period report
python ai_monitor_launcher.py report --hours 168  # 1 week

# Generate report for specific date range
python ai_activity_dashboard.py --export 24
```

### Monitoring Commands
```bash
# Start monitoring system (background)
python ai_monitor_launcher.py start

# Show live activity feed
python ai_monitor_launcher.py feed

# Show system status
python ai_monitor_launcher.py status

# Test with sample activities
python ai_monitor_launcher.py test
```

## 🔍 Querying Activities

### Using the Dashboard
The dashboard provides filtering and search capabilities:
- Filter by agent name
- Filter by activity type
- Filter by time range
- Search descriptions

### Direct Database Access
```python
from ai_activity_monitor import get_monitor

monitor = get_monitor()

# Get activities for specific agent
activities = monitor.get_agent_activities("PerformanceAgent", limit=50)

# Get activities by type
activities = monitor.db.get_activities(activity_type="decision", limit=100)

# Get activities since specific time
from datetime import datetime, timedelta
since = (datetime.now() - timedelta(hours=6)).isoformat()
activities = monitor.db.get_activities(since=since)
```

### Exporting Data
```python
from ai_activity_dashboard import AIActivityDashboard

dashboard = AIActivityDashboard(workspace_root)

# Export comprehensive report
report = dashboard.export_report(hours=24)

# Save to file
filepath = dashboard.save_report_to_file(hours=48)
```

## 🛠️ Configuration

### Environment Variables
```bash
# Disable auto-monitoring of existing agents
export DISABLE_AI_MONITORING=true

# Custom workspace root
export AI_WORKSPACE_ROOT=/path/to/workspace
```

### Config File (`monitoring_config.json`)
```json
{
  "workspace_root": "/home/user/semantic-kernel",
  "logs_directory": "/home/user/semantic-kernel/02-ai-workspace/logs",
  "auto_monitor": true,
  "dashboard_refresh_interval": 5,
  "max_activities_in_memory": 1000,
  "file_watch_patterns": [".py", ".js", ".ts", ".json", ".md"]
}
```

## 🔧 Troubleshooting

### Common Issues

**Q: Dashboard shows no activities**
```bash
# Test the system first
python ai_monitor_launcher.py test

# Check if monitoring is running
python ai_monitor_launcher.py status
```

**Q: File watching not working**
```bash
# Install watchdog dependency
pip install watchdog

# Check file permissions
ls -la logs/
```

**Q: Database errors**
```bash
# Reset database
rm logs/ai_activities.db
python setup_monitoring.py
```

**Q: Import errors**
```bash
# Make sure you're in the scripts directory
cd 02-ai-workspace/scripts

# Check Python path
python -c "import sys; print(sys.path)"
```

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now run monitoring with detailed logs
```

## 📈 Performance Impact

The monitoring system is designed to be **lightweight and non-intrusive**:

- **< 5% CPU overhead** for normal operations
- **< 10MB memory footprint** for the monitoring system
- **Async processing** prevents blocking AI operations
- **Background database writes** for minimal latency
- **Automatic cleanup** of old log files

## 🤝 Integration Examples

### With Existing Improvement Loop
```python
# The monitoring system automatically patches existing agents
# No code changes needed!

# But you can add manual logging for more detail:
from ai_monitoring_integration import get_logger

class MyAgent(ImprovementAgent):
    def __init__(self):
        super().__init__()
        self.logger = get_logger(self.__class__.__name__)
    
    async def analyze(self):
        self.logger.thought("Starting analysis phase")
        
        # Your existing code
        metrics = await super().analyze()
        
        self.logger.analysis("metrics_calculated", 
                           metric_count=len(metrics),
                           avg_score=sum(m.score() for m in metrics) / len(metrics))
        
        return metrics
```

### With Custom AI Scripts
```python
from ai_monitoring_integration import track_ai_action, get_logger

logger = get_logger("DataProcessor")

async def process_large_dataset(data):
    async with track_ai_action("DataProcessor", "dataset_processing", 
                              records=len(data)):
        
        logger.thought(f"Processing {len(data)} records")
        
        for chunk in chunked_data(data):
            result = await process_chunk(chunk)
            logger.analysis("chunk_processed", 
                           records=len(chunk), 
                           processing_time=result.duration)
        
        logger.decision("Use caching strategy", 
                       "Repeated patterns detected",
                       ["cache", "recompute", "partial_cache"])
        
        return final_result
```

## 🎯 Use Cases

### 1. **Debugging AI Behavior**
- See exactly what decisions your AI agents are making
- Trace the reasoning behind actions
- Identify bottlenecks and performance issues

### 2. **Performance Optimization**
- Monitor agent execution times
- Identify slow or failing operations
- Track success rates over time

### 3. **Development Insights**
- Understand how agents interact with files
- See which agents are most active
- Track the impact of code changes

### 4. **System Monitoring**
- Real-time dashboard for production environments
- Historical reporting for analysis
- Alert on unusual patterns or failures

### 5. **Research & Analysis**
- Study AI agent behavior patterns
- Generate datasets for ML research
- Analyze decision-making processes

## 🚀 Next Steps

1. **Start with the dashboard**: `python ai_monitor_launcher.py dashboard`
2. **Run some AI operations** and watch them appear in real-time
3. **Generate a report** to see historical data
4. **Add manual logging** to your custom agents for more detail
5. **Set up automated monitoring** for production use

---

**Happy Monitoring! 🤖📊**

For questions or issues, check the troubleshooting section above or examine the generated log files in `02-ai-workspace/logs/`.
