#!/usr/bin/env python3
"""
Test module for system

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
import socket
import subprocess
import platform
import time
import json
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path

# Try importing optional dependencies
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

class SystemTester:
    """Comprehensive system tester for the AI chat application"""

    def __init__(self):
        """Initialize the tester with base directory path"""
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.results = {
            "dependencies": {},
            "files": {},
            "directories": {},
            "services": {},
            "network": {},
            "environment": {},
            "functionality": {}
        }

    def check_dependency(self, module_name: str) -> bool:
        """Check if a Python module is installed"""
        try:
            __import__(module_name)
            self.results["dependencies"][module_name] = True
            return True
        except ImportError:
            self.results["dependencies"][module_name] = False
            return False

    def check_file_exists(self, file_path: str) -> bool:
        """Check if a file exists"""
        full_path = os.path.join(self.base_dir, file_path)
        exists = os.path.exists(full_path)
        self.results["files"][file_path] = exists
        return exists

    def check_dir_exists(self, dir_path: str) -> bool:
        """Check if a directory exists"""
        full_path = os.path.join(self.base_dir, dir_path)
        exists = os.path.exists(full_path) and os.path.isdir(full_path)
        self.results["directories"][dir_path] = exists
        return exists

    def check_port_available(self, port: int) -> bool:
        """Check if a port is available"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                available = True
            except OSError:
                available = False

        self.results["network"][f"port_{port}_available"] = available
        return available

    def check_service_running(self, url: str, service_name: str) -> bool:
        """Check if a service is responding at the given URL"""
        if not REQUESTS_AVAILABLE:
            self.results["services"][service_name] = {"status": False, "error": "Requests module not installed"}
            return False

        try:
            response = requests.get(url, timeout=5)
            success = response.status_code == 200
            self.results["services"][service_name] = {
                "status": success,
                "code": response.status_code,
                "response": response.text[:100] if success else None
            }
            return success
        except Exception as e:
            self.results["services"][service_name] = {"status": False, "error": str(e)}
            return False

    def check_env_file(self) -> bool:
        """Check if .env file exists and has required configurations"""
        env_path = os.path.join(self.base_dir, ".env")
        if not os.path.exists(env_path):
            self.results["environment"]["env_file"] = {"status": False, "error": "File not found"}
            return False

        try:
            with open(env_path, 'r') as f:
                content = f.read()

            has_lm_studio = "LM_STUDIO_URL" in content
            self.results["environment"]["env_file"] = {
                "status": has_lm_studio,
                "has_lm_studio_url": has_lm_studio
            }
            return has_lm_studio
        except Exception as e:
            self.results["environment"]["env_file"] = {"status": False, "error": str(e)}
            return False

    def test_backend_ping(self) -> bool:
        """Test if the backend server responds to ping"""
        return self.check_service_running("http://localhost:8000/ping", "backend_ping")

    def test_lm_studio_models(self) -> Tuple[bool, List[str]]:
        """Test connection to LM Studio API and get available models"""
        if not REQUESTS_AVAILABLE:
            self.results["functionality"]["lm_studio_models"] = {"status": False, "error": "Requests module not installed"}
            return False, []

        try:
            response = requests.get("http://localhost:1234/v1/models", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = data.get("data", [])
                model_names = [model.get("id", "Unknown") for model in models]

                self.results["functionality"]["lm_studio_models"] = {
                    "status": True,
                    "count": len(models),
                    "models": model_names
                }
                return True, model_names
            else:
                self.results["functionality"]["lm_studio_models"] = {
                    "status": False,
                    "error": f"Status code {response.status_code}"
                }
                return False, []
        except Exception as e:
            self.results["functionality"]["lm_studio_models"] = {"status": False, "error": str(e)}
            return False, []

    def test_chat_endpoint(self, message: str = "Hello, can you help me test this system?") -> bool:
        """Test the chat endpoint with a simple message"""
        if not REQUESTS_AVAILABLE:
            self.results["functionality"]["chat_endpoint"] = {"status": False, "error": "Requests module not installed"}
            return False

        try:
            response = requests.post(
                "http://localhost:8000/api/chat",
                json={"message": message},
                timeout=15
            )

            success = response.status_code == 200
            if success:
                self.results["functionality"]["chat_endpoint"] = {
                    "status": True,
                    "response_length": len(response.text)
                }
            else:
                self.results["functionality"]["chat_endpoint"] = {
                    "status": False,
                    "error": f"Status code {response.status_code}",
                    "response": response.text
                }
            return success
        except Exception as e:
            self.results["functionality"]["chat_endpoint"] = {"status": False, "error": str(e)}
            return False

    def test_plugins(self) -> bool:
        """Test plugins functionality"""
        if not REQUESTS_AVAILABLE:
            self.results["functionality"]["plugins"] = {"status": False, "error": "Requests module not installed"}
            return False

        try:
            # First check if plugins endpoint responds
            response = requests.get("http://localhost:8000/api/plugins", timeout=5)
            if response.status_code != 200:
                self.results["functionality"]["plugins"] = {
                    "status": False,
                    "error": f"Status code {response.status_code}"
                }
                return False

            # Check if we have any plugins available
            plugins = response.json()
            if not plugins:
                self.results["functionality"]["plugins"] = {
                    "status": True,
                    "warning": "No plugins found",
                    "plugins": []
                }
                return True

            # Try to run the simplest plugin if available
            plugin_names = [p["name"] for p in plugins]
            self.results["functionality"]["plugins"] = {
                "status": True,
                "count": len(plugins),
                "plugins": plugin_names
            }
            return True
        except Exception as e:
            self.results["functionality"]["plugins"] = {"status": False, "error": str(e)}
            return False

    def test_file_upload(self) -> bool:
        """Test file upload functionality with a simple text file"""
        if not REQUESTS_AVAILABLE:
            self.results["functionality"]["file_upload"] = {"status": False, "error": "Requests module not installed"}
            return False

        try:
            # Create a simple test file
            test_file_path = os.path.join(self.base_dir, "test_upload.txt")
            with open(test_file_path, "w") as f:
                f.write("This is a test file for upload functionality.")

            # Upload the file
            with open(test_file_path, "rb") as f:
                files = {"file": ("test_upload.txt", f)}
                response = requests.post(
                    "http://localhost:8000/api/upload",
                    files=files,
                    timeout=10
                )

            # Clean up
            try:
                os.remove(test_file_path)
            except:
                pass

            success = response.status_code == 200
            if success:
                self.results["functionality"]["file_upload"] = {
                    "status": True,
                    "response": response.json()
                }
            else:
                self.results["functionality"]["file_upload"] = {
                    "status": False,
                    "error": f"Status code {response.status_code}",
                    "response": response.text
                }
            return success
        except Exception as e:
            self.results["functionality"]["file_upload"] = {"status": False, "error": str(e)}
            return False

    def run_all_tests(self):
        """Run all system tests and collect results"""
        print(f"{Colors.BOLD}Running AI Chat System Tests{Colors.END}")
        print("=" * 50)

        # Check Python version
        version = platform.python_version()
        self.results["environment"]["python_version"] = {
            "version": version,
            "compatible": version >= "3.8"
        }

        # Check required dependencies
        print(f"\n{Colors.BLUE}Checking dependencies...{Colors.END}")
        dependencies = ["fastapi", "uvicorn", "pydantic", "requests", "python-multipart"]
        for dep in dependencies:
            status = self.check_dependency(dep)
            status_str = f"{Colors.GREEN}OK{Colors.END}" if status else f"{Colors.RED}Missing{Colors.END}"
            print(f"  {dep}: {status_str}")

        # Check optional dependencies
        print(f"\n{Colors.BLUE}Checking optional dependencies...{Colors.END}")
        opt_dependencies = ["Pillow", "python-docx", "openpyxl", "PyPDF2"]
        for dep in opt_dependencies:
            status = self.check_dependency(dep)
            status_str = f"{Colors.GREEN}OK{Colors.END}" if status else f"{Colors.YELLOW}Not installed{Colors.END}"
            print(f"  {dep}: {status_str}")

        # Check required files
        print(f"\n{Colors.BLUE}Checking required files...{Colors.END}")
        required_files = ["backend.py", "backend_starter_server.py", "start_chat_unified.py", "error_handling.py", "file_analyzer.py"]
        for file in required_files:
            status = self.check_file_exists(file)
            status_str = f"{Colors.GREEN}Found{Colors.END}" if status else f"{Colors.RED}Missing{Colors.END}"
            print(f"  {file}: {status_str}")

        # Check directories
        print(f"\n{Colors.BLUE}Checking directories...{Colors.END}")
        dirs = ["uploads", "plugins"]
        for dir_path in dirs:
            status = self.check_dir_exists(dir_path)
            status_str = f"{Colors.GREEN}Found{Colors.END}" if status else f"{Colors.YELLOW}Missing{Colors.END}"
            print(f"  {dir_path}/: {status_str}")

        # Check environment
        print(f"\n{Colors.BLUE}Checking environment...{Colors.END}")
        env_status = self.check_env_file()
        env_status_str = f"{Colors.GREEN}OK{Colors.END}" if env_status else f"{Colors.RED}Issue{Colors.END}"
        print(f"  .env file: {env_status_str}")

        # Check services
        print(f"\n{Colors.BLUE}Checking services...{Colors.END}")

        # Check if ports are in use (services running)
        backend_port_used = not self.check_port_available(8000)
        lm_studio_port_used = not self.check_port_available(1234)
        starter_port_used = not self.check_port_available(9500)

        backend_port_str = f"{Colors.GREEN}Running{Colors.END}" if backend_port_used else f"{Colors.YELLOW}Not Running{Colors.END}"
        lm_studio_port_str = f"{Colors.GREEN}Running{Colors.END}" if lm_studio_port_used else f"{Colors.YELLOW}Not Running{Colors.END}"
        starter_port_str = f"{Colors.GREEN}Running{Colors.END}" if starter_port_used else f"{Colors.YELLOW}Not Running{Colors.END}"

        print(f"  Backend server (port 8000): {backend_port_str}")
        print(f"  LM Studio API (port 1234): {lm_studio_port_str}")
        print(f"  Starter server (port 9500): {starter_port_str}")

        # Test backend service if running
        if backend_port_used:
            print(f"\n{Colors.BLUE}Testing backend functionality...{Colors.END}")

            # Test basic backend ping
            backend_ping_ok = self.test_backend_ping()
            backend_ping_str = f"{Colors.GREEN}OK{Colors.END}" if backend_ping_ok else f"{Colors.RED}Failed{Colors.END}"
            print(f"  Backend ping test: {backend_ping_str}")

            # Test plugins
            plugins_ok = self.test_plugins()
            plugins_str = f"{Colors.GREEN}OK{Colors.END}" if plugins_ok else f"{Colors.RED}Failed{Colors.END}"
            print(f"  Plugins test: {plugins_str}")

            # Test file upload
            upload_ok = self.test_file_upload()
            upload_str = f"{Colors.GREEN}OK{Colors.END}" if upload_ok else f"{Colors.RED}Failed{Colors.END}"
            print(f"  File upload test: {upload_str}")

        # Test LM Studio API if running
        if lm_studio_port_used:
            print(f"\n{Colors.BLUE}Testing LM Studio API...{Colors.END}")

            # Test LM Studio models endpoint
            models_ok, models = self.test_lm_studio_models()
            models_str = f"{Colors.GREEN}OK ({len(models)} models){Colors.END}" if models_ok else f"{Colors.RED}Failed{Colors.END}"
            print(f"  LM Studio models test: {models_str}")

            # If we have both backend and LM Studio running, test chat functionality
            if backend_port_used and models_ok:
                print(f"\n{Colors.BLUE}Testing chat functionality...{Colors.END}")
                chat_ok = self.test_chat_endpoint()
                chat_str = f"{Colors.GREEN}OK{Colors.END}" if chat_ok else f"{Colors.RED}Failed{Colors.END}"
                print(f"  Chat endpoint test: {chat_str}")

        # Overall status
        print("\n" + "=" * 50)
        print(f"{Colors.BOLD}Test Summary:{Colors.END}")

        # Count successes and failures
        success_count = 0
        failure_count = 0

        for category, results in self.results.items():
            for name, value in results.items():
                if isinstance(value, dict) and "status" in value:
                    if value["status"]:
                        success_count += 1
                    else:
                        failure_count += 1
                elif value is True:
                    success_count += 1
                elif value is False:
                    failure_count += 1

        print(f"  {Colors.GREEN}Passed: {success_count}{Colors.END}")
        print(f"  {Colors.RED}Failed: {failure_count}{Colors.END}")

        if failure_count == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}All tests passed! The system is ready for use.{Colors.END}")
        elif failure_count <= 3:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}The system is usable but has some minor issues.{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}The system has significant issues that need to be addressed.{Colors.END}")

        # Troubleshooting suggestions
        if failure_count > 0:
            print("\nTroubleshooting suggestions:")

            # Missing dependencies
            if any(not status for dep, status in self.results["dependencies"].items()):
                print(f"  • Run '{Colors.BOLD}python setup.py{Colors.END}' to install missing dependencies")

            # Missing files
            if any(not status for file, status in self.results["files"].items()):
                print(f"  • Ensure all required files are in place (see list above)")

            # Environment issues
            if "env_file" in self.results["environment"] and not self.results["environment"]["env_file"].get("status", False):
                print(f"  • Create or fix your {Colors.BOLD}.env{Colors.END} file with correct LM Studio URL")

            # Service issues
            if not backend_port_used:
                print(f"  • Start the backend server with '{Colors.BOLD}python start_chat_unified.py{Colors.END}'")
            elif not self.test_backend_ping():
                print(f"  • Backend is running but not responding. Check for errors in the backend console")

            if not lm_studio_port_used:
                print(f"  • Start LM Studio and enable the API server from the API tab")

        print("\nDetailed test results have been saved to 'system_test_results.json'")

        # Save results to file
        results_path = os.path.join(self.base_dir, "system_test_results.json")
        try:
            with open(results_path, 'w') as f:
                json.dump(self.results, f, indent=2)
        except Exception as e:
            print(f"{Colors.RED}Error saving results: {str(e)}{Colors.END}")

if __name__ == "__main__":
    try:
        tester = SystemTester()
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\nTesting interrupted.")
    except Exception as e:
        print(f"\nError running tests: {str(e)}")
        import traceback
        traceback.print_exc()

    input("\nPress Enter to exit...")
