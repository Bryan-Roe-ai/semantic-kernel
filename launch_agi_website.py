#!/usr/bin/env python3
"""
AGI Website Launcher
Starts both the AGI MCP Server and the website server
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

# Configuration
WEBSITE_PORT = 3000
AGI_SERVER_PORT = 8080
WEBSITE_DIR = Path(__file__).parent / "agi-website"
AGI_SERVER_DIR = Path(__file__).parent / "agi-mcp-server"

class AGILauncher:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def start_agi_server(self):
        """Start the AGI MCP Server"""
        print("🧠 Starting AGI MCP Server...")
        
        try:
            # Change to AGI server directory
            os.chdir(AGI_SERVER_DIR)
            
            # Start the AGI server
            cmd = [sys.executable, "-m", "mcp_agi_server.main", "--port", str(AGI_SERVER_PORT)]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            self.processes.append(process)
            print(f"✅ AGI MCP Server started on port {AGI_SERVER_PORT}")
            return process
            
        except Exception as e:
            print(f"❌ Failed to start AGI server: {e}")
            return None
    
    def start_website(self):
        """Start the website server"""
        print("🌐 Starting AGI Website...")
        
        try:
            # Change to website directory
            os.chdir(WEBSITE_DIR)
            
            # Start website server using Node.js if available, otherwise Python
            try:
                # Try Node.js first
                cmd = ["npx", "http-server", "-p", str(WEBSITE_PORT), "--cors"]
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
            except FileNotFoundError:
                # Fallback to Python HTTP server
                cmd = [sys.executable, "-m", "http.server", str(WEBSITE_PORT)]
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
            
            self.processes.append(process)
            print(f"✅ Website started on http://localhost:{WEBSITE_PORT}")
            return process
            
        except Exception as e:
            print(f"❌ Failed to start website: {e}")
            return None
    
    def monitor_processes(self):
        """Monitor and log process output"""
        def log_output(process, name):
            while self.running and process.poll() is None:
                try:
                    line = process.stdout.readline()
                    if line:
                        print(f"[{name}] {line.strip()}")
                except:
                    break
        
        for i, process in enumerate(self.processes):
            name = "AGI-Server" if i == 0 else "Website"
            thread = threading.Thread(target=log_output, args=(process, name))
            thread.daemon = True
            thread.start()
    
    def wait_for_servers(self):
        """Wait for servers to be ready"""
        print("⏳ Waiting for servers to be ready...")
        
        # Wait for AGI server
        agi_ready = False
        for _ in range(30):  # 30 second timeout
            try:
                import requests
                response = requests.get(f"http://localhost:{AGI_SERVER_PORT}/api/status", timeout=1)
                if response.status_code == 200:
                    agi_ready = True
                    break
            except:
                pass
            time.sleep(1)
        
        # Wait for website
        website_ready = False
        for _ in range(10):  # 10 second timeout
            try:
                import requests
                response = requests.get(f"http://localhost:{WEBSITE_PORT}", timeout=1)
                if response.status_code == 200:
                    website_ready = True
                    break
            except:
                pass
            time.sleep(1)
        
        if agi_ready and website_ready:
            print("🎉 All servers are ready!")
            print(f"🌐 Website: http://localhost:{WEBSITE_PORT}")
            print(f"🧠 AGI Server: http://localhost:{AGI_SERVER_PORT}")
        elif website_ready:
            print("🌐 Website is ready (AGI server in demo mode)")
            print(f"🌐 Website: http://localhost:{WEBSITE_PORT}")
        else:
            print("⚠️  Servers may not be fully ready")
    
    def open_browser(self):
        """Open the website in the default browser"""
        try:
            import webbrowser
            webbrowser.open(f"http://localhost:{WEBSITE_PORT}")
            print("🚀 Opening website in browser...")
        except Exception as e:
            print(f"Could not open browser: {e}")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\n🛑 Shutting down servers...")
        self.running = False
        
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except:
                pass
        
        print("✅ Servers stopped")
        sys.exit(0)
    
    def run(self):
        """Main run method"""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("🚀 Starting AGI Website & Server...")
        print("=" * 50)
        
        # Start servers
        agi_process = self.start_agi_server()
        website_process = self.start_website()
        
        if not website_process:
            print("❌ Failed to start website server")
            return 1
        
        # Monitor processes
        self.monitor_processes()
        
        # Wait for servers to be ready
        self.wait_for_servers()
        
        # Open browser
        self.open_browser()
        
        print("\n📝 Instructions:")
        print("  • The website provides a chat interface to interact with AGI")
        print("  • Use the config panel (⚙️) to change server settings")
        print("  • The AGI server provides advanced reasoning, memory, and learning")
        print("  • Press Ctrl+C to stop all servers")
        print("\n🔄 Servers running... Press Ctrl+C to stop")
        
        # Keep running until interrupted
        try:
            while self.running:
                # Check if processes are still alive
                if any(p.poll() is not None for p in self.processes):
                    print("⚠️  A server process has stopped")
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        
        return 0

def main():
    """Main entry point"""
    launcher = AGILauncher()
    return launcher.run()

if __name__ == "__main__":
    sys.exit(main())
