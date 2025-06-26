#!/usr/bin/env python3
"""
Diagnose System module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# AI Chat System Diagnostic Dashboard
# Provides a visual status overview of the AI chat system components

import os
import sys
import platform
import subprocess
import socket
import webbrowser
import time
from pathlib import Path
from datetime import datetime
import importlib.util

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# ANSI colors for terminal output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def check_dependency(module_name: str) -> bool:
    """Check if a Python module is installed."""
    return importlib.util.find_spec(module_name) is not None

def check_port_available(port: int) -> bool:
    """Check if a port is available."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return True
        except OSError:
            return False

def check_lm_studio_status():
    """Check LM Studio connection status and get model info."""
    if not REQUESTS_AVAILABLE:
        return False, "Requests module not installed", []

    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get("data", [])
            model_names = [model.get("id", "Unknown") for model in models]
            return True, f"Connected (Found {len(models)} models)", model_names
        else:
            return False, f"Error: Status code {response.status_code}", []
    except requests.exceptions.ConnectionError:
        return False, "Connection refused - API server not running", []
    except requests.exceptions.Timeout:
        return False, "Connection timeout - server not responding", []
    except Exception as e:
        return False, f"Error: {str(e)}", []

def check_backend_status():
    """Check if the backend server is running."""
    if not REQUESTS_AVAILABLE:
        return False, "Requests module not installed"

    try:
        response = requests.get("http://localhost:8000/ping", timeout=5)
        if response.status_code == 200:
            return True, "Connected (Backend server running)"
        else:
            return False, f"Error: Status code {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused - Backend not running"
    except requests.exceptions.Timeout:
        return False, "Connection timeout - server not responding"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_python_version():
    """Check Python version and return status."""
    version = platform.python_version()
    if version >= "3.8":
        return True, f"Python {version} (Compatible)"
    else:
        return False, f"Python {version} (Not compatible - 3.8+ required)"

def check_file_exists(path):
    """Check if a file exists and return status."""
    if os.path.exists(path):
        return True, "File found"
    else:
        return False, "File not found"

def check_dir_exists(path):
    """Check if a directory exists and return status."""
    if os.path.exists(path) and os.path.isdir(path):
        return True, "Directory found"
    else:
        return False, "Directory not found or not a directory"

def check_env_file():
    """Check .env file and its content."""
    env_path = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(env_path):
        return False, "File not found"

    try:
        with open(env_path, 'r') as f:
            content = f.read()

        if "LM_STUDIO_URL" in content:
            return True, "File found with LM_STUDIO_URL configured"
        else:
            return False, "LM_STUDIO_URL not found in .env file"
    except Exception as e:
        return False, f"Error reading file: {str(e)}"

def print_component_status(name, status_ok, status_msg, indent=0):
    """Print component status with color coding."""
    indent_str = "  " * indent
    status_color = Colors.GREEN if status_ok else Colors.RED
    status_symbol = "✓" if status_ok else "✗"

    print(f"{indent_str}{status_color}{status_symbol}{Colors.END} {name}: {status_msg}")

def print_header(title):
    """Print a section header."""
    print(f"\n{Colors.BOLD}{title}{Colors.END}")
    print("─" * 50)

def run_diagnostic():
    """Run the diagnostic checks and display results."""
    print(f"{Colors.BOLD}AI Chat System Diagnostic Dashboard{Colors.END}")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"System: {platform.system()} {platform.version()}")
    print("=" * 50)

    # Check Python environment
    print_header("Python Environment")
    python_ok, python_msg = check_python_version()
    print_component_status("Python version", python_ok, python_msg)

    # Check dependencies
    dependencies = ["fastapi", "uvicorn", "pydantic", "requests", "python-multipart"]
    for dep in dependencies:
        dep_ok = check_dependency(dep)
        print_component_status(dep, dep_ok, "Installed" if dep_ok else "Not installed", indent=1)

    # Check optional dependencies
    print("\nOptional dependencies:")
    opt_dependencies = ["Pillow", "python-docx", "openpyxl", "PyPDF2"]
    for dep in opt_dependencies:
        dep_ok = check_dependency(dep)
        print_component_status(dep, dep_ok, "Installed" if dep_ok else "Not installed", indent=1)

    # Check configuration
    print_header("Configuration")
    env_ok, env_msg = check_env_file()
    print_component_status(".env file", env_ok, env_msg)

    # Check backend files
    print_header("Required Files")
    backend_ok, backend_msg = check_file_exists("backend.py")
    print_component_status("backend.py", backend_ok, backend_msg)

    unified_ok, unified_msg = check_file_exists("start_chat_unified.py")
    print_component_status("start_chat_unified.py", unified_ok, unified_msg)

    # Check directories
    uploads_ok, uploads_msg = check_dir_exists("uploads")
    print_component_status("uploads directory", uploads_ok, uploads_msg)

    plugins_ok, plugins_msg = check_dir_exists("plugins")
    print_component_status("plugins directory", plugins_ok, plugins_msg)

    # Check services
    print_header("Services")
    lm_studio_ok, lm_studio_msg, models = check_lm_studio_status()
    print_component_status("LM Studio API", lm_studio_ok, lm_studio_msg)

    if models:
        print("\nAvailable models:")
        for i, model in enumerate(models[:5]):
            print(f"  {i+1}. {model}")
        if len(models) > 5:
            print(f"  ... and {len(models)-5} more")

    backend_ok, backend_msg = check_backend_status()
    print_component_status("Backend server", backend_ok, backend_msg)

    # Check ports
    print_header("Network")
    port8000_ok = not check_port_available(8000)
    print_component_status("Port 8000 (Backend)", port8000_ok, "In use (service running)" if port8000_ok else "Available (service not running)")

    port1234_ok = not check_port_available(1234)
    print_component_status("Port 1234 (LM Studio)", port1234_ok, "In use (service running)" if port1234_ok else "Available (service not running)")

    # Overall status
    print_header("Overall Status")
    critical_components = [python_ok, backend_ok, env_ok, backend_ok]
    if all(critical_components):
        print(f"{Colors.GREEN}{Colors.BOLD}✓ System is ready!{Colors.END}")
        if not lm_studio_ok:
            print(f"{Colors.YELLOW}⚠️  Warning: LM Studio is not running - Chat will have limited functionality{Colors.END}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ System has issues that need to be addressed{Colors.END}")

        # Provide troubleshooting suggestions
        print("\nTroubleshooting suggestions:")
        if not python_ok:
            print("• Install Python 3.8 or higher from https://www.python.org/downloads/")
        if not all(check_dependency(dep) for dep in dependencies):
            print("• Run 'python setup.py' to install required dependencies")
        if not backend_ok:
            if backend_ok:
                print("• Start the backend server with 'python start_chat_unified.py'")
            else:
                print("• Make sure backend.py exists in the current directory")
        if not env_ok:
            print("• Create a .env file with 'LM_STUDIO_URL=\"http://localhost:1234/v1/chat/completions\"'")
        if not lm_studio_ok:
            print("• Start LM Studio and enable the API server from the API tab")

    print("\nFor detailed setup instructions, see SETUP_AND_USAGE.md")
    print("=" * 50)

    user_action = input("\nWhat would you like to do next? (Enter a number)\n"
                       "1. Run setup script\n"
                       "2. Start AI Chat application\n"
                       "3. View setup documentation\n"
                       "4. Exit\n"
                       "> ")

    if user_action == "1":
        print("\nRunning setup script...")
        subprocess.run([sys.executable, "setup.py"])
    elif user_action == "2":
        print("\nStarting AI Chat application...")
        subprocess.run([sys.executable, "start_chat_unified.py"])
    elif user_action == "3":
        print("\nOpening documentation...")
        doc_path = os.path.join(os.getcwd(), "SETUP_AND_USAGE.md")
        if os.path.exists(doc_path):
            webbrowser.open(f"file:///{os.path.abspath(doc_path)}")
        else:
            print(f"{Colors.RED}Documentation file not found: {doc_path}{Colors.END}")
    else:
        print("\nExiting...")

if __name__ == "__main__":
    try:
        run_diagnostic()
    except KeyboardInterrupt:
        print("\nDiagnostic interrupted.")
    except Exception as e:
        print(f"\n{Colors.RED}Error running diagnostics: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()

    input("\nPress Enter to exit...")
