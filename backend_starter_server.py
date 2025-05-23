#!/usr/bin/env python
"""
Backend Starter Server
----------------------
This small HTTP server allows the web UI to start the backend server.
Run this script in the background to enable the "Start Backend" button.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import subprocess
import sys
import threading
import webbrowser
from typing import Any

PORT = 9500

class BackendStarterHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/start':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Start the backend process in a new thread
            threading.Thread(target=self.start_backend, daemon=True).start()
            
            self.wfile.write(b'{"status": "starting"}')
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
    
    def start_backend(self):
        try:
            # Get the current directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Construct the command to run the backend
            cmd = [sys.executable, "-m", "uvicorn", "backend:app", "--reload", "--host", "127.0.0.1", "--port", "8000"]
            
            # Start the process
            subprocess.Popen(cmd, cwd=current_dir)
            print("Backend server started successfully")
        except Exception as e:
            print(f"Error starting backend: {e}")
    
    def log_message(self, format: str, *args: Any) -> None:
        """Override to suppress favicon and health check logs for quieter output."""
        if args and any('favicon' in str(arg) or 'health' in str(arg) for arg in args):
            return
        return super().log_message(format, *args)

def run_server():
    server_address = ('127.0.0.1', PORT)
    httpd = HTTPServer(server_address, BackendStarterHandler)
    print(f"Backend starter server running on http://127.0.0.1:{PORT}")
    print("This server allows the web UI to start the backend server.")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == "__main__":
    # Open the chat interface
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chat_path = os.path.join(current_dir, 'advanced-ai-chat.html')
    webbrowser.open(f'file:///{chat_path}')
    
    # Run the starter server
    run_server()
