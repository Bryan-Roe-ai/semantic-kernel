#!/usr/bin/env python
"""
Ultra Enhanced Startup Script for Long-Running AutoMode
Provides maximum reliability and stability for 24/7 operation.
"""

import os
import sys
import time
import json
import asyncio
import logging
import argparse
import subprocess
import signal
from pathlib import Path
from typing import Dict, List, Optional

# Add the current directory to the path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from auto_mode_ultra_enhanced import UltraEnhancedAutoMode, UltraAutoModeConfig, create_ultra_automode_config
except ImportError as e:
    print(f"Ultra Enhanced AutoMode not found: {e}")
    print("Please ensure auto_mode_ultra_enhanced.py is in the same directory.")
    sys.exit(1)


class UltraApplicationManager:
    """Ultra comprehensive application lifecycle manager"""

    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path(__file__).parent
        self.automode = None
        self.config = None
        self.pre_flight_checks_passed = False

    def setup_ultra_environment(self) -> bool:
        """Setup ultra comprehensive environment"""
        try:
            logging.info("Setting up ultra enhanced environment...")

            # Create all required directories
            required_dirs = [
                self.base_dir / "logs",
                self.base_dir / "temp",
                self.base_dir / "uploads",
                self.base_dir / "plugins",
                self.base_dir / ".automode_ultra_state",
                self.base_dir / ".automode_ultra_state" / "backups",
                self.base_dir / "cache",
                self.base_dir / "monitoring",
                self.base_dir / "recovery"
            ]

            for dir_path in required_dirs:
                dir_path.mkdir(parents=True, exist_ok=True)
                # Set appropriate permissions
                os.chmod(dir_path, 0o755)

            # Create ultra config if not exists
            ultra_config_file = self.base_dir / "auto_mode_ultra_config.json"
            if not ultra_config_file.exists():
                default_config = create_ultra_automode_config()
                config_dict = {
                    field.name: getattr(default_config, field.name)
                    for field in default_config.__dataclass_fields__.values()
                }
                with open(ultra_config_file, 'w') as f:
                    json.dump(config_dict, f, indent=2, default=str)
                print(f"Created ultra config at {ultra_config_file}")

            # Setup ultra logging
            self._setup_ultra_startup_logging()

            # Check system compatibility
            if not self._check_system_compatibility():
                return False

            # Setup system optimizations
            self._apply_system_optimizations()

            logging.info("Ultra environment setup completed successfully")
            return True

        except Exception as e:
            print(f"Failed to setup ultra environment: {e}")
            return False

    def _setup_ultra_startup_logging(self) -> None:
        """Setup comprehensive startup logging"""
        log_dir = self.base_dir / "logs"
        startup_log = log_dir / "startup_ultra.log"

        # Create rotating file handler
        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler(
            startup_log, maxBytes=10*1024*1024, backupCount=5
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        ))

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))

        logging.basicConfig(
            level=logging.INFO,
            handlers=[file_handler, console_handler]
        )

        logging.info("Ultra startup logging initialized")

    def _check_system_compatibility(self) -> bool:
        """Check system compatibility for ultra enhanced mode"""
        try:
            # Python version check
            if sys.version_info < (3, 8):
                logging.error("Python 3.8+ is required for ultra enhanced mode")
                return False

            # Memory check
            try:
                import psutil
                memory = psutil.virtual_memory()
                if memory.total < 1 * 1024**3:  # 1 GB minimum
                    logging.warning(f"Low system memory: {memory.total / 1024**3:.1f} GB")
                else:
                    logging.info(f"System memory: {memory.total / 1024**3:.1f} GB")
            except ImportError:
                logging.error("psutil package required for system monitoring")
                return False

            # Disk space check
            disk_usage = psutil.disk_usage('/')
            free_gb = disk_usage.free / 1024**3
            if free_gb < 1:
                logging.error(f"Insufficient disk space: {free_gb:.1f} GB free")
                return False

            logging.info(f"Disk space available: {free_gb:.1f} GB")
            return True

        except Exception as e:
            logging.error(f"System compatibility check failed: {e}")
            return False

    def _apply_system_optimizations(self) -> None:
        """Apply system-level optimizations"""
        try:
            # Set process priority
            try:
                os.nice(-5)  # Higher priority (requires privileges)
                logging.info("Set higher process priority")
            except PermissionError:
                logging.info("Could not set higher priority (insufficient privileges)")
            except Exception as e:
                logging.warning(f"Failed to set process priority: {e}")

            # Set resource limits
            try:
                import resource

                # Increase file descriptor limit
                soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
                resource.setrlimit(resource.RLIMIT_NOFILE, (min(4096, hard), hard))
                logging.info(f"Set file descriptor limit to {min(4096, hard)}")

            except Exception as e:
                logging.warning(f"Failed to set resource limits: {e}")

        except Exception as e:
            logging.error(f"Error applying system optimizations: {e}")

    def comprehensive_dependency_check(self) -> Dict[str, bool]:
        """Ultra comprehensive dependency check"""
        results = {}

        try:
            # Required packages
            required_packages = {
                'psutil': 'System monitoring',
                'requests': 'HTTP requests',
                'asyncio': 'Async operations',
                'json': 'JSON handling',
                'pathlib': 'Path operations',
                'logging': 'Logging',
                'threading': 'Threading',
                'multiprocessing': 'Process management',
                'gc': 'Garbage collection',
                'weakref': 'Weak references',
                'resource': 'Resource limits',
                'signal': 'Signal handling'
            }

            for package, description in required_packages.items():
                try:
                    __import__(package)
                    results[package] = True
                    logging.info(f"✓ {package} ({description})")
                except ImportError:
                    results[package] = False
                    logging.error(f"✗ {package} ({description}) - MISSING")

            # Optional packages
            optional_packages = {
                'watchdog': 'File watching capabilities',
                'prometheus_client': 'Metrics export',
                'redis': 'Advanced caching',
                'uvicorn': 'ASGI server',
                'fastapi': 'Web framework'
            }

            for package, description in optional_packages.items():
                try:
                    __import__(package)
                    results[f"optional_{package}"] = True
                    logging.info(f"✓ {package} ({description}) - OPTIONAL")
                except ImportError:
                    results[f"optional_{package}"] = False
                    logging.info(f"○ {package} ({description}) - optional, not installed")

            # Auto-install missing critical packages
            missing_critical = [pkg for pkg, available in results.items()
                              if not available and not pkg.startswith('optional_')]

            if missing_critical:
                logging.warning(f"Attempting to install missing packages: {missing_critical}")
                for package in missing_critical:
                    try:
                        subprocess.check_call([
                            sys.executable, "-m", "pip", "install", package, "--quiet"
                        ])
                        logging.info(f"Successfully installed {package}")
                        results[package] = True
                    except subprocess.CalledProcessError:
                        logging.error(f"Failed to install {package}")

            return results

        except Exception as e:
            logging.error(f"Error in dependency check: {e}")
            return {}

    def ultra_service_check(self) -> Dict[str, Dict[str, any]]:
        """Ultra comprehensive service health check"""
        services = {}

        try:
            # Check LM Studio
            services['lm_studio'] = self._check_lm_studio()

            # Check backend service
            services['backend'] = self._check_backend_service()

            # Check Redis (optional)
            services['redis'] = self._check_redis_service()

            # Check system services
            services['system'] = self._check_system_services()

            # Check network connectivity
            services['network'] = self._check_network_connectivity()

            return services

        except Exception as e:
            logging.error(f"Error in service check: {e}")
            return {}

    def _check_lm_studio(self) -> Dict[str, any]:
        """Check LM Studio service"""
        try:
            import socket
            with socket.create_connection(('localhost', 1234), timeout=5):
                # Try to make an API call
                try:
                    import requests
                    response = requests.get('http://localhost:1234/v1/models', timeout=5)
                    return {
                        'available': True,
                        'api_responsive': response.status_code == 200,
                        'response_time': response.elapsed.total_seconds(),
                        'models': len(response.json().get('data', [])) if response.status_code == 200 else 0
                    }
                except Exception as e:
                    return {
                        'available': True,
                        'api_responsive': False,
                        'error': str(e)
                    }
        except Exception:
            return {
                'available': False,
                'api_responsive': False,
                'error': 'Connection failed'
            }

    def _check_backend_service(self) -> Dict[str, any]:
        """Check backend service"""
        try:
            import requests
            response = requests.get('http://localhost:8000/health', timeout=5)
            return {
                'available': True,
                'healthy': response.status_code == 200,
                'response_time': response.elapsed.total_seconds(),
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'available': False,
                'healthy': False,
                'error': str(e)
            }

    def _check_redis_service(self) -> Dict[str, any]:
        """Check Redis service (optional)"""
        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, socket_timeout=5)
            r.ping()
            return {
                'available': True,
                'responsive': True,
                'info': r.info()
            }
        except ImportError:
            return {
                'available': False,
                'error': 'Redis package not installed'
            }
        except Exception as e:
            return {
                'available': False,
                'responsive': False,
                'error': str(e)
            }

    def _check_system_services(self) -> Dict[str, any]:
        """Check system-level services"""
        try:
            import psutil

            return {
                'cpu_count': psutil.cpu_count(),
                'memory_total': psutil.virtual_memory().total,
                'memory_available': psutil.virtual_memory().available,
                'disk_free': psutil.disk_usage('/').free,
                'boot_time': psutil.boot_time(),
                'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else None
            }
        except Exception as e:
            return {'error': str(e)}

    def _check_network_connectivity(self) -> Dict[str, any]:
        """Check network connectivity"""
        try:
            import socket

            # Test DNS resolution
            socket.gethostbyname('google.com')

            # Test internet connectivity
            with socket.create_connection(('8.8.8.8', 53), timeout=5):
                pass

            return {
                'dns_resolution': True,
                'internet_connectivity': True,
                'local_interfaces': [addr.address for interface in psutil.net_if_addrs().values()
                                   for addr in interface if addr.family == socket.AF_INET]
            }
        except Exception as e:
            return {
                'dns_resolution': False,
                'internet_connectivity': False,
                'error': str(e)
            }

    async def start_ultra_application(self, config_file: Path = None, recovery_mode: bool = False) -> bool:
        """Start application with ultra enhanced features"""
        try:
            # Load ultra configuration
            self.config = create_ultra_automode_config(config_file)

            # Adjust for recovery mode
            if recovery_mode:
                logging.info("Starting in recovery mode")
                self.config.max_retries = 20
                self.config.enable_auto_restart = True
                self.config.enable_self_healing = True
                self.config.enable_graceful_degradation = True
                self.config.degradation_steps = [
                    "reduce_monitoring_frequency",
                    "disable_non_essential_features",
                    "emergency_mode"
                ]

            # Create ultra AutoMode instance
            self.automode = UltraEnhancedAutoMode(self.config, self.base_dir)

            # Check if recovery is needed
            shutdown_marker = self.base_dir / ".shutdown_marker"
            if shutdown_marker.exists():
                logging.info("Clean shutdown detected, removing marker")
                shutdown_marker.unlink()
            else:
                logging.warning("No clean shutdown marker found - may need recovery")
                recovery_mode = True

            # Start services based on availability
            services = self.ultra_service_check()

            # Start backend if not running
            if not services.get('backend', {}).get('available', False):
                await self._start_backend_service()

            # Start additional ultra services
            await self._start_ultra_services()

            logging.info("Ultra application startup completed successfully")
            return True

        except Exception as e:
            logging.error(f"Failed to start ultra application: {e}")
            return False

    async def _start_backend_service(self) -> bool:
        """Start backend service with ultra monitoring"""
        try:
            backend_file = self.base_dir / "backend.py"
            if not backend_file.exists():
                logging.warning("No backend.py found")
                return False

            logging.info("Starting backend service with ultra monitoring...")

            # Define health check for backend
            async def backend_health_check():
                try:
                    import requests
                    response = requests.get('http://localhost:8000/health', timeout=5)
                    return {
                        'healthy': response.status_code == 200,
                        'response_time': response.elapsed.total_seconds(),
                        'details': response.json() if response.status_code == 200 else None
                    }
                except Exception as e:
                    return {'healthy': False, 'error': str(e)}

            success = await self.automode.process_manager.start_managed_process_advanced(
                "backend",
                [sys.executable, str(backend_file)],
                restart_strategy="exponential_backoff",
                health_check_func=backend_health_check
            )

            if success:
                logging.info("Backend service started successfully")

                # Wait for backend to be ready
                for i in range(30):  # Wait up to 30 seconds
                    try:
                        import requests
                        response = requests.get('http://localhost:8000/health', timeout=2)
                        if response.status_code == 200:
                            logging.info(f"Backend ready after {i+1} seconds")
                            return True
                    except:
                        pass
                    await asyncio.sleep(1)

                logging.warning("Backend started but not responding to health checks")
                return True
            else:
                logging.error("Failed to start backend service")
                return False

        except Exception as e:
            logging.error(f"Error starting backend service: {e}")
            return False

    async def _start_ultra_services(self) -> None:
        """Start ultra enhanced services"""
        try:
            # Start file watcher with ultra features
            watcher_file = self.base_dir / "plugin_hotreload.py"
            if watcher_file.exists():
                await self.automode.process_manager.start_managed_process_advanced(
                    "file_watcher",
                    [sys.executable, str(watcher_file)],
                    restart_strategy="linear"
                )
                logging.info("File watcher started with ultra monitoring")

            # Start metrics exporter
            metrics_file = self.base_dir / "metrics_exporter.py"
            if metrics_file.exists():
                await self.automode.process_manager.start_managed_process_advanced(
                    "metrics_exporter",
                    [sys.executable, str(metrics_file)],
                    restart_strategy="immediate"
                )
                logging.info("Metrics exporter started")

            # Start system monitor (if available)
            monitor_file = self.base_dir / "system_monitor.py"
            if monitor_file.exists():
                await self.automode.process_manager.start_managed_process_advanced(
                    "system_monitor",
                    [sys.executable, str(monitor_file)],
                    restart_strategy="exponential_backoff"
                )
                logging.info("System monitor started")

        except Exception as e:
            logging.error(f"Error starting ultra services: {e}")

    async def run_ultra_forever(self) -> None:
        """Run in ultra enhanced mode forever"""
        if not self.automode:
            raise RuntimeError("Ultra application not started")

        logging.info("Starting ultra enhanced long-running mode...")

        # Setup signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            logging.info(f"Received signal {signum}, initiating ultra graceful shutdown...")
            asyncio.create_task(self.automode.graceful_shutdown())

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Run the ultra enhanced AutoMode
        await self.automode.run_ultra()

    async def shutdown_ultra(self) -> None:
        """Ultra enhanced shutdown procedure"""
        logging.info("Initiating ultra enhanced shutdown...")

        if self.automode:
            await self.automode.graceful_shutdown()

        logging.info("Ultra enhanced shutdown completed")


def create_ultra_launcher() -> None:
    """Create ultra enhanced launcher script"""
    launcher_content = '''#!/usr/bin/env python
"""Ultra Enhanced AutoMode Launcher - Production Ready"""
import asyncio
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from startup_ultra_enhanced import UltraApplicationManager

async def main():
    """Main launcher function"""
    manager = UltraApplicationManager()

    print("🚀 Ultra Enhanced AutoMode Launcher")
    print("=" * 50)

    # Setup ultra environment
    print("Setting up ultra environment...")
    if not manager.setup_ultra_environment():
        print("❌ Environment setup failed")
        return 1

    # Check dependencies
    print("Checking dependencies...")
    deps = manager.comprehensive_dependency_check()
    failed_deps = [dep for dep, available in deps.items()
                   if not available and not dep.startswith('optional_')]

    if failed_deps:
        print(f"❌ Critical dependencies missing: {failed_deps}")
        return 1

    # Check services
    print("Checking services...")
    services = manager.ultra_service_check()

    # Start ultra application
    print("Starting ultra application...")
    if not await manager.start_ultra_application():
        print("❌ Failed to start ultra application")
        return 1

    print("✅ Ultra Enhanced AutoMode is running!")
    print("Press Ctrl+C to shutdown gracefully")

    # Run forever
    await manager.run_ultra_forever()

    return 0

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\\n🛑 Graceful shutdown requested by user")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)
'''

    launcher_file = Path(__file__).parent / "launch_ultra.py"
    with open(launcher_file, 'w') as f:
        f.write(launcher_content)

    # Make executable
    os.chmod(launcher_file, 0o755)
    print(f"Created ultra launcher: {launcher_file}")


def main():
    """Main entry point for ultra startup"""
    parser = argparse.ArgumentParser(description="Ultra Enhanced AutoMode Startup")
    parser.add_argument("--config", type=Path, help="Ultra configuration file")
    parser.add_argument("--base-dir", type=Path, help="Base directory", default=Path(__file__).parent)
    parser.add_argument("--check-only", action="store_true", help="Only perform checks")
    parser.add_argument("--recovery-mode", action="store_true", help="Start in recovery mode")
    parser.add_argument("--create-launcher", action="store_true", help="Create launcher script")
    parser.add_argument("--emergency-mode", action="store_true", help="Start in emergency mode")

    args = parser.parse_args()

    if args.create_launcher:
        create_ultra_launcher()
        return 0

    try:
        manager = UltraApplicationManager(args.base_dir)

        print("🚀 Ultra Enhanced AutoMode Startup")
        print("=" * 50)

        # Setup environment
        if not manager.setup_ultra_environment():
            print("❌ Environment setup failed")
            return 1

        # Check dependencies
        deps = manager.comprehensive_dependency_check()
        failed_deps = [dep for dep, available in deps.items()
                      if not available and not dep.startswith('optional_')]

        if failed_deps:
            print(f"❌ Critical dependencies failed: {failed_deps}")
            return 1

        # Check services
        services = manager.ultra_service_check()
        print(f"Service status: {len([s for s in services.values() if s.get('available')])} available")

        if args.check_only:
            print("✅ All checks passed")
            return 0

        # Create ultra config if specified
        config_file = args.config or (args.base_dir / "auto_mode_ultra_config.json")

        # Run ultra application
        async def run_app():
            if not await manager.start_ultra_application(config_file, args.recovery_mode):
                return 1
            await manager.run_ultra_forever()
            return 0

        return asyncio.run(run_app())

    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested by user")
        return 0
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
