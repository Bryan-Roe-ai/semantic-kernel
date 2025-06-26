#!/usr/bin/env python3
#!/usr/bin/env python3
"""
Master Launcher for Semantic Kernel Workspace

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT

This script fixes all files and makes everything runnable from one place.
"""

import os
import sys
import subprocess
import argparse
import time
import json
import platform
from pathlib import Path
from typing import Dict, List
import logging

# Add workspace to Python path
WORKSPACE_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(WORKSPACE_ROOT))

# ANSI colors for terminal output


class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class MasterLauncher:
    """Unified launcher for all workspace functionality"""
    
    def __init__(self):
        self.workspace_root = WORKSPACE_ROOT
        self.python_path = sys.executable
        self.running_processes = []
        self.available_scripts = {}
        self.config = self._load_config()
        
        # Setup logging
        log_dir = self.workspace_root / "logs"
        log_dir.mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "master_launcher.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("MasterLauncher")
        
    def _load_config(self) -> Dict:
        """Load configuration for the launcher"""
        config_file = self.workspace_root / "launcher_config.json"
        default_config = {
            "auto_fix_files": True,
            "preferred_python": sys.executable,
            "startup_scripts": [],
            "environment_vars": {},
            "aliases": {}
        }
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return {**default_config, **json.load(f)}
            except Exception as e:
                self.logger.warning(f"Failed to load config: {e}")
        
        return default_config
    
    def discover_scripts(self):
        """Discover all runnable scripts in the workspace"""
        self.logger.info("Discovering runnable scripts...")
        
        # Common script patterns
        script_patterns = [
            "**/*launcher*.py",
            "**/*main*.py", 
            "**/__main__.py",
            "**/launch*.py",
            "**/start*.py",
            "**/setup*.py",
            "**/run*.py"
        ]
        
        # Script categories
        categories = {
            "core": [],
            "demos": [],
            "tools": [],
            "servers": [],
            "tests": [],
            "automation": [],
            "monitoring": [],
            "setup": []
        }
        
        for pattern in script_patterns:
            for script_path in self.workspace_root.glob(pattern):
                if script_path.is_file() and script_path.suffix == '.py':
                    # Skip __pycache__ and other temporary files
                    path_str = str(script_path)
                    if '__pycache__' in path_str or script_path.name.startswith('.'):
                        continue
                        
                    # Categorize script
                    category = self._categorize_script(script_path)
                    rel_path = script_path.relative_to(self.workspace_root)
                    
                    script_info = {
                        'path': script_path,
                        'relative_path': rel_path,
                        'category': category,
                        'description': self._get_script_description(
                            script_path),
                        'working_dir': script_path.parent,
                        'can_run': self._check_script_runnable(script_path)
                    }
                    
                    categories[category].append(script_info)
                    
        self.available_scripts = categories
        
        total_scripts = sum(len(scripts) for scripts in categories.values())
        self.logger.info(
            f"Discovered {total_scripts} scripts across "
            f"{len(categories)} categories")
        
    def _categorize_script(self, script_path: Path) -> str:
        """Categorize a script based on its path and name"""
        path_str = str(script_path).lower()
        name = script_path.name.lower()
        
        if 'test' in path_str or 'test' in name:
            return 'tests'
        elif 'demo' in path_str or 'demo' in name or 'example' in path_str:
            return 'demos'
        elif 'server' in name or 'backend' in name or 'api' in name:
            return 'servers'
        elif 'monitor' in name or 'dashboard' in name or 'status' in name:
            return 'monitoring'
        elif 'setup' in name or 'install' in name or 'config' in name:
            return 'setup'
        elif 'automation' in path_str or 'scripts' in path_str:
            return 'automation'
        elif any(core_dir in path_str for core_dir in [
                '01-core', 'python/semantic_kernel']):
            return 'core'
        else:
            return 'tools'
    
    def _get_script_description(self, script_path: Path) -> str:
        """Extract description from script docstring or comments"""
        try:
            with open(script_path, 'r', encoding='utf-8',
                      errors='ignore') as f:
                content = f.read(500)  # Read first 500 chars
                
            # Look for docstring
            lines = content.split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith('"""') or line.startswith("'''"):
                    # Multi-line docstring
                    for j in range(i+1, min(i+5, len(lines))):
                        desc_line = lines[j].strip()
                        if desc_line and not desc_line.startswith(('"""', "'''", '#', 'Copyright', 'License')):
                            return desc_line[:80]
                elif line.startswith('#') and not line.startswith('#!/'):
                    # Comment description
                    desc = line[1:].strip()
                    if len(desc) > 10 and not desc.startswith(('filepath:', 'Copyright', 'License')):
                        return desc[:80]
                        
        except Exception:
            pass
            
        return f"Script: {script_path.name}"
    
    def _check_script_runnable(self, script_path: Path) -> bool:
        """Check if a script can be run (has main function, etc.)"""
        try:
            with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Look for main function or __main__ block
            has_main = (
                'def main(' in content or 
                'if __name__ == "__main__"' in content or
                'async def main(' in content or
                'class ' in content  # Class-based scripts
            )
            
            return has_main
            
        except Exception:
            return False
    
    def fix_all_files(self):
        """Fix common issues in Python files"""
        if not self.config.get('auto_fix_files', True):
            return
            
        self.logger.info("Fixing common issues in Python files...")
        
        fixes_applied = 0
        
        # Find all Python files
        for py_file in self.workspace_root.rglob("*.py"):
            if '__pycache__' in str(py_file) or py_file.name.startswith('.'):
                continue
                
            try:
                fixes_applied += self._fix_file(py_file)
            except Exception as e:
                self.logger.warning(f"Failed to fix {py_file}: {e}")
        
        self.logger.info(f"Applied {fixes_applied} fixes to Python files")
    
    def _fix_file(self, file_path: Path) -> int:
        """Fix common issues in a specific Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            original_content = content
            fixes = 0
            
            # Fix 1: Remove duplicate if __name__ == "__main__" blocks
            if main_blocks > 1:
                # Keep only the last one
                lines = content.split('\n')
                new_lines = []
                main_found = False
                
                for line in reversed(lines):
                        main_found = True
                        new_lines.append(line)
                        # Skip duplicate
                        continue
                    else:
                        new_lines.append(line)
                
                content = '\n'.join(reversed(new_lines))
                fixes += 1
            
            # Fix 2: Add missing imports
            missing_imports = self._detect_missing_imports(content)
            if missing_imports:
                import_section = '\n'.join(missing_imports)
                # Insert after existing imports
                lines = content.split('\n')
                import_end = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith(('import ', 'from ')):
                        import_end = i + 1
                
                lines.insert(import_end, import_section)
                content = '\n'.join(lines)
                fixes += 1
            
            # Fix 3: Fix path issues
            if 'sys.path.insert' not in content and 'Path(__file__).parent' in content:
                # Add sys import if needed
                if 'import sys' not in content:
                    content = 'import sys\n' + content
                    fixes += 1
            
            # Fix 4: Add shebang if missing
            if not content.startswith('#!') and file_path.name in ['main.py', 'launcher.py'] or 'launcher' in file_path.name:
                content = '#!/usr/bin/env python3\n' + content
                fixes += 1
            
            # Write back if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Make executable on Unix-like systems
                if platform.system() != 'Windows':
                    os.chmod(file_path, 0o755)
                    
            return fixes
            
        except Exception as e:
            self.logger.warning(f"Error fixing {file_path}: {e}")
            return 0
    
    def _detect_missing_imports(self, content: str) -> List[str]:
        """Detect commonly missing imports"""
        missing = []
        
        # Common missing imports
        if 'asyncio.' in content and 'import asyncio' not in content:
            missing.append('import asyncio')
        if 'json.' in content and 'import json' not in content:
            missing.append('import json')
        if 'Path(' in content and 'from pathlib import Path' not in content:
            missing.append('from pathlib import Path')
        if 'logging.' in content and 'import logging' not in content:
            missing.append('import logging')
        if 'subprocess.' in content and 'import subprocess' not in content:
            missing.append('import subprocess')
        if 'argparse.' in content and 'import argparse' not in content:
            missing.append('import argparse')
        if 'time.sleep' in content and 'import time' not in content:
            missing.append('import time')
        
        return missing
    
    def create_environment(self):
        """Create and setup the environment"""
        self.logger.info("Setting up environment...")
        
        # Create necessary directories
        dirs_to_create = [
            "logs",
            "temp", 
            "uploads",
            "plugins",
            ".automode_state",
            "config"
        ]
        
        for dir_name in dirs_to_create:
            dir_path = self.workspace_root / dir_name
            dir_path.mkdir(exist_ok=True)
            
        # Install common requirements
        self._install_requirements()
        
        # Set environment variables
        for key, value in self.config.get('environment_vars', {}).items():
            os.environ[key] = value
            
    def _install_requirements(self):
        """Install common Python packages"""
        common_packages = [
            'asyncio',
            'requests', 
            'fastapi',
            'uvicorn',
            'psutil',
            'watchdog',
            'aiofiles',
            'pydantic'
        ]
        
        optional_packages = [
            'prometheus-client',
            'redis',
            'streamlit',
            'gradio'
        ]
        
        # Install required packages
        for package in common_packages:
            try:
                subprocess.run([
                    self.python_path, '-m', 'pip', 'install', package, '--quiet'
                ], check=False, capture_output=True)
            except Exception:
                pass
                
        # Try to install optional packages
        for package in optional_packages:
            try:
                subprocess.run([
                    self.python_path, '-m', 'pip', 'install', package, '--quiet'
                ], check=False, capture_output=True)
            except Exception:
                pass
    
    def run_script(self, script_info: Dict, args: List[str] = None) -> subprocess.Popen:
        """Run a specific script"""
        script_path = script_info['path']
        working_dir = script_info['working_dir']
        
        cmd = [self.python_path, str(script_path)]
        if args:
            cmd.extend(args)
            
        self.logger.info(f"Running: {' '.join(cmd)} (in {working_dir})")
        
        try:
            process = subprocess.Popen(
                cmd,
                cwd=working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            self.running_processes.append({
                'process': process,
                'script': script_info,
                'start_time': time.time()
            })
            
            return process
            
        except Exception as e:
            self.logger.error(f"Failed to run {script_path}: {e}")
            return None
    
    def show_interactive_menu(self):
        """Show interactive menu for script selection"""
        while True:
            self._clear_screen()
            self._print_banner()
            
            print(f"\n{Colors.CYAN}📁 Available Scripts by Category:{Colors.END}\n")
            
            all_scripts = []
            category_start = {}
            current_index = 1
            
            for category, scripts in self.available_scripts.items():
                if not scripts:
                    continue
                    
                print(f"{Colors.BOLD}{category.upper()}:{Colors.END}")
                category_start[category] = current_index
                
                for script in scripts:
                    status = "✅" if script['can_run'] else "⚠️"
                    print(f"  {current_index:2d}. {status} {script['relative_path']}")
                    print(f"      {Colors.BLUE}{script['description']}{Colors.END}")
                    all_scripts.append(script)
                    current_index += 1
                    
                print()
            
            print(f"{Colors.YELLOW}Special Commands:{Colors.END}")
            print(f"  {current_index}. 🔧 Fix all files")
            print(f"  {current_index + 1}. 🌍 Setup environment") 
            print(f"  {current_index + 2}. 📊 Show running processes")
            print(f"  {current_index + 3}. 🛑 Stop all processes")
            print(f"  {current_index + 4}. 🔄 Refresh script list")
            print(f"  {current_index + 5}. ❌ Exit")
            
            try:
                choice = input(f"\n{Colors.GREEN}Enter your choice (1-{current_index + 5}): {Colors.END}").strip()
                
                if not choice.isdigit():
                    continue
                    
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(all_scripts):
                    script = all_scripts[choice_num - 1]
                    
                    # Get additional arguments
                    args_input = input(f"{Colors.YELLOW}Enter arguments (or press Enter for none): {Colors.END}").strip()
                    args = args_input.split() if args_input else []
                    
                    self.run_script(script, args)
                    input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.END}")
                    
                elif choice_num == current_index:
                    self.fix_all_files()
                    input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.END}")
                    
                elif choice_num == current_index + 1:
                    self.create_environment()
                    input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.END}")
                    
                elif choice_num == current_index + 2:
                    self.show_running_processes()
                    input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.END}")
                    
                elif choice_num == current_index + 3:
                    self.stop_all_processes()
                    input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.END}")
                    
                elif choice_num == current_index + 4:
                    self.discover_scripts()
                    
                elif choice_num == current_index + 5:
                    break
                    
            except KeyboardInterrupt:
                break
            except ValueError:
                continue
    
    def show_running_processes(self):
        """Show currently running processes"""
        print(f"\n{Colors.CYAN}🔄 Running Processes:{Colors.END}\n")
        
        if not self.running_processes:
            print("No processes currently running.")
            return
            
        for i, proc_info in enumerate(self.running_processes):
            process = proc_info['process']
            script = proc_info['script']
            start_time = proc_info['start_time']
            
            status = "Running" if process.poll() is None else "Stopped"
            runtime = time.time() - start_time
            
            print(f"{i+1}. {script['relative_path']}")
            print(f"   Status: {status} | Runtime: {runtime:.1f}s | PID: {process.pid}")
    
    def stop_all_processes(self):
        """Stop all running processes"""
        print(f"\n{Colors.YELLOW}🛑 Stopping all processes...{Colors.END}")
        
        for proc_info in self.running_processes:
            process = proc_info['process']
            if process.poll() is None:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except Exception:
                    try:
                        process.kill()
                    except Exception:
                        pass
        
        self.running_processes.clear()
        print("All processes stopped.")
    
    def _clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if platform.system() == 'Windows' else 'clear')
    
    def _print_banner(self):
        """Print the application banner"""
        print(f"{Colors.BOLD}{Colors.BLUE}")
        print("=" * 60)
        print("      🚀 SEMANTIC KERNEL MASTER LAUNCHER 🚀")
        print("=" * 60)
        print(f"{Colors.END}")
        print(f"{Colors.GREEN}Workspace: {self.workspace_root}{Colors.END}")
        print(f"{Colors.BLUE}Python: {self.python_path}{Colors.END}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Master Launcher for Semantic Kernel Workspace")
    parser.add_argument("--script", help="Run specific script by name")
    parser.add_argument("--category", help="List scripts in specific category")
    parser.add_argument("--fix", action="store_true", help="Fix all files and exit")
    parser.add_argument("--setup", action="store_true", help="Setup environment and exit")
    parser.add_argument("--list", action="store_true", help="List all scripts and exit")
    parser.add_argument("--args", nargs="*", help="Arguments to pass to the script")
    
    args = parser.parse_args()
    
    # Create launcher
    launcher = MasterLauncher()
    
    # Setup signal handlers
    import signal
    
    def signal_handler(sig, frame):
        print(f"\n{Colors.YELLOW}Shutting down...{Colors.END}")
        launcher.stop_all_processes()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Discover scripts
    launcher.discover_scripts()
    
    try:
        if args.fix:
            launcher.fix_all_files()
            
        elif args.setup:
            launcher.create_environment()
            
        elif args.list:
            print(f"\n{Colors.CYAN}📋 Available Scripts:{Colors.END}\n")
            for category, scripts in launcher.available_scripts.items():
                if scripts:
                    print(f"{Colors.BOLD}{category.upper()}:{Colors.END}")
                    for script in scripts:
                        status = "✅" if script['can_run'] else "⚠️"
                        print(f"  {status} {script['relative_path']}")
                        print(f"     {Colors.BLUE}{script['description']}{Colors.END}")
                    print()
                    
        elif args.script:
            # Find and run specific script
            script_found = False
            for category, scripts in launcher.available_scripts.items():
                for script in scripts:
                    if args.script in str(script['relative_path']) or args.script in script['path'].name:
                        launcher.run_script(script, args.args or [])
                        script_found = True
                        break
                if script_found:
                    break
            
            if not script_found:
                print(f"{Colors.RED}Script '{args.script}' not found{Colors.END}")
                
        elif args.category:
            # List scripts in specific category
            category = args.category.lower()
            if category in launcher.available_scripts:
                scripts = launcher.available_scripts[category]
                print(f"\n{Colors.CYAN}📋 {category.upper()} Scripts:{Colors.END}\n")
                for script in scripts:
                    status = "✅" if script['can_run'] else "⚠️"
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
