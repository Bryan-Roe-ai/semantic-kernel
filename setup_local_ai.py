#!/usr/bin/env python3
"""DEPRECATION SHIM: setup_local_ai.py moved to tools/environment/setup_local_ai.py"""
import importlib
print("[DEPRECATED] setup_local_ai.py moved to tools/environment/setup_local_ai.py")
impl = importlib.import_module('tools.environment.setup_local_ai')
if __name__ == '__main__':
    impl.main()

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
