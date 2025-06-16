#!/usr/bin/env python3
"""
MCP AGI Server - Advanced Model Context Protocol Server for AGI Applications

This is the main entry point for the MCP AGI Server, providing comprehensive
AGI capabilities through the Model Context Protocol.
"""

import argparse
import asyncio
import json
import logging
import signal
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Core MCP and AGI imports
from mcp_agi_server.core.server import MCPAGIServer
from mcp_agi_server.core.config import AGIConfig, load_config
from mcp_agi_server.core.logging_setup import setup_logging
from mcp_agi_server.safety.sandbox import SandboxManager
from mcp_agi_server.memory.knowledge_graph import KnowledgeGraph
from mcp_agi_server.reasoning.engine import ReasoningEngine
from mcp_agi_server.monitoring.health import HealthMonitor

class MCPAGIApplication:
    """Main application class for MCP AGI Server"""

    def __init__(self, config: AGIConfig):
        self.config = config
        self.server: Optional[MCPAGIServer] = None
        self.sandbox_manager: Optional[SandboxManager] = None
        self.knowledge_graph: Optional[KnowledgeGraph] = None
        self.reasoning_engine: Optional[ReasoningEngine] = None
        self.health_monitor: Optional[HealthMonitor] = None
        self.shutdown_event = asyncio.Event()

    async def initialize(self) -> bool:
        """Initialize all components"""
        try:
            logging.info("Initializing MCP AGI Server...")

            # Initialize core components
            self.sandbox_manager = SandboxManager(self.config.safety)
            await self.sandbox_manager.initialize()

            self.knowledge_graph = KnowledgeGraph(self.config.memory)
            await self.knowledge_graph.initialize()

            self.reasoning_engine = ReasoningEngine(
                self.config.reasoning,
                self.knowledge_graph
            )
            await self.reasoning_engine.initialize()

            self.health_monitor = HealthMonitor(self.config.monitoring)
            await self.health_monitor.start()

            # Initialize MCP server
            self.server = MCPAGIServer(
                config=self.config,
                sandbox_manager=self.sandbox_manager,
                knowledge_graph=self.knowledge_graph,
                reasoning_engine=self.reasoning_engine,
                health_monitor=self.health_monitor
            )

            await self.server.initialize()

            logging.info("MCP AGI Server initialized successfully")
            return True

        except Exception as e:
            logging.error(f"Failed to initialize MCP AGI Server: {e}")
            return False

    async def start(self) -> None:
        """Start the server"""
        try:
            if not self.server:
                raise RuntimeError("Server not initialized")

            logging.info(f"Starting MCP AGI Server on {self.config.server.host}:{self.config.server.port}")

            # Start the server
            await self.server.start()

            # Wait for shutdown signal
            await self.shutdown_event.wait()

        except Exception as e:
            logging.error(f"Error running server: {e}")
            raise

    async def shutdown(self) -> None:
        """Graceful shutdown"""
        try:
            logging.info("Shutting down MCP AGI Server...")

            # Stop components in reverse order
            if self.health_monitor:
                await self.health_monitor.stop()

            if self.server:
                await self.server.shutdown()

            if self.reasoning_engine:
                await self.reasoning_engine.shutdown()

            if self.knowledge_graph:
                await self.knowledge_graph.shutdown()

            if self.sandbox_manager:
                await self.sandbox_manager.cleanup()

            logging.info("MCP AGI Server shutdown complete")

        except Exception as e:
            logging.error(f"Error during shutdown: {e}")

    def signal_handler(self, signum: int, frame) -> None:
        """Handle shutdown signals"""
        logging.info(f"Received signal {signum}, initiating shutdown...")
        self.shutdown_event.set()

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="MCP AGI Server")
    parser.add_argument(
        "--config",
        type=Path,
        default="config/default.json",
        help="Configuration file path"
    )
    parser.add_argument(
        "--host",
        type=str,
        help="Server host (overrides config)"
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Server port (overrides config)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level"
    )
    parser.add_argument(
        "--enable-autonomous",
        action="store_true",
        help="Enable autonomous mode"
    )
    parser.add_argument(
        "--safe-mode",
        action="store_true",
        help="Run in safe mode (enhanced restrictions)"
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run performance benchmarks"
    )

    args = parser.parse_args()

    try:
        # Load configuration
        config = load_config(args.config)

        # Override with command line arguments
        if args.host:
            config.server.host = args.host
        if args.port:
            config.server.port = args.port
        if args.enable_autonomous:
            config.agi.enable_autonomous_mode = True
        if args.safe_mode:
            config.safety.enable_strict_mode = True
            config.safety.max_execution_time = 10
            config.safety.max_memory_mb = 256

        # Setup logging
        setup_logging(args.log_level, config.logging)

        # Create and start application
        app = MCPAGIApplication(config)

        # Setup signal handlers
        signal.signal(signal.SIGINT, app.signal_handler)
        signal.signal(signal.SIGTERM, app.signal_handler)

        # Initialize components
        if not await app.initialize():
            logging.error("Failed to initialize application")
            return 1

        # Run benchmarks if requested
        if args.benchmark:
            from mcp_agi_server.utils.benchmark import run_benchmarks
            await run_benchmarks(app.server)
            return 0

        # Start server
        try:
            await app.start()
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received")
        finally:
            await app.shutdown()

        return 0

    except Exception as e:
        logging.error(f"Fatal error: {e}")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logging.info("Application interrupted")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        sys.exit(1)
