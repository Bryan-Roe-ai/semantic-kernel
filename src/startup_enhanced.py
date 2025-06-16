#!/usr/bin/env python
"""
Enhanced Startup Script with AutoMode Integration
Provides reliable long-running operation with auto-recovery and monitoring.
"""

import os
import sys
import time
import json
import asyncio
import logging
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

# Add the current directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

try:
    from auto_mode_enhanced import EnhancedAutoMode, AutoModeConfig, create_automode_config
except ImportError:
    print("Enhanced AutoMode not found. Please ensure auto_mode_enhanced.py is in the same directory.")
    sys.exit(1)


class ApplicationManager:
    """Manages the complete AI application lifecycle"""

    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path(__file__).parent
        self.automode = None
        self.config = None

    def setup_environment(self) -> bool:
        """Setup the environment for long-running operation"""
        try:
            # Ensure required directories exist
            required_dirs = [
                self.base_dir / "logs",
                self.base_dir / "temp",
                self.base_dir / "uploads",
                self.base_dir / "plugins",
                self.base_dir / ".automode_state"
            ]

            for dir_path in required_dirs:
                dir_path.mkdir(exist_ok=True)

            # Create default config if not exists
            config_file = self.base_dir / "auto_mode_config.json"
            if not config_file.exists():
                default_config = create_automode_config()
                with open(config_file, 'w') as f:
                    json.dump(default_config.__dict__, f, indent=2)
                print(f"Created default config at {config_file}")

            # Setup basic logging
            log_file = self.base_dir / "logs" / "startup.log"
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_file),
                    logging.StreamHandler()
                ]
            )

            logging.info("Environment setup completed")
            return True

        except Exception as e:
            print(f"Failed to setup environment: {e}")
            return False

    def check_dependencies(self) -> bool:
        """Check if all required dependencies are available"""
        try:
            # Check Python version
            if sys.version_info < (3, 8):
                logging.error("Python 3.8+ is required")
                return False

            # Check for required Python packages
            required_packages = [
                'psutil', 'requests', 'fastapi', 'uvicorn'
            ]

            missing_packages = []
            for package in required_packages:
                try:
                    __import__(package)
                except ImportError:
                    missing_packages.append(package)

            if missing_packages:
                logging.warning(f"Missing packages: {missing_packages}")

                # Try to install missing packages
                for package in missing_packages:
                    try:
                        subprocess.check_call([
                            sys.executable, "-m", "pip", "install", package
                        ])
                        logging.info(f"Installed {package}")
                    except subprocess.CalledProcessError:
                        logging.error(f"Failed to install {package}")
                        return False

            # Check for optional dependencies
            optional_packages = {
                'watchdog': 'for file watching',
                'redis': 'for advanced caching',
                'prometheus_client': 'for metrics export'
            }

            for package, purpose in optional_packages.items():
                try:
                    __import__(package)
                    logging.info(f"Optional package {package} available")
                except ImportError:
                    logging.info(f"Optional package {package} not available ({purpose})")

            logging.info("Dependency check completed")
            return True

        except Exception as e:
            logging.error(f"Error checking dependencies: {e}")
            return False

    def check_services(self) -> Dict[str, bool]:
        """Check the status of external services"""
        services = {}

        # Check LM Studio
        try:
            import socket
            with socket.create_connection(('localhost', 1234), timeout=5):
                services['lm_studio'] = True
                logging.info("LM Studio API is available")
        except:
            services['lm_studio'] = False
            logging.warning("LM Studio API is not available")

        # Check Redis if available
        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, socket_timeout=5)
            r.ping()
            services['redis'] = True
            logging.info("Redis is available")
        except:
            services['redis'] = False
            logging.info("Redis is not available (optional)")

        # Check if backend is already running
        try:
            import requests
            response = requests.get('http://localhost:8000/health', timeout=5)
            services['backend'] = response.status_code == 200
            if services['backend']:
                logging.info("Backend is already running")
            else:
                logging.warning("Backend is not responding properly")
        except:
            services['backend'] = False
            logging.info("Backend is not running")

        return services

    async def start_application(self, config_file: Path = None) -> bool:
        """Start the application with enhanced AutoMode"""
        try:
            # Load configuration
            self.config = create_automode_config(config_file)

            # Create enhanced AutoMode instance
            self.automode = EnhancedAutoMode(self.config, self.base_dir)

            # Start backend if not already running
            services = self.check_services()
            if not services.get('backend', False):
                backend_file = self.base_dir / "backend.py"
                if backend_file.exists():
                    logging.info("Starting backend server...")
                    success = await self.automode.start_managed_process(
                        "backend",
                        [sys.executable, str(backend_file)]
                    )
                    if success:
                        logging.info("Backend started successfully")
                    else:
                        logging.error("Failed to start backend")
                        return False
                else:
                    logging.warning("No backend.py found")

            # Start additional services
            await self._start_additional_services()

            logging.info("Application startup completed")
            return True

        except Exception as e:
            logging.error(f"Failed to start application: {e}")
            return False

    async def _start_additional_services(self) -> None:
        """Start additional services and monitoring"""
        try:
            # Start file watcher if watchdog is available
            try:
                import watchdog
                watcher_script = self.base_dir / "plugin_hotreload.py"
                if watcher_script.exists():
                    await self.automode.start_managed_process(
                        "file_watcher",
                        [sys.executable, str(watcher_script)]
                    )
                    logging.info("File watcher started")
            except ImportError:
                logging.info("Watchdog not available, skipping file watcher")

            # Start metrics exporter if prometheus_client is available
            try:
                import prometheus_client
                metrics_script = self.base_dir / "metrics_exporter.py"
                if metrics_script.exists():
                    await self.automode.start_managed_process(
                        "metrics_exporter",
                        [sys.executable, str(metrics_script)]
                    )
                    logging.info("Metrics exporter started")
            except ImportError:
                logging.info("Prometheus client not available, skipping metrics exporter")

        except Exception as e:
            logging.error(f"Error starting additional services: {e}")

    async def run_forever(self) -> None:
        """Run the application indefinitely with AutoMode"""
        if not self.automode:
            raise RuntimeError("Application not started")

        logging.info("Starting long-running mode...")
        await self.automode.run()

    async def shutdown(self) -> None:
        """Gracefully shutdown the application"""
        if self.automode:
            await self.automode.graceful_shutdown()
        logging.info("Application shutdown completed")


def create_startup_launcher() -> None:
    """Create a simple startup launcher script"""
    launcher_content = '''#!/usr/bin/env python
"""Simple launcher for enhanced AutoMode"""
import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from startup_enhanced import ApplicationManager

async def main():
    manager = ApplicationManager()

    # Setup environment
    if not manager.setup_environment():
        print("Failed to setup environment")
        return 1

    # Check dependencies
    if not manager.check_dependencies():
        print("Dependency check failed")
        return 1

    # Start application
    if not await manager.start_application():
        print("Failed to start application")
        return 1

    # Run forever
    await manager.run_forever()

    return 0

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\\nShutdown requested by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
'''

    launcher_file = Path(__file__).parent / "start_enhanced.py"
    with open(launcher_file, 'w') as f:
        f.write(launcher_content)

    # Make executable on Unix-like systems
    try:
        import stat
        launcher_file.chmod(launcher_file.stat().st_mode | stat.S_IEXEC)
    except:
        pass

    print(f"Created launcher at {launcher_file}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Enhanced Application Startup")
    parser.add_argument("--config", type=Path, help="Configuration file")
    parser.add_argument("--base-dir", type=Path, help="Base directory",
                       default=Path(__file__).parent)
    parser.add_argument("--create-launcher", action="store_true",
                       help="Create a simple launcher script")
    parser.add_argument("--check-only", action="store_true",
                       help="Only check dependencies and services")

    args = parser.parse_args()

    if args.create_launcher:
        create_startup_launcher()
        return

    # Create application manager
    manager = ApplicationManager(args.base_dir)

    # Setup environment
    if not manager.setup_environment():
        print("Failed to setup environment")
        sys.exit(1)

    # Check dependencies
    if not manager.check_dependencies():
        print("Dependency check failed")
        sys.exit(1)

    # Check services
    services = manager.check_services()
    print("Service Status:")
    for service, status in services.items():
        status_str = "✓ Available" if status else "✗ Not Available"
        print(f"  {service}: {status_str}")

    if args.check_only:
        return

    # Start application
    async def run_app():
        if not await manager.start_application(args.config):
            print("Failed to start application")
            return 1

        print("Application started successfully. Running in long-running mode...")
        print("Press Ctrl+C to shutdown gracefully")

        await manager.run_forever()
        return 0

    try:
        exit_code = asyncio.run(run_app())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
