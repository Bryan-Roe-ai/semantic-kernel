#!/usr/bin/env python3
"""
🔍 Universal AI Activity Monitor
Complete tracking system for all AI actions, thoughts, and changes in the repository.
Provides 100% visibility into AI behavior across all agents and systems.
"""

import json
import os
import sys
import asyncio
import logging
import sqlite3
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Union
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import hashlib
import subprocess
from contextlib import contextmanager
import traceback
import psutil
import signal

# Add workspace scripts to path
workspace_root = Path(__file__).parent.parent.parent
sys.path.append(str(workspace_root / "02-ai-workspace" / "scripts"))

try:
    from ai_activity_monitor import AIActivityMonitor, AIActivity, get_monitor
except ImportError:
    print("⚠️  Warning: Could not import existing AI monitor. Will create standalone system.")
    AIActivityMonitor = None

# Set up comprehensive logging
def setup_logging():
    """Setup logging with proper path handling"""
    monitoring_dir = Path(__file__).parent
    log_file = monitoring_dir / 'logs' / 'universal_monitor.log'
    log_file.parent.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

setup_logging()
logger = logging.getLogger('UniversalAIMonitor')

@dataclass
class AIEvent:
    """Enhanced AI event with complete context"""
    id: str
    timestamp: str
    agent_name: str
    event_type: str  # action, thought, decision, analysis, change, error, communication
    description: str
    details: Dict[str, Any]
    file_path: Optional[str] = None
    line_numbers: Optional[List[int]] = None
    stack_trace: Optional[str] = None
    parent_event_id: Optional[str] = None
    child_event_ids: List[str] = None
    duration_ms: Optional[float] = None
    success: Optional[bool] = None
    confidence: Optional[float] = None
    impact_score: Optional[float] = None
    tags: List[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.child_event_ids is None:
            self.child_event_ids = []
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class UniversalAIMonitor:
    """
    Universal AI monitoring system that captures EVERYTHING:
    - All AI agent actions and thoughts
    - File system changes with AI context
    - Inter-agent communications
    - Performance metrics
    - Error patterns
    - Decision trees
    - Learning behaviors
    """

    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.monitoring_dir = self.workspace_root / '.ai-monitoring'
        self.monitoring_dir.mkdir(exist_ok=True)

        # Create subdirectories
        for subdir in ['logs', 'reports', 'config', 'agents', 'dashboards']:
            (self.monitoring_dir / subdir).mkdir(exist_ok=True)

        # Enhanced database
        self.db_path = self.monitoring_dir / 'logs' / 'universal_ai_events.db'
        self._init_database()

        # Active monitoring
        self.active_agents: Set[str] = set()
        self.event_queue = deque(maxlen=10000)
        self.event_cache = {}
        self.agent_relationships = defaultdict(set)
        self.performance_metrics = defaultdict(dict)

        # Real-time streams
        self.event_streams = defaultdict(list)
        self.subscribers = []

        # Monitoring state
        self.is_monitoring = True
        self.start_time = datetime.now()

        # Start background processors
        self._start_background_services()

        logger.info("🔍 Universal AI Monitor initialized")
        self.log_system_event("monitor_started", "Universal AI monitoring system activated")

    def _init_database(self):
        """Initialize enhanced database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ai_events (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    agent_name TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    details TEXT NOT NULL,
                    file_path TEXT,
                    line_numbers TEXT,
                    stack_trace TEXT,
                    parent_event_id TEXT,
                    child_event_ids TEXT,
                    duration_ms REAL,
                    success BOOLEAN,
                    confidence REAL,
                    impact_score REAL,
                    tags TEXT,
                    metadata TEXT,
                    FOREIGN KEY (parent_event_id) REFERENCES ai_events (id)
                )
            """)

            # Enhanced indexes for fast querying
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_timestamp ON ai_events (timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_agent_name ON ai_events (agent_name)",
                "CREATE INDEX IF NOT EXISTS idx_event_type ON ai_events (event_type)",
                "CREATE INDEX IF NOT EXISTS idx_success ON ai_events (success)",
                "CREATE INDEX IF NOT EXISTS idx_parent_child ON ai_events (parent_event_id, id)",
            ]

            for index in indexes:
                conn.execute(index)

            # Agent relationship tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_interactions (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    source_agent TEXT NOT NULL,
                    target_agent TEXT NOT NULL,
                    interaction_type TEXT NOT NULL,
                    details TEXT NOT NULL
                )
            """)

            # Performance metrics
            conn.execute("""
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    agent_name TEXT NOT NULL,
                    metric_type TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    metadata TEXT
                )
            """)

    def _start_background_services(self):
        """Start all background monitoring services"""
        # Event processor
        threading.Thread(target=self._process_event_queue, daemon=True).start()

        # Performance monitor
        threading.Thread(target=self._monitor_performance, daemon=True).start()

        # File system watcher
        threading.Thread(target=self._monitor_file_system, daemon=True).start()

        # Agent discovery
        threading.Thread(target=self._discover_agents, daemon=True).start()

        # Report generator
        threading.Thread(target=self._generate_periodic_reports, daemon=True).start()

    def log_ai_event(self,
                     agent_name: str,
                     event_type: str,
                     description: str,
                     details: Dict[str, Any] = None,
                     **kwargs) -> str:
        """Log any AI event with full context capture"""

        event_id = self._generate_event_id(agent_name, event_type, description)

        # Capture stack trace for debugging
        stack_trace = None
        if kwargs.get('capture_stack', False):
            stack_trace = traceback.format_stack()

        event = AIEvent(
            id=event_id,
            timestamp=datetime.now().isoformat(),
            agent_name=agent_name,
            event_type=event_type,
            description=description,
            details=details or {},
            stack_trace=stack_trace,
            **{k: v for k, v in kwargs.items() if k != 'capture_stack'}
        )

        # Add to processing queue
        self.event_queue.append(event)

        # Cache for real-time access
        self.event_cache[event_id] = event

        # Track active agents
        self.active_agents.add(agent_name)

        # Real-time streaming
        for subscriber in self.subscribers:
            try:
                subscriber(event)
            except Exception as e:
                logger.error(f"Error notifying subscriber: {e}")

        return event_id

    def log_ai_thought(self, agent_name: str, thought: str, context: Dict[str, Any] = None):
        """Log AI reasoning and thoughts"""
        return self.log_ai_event(
            agent_name=agent_name,
            event_type="thought",
            description=f"💭 {thought}",
            details=context or {},
            tags=["reasoning", "cognitive"]
        )

    def log_ai_decision(self, agent_name: str, decision: str, reasoning: str,
                       options: List[str] = None, confidence: float = None):
        """Log AI decisions with full context"""
        return self.log_ai_event(
            agent_name=agent_name,
            event_type="decision",
            description=f"🎯 {decision}",
            details={
                "reasoning": reasoning,
                "options_considered": options or [],
                "decision_confidence": confidence
            },
            confidence=confidence,
            tags=["decision", "reasoning"]
        )

    def log_ai_action(self, agent_name: str, action: str,
                     file_path: str = None, **action_details):
        """Log AI actions with performance tracking"""
        start_time = time.time()

        event_id = self.log_ai_event(
            agent_name=agent_name,
            event_type="action",
            description=f"⚡ {action}",
            details=action_details,
            file_path=file_path,
            tags=["action", "execution"]
        )

        return event_id, start_time

    def complete_ai_action(self, event_id: str, start_time: float,
                          success: bool = True, result: Any = None):
        """Complete an AI action with timing and results"""
        duration_ms = (time.time() - start_time) * 1000

        if event_id in self.event_cache:
            event = self.event_cache[event_id]
            event.duration_ms = duration_ms
            event.success = success
            if result:
                event.details['result'] = str(result)

        # Log completion event
        self.log_ai_event(
            agent_name=self.event_cache[event_id].agent_name if event_id in self.event_cache else "Unknown",
            event_type="completion",
            description=f"✅ Action completed {'successfully' if success else 'with errors'}",
            details={
                "parent_action_id": event_id,
                "duration_ms": duration_ms,
                "success": success,
                "result": str(result) if result else None
            },
            parent_event_id=event_id,
            duration_ms=duration_ms,
            success=success
        )

    def log_agent_communication(self, source_agent: str, target_agent: str,
                               message: str, communication_type: str = "message"):
        """Log inter-agent communications"""
        self.agent_relationships[source_agent].add(target_agent)

        # Store in database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO agent_interactions
                (id, timestamp, source_agent, target_agent, interaction_type, details)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                self._generate_event_id(source_agent, "communication", message),
                datetime.now().isoformat(),
                source_agent,
                target_agent,
                communication_type,
                json.dumps({"message": message})
            ))

        return self.log_ai_event(
            agent_name=f"{source_agent}→{target_agent}",
            event_type="communication",
            description=f"📡 {communication_type}: {message}",
            details={
                "source_agent": source_agent,
                "target_agent": target_agent,
                "communication_type": communication_type,
                "message": message
            },
            tags=["communication", "multi-agent"]
        )

    def log_file_change(self, file_path: str, change_type: str, agent_context: str = None):
        """Log file changes with AI context"""
        rel_path = str(Path(file_path).relative_to(self.workspace_root))

        return self.log_ai_event(
            agent_name=agent_context or "FileSystemMonitor",
            event_type="file_change",
            description=f"📁 {change_type}: {rel_path}",
            details={
                "change_type": change_type,
                "file_path": rel_path,
                "absolute_path": file_path,
                "file_size": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                "file_extension": Path(file_path).suffix,
                "ai_context": agent_context
            },
            file_path=rel_path,
            tags=["file_change", "system"]
        )

    def log_system_event(self, event_type: str, description: str, **details):
        """Log system-level events"""
        return self.log_ai_event(
            agent_name="SystemMonitor",
            event_type="system",
            description=f"🖥️ {description}",
            details=details,
            tags=["system", event_type]
        )

    def log_error(self, agent_name: str, error: Exception, context: str = ""):
        """Log errors with full context"""
        return self.log_ai_event(
            agent_name=agent_name,
            event_type="error",
            description=f"❌ {type(error).__name__}: {str(error)}",
            details={
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context,
                "traceback": traceback.format_exc()
            },
            success=False,
            stack_trace=traceback.format_exc(),
            tags=["error", "failure"]
        )

    def _process_event_queue(self):
        """Background processor for event queue"""
        while self.is_monitoring:
            try:
                if self.event_queue:
                    events_to_process = []
                    # Process in batches for efficiency
                    for _ in range(min(50, len(self.event_queue))):
                        events_to_process.append(self.event_queue.popleft())

                    self._persist_events(events_to_process)

                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
            except Exception as e:
                logger.error(f"Error processing event queue: {e}")

    def _persist_events(self, events: List[AIEvent]):
        """Persist events to database"""
        with sqlite3.connect(self.db_path) as conn:
            for event in events:
                conn.execute("""
                    INSERT OR REPLACE INTO ai_events
                    (id, timestamp, agent_name, event_type, description, details,
                     file_path, line_numbers, stack_trace, parent_event_id,
                     child_event_ids, duration_ms, success, confidence,
                     impact_score, tags, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    event.id,
                    event.timestamp,
                    event.agent_name,
                    event.event_type,
                    event.description,
                    json.dumps(event.details),
                    event.file_path,
                    json.dumps(event.line_numbers) if event.line_numbers else None,
                    event.stack_trace,
                    event.parent_event_id,
                    json.dumps(event.child_event_ids),
                    event.duration_ms,
                    event.success,
                    event.confidence,
                    event.impact_score,
                    json.dumps(event.tags),
                    json.dumps(event.metadata)
                ))

    def _monitor_performance(self):
        """Monitor system performance and AI agent efficiency"""
        while self.is_monitoring:
            try:
                # System metrics
                cpu_percent = psutil.cpu_percent()
                memory_percent = psutil.virtual_memory().percent
                disk_usage = psutil.disk_usage('/').percent

                self.log_system_event(
                    "performance_metrics",
                    f"System performance snapshot",
                    cpu_percent=cpu_percent,
                    memory_percent=memory_percent,
                    disk_usage=disk_usage,
                    active_agents=len(self.active_agents)
                )

                # Agent performance analysis
                for agent_name in self.active_agents:
                    self._analyze_agent_performance(agent_name)

                time.sleep(30)  # Update every 30 seconds
            except Exception as e:
                logger.error(f"Error monitoring performance: {e}")

    def _analyze_agent_performance(self, agent_name: str):
        """Analyze individual agent performance"""
        # Get recent events for this agent
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT duration_ms, success, event_type
                FROM ai_events
                WHERE agent_name = ?
                AND timestamp > datetime('now', '-1 hour')
                AND duration_ms IS NOT NULL
            """, (agent_name,))

            events = cursor.fetchall()

            if events:
                durations = [e[0] for e in events if e[0] is not None]
                success_rate = sum(1 for e in events if e[1]) / len(events) * 100
                avg_duration = sum(durations) / len(durations) if durations else 0

                # Store performance metrics
                conn.execute("""
                    INSERT INTO performance_metrics
                    (id, timestamp, agent_name, metric_type, metric_value, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    self._generate_event_id(agent_name, "performance", "metrics"),
                    datetime.now().isoformat(),
                    agent_name,
                    "performance_summary",
                    success_rate,
                    json.dumps({
                        "avg_duration_ms": avg_duration,
                        "success_rate": success_rate,
                        "total_events": len(events),
                        "event_types": list(set(e[2] for e in events))
                    })
                ))

    def _monitor_file_system(self):
        """Monitor file system for AI-related changes"""
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler

            class AIFileHandler(FileSystemEventHandler):
                def __init__(self, monitor):
                    self.monitor = monitor

                def on_modified(self, event):
                    if not event.is_directory:
                        self.monitor.log_file_change(event.src_path, "modified")

                def on_created(self, event):
                    if not event.is_directory:
                        self.monitor.log_file_change(event.src_path, "created")

                def on_deleted(self, event):
                    if not event.is_directory:
                        self.monitor.log_file_change(event.src_path, "deleted")

            observer = Observer()
            observer.schedule(AIFileHandler(self), str(self.workspace_root), recursive=True)
            observer.start()

            while self.is_monitoring:
                time.sleep(1)

            observer.stop()
            observer.join()

        except ImportError:
            logger.warning("Watchdog not available. File system monitoring disabled.")

    def _discover_agents(self):
        """Discover active AI agents in the system"""
        while self.is_monitoring:
            try:
                # Look for Python processes that might be AI agents
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        cmdline = proc.info['cmdline']
                        if cmdline and any('ai' in arg.lower() or 'agent' in arg.lower()
                                         for arg in cmdline):
                            agent_name = f"Process_{proc.info['pid']}"
                            if agent_name not in self.active_agents:
                                self.log_system_event(
                                    "agent_discovered",
                                    f"New AI agent process discovered: {proc.info['name']}",
                                    pid=proc.info['pid'],
                                    cmdline=cmdline
                                )
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass

                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error discovering agents: {e}")

    def _generate_periodic_reports(self):
        """Generate periodic summary reports"""
        while self.is_monitoring:
            try:
                # Generate hourly report
                self.generate_activity_report(hours=1, save_to_file=True)
                time.sleep(3600)  # Wait 1 hour
            except Exception as e:
                logger.error(f"Error generating periodic reports: {e}")

    def generate_activity_report(self, hours: int = 24, save_to_file: bool = False) -> Dict[str, Any]:
        """Generate comprehensive activity report"""
        since = (datetime.now() - timedelta(hours=hours)).isoformat()

        with sqlite3.connect(self.db_path) as conn:
            # Get all events in time period
            cursor = conn.execute("""
                SELECT * FROM ai_events
                WHERE timestamp > ?
                ORDER BY timestamp DESC
            """, (since,))

            events = cursor.fetchall()

            # Generate comprehensive report
            report = {
                "report_generated": datetime.now().isoformat(),
                "time_period_hours": hours,
                "total_events": len(events),
                "active_agents": list(self.active_agents),
                "event_types": self._analyze_event_types(events),
                "agent_performance": self._analyze_agent_performance_summary(events),
                "file_changes": self._analyze_file_changes(events),
                "communication_patterns": self._analyze_communications(),
                "error_analysis": self._analyze_errors(events),
                "trends": self._analyze_trends(events)
            }

            if save_to_file:
                report_file = self.monitoring_dir / 'reports' / f'activity_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                with open(report_file, 'w') as f:
                    json.dump(report, f, indent=2)
                logger.info(f"📊 Activity report saved: {report_file}")

            return report

    def get_real_time_dashboard_data(self) -> Dict[str, Any]:
        """Get data for real-time dashboard"""
        return {
            "timestamp": datetime.now().isoformat(),
            "active_agents": list(self.active_agents),
            "recent_events": self._get_recent_events(20),
            "system_health": self._get_system_health(),
            "performance_summary": self._get_performance_summary(),
            "agent_relationships": dict(self.agent_relationships)
        }

    def _get_recent_events(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent events for dashboard"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT agent_name, event_type, description, timestamp, success
                FROM ai_events
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))

            return [
                {
                    "agent_name": row[0],
                    "event_type": row[1],
                    "description": row[2],
                    "timestamp": row[3],
                    "success": row[4]
                }
                for row in cursor.fetchall()
            ]

    def get_recent_activities(self, limit: int = 100) -> List[AIEvent]:
        """Get recent AI activities"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM ai_events
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))

            events = []
            for row in cursor.fetchall():
                event = AIEvent(
                    id=row[0],
                    timestamp=row[1],
                    agent_name=row[2],
                    event_type=row[3],
                    description=row[4],
                    details=json.loads(row[5]),
                    file_path=row[6],
                    line_numbers=json.loads(row[7]) if row[7] else None,
                    stack_trace=row[8],
                    parent_event_id=row[9],
                    child_event_ids=json.loads(row[10]) if row[10] else [],
                    duration_ms=row[11],
                    success=row[12],
                    confidence=row[13],
                    impact_score=row[14],
                    tags=json.loads(row[15]) if row[15] else [],
                    metadata=json.loads(row[16]) if row[16] else {}
                )
                events.append(event)

            return events

    def get_agent_activities(self, agent_name: str, limit: int = 50) -> List[AIEvent]:
        """Get activities for a specific agent"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM ai_events
                WHERE agent_name = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (agent_name, limit))

            events = []
            for row in cursor.fetchall():
                event = AIEvent(
                    id=row[0],
                    timestamp=row[1],
                    agent_name=row[2],
                    event_type=row[3],
                    description=row[4],
                    details=json.loads(row[5]),
                    file_path=row[6],
                    line_numbers=json.loads(row[7]) if row[7] else None,
                    stack_trace=row[8],
                    parent_event_id=row[9],
                    child_event_ids=json.loads(row[10]) if row[10] else [],
                    duration_ms=row[11],
                    success=row[12],
                    confidence=row[13],
                    impact_score=row[14],
                    tags=json.loads(row[15]) if row[15] else [],
                    metadata=json.loads(row[16]) if row[16] else {}
                )
                events.append(event)

            return events

    def stop_monitoring(self):
        """Stop all monitoring"""
        self.is_monitoring = False
        self.log_system_event("monitor_stopped", "Universal AI monitoring stopped")
        logger.info("🛑 Universal AI Monitor stopped")

    def _generate_event_id(self, agent_name: str, event_type: str, description: str) -> str:
        """Generate unique event ID"""
        content = f"{agent_name}:{event_type}:{description}:{time.time()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _analyze_event_types(self, events) -> Dict[str, int]:
        """Analyze event type distribution"""
        type_counts = defaultdict(int)
        for event in events:
            type_counts[event[3]] += 1  # event_type is at index 3
        return dict(type_counts)

    def _analyze_agent_performance_summary(self, events) -> Dict[str, Dict[str, Any]]:
        """Analyze agent performance from events"""
        agent_stats = defaultdict(lambda: {"count": 0, "success": 0, "durations": []})

        for event in events:
            agent_name = event[2]
            success = event[12]
            duration = event[11]

            agent_stats[agent_name]["count"] += 1
            if success:
                agent_stats[agent_name]["success"] += 1
            if duration:
                agent_stats[agent_name]["durations"].append(duration)

        summary = {}
        for agent, stats in agent_stats.items():
            summary[agent] = {
                "total_events": stats["count"],
                "success_rate": (stats["success"] / stats["count"] * 100) if stats["count"] > 0 else 0,
                "avg_duration_ms": sum(stats["durations"]) / len(stats["durations"]) if stats["durations"] else 0
            }

        return summary

    def _analyze_file_changes(self, events) -> Dict[str, Any]:
        """Analyze file change patterns"""
        file_events = [e for e in events if e[3] == "file_change"]  # event_type

        change_types = defaultdict(int)
        file_extensions = defaultdict(int)

        for event in file_events:
            details = json.loads(event[5])  # details
            change_types[details.get("change_type", "unknown")] += 1
            ext = details.get("file_extension", "")
            if ext:
                file_extensions[ext] += 1

        return {
            "total_changes": len(file_events),
            "change_types": dict(change_types),
            "file_extensions": dict(file_extensions)
        }

    def _analyze_communications(self) -> Dict[str, Any]:
        """Analyze agent communication patterns"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT source_agent, target_agent, interaction_type, COUNT(*)
                FROM agent_interactions
                WHERE timestamp > datetime('now', '-24 hours')
                GROUP BY source_agent, target_agent, interaction_type
            """)

            communications = cursor.fetchall()

            return {
                "total_interactions": len(communications),
                "agent_pairs": [
                    {
                        "source": row[0],
                        "target": row[1],
                        "type": row[2],
                        "count": row[3]
                    }
                    for row in communications
                ]
            }

    def _analyze_errors(self, events) -> Dict[str, Any]:
        """Analyze error patterns"""
        error_events = [e for e in events if e[3] == "error"]

        error_types = defaultdict(int)
        agent_errors = defaultdict(int)

        for event in error_events:
            details = json.loads(event[5])
            error_types[details.get("error_type", "Unknown")] += 1
            agent_errors[event[2]] += 1  # agent_name

        return {
            "total_errors": len(error_events),
            "error_types": dict(error_types),
            "agents_with_errors": dict(agent_errors)
        }

    def _analyze_trends(self, events) -> Dict[str, Any]:
        """Analyze activity trends"""
        # Group events by hour
        hourly_activity = defaultdict(int)

        for event in events:
            timestamp = datetime.fromisoformat(event[1].replace('Z', '+00:00'))
            hour_key = timestamp.strftime("%Y-%m-%d %H:00")
            hourly_activity[hour_key] += 1

        return {
            "hourly_activity": dict(hourly_activity),
            "peak_hour": max(hourly_activity.items(), key=lambda x: x[1])[0] if hourly_activity else None,
            "activity_trend": "increasing" if len(hourly_activity) > 1 and
                            list(hourly_activity.values())[-1] > list(hourly_activity.values())[0] else "stable"
        }

    def _get_system_health(self) -> Dict[str, Any]:
        """Get system health metrics"""
        return {
            "uptime_hours": (datetime.now() - self.start_time).total_seconds() / 3600,
            "queue_size": len(self.event_queue),
            "cache_size": len(self.event_cache),
            "active_agents": len(self.active_agents),
            "monitoring_status": "healthy" if self.is_monitoring else "stopped"
        }

    def _get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT agent_name, COUNT(*) as event_count,
                       AVG(CASE WHEN success = 1 THEN 1.0 ELSE 0.0 END) as success_rate,
                       AVG(duration_ms) as avg_duration
                FROM ai_events
                WHERE timestamp > datetime('now', '-1 hour')
                GROUP BY agent_name
            """)

            return {
                row[0]: {
                    "event_count": row[1],
                    "success_rate": row[2] * 100 if row[2] else 0,
                    "avg_duration_ms": row[3] if row[3] else 0
                }
                for row in cursor.fetchall()
            }


# Global monitor instance
_universal_monitor = None

def get_universal_monitor() -> UniversalAIMonitor:
    """Get or create the global universal monitor instance"""
    global _universal_monitor
    if _universal_monitor is None:
        workspace_root = Path(__file__).parent.parent.parent
        _universal_monitor = UniversalAIMonitor(workspace_root)
    return _universal_monitor

# Convenience functions for easy integration
def log_ai_event(agent_name: str, event_type: str, description: str, **kwargs):
    """Convenience function to log AI events"""
    return get_universal_monitor().log_ai_event(agent_name, event_type, description, **kwargs)

def log_ai_thought(agent_name: str, thought: str, **context):
    """Convenience function to log AI thoughts"""
    return get_universal_monitor().log_ai_thought(agent_name, thought, context)

def log_ai_decision(agent_name: str, decision: str, reasoning: str, options: List[str] = None, confidence: float = None):
    """Convenience function to log AI decisions"""
    return get_universal_monitor().log_ai_decision(agent_name, decision, reasoning, options, confidence)

@contextmanager
def track_ai_action(agent_name: str, action: str, **details):
    """Context manager for tracking AI actions"""
    monitor = get_universal_monitor()
    event_id, start_time = monitor.log_ai_action(agent_name, action, **details)

    try:
        yield event_id
        monitor.complete_ai_action(event_id, start_time, success=True)
    except Exception as e:
        monitor.complete_ai_action(event_id, start_time, success=False, result=str(e))
        monitor.log_error(agent_name, e, f"During action: {action}")
        raise


if __name__ == "__main__":
    # Test the universal monitor
    monitor = get_universal_monitor()

    # Test various event types
    monitor.log_ai_thought("TestAgent", "Analyzing repository structure for optimization opportunities")
    monitor.log_ai_decision("TestAgent", "Reorganize repository", "Current structure is inefficient",
                           ["reorganize", "keep_current", "partial_cleanup"], confidence=0.85)

    with track_ai_action("TestAgent", "file_analysis") as action_id:
        time.sleep(0.1)  # Simulate work

    monitor.log_agent_communication("TestAgent", "FileSystemMonitor", "Request file scan", "request")

    # Generate test report
    report = monitor.generate_activity_report(hours=1)
    print("📊 Generated test report with", report["total_events"], "events")

    print("🔍 Universal AI Monitor test completed successfully!")
