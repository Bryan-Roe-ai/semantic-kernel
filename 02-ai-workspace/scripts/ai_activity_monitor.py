#!/usr/bin/env python3
"""
🤖 AI Activity Monitor
Comprehensive monitoring system for all AI actions, thoughts, and changes
"""

import json
import os
import time
import asyncio
import logging
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from contextlib import asynccontextmanager
import threading
import queue
import sqlite3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AIActivity:
    """Represents a single AI activity/action"""
    id: str
    timestamp: str
    agent_name: str
    activity_type: str  # 'action', 'thought', 'change', 'analysis', 'decision'
    description: str
    details: Dict[str, Any]
    file_path: Optional[str] = None
    line_numbers: Optional[List[int]] = None
    success: Optional[bool] = None
    duration_ms: Optional[float] = None
    parent_activity_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class ActivityDatabase:
    """SQLite database for storing AI activities"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize the database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ai_activities (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    agent_name TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    details TEXT NOT NULL,
                    file_path TEXT,
                    line_numbers TEXT,
                    success BOOLEAN,
                    duration_ms REAL,
                    parent_activity_id TEXT,
                    metadata TEXT,
                    FOREIGN KEY (parent_activity_id) REFERENCES ai_activities (id)
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON ai_activities (timestamp);
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_agent_name ON ai_activities (agent_name);
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_activity_type ON ai_activities (activity_type);
            """)

    def insert_activity(self, activity: AIActivity):
        """Insert a new activity into the database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO ai_activities
                (id, timestamp, agent_name, activity_type, description, details,
                 file_path, line_numbers, success, duration_ms, parent_activity_id, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                activity.id,
                activity.timestamp,
                activity.agent_name,
                activity.activity_type,
                activity.description,
                json.dumps(activity.details),
                activity.file_path,
                json.dumps(activity.line_numbers) if activity.line_numbers else None,
                activity.success,
                activity.duration_ms,
                activity.parent_activity_id,
                json.dumps(activity.metadata) if activity.metadata else None
            ))

    def get_activities(self,
                      agent_name: Optional[str] = None,
                      activity_type: Optional[str] = None,
                      since: Optional[str] = None,
                      limit: Optional[int] = None) -> List[AIActivity]:
        """Retrieve activities with filtering options"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            query = "SELECT * FROM ai_activities WHERE 1=1"
            params = []

            if agent_name:
                query += " AND agent_name = ?"
                params.append(agent_name)

            if activity_type:
                query += " AND activity_type = ?"
                params.append(activity_type)

            if since:
                query += " AND timestamp >= ?"
                params.append(since)

            query += " ORDER BY timestamp DESC"

            if limit:
                query += " LIMIT ?"
                params.append(limit)

            rows = conn.execute(query, params).fetchall()

            activities = []
            for row in rows:
                activity = AIActivity(
                    id=row['id'],
                    timestamp=row['timestamp'],
                    agent_name=row['agent_name'],
                    activity_type=row['activity_type'],
                    description=row['description'],
                    details=json.loads(row['details']),
                    file_path=row['file_path'],
                    line_numbers=json.loads(row['line_numbers']) if row['line_numbers'] else None,
                    success=row['success'],
                    duration_ms=row['duration_ms'],
                    parent_activity_id=row['parent_activity_id'],
                    metadata=json.loads(row['metadata']) if row['metadata'] else None
                )
                activities.append(activity)

            return activities

class FileChangeHandler(FileSystemEventHandler):
    """Handles file system changes and logs them as AI activities"""

    def __init__(self, monitor: 'AIActivityMonitor'):
        self.monitor = monitor
        self.ai_related_patterns = [
            '.py', '.js', '.ts', '.json', '.md', '.txt', '.yml', '.yaml',
            '.sh', '.bat', '.ps1', '.ipynb', '.cs', '.java', '.cpp', '.h'
        ]

    def on_modified(self, event):
        if not event.is_directory and self._is_ai_related(event.src_path):
            self.monitor.log_file_change(event.src_path, 'modified')

    def on_created(self, event):
        if not event.is_directory and self._is_ai_related(event.src_path):
            self.monitor.log_file_change(event.src_path, 'created')

    def on_deleted(self, event):
        if not event.is_directory and self._is_ai_related(event.src_path):
            self.monitor.log_file_change(event.src_path, 'deleted')

    def _is_ai_related(self, file_path: str) -> bool:
        """Check if file is AI-related"""
        return any(file_path.endswith(pattern) for pattern in self.ai_related_patterns)

class AIActivityMonitor:
    """Central monitoring system for all AI activities"""

    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.logs_dir = self.workspace_root / "02-ai-workspace" / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Database for structured storage
        self.db = ActivityDatabase(self.logs_dir / "ai_activities.db")

        # Activity queue for async processing
        self.activity_queue = queue.Queue()
        self.is_running = True

        # File watcher
        self.observer = Observer()
        self.file_handler = FileChangeHandler(self)

        # Start background processors
        self._start_background_processors()
        self._start_file_watcher()

    def _start_background_processors(self):
        """Start background threads for processing activities"""
        processor_thread = threading.Thread(target=self._process_activity_queue, daemon=True)
        processor_thread.start()

    def _start_file_watcher(self):
        """Start file system monitoring"""
        self.observer.schedule(self.file_handler, str(self.workspace_root), recursive=True)
        self.observer.start()

    def _process_activity_queue(self):
        """Background processor for activity queue"""
        while self.is_running:
            try:
                activity = self.activity_queue.get(timeout=1)
                self._persist_activity(activity)
                self.activity_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing activity: {e}")

    def _persist_activity(self, activity: AIActivity):
        """Persist activity to database and JSON logs"""
        # Store in database
        self.db.insert_activity(activity)

        # Also store in JSON for human readability
        json_file = self.logs_dir / f"activities_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        with open(json_file, 'a') as f:
            f.write(json.dumps(activity.to_dict()) + '\n')

    def log_activity(self,
                    agent_name: str,
                    activity_type: str,
                    description: str,
                    details: Dict[str, Any],
                    file_path: Optional[str] = None,
                    line_numbers: Optional[List[int]] = None,
                    success: Optional[bool] = None,
                    duration_ms: Optional[float] = None,
                    parent_activity_id: Optional[str] = None) -> str:
        """Log a new AI activity"""

        activity_id = self._generate_activity_id(agent_name, activity_type, description)

        activity = AIActivity(
            id=activity_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            agent_name=agent_name,
            activity_type=activity_type,
            description=description,
            details=details,
            file_path=file_path,
            line_numbers=line_numbers,
            success=success,
            duration_ms=duration_ms,
            parent_activity_id=parent_activity_id,
            metadata={
                "workspace_root": str(self.workspace_root),
                "python_process_id": os.getpid()
            }
        )

        # Queue for async processing
        self.activity_queue.put(activity)

        return activity_id

    def log_file_change(self, file_path: str, change_type: str):
        """Log file system changes"""
        rel_path = str(Path(file_path).relative_to(self.workspace_root))

        self.log_activity(
            agent_name="FileSystemMonitor",
            activity_type="change",
            description=f"File {change_type}: {rel_path}",
            details={
                "change_type": change_type,
                "file_path": rel_path,
                "absolute_path": file_path,
                "file_size": os.path.getsize(file_path) if os.path.exists(file_path) else 0
            }
        )

    def _generate_activity_id(self, agent_name: str, activity_type: str, description: str) -> str:
        """Generate unique activity ID"""
        content = f"{agent_name}:{activity_type}:{description}:{time.time()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    @asynccontextmanager
    async def track_action(self, agent_name: str, action_name: str, details: Dict[str, Any] = None):
        """Context manager for tracking AI actions with timing"""
        details = details or {}
        start_time = time.time()

        activity_id = self.log_activity(
            agent_name=agent_name,
            activity_type="action",
            description=f"Starting: {action_name}",
            details={**details, "status": "started"}
        )

        try:
            yield activity_id
            success = True
            final_details = {**details, "status": "completed"}
        except Exception as e:
            success = False
            final_details = {**details, "status": "failed", "error": str(e)}
            raise
        finally:
            duration_ms = (time.time() - start_time) * 1000

            self.log_activity(
                agent_name=agent_name,
                activity_type="action",
                description=f"Completed: {action_name}",
                details=final_details,
                success=success,
                duration_ms=duration_ms,
                parent_activity_id=activity_id
            )

    def log_thought(self, agent_name: str, thought: str, context: Dict[str, Any] = None):
        """Log AI agent thoughts/reasoning"""
        self.log_activity(
            agent_name=agent_name,
            activity_type="thought",
            description=thought,
            details=context or {}
        )

    def log_decision(self, agent_name: str, decision: str, reasoning: str, options: List[str] = None):
        """Log AI agent decisions"""
        self.log_activity(
            agent_name=agent_name,
            activity_type="decision",
            description=decision,
            details={
                "reasoning": reasoning,
                "options_considered": options or [],
                "decision_type": "automated"
            }
        )

    def log_analysis(self, agent_name: str, analysis_type: str, results: Dict[str, Any]):
        """Log AI analysis results"""
        self.log_activity(
            agent_name=agent_name,
            activity_type="analysis",
            description=f"Analysis: {analysis_type}",
            details=results
        )

    def get_recent_activities(self, limit: int = 100) -> List[AIActivity]:
        """Get recent activities"""
        return self.db.get_activities(limit=limit)

    def get_agent_activities(self, agent_name: str, limit: int = 50) -> List[AIActivity]:
        """Get activities for a specific agent"""
        return self.db.get_activities(agent_name=agent_name, limit=limit)

    def stop(self):
        """Stop the monitoring system"""
        self.is_running = False
        self.observer.stop()
        self.observer.join()

# Global monitor instance
_monitor_instance = None

def get_monitor() -> AIActivityMonitor:
    """Get or create the global monitor instance"""
    global _monitor_instance
    if _monitor_instance is None:
        workspace_root = Path(__file__).parent.parent.parent
        _monitor_instance = AIActivityMonitor(workspace_root)
    return _monitor_instance

def log_ai_activity(agent_name: str, activity_type: str, description: str, **kwargs) -> str:
    """Convenient function to log AI activity"""
    monitor = get_monitor()
    return monitor.log_activity(agent_name, activity_type, description, kwargs)

def log_ai_thought(agent_name: str, thought: str, **context):
    """Convenient function to log AI thoughts"""
    monitor = get_monitor()
    monitor.log_thought(agent_name, thought, context)

def log_ai_decision(agent_name: str, decision: str, reasoning: str, options: List[str] = None):
    """Convenient function to log AI decisions"""
    monitor = get_monitor()
    monitor.log_decision(agent_name, decision, reasoning, options)

def log_ai_analysis(agent_name: str, analysis_type: str, **results):
    """Convenient function to log AI analysis"""
    monitor = get_monitor()
    monitor.log_analysis(agent_name, analysis_type, results)

# Context manager for tracking actions
track_ai_action = lambda agent, action, **details: get_monitor().track_action(agent, action, details)

if __name__ == "__main__":
    # Example usage
    monitor = get_monitor()

    # Example activities
    monitor.log_thought("TestAgent", "Analyzing code quality patterns")
    monitor.log_decision("TestAgent", "Refactor function X", "High complexity detected", ["refactor", "ignore", "document"])
    monitor.log_analysis("TestAgent", "code_complexity", complexity_score=0.85, issues_found=3)

    print("Monitor started. Recent activities:")
    for activity in monitor.get_recent_activities(5):
        print(f"[{activity.timestamp}] {activity.agent_name}: {activity.description}")
