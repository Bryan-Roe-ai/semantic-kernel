#!/usr/bin/env python3
"""
Local AI Setup Script

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import os
import sys
import subprocess
import webbrowser
import time
import platform
import requests
from pathlib import Path
from typing import Optional, List

# ANSI colors for terminal output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    END = '\033[0m'

class LocalAISetup:
    def __init__(self):
        self.workspace_root = Path("/workspaces/semantic-kernel")
        self.backend_dir = self.workspace_root / "19-miscellaneous" / "src"
        self.frontend_dir = self.workspace_root / "07-resources" / "public"
        self.lm_studio_url = "http://localhost:1234"
        self.backend_url = "http://localhost:8000"

    def print_header(self):
        """Print a beautiful header"""
        print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║                              🤖 LOCAL AI SETUP 🤖                            ║
║                         Semantic Kernel Local AI System                     ║
║                              by Bryan Roe (2025)                            ║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.BOLD}Welcome to your complete local AI development environment!{Colors.END}
This script will help you set up and run:
  • LM Studio integration
  • Local AI chat interfaces
  • Plugin system
  • Backend API services
  • File analysis capabilities

{Colors.YELLOW}Let's get started!{Colors.END}
""")

    def check_dependencies(self) -> bool:
        """Check and install required dependencies"""
        print(f"\n{Colors.BLUE}🔍 Checking dependencies...{Colors.END}")

        required_packages = [
            "fastapi",
            "uvicorn",
            "requests",
            "pydantic",
            "starlette"
        ]

        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
                print(f"  ✓ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"  ✗ {package} (missing)")

        if missing_packages:
            print(f"\n{Colors.YELLOW}Installing missing packages...{Colors.END}")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install"
                ] + missing_packages)
                print(f"{Colors.GREEN}✓ All dependencies installed!{Colors.END}")
                return True
            except subprocess.CalledProcessError:
                print(f"{Colors.RED}✗ Failed to install dependencies{Colors.END}")
                return False
        else:
            print(f"{Colors.GREEN}✓ All dependencies are already installed!{Colors.END}")
            return True

    def check_lm_studio(self) -> bool:
        """Check if LM Studio is running"""
        print(f"\n{Colors.BLUE}🔍 Checking LM Studio...{Colors.END}")

        try:
            response = requests.get(f"{self.lm_studio_url}/v1/models", timeout=3)
            if response.status_code == 200:
                models = response.json()
                model_count = len(models.get('data', []))
                print(f"  ✓ LM Studio is running with {model_count} models available")
                return True
            else:
                print(f"  ✗ LM Studio returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException:
            print(f"  ✗ LM Studio is not running or not accessible")
            return False

    def setup_environment(self):
        """Set up environment files"""
        print(f"\n{Colors.BLUE}⚙️ Setting up environment...{Colors.END}")

        # Create .env file in backend directory
        env_file = self.backend_dir / ".env"
        env_content = f'LM_STUDIO_URL="{self.lm_studio_url}/v1/chat/completions"'

        with open(env_file, "w") as f:
            f.write(env_content)

        print(f"  ✓ Environment file created: {env_file}")

        # Ensure directories exist
        directories = [
            self.backend_dir / "plugins",
            self.backend_dir / "uploads"
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Directory ensured: {directory}")

    def start_backend(self) -> Optional[subprocess.Popen]:
        """Start the FastAPI backend server"""
        print(f"\n{Colors.BLUE}🚀 Starting backend server...{Colors.END}")

        backend_script = self.backend_dir / "backend.py"
        if not backend_script.exists():
            print(f"  ✗ Backend script not found: {backend_script}")
            return None

        try:
            # Change to backend directory
            os.chdir(self.backend_dir)

            # Start uvicorn server
            process = subprocess.Popen([
                sys.executable, "-m", "uvicorn",
                "backend:app",
                "--reload",
                "--host", "127.0.0.1",
                "--port", "8000"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Give it time to start
            time.sleep(3)

            # Check if it's running
            try:
                response = requests.get(f"{self.backend_url}/ping", timeout=2)
                if response.status_code == 200:
                    print(f"  ✓ Backend server running at {self.backend_url}")
                    return process
                else:
                    print(f"  ✗ Backend server failed to respond")
                    return None
            except requests.exceptions.RequestException:
                print(f"  ✗ Backend server not responding")
                return None

        except Exception as e:
            print(f"  ✗ Failed to start backend: {str(e)}")
            return None

    def list_available_interfaces(self) -> List[str]:
        """List available chat interfaces"""
        interfaces = []
        interface_files = [
            ("simple-chat.html", "Simple Chat", "Basic chat interface"),
            ("ai-chat-launcher.html", "Advanced Chat", "Full-featured interface with settings"),
            ("plugin-chat.html", "Plugin Chat", "Chat with plugin support"),
            ("sk-demo.html", "SK Demo", "Semantic Kernel demonstration"),
        ]

        print(f"\n{Colors.BLUE}🌐 Available Chat Interfaces:{Colors.END}")

        for i, (filename, name, description) in enumerate(interface_files, 1):
            filepath = self.frontend_dir / filename
            if filepath.exists():
                interfaces.append(str(filepath))
                print(f"  {i}. {Colors.BOLD}{name}{Colors.END} - {description}")
                print(f"     File: {filename}")

        return interfaces

    def open_interface(self, interface_path: str):
        """Open a chat interface in the browser"""
        try:
            # Use the BROWSER environment variable if available (for dev containers)
            browser_cmd = os.environ.get('BROWSER')
            if browser_cmd:
                subprocess.run([browser_cmd, f"file://{interface_path}"])
            else:
                webbrowser.open(f"file://{interface_path}")
            print(f"  ✓ Opened {Path(interface_path).name} in browser")
        except Exception as e:
            print(f"  ✗ Failed to open browser: {str(e)}")
            print(f"  📝 Manual: Open file://{interface_path} in your browser")

    def show_usage_instructions(self):
        """Show how to use the local AI system"""
        print(f"""
{Colors.CYAN}📚 How to Use Your Local AI System:{Colors.END}

{Colors.BOLD}1. LM Studio Setup:{Colors.END}
   • Download and install LM Studio from https://lmstudio.ai/
   • Load your preferred model (Phi, Llama, Mistral, etc.)
   • Go to the "API" tab and click "Start server"
   • Default port is 1234 (configurable)

{Colors.BOLD}2. Chat Interfaces:{Colors.END}
   • Simple Chat: Basic conversation interface
   • Advanced Chat: Full settings control (temperature, tokens, etc.)
   • Plugin Chat: Enhanced with plugin support
   • SK Demo: Semantic Kernel feature showcase

{Colors.BOLD}3. Plugin System:{Colors.END}
   • Add plugins to: {self.backend_dir}/plugins/
   • Supports both Python and template-based plugins
   • File analysis, math, text processing included

{Colors.BOLD}4. File Analysis:{Colors.END}
   • Upload files through the chat interface
   • Supports: Text, CSV, JSON, Images, Documents
   • Automatic analysis and insights

{Colors.BOLD}5. Backend API:{Colors.END}
   • REST API at {self.backend_url}
   • Endpoints: /ping, /api/chat, /api/plugins, /files/*
   • Swagger docs: {self.backend_url}/docs

{Colors.YELLOW}🔥 Pro Tips:{Colors.END}
   • Use system prompts to customize AI behavior
   • Adjust temperature for creativity vs. precision
   • Create custom plugins for specialized tasks
   • Use the plugin chat for advanced workflows
""")

    def main_menu(self):
        """Interactive main menu"""
        backend_process = None

        try:
            while True:
                print(f"""
{Colors.BOLD}What would you like to do?{Colors.END}

1. 🚀 Quick Start (Check everything and launch)
2. 🔧 Setup Only (Install deps, configure)
3. 🌐 List Chat Interfaces
4. 📖 Show Usage Instructions
5. 🧪 Test Backend Connection
6. 📋 Show System Status
7. ❌ Exit

""")

                choice = input(f"{Colors.CYAN}Enter your choice (1-7): {Colors.END}").strip()

                if choice == "1":
                    # Quick start
                    if not self.check_dependencies():
                        continue

                    self.setup_environment()

                    if not self.check_lm_studio():
                        print(f"\n{Colors.YELLOW}⚠️ LM Studio not detected. Please start it manually.{Colors.END}")
                        input("Press Enter when LM Studio is running...")

                    backend_process = self.start_backend()
                    if backend_process:
                        interfaces = self.list_available_interfaces()
                        if interfaces:
                            print(f"\n{Colors.CYAN}Which interface would you like to open?{Colors.END}")
                            choice = input("Enter number (or Enter for Advanced Chat): ").strip()

                            if choice.isdigit() and 1 <= int(choice) <= len(interfaces):
                                self.open_interface(interfaces[int(choice) - 1])
                            else:
                                # Default to advanced chat
                                advanced_chat = self.frontend_dir / "ai-chat-launcher.html"
                                if advanced_chat.exists():
                                    self.open_interface(str(advanced_chat))

                elif choice == "2":
                    # Setup only
                    self.check_dependencies()
                    self.setup_environment()
                    print(f"{Colors.GREEN}✓ Setup complete!{Colors.END}")

                elif choice == "3":
                    # List interfaces
                    self.list_available_interfaces()

                elif choice == "4":
                    # Usage instructions
                    self.show_usage_instructions()

                elif choice == "5":
                    # Test backend
                    try:
                        response = requests.get(f"{self.backend_url}/ping", timeout=2)
                        if response.status_code == 200:
                            print(f"{Colors.GREEN}✓ Backend is running and responding{Colors.END}")
                        else:
                            print(f"{Colors.RED}✗ Backend returned status {response.status_code}{Colors.END}")
                    except requests.exceptions.RequestException:
                        print(f"{Colors.RED}✗ Backend is not running{Colors.END}")

                elif choice == "6":
                    # System status
                    print(f"\n{Colors.BOLD}System Status:{Colors.END}")
                    self.check_dependencies()
                    self.check_lm_studio()

                    try:
                        response = requests.get(f"{self.backend_url}/ping", timeout=2)
                        print(f"  ✓ Backend: Running" if response.status_code == 200 else f"  ✗ Backend: Error {response.status_code}")
                    except:
                        print(f"  ✗ Backend: Not running")

                elif choice == "7":
                    # Exit
                    if backend_process:
                        print(f"\n{Colors.YELLOW}Stopping backend server...{Colors.END}")
                        backend_process.terminate()
                        backend_process.wait()
                    print(f"{Colors.GREEN}👋 Thanks for using Local AI Setup!{Colors.END}")
                    break

                else:
                    print(f"{Colors.RED}Invalid choice. Please enter 1-7.{Colors.END}")

                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

        except KeyboardInterrupt:
            if backend_process:
                print(f"\n{Colors.YELLOW}Stopping backend server...{Colors.END}")
                backend_process.terminate()
                backend_process.wait()
            print(f"\n{Colors.GREEN}👋 Goodbye!{Colors.END}")

def main():
    setup = LocalAISetup()
    setup.print_header()
    setup.main_menu()

if __name__ == "__main__":
    main()
