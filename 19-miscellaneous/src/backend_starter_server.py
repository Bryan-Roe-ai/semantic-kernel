#!/usr/bin/env python3
"""
Backend Starter Server module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket
import subprocess
import sys
import threading
import webbrowser
import time
from typing import Any, Optional, Tuple, List

PORT = 9500

class BackendStarterHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/start':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Start the backend process in a new thread
            thread = threading.Thread(target=self.start_backend, daemon=True)
            thread.start()
            
            self.wfile.write(b'{"status": "starting", "message": "Backend server is starting, please wait..."}')
        elif self.path == '/check':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Check if backend is already running
            backend_running = self.check_backend_running()
            
            if backend_running:
                self.wfile.write(b'{"status": "running", "message": "Backend server is already running"}')
            else:
                self.wfile.write(b'{"status": "stopped", "message": "Backend server is not running"}')
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <head><title>Backend Starter Server</title></head>
            <body>
                <h1>Backend Starter Server</h1>
                <p>This service allows the web UI to start the backend server.</p>
                <p>Status: Running</p>
                <button onclick="startBackend()">Start Backend Manually</button>
                <script>
                function startBackend() {
                    fetch('/start')
                        .then(response => response.json())
                        .then(data => alert('Backend is starting...'))
                        .catch(error => alert('Error starting backend: ' + error));
                }
                </script>
            </body>
            </html>
            """)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    def check_backend_running(self):
        """Check if the backend is already running on port 8000"""
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(('localhost', 8000)) == 0
        except:
            return False
    
    def start_backend(self):
        try:
            # Check if the backend is already running
            if self.check_backend_running():
                print("Backend is already running on port 8000. Skipping startup.")
                return
                
            # Get the current directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Check if Python is available
            try:
                subprocess.run([sys.executable, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except (subprocess.SubprocessError, FileNotFoundError):
                print("Error: Python interpreter not found or not working correctly.")
                return
                
            # Check if uvicorn is available
            uvicorn_available = False
            try:
                subprocess.run([sys.executable, "-m", "uvicorn", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                uvicorn_available = True
            except subprocess.SubprocessError:
                print("Warning: uvicorn not found. Will attempt to install it.")
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "uvicorn"], check=True)
                    print("Successfully installed uvicorn.")
                    uvicorn_available = True
                except subprocess.SubprocessError:
                    print("Error: Failed to install uvicorn. Cannot start backend.")
                    return
            
            # Check if backend.py exists
            backend_path = os.path.join(current_dir, 'backend.py')
            if not os.path.exists(backend_path):
                print(f"Error: {backend_path} not found!")
                return
                
            # Check if .env file exists and create one if needed
            env_path = os.path.join(current_dir, '.env')
            if not os.path.exists(env_path):
                print("Creating default .env file...")
                with open(env_path, 'w') as env_file:
                    env_file.write('LM_STUDIO_URL="http://localhost:1234/v1/chat/completions"\n')
            
            # Create uploads directory if it doesn't exist
            uploads_dir = os.path.join(current_dir, 'uploads')
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
                print(f"Created uploads directory: {uploads_dir}")
                
            # Create plugins directory if it doesn't exist
            plugins_dir = os.path.join(current_dir, 'plugins')
            if not os.path.exists(plugins_dir):
                os.makedirs(plugins_dir)
                print(f"Created plugins directory: {plugins_dir}")
                
            # Check if port 8000 is available
            backend_port = 8000
            if not check_port_available(backend_port):
                # Port 8000 is not available but the backend isn't running (we checked above)
                # This means another process is using the port
                print(f"Warning: Port {backend_port} is in use by another application.")
                alt_port = find_available_port(backend_port + 1, max_attempts=10)
                if alt_port:
                    print(f"Using alternative port for backend: {alt_port}")
                    backend_port = alt_port
                else:
                    print("Error: Could not find an available port for the backend server.")
                    print("Please close some applications and try again.")
                    return
            
            # Construct the command to run the backend
            cmd = [sys.executable, "-m", "uvicorn", "backend:app", "--reload", "--host", "127.0.0.1", "--port", str(backend_port)]
            
            # Start the process
            subprocess.Popen(cmd, cwd=current_dir)
            print(f"Backend server started successfully on port {backend_port}")
        except Exception as e:
            print(f"Error starting backend: {e}")
    
    def log_message(self, format: str, *args: Any) -> None:
        """Override to suppress favicon and health check logs for quieter output."""
        if args and any('favicon' in str(arg) or 'health' in str(arg) for arg in args):
            return
        return super().log_message(format, *args)

def check_port_available(port: int) -> bool:
    """Check if a port is available to use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return True
        except OSError:
            return False

def find_available_port(start_port: int, max_attempts: int = 10) -> Optional[int]:
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        if check_port_available(port):
            return port
    return None  # No available ports found

def run_server():
    # Check if default port is available
    if not check_port_available(PORT):
        print(f"Port {PORT} is not available. Looking for an alternative port...")
        alt_port = find_available_port(PORT + 1)
        if alt_port:
            print(f"Using alternative port: {alt_port}")
            server_port = alt_port
        else:
            print("No available ports found. Please close some applications and try again.")
            return
    else:
        server_port = PORT
    
    # Initialize httpd variable before the try block
    httpd = None
    
    try:
        server_address = ('127.0.0.1', server_port)
        httpd = HTTPServer(server_address, BackendStarterHandler)
        print(f"Backend starter server running on http://127.0.0.1:{server_port}")
        print("This server allows the web UI to start the backend server.")
        print("Press Ctrl+C to stop.")
        
        # Open the page in a browser if this is the first run
        first_run_flag = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".starter_shown")
        if not os.path.exists(first_run_flag):
            print("Opening starter page in browser...")
            webbrowser.open(f"http://127.0.0.1:{server_port}")
            # Create flag file to prevent opening browser on subsequent runs
            with open(first_run_flag, "w") as f:
                f.write("shown")
        
        # Start the server
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        if httpd:
            httpd.server_close()
        print("Server stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Please check if another application is using the port.")

if __name__ == "__main__":
    # Open the chat interface
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chat_path = os.path.join(current_dir, 'advanced-ai-chat.html')
    webbrowser.open(f'file:///{chat_path}')
    
    # Run the starter server
    run_server()
