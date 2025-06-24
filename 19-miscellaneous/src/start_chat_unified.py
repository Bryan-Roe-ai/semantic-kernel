#!/usr/bin/env python3
"""
Start Chat Unified module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# AI Chat Launcher - Start FastAPI backend and open the chat interface
# Uses a unified approach with better error handling

import os
import sys
import subprocess
import webbrowser
import time
import importlib.util
import socket
import signal
import platform
from pathlib import Path
from typing import Optional, Tuple

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

def install_dependency(module_name: str) -> bool:
    """Install a Python module using pip."""
    try:
        print(f"Installing {module_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Colors.GREEN}✓ {module_name} installed successfully{Colors.END}")
        return True
    except subprocess.CalledProcessError:
        print(f"{Colors.RED}✗ Failed to install {module_name}{Colors.END}")
        return False

def check_port_available(port: int) -> bool:
    """Check if a port is available."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return True
        except OSError:
            return False

def find_available_port(start_port: int, max_attempts: int = 10) -> int:
    """Find an available port starting from start_port."""
    port = start_port
    attempts = 0
    
    while attempts < max_attempts:
        if check_port_available(port):
            return port
        port += 1
        attempts += 1
    
    # If we couldn't find an available port, return the original
    # and let the application handle the error
    return start_port

def check_lm_studio() -> Tuple[bool, str]:
    """Check if LM Studio API is running.
    
    Returns:
        tuple: (is_running, error_message)
    """
    try:
        import requests
        lm_studio_url = "http://localhost:1234/v1/models"
        try:
            response = requests.get(lm_studio_url, timeout=5)
            if response.status_code == 200:
                return True, ""
            else:
                return False, f"LM Studio returned status code {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "Connection error - LM Studio server is not running"
        except requests.exceptions.Timeout:
            return False, "Connection timeout - LM Studio server is not responding"
    except ImportError:
        return False, "Requests module not installed"

def create_env_file(base_dir: Path, lm_studio_url: str) -> None:
    """Create or update .env file with LM Studio URL."""
    env_path = base_dir / ".env"
    
    # Read existing content if file exists
    env_vars = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"').strip("'")
    
    # Update LM_STUDIO_URL
    env_vars['LM_STUDIO_URL'] = lm_studio_url
    
    # Write back to file
    with open(env_path, 'w') as f:
        for key, value in env_vars.items():
            f.write(f'{key}="{value}"\n')

def terminate_process(process: Optional[subprocess.Popen]) -> None:
    """Safely terminate a process."""
    if process and process.poll() is None:
        try:
            if platform.system() == 'Windows':
                # On Windows, we need to use CTRL+C signal to properly terminate
                import ctypes
                kernel32 = ctypes.WinDLL('kernel32')
                kernel32.GenerateConsoleCtrlEvent(0, process.pid)
            else:
                # On Unix, SIGTERM works better than SIGINT (CTRL+C)
                process.terminate()
            
            # Wait for a short time for graceful shutdown
            for _ in range(10):
                if process.poll() is not None:
                    break
                time.sleep(0.2)
                
            # If it's still running, force kill
            if process.poll() is None:
                if platform.system() == 'Windows':
                    os.kill(process.pid, signal.SIGTERM)
                else:
                    process.kill()
        except Exception as e:
            print(f"Error terminating process: {str(e)}")

def start_backend_and_chat():
    """Start the FastAPI backend and open the chat interface."""
    process = None
    
    try:
        print(f"{Colors.BOLD}========================================{Colors.END}")
        print(f"{Colors.BOLD}    AI Chat Interface - Quick Start    {Colors.END}")
        print(f"{Colors.BOLD}========================================{Colors.END}")
        print()
        
        # Get the base directory 
        base_dir = Path(__file__).parent.absolute()
        
        # Check for required dependencies
        print(f"{Colors.BLUE}[1/5] Checking dependencies...{Colors.END}")
        dependencies = ["fastapi", "uvicorn", "pydantic", "requests"]
        missing_deps = []
        
        for dep in dependencies:
            if not check_dependency(dep):
                missing_deps.append(dep)
        
        if missing_deps:
            print(f"Installing missing dependencies: {', '.join(missing_deps)}")
            for dep in missing_deps:
                if not install_dependency(dep):
                    print(f"{Colors.RED}Error: Failed to install required dependency: {dep}{Colors.END}")
                    print("Please install it manually with:")
                    print(f"  pip install {dep}")
                    input("Press Enter to exit...")
                    return
        else:
            print(f"{Colors.GREEN}✓ All dependencies are installed{Colors.END}")
        
        # Check for backend.py
        print(f"\n{Colors.BLUE}[2/5] Checking backend files...{Colors.END}")
        backend_path = base_dir / "backend.py"
        if not backend_path.exists():
            print(f"{Colors.RED}Error: {backend_path} not found!{Colors.END}")
            input("Press Enter to exit...")
            return
        print(f"{Colors.GREEN}✓ Backend file found at {backend_path}{Colors.END}")
        
        # Check for available port
        print(f"\n{Colors.BLUE}[3/5] Checking available port...{Colors.END}")
        preferred_port = 8000
        if not check_port_available(preferred_port):
            print(f"{Colors.YELLOW}⚠ Port {preferred_port} is already in use{Colors.END}")
            available_port = find_available_port(8001)
            if available_port == preferred_port:
                print(f"{Colors.RED}Error: Could not find an available port{Colors.END}")
                input("Press Enter to exit...")
                return
            print(f"{Colors.GREEN}✓ Using alternative port: {available_port}{Colors.END}")
        else:
            available_port = preferred_port
            print(f"{Colors.GREEN}✓ Port {available_port} is available{Colors.END}")
        
        # Check or create .env file
        print(f"\n{Colors.BLUE}[4/5] Checking configuration...{Colors.END}")
        env_path = base_dir / ".env"
        lm_studio_url = "http://localhost:1234/v1/chat/completions"
        
        if not env_path.exists():
            print("Creating .env file with default settings...")
            create_env_file(base_dir, lm_studio_url)
            print(f"{Colors.GREEN}✓ Created .env file with default settings{Colors.END}")
        else:
            print(f"{Colors.GREEN}✓ Found existing .env file{Colors.END}")
        
        # Check LM Studio
        print(f"\n{Colors.BLUE}[5/5] Checking LM Studio...{Colors.END}")
        lm_studio_running, lm_studio_error = check_lm_studio()
        if not lm_studio_running:
            print(f"{Colors.YELLOW}⚠ LM Studio API server not detected: {lm_studio_error}{Colors.END}")
            print("Please make sure LM Studio is running:")
            print("1. Start LM Studio application")
            print("2. Go to the 'API' tab")
            print("3. Click 'Start server'")
            print("\nContinuing anyway... but chat functionality will be limited.")
        else:
            print(f"{Colors.GREEN}✓ LM Studio API server is running{Colors.END}")
        
        # Start backend server
        print(f"\n{Colors.BLUE}Starting backend server...{Colors.END}")
        cmd = [sys.executable, "-m", "uvicorn", "backend:app", "--reload", "--host", "127.0.0.1", "--port", str(available_port)]
        
        # Start backend
        process = subprocess.Popen(cmd, cwd=str(base_dir))
        print("Waiting for backend server to start...")
        time.sleep(2)
        
        # Check if process is running
        if process.poll() is not None:
            print(f"{Colors.RED}Error: Failed to start backend server{Colors.END}")
            input("Press Enter to exit...")
            return
            
        print(f"{Colors.GREEN}✓ Backend server started at http://127.0.0.1:{available_port}{Colors.END}")
        
        # Open chat interface
        chat_options = [
            ("advanced-ai-chat.html", "Advanced Chat Interface"),
            ("simple-chat.html", "Simple Chat Interface"),
            ("ai-chat.html", "Standard Chat Interface")
        ]
        
        # Filter to only available interfaces
        available_interfaces = []
        for filename, desc in chat_options:
            file_path = base_dir / filename
            if file_path.exists():
                available_interfaces.append((filename, desc))
        
        if not available_interfaces:
            print(f"{Colors.RED}Error: No chat interface HTML files found!{Colors.END}")
            print("Please make sure at least one of these files exists:")
            for filename, desc in chat_options:
                print(f" - {filename}")
            input("Press Enter to exit...")
            terminate_process(process)
            return
            
        print(f"\n{Colors.BOLD}Available chat interfaces:{Colors.END}")
        for i, (filename, desc) in enumerate(available_interfaces):
            print(f"{i+1}. {desc} ({filename})")
                
        choice = input(f"\n{Colors.BOLD}Enter interface number to open (default=1): {Colors.END}")
        if not choice:
            choice = "1"
            
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(available_interfaces):
                selected = available_interfaces[idx][0]
                file_path = base_dir / selected
                if file_path.exists():
                    print(f"Opening {selected}...")
                    # Update HTML with correct port if different from default
                    if available_port != 8000:
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            # Replace port in API URL
                            content = content.replace('http://localhost:8000', f'http://localhost:{available_port}')
                            
                            # Write temporary file
                            temp_file = base_dir / f"temp_{selected}"
                            with open(temp_file, 'w', encoding='utf-8') as f:
                                f.write(content)
                            
                            # Open temporary file
                            webbrowser.open(f'file:///{temp_file.absolute()}')
                        except Exception as e:
                            print(f"{Colors.YELLOW}Warning: Could not create temporary file with port update: {str(e)}{Colors.END}")
                            print(f"Opening original file, you may need to update the API URL manually to port {available_port}")
                            webbrowser.open(f'file:///{file_path.absolute()}')
                    else:
                        webbrowser.open(f'file:///{file_path.absolute()}')
                else:
                    print(f"{Colors.RED}Error: {selected} not found{Colors.END}")
                    print("You can manually open any HTML file in your browser.")
            else:
                print("Invalid choice. Opening default interface.")
                default_file = available_interfaces[0][0]
                webbrowser.open(f'file:///{(base_dir / default_file).absolute()}')
        except ValueError:
            print("Invalid input. Opening default interface.")
            default_file = available_interfaces[0][0]
            webbrowser.open(f'file:///{(base_dir / default_file).absolute()}')
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}Server is running! Press Ctrl+C to stop.{Colors.END}")
        process.wait()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Stopping server...{Colors.END}")
        terminate_process(process)
    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.END}")
        terminate_process(process)
    finally:
        # Clean up temporary files
        for temp_file in Path(base_dir).glob('temp_*.html'):
            try:
                os.remove(temp_file)
            except:
                pass

if __name__ == "__main__":
    try:
        start_backend_and_chat()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        input("Press Enter to exit...")
