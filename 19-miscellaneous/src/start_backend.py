#!/usr/bin/env python3
"""
Start Backend module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import subprocess
import os
import sys
import webbrowser
import time
import importlib.util

def check_dependency(module_name):
    """Check if a Python module is installed."""
    return importlib.util.find_spec(module_name) is not None

def install_dependency(module_name):
    """Install a Python module using pip."""
    print(f"Installing {module_name}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", module_name], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✓ {module_name} installed successfully")

def start_backend():
    try:
        print("=====================================")
        print("    Starting FastAPI Backend Server")
        print("=====================================")
        
        # Check and install dependencies
        dependencies = ["fastapi", "uvicorn", "pydantic"]
        for dep in dependencies:
            if not check_dependency(dep):
                install_dependency(dep)
                # Verify installation was successful
                if not check_dependency(dep):
                    print(f"Error: Failed to install {dep}. Please install it manually with:")
                    print(f"pip install {dep}")
                    input("Press Enter to exit...")
                    return
        
        # Check if .env file exists and create one if needed
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
        if not os.path.exists(env_path):
            print("Creating default .env file...")
            with open(env_path, 'w') as env_file:
                env_file.write('LM_STUDIO_URL="http://localhost:1234/v1/chat/completions"\n')
            print("Created .env file with default settings")
        
        # Get the backend path
        backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend.py')
        cwd = os.path.dirname(backend_path)
        
        # Check if backend.py exists
        if not os.path.exists(backend_path):
            print(f"Error: {backend_path} not found!")
            input("Press Enter to exit...")
            return
            
        # Use subprocess to run the uvicorn command
        cmd = [sys.executable, "-m", "uvicorn", "backend:app", "--reload", "--host", "127.0.0.1", "--port", "8000"]
        
        print("Starting backend server...")
        print(f"Command: {' '.join(cmd)}")
        
        # Start the backend process
        process = subprocess.Popen(cmd, cwd=cwd)
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        # Check if the process is still running
        if process.poll() is None:
            print("Backend server started successfully at http://127.0.0.1:8000")
            # Open the chat UI
            html_path = os.path.join(cwd, 'advanced-ai-chat.html')
            print(f"Opening chat interface: {html_path}")
            if os.path.exists(html_path):
                webbrowser.open(f'file:///{html_path}')
            else:
                print(f"Warning: Chat UI file not found at {html_path}")
                print("You can manually open any of the HTML files in your browser.")
            
            print("\nServer is running. Press Ctrl+C to stop.")
            # Keep the script running until the user presses Ctrl+C
            process.wait()
        else:
            print("Failed to start backend server")
            print("Check the output above for any error messages")
            input("Press Enter to exit...")
    except Exception as e:
        print(f"Error starting backend: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        start_backend()
    except KeyboardInterrupt:
        print("\nShutting down backend server...")
        sys.exit(0)
