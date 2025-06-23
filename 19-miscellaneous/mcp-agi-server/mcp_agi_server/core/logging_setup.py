"""
Logging setup for MCP AGI Server
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
import json
from datetime import datetime

from .config import LoggingConfig

class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "user_id"):
            log_entry["user_id"] = record.user_id
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        if hasattr(record, "tool_name"):
            log_entry["tool_name"] = record.tool_name
        if hasattr(record, "execution_time"):
            log_entry["execution_time"] = record.execution_time

        return json.dumps(log_entry, default=str)

class AGILogFilter(logging.Filter):
    """Custom filter for AGI-specific logs"""

    def filter(self, record: logging.LogRecord) -> bool:
        # Add contextual information
        if not hasattr(record, "component"):
            record.component = "unknown"

        # Filter out sensitive information
        message = record.getMessage()
        sensitive_keywords = ["password", "token", "key", "secret"]

        for keyword in sensitive_keywords:
            if keyword.lower() in message.lower():
                record.msg = message.replace(keyword, "[REDACTED]")
                break

        return True

def setup_logging(level: str = "INFO", config: Optional[LoggingConfig] = None) -> None:
    """Setup comprehensive logging system"""

    if config is None:
        config = LoggingConfig()

    # Create logs directory if needed
    if config.file_path:
        log_path = Path(config.file_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)

    # Clear existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    # Set level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    root_logger.setLevel(numeric_level)

    # Create formatters
    if config.enable_structured_logging:
        formatter = StructuredFormatter()
    else:
        formatter = logging.Formatter(config.format)

    # Console handler
    if config.enable_console_logging:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        console_handler.addFilter(AGILogFilter())
        root_logger.addHandler(console_handler)

    # File handler with rotation
    if config.file_path:
        file_handler = logging.handlers.RotatingFileHandler(
            config.file_path,
            maxBytes=config.max_file_size_mb * 1024 * 1024,
            backupCount=config.backup_count
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        file_handler.addFilter(AGILogFilter())
        root_logger.addHandler(file_handler)

    # Create specialized loggers
    setup_component_loggers(numeric_level, formatter)

    logging.info("Logging system initialized")

def setup_component_loggers(level: int, formatter: logging.Formatter) -> None:
    """Setup component-specific loggers"""

    components = [
        "mcp_agi_server.core",
        "mcp_agi_server.reasoning",
        "mcp_agi_server.memory",
        "mcp_agi_server.tools",
        "mcp_agi_server.safety",
        "mcp_agi_server.monitoring",
        "mcp_agi_server.learning"
    ]

    for component in components:
        logger = logging.getLogger(component)
        logger.setLevel(level)
        logger.propagate = True  # Let root logger handle the actual output

def get_logger(name: str) -> logging.Logger:
    """Get a logger with AGI-specific configuration"""
    return logging.getLogger(f"mcp_agi_server.{name}")

class PerformanceLogger:
    """Logger for performance metrics"""

    def __init__(self):
        self.logger = get_logger("performance")

    def log_tool_execution(self, tool_name: str, execution_time: float,
                          success: bool, resource_usage: dict = None) -> None:
        """Log tool execution metrics"""
        extra = {
            "tool_name": tool_name,
            "execution_time": execution_time,
            "success": success
        }

        if resource_usage:
            extra.update(resource_usage)

        level = logging.INFO if success else logging.WARNING
        self.logger.log(level, f"Tool {tool_name} executed in {execution_time:.3f}s", extra=extra)

    def log_reasoning_step(self, step_type: str, duration: float,
                          confidence: float, tokens_used: int = None) -> None:
        """Log reasoning step metrics"""
        extra = {
            "step_type": step_type,
            "duration": duration,
            "confidence": confidence
        }

        if tokens_used:
            extra["tokens_used"] = tokens_used

        self.logger.info(f"Reasoning step {step_type} completed", extra=extra)

    def log_memory_operation(self, operation: str, duration: float,
                           items_affected: int, success: bool) -> None:
        """Log memory operation metrics"""
        extra = {
            "operation": operation,
            "duration": duration,
            "items_affected": items_affected,
            "success": success
        }

        level = logging.INFO if success else logging.ERROR
        self.logger.log(level, f"Memory operation {operation} completed", extra=extra)

class SecurityLogger:
    """Logger for security events"""

    def __init__(self):
        self.logger = get_logger("security")

    def log_access_attempt(self, user_id: str, resource: str,
                          granted: bool, reason: str = None) -> None:
        """Log access attempts"""
        extra = {
            "user_id": user_id,
            "resource": resource,
            "granted": granted
        }

        if reason:
            extra["reason"] = reason

        level = logging.INFO if granted else logging.WARNING
        self.logger.log(level, f"Access {'granted' if granted else 'denied'} to {resource}", extra=extra)

    def log_security_violation(self, violation_type: str, details: str,
                             user_id: str = None, severity: str = "medium") -> None:
        """Log security violations"""
        extra = {
            "violation_type": violation_type,
            "severity": severity
        }

        if user_id:
            extra["user_id"] = user_id

        self.logger.error(f"Security violation: {violation_type} - {details}", extra=extra)

    def log_sandbox_violation(self, violation_type: str, attempted_action: str,
                            blocked: bool, resource: str = None) -> None:
        """Log sandbox violations"""
        extra = {
            "violation_type": violation_type,
            "attempted_action": attempted_action,
            "blocked": blocked
        }

        if resource:
            extra["resource"] = resource

        level = logging.WARNING if blocked else logging.CRITICAL
        self.logger.log(level, f"Sandbox violation: {violation_type}", extra=extra)

class AuditLogger:
    """Logger for audit trails"""

    def __init__(self):
        self.logger = get_logger("audit")

    def log_user_action(self, user_id: str, action: str, resource: str = None,
                       request_id: str = None, result: str = "success") -> None:
        """Log user actions for audit trail"""
        extra = {
            "user_id": user_id,
            "action": action,
            "result": result
        }

        if resource:
            extra["resource"] = resource
        if request_id:
            extra["request_id"] = request_id

        self.logger.info(f"User action: {action}", extra=extra)

    def log_system_event(self, event_type: str, description: str,
                        component: str = None, data: dict = None) -> None:
        """Log system events"""
        extra = {
            "event_type": event_type
        }

        if component:
            extra["component"] = component
        if data:
            extra.update(data)

        self.logger.info(f"System event: {event_type} - {description}", extra=extra)

    def log_configuration_change(self, changed_by: str, section: str,
                               old_value: str, new_value: str) -> None:
        """Log configuration changes"""
        extra = {
            "changed_by": changed_by,
            "section": section,
            "old_value": old_value,
            "new_value": new_value
        }

        self.logger.warning(f"Configuration changed: {section}", extra=extra)

# Global logger instances
performance_logger = PerformanceLogger()
security_logger = SecurityLogger()
audit_logger = AuditLogger()
