from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import subprocess
import sys
import webbrowser
import threading
import time

class BackendStarterHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/startbackend':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Get the backend path - this should be in the same directory as this script
            backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend.py')
            
            # Start the backend process in a new thread to avoid blocking
            threading.Thread(target=self.start_backend, args=(backend_path,), daemon=True).start()
            
            self.wfile.write(b"Starting backend server...")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
    
    def start_backend(self, backend_path: str) -> None:
        try:
            # Use subprocess to run the uvicorn command
            cwd = os.path.dirname(backend_path)
            cmd = [sys.executable, "-m", "uvicorn", "backend:app", "--reload", "--port", "8000"]
            
            # Start the backend process
            subprocess.Popen(cmd, cwd=cwd, shell=True)
            print(f"Backend server started with command: {' '.join(cmd)}")
        except Exception as e:
            print(f"Error starting backend: {e}")
    
    def log_message(self, format, *args):
        # Override to reduce console output
        return

def run_server(port=9900):
    server_address = ('', port)
    httpd = HTTPServer(server_address, BackendStarterHandler)
    print(f"Backend starter server running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    # Start the helper server
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Open the advanced-ai-chat.html page
    time.sleep(1)
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'advanced-ai-chat.html')
    webbrowser.open(f'file:///{html_path}')
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down helper server...")
        sys.exit(0)
