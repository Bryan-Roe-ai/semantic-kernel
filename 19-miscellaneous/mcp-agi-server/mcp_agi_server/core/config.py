"""
Core configuration management for MCP AGI Server
"""

import json
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

@dataclass
class ServerConfig:
    """Server configuration"""
    host: str = "localhost"
    port: int = 8080
    max_concurrent_requests: int = 100
    request_timeout: int = 300
    enable_cors: bool = True
    ssl_cert: Optional[str] = None
    ssl_key: Optional[str] = None

@dataclass
class AGIFeatures:
    """AGI-specific feature configuration"""
    enable_autonomous_mode: bool = True
    max_reasoning_depth: int = 10
    learning_rate: float = 0.1
    enable_self_reflection: bool = True
    enable_metacognition: bool = True
    enable_creative_thinking: bool = True
    enable_emotional_intelligence: bool = False
    autonomous_learning_threshold: float = 0.8
    creativity_temperature: float = 0.7
    enable_goal_generation: bool = True
    max_concurrent_goals: int = 5

@dataclass
class ReasoningConfig:
    """Reasoning engine configuration"""
    default_reasoning_mode: str = "mixed"  # deductive, inductive, abductive, mixed
    max_inference_steps: int = 50
    confidence_threshold: float = 0.7
    enable_chain_of_thought: bool = True
    enable_tree_of_thought: bool = True
    enable_analogical_reasoning: bool = True
    working_memory_size: int = 100
    long_term_memory_size: int = 10000
    reasoning_timeout: int = 120

@dataclass
class MemoryConfig:
    """Memory system configuration"""
    episodic_memory_size: int = 1000
    semantic_memory_size: int = 10000
    working_memory_size: int = 50
    knowledge_graph_max_nodes: int = 100000
    vector_embedding_size: int = 768
    similarity_threshold: float = 0.8
    memory_consolidation_interval: int = 3600
    enable_forgetting: bool = True
    forgetting_decay_rate: float = 0.01

@dataclass
class SafetyConfig:
    """Safety and security configuration"""
    enable_sandboxing: bool = True
    enable_strict_mode: bool = False
    max_execution_time: int = 30
    max_memory_mb: int = 512
    max_cpu_percent: float = 80.0
    max_disk_io_mb: int = 100
    allowed_modules: List[str] = field(default_factory=lambda: [
        "math", "json", "datetime", "random", "string", "re",
        "collections", "itertools", "functools", "operator"
    ])
    blocked_modules: List[str] = field(default_factory=lambda: [
        "os", "sys", "subprocess", "socket", "urllib", "requests",
        "eval", "exec", "compile", "__import__"
    ])
    allowed_file_extensions: List[str] = field(default_factory=lambda: [
        ".txt", ".json", ".csv", ".py", ".md", ".yaml", ".yml"
    ])
    max_file_size_mb: int = 10
    enable_network_access: bool = False
    allowed_domains: List[str] = field(default_factory=list)

@dataclass
class ToolsConfig:
    """Tools configuration"""
    enable_code_execution: bool = True
    enable_web_search: bool = True
    enable_file_operations: bool = True
    enable_system_info: bool = True
    enable_image_processing: bool = False
    enable_audio_processing: bool = False
    enable_data_analysis: bool = True
    max_tool_execution_time: int = 60
    tool_result_max_size_mb: int = 50

@dataclass
class LearningConfig:
    """Learning system configuration"""
    enable_online_learning: bool = True
    enable_transfer_learning: bool = True
    enable_meta_learning: bool = True
    learning_batch_size: int = 32
    learning_epochs: int = 10
    validation_split: float = 0.2
    early_stopping_patience: int = 5
    learning_rate_decay: float = 0.95
    regularization_strength: float = 0.01

@dataclass
class MonitoringConfig:
    """Monitoring and metrics configuration"""
    enable_health_checks: bool = True
    health_check_interval: int = 30
    enable_performance_metrics: bool = True
    metrics_collection_interval: int = 10
    enable_audit_logging: bool = True
    log_retention_days: int = 30
    enable_prometheus_metrics: bool = False
    prometheus_port: int = 9090

@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = "logs/mcp_agi_server.log"
    max_file_size_mb: int = 100
    backup_count: int = 5
    enable_console_logging: bool = True
    enable_structured_logging: bool = True

@dataclass
class AGIConfig:
    """Complete AGI configuration"""
    server: ServerConfig = field(default_factory=ServerConfig)
    agi: AGIFeatures = field(default_factory=AGIFeatures)
    reasoning: ReasoningConfig = field(default_factory=ReasoningConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    tools: ToolsConfig = field(default_factory=ToolsConfig)
    learning: LearningConfig = field(default_factory=LearningConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    def save(self, path: Union[str, Path]) -> None:
        """Save configuration to file"""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    def validate(self) -> bool:
        """Validate configuration"""
        try:
            # Validate server config
            if not (1 <= self.server.port <= 65535):
                raise ValueError(f"Invalid port: {self.server.port}")

            # Validate AGI config
            if not (0.0 <= self.agi.learning_rate <= 1.0):
                raise ValueError(f"Invalid learning rate: {self.agi.learning_rate}")

            # Validate reasoning config
            if self.reasoning.confidence_threshold < 0.0 or self.reasoning.confidence_threshold > 1.0:
                raise ValueError(f"Invalid confidence threshold: {self.reasoning.confidence_threshold}")

            # Validate safety config
            if self.safety.max_execution_time <= 0:
                raise ValueError(f"Invalid max execution time: {self.safety.max_execution_time}")

            # Validate memory config
            if self.memory.similarity_threshold < 0.0 or self.memory.similarity_threshold > 1.0:
                raise ValueError(f"Invalid similarity threshold: {self.memory.similarity_threshold}")

            return True

        except Exception as e:
            logging.error(f"Configuration validation failed: {e}")
            return False

def load_config(config_path: Union[str, Path]) -> AGIConfig:
    """Load configuration from file"""
    config_path = Path(config_path)

    if not config_path.exists():
        logging.warning(f"Config file {config_path} not found, using defaults")
        return AGIConfig()

    try:
        with open(config_path, 'r') as f:
            data = json.load(f)

        # Create config objects from dict data
        config = AGIConfig()

        if 'server' in data:
            config.server = ServerConfig(**data['server'])
        if 'agi' in data:
            config.agi = AGIFeatures(**data['agi'])
        if 'reasoning' in data:
            config.reasoning = ReasoningConfig(**data['reasoning'])
        if 'memory' in data:
            config.memory = MemoryConfig(**data['memory'])
        if 'safety' in data:
            config.safety = SafetyConfig(**data['safety'])
        if 'tools' in data:
            config.tools = ToolsConfig(**data['tools'])
        if 'learning' in data:
            config.learning = LearningConfig(**data['learning'])
        if 'monitoring' in data:
            config.monitoring = MonitoringConfig(**data['monitoring'])
        if 'logging' in data:
            config.logging = LoggingConfig(**data['logging'])

        # Validate configuration
        if not config.validate():
            raise ValueError("Configuration validation failed")

        return config

    except Exception as e:
        logging.error(f"Failed to load config from {config_path}: {e}")
        logging.info("Using default configuration")
        return AGIConfig()

def create_default_config() -> AGIConfig:
    """Create default configuration"""
    return AGIConfig()

def create_production_config() -> AGIConfig:
    """Create production-ready configuration"""
    config = AGIConfig()

    # Production server settings
    config.server.max_concurrent_requests = 1000
    config.server.request_timeout = 600

    # Enhanced safety for production
    config.safety.enable_strict_mode = True
    config.safety.max_execution_time = 15
    config.safety.max_memory_mb = 256
    config.safety.enable_network_access = False

    # Production monitoring
    config.monitoring.enable_prometheus_metrics = True
    config.monitoring.health_check_interval = 15
    config.monitoring.metrics_collection_interval = 5

    # Production logging
    config.logging.level = "WARNING"
    config.logging.enable_structured_logging = True
    config.logging.max_file_size_mb = 500
    config.logging.backup_count = 10

    return config

def create_development_config() -> AGIConfig:
    """Create development configuration"""
    config = AGIConfig()

    # Development server settings
    config.server.max_concurrent_requests = 10
    config.server.enable_cors = True

    # Relaxed safety for development
    config.safety.enable_strict_mode = False
    config.safety.max_execution_time = 60
    config.safety.max_memory_mb = 1024
    config.safety.enable_network_access = True

    # Development logging
    config.logging.level = "DEBUG"
    config.logging.enable_console_logging = True

    # Enable all features for development
    config.agi.enable_autonomous_mode = True
    config.agi.enable_metacognition = True
    config.agi.enable_creative_thinking = True

    return config
