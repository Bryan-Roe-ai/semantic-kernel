#!/usr/bin/env python
# AI Chat Application Setup Helper
# This script helps with the initial setup of dependencies and configuration

import os
import sys
import subprocess
import platform
from pathlib import Path

# ANSI colors for terminal output (will be stripped on Windows CMD)
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def is_admin():
    """Check if the script is running with admin/root privileges"""
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except:
        return False

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    return sys.version_info >= (3, 8)

def main():
    print(f"{Colors.BOLD}===================================={Colors.END}")
    print(f"{Colors.BOLD}  AI Chat Application Setup Helper  {Colors.END}")
    print(f"{Colors.BOLD}===================================={Colors.END}")
    print()

    # Get the base directory
    base_dir = Path(__file__).parent.absolute()

    # --- Automation: Run all setup steps without user input if --auto or /auto is passed ---
    auto_mode = any(arg.lower() in ('--auto', '/auto', '-y', '/y', '--enhanced') for arg in sys.argv)
    enhanced_mode = any(arg.lower() in ('--enhanced', '--enhanced-auto') for arg in sys.argv)

    def auto_input(prompt):
        if auto_mode:
            print(f"[AUTO] {prompt} -> Y")
            return 'y'
        return input(prompt)

    # Check Python version
    print(f"{Colors.BLUE}[1/5] Checking Python version...{Colors.END}")
    if check_python_version():
        print(f"{Colors.GREEN}✓ Python {sys.version.split()[0]} detected (3.8+ required){Colors.END}")
    else:
        print(f"{Colors.RED}✗ Python {sys.version.split()[0]} detected but 3.8+ is required{Colors.END}")
        print("Please install Python 3.8 or higher from https://www.python.org/downloads/")
        auto_input("Press Enter to exit...")
        return False

    # Check for pip
    print(f"\n{Colors.BLUE}[2/5] Checking for pip...{Colors.END}")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True,
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{Colors.GREEN}✓ pip is installed{Colors.END}")
    except:
        print(f"{Colors.RED}✗ pip is not installed or not in PATH{Colors.END}")
        print("Please install pip - it should come with Python but sometimes needs separate installation.")
        print("Visit https://pip.pypa.io/en/stable/installation/ for installation instructions.")
        auto_input("Press Enter to exit...")
        return False

    # Install dependencies
    print(f"\n{Colors.BLUE}[3/5] Installing dependencies...{Colors.END}")
    requirements_file = base_dir / "requirements.txt"

    if not requirements_file.exists():
        print(f"{Colors.YELLOW}! requirements.txt not found, creating default...{Colors.END}")
        with open(requirements_file, 'w') as f:
            f.write("fastapi>=0.110.0\n")
            f.write("uvicorn>=0.28.0\n")
            f.write("pydantic>=2.6.3\n")
            f.write("requests>=2.31.0\n")
            f.write("python-multipart>=0.0.9\n")
            f.write("Pillow>=10.2.0  # Optional: for image analysis\n")

    print("Installing required packages...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                      check=True, stdout=subprocess.PIPE)
        print(f"{Colors.GREEN}✓ Dependencies installed successfully{Colors.END}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}✗ Error installing dependencies: {str(e)}{Colors.END}")
        print("You may need administrator privileges to install packages.")

        if platform.system() == "Windows":
            print("\nTry running the command below in an Administrator PowerShell or Command Prompt:")
            print(f"python -m pip install -r \"{requirements_file}\"")
        else:
            print("\nTry running the command below with sudo:")
            print(f"sudo python3 -m pip install -r \"{requirements_file}\"")

        auto_input("Press Enter to continue anyway (some features may not work)...")

    # Create uploads directory
    print(f"\n{Colors.BLUE}[4/5] Creating required directories...{Colors.END}")
    uploads_dir = base_dir / "uploads"
    plugins_dir = base_dir / "plugins"

    try:
        os.makedirs(uploads_dir, exist_ok=True)
        os.makedirs(plugins_dir, exist_ok=True)
        print(f"{Colors.GREEN}✓ Created required directories{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error creating directories: {str(e)}{Colors.END}")
        print("Make sure you have write permissions in this folder.")
        auto_input("Press Enter to continue anyway...")

    # Create .env file if it doesn't exist
    print(f"\n{Colors.BLUE}[5/5] Checking configuration...{Colors.END}")
    env_file = base_dir / ".env"

    if not env_file.exists():
        print("Creating default .env configuration file...")
        with open(env_file, 'w') as f:
            f.write('LM_STUDIO_URL="http://localhost:1234/v1/chat/completions"\n')
        print(f"{Colors.GREEN}✓ Created default .env configuration{Colors.END}")
    else:
        print(f"{Colors.GREEN}✓ Configuration file exists{Colors.END}")

    # --- Automation: Health checks and auto-update ---
    print(f"\n{Colors.BLUE}Performing health checks...{Colors.END}")
    # Check Python version again
    if not check_python_version():
        print(f"{Colors.RED}Python version is below 3.8. Please upgrade!{Colors.END}")
    # Check pip version
    try:
        pip_ver = subprocess.check_output([sys.executable, "-m", "pip", "--version"]).decode().strip()
        print(f"{Colors.GREEN}✓ {pip_ver}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Could not check pip version: {e}{Colors.END}")
    # Check for updates to requirements
    print(f"{Colors.BLUE}Checking for outdated packages...{Colors.END}")
    try:
        outdated = subprocess.check_output([sys.executable, "-m", "pip", "list", "--outdated", "--format=columns"]).decode()
        if 'Package' in outdated:
            print(f"{Colors.YELLOW}Outdated packages detected:{Colors.END}\n{outdated}")
            if auto_mode or auto_input("Upgrade all packages now? (Y/n): ").lower() != 'n':
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "-r", str(requirements_file)])
                print(f"{Colors.GREEN}✓ All packages upgraded{Colors.END}")
        else:
            print(f"{Colors.GREEN}✓ All packages up to date{Colors.END}")
    except Exception as e:
        print(f"{Colors.YELLOW}Could not check for outdated packages: {e}{Colors.END}")

    # --- Automation: Schedule health checks (Windows Task Scheduler) ---
    if platform.system() == "Windows":
        import getpass
        username = getpass.getuser()
        task_name = "AIChatAppHealthCheck"
        script_path = str(base_dir / "setup.py")
        schtasks_cmd = f'SCHTASKS /Query /TN {task_name}'
        result = subprocess.run(schtasks_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if b"ERROR:" in result.stderr:
            if auto_mode or auto_input("Schedule daily health check for this app? (Y/n): ").lower() != 'n':
                schedule_cmd = f'SCHTASKS /Create /SC DAILY /TN {task_name} /TR "{sys.executable} {script_path} --auto" /ST 09:00 /RL HIGHEST /F'
                try:
                    subprocess.run(schedule_cmd, shell=True, check=True)
                    print(f"{Colors.GREEN}✓ Daily health check scheduled at 09:00{Colors.END}")
                except Exception as e:
                    print(f"{Colors.RED}Failed to schedule health check: {e}{Colors.END}")
        else:
            print(f"{Colors.GREEN}✓ Health check already scheduled as Windows Task{Colors.END}")

    # --- Automation: Remote monitoring (optional) ---
    print(f"\n{Colors.BLUE}Optional: Enable remote monitoring?{Colors.END}")
    if auto_mode or auto_input("Enable remote monitoring (send health status to webhook)? (Y/n): ").lower() != 'n':
        webhook_url = os.environ.get('AICHAT_MONITOR_WEBHOOK') or auto_input("Enter webhook URL for monitoring: ")
        try:
            import requests
            status = {
                'user': os.environ.get('USERNAME', 'unknown'),
                'date': __import__('datetime').datetime.now().isoformat(),
                'status': 'ok',
                'python': sys.version,
                'pip': pip_ver if 'pip_ver' in locals() else 'unknown',
            }
            requests.post(webhook_url, json=status, timeout=5)
            print(f"{Colors.GREEN}✓ Health status sent to webhook{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}Failed to send health status: {e}{Colors.END}")

    # Optional: Offer to install extra plugins/tools
    print(f"\n{Colors.BLUE}Optional: Install extra features?{Colors.END}")
    extras = [
        ("OCR (Image-to-Text)", "pytesseract", "Tesseract OCR", "https://github.com/tesseract-ocr/tesseract"),
        ("Audio (Speech-to-Text)", "speechrecognition", "ffmpeg", "https://ffmpeg.org/download.html"),
        ("Code Execution (Python)", "restrictedpython", None, None),
        ("Web Search", "duckduckgo-search", None, None),
    ]
    enabled = []
    for name, pip_pkg, sys_dep, sys_url in extras:
        choice = auto_input(f"Enable {name}? (Y/n): ")
        if choice.lower() == 'n':
            continue
        print(f"Installing {pip_pkg}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", pip_pkg], check=True)
            enabled.append(name)
        except Exception as e:
            print(f"{Colors.RED}Failed to install {pip_pkg}: {e}{Colors.END}")
        if sys_dep:
            print(f"{Colors.YELLOW}Note: You may need to install {sys_dep} separately. See: {sys_url}{Colors.END}")

    # Advanced: Offer to install and configure Redis for chat memory (optional)
    print(f"\n{Colors.BLUE}Optional: Enable Redis for advanced chat memory?{Colors.END}")
    choice = auto_input("Enable Redis support? (Y/n): ")
    if choice.lower() != 'n':
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "redis"], check=True)
            print(f"{Colors.GREEN}✓ redis-py installed{Colors.END}")
            # Try to detect if Redis is running
            try:
                import redis
                r = redis.Redis(host='localhost', port=6379)
                r.ping()
                print(f"{Colors.GREEN}✓ Redis server detected on localhost:6379{Colors.END}")
            except Exception:
                print(f"{Colors.YELLOW}! Redis server not detected. You can download it from https://redis.io/download or use a cloud service.{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}Failed to install redis-py: {e}{Colors.END}")

    # Advanced: Offer to install OpenAI, Azure, or Gemini SDKs for cloud LLMs
    print(f"\n{Colors.BLUE}Optional: Install cloud LLM SDKs?{Colors.END}")
    cloud_sdks = [
        ("OpenAI", "openai"),
        ("Azure OpenAI", "azure-ai-ml"),
        ("Google Gemini", "google-generativeai"),
    ]
    for name, pkg in cloud_sdks:
        choice = auto_input(f"Install {name} SDK? (Y/n): ")
        if choice.lower() != 'n':
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", pkg], check=True)
                print(f"{Colors.GREEN}✓ {pkg} installed{Colors.END}")
            except Exception as e:
                print(f"{Colors.RED}Failed to install {pkg}: {e}{Colors.END}")

    # Advanced: Offer to install Jupyter for notebook support
    print(f"\n{Colors.BLUE}Optional: Install Jupyter Notebook support?{Colors.END}")
    choice = auto_input("Install Jupyter? (Y/n): ")
    if choice.lower() != 'n':
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "notebook"], check=True)
            print(f"{Colors.GREEN}✓ Jupyter Notebook installed{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}Failed to install Jupyter: {e}{Colors.END}")

    # Print plugin discovery
    print(f"\n{Colors.BLUE}Plugin discovery:{Colors.END}")
    found_plugins = []
    for f in plugins_dir.glob('*.py'):
        found_plugins.append(f.name)
    if found_plugins:
        print(f"{Colors.GREEN}Found plugins:{Colors.END} {', '.join(found_plugins)}")
    else:
        print(f"{Colors.YELLOW}No plugins found in {plugins_dir}{Colors.END}")

    # Check if LM Studio backend is running
    print(f"\n{Colors.BLUE}Checking LM Studio backend...{Colors.END}")
    import socket
    def is_port_open(host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex((host, port)) == 0
    lmstudio_running = is_port_open('localhost', 1234)
    if lmstudio_running:
        print(f"{Colors.GREEN}✓ LM Studio API server is running on port 1234{Colors.END}")
    else:
        print(f"{Colors.RED}✗ LM Studio API server is NOT running on port 1234{Colors.END}")
        print("Start LM Studio and enable the API server.")

    # Offer to start backend server (FastAPI/Uvicorn)
    backend_file = base_dir / "backend.py"
    if backend_file.exists():
        choice = auto_input("\nStart the backend API server now? (Y/n): ")
        if choice.lower() != 'n':
            print("\nStarting backend server (FastAPI/Uvicorn)...")
            try:
                subprocess.Popen([sys.executable, str(backend_file)])
                print(f"{Colors.GREEN}Backend server started in a new process.{Colors.END}")
            except Exception as e:
                print(f"{Colors.RED}Error starting backend: {str(e)}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}No backend.py found. Skipping backend server launch.{Colors.END}")

    # Offer to start LM Studio (if on Windows and LM Studio is installed)
    if platform.system() == "Windows":
        lmstudio_path = Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / "LM Studio" / "LM Studio.exe"
        if lmstudio_path.exists():
            choice = auto_input("\nStart LM Studio now? (Y/n): ")
            if choice.lower() != 'n':
                print("\nLaunching LM Studio...")
                try:
                    os.startfile(str(lmstudio_path))
                    print(f"{Colors.GREEN}LM Studio launched.{Colors.END}")
                except Exception as e:
                    print(f"{Colors.RED}Error launching LM Studio: {str(e)}{Colors.END}")
        else:
            print(f"{Colors.YELLOW}LM Studio not found at {lmstudio_path}{Colors.END}")

    # --- Enhanced AutoMode Setup ---
    if enhanced_mode or auto_mode:
        print(f"\n{Colors.BLUE}Setting up Enhanced AutoMode for long-running operations...{Colors.END}")

        # Install additional packages for enhanced mode
        enhanced_packages = [
            "psutil",
            "watchdog",
            "prometheus-client"
        ]

        for package in enhanced_packages:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package],
                              check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"{Colors.GREEN}✓ {package} installed{Colors.END}")
            except subprocess.CalledProcessError:
                print(f"{Colors.YELLOW}! Failed to install {package} (optional){Colors.END}")

        # Create enhanced AutoMode files if they don't exist
        enhanced_files = [
            "auto_mode_enhanced.py",
            "startup_enhanced.py",
            "metrics_exporter.py",
            "auto_mode_config.json"
        ]

        files_created = []
        for filename in enhanced_files:
            filepath = base_dir / filename
            if not filepath.exists():
                print(f"{Colors.YELLOW}! Enhanced file {filename} not found{Colors.END}")
                print(f"  Please ensure enhanced AutoMode files are in the directory")
            else:
                files_created.append(filename)

        if files_created:
            print(f"{Colors.GREEN}✓ Enhanced AutoMode files available: {', '.join(files_created)}{Colors.END}")

            # Create startup script
            startup_script = base_dir / "start_enhanced.py"
            if not startup_script.exists():
                with open(startup_script, 'w') as f:
                    f.write('''#!/usr/bin/env python
"""Enhanced AutoMode Launcher"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from startup_enhanced import ApplicationManager

async def main():
    manager = ApplicationManager()

    if not manager.setup_environment():
        return 1

    if not manager.check_dependencies():
        return 1

    if not await manager.start_application():
        return 1

    await manager.run_forever()
    return 0

    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\\nShutdown requested")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
''')
                print(f"{Colors.GREEN}✓ Created enhanced startup script{Colors.END}")

        if enhanced_mode:
            print(f"\n{Colors.GREEN}{Colors.BOLD}Enhanced AutoMode setup completed!{Colors.END}")
            print("You can now run with long-running capabilities:")
            print(f"  {Colors.BOLD}python start_enhanced.py{Colors.END}")
            print("Features enabled:")
            print("  - Automatic process restart")
            print("  - Health monitoring and self-healing")
            print("  - Resource usage monitoring")
            print("  - Graceful degradation")
            print("  - State persistence and recovery")
            print("  - Prometheus metrics export")

    # --- Advanced Features: Plugin hot-reload system ---
    print(f"\n{Colors.BLUE}Setting up plugin hot-reload system...{Colors.END}")
    hotreload_file = base_dir / "plugin_hotreload.py"
    if not hotreload_file.exists():
        try:
            with open(hotreload_file, 'w') as f:
                f.write('''#!/usr/bin/env python
# Plugin Hot-Reload System - Auto-created by setup.py
import os
import sys
import time
import importlib
import threading
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s',
                   handlers=[logging.FileHandler("plugin_hotreload.log"),
                             logging.StreamHandler()])

class PluginReloader(FileSystemEventHandler):
    """Watches plugin directory and reloads plugins on change"""

    def __init__(self, plugins_dir):
        self.plugins_dir = plugins_dir
        self.last_reload = {}
        self.lock = threading.Lock()

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith('.py'):
            return

        path = Path(event.src_path)
        plugin_name = path.stem

        # Avoid reloading too frequently (debounce)
        with self.lock:
            now = time.time()
            if plugin_name in self.last_reload and now - self.last_reload[plugin_name] < 2:
                return
            self.last_reload[plugin_name] = now

        try:
            # Try to reload the module if it's loaded
            if plugin_name in sys.modules:
                logging.info(f"Hot-reloading plugin: {plugin_name}")
                importlib.reload(sys.modules[plugin_name])
            else:
                logging.info(f"New plugin detected: {plugin_name}")
        except Exception as e:
            logging.error(f"Error reloading plugin {plugin_name}: {str(e)}")

def start_watching(plugins_dir):
    """Start watching the plugins directory"""
    event_handler = PluginReloader(plugins_dir)
    observer = Observer()
    observer.schedule(event_handler, plugins_dir, recursive=True)
    observer.start()
    logging.info(f"Watching for changes in: {plugins_dir}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    plugins_dir = Path(__file__).parent / "plugins"
    start_watching(plugins_dir)
''')
            print(f"{Colors.GREEN}✓ Created plugin hot-reload system{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}Failed to create plugin hot-reload script: {e}{Colors.END}")
    else:
        print(f"{Colors.GREEN}✓ Plugin hot-reload system already exists{Colors.END}")

    # Install watchdog if needed for hot-reload
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "watchdog"], check=True)
        print(f"{Colors.GREEN}✓ Watchdog installed for plugin hot-reload{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Failed to install watchdog: {e}{Colors.END}")

    # --- Advanced Features: Self-healing capabilities ---
    print(f"\n{Colors.BLUE}Setting up self-healing capabilities...{Colors.END}")
    selfheal_file = base_dir / "self_heal.py"
    if not selfheal_file.exists():
        try:
            with open(selfheal_file, 'w') as f:
                f.write('''#!/usr/bin/env python
# Self-Healing System - Auto-created by setup.py
import os
import sys
import time
import psutil
import logging
import subprocess
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s',
                   handlers=[logging.FileHandler("self_heal.log"),
                             logging.StreamHandler()])

class SelfHealer:
    """Monitors and restarts critical services when they fail"""

    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.backend_script = self.base_dir / "backend.py"
        self.backend_process = None
        self.max_memory_percent = 90  # Restart if memory usage > 90%
        self.max_failures = 0

    def check_backend(self):
        """Check if backend is running, start if not"""
        if self.backend_process is None or not psutil.pid_exists(self.backend_process.pid):
            logging.info("Backend not running. Starting...")
            try:
                self.backend_process = subprocess.Popen(
                    [sys.executable, str(self.backend_script)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                logging.info(f"Backend started with PID: {self.backend_process.pid}")
            except Exception as e:
                logging.error(f"Failed to start backend: {e}")
                self.max_failures += 1
        else:
            # Check resource usage
            try:
                process = psutil.Process(self.backend_process.pid)
                memory_percent = process.memory_percent()
                if memory_percent > self.max_memory_percent:
                    logging.warning(f"Backend using high memory: {memory_percent}%. Restarting...")
                    process.terminate()
                    time.sleep(2)
                    if psutil.pid_exists(self.backend_process.pid):
                        process.kill()
                    self.backend_process = None
            except Exception as e:
                logging.error(f"Error monitoring backend: {e}")

    def run_forever(self, check_interval=30):
        """Run continuous monitoring"""
        logging.info("Self-healer started...")
        while True:
            try:
                self.check_backend()
                if self.max_failures >= 5:
                    logging.critical("Too many failures. Please check system manually.")
                    break
                time.sleep(check_interval)
            except KeyboardInterrupt:
                logging.info("Self-healer stopped by user")
                break
            except Exception as e:
                logging.error(f"Error in self-healer: {e}")
                time.sleep(check_interval)

    base_dir = Path(__file__).parent
    healer = SelfHealer(base_dir)
    healer.run_forever()
''')
            print(f"{Colors.GREEN}✓ Created self-healing system{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}Failed to create self-healing script: {e}{Colors.END}")
    else:
        print(f"{Colors.GREEN}✓ Self-healing system already exists{Colors.END}")

    # Install psutil if needed for self-healing
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "psutil"], check=True)
        print(f"{Colors.GREEN}✓ psutil installed for self-healing{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Failed to install psutil: {e}{Colors.END}")

    # --- Advanced Features: Azure Functions Integration ---
    print(f"\n{Colors.BLUE}Setting up Azure Functions integration...{Colors.END}")
    if auto_mode or auto_input("Set up Azure Functions integration? (Y/n): ").lower() != 'n':
        try:
            # Check if Azure Functions Core Tools are installed
            result = subprocess.run(["func", "--version"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                print(f"{Colors.YELLOW}Azure Functions Core Tools not found. Installing...{Colors.END}")
                if platform.system() == "Windows":
                    subprocess.run(["powershell", "-Command", "npm install -g azure-functions-core-tools@4 --unsafe-perm true"], shell=True)
                else:
                    subprocess.run(["npm", "install", "-g", "azure-functions-core-tools@4", "--unsafe-perm", "true"], shell=True)
                print(f"{Colors.GREEN}✓ Azure Functions Core Tools installed{Colors.END}")
            else:
                print(f"{Colors.GREEN}✓ Azure Functions Core Tools detected: {result.stdout.decode().strip()}{Colors.END}")

            # Check for existing Azure Functions project
            azure_func_dir = base_dir / "AzureFunctions"
            if not azure_func_dir.exists():
                print(f"Creating Azure Functions project in {azure_func_dir}")
                os.makedirs(azure_func_dir, exist_ok=True)
                subprocess.run(["func", "init", "--worker-runtime", "python"], cwd=str(azure_func_dir), shell=True)
                subprocess.run(["func", "new", "--name", "ChatEndpoint", "--template", "HttpTrigger"], cwd=str(azure_func_dir), shell=True)
                print(f"{Colors.GREEN}✓ Azure Functions project created{Colors.END}")
            else:
                print(f"{Colors.GREEN}✓ Azure Functions project exists{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}Failed to set up Azure Functions: {e}{Colors.END}")

    # --- Advanced Features: Advanced Metrics Logging ---
    print(f"\n{Colors.BLUE}Setting up advanced metrics logging...{Colors.END}")
    metrics_file = base_dir / "metrics_logger.py"
    if not metrics_file.exists():
        try:
            with open(metrics_file, 'w') as f:
                f.write('''#!/usr/bin/env python
# Advanced Metrics Logger - Auto-created by setup.py
import os
import time
import json
import psutil
import logging
import threading
from datetime import datetime
from pathlib import Path

class MetricsLogger:
    """Logs system and application metrics"""

    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.metrics_dir = self.base_dir / "metrics"
        os.makedirs(self.metrics_dir, exist_ok=True)

        logging.basicConfig(level=logging.INFO,
                         format='%(asctime)s - %(levelname)s - %(message)s',
                         handlers=[logging.FileHandler(self.metrics_dir / "metrics.log"),
                                   logging.StreamHandler()])
        self.stop_event = threading.Event()

    def collect_system_metrics(self):
        """Collect system-level metrics"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "network_io": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv
            }
        }
        return metrics

    def collect_process_metrics(self):
        """Collect process-specific metrics"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "processes": []
        }

        # Look for Python processes related to our app
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            if 'python' in proc.info['name'].lower():
                try:
                    cmdline = proc.cmdline()
                    if any(x in ' '.join(cmdline) for x in ['backend.py', 'start_chat', 'start_backend']):
                        proc_info = {
                            'pid': proc.info['pid'],
                            'cpu_percent': proc.info['cpu_percent'],
                            'memory_percent': proc.info['memory_percent'],
                            'cmdline': ' '.join(cmdline),
                            'connections': len(proc.connections())
                        }
                        metrics['processes'].append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

        return metrics

    def log_metrics(self):
        """Log system and process metrics to file"""
        sys_metrics = self.collect_system_metrics()
        proc_metrics = self.collect_process_metrics()

        # Log to JSON files with timestamp in filename
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        with open(self.metrics_dir / f"system_metrics_{timestamp}.json", 'w') as f:
            json.dump(sys_metrics, f, indent=2)

        with open(self.metrics_dir / f"process_metrics_{timestamp}.json", 'w') as f:
            json.dump(proc_metrics, f, indent=2)

        # Also log summary to console/log file
        logging.info(f"System: CPU {sys_metrics['cpu_percent']}%, Memory {sys_metrics['memory_percent']}%")
        logging.info(f"Monitored {len(proc_metrics['processes'])} AI Chat processes")

        # Clean up old metrics (keep last 100)
        self._cleanup_old_metrics()

    def _cleanup_old_metrics(self):
        """Delete old metric files to prevent disk fill"""
        all_files = []
        for pattern in ["system_metrics_*.json", "process_metrics_*.json"]:
            all_files.extend(list(self.metrics_dir.glob(pattern)))

        # Sort by modification time (oldest first)
        all_files.sort(key=lambda x: x.stat().st_mtime)

        # Keep only the last 100 files
        if len(all_files) > 100:
            for old_file in all_files[:-100]:
                try:
                    old_file.unlink()
                except:
                    pass

    def run_periodic_logging(self, interval=300):
        """Run metrics logging at regular intervals"""
        logging.info(f"Metrics logger started, interval: {interval} seconds")
        while not self.stop_event.is_set():
            try:
                self.log_metrics()
            except Exception as e:
                logging.error(f"Error logging metrics: {e}")
            # Wait for interval or until stop event
            self.stop_event.wait(interval)

    def start(self, interval=300):
        """Start metrics logging in a background thread"""
        thread = threading.Thread(target=self.run_periodic_logging, args=(interval,))
        thread.daemon = True
        thread.start()
        return thread

    def stop(self):
        """Stop the metrics logging"""
        self.stop_event.set()

    base_dir = Path(__file__).parent
    logger = MetricsLogger(base_dir)

    try:
        logging_thread = logger.start(interval=60)  # Log every minute
        logging_thread.join()
    except KeyboardInterrupt:
        logger.stop()
        print("Metrics logging stopped.")
''')
            print(f"{Colors.GREEN}✓ Created advanced metrics logger{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}Failed to create metrics logger: {e}{Colors.END}")
    else:
        print(f"{Colors.GREEN}✓ Advanced metrics logger already exists{Colors.END}")

    # --- Advanced Features: Cloud deployment automation ---
    print(f"\n{Colors.BLUE}Setting up cloud deployment automation...{Colors.END}")
    if auto_mode or auto_input("Set up cloud deployment automation? (Y/n): ").lower() != 'n':
        deploy_file = base_dir / "cloud_deploy.py"
        try:
            with open(deploy_file, 'w') as f:
                f.write('''#!/usr/bin/env python
# Cloud Deployment Automation - Auto-created by setup.py
import os
import sys
import time
import json
import logging
import argparse
import subprocess
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s',
                   handlers=[logging.FileHandler("cloud_deploy.log"),
                             logging.StreamHandler()])

class CloudDeployer:
    """Handles deployment to various cloud platforms"""

    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.config_path = self.base_dir / "cloud_deploy_config.json"
        self.load_config()

    def load_config(self):
        """Load deployment configuration"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                logging.info(f"Loaded configuration from {self.config_path}")
            except Exception as e:
                logging.error(f"Error loading configuration: {e}")
                self.config = {}
        else:
            logging.warning(f"No configuration found at {self.config_path}, using defaults")
            # Default configuration
            self.config = {
                "azure": {
                    "resource_group": "ai-chat-app-rg",
                    "app_name": "ai-chat-app",
                    "location": "eastus",
                    "sku": "F1"
                },
                "aws": {
                    "s3_bucket": "ai-chat-app-bucket",
                    "region": "us-east-1"
                },
                "docker": {
                    "image_name": "ai-chat-app",
                    "tag": "latest"
                }
            }
            # Save default config
            self.save_config()

    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            logging.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logging.error(f"Error saving configuration: {e}")

    def create_dockerfile(self):
        """Create Dockerfile for containerization"""
        docker_path = self.base_dir / "Dockerfile"
        if not docker_path.exists():
            try:
                with open(docker_path, 'w') as f:
                    f.write("""FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Expose the port
EXPOSE 8000

# Start the application
CMD ["python", "backend.py"]
""")
                logging.info(f"Created Dockerfile at {docker_path}")
            except Exception as e:
                logging.error(f"Error creating Dockerfile: {e}")
                return False
        return True

    def build_docker_image(self):
        """Build Docker image from Dockerfile"""
        if not self.create_dockerfile():
            return False

        image_name = f"{self.config['docker']['image_name']}:{self.config['docker']['tag']}"
        logging.info(f"Building Docker image: {image_name}")

        try:
            result = subprocess.run(
                ["docker", "build", "-t", image_name, "."],
                cwd=str(self.base_dir),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            logging.info("Docker image built successfully")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Docker build failed: {e.stderr.decode()}")
            return False
        except Exception as e:
            logging.error(f"Error building Docker image: {e}")
            return False

    def deploy_to_azure(self):
        """Deploy application to Azure App Service"""
        logging.info("Starting deployment to Azure")

        # Check Azure CLI is installed
        try:
            subprocess.run(["az", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            logging.error("Azure CLI not installed. Please install it first.")
            return False

        # Login to Azure (if needed)
        try:
            subprocess.run(["az", "account", "show"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            logging.info("Please log in to Azure...")
            subprocess.run(["az", "login"], check=True)

        rg = self.config["azure"]["resource_group"]
        app_name = self.config["azure"]["app_name"]
        location = self.config["azure"]["location"]
        sku = self.config["azure"]["sku"]

        # Create resource group if it doesn't exist
        try:
            subprocess.run(
                ["az", "group", "create", "--name", rg, "--location", location],
                check=True,
                stdout=subprocess.PIPE
            )
            logging.info(f"Resource group '{rg}' created or already exists")
        except Exception as e:
            logging.error(f"Failed to create resource group: {e}")
            return False

        # Deploy as App Service
        try:
            # Create App Service plan
            subprocess.run(
                ["az", "appservice", "plan", "create", "--name", f"{app_name}-plan",
                 "--resource-group", rg, "--sku", sku],
                check=True,
                stdout=subprocess.PIPE
            )
            # Create Web App
            subprocess.run(
                ["az", "webapp", "create", "--name", app_name,
                 "--resource-group", rg, "--plan", f"{app_name}-plan",
                 "--runtime", "PYTHON:3.10"],
                check=True,
                stdout=subprocess.PIPE
            )
            # Deploy code
            subprocess.run(
                ["az", "webapp", "up", "--name", app_name, "--resource-group", rg],
                check=True,
                cwd=str(self.base_dir),
                stdout=subprocess.PIPE
            )
            logging.info(f"Web App deployed to https://{app_name}.azurewebsites.net")
            return True
        except Exception as e:
            logging.error(f"Azure deployment failed: {e}")
            return False

    def deploy_to_aws(self):
        """Deploy application to AWS (basic S3 static hosting)"""
        logging.info("Starting deployment to AWS")

        # Check AWS CLI is installed
        try:
            subprocess.run(["aws", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            logging.error("AWS CLI not installed. Please install it first.")
            return False

        bucket = self.config["aws"]["s3_bucket"]
        region = self.config["aws"]["region"]

        # Create bucket if it doesn't exist
        try:
            subprocess.run(
                ["aws", "s3", "mb", f"s3://{bucket}", "--region", region],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except:
            logging.info(f"Bucket {bucket} might already exist")

        # Enable website hosting
        try:
            subprocess.run(
                ["aws", "s3", "website", f"s3://{bucket}",
                 "--index-document", "ai-chat-launcher.html"],
                check=True,
                stdout=subprocess.PIPE
            )
            logging.info(f"S3 website hosting enabled on bucket {bucket}")
        except Exception as e:
            logging.error(f"Failed to enable website hosting: {e}")
            return False

        # Sync files
        try:
            # Upload HTML files
            for html_file in self.base_dir.glob("*.html"):
                subprocess.run(
                    ["aws", "s3", "cp", str(html_file), f"s3://{bucket}/",
                     "--acl", "public-read"],
                    check=True,
                    stdout=subprocess.PIPE
                )
            logging.info(f"Deployed static files to http://{bucket}.s3-website-{region}.amazonaws.com/")
            return True
        except Exception as e:
            logging.error(f"AWS deployment failed: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Cloud Deployment Tool")
    parser.add_argument("--target", choices=["azure", "aws", "docker"],
                      help="Deployment target")
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    deployer = CloudDeployer(base_dir)

    if not args.target:
        print("Please specify a deployment target: azure, aws, or docker")
        return

    if args.target == "azure":
        deployer.deploy_to_azure()
    elif args.target == "aws":
        deployer.deploy_to_aws()
    elif args.target == "docker":
        deployer.build_docker_image()

    main()
''')
            print(f"{Colors.GREEN}✓ Created cloud deployment automation script{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}Failed to create cloud deployment script: {e}{Colors.END}")

    # Print enabled features summary
    print(f"\n{Colors.BOLD}Enabled features:{Colors.END}")
    print(f"  - Core chat backend")
    for name in enabled:
        print(f"  - {name}")
    print(f"  - Plugins: {', '.join(found_plugins) if found_plugins else 'None'}")

    # Print success message
    print(f"\n{Colors.GREEN}{Colors.BOLD}Setup completed successfully!{Colors.END}")
    print("You can now run the AI Chat Application with:")
    print(f"  {Colors.BOLD}python start_chat_unified.py{Colors.END}")
    print("Or for Windows users, double-click on:")
    print(f"  {Colors.BOLD}start_ai_chat.bat{Colors.END}")
    print("\nMake sure LM Studio is running with the API server started.")

    # Ask if the user wants to start the application now
    choice = auto_input("\nStart the AI Chat Application now? (Y/n): ")
    if choice.lower() != 'n':
        print("\nStarting AI Chat Application...")
        try:
            subprocess.run([sys.executable, "start_chat_unified.py"])
        except Exception as e:
            print(f"{Colors.RED}Error starting application: {str(e)}{Colors.END}")
            auto_input("Press Enter to exit...")

    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSetup interrupted.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        auto_input("Press Enter to exit...")
