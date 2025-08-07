#!/usr/bin/env python3
"""
🚀 Semantic Kernel Workspace Quick Setup
Complete environment configuration for all capabilities

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"  ✅ Success")
            return True
        else:
            print(f"  ⚠️ Warning: {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def check_tool(tool_name):
    """Check if a tool is available"""
    return shutil.which(tool_name) is not None

def main():
    """Main setup function"""
    workspace_root = Path("/workspaces/semantic-kernel")

    print_header("SEMANTIC KERNEL WORKSPACE SETUP")
    print(f"📁 Workspace: {workspace_root}")
    print(f"🐍 Python: {sys.version}")

    # 1. 🔍 EXPLORE - Workspace Structure Check
    print_header("1. EXPLORE - Workspace Structure")

    key_dirs = [
        "01-core-implementations",
        "02-ai-workspace",
        "09-agi-development",
        "13-testing"
    ]

    print("📁 Checking key directories:")
    for dir_name in key_dirs:
        dir_path = workspace_root / dir_name
        status = "✅" if dir_path.exists() else "❌"
        print(f"  {status} {dir_name}")

    # 2. 🏗️ SETUP - Development Environment
    print_header("2. SETUP - Development Environment")

    # Check essential tools
    tools = ["git", "docker", "python3", "pip"]
    print("🛠️ Checking tools:")
    for tool in tools:
        status = "✅" if check_tool(tool) else "❌"
        print(f"  {status} {tool}")

    # Install essential Python packages
    essential_packages = [
        "semantic-kernel",
        "openai",
        "jupyter",
        "ipykernel",
        "notebook",
        "numpy",
        "pandas",
        "matplotlib",
        "requests",
        "aiohttp"
    ]

    print("\n📦 Installing essential packages:")
    for package in essential_packages:
        cmd = f"{sys.executable} -m pip install {package} --quiet"
        success = run_command(cmd, f"Installing {package}")
        if not success:
            print(f"    💡 You may need to install {package} manually")

    # 3. 📓 NOTEBOOKS - Jupyter Setup
    print_header("3. NOTEBOOKS - Jupyter Configuration")

    # Install Jupyter kernel
    kernel_cmd = f"{sys.executable} -m ipykernel install --user --name semantic-kernel"
    run_command(kernel_cmd, "Installing Jupyter kernel")

    # Check for existing notebooks
    notebooks = list(workspace_root.glob("**/*.ipynb"))
    print(f"📓 Found {len(notebooks)} Jupyter notebooks")

    # 4. 🧪 BUILD & TEST - Environment Check
    print_header("4. BUILD & TEST - Environment Check")

    # Check Python environment
    print("🐍 Python environment check:")
    try:
        import semantic_kernel as sk
        print("  ✅ Semantic Kernel imported successfully")
    except ImportError:
        print("  ⚠️ Semantic Kernel not available - may need manual installation")

    # Find test files
    test_files = list(workspace_root.glob("**/test_*.py"))
    print(f"🧪 Found {len(test_files)} test files")

    # 5. 🚀 DEPLOY - Docker Check
    print_header("5. DEPLOY - Docker Configuration")

    docker_files = ["Dockerfile", "docker-compose.yml", "docker-compose.dev.yml"]
    print("🐳 Docker configuration:")
    for docker_file in docker_files:
        matches = list(workspace_root.glob(f"**/{docker_file}"))
        print(f"  {docker_file}: {len(matches)} found")

    if check_tool("docker"):
        print("  ✅ Docker CLI available")
        # Check if Docker daemon is running
        run_command("docker info", "Checking Docker daemon")
    else:
        print("  ❌ Docker not available")

    # 6. 📊 ANALYZE - Codebase Overview
    print_header("6. ANALYZE - Codebase Overview")

    file_types = {".py": 0, ".md": 0, ".json": 0, ".yml": 0, ".cs": 0, ".java": 0}

    print("📊 Analyzing file types...")
    for file_path in workspace_root.rglob("*"):
        if file_path.is_file():
            suffix = file_path.suffix.lower()
            if suffix in file_types:
                file_types[suffix] += 1

    for ext, count in file_types.items():
        if count > 0:
            print(f"  {ext}: {count} files")

    # 7. 🤖 AI MODELS - Framework Check
    print_header("7. AI MODELS - Framework Check")

    ai_frameworks = ["torch", "tensorflow", "transformers", "huggingface_hub"]
    print("🤖 AI framework availability:")
    for framework in ai_frameworks:
        try:
            __import__(framework)
            print(f"  ✅ {framework}")
        except ImportError:
            print(f"  ❌ {framework} (optional)")

    # Check for GPU
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        print(f"  🎮 CUDA: {'✅ Available' if cuda_available else '❌ Not available'}")
    except:
        print("  🎮 CUDA: Cannot check (PyTorch not available)")

    # Final Summary
    print_header("SETUP COMPLETE!")

    print("🎉 Your Semantic Kernel workspace is ready!")
    print("\n🚀 NEXT STEPS:")
    print("  1. Open the Semantic_Kernel_Workspace_Explorer.ipynb notebook")
    print("  2. Run the cells to explore your workspace")
    print("  3. Try: python unified_launcher.py")
    print("  4. Navigate to: cd 02-ai-workspace && python ai_workspace_control.py")
    print("  5. Start Jupyter: jupyter lab")

    print("\n📚 KEY FILES CREATED:")
    print("  📄 Semantic_Kernel_Workspace_Explorer.ipynb - Main exploration notebook")
    print("  📄 workspace_quick_setup.py - This setup script")

    print("\n💡 TIPS:")
    print("  - Use the notebook for interactive exploration")
    print("  - Check the README.md files for detailed documentation")
    print("  - Use the unified launcher for centralized access")

    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✨ Setup completed successfully!")
            sys.exit(0)
        else:
            print("\n⚠️ Setup completed with warnings.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
