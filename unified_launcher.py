#!/usr/bin/env python3
"""
import asyncio
Unified Master Launcher for Semantic Kernel Workspace

This script provides a central launcher for all functionality and handles dependency management and file fixing.

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License
"""

import os
import sys
import subprocess
import argparse
import time
import json
import platform
import logging
import shutil
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import importlib.util
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add workspace to Python path
WORKSPACE_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(WORKSPACE_ROOT))


# ANSI colors for terminal output
class Colors:
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    MAGENTA = "\033[35m"
    WHITE = "\033[37m"
    END = "\033[0m"


class UnifiedLauncher:
    """Unified launcher that fixes all files and provides centralized access"""

    def __init__(self):
        self.workspace_root = WORKSPACE_ROOT
        self.python_path = sys.executable
        self.running_processes = []
        self.available_scripts = {}
        self.issues_fixed = 0
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = self.workspace_root / "logs"
        log_dir.mkdir(exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_dir / "unified_launcher.log"),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger("UnifiedLauncher")

    def print_banner(self):
        """Print the unified launcher banner"""
        print(f"\n{Colors.CYAN}{'='*80}{Colors.END}")
        print(
            f"{Colors.BOLD}{Colors.WHITE}🚀 SEMANTIC KERNEL UNIFIED LAUNCHER{Colors.END}"
        )
        print(f"{Colors.CYAN}{'='*80}{Colors.END}")
        print(f"{Colors.YELLOW}Making everything runnable from one place!{Colors.END}")
        print(f"{Colors.BLUE}Workspace: {self.workspace_root}{Colors.END}")
        print(f"{Colors.GREEN}Python: {self.python_path}{Colors.END}")
        print()

    def discover_all_scripts(self):
        """Discover all Python scripts in the workspace"""
        self.logger.info("Discovering all scripts...")

        # Script patterns to find
        patterns = [
            "**/*.py",
            "**/*.sh",
            "**/launch*",
            "**/start*",
            "**/run*",
            "**/setup*",
        ]

        categories = {
            "launchers": [],
            "servers": [],
            "demos": [],
            "tools": [],
            "ai_agents": [],
            "monitoring": [],
            "setup": [],
            "tests": [],
            "automation": [],
            "core": [],
        }

        for pattern in patterns:
            for script_path in self.workspace_root.glob(pattern):
                if (
                    script_path.is_file()
                    and not str(script_path).startswith(".")
                    and "__pycache__" not in str(script_path)
                ):

                    category = self._categorize_script(script_path)
                    script_info = {
                        "path": script_path,
                        "relative_path": script_path.relative_to(self.workspace_root),
                        "category": category,
                        "description": self._get_description(script_path),
                        "can_run": self._can_run(script_path),
                        "has_main": self._has_main(script_path),
                        "dependencies": self._get_dependencies(script_path),
                    }

                    categories[category].append(script_info)

        self.available_scripts = categories
        total = sum(len(scripts) for scripts in categories.values())
        self.logger.info(
            f"Discovered {total} scripts across {len(categories)} categories"
        )

    def _categorize_script(self, script_path: Path) -> str:
        """Categorize script based on path and content"""
        path_str = str(script_path).lower()
        name = script_path.name.lower()

        # Check path and name for category hints
        if any(x in path_str for x in ["launch", "start", "main"]):
            return "launchers"
        elif any(x in name for x in ["server", "api", "backend"]):
            return "servers"
        elif any(x in path_str for x in ["demo", "example", "sample"]):
            return "demos"
        elif any(x in name for x in ["agent", "cognitive", "intelligence"]):
            return "ai_agents"
        elif any(x in name for x in ["monitor", "dashboard", "status"]):
            return "monitoring"
        elif any(x in name for x in ["setup", "install", "config"]):
            return "setup"
        elif any(x in path_str for x in ["test", "tests"]):
            return "tests"
        elif any(x in path_str for x in ["automation", "scripts"]):
            return "automation"
        elif "01-core" in path_str or "semantic_kernel" in path_str:
            return "core"
        else:
            return "tools"

    def _get_description(self, script_path: Path) -> str:
        """Extract description from script"""
        try:
            with open(script_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(1000)

            # Look for docstring or comments
            if '"""' in content:
                start = content.find('"""') + 3
                end = content.find('"""', start)
                if end > start:
                    desc = content[start:end].strip()
                    return desc.split("\n")[0][:80]

            lines = content.split("\n")
            for line in lines[:10]:
                if line.strip().startswith("#") and len(line.strip()) > 5:
                    return line.strip()[1:].strip()[:80]

        except Exception:
            pass

        return f"Script: {script_path.name}"

    def _can_run(self, script_path: Path) -> bool:
        """Check if script can be executed"""
        if script_path.suffix == ".py":
            return self._has_main(script_path)
        elif script_path.suffix == ".sh":
            return True
        return False

    def _has_main(self, script_path: Path) -> bool:
        """Check if Python script has main function"""
        try:
            with open(script_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            return any(
                pattern in content
                for pattern in [
                    "def main(",
                    'if __name__ == "__main__"',
                    "async def main(",
                    "class " + script_path.stem.title(),
                ]
            )
        except Exception:
            return False

    def _get_dependencies(self, script_path: Path) -> List[str]:
        """Extract dependencies from script"""
        deps = []
        try:
            with open(script_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Find import statements
            import_pattern = r"^(?:from\s+(\S+)|import\s+(\S+))"
            for match in re.finditer(import_pattern, content, re.MULTILINE):
                module = match.group(1) or match.group(2)
                if (
                    module
                    and "." not in module
                    and module not in ["sys", "os", "json", "time"]
                ):
                    deps.append(module.split()[0])

        except Exception:
            pass

        return list(set(deps))

    def fix_all_files(self):
        """Fix all Python files in the workspace"""
        print(f"\n{Colors.YELLOW}🔧 FIXING ALL FILES{Colors.END}")
        print(f"{Colors.CYAN}{'='*50}{Colors.END}")

        python_files = list(self.workspace_root.rglob("*.py"))
        total_files = len(python_files)

        print(f"Found {total_files} Python files to fix...")

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(self._fix_file, f): f for f in python_files}

            for i, future in enumerate(as_completed(futures), 1):
                file_path = futures[future]
                try:
                    fixes = future.result()
                    self.issues_fixed += fixes
                    if fixes > 0:
                        print(
                            f"  {i:3d}/{total_files} ✅ {file_path.name} ({fixes} fixes)"
                        )
                    else:
                        print(f"  {i:3d}/{total_files} ⚪ {file_path.name}")
                except Exception as e:
                    print(f"  {i:3d}/{total_files} ❌ {file_path.name} - Error: {e}")

        print(
            f"\n{Colors.GREEN}✅ Fixed {self.issues_fixed} issues across {total_files} files{Colors.END}"
        )

    def _fix_file(self, file_path: Path) -> int:
        """Fix issues in a specific Python file"""
        fixes_applied = 0

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            original_content = content

            # Fix 1: Remove duplicate shebang lines
            lines = content.split("\n")
            shebang_count = sum(1 for line in lines[:5] if line.startswith("#!"))
            if shebang_count > 1:
                new_lines = []
                shebang_added = False
                for line in lines:
                    if line.startswith("#!"):
                        if not shebang_added:
                            new_lines.append("#!/usr/bin/env python3")
                            shebang_added = True
                    else:
                        new_lines.append(line)
                content = "\n".join(new_lines)
                fixes_applied += 1

            # Fix 2: Add missing imports
            missing_imports = self._detect_missing_imports(content)
            if missing_imports:
                import_section = []
                for imp in missing_imports:
                    if imp == "Path":
                        import_section.append("from pathlib import Path")
                    elif imp in ["Dict", "List", "Optional", "Tuple"]:
                        import_section.append(f"from typing import {imp}")
                    else:
                        import_section.append(f"import {imp}")

                # Insert imports after shebang and docstring
                lines = content.split("\n")
                insert_index = 0

                # Skip shebang
                if lines and lines[0].startswith("#!"):
                    insert_index = 1

                # Skip docstring
                while insert_index < len(lines) and (
                    lines[insert_index].strip().startswith("#")
                    or lines[insert_index].strip().startswith('"""')
                    or lines[insert_index].strip() == ""
                ):
                    insert_index += 1

                # Insert imports
                for imp in reversed(import_section):
                    lines.insert(insert_index, imp)

                content = "\n".join(lines)
                fixes_applied += len(import_section)

            # Fix 3: Fix common syntax issues
            content = re.sub(
                r"\bexcept Exception as e:\s*pass",
                'except Exception as e:\n    logging.warning(f"Error: {e}")',
                content,
            )

            # Fix 4: Add main guard if missing
            if "def main(" in content and 'if __name__ == "__main__"' not in content:
                content += '\n\nif __name__ == "__main__":\n    main()\n'
                fixes_applied += 1

            # Fix 5: Remove trailing whitespace
            lines = content.split("\n")
            cleaned_lines = [line.rstrip() for line in lines]
            content = "\n".join(cleaned_lines)

            # Only write if changes were made
            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

        except Exception as e:
            self.logger.warning(f"Failed to fix {file_path}: {e}")

        return fixes_applied

    def _detect_missing_imports(self, content: str) -> List[str]:
        """Detect commonly missing imports"""
        missing = []

        # Check for Path usage without import
        if "Path(" in content and "from pathlib import Path" not in content:
            missing.append("Path")

        # Check for typing imports
        typing_usage = ["Dict", "List", "Optional", "Tuple"]
        for typ in typing_usage:
            if f"{typ}[" in content and f"from typing import" not in content:
                missing.append(typ)

        # Check for common modules
        common_modules = {
            "asyncio": ["async def", "await "],
            "json": ["json."],
            "logging": ["logging."],
            "argparse": ["ArgumentParser"],
            "subprocess": ["subprocess."],
            "time": ["time.sleep", "time.time"],
            "platform": ["platform."],
            "re": ["re."],
        }

        for module, patterns in common_modules.items():
            if (
                any(pattern in content for pattern in patterns)
                and f"import {module}" not in content
            ):
                missing.append(module)

        return missing

    def install_dependencies(self):
        """Install all required dependencies"""
        print(f"\n{Colors.YELLOW}📦 INSTALLING DEPENDENCIES{Colors.END}")
        print(f"{Colors.CYAN}{'='*50}{Colors.END}")

        # Collect all requirements files
        req_files = list(self.workspace_root.rglob("requirements*.txt"))

        # Common packages that are often needed
        common_packages = [
            "fastapi",
            "uvicorn",
            "requests",
            "numpy",
            "pandas",
            "matplotlib",
            "jupyter",
            "notebook",
            "psutil",
            "prometheus-client",
            "watchdog",
            "pydantic",
            "aiofiles",
            "websockets",
        ]

        print(f"Found {len(req_files)} requirements files")

        # Install from requirements files
        for req_file in req_files:
            print(f"Installing from {req_file.relative_to(self.workspace_root)}...")
            try:
                subprocess.run(
                    [self.python_path, "-m", "pip", "install", "-r", str(req_file)],
                    check=True,
                    capture_output=True,
                )
                print(f"  ✅ Installed from {req_file.name}")
            except subprocess.CalledProcessError as e:
                print(f"  ⚠️ Failed to install from {req_file.name}: {e}")

        # Install common packages
        print("Installing common packages...")
        for package in common_packages:
            try:
                subprocess.run(
                    [self.python_path, "-m", "pip", "install", package],
                    check=True,
                    capture_output=True,
                )
                print(f"  ✅ {package}")
            except subprocess.CalledProcessError:
                print(f"  ⚠️ {package} (optional)")

        print(f"{Colors.GREEN}✅ Dependency installation completed{Colors.END}")

    def create_virtual_environment(self):
        """Create a virtual environment if it doesn't exist"""
        venv_path = self.workspace_root / "venv"

        if not venv_path.exists():
            print(f"\n{Colors.YELLOW}🌍 CREATING VIRTUAL ENVIRONMENT{Colors.END}")
            print(f"{Colors.CYAN}{'='*50}{Colors.END}")

            try:
                subprocess.run([
                    self.python_path, "-m", "venv", str(venv_path)
                ], check=True, capture_output=True)
                print(f"  ✅ Virtual environment created at {venv_path}")
            except subprocess.CalledProcessError as e:
                print(f"  ⚠️ Failed to create virtual environment: {e}")
                return

            # Update python path to use venv
            if platform.system() == "Windows":
                self.python_path = str(venv_path / "Scripts" / "python.exe")
            else:
                self.python_path = str(venv_path / "bin" / "python")

            print(f"Updated Python path: {self.python_path}")

        else:
            print(f"{Colors.GREEN}✅ Virtual environment already exists{Colors.END}")

    def run_script(self, script_info: Dict, args: List[str] = None):
        """Run a specific script"""
        script_path = script_info["path"]
        args = args or []

        print(
            f"\n{Colors.YELLOW}🚀 RUNNING: {script_info['relative_path']}{Colors.END}"
        )
        print(f"{Colors.BLUE}Description: {script_info['description']}{Colors.END}")

        try:
            if script_path.suffix == ".py":
                cmd = [self.python_path, str(script_path)] + args
            elif script_path.suffix == ".sh":
                cmd = ["bash", str(script_path)] + args
            else:
                print(f"{Colors.RED}❌ Unsupported script type{Colors.END}")
                return

            print(f"Command: {' '.join(cmd)}")
            print(f"{Colors.CYAN}{'-'*60}{Colors.END}")

            process = subprocess.Popen(cmd, cwd=script_path.parent, text=True)

            self.running_processes.append(
                {"process": process, "script": script_info, "start_time": time.time()}
            )

            process.wait()

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}⏸️ Script interrupted by user{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error running script: {e}{Colors.END}")

    def show_interactive_menu(self):
        """Show interactive menu for script selection"""
        while True:
            self._clear_screen()
            self.print_banner()

            print(f"{Colors.CYAN}📋 AVAILABLE SCRIPTS BY CATEGORY{Colors.END}\n")

            all_scripts = []
            current_index = 1

            for category, scripts in self.available_scripts.items():
                if not scripts:
                    continue

                print(
                    f"{Colors.BOLD}{Colors.MAGENTA}{category.upper().replace('_', ' ')}:{Colors.END}"
                )

                for script in scripts:
                    status = "✅" if script["can_run"] else "⚠️"
                    print(f"  {current_index:2d}. {status} {script['relative_path']}")
                    print(f"      {Colors.BLUE}{script['description']}{Colors.END}")
                    all_scripts.append(script)
                    current_index += 1

                print()

            print(f"{Colors.YELLOW}SPECIAL COMMANDS:{Colors.END}")
            special_start = current_index
            print(f"  {current_index}. 🔧 Fix all files")
            print(f"  {current_index + 1}. 📦 Install dependencies")
            print(f"  {current_index + 2}. 🌍 Create virtual environment")
            print(f"  {current_index + 3}. 📊 Show running processes")
            print(f"  {current_index + 4}. 🛑 Stop all processes")
            print(f"  {current_index + 5}. 🔄 Refresh script list")
            print(f"  {current_index + 6}. ❌ Exit")

            try:
                choice = input(
                    f"\n{Colors.GREEN}Enter your choice (1-{current_index + 6}): {Colors.END}"
                ).strip()

                if not choice.isdigit():
                    continue

                choice_num = int(choice)

                if 1 <= choice_num <= len(all_scripts):
                    script = all_scripts[choice_num - 1]

                    # Get additional arguments
                    args_input = input(
                        f"{Colors.YELLOW}Enter arguments (or press Enter for none): {Colors.END}"
                    ).strip()
                    args = args_input.split() if args_input else []

                    self.run_script(script, args)
                    input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.END}")

                elif choice_num == special_start:
                    self.fix_all_files()
                    input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.END}")

                elif choice_num == special_start + 1:
                    self.install_dependencies()
                    input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.END}")

                elif choice_num == special_start + 2:
                    self.create_virtual_environment()
                    input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.END}")

                elif choice_num == special_start + 3:
                    self.show_running_processes()
                    input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.END}")

                elif choice_num == special_start + 4:
                    self.stop_all_processes()
                    input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.END}")

                elif choice_num == special_start + 5:
                    self.discover_all_scripts()

                elif choice_num == special_start + 6:
                    break

            except KeyboardInterrupt:
                break
            except ValueError:
                continue

    def show_running_processes(self):
        """Show currently running processes"""
        print(f"\n{Colors.CYAN}📊 RUNNING PROCESSES{Colors.END}")
        print(f"{Colors.CYAN}{'='*50}{Colors.END}")

        if not self.running_processes:
            print("No processes currently running.")
            return

        for i, proc_info in enumerate(self.running_processes, 1):
            process = proc_info["process"]
            script = proc_info["script"]
            start_time = proc_info["start_time"]
            runtime = time.time() - start_time

            status = "🟢 Running" if process.poll() is None else "🔴 Stopped"
            print(f"{i}. {status} - {script['relative_path']}")
            print(f"   Runtime: {runtime:.1f}s | PID: {process.pid}")

    def stop_all_processes(self):
        """Stop all running processes"""
        print(f"\n{Colors.YELLOW}🛑 STOPPING ALL PROCESSES{Colors.END}")

        for proc_info in self.running_processes:
            process = proc_info["process"]
            script = proc_info["script"]

            if process.poll() is None:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    print(f"✅ Stopped {script['relative_path']}")
                except subprocess.TimeoutExpired:
                    process.kill()
                    print(f"🔴 Force killed {script['relative_path']}")
                except Exception as e:
                    print(f"❌ Error stopping {script['relative_path']}: {e}")

        self.running_processes.clear()
        print(f"{Colors.GREEN}✅ All processes stopped{Colors.END}")

    def _clear_screen(self):
        """Clear the terminal screen"""
        os.system("cls" if platform.system() == "Windows" else "clear")

    def create_startup_scripts(self):
        """Create convenient startup scripts"""
        print(f"\n{Colors.YELLOW}📝 CREATING STARTUP SCRIPTS{Colors.END}")

        # Create Windows batch file
        bat_file = self.workspace_root / "launch.bat"
        with open(bat_file, "w") as f:
            f.write(f"@echo off\n")
            f.write(f'cd /d "{self.workspace_root}"\n')
            f.write(f"python unified_launcher.py\n")
            f.write(f"pause\n")
        print(f"✅ Created {bat_file}")

        # Create shell script
        sh_file = self.workspace_root / "launch"
        with open(sh_file, "w") as f:
            f.write(f"#!/bin/bash\n")
            f.write(f'cd "{self.workspace_root}"\n')
            f.write(f'python3 unified_launcher.py "$@"\n')

        # Make executable
        try:
            os.chmod(sh_file, 0o755)
            print(f"✅ Created {sh_file}")
        except Exception as e:
            print(f"⚠️ Created {sh_file} but couldn't make executable: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Unified Launcher for Semantic Kernel Workspace"
    )
    parser.add_argument("--fix", action="store_true", help="Fix all files and exit")
    parser.add_argument(
        "--setup", action="store_true", help="Setup environment and exit"
    )
    parser.add_argument(
        "--install", action="store_true", help="Install dependencies and exit"
    )
    parser.add_argument("--script", help="Run specific script by name")
    parser.add_argument("--category", help="List scripts in specific category")
    parser.add_argument("--list", action="store_true", help="List all scripts and exit")
    parser.add_argument("--args", nargs="*", help="Arguments to pass to the script")

    args = parser.parse_args()

    # Create launcher
    launcher = UnifiedLauncher()

    # Setup signal handlers
    import signal

    def signal_handler(sig, frame):
        print(f"\n{Colors.YELLOW}Shutting down...{Colors.END}")
        launcher.stop_all_processes()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Always discover scripts first
    launcher.discover_all_scripts()

    try:
        if args.fix:
            launcher.fix_all_files()

        elif args.setup:
            launcher.create_virtual_environment()
            launcher.install_dependencies()
            launcher.fix_all_files()
            launcher.create_startup_scripts()

        elif args.install:
            launcher.install_dependencies()

        elif args.list:
            print(f"\n{Colors.CYAN}📋 AVAILABLE SCRIPTS:{Colors.END}\n")
            for category, scripts in launcher.available_scripts.items():
                if scripts:
                    print(
                        f"{Colors.BOLD}{category.upper().replace('_', ' ')}:{Colors.END}"
                    )
                    for script in scripts:
                        status = "✅" if script["can_run"] else "⚠️"
                        print(f"  {status} {script['relative_path']}")
                        print(f"     {Colors.BLUE}{script['description']}{Colors.END}")
                    print()

        elif args.script:
            # Find and run specific script
            script_found = False
            for category, scripts in launcher.available_scripts.items():
                for script in scripts:
                    if (
                        args.script in str(script["relative_path"])
                        or args.script in script["path"].name
                    ):
                        launcher.run_script(script, args.args or [])
                        script_found = True
                        break
                if script_found:
                    break

            if not script_found:
                print(f"{Colors.RED}Script '{args.script}' not found{Colors.END}")

        elif args.category:
            # List scripts in specific category
            category = args.category.lower().replace(" ", "_")
            if category in launcher.available_scripts:
                scripts = launcher.available_scripts[category]
                print(
                    f"\n{Colors.CYAN}📋 {category.upper().replace('_', ' ')} SCRIPTS:{Colors.END}\n"
                )
                for script in scripts:
                    status = "✅" if script["can_run"] else "⚠️"
                    print(f"  {status} {script['relative_path']}")
                    print(f"     {Colors.BLUE}{script['description']}{Colors.END}")
            else:
                print(f"{Colors.RED}Category '{args.category}' not found{Colors.END}")

        else:
            # Interactive mode
            launcher.show_interactive_menu()

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        return 1
    finally:
        launcher.stop_all_processes()

    return 0


if __name__ == "__main__":
    sys.exit(main())
